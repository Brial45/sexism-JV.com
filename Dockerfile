FROM tensorflow/tensorflow:2.10.0
COPY jvcom /jvcom
COPY requirements_prod.txt /requirements_prod.txt
COPY model /model
RUN pip install --upgrade pip
RUN pip install -r requirements_prod.txt
CMD uvicorn jvcom.api.fast:app --host 0.0.0.0
