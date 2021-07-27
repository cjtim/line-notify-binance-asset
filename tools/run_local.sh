#! /bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# for cloud functions
functions-framework \
  --source=main.py \
  --target=cloud_function \
  --signature-type=http \
  --port=8080 \
  --debug

# for cloud run
# functions-framework \
#   --source=main.py \
#   --target=cloudFunc_pubsub \
#   --signature-type=http \
#   --port=8080 \
#   --debug