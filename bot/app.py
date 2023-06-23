from flask import Flask
from main import client

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return client.main()

if __name__ == "__main__":
    app.run()