from kucoin.client import Market, User
from typing import Dict, List
client = Market()

class Kucoin:
    def __init__(self, key='', secret='', passphrase='') -> None:
        self.user = User(key, secret, passphrase)
        self.client = Market()
        pass
    
    def __get_asset(self) -> Dict[str, float]:
        result ={}
        balances = self.user.get_account_list()
        for i in balances:
            coin_name = i['currency']
            if coin_name in result:
                    result[coin_name] = result[coin_name] + float(i['balance'])
            else:
                result.update({
                    coin_name: float(i['balance'])
                })
        return result

    def __get_price_usdt(self) -> Dict[str, float]:
        tickers = self.client.get_all_tickers()
        result: Dict[str, float] = {}
        for i in tickers['ticker']:
            if i['symbol'].endswith("USDT"):
                coin_name = i['symbol'].replace("-USDT", "")
                result.update({
                    coin_name: float(i['averagePrice'])
                })
        return result
        
    def asset_report(self, buy_price: Dict[str, any] = {}) -> List[Dict[str, any]]:
        result = []
        price = self.__get_price_usdt()
        asset = self.__get_asset()
        for coin_name, coin_unit in asset.items():
            profit = 0.00
            worth_usdt = 0.00
            if coin_name in price:
              worth_usdt = coin_unit * price[coin_name]
            if coin_name in buy_price:
                profit = worth_usdt - (coin_unit * buy_price[coin_name])
            result.append({
                'asset': coin_name,
                'current_price': round(price[coin_name] if coin_name in price else 0, 4),
                'vol': round(coin_unit, 3),
                'worth_usdt': round(worth_usdt, 3),
                'profit': round(profit, 3)
            })
        return result