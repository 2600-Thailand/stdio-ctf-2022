#!/bin/sh
# version 3

export CATEGORY="crypto"
export CHALLENGE_NAME="ch8_m3_ezdsa"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -