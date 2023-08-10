import sys 
import os 
sys.path.append('D:/Credit_Card_Fraud_Detection')
import pandas as pd 
import numpy as np 
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV
# from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass


@dataclass
class ModelTrainConfig:
    train_model_path = os.path.join(artifact_folder, 'model.pkl')
    artifact_folder:str=os.path.join(artifact_folder,'train.csv')
    # model_config_file_path = os.path.join('config', 'model.yaml')


class ModelTrainer:
    def __init__(self):
        self.model_train_config = ModelTrainConfig()
        self.utils = MainUtils()
        self.models = {
            # 'GaussianNB': GaussianNB(),
          #   'XGBClassofier': XGBClassifier(),
            'SVC': SVC()
        }
        # self.artifact_folder=artifact_folder

    def evaluate_models(self, X, y, models):
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
            # df=pd.DataFrame(X_train)
            # df.to_csv(self.model_train_config.artifact_folder)
            report = {}
            for model_name, model in models.items():
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                k = accuracy_score(y_test, y_pred)
                report[model_name] = k
            return report
        except Exception as e:
            raise CustomException(e, sys)

    def best_model(self, X, y):
        try:
            report = self.evaluate_models(X, y, models=self.models)
            print(report)
            best_model_score = max(sorted(report.values()))
            best_model_name = list(report.keys())[
                list(report.values()).index(best_model_score)
            ]
            best_model_object = self.models[best_model_name]

            return best_model_score, best_model_name, best_model_object
        except Exception as e:
            raise CustomException(e, sys)

    def finetune_best_model(self, best_model_name, best_model_object, X_train, y_train):
        try:
            X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.33, random_state=42)
            # model_param_grid ={"var_smoothing":[1e-9,0.1,0.001,0.5,0.05,0.01,1e-8,1e-7,1e-6,1e-10,1e-11]}
            model_param_grid = {
            'C': [0.1, 1, 10],
             'kernel': ['linear', 'rbf', 'poly'],
             'gamma': ['scale', 'auto']
}

            best_model_tune = GridSearchCV(best_model_object, param_grid=model_param_grid, cv=10, verbose=3)
            best_model_tune.fit(X_train, y_train)
            y_pred = best_model_tune.predict(X_test)
            print(best_model_tune.best_params_)
            logging.info("Model Accuracy by doing the Hypertuning")
            score = accuracy_score(y_pred, y_test)
          #   logging.info("Best model name %s and score: %s", best_model_name, )
            return score
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info(f"Splitting training and testing input and target feature")
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            # logging.info("Save the train file into artifact folder")
            # train_file=pd.DataFrame(train_array)
            # train_path=os.path.join(self.artifact_folder)
            # train_file.to_csv(train_path,index=False)
            # df=pd.DataFrame(train_array)
            # # os.makedirs(os.path.dirname(self.model_train_config.artifact_folder),exist_ok=True)
            # df.to_csv(self.model_train_config.artifact_folder,index=False)
            
            logging.info(f"Extracting model config file path")
            
            best_model_score, best_model_name, best_model_object = self.best_model(X=x_train, y=y_train)

            score = self.finetune_best_model(
                best_model_name=best_model_name,
                best_model_object=best_model_object,
                X_train=x_train,
                y_train=y_train
            )

            best_model_object.fit(x_train, y_train)
            y_pred = best_model_object.predict(x_test)
            best_model_score = accuracy_score(y_test, y_pred)

            logging.info(f"Best model name {best_model_name} and score: {best_model_score}")

            logging.info(f"Saving model at path: {self.model_train_config.train_model_path}")

            os.makedirs(os.path.dirname(self.model_train_config.train_model_path), exist_ok=True)
            

            self.utils.save_objects(
                file_path=self.model_train_config.train_model_path,
                obj=best_model_object
            )

            return best_model_score

        except Exception as e:
            raise CustomException(e, sys)
