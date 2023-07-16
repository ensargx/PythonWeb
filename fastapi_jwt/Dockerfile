FROM python:3.10

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY ./app /api/app
EXPOSE 80

ENV JWT_SECRET_KEY=SECRET

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]