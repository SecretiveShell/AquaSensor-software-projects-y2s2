from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from aquasensor_backend.templates import templates, static_files
from aquasensor_backend.api import router as api_router
from aquasensor_backend.lifespan import lifespan

app = FastAPI(
    title="AquaSensor Backend",
    description="A backend for the AquaSensor project.",
    lifespan=lifespan,
)

app.mount("/static", static_files, name="static")

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chart")
async def read_chart(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chart.html", {"request": request})


@app.get("/map")
async def read_map(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("map.html", {"request": request})

@app.get("/dataFunction.js")
async def read_datfunc(request:Request) -> Response:
    return Response(templates.TemplateResponse("dataFunction.js",{"request": request}).body, media_type="application/javascript")

@app.get("/test")
async def read_test(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("test.html",{"request":request})

@app.get("/contactus")
async def read_contact(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("contactus.html",{"request":request})

@app.get("/login")
async def read_login(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("signin.html",{"request":request})

@app.get("/login-homepage")
async def read_authed_homepage(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("loginsuccess.html",{"request":request})
