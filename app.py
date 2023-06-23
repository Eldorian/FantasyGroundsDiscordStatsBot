from flask import Flask
from main import client
import sys
import logging

app = Flask(__name__)
app.debug = True
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

@app.route("/", methods=["POST"])
def index():
    logging.debug("index")
    return client.main()

if __name__ == "__main__":
    app.run()