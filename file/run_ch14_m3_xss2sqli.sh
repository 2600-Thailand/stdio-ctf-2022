#!/bin/sh
# version 1

export CATEGORY="web"
export CHALLENGE_NAME="ch14_m3_xss2sqli"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -
