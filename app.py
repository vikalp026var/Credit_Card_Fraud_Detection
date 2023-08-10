from flask import Flask ,render_template,request,app,send_file,jsonify
from src.exception import CustomException
from src.logger import logging
import os,sys 
sys.path.append('D:/Credit_Card_Fraud_Detection')
from src.pipelines.training import Pipeline
from src.pipelines.prediction import PredictionPipeline

app=Flask(__name__)
@app.route("/")
def home():
    return render_template('index.html')
@app.route('/train')
def train():
    try:
        train_pipeline=Pipeline()
        train_pipeline.run_pipeline()
        return render_template('index.html')
    except Exception as e:
        raise CustomException(e,sys)
@app.route('/predict',methods=['POST','GET'])
def upload():
    try:
        if request.method=='POST':
            prediction_pipeline=PredictionPipeline(request)
            prediction_file_detail=prediction_pipeline.run_pipeline()
            logging.info("prediction completed .Downloading prediction file")
            return send_file(prediction_file_detail.prediction_file_path,download_name=prediction_file_detail.prediction_file_path,as_attachment=True)
        else:
            return render_template('index.html')
    except Exception as e:
        raise CustomException(e,sys) from e
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5050,debug=True)