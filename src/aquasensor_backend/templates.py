from datetime import datetime
import os
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader, select_autoescape

JINJA_TEMPLATES_DIR = os.getenv("JINJA_TEMPLATES_DIR", "./src/frontend")

# jinja environment
env = Environment(
    loader=FileSystemLoader(JINJA_TEMPLATES_DIR),
    autoescape=select_autoescape(["html", "xml"]),
    extensions=["jinja2.ext.loopcontrols", "jinja2.ext.i18n"],
)

env.globals["now"] = datetime.now

templates = Jinja2Templates(env=env)

static_files = StaticFiles(directory=JINJA_TEMPLATES_DIR + "/static", html=True)
