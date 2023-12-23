from dotenv import dotenv_values
import sqlalchemy as sql

def connect_to_base() -> sql.Engine:
    config = dotenv_values()
    session_url = sql.engine.URL.create(
        drivername="postgresql+psycopg2",
        username=config.get("BASE_USER"),  # config["POSTGRES_USER"]
        password=config.get("BASE_PASSWORD"),
        host=config.get("BASE_HOST"),
        port=config.get("BASE_PORT"),
        database=config.get("BASE_DB")
    )
    return sql.create_engine(session_url)  # return engine