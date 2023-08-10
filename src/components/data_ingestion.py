import os
import sys
import pandas as pd
from pymongo import MongoClient
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Add the project root directory to the Python path
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

@dataclass
class DataIngestionConfig:
    artifact_folder: str = os.path.join(artifact_folder)

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.utils = MainUtils()

    def export_collection_as_dataframe(self, collection_name, db_name):
        try:
            mongo_client = MongoClient(MONGO_DB_URL)
            collection = mongo_client[db_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            # Check if specific columns exist and drop them if present
            columns_to_drop = ['EDUCATION', 'MARRIAGE', 'AGE','_id']
            if all(col in df.columns for col in columns_to_drop):
                df = df.drop(columns=columns_to_drop, axis=1)
            # X=df.iloc[:,:-1]
            # y=df.iloc[:,-1]
            # X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.33,random_state=42)
            # X_train=pd.DataFrame(X_train)
            # X_train.to_csv(self.data_ingestion_config.artifact_folder,index=False)
            return df

        except Exception as e:
            raise CustomException(e, sys) from e

    def export_collection_into_feature_store_file_path(self) -> str:
        try:
            logging.info("Exporting the data from MongoDB...")
            raw_file_path = self.data_ingestion_config.artifact_folder
            os.makedirs(raw_file_path, exist_ok=True)
            sensor_data = self.export_collection_as_dataframe(collection_name=MONGO_COLLECTION_NAMES, db_name=MONGO_DATABASE_NAMES)
            logging.info("Successfully exported data from MongoDB. Now converting to CSV and saving it to the artifact folder.")
            file_path = os.path.join(raw_file_path, "credit.csv")
            sensor_data.to_csv(file_path, index=False)
            return file_path

        except Exception as e:
            raise CustomException(e, sys) from e

    def initiate_data_ingestion(self) -> str:
        logging.info("Entered the initiate data ingestion method of DataIngestion class")
        try:
            feature_store_file_path = self.export_collection_into_feature_store_file_path()
            logging.info("Successfully retrieved data from MongoDB")
            logging.info("Exited the initiate_data_ingestion method of DataIngestion class")
            return feature_store_file_path

        except Exception as e:
            raise CustomException(e, sys) from e
