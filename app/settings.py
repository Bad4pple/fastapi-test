from pydantic import BaseSettings

class Settings(BaseSettings):
    datbase_username: str = "localhost:8000"
    database_password: str = "password"