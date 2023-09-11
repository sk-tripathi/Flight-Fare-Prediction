import numpy as np
from dataclasses import dataclass
import os,sys
from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pickle
import bz2
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifact","model.pkl")
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array):
        try:
            logging.info("split dependent and independent column")
            logging.info("datatrain array size is:{}".format(train_array.shape))
            X,y = (
                train_array.loc[:, ['Total_Stops', 'Journey_day', 'Journey_month',
            'Dep_hour', 'Dep_min', 'Arrival_hour', 'Arrival_min', 'Duration_hours',
            'Duration_mins', 'Airline_Air India', 'Airline_GoAir', 'Airline_IndiGo',
            'Airline_Jet Airways', 'Airline_Jet Airways Business',
            'Airline_Multiple carriers',
            'Airline_Multiple carriers Premium economy', 'Airline_SpiceJet',
            'Airline_Trujet', 'Airline_Vistara', 'Airline_Vistara Premium economy',
            'Source_Chennai', 'Source_Delhi', 'Source_Kolkata', 'Source_Mumbai',
            'Destination_Cochin', 'Destination_Delhi', 'Destination_Hyderabad',
            'Destination_Kolkata', 'Destination_New Delhi', 'week_day_Mon',
            'week_day_Sat', 'week_day_Sun', 'week_day_Thu', 'week_day_Tue',
            'week_day_Wed']],
            train_array.iloc[:, 2]
            )

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            reg_rf = RandomForestRegressor()
            reg_rf.fit(X_train, y_train)
            y_pred = reg_rf.predict(X_test)
            reg_rf.score(X_train, y_train)
            logging.info("this is the score {}:".format(reg_rf.score(X_test,y_test)))

            logging.info("Number of trees in random forest")
            n_estimators = [int(x) for x in np.linspace(start=100, stop=1200, num=12)]

            logging.info("NUmber of feature to consider at every split")
            max_features = ['auto', 'sqrt']

            logging.info("Maximum number of levels in tree")
            max_depth = [int(x) for x in np.linspace(5, 30, num=6)]
#6
            logging.info("Minimum number of sample required to split a node")
            min_samples_split = [2, 5,10,15]
            #10,15

            logging.info("Minimum number of samples required at each leaf node")
            min_samples_leaf = [1, 2,5,10]

            logging.info("Create the random grid")

            random_grid = {
                "n_estimators": n_estimators,
                "max_features": max_features,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
                "min_samples_leaf": min_samples_leaf
            }
            logging.info("search across 100 different combinations")
            rf_random = RandomizedSearchCV(estimator=reg_rf, param_distributions=random_grid,
                                           scoring='neg_mean_squared_error', n_iter=10, cv=5, verbose=2,
                                           random_state=42, n_jobs=1)
            rf_random.fit(X_train, y_train)

            prediction = rf_random.predict(X_test)


            logging.info("open a file,where you want to store the data")

            #file = open(r"flight_rf.pkl", 'wb')
            logging.info("Compressing Data")

            ofile = bz2.BZ2File("flight_rf.pkl", 'wb')
            pickle.dump(rf_random, ofile)
            ofile.close()

            #logging.info("dump information to that file")
            #pickle.dump(rf_random, file)

            #model = open(r"flight_rf.pkl", "rb")
            #forest = pickle.load(model)
            model = bz2.BZ2File(r"flight_rf.pkl", 'rb')
            forest = pickle.load(model)

            y_prediction = forest.predict(X_test)
            logging.info("the new accuracy is {}:".format(metrics.r2_score(y_test,y_prediction)))
            r2_square = metrics.r2_score(y_test,y_prediction)


            logging.info("finding the r2_score")
            logging.info("the r2_score is: {}".format(r2_square))
            return r2_square


        except Exception as e:
            raise CustomException(e,sys)