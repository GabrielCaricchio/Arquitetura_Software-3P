from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PedidoSocorro(Base):
    __tablename__ = "pedidos_socorro"

    id = Column(Integer, primary_key=True, index=True)
    nome_vitima = Column(String, default="Anônima") 
    urgencia = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    data_hora = Column(DateTime, default=datetime.utcnow)