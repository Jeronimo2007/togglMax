from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, eventsRouter, projects


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




app.include_router(auth.router)
app.include_router(eventsRouter.router)
app.include_router(projects.router)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Ruta principal de bienvenida"""
    return {"message": "hello world"}





