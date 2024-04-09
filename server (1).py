from flask import Flask, request
from googletrans import Translator

app = Flask(__name__)


@app.route("/submit", methods=["GET", "POST"])
def translator():
    if request.method == "POST":
        res = request.form
        word = res["word"]
        scr = res["scr"]
        trans = Translator()
        return trans.translate(word).text



if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")