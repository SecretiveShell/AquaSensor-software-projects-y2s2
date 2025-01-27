FROM python:3.12

RUN pip install --upgrade pip
RUN pip install uv

COPY . .

RUN uv sync

CMD [ "uv", "run", "aquasensor_backend:app"]