#!/bin/sh
# version 1

export CATEGORY="crypto"
export CHALLENGE_NAME="ch7_m2_byoh"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -