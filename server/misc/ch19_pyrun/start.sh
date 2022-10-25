#!/bin/sh

echo $FLAG > $(cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32).txt
/etc/init.d/xinetd start;
sleep infinity;