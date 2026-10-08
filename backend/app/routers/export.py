from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.export import ContentExporter

router = APIRouter(prefix="/api/export", tags=["Export"])

@router.get("/products.csv")
def export_products_csv(db: Session = Depends(get_db)):
    data = ContentExporter.prepare_export_data(db)
    csv_content = ContentExporter.to_csv_string(data)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=catalogcraft_products.csv"}
    )

@router.get("/products.json")
def export_products_json(db: Session = Depends(get_db)):
    data = ContentExporter.prepare_export_data(db)
    json_content = ContentExporter.to_json_string(data)
    return Response(
        content=json_content,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=catalogcraft_products.json"}
    )

@router.get("/batch/{batch_id}.csv")
def export_batch_csv(batch_id: int, db: Session = Depends(get_db)):
    data = ContentExporter.prepare_export_data(db, batch_job_id=batch_id)
    csv_content = ContentExporter.to_csv_string(data)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=batch_{batch_id}_export.csv"}
    )

@router.get("/batch/{batch_id}.json")
def export_batch_json(batch_id: int, db: Session = Depends(get_db)):
    data = ContentExporter.prepare_export_data(db, batch_job_id=batch_id)
    json_content = ContentExporter.to_json_string(data)
    return Response(
        content=json_content,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=batch_{batch_id}_export.json"}
    )
