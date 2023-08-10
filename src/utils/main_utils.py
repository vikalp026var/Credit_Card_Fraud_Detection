import sys
import os
sys.path.append('D:/Credit_Card_Fraud_Detection')

# Add the project root directory to the Python path
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

import pandas as pd
import pickle
import boto3
import yaml
from src.constant import *
from src.exception import CustomException
from src.logger import logging

# Add the project directory to the Python path
AWS_S3_BUCKET_NAME="Credit_Card_Fraud_Detection"
MONGO_DATABASE_NAME="Credit_Card"
MONGO_COLLECTION_NAME='collection'
TARGET_COLUMN='default payment next month'
MONGO_DB_URL="mongodb+srv://vikalp026varshney:Vikalp026var@cluster0.r31hq0n.mongodb.net/?retryWrites=true&w=majority"
MODEL_FILE_NAME="model"
MODEL_FILE_EXTENSION=".pkl"
artifact_folder="artifacts"

class MainUtils:
    def __init__(self) -> None:
        pass

    def read_yaml_file(self, filename: str) -> dict:
        try:
            with open(filename, "r") as yaml_file:  # Use "r" for reading text files
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise CustomException(e, sys) from e

    def read_schema_config_file(self) -> dict:
        try:
            schema_config = self.read_yaml_file(os.path.join("config", "schema.yaml"))
            return schema_config
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def save_objects(file_path: str, obj: object) -> None:
        logging.info("Entered the save_objects method of MainUtils class")
        try:
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)
            logging.info("Exited the save_objects method of MainUtils class")
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def load_object(file_path):
        try:
            with open(file_path, 'rb') as file_obj:
                return pickle.load(file_obj)
        except Exception as e:
            # Log or raise a CustomException here to handle loading errors properly
            logging.error('Exception occurred while loading object from file:', e)
            raise CustomException(e, sys) from e
