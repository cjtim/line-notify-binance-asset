from os import getenv
from project.server import app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=getenv('PORT', 8080))