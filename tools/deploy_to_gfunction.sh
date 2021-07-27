#! /bin/bash

gcloud functions deploy binance-bot --memory=512MB --timeout=60 --runtime=python38 \
--region=asia-southeast2 --trigger-http \
--entry-point=cloud_function --env-vars-file=$(pwd)/.env.json