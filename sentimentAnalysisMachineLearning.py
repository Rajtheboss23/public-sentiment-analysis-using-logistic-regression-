
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,classification_report
from joblib import Parallel,delayed
import joblib


# Reading CSV file of dataset using pandas libraries 
data=pd.read_csv(r"D:\News Sentiment\UserInterface\dataset.csv",encoding='ISO-8859-1',names=['target','id','date','flag','user','text'])


data.head(4)


x = data.text.values


y = data.target.values


# Splitting the data into training dataset (80% data) and testing dataset (20% data)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2)
#printing the shapes of training and testing dataset
print("Training data:\n", "X_train shape: ", x_train.shape, " y_train shape: ", y_train.shape)
print("Testing data:\n", "X_test shape: ", x_test.shape, " y_test shape: ", y_test.shape)
# Print the dataframes
print("x_train:\n", x_train)
print("y_train:\n", y_train)
print("x_test:\n", x_test)
print("y_test:\n", y_test)


vectorizer = CountVectorizer()
vectorizer.fit(x_train)
x_trainVectorized = vectorizer.transform(x_train)
x_testVectorized = vectorizer.transform(x_test)


print(x_train[0])
print(x_trainVectorized[0])


classifier = LogisticRegression(max_iter=1000)
classifier.fit(x_trainVectorized, y_train)


# Testing the accuracy of the model on the testing dataset
score = classifier.score(x_testVectorized, y_test)
print("Accuracy =", score*100)


# Saving the trained classifier and vectorizer for future use
joblib.dump(classifier,r"D:\News Sentiment\UserInterface\trained_dataset\sentiment.pkl")
joblib.dump(vectorizer,r"D:\News Sentiment\UserInterface\trained_dataset\vocabulary.pkl")