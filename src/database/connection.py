from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select  # test session connection
from dotenv import load_dotenv
import os

load_dotenv()  # .env file load

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL, echo=True
)  # echo=True: sqlalchemy에 의해 query가 대신 처리될 때, 사용된 시점의 SQL문을 출력 - 디버깅용(개발환경에서만 사용, 운영환경에서는 사용하지 않음)
SessionFactory = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # commit, flush 연산을 자동으로 수행하지 않고, 명시적으로 수행해하도록 설정


def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


# session 연결 테스트
if __name__ == "__main__":
    session = SessionFactory()  # session 객체 생성
    result = session.scalar(select(1))  # scalar로 세션에 select 1을 출력하는 query를 실행
    print(result)
