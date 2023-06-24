import json

PREDICTION_DIR = 'storage/prediction.json'
CAM_OUTPUT_DIR = 'storage/cam_photos'

def write_predict_result(data):
    with open(PREDICTION_DIR, "w") as file:
        json.dump(data, file)

def read_predict_result():
    with open(PREDICTION_DIR, "r") as file:
        data = json.load(file)
    return data
