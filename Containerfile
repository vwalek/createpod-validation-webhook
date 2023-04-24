FROM registry.redhat.io/ubi8/python-38:latest

WORKDIR /code

COPY requirements.txt .

RUN pip install gunicorn && pip install -r requirements.txt

COPY app /code

EXPOSE 8443

CMD [ "/opt/app-root/bin/gunicorn", "app:app", "--certfile=/ssl/tls.crt", "--keyfile=/ssl/tls.key", "--bind", "0.0.0.0:8443", "--keep-alive", "1" ]