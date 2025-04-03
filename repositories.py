import io
import pandas as pd
from google.cloud import storage
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from models.models import Atendimento, LoteProcessado
from datetime import datetime
from typing import List, Dict

"""
Repositório para operações de banco de dados e manipulação de dados.
"""

def ler_parquet_do_bucket(bucket_name: str, arquivo: str) -> pd.DataFrame:
    """Lê um arquivo Parquet diretamente do bucket sem baixar."""
    try:
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(arquivo)
        buffer = io.BytesIO()
        blob.download_to_file(buffer)
        buffer.seek(0)
        return pd.read_parquet(buffer)
    except Exception as e:
        print(f"Erro ao ler arquivo Parquet do bucket: {e}")
        raise e
    
def verificar_lote_processado(arquivo_nome: str, db_session: Session) -> bool:
    """Verifica se o arquivo (lote) já foi processado."""
    try:
        return db_session.query(LoteProcessado).filter(LoteProcessado.arquivo_nome == arquivo_nome).first() is not None
    except SQLAlchemyError as e:
        print(f"Erro ao verificar lote processado: {e}")
        raise e


def registrar_lote_processado(arquivo_nome: str, db_session: Session):
    """Registra o arquivo (lote) como processado no banco."""
    try:
        lote = LoteProcessado(arquivo_nome=arquivo_nome, data_processamento=datetime.now())
        db_session.add(lote)
        db_session.commit()
    except SQLAlchemyError as e:
        print(f"Erro ao registrar lote processado: {e}")
        raise e

def inserir_dados(session: Session, dados: List[Dict]):
    """Insere os dados no banco em lote usando bulk_insert_mappings."""
    if not dados:
        return  # Evita tentativa de inserção vazia

    try:
        # Usando bulk_insert_mappings para inserção mais rápida
        session.bulk_insert_mappings(Atendimento, dados)
        session.commit()  # Confirma a transação
    except SQLAlchemyError as e:
        session.rollback()  # Em caso de erro, reverte a transação
        print(f"Erro ao inserir dados: {e}")
        raise e

def associar_imagens_aos_atendimentos(session: Session, bucket_name: str, imagens: list):
    """Associa imagens aos atendimentos no banco de dados."""
    try:
        for imagem in imagens:
            order_number = imagem.split("/")[-1].split(".")[0]  # Pega o número da ordem
            
            # Verificar se existe um atendimento com esse número
            atendimento = session.query(Atendimento).filter_by(order_number=order_number).first()
            if atendimento:
                atendimento.image_path = f"https://storage.googleapis.com/{bucket_name}/{imagem}"  # URL da imagem
                session.commit()
                print("Imagens associadas com sucesso.")

    except Exception as e:
        session.rollback()
        print(f"Erro ao associar imagens no banco: {e}")
        raise e