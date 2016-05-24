import json, audioutil
from flask import Flask, request
from classifier import Classifier
from base64 import b64decode

classifier = Classifier()
app = Flask(__name__)
app.debug = True


def get_audio(r):
    print 'retrieving audio data'
    data = b64decode(r['data'])
    if(r['type'] == 'wav'):
        return data
    # convert raw pcm to wav
    print 'making wave format'
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
    body = json.loads(request.data)
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
    print 'classify request'
    body = json.loads(request.data)
    audio = get_audio(body['audio'])
    print 'wave audio retrieved'
    try:
        print 'running classifier'
        res = classifier.detect_class(audio)
        print 'classify response', res
        return json_response(res)
    except:
        return server_error()


@app.route('/api/feedback', methods=['POST'])
def feedback():
    print 'feedback request'
    body = json.loads(request.data)
    file_id = body["id"]
    class_name = body["class"]
    print 'feedback id', file_id, 'class', class_name
    try:
        print 'classify unclassified'
        classifier.classify_unclassified(file_id, class_name)
        print 'retrain classifier'
        classifier.train()
        print 'classifier trained'
        return json_response({'message':'OK'})
    except ValueError as e:
        return server_error()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
