from flask import Flask, request
from flask import abort

import json
import base64
import os
import time

app = Flask(__name__)

# method to dump the request yaml and approve the request
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

# method to dump the yaml and add custom annotation that it was checked
@app.route('/mutate', methods=['GET', 'POST', 'PUT', 'HEAD'])
def mutate():
    try:
        request_json = json.loads(request.data.decode('utf-8'))
    except Exception as e:
        print(str(e), flush = True)

    print(str(request_json), flush = True)

    patch = "[{ \"op\": \"add\", \"path\": \"/metadata/labels/custom-webhook\", \"value\": \"true\" }]"
    patch_bytes = patch.encode('ascii')
    patch_base64_bytes = base64.b64encode(patch_bytes)
    patch_base64 = patch_base64_bytes.decode('ascii')

    print(request_json['request'], flush = True)

    response = {
        "apiVersion": "admission.k8s.io/v1",
        "kind": "AdmissionReview",
        "response": {
          "uid": request_json['request']['uid'],
          "allowed": True,
          'patch': patch_base64,
          'patchType': "JSONPatch",
        }
    }

    return json.dumps(response), 200, {'ContentType':'application/json-patch+json'} 
    

@app.route('/healthz')
def health():
    return json.dumps(str({'result': 'ok'})), 200, {'ContentType':'application/json'}

@app.route('/<path:path>')
def catch_all(path):
    abort(404)