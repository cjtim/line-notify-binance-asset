from os import getenv
import requests
import urllib
import hmac
import hashlib
import json
from datetime import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff

BINANCE_API_KEY = getenv('BINANCE_API_KEY')
BINANCE_SECRET_KEY = getenv('BINANCE_SECRET_KEY')
LINE_NOTIFY_API_KEY = getenv("LINE_NOTIFY_API_KEY")


def get_json(path: str, query: dict = {}, timestamp=True, signature=True):
    headers = {
        'X-MBX-APIKEY': BINANCE_API_KEY
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
            key=bytes(BINANCE_SECRET_KEY, 'UTF-8'),
            msg=bytes(params, 'UTF-8'),
            digestmod=hashlib.sha256).hexdigest()
        params += '&signature=' + signature

    print(params)
    resp = requests.get(
        f'https://api.binance.com{path}?{params}', headers=headers)
    [print(f'{i}: {resp.headers[i]}')
     for i in resp.headers if i.startswith('x')]
    dict_data = json.loads(resp.content)
    return dict_data


def get_price_usdt(symbols: list):
    result = {}
    all_symbols = get_json('/api/v3/ticker/price', {}, False, False)
    for i in all_symbols:
        if (i['symbol'].endswith('USDT') and
                i['symbol'][:-4] in symbols):
            result.update({
                i['symbol']: i['price']
            })
    return result


def get_asset():
    account = get_json('/api/v3/account', {}, True, True)
    arr = [i for i in account['balances'] if float(
        i['free']) != 0 or float(i['locked']) != 0]
    return arr


def asset_report():
    asset = get_asset()
    price = get_price_usdt([i['asset'] for i in asset])
    result = []
    for i in asset:
        vol = float(i['free']) + float(i['locked'])
        if i['asset'].endswith('USDT'):
            result.append({
                **i,
                'vol': vol,
                'worth_usdt': vol,
            })
        else:
            result.append({
                **i,
                'vol': vol,
                'worth_usdt': vol * float(price[i['asset'] + 'USDT']),
            })
    return result


def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])
                ) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox,
                         colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    mpl_table.set_fontsize(font_size)

    for k, cell in mpl_table._cells.items():
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w')
            cell.set_facecolor(header_color)
        else:
            cell.set_facecolor(row_colors[k[0] % len(row_colors)])
    return ax.get_figure(), ax


def line_notify(message: str, files: bytes):
    return requests.Session().post('https://notify-api.line.me/api/notify', data={
        'message': message
    }, files={'imageFile': files}, headers={
        'Authorization': 'Bearer ' + LINE_NOTIFY_API_KEY
    })
