from flask import Flask
from main import client
import logging

app = Flask(__name__)
app.debug = True
logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET","POST"])
def index():
    logging.debug("index")
    return client.main()

if __name__ == "__main__":
    app.run()