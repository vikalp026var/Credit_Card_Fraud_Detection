import os 
import sys 
sys.path.append('D:/Credit_Card_Fraud_Detection')
from src.logger import logging
from src.exception import CustomException
from src.utils.main_utils import MainUtils
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


class Pipeline:
    def start_data_ingestion(self):
        try:
           data=DataIngestion()
           file_path=data.initiate_data_ingestion()
           return file_path
        except Exception as e:
            raise CustomException(e,sys) from e
    def start_data_transformation(self,file_path):
        try:
            data_transformer=DataTransformation(feature_store_file_path=file_path)
            train_arr, test_arr, preprocessor_path=data_transformer.initiate_data_transformation()
            return train_arr, test_arr, preprocessor_path
        except Exception as e:
            raise CustomException(e,sys) from e
    def start_model_trainer(self,train_arr, test_arr):
        try:
            model_trainer=ModelTrainer()
            score= model_trainer.initiate_model_trainer(train_array=train_arr,test_array=test_arr)
            return score
        except Exception as e:
            raise CustomException(e,sys) from e
    def run_pipeline(self):
        try:
            logging.info("Entered into the file data_ingestion of run_pipeline")
            file_path=self.start_data_ingestion()
            logging.info("Exited from  the file data_ingestion of run_pipeline")
            logging.info("Entered into the file data_transformation of run_pipeline")
            train_arr, test_arr, preprocessor_path=self.start_data_transformation(file_path=file_path)
            logging.info("Exited from the file data_transformation of run_pipeline")
            score=self.start_model_trainer(train_arr=train_arr,test_arr=test_arr)
            logging.info(f" Congratulation!! model is train completed and their score is :{score}")
        except Exception as e:
            raise CustomException(e,sys) from e
     
        
     


            