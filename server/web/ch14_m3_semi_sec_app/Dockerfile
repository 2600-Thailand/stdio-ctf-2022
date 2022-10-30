FROM debian:latest
RUN apt-get update && apt-get -y install python3-pip
COPY . /app
COPY chromedriver /usr/local/bin/
WORKDIR "/app"

RUN apt install -y --allow-downgrades ./chrome.deb

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# RUN flask --app flaskr init-db 
# CMD gunicorn --bind 0.0.0.0:8000 -w 4 "flaskr:create_app()" 
CMD ./run.sh
EXPOSE 8000
