FROM php:7.2-apache
COPY . /var/www/html/

RUN echo "STDIO14{8d9cd6cd14bf75a9c782d0628c7e60d0}" > /var/www/flag.txt
RUN chmod 444 /var/www/flag.txt
RUN chsh -s /usr/sbin/nologin root



