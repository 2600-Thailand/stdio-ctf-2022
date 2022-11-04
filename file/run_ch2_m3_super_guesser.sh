#!/bin/sh
# version 1

export CATEGORY="pwn"
export CHALLENGE_NAME="ch2_m3_super_guesser"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -