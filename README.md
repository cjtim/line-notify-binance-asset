# [line-notify-binance-asset](https://github.com/cjtim/line-notify-binance-asset)


## setup
- Environment variable
	- BINANCE_API_KEY
	- BINANCE_SECRET_KEY
	- LINE_NOTIFY_API_KEY
	- REQ_AUTH_KEY (allow only request headers `Authorization` with this value to proceed)
- Deploy on GCP Cloud Function
	- Runtime `Python 3.8`
	- Recommend Ram 512 mb
	- Timeout 30 sec
	- Excecuted Function `cloud_function`
	- trigger `http` method
	- Allow unauthenticated

![screenshot](https://raw.githubusercontent.com/cjtim/line-notify-binance-asset/master/img/screenshot.jpg)