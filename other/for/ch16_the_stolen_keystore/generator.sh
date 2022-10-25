#!/bin/sh

openssl req -x509 -newkey rsa:4096 -keyout secret.key -out cert.pem -days 365 -nodes -subj "/C=/ST=/L=/O=/CN="
openssl pkcs12 -export -out keyStore.p12 -inkey secret.key -in cert.pem -password 'pass:*2600atari'
openssl smime -encrypt -binary -aes-256-cbc -in flag.txt -out flag.txt.enc -outform PEM cert.pem
zip ../../../file/ch16_the_stolen_keystore.zip flag.txt.enc keyStore.p12
rm secret.key cert.pem flag.txt.enc