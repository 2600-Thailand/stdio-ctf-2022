#!/bin/sh
# version 1

export CATEGORY="crypto"
export CHALLENGE_NAME="ch6_m1_pudding"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -