import os,sys
from src.logger import logging
from src.exception import CustomException
import numpy as np
import pandas as pd
from dataclasses import dataclass
import warnings
warnings.simplefilter('ignore')
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def initiate_data_transformation(self,train_path):
        try:
            train_df = pd.read_csv(train_path)
            logging.info("Read train and test data completed")

            train_df.dropna(inplace=True)
            logging.info("Deleting the null row")

            logging.info("converting string dtype to datetime")
            train_df['Date_of_Journey'] = pd.to_datetime(train_df['Date_of_Journey'])

            train_df['Journey_day'] = pd.to_datetime(train_df.Date_of_Journey, format="%d/%m/%Y").dt.day

            train_df['Journey_month'] = pd.to_datetime(train_df.Date_of_Journey, format="%d/%m/%Y").dt.month
            train_df['Journey_year'] = pd.to_datetime(train_df.Date_of_Journey, format="%d/%m/%Y").dt.year

            logging.info("Since we have converted Date_of_Journey coulmn into integers,Now we can drop as it is of no use")
            train_df.drop(['Date_of_Journey'], axis=1, inplace=True)

            logging.info("Extracting Hours")
            train_df['Dep_hour'] = pd.to_datetime(train_df['Dep_Time']).dt.hour

            logging.info("Extracting Minutes")
            train_df['Dep_min'] = pd.to_datetime(train_df['Dep_Time']).dt.minute

            logging.info("Now we can Drop Dep_Time as it is of no use")
            train_df.drop(['Dep_Time'], axis=1, inplace=True)

            logging.info("Extracting Hours")
            train_df['Arrival_hour'] = pd.to_datetime(train_df['Arrival_Time']).dt.hour

            logging.info("Extracting Minutes")
            train_df['Arrival_min'] = pd.to_datetime(train_df['Arrival_Time']).dt.minute

            logging.info("Now we can Drop Dep_Time as it is of no use")
            train_df.drop(['Arrival_Time'], axis=1, inplace=True)

            logging.info("Assigning and converting Duration column into list")
            duration = list(train_df['Duration'])

            for i in range(len(duration)):
                if len(duration[i].split()) != 2:  # check if duration conatins only hour or mins
                    if 'h' in duration[i]:
                        duration[i] = duration[i].strip() + ' 0m'  # add 0 min
                    else:
                        duration[i] = '0h ' + duration[i]
            duration_hours = []
            duration_mins = []

            for i in range(len(duration)):
                duration_hours.append(int(duration[i].split(sep='h')[0]))  # Extract hours from duration
                duration_mins.append(int(duration[i].split(sep='m')[0].split()[-1]))  # Extract hours from duration

            train_df["Duration_hours"] = duration_hours
            train_df["Duration_mins"] = duration_mins
            train_df.drop(['Duration'], axis=1, inplace=True)

            week_day = []
            logging.info("Loop over each row of the dataframe using the iterrows method")
            for i, row in train_df.iterrows():
                # Combine the year, month and day columns into a single integer
                ymd = row['Journey_year'] * 10000 + row['Journey_month'] * 100 + row['Journey_day']
                # Convert the integer to a datetime.datetime object using the to_datetime function and specifying the format
                dt = pd.to_datetime(ymd, format='%Y%m%d')
                # Extract the date part of the datetime object using the date method
                d = dt.date()
                # Format the date as a weekday name using the strftime method and the %a directive
                w = d.strftime('%a')
                # Append the weekday name to the week_day list
                week_day.append(w)
            train_df['week_day'] = week_day

            logging.info("As Airline and week_day is Nominal Categorical data we will perform OneHotEncoding")
            Airline = train_df[["Airline"]]
            Airline = pd.get_dummies(Airline, drop_first=True)
            Airline.head()
            Week_day = train_df[["week_day"]]
            Week_day = pd.get_dummies(Week_day, drop_first=True)
            Week_day.head()

            logging.info("As Source is Nominal Categorical data we will perform OneHotEncoding")

            Source = train_df[['Source']]
            Source = pd.get_dummies(Source, drop_first=True)
            Source.head()

            logging.info("As Destination is Nominal Categorical data we will perform OneHotEncoding")

            Destination = train_df[['Destination']]
            Destination = pd.get_dummies(Destination, drop_first=True)
            Destination.head()

            train_df.replace({'non-stop': 0, '1 stop': 1, '2 stops': 2, '3 stops': 3, '4 stops': 4}, inplace=True)
            logging.info("As atleast 80% of Additional_Info value is No info so we can remove it")
            train_df.drop("Additional_Info", axis=1, inplace=True)

            df_train = pd.concat([train_df, Airline, Source, Destination, Week_day], axis=1)
            df_train.drop(['Airline', "Destination", 'Source', 'week_day'], axis=1, inplace=True)

            logging.info("dataTransformation completed ")
            logging.info("data train columns {}".format(df_train.columns))
            df_train

            return df_train




        except Exception as e:
            raise CustomException(e,sys)