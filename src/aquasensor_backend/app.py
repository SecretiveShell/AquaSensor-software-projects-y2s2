from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aquasensor_backend.templates import templates, static_files

app = FastAPI(
    title="AquaSensor Backend",
    description="A backend for the AquaSensor project.",
)

app.mount("/static", static_files, name="static")

@app.get("/")
async def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chart")
async def read_chart(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chart.html", {"request": request})

@app.get("/map")
async def read_map(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("map.html", {"request": request})