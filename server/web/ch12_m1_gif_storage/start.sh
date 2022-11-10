echo $FLAG > /var/www/html/$(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
chmod 444 /var/www/html/flag.txt
apache2-foreground