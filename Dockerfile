# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Definir variáveis de ambiente para não interagir com o sistema durante a instalação
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de requisitos para o container
COPY requirements.txt /app/

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o container
COPY . /app/

# Definir o entrypoint para iniciar o Airflow
ENTRYPOINT ["airflow"]

# Comando para rodar o Airflow scheduler
CMD ["scheduler"]
