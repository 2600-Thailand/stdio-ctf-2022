FROM php:7.2-apache
COPY . /var/www/html/

RUN echo $FLAG > /var/www/flag.txt
RUN chmod 444 /var/www/flag.txt
RUN chown www-data ./uploads
RUN chsh -s /usr/sbin/nologin root



