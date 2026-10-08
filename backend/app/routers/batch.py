import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product, BatchJob, BatchItem
from app.repositories import BatchRepository, SettingsRepository, ProductRepository
from app.schemas.product import ProductCreate
from app.schemas.batch import BatchJobResponse, BatchItemResponse, BatchGenerateRequest
from app.services.batch import BatchProcessor

router = APIRouter(prefix="/api/batch", tags=["Batch Processing"])

@router.post("/upload", response_model=BatchJobResponse, status_code=status.HTTP_201_CREATED)
async def upload_batch_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    filename = file.filename or "uploaded_file"
    file_ext = filename.split(".")[-1].lower()

    if file_ext not in ["csv", "json"]:
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV and JSON files are supported.")

    content = await file.read()
    valid_rows, invalid_rows = BatchProcessor.parse_file(content, file_ext)

    total_count = len(valid_rows) + len(invalid_rows)
    if total_count == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty or could not be parsed.")

    # Create BatchJob
    job = BatchRepository.create_job(db, filename, file_ext, total_count)

    # Process invalid rows first
    for inv in invalid_rows:
        BatchRepository.add_item(
            db, batch_job_id=job.id, row_number=inv["row_number"], status="failed", error_message=inv["error"]
        )
        job.failed_products += 1
        job.processed_products += 1

    # Create products & batch items for valid rows
    for row in valid_rows:
        try:
            row_num = row.pop("row_number", 0)
            prod_create = ProductCreate(**row)
            db_product = ProductRepository.create(db, prod_create)
            
            BatchRepository.add_item(
                db, batch_job_id=job.id, row_number=row_num, product_id=db_product.id, status="pending"
            )
        except Exception as e:
            BatchRepository.add_item(
                db, batch_job_id=job.id, row_number=row.get("row_number", 0), status="failed", error_message=str(e)
            )
            job.failed_products += 1
            job.processed_products += 1

    db.commit()
    db.refresh(job)
    return job

@router.get("/{batch_id}", response_model=BatchJobResponse)
def get_batch_job(batch_id: int, db: Session = Depends(get_db)):
    job = BatchRepository.get_job(db, batch_id)
    if not job:
        raise HTTPException(status_code=404, detail="Batch job not found")
    return job

@router.post("/{batch_id}/generate")
def start_batch_generation(
    batch_id: int,
    req: BatchGenerateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    job = BatchRepository.get_job(db, batch_id)
    if not job:
        raise HTTPException(status_code=404, detail="Batch job not found")

    brand_settings_db = SettingsRepository.get_settings(db)
    brand_settings = SettingsRepository.to_schema(brand_settings_db)

    # Process synchronously for demo or background task
    BatchProcessor.process_batch(
        db=db,
        batch_job=job,
        brand_settings=brand_settings,
        tone=req.tone or "Professional",
        language=req.language or "English",
        word_count_preference=req.word_count_preference or "Medium"
    )

    return {"message": "Batch generation initiated successfully", "batch_id": batch_id, "status": job.status}

@router.post("/{batch_id}/retry-failed")
def retry_failed_batch_items(batch_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job = BatchRepository.get_job(db, batch_id)
    if not job:
        raise HTTPException(status_code=404, detail="Batch job not found")

    failed_items = db.query(BatchItem).filter(
        BatchItem.batch_job_id == batch_id, BatchItem.status == "failed", BatchItem.product_id.isnot(None)
    ).all()

    for item in failed_items:
        item.status = "pending"
        item.error_message = None
        job.failed_products -= 1
        job.processed_products -= 1

    db.commit()

    brand_settings_db = SettingsRepository.get_settings(db)
    brand_settings = SettingsRepository.to_schema(brand_settings_db)

    BatchProcessor.process_batch(
        db=db, batch_job=job, brand_settings=brand_settings
    )

    return {"message": "Retrying failed batch items", "batch_id": batch_id}

@router.get("/{batch_id}/results")
def get_batch_results(batch_id: int, db: Session = Depends(get_db)):
    job = BatchRepository.get_job(db, batch_id)
    if not job:
        raise HTTPException(status_code=404, detail="Batch job not found")

    items = BatchRepository.get_items_by_job(db, batch_id)
    results = []

    for item in items:
        prod_data = None
        gen_data = None
        if item.product_id:
            p = ProductRepository.get_by_id(db, item.product_id)
            if p:
                prod_data = ProductRepository.to_dict(p)
        if item.generated_content_id:
            from app.repositories import ContentRepository
            c = ContentRepository.get_by_id(db, item.generated_content_id)
            if c:
                gen_data = ProductRepository.content_to_dict(c)

        results.append({
            "item": {
                "id": item.id,
                "row_number": item.row_number,
                "status": item.status,
                "error_message": item.error_message,
            },
            "product": prod_data,
            "generated_content": gen_data
        })

    return {
        "job": {
            "id": job.id,
            "file_name": job.file_name,
            "total": job.total_products,
            "processed": job.processed_products,
            "successful": job.successful_products,
            "failed": job.failed_products,
            "status": job.status
        },
        "results": results
    }
