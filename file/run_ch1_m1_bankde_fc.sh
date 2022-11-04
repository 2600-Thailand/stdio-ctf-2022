#!/bin/sh
# version 3

export CATEGORY="pwn"
export CHALLENGE_NAME="ch1_m1_pwn_bankde_fc"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -
