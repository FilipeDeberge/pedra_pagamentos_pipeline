from config import SessionLocal
from google.cloud import storage
from repositories import (
    ler_parquet_do_bucket,
    verificar_lote_processado,
    registrar_lote_processado,
    inserir_dados,
    associar_imagens_aos_atendimentos
)
from export_dw import exportar_para_dw
from airflow.exceptions import AirflowException
import logging

logger = logging.getLogger("airflow.task")

"""Serviços de ETL para processar arquivos Parquet e exportar dados para o Data Warehouse, camada que abstrai a lógica de negócio."""

BUCKET_NAME = "desafio-eng-dados"
SUBPASTA = "evidencias_atendimentos" 

# Função para verificar se o lote foi processado
def verificar_lote_task():
    try:
        db_session = SessionLocal()
        client = storage.Client.create_anonymous_client() #Cliente com autenticação anônima
        bucket = client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs())

        for blob in blobs:
            if blob.name.endswith(".pq"):
                if not verificar_lote_processado(blob.name, db_session):
                    print(f"Lote {blob.name} não processado. Verificando agora.")
                else:
                    print(f"Lote {blob.name} já foi processado.")
        db_session.close()
    except Exception as e:
        logger.error("Erro ao executar a função: %s", str(e), exc_info=True)
        raise AirflowException("Falha na execução da tarefa.")

# Função para ler os arquivos Parquet do bucket
def ler_parquet_task():
    try:
        db_session = SessionLocal()
        client = storage.Client.create_anonymous_client() #Cliente com autenticação anônima
        bucket = client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs())

        for blob in blobs:
            if blob.name.endswith(".pq"):
                if not verificar_lote_processado(blob.name, db_session):
                    print(f"Lendo arquivo {blob.name}...")
                    df = ler_parquet_do_bucket(BUCKET_NAME, blob.name)
                    dados = df.to_dict(orient="records")
                    print(f"Arquivo {blob.name} lido com sucesso.")
        db_session.close()
    except Exception as e:
        logger.error("Erro ao executar a função: %s", str(e), exc_info=True)
        raise AirflowException("Falha na execução da tarefa.")

# Função para inserir os dados no banco
def inserir_dados_task():
    try:
        db_session = SessionLocal()
        client = storage.Client.create_anonymous_client() #Cliente com autenticação anônima
        bucket = client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs())

        for blob in blobs:
            if blob.name.endswith(".pq"):
                if not verificar_lote_processado(blob.name, db_session):
                    print(f"Inserindo dados do arquivo {blob.name}...")
                    df = ler_parquet_do_bucket(BUCKET_NAME, blob.name)
                    dados = df.to_dict(orient="records")
                    inserir_dados(db_session, dados)
                    print(f"Dados do arquivo {blob.name} inseridos com sucesso.")
        db_session.close()
    except Exception as e:
        logger.error("Erro ao executar a função: %s", str(e), exc_info=True)
        raise AirflowException("Falha na execução da tarefa.")

# Função para registrar o lote processado
def registrar_lote_task():
    try:
        db_session = SessionLocal()
        client = storage.Client.create_anonymous_client() #Cliente com autenticação anônima
        bucket = client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs())

        for blob in blobs:
            if blob.name.endswith(".pq"):
                if not verificar_lote_processado(blob.name, db_session):
                    print(f"Registrando lote {blob.name} como processado...")
                    registrar_lote_processado(blob.name, db_session)
                    print(f"Lote {blob.name} registrado como processado.")
        db_session.close()
    except Exception as e:
        logger.error("Erro ao executar a função: %s", str(e), exc_info=True)
        raise AirflowException("Falha na execução da tarefa.")

# Função para exportar os dados para o Data Warehouse
def exportar_para_dw_task():
    try:
        db_session = SessionLocal()
        exportar_para_dw(db_session)
        print("Dados exportados para o Data Warehouse com sucesso.")
    except Exception as e:
        logger.error("Erro ao executar a função: %s", str(e), exc_info=True)
        raise AirflowException("Falha na execução da tarefa.")
    finally:
        db_session.close()

def processar_e_associar_imagens_task():
    """Obtém imagens do bucket e associa aos atendimentos no banco de dados."""
    try:
        db_session = SessionLocal()
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs(prefix=f"{SUBPASTA}/"))  # Filtra arquivos na subpasta

        # Filtrar apenas imagens (ex: jpg, png)
        imagens = [blob.name for blob in blobs if blob.name.lower().endswith((".jpg", ".png"))]

        if not imagens:
            print("Nenhuma imagem encontrada no bucket.")
            return

        # Chamar o Repository para atualizar o banco
        associar_imagens_aos_atendimentos(db_session, BUCKET_NAME, imagens)

    except Exception as e:
        logger.error("Erro ao executar a função: %s", str(e), exc_info=True)
        raise AirflowException("Falha na execução da tarefa.")
    
processar_e_associar_imagens_task()