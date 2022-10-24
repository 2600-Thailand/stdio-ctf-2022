#!/bin/sh

# The following env is require
# IPFS_DEPLOY_INFURA__PROJECT_ID
# IPFS_DEPLOY_INFURA__PROJECT_SECRET 

wasm-pack build
cd www
yarn build
ipd dist