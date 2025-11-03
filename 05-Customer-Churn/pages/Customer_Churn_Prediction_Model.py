# Load libraries
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix, classification_report, f1_score, precision_score, recall_score, roc_auc_score, roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

# Set page config
st.set_page_config(page_title = 'Customer Churn Prediction Model', layout = 'wide')

# Title and description
'''
# Customer Churn Prediction Model
This page will present a linear regression model used to predict Churn given the variables in this table.
This page will also allow users to choose the values for each variable to see if a customer would churn or not.
'''

df = pd.read_csv('/Users/kiroshenouda/Desktop/COMPSCI/DATASETS/Customer Churn/customer_churn_dataset-training-master.csv')
X = df.drop('Churn', axis = 1)
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 12345)
log_reg_model = LogisticRegression(X_train, y_train)
y_pred = log_reg_model.predict(X_test)
conf_mat = confusion_matrix(y_pred, y_test)
st.write(conf_mat)