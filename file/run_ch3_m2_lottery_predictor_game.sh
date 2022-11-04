#!/bin/sh
# version 2

export CATEGORY="pwn"
export CHALLENGE_NAME="ch3_m2_lottery_predictor_game"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -
