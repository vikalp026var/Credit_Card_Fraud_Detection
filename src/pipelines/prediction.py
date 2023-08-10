import os
import sys
import pandas as pd
from flask import request
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.utils.main_utils import MainUtils
from src.constant import TARGET_COLUMN  # Assuming TARGET_COLUMN is defined in src.constant
from src.constant import artifact_folder  # Assuming artifact_folder is defined in src.constant
import shutil


@dataclass
class PredictionPipelineConfig:
    prediction_output_dirname: str = "prediction"
    prediction_filename: str = "prediction_file.csv"
    model_file_path: str = os.path.join(artifact_folder, "model.pkl")
    preprocessor_file_path: str = os.path.join(artifact_folder, "preprocessor.pkl")
    prediction_file_path: str = os.path.join(
        prediction_output_dirname, prediction_filename
    )
    input_path=os.path.join(artifact_folder,"test.csv")
class PredictionPipeline:
    def __init__(self,request:request):
        self.request = request
        self.utils = MainUtils()
        self.prediction_pipeline_config = PredictionPipelineConfig()

    def save_input_files(self) -> str:
        try:
            pred_file_input_dir = "predictions_artifact"
            os.makedirs(pred_file_input_dir, exist_ok=True)
            input_file = request.files['file']
            input_filename = input_file.filename  # Extract the filename
            pred_file_path = os.path.join(pred_file_input_dir, input_filename)
            input_file.save(pred_file_path)
            return pred_file_path
        except Exception as e:
            raise CustomException(e, sys)



   


    def predict(self, features):
        try:
            model = self.utils.load_object(self.prediction_pipeline_config.model_file_path)
            preprocessor = self.utils.load_object(
                self.prediction_pipeline_config.preprocessor_file_path
            )
            transformed = preprocessor.transform(features)
            pred = model.predict(transformed)
            return pred
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_predicted_dataframe(self, input_dataframe_path: pd.DataFrame):
        try:
            input_dataframe = pd.read_csv(input_dataframe_path)
            predictions = self.predict(input_dataframe)
            prediction_column_name = TARGET_COLUMN
            input_dataframe[prediction_column_name] = predictions
            target_column_mapping = {0: "No", 1: "Yes"}
            input_dataframe[prediction_column_name] = input_dataframe[
                prediction_column_name
            ].map(target_column_mapping)
            os.makedirs(
                self.prediction_pipeline_config.prediction_output_dirname, exist_ok=True
            )
            input_dataframe.to_csv(
                self.prediction_pipeline_config.prediction_file_path, index=False
            )
            logging.info("Predictions completed.")
        except Exception as e:
            raise CustomException(e, sys) from e

    def run_pipeline(self):
        try:
            input_csv_path = self.save_input_files()
            self.get_predicted_dataframe(input_csv_path)
            return self.prediction_pipeline_config
        except Exception as e:
            raise CustomException(e, sys)
