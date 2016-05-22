import json
from flask import Flask, request
from classifier import Classifier

classifier = Classifier()
app = Flask(__name__)
app.debug = True


def json_response(resp, status=200):
    return json.dumps(resp), status, {'Content-Type': 'application/json'}


def server_error(message=''):
    if not message:
        message = 'Error occured, please try again.'
    return json_response({'message': message}, 500)

@app.route('/')
def ping():
    return "OK", 200

@app.route('/api/train', methods=['POST'])
def train():
    class_name = request.form('class')
    f = request.files['audio']
    audio = f.read()
    try:
        classifier.classify_audio(audio, class_name)
        classifier.train()
        return json_response({'message': 'OK'})
    except ValueError as e:
        return server_error()


@app.route('/api/classify', methods=['POST'])
def classify():
    f = request.files['audio']
    audio = f.read()
    try:
        res = classifier.detect_class(audio)
        return json_response(res)
    except:
        return server_error()


@app.route('/api/feedback', methods=['POST'])
def feedback():
    file_id = request.form['id']
    class_name = request.form['class']
    try:
        classifier.classify_unclassified(file_id, class_name)
        classifier.train()
        return json_response({'message':'OK'})
    except ValueError as e:
        return server_error()

if __name__ == '__main__':
    app.run(host='0.0.0.0')