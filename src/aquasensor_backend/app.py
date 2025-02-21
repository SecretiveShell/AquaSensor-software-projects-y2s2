from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from aquasensor_backend.templates import templates, static_files
from aquasensor_backend.api import router as api_router
from aquasensor_backend.lifespan import lifespan
from aquasensor_backend.routes import router as routes

app = FastAPI(
    title="AquaSensor Backend",
    description="A backend for the AquaSensor project.",
    lifespan=lifespan,
)

app.mount("/static", static_files, name="static")

app.include_router(api_router, prefix="/api/v1")
app.include_router(routes)


@app.exception_handler(404)
async def read_404page(request: Request, exc: HTTPException) -> HTMLResponse:
    return templates.TemplateResponse("e404.html",{"request":request}, status_code=404)
