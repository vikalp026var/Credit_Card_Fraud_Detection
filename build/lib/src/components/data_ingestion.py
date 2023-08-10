import sys
import os 
import numpy as np 
import pandas as pd 
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
# import sys
# import os

# Add the project root directory to the Python path
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)



@dataclass
class DataIngestionConfig:
    artifact_folder:str=os.path.join(artifact_folder)

class DataIngestion:
    def __init__(self) :
        self.data_ingestion_config=DataIngestionConfig()
        self.utils=MainUtils()
    def export_collection_as_dataframe(self,collection_name,db_name):
        try:
            mongo_client=MongoClient(MONGO_DB_URL)
            collection=mongo_client[db_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "EDUCATION,MARRIAGE,AGE" in df.columns.to_list():
                df.drop(columns=['EDUCATION',"MARRIAGE","AGE"],axis=1)
                return df 
        except Exception as e:
            raise CustomException(e,sys) from e 
    def export_colection_into_feature_store_file_path(self)->pd.DataFrame:
        try:
             logging.info(f"Exporting the data from mongodb starting .....")
             logging.info(f"Exporting the data from mongodb starting .....")
             raw_file_path=self.data_ingestion_config.artifact_folder
             os.makedirs(raw_file_path,exist_ok=True)
             sensor_data=self.export_collection_as_dataframe(collection_name=MONGO_COLLECTION_NAME,db_name=MONGO_DATABASE_NAME)
             logging.info("Now the data is suuccessfully export from mongodb and now form the csv file and save into artifact folder ")
             file_path=os.path.join(raw_file_path,"credit.csv")
             sensor_data.to_csv(file_path,index=False)
             return file_path
        except Exception as e:
            raise CustomException(e,sys) from e
    def initiate_data_indestion(self)->Path:
        logging.info("Entererd into initiate data ingestion method of Data ingestion class")
        try:
            feature_store_file_path=self.export_colection_into_feature_store_file_path()
            logging.info("Got the data from mongodb")
            logging.info(
                "Exited initiate_data_ingestion method of Data_Ingestion class"
            )
            return feature_store_file_path
        except Exception as e:
            raise CustomException(e,sys) from e
    