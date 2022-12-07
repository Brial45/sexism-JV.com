FROM python:3.10.6-slim
COPY requirements_prod.txt /requirements_prod.txt
RUN pip install --upgrade pip
RUN pip install -r requirements_prod.txt
COPY jvcom /jvcom
CMD uvicorn jvcom.api.fast:app --host 0.0.0.0 --port $PORT
