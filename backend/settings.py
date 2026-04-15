from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  ollama_base_url: str
  ollama_model_name: str = "gemma4:e4b"
  
  graph_image_path: str = "images"

  mariadb_user: str
  mariadb_password: str
  mariadb_host: str
  mariadb_port: int
  mariadb_database: str

  naver_client_id: str
  naver_client_secret: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
  )

settings = Settings()