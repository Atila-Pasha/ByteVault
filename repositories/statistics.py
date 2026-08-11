from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Snippet


def get_total_snippets(db: Session) -> int:
    return (
        db.query(Snippet)
        .filter(Snippet.is_deleted == False)
        .count()
    )


def get_language_statistics(db: Session):
    return (
        db.query(
            Snippet.language,
            func.count(Snippet.id).label("count")
        )
        .filter(Snippet.is_deleted == False)
        .group_by(Snippet.language)
        .order_by(func.count(Snippet.id).desc())
        .all()
    )


def get_total_views(db: Session) -> int:
    result = (
        db.query(func.sum(Snippet.view_count))
        .filter(Snippet.is_deleted == False)
        .scalar()
    )

    return result or 0


def get_most_viewed_snippets(
    db: Session,
    limit: int = 5
):
    return (
        db.query(Snippet)
        .filter(Snippet.is_deleted == False)
        .order_by(Snippet.view_count.desc())
        .limit(limit)
        .all()
    )
    
def get_total_favorites(db: Session) -> int:
    return (
        db.query(Snippet)
        .filter(
            Snippet.is_favorite == True,
            Snippet.is_deleted == False,
        )
        .count()
    )