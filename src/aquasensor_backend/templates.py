import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

JINJA_TEMPLATES_DIR = os.getenv("JINJA_TEMPLATES_DIR", "./src/frontend")

templates = Jinja2Templates(directory="templates")

static_files = StaticFiles(directory=JINJA_TEMPLATES_DIR+"/static", html=True)