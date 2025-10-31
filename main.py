from flask import Flask
from model.model import WordGraph

app = Flask(__name__)

@app.route('/')
def home():

    wg = WordGraph()

    text = [
        "hola como estas bro",
        "hola como estas mi tilin insano",
        "quiero saber como hacer que esto funcione",
        "como estas jejej",
        "estas bien",
        "estas bien",
        "estas bien"
    ]

    wg.train(text)

    user_text = "estas"
    return wg.predict_next(*user_text.split())

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
