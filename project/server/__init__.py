# coding: utf8

from typing import Tuple
from project.server.kucoin_lib.kucoin import Kucoin
from project.server.table_image.render_mpl_table import render_mpl_table
from project.server.binance.binance import Binance
from project.server.line_notify.line_notify import line_notify
from pandas import DataFrame

from os import getenv
from flask_cors import CORS, cross_origin
from flask import Flask, abort, request, send_file, Request
from io import BytesIO
from gc import collect as gc_collect

REQ_AUTH_KEY = getenv('REQ_AUTH_KEY', '')

app = Flask(__name__)

CORS(app)

def extract_flag(req: Request) -> Tuple[bool, bool]:
    notify = req.args.get('notify', 'true').lower() == 'true'
    send_image = req.args.get('image', 'false').lower() == 'true'
    return notify, send_image

@app.route("/", methods=["POST", "OPTIONS"])
@cross_origin()
def binance():
    request_json = request.get_json()
    notify, send_image = extract_flag(request)
    if "Authorization" in request.headers:
        if request.headers['Authorization'] == REQ_AUTH_KEY:
            binance = Binance(
                request_json['binanceApiKey'],
                request_json['binanceSecretKey']
            )
            image: bytes = None
            report = binance.asset_report(request_json['prices'])
            df = DataFrame(report)
            fig, ax = render_mpl_table(df, header_columns=0, col_width=2)
            with BytesIO() as buf:
                fig.savefig(buf, bbox_inches='tight',
                            pad_inches=0, format='png')
                if notify:
                    buf.seek(0)
                    line_notify(request_json['lineNotifyToken'],
                                '\nBinance' +
                                '\nNet Worth: ' + str(round(df.worth_usdt.sum(), 3)) +
                                '\nProfit: ' + str(round(df.profit.sum(), 3)),
                                files=buf)
                if send_image:
                    buf.seek(0)
                    image = buf.read()
                buf.close()
            if send_image:
                return send_file(path_or_file=BytesIO(image),
                    attachment_filename='image.png',
                    mimetype='image/png')
            del buf
            del image
            gc_collect()
            return {'status': 'success'}, 200
    return abort(403)

@app.route("/kucoin", methods=["POST", "OPTIONS"])
@cross_origin()
def kucoin():
    request_json = request.get_json()
    notify, send_image = extract_flag(request)
    if "Authorization" in request.headers:
        if request.headers['Authorization'] == REQ_AUTH_KEY:
            kucoin = Kucoin(
                request_json['kucoinApiKey'],
                request_json['kucoinSecretKey'],
                request_json['kucoinPassphrase']
            )
            image: bytes = None
            report = kucoin.asset_report(request_json['prices'])
            df = DataFrame(report)
            fig, ax = render_mpl_table(df, header_columns=0, col_width=2)
            with BytesIO() as buf:
                fig.savefig(buf, bbox_inches='tight',
                            pad_inches=0, format='png')
                if notify:
                    buf.seek(0)
                    line_notify(request_json['lineNotifyToken'],
                                '\nKucoin' +
                                '\nNet Worth: ' + str(round(df.worth_usdt.sum(), 3)) +
                                '\nProfit: ' + str(round(df.profit.sum(), 3)),
                                files=buf)
                if send_image:
                    buf.seek(0)
                    image = buf.read()
                buf.close()
            if send_image:
                return send_file(path_or_file=BytesIO(image),
                    attachment_filename='image.png',
                    mimetype='image/png')
            del buf
            del image
            gc_collect()
            return {'status': 'success'}, 200
    return abort(403)


