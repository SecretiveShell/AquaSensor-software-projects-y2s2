from fastapi import FastAPI, Request
from aquasensor_backend.templates import templates, static_files

app = FastAPI(
    title="AquaSensor Backend",
    description="A backend for the AquaSensor project.",
)

app.mount("/static", static_files, name="static")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})