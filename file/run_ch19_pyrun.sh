#!/bin/sh
# version 2

export CATEGORY="misc"
export CHALLENGE_NAME="ch19_pyrun"

cd server/${CATEGORY}/${CHALLENGE_NAME}
zip -r ../../../file/${CHALLENGE_NAME}.zip *
cd -