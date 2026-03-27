from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, rooms, guests, reservations, ws
from .database import engine, Base 


Base.metadata.create_all(bind=engine) 

app = FastAPI(title="StayEase API")

# Configuración de CORS para que el Frontend pueda hablar con el Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción poner la URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir todos los routers
app.include_router(auth.router)
app.include_router(rooms.router)
app.include_router(guests.router)
app.include_router(reservations.router)
app.include_router(ws.router)

@app.get("/health")
def health():
    return {"status": "ok"}