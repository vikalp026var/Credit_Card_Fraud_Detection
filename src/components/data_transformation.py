import sys
import os 

sys.path.append('D:/Credit_Card_Fraud_Detection')

import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass
@dataclass  
class DataTransformationConfig:
    artifact_dir=os.path.join(artifact_folder)
    transformed_train_file_path=os.path.join(artifact_dir,'train.npy')
    transformed_test_file_path=os.path.join(artifact_dir,'test.npy')
    transformed_object_file_path=os.path.join(artifact_dir,'preprocessor.pkl')
    test_path=os.path.join(artifact_folder,"test.csv")
    train_path=os.path.join(artifact_folder,"train.csv")


class DataTransformation:
    def __init__(self,feature_store_file_path):
        self.feature_store_file_path=feature_store_file_path
        self.data_transformation_config=DataTransformationConfig()
        self.utils=MainUtils()

    @staticmethod
    def get_data(feature_store_file_path:str)->pd.DataFrame:
        try:
            data=pd.read_csv(feature_store_file_path)
            return data
        except Exception as e:
            raise CustomException(e,sys)
    def get_data_transformer_object(self):
        try:
            imputer_step=('imputer',SimpleImputer(strategy='constant',fill_value=0))
            scaler_step=('scaler',StandardScaler())
            preprocessor=Pipeline(
                steps=[
                    imputer_step,
                    scaler_step
                ]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self):
        logging.info("Entered initiate_data_transformation method of Data_Transformation class")
        try:
            dataframe = self.get_data(feature_store_file_path=self.feature_store_file_path)
            X = dataframe.drop(labels=["default payment next month"], axis=1)
            y = dataframe[TARGET_COLUMN]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=50)
            preprocessor = self.get_data_transformer_object()

            # Fit and transform the data
            X_train_scale = preprocessor.fit_transform(X_train)
            X_test_scale = preprocessor.transform(X_test)

            # Create DataFrame with scaled data and rename columns
            X_train_scale_df = pd.DataFrame(X_train_scale, columns=X_train.columns)
            X_test_scale_df = pd.DataFrame(X_test_scale, columns=X_test.columns)

            # Save the scaled DataFrames to CSV files
            X_train_scale_df.to_csv(self.data_transformation_config.train_path, index=False)
            X_test_scale_df.to_csv(self.data_transformation_config.test_path, index=False)

            # Save the preprocessor object
            preprocessor_path = self.data_transformation_config.transformed_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            self.utils.save_objects(file_path=preprocessor_path, obj=preprocessor)

            train_arr = np.c_[X_train_scale, np.array(y_train)]
            test_arr = np.c_[X_test_scale, np.array(y_test)]

            return train_arr, test_arr, preprocessor_path
        except Exception as e:
            raise CustomException(e, sys) from e




