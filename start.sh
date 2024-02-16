#!/bin/bash
set -euo pipefail

if [ "${PLATFORM:=}" != "docker" ]; then
  echo -e "\033[0;31mERROR: This start script is meant to be run inside the container.\033[0m"
  exit 1
fi

livy-server start
echo "SSL Disabled"
jupyter lab --no-browser \
  --ip=0.0.0.0 \
  --ServerApp.root_dir=/home/glue_user/workspace/ \
  --ServerApp.token='' \
  --ServerApp.password=''
