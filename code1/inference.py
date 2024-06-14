import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
import requests
import boto3

def get_json_from_s3(key):
    try:
        print("About to initialize S3 client")
        s3_client = boto3.client('s3')
        print("About to load S3 object")
        json_object = s3_client.get_object(Bucket="jsonstore1", Key=key)
        json_bytes = json_object['Body'].read()
        json_string = json_bytes.decode('utf-8') 
        return json.loads(json_string) 
    except Exception as e:
        print(f"Error fetching JSON from S3: {e}")
        raise e
        
def get_model_specific_uri(base_uri, model_name):
    if ":predict" in base_uri:
        base_uri = base_uri.rsplit(':', 1)[0]
        base_uri = base_uri.rsplit('/', 1)[0] 
    return f"{base_uri}/{model_name}:predict"

def handler(request_body, context):
    print("I am in the input handler before first if")
    print(f"request body type is {type(request_body)}")
    print(f"request body content is {request_body}")

    if context.request_content_type == 'application/json':
        try:
            request_body = request_body.read().decode('utf-8')
            print("Here is before parsing the payload")
            payload = json.loads(request_body)
            key = payload['key']
            print(f"Key is {key}")

            # Fetching JSON object from S3
            json_object = get_json_from_s3(key)
            input_list = json_object.get("input")

            prediction_payload = {"inputs": {'input': input_list}}
            json_payload = json.dumps(prediction_payload)
            print("About to make prediction")

            #POST request to the model endpoint
            model_name = 'simple_model'
            rest_uri_with_model = get_model_specific_uri(context.rest_uri, model_name)
            response = requests.post(rest_uri_with_model, data=json_payload)
            print(f"Response status code: {response.status_code}")

            return _process_output(response, context)
        
        except Exception as e:
            print(f"Error in processing JSON request: {str(e)}")
            return None
    else:
        raise ValueError(f"Unsupported content type: {context.request_content_type}")

def _process_output(data, context):
    print("I am in process_output")
    if data.status_code != 200:
        raise ValueError(data.content.decode('utf-8'))
    output = json.loads(data.content.decode('utf-8'))
    print(f"Output is: {output}")
    probability = output['outputs'][0][0]
    print(f"Probability is: {probability}")
    if probability > 0.5:
        label = "Yay! Class 1"
    else:
        label = "Nay! Class 0"
        probability = 1 - probability
    prediction = json.dumps({"label": label, "probability": probability})
    byte_prediction = prediction.encode('utf-8')
    print("Got to the return")
    return byte_prediction, context.accept_header