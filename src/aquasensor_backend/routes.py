from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from aquasensor_backend.templates import templates

router = APIRouter(include_in_schema=False)


@router.get("/")
async def read_root(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/sitemap.xml")
async def read_sitemap(request:Request) -> Response:
    return Response(templates.TemplateResponse("sitemap.xml",{"request":request}).body,media_type="application/xml")

@router.get("/chart")
async def read_chart(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("chart.html", {"request": request})


@router.get("/dataLoading.js")
async def read_datfunc(request: Request) -> Response:
    return Response(
        templates.TemplateResponse("dataLoading.js", {"request": request}).body,
        media_type="application/javascript",
    )


@router.get("/contactus")
async def read_contact(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("contactus.html", {"request": request})


@router.get("/login")
async def read_login(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("signin.html", {"request": request})


@router.get("/register")
async def read_reg(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/aboutus")
async def read_aboutus(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("aboutus.html", {"request": request})


@router.get("/faq")
async def read_faq(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("faq.html", {"request": request})


@router.get("/privacy-policy")
async def read_privacypolicy(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("privacy-policy.html", {"request": request})


@router.get("/studio")
async def read_studio(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("studio.html", {"request": request})


@router.get("/studio-mobile")
async def read_studiomobile(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("studio-mobile.html",{"request":request})


@router.get("/correlate")
async def read_correlate(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("correlation.html",{"request":request})

