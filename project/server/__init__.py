# coding: utf8

from project.server.kucoin_lib.kucoin import Kucoin
from project.server.table_image.render_mpl_table import render_mpl_table
from project.server.binance.binance import Binance
from project.server.line_notify.line_notify import line_notify
from pandas import DataFrame

from os import getenv
from flask_cors import CORS, cross_origin
from flask import Flask, abort, request
from io import BytesIO
from gc import collect as gc_collect

REQ_AUTH_KEY = getenv('REQ_AUTH_KEY', '')

app = Flask(__name__)

CORS(app)


@app.route("/", methods=["POST", "OPTIONS"])
@cross_origin()
def binance():
    request_json = request.get_json()
    if "Authorization" in request.headers:
        if request.headers['Authorization'] == REQ_AUTH_KEY:
            binance = Binance(
                request_json['binanceApiKey'],
                request_json['binanceSecretKey']
            )
            report = binance.asset_report(request_json['prices'])
            df = DataFrame(report)
            fig, ax = render_mpl_table(df, header_columns=0, col_width=2)
            with BytesIO() as buf:
                fig.savefig(buf, bbox_inches='tight',
                            pad_inches=0, format='png')
                buf.seek(0)
                line_notify(request_json['lineNotifyToken'],
                            '\nBinance' +
                            '\nNet Worth: ' + str(round(df.worth_usdt.sum(), 3)) +
                            '\nProfit: ' + str(round(df.profit.sum(), 3)),
                            files=buf)
                buf.close()
            del buf
            gc_collect()
            return {'status': 'success'}, 200
    return abort(403)

@app.route("/kucoin", methods=["POST", "OPTIONS"])
@cross_origin()
def kucoin():
    request_json = request.get_json()
    if "Authorization" in request.headers:
        if request.headers['Authorization'] == REQ_AUTH_KEY:
            kucoin = Kucoin(
                request_json['kucoinApiKey'],
                request_json['kucoinSecretKey'],
                request_json['kucoinPassphrase']
            )
            report = kucoin.asset_report(request_json['prices'])
            df = DataFrame(report)
            fig, ax = render_mpl_table(df, header_columns=0, col_width=2)
            with BytesIO() as buf:
                fig.savefig(buf, bbox_inches='tight',
                            pad_inches=0, format='png')
                buf.seek(0)
                line_notify(request_json['lineNotifyToken'],
                            '\nKucoin' +
                            '\nNet Worth: ' + str(round(df.worth_usdt.sum(), 3)) +
                            '\nProfit: ' + str(round(df.profit.sum(), 3)),
                            files=buf)
                buf.close()
            del buf
            gc_collect()
            return {'status': 'success'}, 200
    return abort(403)


