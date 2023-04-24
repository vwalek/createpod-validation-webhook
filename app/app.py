from flask import Flask, request
from flask import abort

import json

app = Flask(__name__)

@app.route('/validate', methods=['GET', 'POST', 'PUT', 'HEAD'])
def validate():
    
    try:
        request_json = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        print(str(e), flush = True)
    
    print(str(request_json['request']), flush = True)

    response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
            "uid": request_json['request']['uid'],
            "allowed": True
        }
    }

    return json.dumps(response), 200, {'ContentType':'application/json'}

@app.route('/healthz')
def health():
    return json.dumps(str({'result': 'ok'})), 200, {'ContentType':'application/json'}

@app.route('/<path:path>')
def catch_all(path):
    abort(404)