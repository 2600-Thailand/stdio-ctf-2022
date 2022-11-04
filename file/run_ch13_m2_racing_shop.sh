#!/bin/sh
# version 1

export CATEGORY="web"
export CHALLENGE_NAME="ch13_m2_racing_shop"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -
