#!/bin/sh
# version 1

export CATEGORY="misc"
export CHALLENGE_NAME="ch20_lottery_v2"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -
