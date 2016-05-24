import json, audioutil
from flask import Flask, request
from classifier import Classifier
from base64 import b64decode

classifier = Classifier()
app = Flask(__name__)
app.debug = True


def get_audio(r):
    data = b64decode(r['data'])
    if(r['type'] == 'wav'):
        return data
    # convert raw pcm to wav
    return audioutil.make_wav(
        data=data,
        sample_rate=int(r['sampleRate']),
        channel_count=int(r['channelCount']),
        sample_width=int(r['sampleWidth'])
    )


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
    body = json.loads(request.body)
    class_name = body['class']
    audio = get_audio(body['audio'])
    try:
        classifier.classify_audio(audio, class_name)
        classifier.train()
        return json_response({'message': 'OK'})
    except ValueError as e:
        return server_error()


@app.route('/api/classify', methods=['POST'])
def classify():
    body = json.loads(request.body)
    audio = get_audio(body['audio'])
    try:
        res = classifier.detect_class(audio)
        return json_response(res)
    except:
        return server_error()


@app.route('/api/feedback', methods=['POST'])
def feedback():
    body = json.loads(request.body)
    file_id = body["id"]
    class_name = body["class"]
    try:
        classifier.classify_unclassified(file_id, class_name)
        classifier.train()
        return json_response({'message':'OK'})
    except ValueError as e:
        return server_error()

if __name__ == '__main__':
    app.run(host='0.0.0.0')