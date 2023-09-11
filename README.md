# Flight_fare_prediction

In this project I am predicting Flight Fare of tickets based on some previous months data and make an app and deploy it on Netlify cloud platform.

# Problem Statement:

Travelling through flights has become an integral part of today’s lifestyle as more and more people are opting for faster travelling options.The flight ticket prices increase or decrease every now and then depending on various factors like timing of the flights, destination, and duration of flights various occasions such as vacations or festive season. Therefore, having some basic idea of the flight fares before planningthe trip will surely help many people save money and time.

# Goal:

The goal is to predict the fares of the flights based on different factors available in the provided dataset.

# Approach:

The classical machine learning tasks like Data Exploration, Data Cleaning, Feature Engineering, Model Building and Model Testing. Try out different machine learning algorithms that best fits for the above case.

# Model Selection:

I have use RandomForest Regression:

    1. In RandomForest i have get Training Score as 95% whereas i have got Testing Score only 83% which is a sign of Overfitting.
    2. In RandomForest i have got 83% of R2 score.

# HyperParmeter Tuning:

1. Use the Hyper-Parameter Tuning to achive the model accuracy good in nature.
2. Uses RandomSearchCV and get a Training and Testing Score 83.85% and 80.21% which is a good sign of a model.
3. After that i have save the model in pkl file so that i can use it in PyCharm for making app.
