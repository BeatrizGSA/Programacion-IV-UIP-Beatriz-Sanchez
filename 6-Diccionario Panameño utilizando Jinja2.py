import redis
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

redis_url = "redis://default:LApzhSSk8YSwXIshipytd2PIEQutVyv5@redis-18733.c228.us-central1-1.gce.cloud.redislabs.com:18733"
r = redis.from_url(redis_url)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    palabras = r.keys()
    palabras_significados = [(palabra.decode('utf-8'), r.get(palabra).decode('utf-8')) for palabra in palabras]
    return templates.TemplateResponse("index.html", {"request": request, "palabras_significados": palabras_significados})

@app.post("/agregar")
async def agregar_palabra(palabra: str = Form(...), significado: str = Form(...)):
    r.set(palabra, significado)
    return {"status": "success"}

@app.post("/editar")
async def editar_palabra(palabra: str = Form(...), nuevo_significado: str = Form(...)):
    if r.exists(palabra):
        r.set(palabra, nuevo_significado)
    return {"status": "success"}

@app.post("/eliminar")
async def eliminar_palabra(palabra: str = Form(...)):
    if r.exists(palabra):
        r.delete(palabra)
    return {"status": "success"}

@app.post("/buscar")
async def buscar_palabra(palabra: str = Form(...)):
    resultado = r.get(palabra)
    if resultado:
        return {"status": "success", "palabra": palabra, "significado": resultado.decode('utf-8')}
    else:
        return {"status": "error", "message": "Palabra no encontrada."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)