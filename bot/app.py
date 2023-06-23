from flask import Flask, request
from main import client

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    req = request
    return client.main(req)

if __name__ == "__main__":
    app.main()