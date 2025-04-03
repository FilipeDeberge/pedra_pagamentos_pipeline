FROM apache/airflow:2.7.3-python3.10

# Define o diretório de trabalho
WORKDIR /opt/airflow

# Copia os arquivos do projeto
COPY . /opt/airflow

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão (docker-compose sobrescreve isso)
CMD ["airflow", "version"]
