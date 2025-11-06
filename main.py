import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request, jsonify
from model.model import WordGraph
from model.getData import getData
from model.draw.draw import draw_candidates_graph   
app = Flask(__name__)

# add the model
wg = WordGraph()
text = getData()
wg.train(text)
"""how predict a word/phrase?
    user_text = ""
    wg.predict_next(*user_text.split())
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update_text', methods=['POST'])
def update_text():
    data = request.get_json()
    text = data.get('text', '')
    number_of_suggestions = int(data.get('suggestions'))
    # here, we are going to predict the word
    
    user_text=text
    predict=wg.predict_next(*user_text.split())
    draw_candidates_graph(predict,text,number_of_suggestions)
    print(f"word: {text} - Predict: {predict}")
    return jsonify({'data': predict})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
