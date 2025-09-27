from sqlmodel import Session, create_engine
import os

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/zapateria_db",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def get_session():
    return Session(engine)

session = Session(engine)
