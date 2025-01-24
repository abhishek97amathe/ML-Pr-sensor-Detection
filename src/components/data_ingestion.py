import os
from pyexpat import features
import sys
import numpy as np
import pandas as pd
from pymongo import MongoClient
from zipfile import Path
from src.constant import *
from src.utils.main_utils import MainUtils
from src.exception import CustomException
from dataclasses import dataclass
from src.logger import logging

@dataclass
class DataIngestionconfig:
    artifact_folder: str = os.path.join(artifact_folder)

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config= DataIngestionconfig()
        self.utils = MainUtils()

    def export_collection_as_DataFrame(self, collection_name, db_name):
        try:          
            MongoClient = MongoClient(MONGO_DB_URL)

            collection = MongoClient[db_name][collection_name]

            df = pd.DataFrame(list(collection.find()))

            if '_id' in df.columns.to_list():
                df.drop('_id', axis=1, inplace=True)

            df.replace('na', np.nan, inplace=True)

            return df
        
        except Exception as e:
             raise CustomException(e,sys)


    def export_data_into_feature_store_file_path(self)->pd.DataFrame:
        try:
            logging.info(f'Exporting from MongoDB')
            raw_file_path = self.data_ingestion_config.artifact_folder

            os.makedirs(raw_file_path, exist_ok=True)

            sensor_data = self.export_collection_as_DataFrame(
                collection_name='sensor_data', db_name='sensor_data')
            
            logging.info(f'saving exported data to :{raw_file_path}')

            feature_store_file_path = os.path.join(raw_file_path, 'wafer_fault.csv')

            sensor_data.to_csv(feature_store_file_path, index=False)

            return sensor_data
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self)-> Path:
        logging.info(f'Entered intiated_data_ingestion method of DataIngestion class')
        
        try:
            feature_store_file_path = self.export_data_into_feature_store_file_path()

            logging.info('Got the data from mongoDB')

            logging.info('exited the initiate_data_ingestion method of DataIngestion class')

            return feature_store_file_path
        
        except Exception as e:
            raise CustomException(e, sys)