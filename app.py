from flask import *

app = Flask(__name__)
app.secret_key = "WhyNotSetTheSecretKeyToSarina?"

@app.route("/")
def index():
    return render_template("index.html", blogs=[1, 2, 3])

if __name__ == "__main__":
    app.run(debug=True, port=12345)
