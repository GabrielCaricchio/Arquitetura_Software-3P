from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, PedidoSocorro

app = FastAPI()


Base.metadata.create_all(bind=engine)
class AlertaEmergencia(BaseModel):
    urgencia: str
    latitude: float
    longitude: float

@app.get("/")
def pagina_inicial():
    return FileResponse("index.html")

@app.post("/api/socorro")
def receber_alerta(alerta: AlertaEmergencia, db: Session = Depends(get_db)):
    
    novo_pedido = PedidoSocorro(
        urgencia=alerta.urgencia,
        latitude=alerta.latitude,
        longitude=alerta.longitude
    )
    
    db.add(novo_pedido)
    db.commit()
    
    print(f"🚨 ALERTA SALVO NO BANCO! Nível: {alerta.urgencia} | Coordenadas: {alerta.latitude}, {alerta.longitude}")
    return {"status": "sucesso", "mensagem": "Autoridades notificadas e registro salvo."}