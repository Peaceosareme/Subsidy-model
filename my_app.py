import streamlit as st
import pandas as pd

import numpy as np
import joblib
import sklearn

model=joblib.load('model_gender1')

st.title('Monthly Income Prediction')

Age=st.number_input('Age',0,150)

Gender=st.selectbox('Gender', ['','Male','Female'])
if Gender=='Male':
    Gender=0
else:
    Gender=1

car=st.selectbox('Own a car or truck',['','Yes','No'])

if car=='Yes':
    car =1
else:
    car=0

insurance=st.selectbox('health insurance',['','Yes','No'])
if insurance=='Yes':
    insurance =0
else:
    insurance=1

Education=st.selectbox('Education',['','Primary or less','Secondary', 'Higher'])

if Education=='Primary or less':
    Education=0
elif Education=='Secondary':
    Education=1
else:
    Education=2

columns=['Age','Gender','Own a car or truck','health insurance','Education']

prediction_placeholder = st.empty()
def predict():
    if Age == 0 or Gender == '' or car == '' or insurance == '' or Education == '':
        st.error('Please fill in all fields.')
    else:
        row = np.array([Age, Gender, car, insurance, Education])
        X = pd.DataFrame([row], columns=columns)
        prediction = model.predict(X)[0]

        if prediction == 0:
            prediction_placeholder.success('Income probability: <50k')
        else:
            prediction_placeholder.error('Income probability: >50k')
        import time
        time.sleep(15)
    


trigger = st.button('Predict', on_click=predict)
