import os,sys


from src.components.data_transformation import DataTransformation

from src.exception import CustomException
from src.logger import logging
import pandas as pd

from dataclasses import dataclass
from src.components.model_trainer import ModelTrainer

@dataclass
class DataInestionConfig:
    raw_data_path: str = os.path.join("artifact", "data.csv")

class DataIngestion:
     def __init__(self):
         self.ingestion_config = DataInestionConfig()

     def initiate_data_ingestion(self):
         logging.info("Entered the data ingestion method or component")
         try:
             df=pd.read_excel('Data_Train.xlsx')
             logging.info('Read the dataset as dataframe')


             os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
             df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)



             return self.ingestion_config.raw_data_path


         except Exception as e:
             raise CustomException(e,sys)


if __name__ =="__main__":
    obj = DataIngestion()
    data_path=obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_array = data_transformation.initiate_data_transformation(data_path)
    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_array))


