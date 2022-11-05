#!/bin/sh
# version 2

export CATEGORY="web"
export CHALLENGE_NAME="ch14_m3_semi_sec_app"

cd server/${CATEGORY}/${CHALLENGE_NAME}/flaskr
zip -r ../../../../file/${CHALLENGE_NAME}.zip *
cd -
