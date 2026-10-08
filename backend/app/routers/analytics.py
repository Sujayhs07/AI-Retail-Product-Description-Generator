import json
from collections import Counter
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Product, GeneratedContent, BatchJob

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/dashboard")
@router.get("/overview")
def get_analytics(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product, GeneratedContent).outerjoin(
        GeneratedContent, Product.id == GeneratedContent.product_id
    )

    if category and category != "All":
        query = query.filter(Product.category == category)
    if brand and brand != "All":
        query = query.filter(Product.brand == brand)

    all_pairs = query.all()
    products_count = len(all_pairs)
    
    contents = [c for _, c in all_pairs if c is not None]
    generated_count = len(contents)
    approved_count = sum(1 for c in contents if c.status == "Approved")
    review_count = sum(1 for c in contents if c.status == "Needs Review")

    avg_seo = round(sum(c.seo_score for c in contents) / generated_count, 1) if generated_count > 0 else 0.0
    avg_quality = round(sum(c.quality_score for c in contents) / generated_count, 1) if generated_count > 0 else 0.0

    batch_completed = db.query(BatchJob).filter(BatchJob.status == "completed").count()

    # 1. Generations Over Time (Past 7 days)
    today = datetime.utcnow().date()
    days = [(today - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
    over_time_map = {d: 0 for d in days}

    for c in contents:
        if c.generated_at:
            d_str = c.generated_at.strftime("%b %d")
            if d_str in over_time_map:
                over_time_map[d_str] += 1
            else:
                # If outside 7 days range, attribute to earliest day for smooth charts
                over_time_map[days[0]] += 1

    generations_over_time = [{"date": k, "count": v} for k, v in over_time_map.items()]

    # 2. Products by Category (Category Distribution across 8 retail verticals)
    CANONICAL_CATEGORIES = [
        "Electronics", "Fashion", "Home and Kitchen", "Beauty and Personal Care",
        "Sports and Fitness", "Furniture", "Grocery", "Travel Accessories"
    ]
    cat_counts = Counter(p.category for p, _ in all_pairs if p.category)
    if not category or category == "All":
        all_cats = list(dict.fromkeys(CANONICAL_CATEGORIES + list(cat_counts.keys())))
        products_by_category = [
            {"category": k, "count": cat_counts.get(k, 0)}
            for k in sorted(all_cats, key=lambda c: cat_counts.get(c, 0), reverse=True)
            if cat_counts.get(k, 0) > 0 or k in CANONICAL_CATEGORIES
        ]
    else:
        products_by_category = [{"category": k, "count": v} for k, v in cat_counts.items()]

    # 3. Quality Score Distribution
    q_ranges = {"Below 60 (Needs Work)": 0, "60 - 79 (Good)": 0, "80 - 100 (Excellent)": 0}
    for c in contents:
        if c.quality_score < 60:
            q_ranges["Below 60 (Needs Work)"] += 1
        elif c.quality_score < 80:
            q_ranges["60 - 79 (Good)"] += 1
        else:
            q_ranges["80 - 100 (Excellent)"] += 1

    quality_score_distribution = [{"range": k, "count": v} for k, v in q_ranges.items()]

    # 4. SEO Score Distribution
    seo_ranges = {"Below 60": 0, "60 - 79": 0, "80 - 100": 0}
    for c in contents:
        if c.seo_score < 60:
            seo_ranges["Below 60"] += 1
        elif c.seo_score < 80:
            seo_ranges["60 - 79"] += 1
        else:
            seo_ranges["80 - 100"] += 1

    seo_score_distribution = [{"range": k, "count": v} for k, v in seo_ranges.items()]

    # 5. Tone Usage Distribution
    tone_counts = Counter(c.tone for c in contents if c.tone)
    tone_usage = [{"tone": k, "count": v} for k, v in tone_counts.items()]

    # 6. Status Breakdown
    status_counts = Counter(c.status for c in contents if c.status)
    status_distribution = [{"status": k, "count": v} for k, v in status_counts.items()]

    # 7. Recent Activities
    recent_activities = []
    sorted_pairs = sorted(all_pairs, key=lambda pair: pair[1].generated_at if pair[1] and pair[1].generated_at else datetime.min, reverse=True)[:10]

    for p, c in sorted_pairs:
        if c:
            recent_activities.append({
                "id": c.id,
                "product_name": p.name,
                "action": "Generated Description",
                "status": c.status,
                "score": c.quality_score,
                "timestamp": c.generated_at.strftime("%Y-%m-%d %H:%M") if c.generated_at else "Just now",
                "source": c.generation_source
            })

    return {
        "metrics": {
            "total_products": products_count,
            "descriptions_generated": generated_count,
            "approved_descriptions": approved_count,
            "products_needing_review": review_count,
            "avg_seo_score": avg_seo,
            "avg_quality_score": avg_quality,
            "batch_jobs_completed": batch_completed
        },
        "generations_over_time": generations_over_time,
        "products_by_category": products_by_category,
        "quality_score_distribution": quality_score_distribution,
        "seo_score_distribution": seo_score_distribution,
        "tone_usage": tone_usage,
        "status_distribution": status_distribution,
        "recent_activities": recent_activities
    }
