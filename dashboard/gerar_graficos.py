from config import engine
from models.models import Atendimento
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sqlalchemy import func
from config import SessionLocal

# Configuração do banco de dados
Session = SessionLocal
output_dir = "/opt/airflow/dashboard"
def gerar_graficos():
    session = Session()

    # Produtividade por Green Angel
    produtividade = (
        session.query(
            Atendimento.technician_email,
            func.count(Atendimento.order_number).label("atendimentos")
        )
        .filter(Atendimento.technician_email.isnot(None))
        .group_by(Atendimento.technician_email)
        .order_by(func.count(Atendimento.order_number).desc())
        .limit(10)
        .all()
    )

    # SLA por Cidade
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

    # SLA por Green Angel
    sla_por_green_angel = (
        session.query(
            Atendimento.technician_email.label("green_angel"),
            (func.count().filter(Atendimento.arrival_date <= Atendimento.deadline_date) * 100.0 / func.count()).label("sla_percentual"),
        )
        .filter(Atendimento.technician_email.isnot(None))
        .group_by(Atendimento.technician_email)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )

    session.close()

    # Criar diretório para salvar os gráficos
    output_dir = "/opt/airflow/dashboard"
    os.makedirs(output_dir, exist_ok=True)

    # Configurar estilo dos gráficos
    sns.set(style="whitegrid")

    # Criar gráfico de produtividade por Green Angel
    plt.figure(figsize=(25, 9))
    sns.barplot(x="atendimentos", y="green_angel", data=pd.DataFrame(produtividade, columns=["green_angel", "atendimentos"]), palette="Blues_r")
    plt.xlabel("Atendimentos")
    plt.ylabel("Green Angel")
    plt.title("Produtividade por Green Angel (Top 10)")
    plt.savefig(f"{output_dir}/produtividade.png")
    plt.close()

    # Criar gráfico de SLA por Cidade
    plt.figure(figsize=(25, 9))
    sns.barplot(x="sla_percentual", y="cidade", data=pd.DataFrame(sla_por_cidade, columns=["cidade", "sla_percentual"]), palette="Greens_r")
    plt.xlabel("SLA (%)")
    plt.ylabel("Cidade (Base Logística)")
    plt.title("SLA por Cidade")
    plt.savefig(f"{output_dir}/sla_cidade.png")
    plt.close()

    # Criar gráfico de SLA por Green Angel
    plt.figure(figsize=(25, 9))
    sns.barplot(x="sla_percentual", y="green_angel", data=pd.DataFrame(sla_por_green_angel, columns=["green_angel", "sla_percentual"]), palette="Oranges_r")
    plt.xlabel("SLA (%)")
    plt.ylabel("Green Angel")
    plt.title("SLA por Green Angel (Top 10)")
    plt.savefig(f"{output_dir}/sla_green_angel.png")
    plt.close()
