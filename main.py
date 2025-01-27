from fastapi import FastAPI

# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Ruta de ejemplo
@app.get("/")
async def read_root():
    return {"message": "¡Servidor HTTP en FastAPI funcionando correctamente!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

