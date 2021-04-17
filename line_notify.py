import requests

def line_notify(LINE_NOTIFY_API_KEY: str, message: str, files: bytes):
    return requests.Session().post('https://notify-api.line.me/api/notify', data={
        'message': message
    }, files={'imageFile': files}, headers={
        'Authorization': 'Bearer ' + LINE_NOTIFY_API_KEY
    })