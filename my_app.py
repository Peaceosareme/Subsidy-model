import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sklearn

mycursor = mydb.cursor()
conn=st.connection('mysql', type='sql')

model = joblib.load("C:/Users/Peace Ikhile/subsidy model/model_gender1")

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

def generate_unique_id():
    while True:
        user_id = ''
        for _ in range(10):
            if np.random.choice([0, 1]):
                user_id += chr(np.random.randint(48, 58))  # Add a random digit
            else:
                user_id += chr(np.random.randint(65, 91))  # Add a random alphabet

        # Check if the generated ID already exists in the database
        mycursor.execute("SELECT user_id FROM tele_users WHERE user_id = %s", (user_id,))
        result = mycursor.fetchone()

        if not result:
            return user_id 
        
        
def predict(Name, DOB, Age, Gender, car, insurance, Education):
    Age_int = int(Age)
    Gender_int = int(Gender)
    car_int = int(car)
    insurance_int = int(insurance)
    Education_int = int(Education)

    row = np.array([Age_int, Gender_int, car_int, insurance_int, Education_int])
    X = pd.DataFrame([row], columns=columns)
    prediction = model.predict(X)[0]

    if prediction == 0:
        prediction='<50k'
        prediction_placeholder.success('Income probability: <50k')
    else:
        prediction='>50k'
        prediction_placeholder.error('Income probability: >50k')
    prediction_str = str(prediction)

    sql = "INSERT INTO tele_users (user_id, Name, DOB, Age, Gender, car, insurance, Education, prediction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    user_id = generate_unique_id() 
    val = (user_id, Name, DOB, Age_int, Gender_str, car_str, insurance_str, Education_str, prediction_str)
    mycursor.execute(sql, val)
    mydb.commit()

trigger = st.button('Predict', on_click=lambda: predict(Name, DOB, Age, Gender, car, insurance, Education))
