FROM python:3.12

RUN pip install --upgrade pip
RUN pip install uv


COPY mqtt .

RUN rm -rf .venv

RUN uv sync

CMD ["uv","run","mqtt.py"]
