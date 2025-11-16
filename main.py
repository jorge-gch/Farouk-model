import matplotlib
matplotlib.use('Agg')
from flask import Flask, render_template, request, jsonify
from model.model import WordGraph
from model.getData import getData
from model.draw.draw import draw_candidates_graph,draw_pdf
from model.generate_pdf import image_to_pdf
from PIL import Image
Image.MAX_IMAGE_PIXELS = None  # Desactiva la protección

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

@app.route('/generate_PDF', methods=['POST'])
def generate_PDF():
    data= request.get_json()
    text = data.get('text', '')
    quality = data.get('quality', True)
    number_of_suggestions = int(data.get('suggestions'))
    draw_pdf(wg,text,number_of_suggestions,quality)
    image_to_pdf("./static/images/candidates_graph_pdf.png","./static/images/pdf_graph.pdf")
    return jsonify({'status': "ok"})

@app.route('/update_text', methods=['POST'])
def update_text():
    data = request.get_json()
    text = data.get('text', '')
    number_of_suggestions = int(data.get('suggestions'))
    # here, we are going to predict the word
    
    user_text=text
    predict=wg.predict_next(*user_text.split())
    draw_candidates_graph(predict,text,number_of_suggestions)
    return jsonify({'data': predict})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
