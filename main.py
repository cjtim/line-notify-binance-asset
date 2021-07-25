# coding: utf8

from line_notify import line_notify
from get_image import render_mpl_table
import pandas as pd
from os import getenv
from flask_cors import CORS, cross_origin
from flask import Request, Flask, Response, abort, request
from binance import Binance
import io, gc

REQ_AUTH_KEY = getenv('REQ_AUTH_KEY')
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST", "OPTIONS"])
@cross_origin()
def cloud_function():
    request_json = request.get_json()
    if "Authorization" in request.headers:
        if request.headers['Authorization'] == REQ_AUTH_KEY:
            binance = Binance(
                request_json['binanceApiKey'],
                request_json['binanceSecretKey']
            )
            report = binance.asset_report(request_json['prices'])
            df = pd.DataFrame(report)
            fig, ax = render_mpl_table(df, header_columns=0, col_width=2)
            with io.BytesIO() as buf:
                fig.savefig(buf, bbox_inches='tight',
                            pad_inches=0, format='png')
                buf.seek(0)
                line_notify(request_json['lineNotifyToken'],
                            '\nNet Worth: ' + str(round(df.worth_usdt.sum(), 3)) +
                            '\nProfit: ' + str(round(df.profit.sum(), 3)),
                            files=buf)
                buf.close()
            del buf
            gc.collect()
            return {'status': 'success'}, 200
    return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=getenv('PORT'))
