from .app import app


def main() -> None:
    from uvicorn import run

    run(app, host="0.0.0.0", port=8000)
