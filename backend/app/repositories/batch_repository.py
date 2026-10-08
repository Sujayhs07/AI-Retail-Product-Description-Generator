from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.batch import BatchJob, BatchItem

class BatchRepository:
    @staticmethod
    def create_job(db: Session, file_name: str, file_type: str, total_products: int) -> BatchJob:
        job = BatchJob(
            file_name=file_name,
            file_type=file_type,
            total_products=total_products,
            processed_products=0,
            successful_products=0,
            failed_products=0,
            status="pending"
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    @staticmethod
    def add_item(
        db: Session,
        batch_job_id: int,
        row_number: int,
        product_id: Optional[int] = None,
        status: str = "pending",
        error_message: Optional[str] = None
    ) -> BatchItem:
        item = BatchItem(
            batch_job_id=batch_job_id,
            row_number=row_number,
            product_id=product_id,
            status=status,
            error_message=error_message
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def get_job(db: Session, batch_id: int) -> Optional[BatchJob]:
        return db.query(BatchJob).filter(BatchJob.id == batch_id).first()

    @staticmethod
    def get_items_by_job(db: Session, batch_id: int) -> List[BatchItem]:
        return db.query(BatchItem).filter(BatchItem.batch_job_id == batch_id).order_by(BatchItem.row_number.asc()).all()
