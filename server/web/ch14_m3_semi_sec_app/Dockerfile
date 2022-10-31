FROM debian:latest
RUN apt-get update && apt-get -y install python3-pip
COPY . /app
COPY chromedriver /usr/local/bin/
WORKDIR "/app"

RUN apt install -y --allow-downgrades ./chrome.deb

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

CMD ./run.sh
EXPOSE 8000
