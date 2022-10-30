#!/bin/sh
# version 1

export CATEGORY="web"
export CHALLENGE_NAME="ch14_m3_semi_sec_app"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -
