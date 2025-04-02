import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os
import sys
# Obtém o diretório principal do projeto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Adiciona a pasta principal ao sys.path
sys.path.append(BASE_DIR)
from config import engine
from models import Atendimento

# Criar sessão do banco de dados
Session = sessionmaker(bind=engine)
session = Session()

# 🔹 1️⃣ Produtividade por Green Angel (Número de atendimentos por técnico)
produtividade = (
    session.query(
        Atendimento.technician_email,
        func.count(Atendimento.order_number).label("atendimentos")
    )
    .filter(Atendimento.technician_email.isnot(None))
    .group_by(Atendimento.technician_email)
    .order_by(func.count(Atendimento.order_number).desc())
    .limit(10)  # Pega os 10 mais produtivos
    .all()
)

# 🔹 2️⃣ SLA por Cidade (Percentual de atendimentos dentro do prazo)
sla_por_cidade = (
    session.query(
        Atendimento.city.label("cidade"),
        (func.count().filter(Atendimento.arrival_date <= Atendimento.deadline_date) * 100.0 / func.count()).label("sla_percentual"),
    )
    .filter(Atendimento.city.isnot(None))
    .group_by(Atendimento.city)
    .order_by(func.count().desc())
    .limit(10)
    .all()
)

# 🔹 3️⃣ SLA por Green Angel (Percentual de atendimentos dentro do prazo por técnico)
sla_por_green_angel = (
    session.query(
        Atendimento.technician_email.label("green_angel"),
        (func.count().filter(Atendimento.arrival_date <= Atendimento.deadline_date) * 100.0 / func.count()).label("sla_percentual"),
    )
    .filter(Atendimento.technician_email.isnot(None))
    .group_by(Atendimento.technician_email)
    .order_by(func.count().desc())  # Ordena pelos técnicos com mais atendimentos
    .limit(10)  # Pega os 10 principais técnicos
    .all()
)

# Fechar sessão
session.close()

# Converter para DataFrame
df_produtividade = pd.DataFrame(produtividade, columns=["green_angel", "atendimentos"])
df_sla_cidade = pd.DataFrame(sla_por_cidade, columns=["cidade", "sla_percentual"])
df_sla_green_angel = pd.DataFrame(sla_por_green_angel, columns=["green_angel", "sla_percentual"])

# Configurar estilo dos gráficos
sns.set(style="whitegrid")

# 🔹 Criar gráfico de produtividade por Green Angel
plt.figure(figsize=(12, 6))
sns.barplot(x="atendimentos", y="green_angel", data=df_produtividade, palette="Blues_r")
plt.xlabel("Atendimentos")
plt.ylabel("Green Angel")
plt.title("Produtividade por Green Angel (Top 10)")
plt.show()

# 🔹 Criar gráfico de SLA por Cidade
plt.figure(figsize=(12, 6))
sns.barplot(x="sla_percentual", y="cidade", data=df_sla_cidade, palette="Greens_r")
plt.xlabel("SLA (%)")
plt.ylabel("Cidade (Base Logística)")
plt.title("SLA por Cidade")
plt.show()

# 🔹 Criar gráfico de SLA por Green Angel
plt.figure(figsize=(12, 6))
sns.barplot(x="sla_percentual", y="green_angel", data=df_sla_green_angel, palette="Oranges_r")
plt.xlabel("SLA (%)")
plt.ylabel("Green Angel")
plt.title("SLA por Green Angel (Top 10)")
plt.show()