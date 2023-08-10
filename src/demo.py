import os,sys
sys.path.append('D:/Credit_Card_Fraud_Detection')
from src.pipelines.prediction import PredictionPipeline
obj=PredictionPipeline()
obj.run_pipeline()