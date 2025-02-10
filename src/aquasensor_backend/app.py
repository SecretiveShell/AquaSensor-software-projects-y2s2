from fastapi import FastAPI
from aquasensor_backend.templates import static_files

app = FastAPI(
    title="AquaSensor Backend",
    description="A backend for the AquaSensor project.",
)

app.mount("/static", static_files, name="static")