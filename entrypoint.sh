#!/bin/bash

# Habilita modo de erro
set -e
# Aguarda o PostgreSQL estar pronto
until pg_isready -h postgres -p 5432; do
  echo "Aguardando PostgreSQL..."
  sleep 2
done

echo "Inicializando o banco de dados do Airflow..."
airflow db init

sleep 5

  # Verifica se o usuário admin já existe no Airflow
  if airflow users list | grep -q "admin"; then
      echo "Usuário admin já existe, pulando criação."
  else
      echo "Criando usuário admin..."
      airflow users create \
          --username admin \
          --password admin \
          --firstname Admin \
          --lastname User \
          --role Admin \
          --email admin@example.com
  fi

DB_NAME="pedra_pagamentos"
DB_USER="airflow"
DB_HOST="postgres"
SQL_FILE="/opt/airflow/models/create_tables.sql"

echo "Verificando se o banco pedra_pagamentos existe..."
PGPASSWORD=airflow psql -h $DB_HOST -U $DB_USER -tc "SELECT 1 FROM pg_database WHERE datname = 'pedra_pagamentos'" | grep -q 1 || \
PGPASSWORD=airflow psql -h $DB_HOST -U $DB_USER -c "CREATE DATABASE pedra_pagamentos;"

# Executa script Python para criar tabelas
TABLE_COUNT=$(PGPASSWORD=airflow psql -h $DB_HOST -U $DB_USER -d $DB_NAME -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ('atendimentos', 'lotes_processados');")

if [ "$TABLE_COUNT" -lt "2" ]; then
    echo "Criando tabelas no banco de dados..."
    PGPASSWORD=airflow psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f "$SQL_FILE"
    echo "Tabelas criadas com sucesso!"
else
    echo "As tabelas já existem, pulando criação..."
fi
echo "Banco de dados configurado com sucesso!"

exec "$@"
