import json
from flask import Flask
from classifier import Classifier

classifier = Classifier()
app = Flask(__name__)
app.debug = True

@app.route('/')
def ping():
    return "OK", 200

@app.route('/api/clips/train')
def train():
    body = request.get_json()
    class_name = body['class_name']
    f = request.files['audio']
    audio = f.read()
    classifier.classify_audio(audio, class_name)
    classifier.train()
    return "0K", 200, 'text/plain'


@app.route('/api/clips/classify', methods=['POST'])
def classify():
    return "OK", 200, 'text/plain'

@app.route('/api/clips/<file_id>/feedback', methods=['POST'])
def feedback():
    class_name = request.form['class_name']
    classifier.classify_unclassified(file_id, class_name)
    classifier.train()
    return "0K", 200, 'text/plain'

if __name__ == '__main__':
    app.run(host='0.0.0.0')