from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config

# Configuração do banco de dados PostgreSQL
alembic_cfg = Config("alembic.ini")
DATABASE_URL = alembic_cfg.get_main_option("sqlalchemy.url")
# Criar engine e session
engine = create_engine(DATABASE_URL, echo=True)  # `echo=True` para debug SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
