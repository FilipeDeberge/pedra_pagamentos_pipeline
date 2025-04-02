from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Atendimento(Base):
    __tablename__ = "atendimentos"
    
    order_number = Column(Integer, primary_key=True, index=True)
    terminal_id = Column(Integer)
    terminal_serial_number = Column(String)
    terminal_model = Column(String)
    arrival_date = Column(DateTime)
    deadline_date = Column(DateTime)
    cancellation_reason = Column(Text)
    last_modified_date = Column(DateTime)
    country_state = Column(String)
    technician_email = Column(String)
    zip_code = Column(String)
    neighborhood = Column(String)
    customer_phone = Column(String)
    complement = Column(String)
    city = Column(String)
    customer_id = Column(String)
    terminal_type = Column(String)
    street_name = Column(String)
    provider = Column(String)
    country = Column(String)
    exportado_para_dw = Column(Boolean, default=False)

class LoteProcessado(Base):
    __tablename__ = "lotes_processados"
    
    arquivo_nome = Column(String, primary_key=True)
    data_processamento = Column(DateTime, nullable=False)
