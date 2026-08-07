from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from database.config import settings

engine = create_engine(settings.DB_URL, echo=False)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def init_database():
    from alembic.config import Config
    from alembic import command

    project_dir = Path(__file__).resolve().parent.parent
    alembic_ini = project_dir / "alembic.ini"

    cfg = Config(str(alembic_ini))
    command.upgrade(cfg, "head")