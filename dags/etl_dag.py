from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from services import (
    verificar_lote_task,
    ler_parquet_task,
    inserir_dados_task,
    registrar_lote_task,
    exportar_para_dw_task,
)
# Definindo a DAG do Airflow
dag = DAG(
    'processar_atendimentos_dag',
    description='Processa os atendimentos e exporta para o DW',
    schedule_interval='@daily',  # Executa todos os dias
    start_date=datetime(2025, 3, 30),  # Data de início
    catchup=False  # Não executar para datas passadas
)

# Definindo as tarefas da DAG

verificar_lote = PythonOperator(
    task_id='verificar_lote',
    python_callable=verificar_lote_task,
    dag=dag
)

ler_parquet = PythonOperator(
    task_id='ler_parquet',
    python_callable=ler_parquet_task,
    dag=dag
)

inserir_dados = PythonOperator(
    task_id='inserir_dados',
    python_callable=inserir_dados_task,
    dag=dag
)

registrar_lote = PythonOperator(
    task_id='registrar_lote',
    python_callable=registrar_lote_task,
    dag=dag
)

exportar_dw = PythonOperator(
    task_id='exportar_para_dw',
    python_callable=exportar_para_dw_task,
    dag=dag
)

# Definindo a sequência de execução das tarefas
verificar_lote >> ler_parquet >> inserir_dados >> registrar_lote >> exportar_dw
