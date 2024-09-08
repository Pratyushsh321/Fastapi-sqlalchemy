from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

SQLALCHEMY_DATABASE_URL = "postgresql://postgres.hauwyfjiibuhjsvzgtnr:NvR1UJtJiD4ZiACc@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# NvR1UJtJiD4ZiACc


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while true
# try:
#     # user=postgres.rxjaqtceaqvplaxrprrr password=[YOUR-PASSWORD] host=aws-0-ap-south-1.pooler.supabase.com port=6543 dbname=postgres
#     conn = psycopg2.connect(
#         host="aws-0-ap-south-.p1ooler.supabase.com",
#         database="postgres",
#         user="postgres.rxjaqtceaqvplaxrprrr",
#         password="Pratyush@8709",
#         port=6543,
#         cursor_factory=RealDictCursor,
#     )
#     cursor = conn.cursor()
#     print("Database connection was succesfull")
#     break
# except Exception as error:
#     print("Connecting to database failed")
#     print("Error: ", error)
#     break
