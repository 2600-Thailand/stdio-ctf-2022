FROM python:3

COPY app /usr/src/app
WORKDIR /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 1337

CMD ["python", "app.py"]