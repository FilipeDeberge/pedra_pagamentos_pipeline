import unittest
from unittest.mock import patch, MagicMock
from services import (
    verificar_lote_task,
    ler_parquet_task,
    inserir_dados_task,
    registrar_lote_task,
    exportar_para_dw_task,
    processar_e_associar_imagens_task
)
from config import SessionLocal

class TestETLService(unittest.TestCase):
    @patch("services.SessionLocal", autospec=True)
    @patch("services.storage.Client.create_anonymous_client", autospec=True)
    @patch("services.verificar_lote_processado", return_value=False)
    def test_verificar_lote_task(self, mock_verificar_lote, mock_storage_client, mock_session):
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "arquivo.pq"
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.bucket.return_value = mock_bucket
        mock_storage_client.return_value = mock_client
        
        verificar_lote_task()
        mock_verificar_lote.assert_called_once()
        mock_session.assert_called_once()
    
    @patch("services.SessionLocal", autospec=True)
    @patch("services.storage.Client.create_anonymous_client", autospec=True)
    @patch("services.ler_parquet_do_bucket")
    @patch("services.verificar_lote_processado", return_value=False)
    def test_ler_parquet_task(self, mock_verificar_lote, mock_ler_parquet, mock_storage_client, mock_session):
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "arquivo.pq"
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.bucket.return_value = mock_bucket
        mock_storage_client.return_value = mock_client
        mock_ler_parquet.return_value.to_dict.return_value = {}
        
        ler_parquet_task()
        mock_ler_parquet.assert_called_once()
        mock_session.assert_called_once()
    
    @patch("services.SessionLocal", autospec=True)
    @patch("services.storage.Client.create_anonymous_client", autospec=True)
    @patch("services.inserir_dados")
    @patch("services.ler_parquet_do_bucket")
    @patch("services.verificar_lote_processado", return_value=False)
    def test_inserir_dados_task(self, mock_verificar_lote, mock_ler_parquet, mock_inserir_dados, mock_storage_client, mock_session):
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "arquivo.pq"
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.bucket.return_value = mock_bucket
        mock_storage_client.return_value = mock_client
        mock_ler_parquet.return_value.to_dict.return_value = {}
        
        inserir_dados_task()
        mock_inserir_dados.assert_called_once()
        mock_session.assert_called_once()
    
    @patch("services.SessionLocal", autospec=True)
    @patch("services.storage.Client.create_anonymous_client", autospec=True)
    @patch("services.registrar_lote_processado")
    @patch("services.verificar_lote_processado", return_value=False)
    def test_registrar_lote_task(self, mock_verificar_lote, mock_registrar_lote, mock_storage_client, mock_session):
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "arquivo.pq"
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.bucket.return_value = mock_bucket
        mock_storage_client.return_value = mock_client
        
        registrar_lote_task()
        mock_registrar_lote.assert_called_once()
        mock_session.assert_called_once()
    
    @patch("services.SessionLocal", autospec=True)
    @patch("services.exportar_para_dw")
    def test_exportar_para_dw_task(self, mock_exportar, mock_session):
        exportar_para_dw_task()
        mock_exportar.assert_called_once()
        mock_session.assert_called_once()
    
    @patch("services.SessionLocal", autospec=True)
    @patch("services.storage.Client.create_anonymous_client", autospec=True)
    @patch("services.associar_imagens_aos_atendimentos")
    def test_processar_e_associar_imagens_task(self, mock_associar_imagens, mock_storage_client, mock_session):
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_blob.name = "evidencias_atendimentos/imagem.jpg"
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.bucket.return_value = mock_bucket
        mock_storage_client.return_value = mock_client
        
        processar_e_associar_imagens_task()
        mock_associar_imagens.assert_called_once()
        mock_session.assert_called_once()

if __name__ == "__main__":
    unittest.main()