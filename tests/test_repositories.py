import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import io
from repositories import (
    ler_parquet_do_bucket,
    verificar_lote_processado,
    registrar_lote_processado,
    inserir_dados,
    associar_imagens_aos_atendimentos
)
from models.models import LoteProcessado, Atendimento
from datetime import datetime

@pytest.fixture
def mock_db_session():
    return MagicMock()

@patch("repositories.storage.Client.create_anonymous_client")
def test_ler_parquet_do_bucket(mock_client):
    mock_blob = MagicMock()
    mock_blob.download_to_file.side_effect = lambda buffer: buffer.write(b"parquet_data")
    mock_bucket = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_client.return_value.bucket.return_value = mock_bucket
    
    with patch("pandas.read_parquet", return_value=pd.DataFrame({"col1": [1, 2, 3]})) as mock_read:
        df = ler_parquet_do_bucket("test_bucket", "test_file.pq")
        mock_read.assert_called()
        assert not df.empty

@patch("repositories.storage.Client.create_anonymous_client")
def test_ler_parquet_do_bucket_error(mock_client):
    mock_client.side_effect = Exception("Erro ao conectar")
    with pytest.raises(Exception, match="Erro ao conectar"):
        ler_parquet_do_bucket("test_bucket", "test_file.pq")


def test_verificar_lote_processado(mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = True
    assert verificar_lote_processado("test_file.pq", mock_db_session)
    
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    assert not verificar_lote_processado("test_file.pq", mock_db_session)


def test_verificar_lote_processado_error(mock_db_session):
    mock_db_session.query.side_effect = SQLAlchemyError("DB error")
    with pytest.raises(SQLAlchemyError, match="DB error"):
        verificar_lote_processado("test_file.pq", mock_db_session)


def test_registrar_lote_processado(mock_db_session):
    registrar_lote_processado("test_file.pq", mock_db_session)
    mock_db_session.add.assert_called()
    mock_db_session.commit.assert_called()

def test_inserir_dados(mock_db_session):
    dados = [{"id": 1, "name": "Teste"}]
    inserir_dados(mock_db_session, dados)
    mock_db_session.bulk_insert_mappings.assert_called_with(Atendimento, dados)
    mock_db_session.commit.assert_called()


def test_inserir_dados_vazio(mock_db_session):
    inserir_dados(mock_db_session, [])
    mock_db_session.bulk_insert_mappings.assert_not_called()
    mock_db_session.commit.assert_not_called()


def test_inserir_dados_error(mock_db_session):
    mock_db_session.bulk_insert_mappings.side_effect = SQLAlchemyError("DB error")
    with pytest.raises(SQLAlchemyError, match="DB error"):
        inserir_dados(mock_db_session, [{"id": 1, "name": "Teste"}])
    mock_db_session.rollback.assert_called()


def test_associar_imagens_aos_atendimentos(mock_db_session):
    mock_atendimento = MagicMock()
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_atendimento
    associar_imagens_aos_atendimentos(mock_db_session, "test_bucket", ["imagem.jpg"])
    assert mock_atendimento.image_path == "https://storage.googleapis.com/test_bucket/imagem.jpg"
    mock_db_session.commit.assert_called()


def test_associar_imagens_aos_atendimentos_sem_atendimento(mock_db_session):
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = None
    associar_imagens_aos_atendimentos(mock_db_session, "test_bucket", ["imagem.jpg"])
    mock_db_session.commit.assert_not_called()


def test_associar_imagens_aos_atendimentos_error(mock_db_session):
    mock_db_session.query.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        associar_imagens_aos_atendimentos(mock_db_session, "test_bucket", ["imagem.jpg"])
    mock_db_session.rollback.assert_called()
