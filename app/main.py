from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, eventsRouter, projects, reportRouter


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)




app.include_router(auth.router)
app.include_router(eventsRouter.router)
app.include_router(projects.router)
app.include_router(reportRouter.router)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Ruta principal de bienvenida"""
    return {"message": "hello world"}





