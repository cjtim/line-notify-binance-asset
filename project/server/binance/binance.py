from typing import Dict, List, Tuple
import requests
import urllib
import hmac
import hashlib
import json
from datetime import datetime
from logging import error

class Binance:
    def __init__(self, BINANCE_API_KEY: str = "",  BINANCE_SECRET_KEY: str = ""):
        self.BINANCE_API_KEY = BINANCE_API_KEY
        self.BINANCE_SECRET_KEY = BINANCE_SECRET_KEY

    def __get_json(self, path: str, query: dict = {}, timestamp=True, signature=True):
        headers = {
            'X-MBX-APIKEY': self.BINANCE_API_KEY
        }
        body = {}
        if timestamp:
            body.update({'timestamp': int(datetime.now().timestamp() * 1000)})
        params = urllib.parse.urlencode({
            **query,
            **body
        })
        if signature:
            signature = hmac.new(
                key=bytes(self.BINANCE_SECRET_KEY, 'UTF-8'),
                msg=bytes(params, 'UTF-8'),
                digestmod=hashlib.sha256).hexdigest()
            params += '&signature=' + signature
        resp = requests.get(
            f'https://api.binance.com{path}?{params}', headers=headers)
        dict_data = json.loads(resp.content)
        return dict_data

    def __get_price_usdt(self) -> Dict[str, str]:
        result = {}
        all_symbols = self.__get_json('/api/v3/ticker/price', {}, False, False)
        for i in all_symbols:
            result.update({
                i['symbol']: i['price']
            })
        return result

    def __get_asset(self) -> List[Dict[str, any]]:
        account = self.__get_json('/api/v3/account', {}, True, True)
        arr = [i for i in account['balances'] if float(
            i['free']) != 0 or float(i['locked']) != 0]
        return arr

    def asset_report(self, buy_price: Dict[str, float]) -> List[Dict[str, any]]:
        asset = self.__get_asset()
        price = self.__get_price_usdt()
        COMPARE_UNIT: str = 'USDT'
        result = []
        for i in asset:
            try:
                if i['asset'] == COMPARE_UNIT:
                    continue
                vol = float(i['free']) + float(i['locked'])
                profit = 0.00
                price_per_vol = float(price[i['asset'] + COMPARE_UNIT])
                worth_usdt = vol * price_per_vol
                if i['asset'] in buy_price:
                    profit = worth_usdt - (vol * buy_price[i['asset']])
                result.append({
                    'asset': i['asset'],
                    'current_price': round(price_per_vol , 4),
                    'vol': round(vol, 3),
                    'worth_usdt': round(worth_usdt, 3),
                    'profit': round(profit, 3)
                })
            except Exception as e:
                error(e)
        return result
