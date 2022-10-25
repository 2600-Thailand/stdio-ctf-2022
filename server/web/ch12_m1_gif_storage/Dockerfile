FROM php:7.2-apache

COPY web /var/www/html
COPY start.sh /start.sh

RUN chown -R root:root /var/www/html
RUN chmod 755 /var/www/html
RUN chown -R www-data ./uploads
RUN chsh -s /usr/sbin/nologin root

CMD ["/start.sh"]
