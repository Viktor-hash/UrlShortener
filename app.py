from flask import Flask
from api import create_api

app = Flask(__name__)
api = create_api(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)