from sqlmodel import Session, create_engine

from app.core.settings import settings

engine = create_engine(settings.DB_CONNECTION_STR)


def db_session():
    with Session(engine) as session:
        yield session
