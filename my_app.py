import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sklearn

model = joblib.load("model_gender1")

st.title('Monthly Income Prediction')

Name = st.text_input("Name: ")

st.write("Date of birth:")
day = st.selectbox("Day", list(range(1, 32)))
month = st.selectbox("Month", list(range(1, 13)))
year = st.selectbox("Year", list(range(1920, datetime.datetime.now().year + 1)))

DOB = datetime.date(int(year), int(month), int(day))

Age = st.number_input("Age", 0, 150, step=1)

Gender = st.selectbox("Gender", [' ', "Male", "Female"])
Gender_str = Gender  # Store the string value for database insertion
if Gender == 'Male':
    Gender = 0
else:
    Gender = 1

car = st.selectbox('Own a car or truck', [' ', "Yes", "No"])
car_str = car  # Store the string value for database insertion
if car == "Yes":
    car = 1
else:
    car = 0

insurance = st.selectbox('Health insurance', [' ', 'Yes', 'No'])
insurance_str = insurance  # Store the string value for database insertion
if insurance == 'Yes':
    insurance = 0
else:
    insurance = 1

Education = st.selectbox('Education', [' ', 'Primary or less', 'Secondary', 'Higher'])
Education_str = Education  # Store the string value for database insertion
if Education == 'Primary or less':
    Education = 0
elif Education == 'Secondary':
    Education = 1
else:
    Education = 2

columns = ['Age', 'Gender', 'Own a car or truck', 'health insurance', 'Education']
prediction_placeholder = st.empty()

def predict():
    row = np.array([Age, Gender, car, insurance, Education])
    X = pd.DataFrame([row], columns=columns)
    prediction = model.predict(X)[0]

    if prediction == 0:
        prediction_placeholder.success('Income probability: <50k')
    else:
        prediction_placeholder.error('Income probability: >50k')
    import time
    time.sleep(10)
trigger = st.button('Predict', on_click=predict)
