import json
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from app.models import GeneratedContent, ContentVersion

class ContentRepository:
    @staticmethod
    def get_by_id(db: Session, content_id: int) -> Optional[GeneratedContent]:
        return db.query(GeneratedContent).filter(GeneratedContent.id == content_id).first()

    @staticmethod
    def get_by_product_id(db: Session, product_id: int) -> Optional[GeneratedContent]:
        return db.query(GeneratedContent).filter(GeneratedContent.product_id == product_id).first()

    @staticmethod
    def create_version(
        db: Session,
        content: GeneratedContent,
        changed_by: str = "System",
        change_type: str = "Generated"
    ) -> ContentVersion:
        current_versions = db.query(ContentVersion).filter(
            ContentVersion.generated_content_id == content.id
        ).count()

        snapshot = {
            "title": content.title,
            "short_description": content.short_description,
            "full_description": content.full_description,
            "highlights": json.loads(content.highlights) if content.highlights else [],
            "meta_title": content.meta_title,
            "meta_description": content.meta_description,
            "status": content.status,
            "quality_score": content.quality_score
        }

        version = ContentVersion(
            generated_content_id=content.id,
            version_number=current_versions + 1,
            content_snapshot=json.dumps(snapshot),
            changed_by=changed_by,
            change_type=change_type
        )
        db.add(version)
        db.commit()
        db.refresh(version)
        return version

    @staticmethod
    def update(
        db: Session,
        content: GeneratedContent,
        update_data: Dict[str, Any],
        is_human: bool = True
    ) -> GeneratedContent:
        # Create a version snapshot before updating
        ContentRepository.create_version(
            db, content, changed_by="User" if is_human else "System", change_type="Human Edit" if is_human else "Update"
        )

        for k, v in update_data.items():
                if k in ["highlights", "suggested_keywords", "warnings", "candidates_data"]:
                    setattr(content, k, json.dumps(v) if isinstance(v, (list, dict)) else v)
                else:
                    setattr(content, k, v)

        if is_human:
            content.is_human_edited = True

        db.commit()
        db.refresh(content)
        return content

    @staticmethod
    def update_status(db: Session, content: GeneratedContent, new_status: str) -> GeneratedContent:
        ContentRepository.create_version(
            db, content, changed_by="User", change_type=f"Status -> {new_status}"
        )
        content.status = new_status
        db.commit()
        db.refresh(content)
        return content

    @staticmethod
    def get_history(db: Session, content_id: int) -> List[Dict[str, Any]]:
        versions = db.query(ContentVersion).filter(
            ContentVersion.generated_content_id == content_id
        ).order_by(ContentVersion.version_number.desc()).all()

        res = []
        for v in versions:
            res.append({
                "id": v.id,
                "version_number": v.version_number,
                "content_snapshot": json.loads(v.content_snapshot) if v.content_snapshot else {},
                "changed_by": v.changed_by,
                "change_type": v.change_type,
                "created_at": v.created_at.isoformat() if v.created_at else None
            })
        return res
