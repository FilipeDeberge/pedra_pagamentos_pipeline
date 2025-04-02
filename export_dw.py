from sqlalchemy.orm import Session
import pandas as pd
from models import Atendimento

def exportar_para_dw(db: Session):
    """Exporta novos registros para o Data Warehouse de forma otimizada."""
    
    # Busca registros que ainda não foram exportados
    novos_registros = db.query(Atendimento).filter(Atendimento.exportado_para_dw == False).all()
    
    if not novos_registros:
        print("Nenhum novo registro para exportação.")
        return
    
    # Obtém os nomes das colunas diretamente do modelo
    colunas = [c.name for c in Atendimento.__table__.columns]
    
    # Conversão mais rápida usando from_records()
    df = pd.DataFrame.from_records(
        (registro.__dict__ for registro in novos_registros),  # Transforma objetos ORM em dicionários
        columns=colunas
    )

    # Remover a coluna _sa_instance_state que SQLAlchemy adiciona automaticamente
    df.drop(columns=['_sa_instance_state'], errors='ignore', inplace=True)

    # Simulação de persistência no DW (exemplo com CSV)
    df.to_csv("dw_atendimentos.csv", index=False)
    print("Dados exportados para dw_atendimentos.csv")

    # Atualiza os registros no banco para marcar como exportados
    db.query(Atendimento).filter(Atendimento.exportado_para_dw == False).update(
        {Atendimento.exportado_para_dw: True}, synchronize_session=False
    )
    db.commit()
    print("Registros marcados como exportados.")