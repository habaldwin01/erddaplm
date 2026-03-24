#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR
./bitnetserver/build.sh
./webapp/build.sh
docker network create -d bridge public
docker compose up
