from .app import app


def main() -> None:
    from os import getenv
    from uvicorn import run

    PORT = int(getenv("MIDDLEWARE_PORT", 8000))

    run(app, host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
