# coding: utf8

from dotenv import load_dotenv
load_dotenv()
import io
from binance import *
from flask import escape, Request, jsonify, Flask, Response, request, abort
from flask_cors import CORS, cross_origin
from os import getenv

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST", "OPTIONS"])
@cross_origin()
def cloud_function(request: Request):
    if "Authorization" in request.headers:
        if request.headers['Authorization'] == getenv('REQ_AUTH_KEY'):
            report = asset_report()
            df = pd.DataFrame(report)
            fig, ax = render_mpl_table(df, header_columns=0, col_width=3.5)
            buf = io.BytesIO()
            fig.savefig(buf, bbox_inches='tight', pad_inches=0, format='png')
            buf.seek(0)
            line_notify('Net Worth: ' + str(df.worth_usdt.sum()),
                        files=buf)
            buf.close()
            return {'status': 'success'}, 200
    return abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=getenv('PORT'))


@app.errorhandler(403)
def resource_not_found(e):
    return jsonify({'status': 'Access denied'}), 403
