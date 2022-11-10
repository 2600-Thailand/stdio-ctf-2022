#!/bin/sh
# version 2

export CATEGORY="web"
export CHALLENGE_NAME="ch12_m1_gif_storage"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -