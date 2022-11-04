#!/bin/sh
# version 1

export CATEGORY="pwn"
export CHALLENGE_NAME="ch4_m4_super_guesser_v2"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -