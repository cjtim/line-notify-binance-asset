
# [microservice-binance-cronjob](https://github.com/cjtim/microservice-binance-cronjob)

  
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## setup

- environment variable

	- REQ_AUTH_KEY (allow only request headers `Authorization` with this value to proceed)

- Deploy on GCP Cloud Function

- Runtime `Python 3.8`

- Recommend Ram 512 mb

- Timeout 30 sec

- Excecuted Function `cloud_function`

- trigger `http` method

- Allow unauthenticated

  
## POST Body
```
{

	"binanceApiKey": "XXXXX",

	"binanceSecretKey": "XXXXX",

	"lineNotifyToken": "XXXXX",

	"prices": {
		// this is the price you buy the coin
		// so program can calulate your profit

		"FTT": 53.3,

		"CELR": 0.08513,

		"POND": 0.2216663301,

		"LUNA": 16.1,

		"SXP": 5.271,

		"FTM": 0.43663,

		"NEAR": 6.59

	}

}
```

## Cronjob

-  [https://cron-job.org/](https://cron-job.org/)

- using POST method

  

![screenshot](https://raw.githubusercontent.com/cjtim/microservice-binance-cronjob/master/img/screenshot.jpg)
