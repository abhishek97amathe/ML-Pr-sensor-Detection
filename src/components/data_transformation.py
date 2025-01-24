import sys
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer, robust_scale
from sklearn.pipeline import Pipeline

from src.constant import *
from src.exception import custom_exception
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    artifact_dir = os.path.join(artifact_folder)
    transformed_train_file_path = os.path.join(artifact_dir,'train.py')
    transformed_test_file_path = os.path.join(artifact_dir,'test.py')
    transformed_object_file_path = os.path.join(artifact_dir,'preprocessor.pkl')

class DataTransformation:
    def __init__(self, feature_store_file_path):
        self.data_transformation_config = DataTransformationConfig()
        self.feature_store_file_path = feature_store_file_path
        self.utils = MainUtils()

    @staticmethod
    def get_data(feature_store_file_path: str) -> pd.DataFrame:
        try:
            data = pd.read_csv(feature_store_file_path)
            data.rename(columns={'Good/Bad':TARGET_COLUMN}, inplace=True)
            return data
        
        
        except Exception as e:
            raise custom_exception(e, sys)
        
    def get_data_transformer_object(self):
        try:
            imputer_step= ('imputer', SimpleImputer(strategy='constant', fill_value=0))
            scaler_step = ('scaler', robust_scale())
            preprocessor = Pipeline(steps=[imputer_step, scaler_step])
            return preprocessor

        except Exception as e:
            raise custom_exception(e, sys) 


    def initiate_data_transformation(self):
        logging.info('Entered initiate data transformation method of the data transformation class')
        try:
            dataframe = self.get(feature_store_file_path=self.feature_store_file_path)
            x = dataframe.drop(columns=[TARGET_COLUMN])
            y = np.where(dataframe[TARGET_COLUMN])

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
            preprocessor = self.get_data_transformer_object()
            x_train_scaled = preprocessor.fit(x_train)
            x_test_scaled = preprocessor.transform(x_test)
            preprocessor_path = self.data_transformation_config.transformed_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            self.utils.save_object(file_path=preprocessor_path, object=preprocessor)

            train_arr = np.c[x_train_scaled,np.array(y_train)]
            test_arr = np.c[x_test_scaled,np.array(y_test)]

            return(train_arr, test_arr,preprocessor_path)
        
        
        except Exception as e:
            raise custom_exception(e, sys)