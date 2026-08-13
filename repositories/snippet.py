from sqlalchemy.orm import Session
from database.models import Snippet




def get_snippets(db: Session) -> list[Snippet]:
    return (
        db.query(Snippet)
        .filter(Snippet.is_deleted == False)
        .order_by(Snippet.created_at.desc())
        .all()
    )


def create_snippet_func(
    db: Session,
    title: str,
    language: str,
    code: str,
    is_favorite: bool = False,
    description: str | None = None
):

    snippet_obj = Snippet(
        title=title,
        language=language,
        code=code,
        is_favorite=is_favorite,
        description=description
    )
    db.add(snippet_obj)
    db.commit()



def get_snippet_by_id(
    db: Session,
    snippet_id
):
    return db.query(Snippet).filter_by(id=snippet_id).one()


def get_favorite_snippets(db: Session) -> list[Snippet]:
    return (
        db.query(Snippet)
        .filter(
            Snippet.is_favorite == True,
            Snippet.is_deleted == False,
        )
        .all()
    )


def get_deleted_snippets(db: Session) -> list[Snippet]:
    return db.query(Snippet).filter_by(is_deleted=True).all()


def get_recent_snippets(db: Session, limit: int = 10):
    return (
        db.query(Snippet)
        .filter(Snippet.is_deleted == False)
        .order_by(Snippet.updated_at.desc())
        .limit(limit)
        .all()
    )


def search_snippets(db: Session, query: str) -> list[Snippet]:
    return (
        db.query(Snippet)
        .filter(
            Snippet.title.ilike(f"{query}%"),
            Snippet.is_deleted == False
        )
        .all()
    )
    
def delete_all_snippets(db):
    db.query(Snippet).delete()
    db.commit()