import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sklearn

model = joblib.load("model_gender1")

Name = st.text_input("Full name: ")

#DOB
st.write("Date of birth:")
day = st.selectbox("Day", ['Day']+list(range(1, 32)), placeholder='Day')

month = st.selectbox("Month",['Month', 'January','February','March','April','May','June','July','August','September','October','November','December'] )
if month=='January':
    month=1
elif month=='February':
    month=2
elif month=='March':
    month=3
elif month=='April':
    month=4
elif month=='May':
    month=5
elif month=='June':
    month=6
elif month=='July':
    month=7
elif month=='August':
    month=8
elif month=='September':
    month=9
elif month=='October':
    month=10
elif month=='November':
    month=11
elif month=='December':
    month=12

import datetime 

year = st.selectbox("Year", ['Year'] + list(range(datetime.datetime.now().year, 1919, -1)))

if day != 'Day' and month != 'Month' and year != 'Year':
    DOB = datetime.date(int(year), int(month), int(day))
else:
    DOB = None

if year !='Year':
    Age=datetime.datetime.now().year - int(year)


#GENDER
Gender = st.selectbox("Gender", ["Select your gender", "Male", "Female"])
Gender_str = Gender  # Store the string value for database insertion
if Gender == 'Male':
    Gender = 0
else:
    Gender = 1


#MARITAL STATUS
Marital_status=st.selectbox("Marital status", ['Select marital status', 'Single', 'Married'])

#Phone number
Phone_number=st.text_input('Phone number')
#if len(Phone_number) != 11:
 #   st.error("Phone number must be 11 digits long.")

#CAR
car = st.selectbox('Own a car or truck', ['select:', "Yes", "No"])
car_str = car  # Store the string value for database insertion
if car == "Yes":
    car = 1
else:
    car = 0


#Health insurance
insurance = st.selectbox('Health insurance', ['Do you have health insurance?','Yes', 'No'])
insurance_str = insurance  # Store the string value for database insertion
if insurance == 'Yes':
    insurance = 0
else:
    insurance = 1



#level of education
Education = st.selectbox('Education', ['select level of education', 'Primary or less', 'Secondary', 'Higher'])
Education_str = Education  # Store the string value for database insertion
if Education == 'Primary or less':
    Education = 0
elif Education == 'Secondary':
    Education = 1
else:
    Education = 2


#PHYSICAL ADDRESS
physical_address=st.text_input('Home address: ')


ibile_to_lga = {
    'Ikorodu': ['Ikorodu'],
    'Badagry': ['Ojo', 'Amuwo-Odofin', 'Ajeromi-Ifelodun', 'Badagry'],
    'Ikeja': ['Agege', 'Ifako-Ijaiye', 'Kosofe', 'Mushin', 'Alimosho', 'Oshodi-Isolo', 'Shomolu', 'Ikeja'],
    'Lagos/Eko': ['Lagos Island', 'Lagos Mainland', 'Surulere', 'Apapa', 'Eti-Osa'],
    'Epe': ['Epe', 'Ibeju-Lekki']
}

# IBILE selection
Ibile = st.selectbox('IBILE', ['Select IBILE division'] + list(ibile_to_lga.keys()))

# LGA selection based on IBILE selection
if Ibile != 'Select IBILE division':
    LGA = st.selectbox('LGA', ['Select LGA'] + ibile_to_lga[Ibile])
else:
    LGA = st.selectbox('LGA', ['Select LGA'])

# Mapping of LGAs to their respective location divisions
location_division = {
    'Ikeja': ['Agege', 'Ifako-Ijaiye', 'Kosofe', 'Mushin', 'Alimosho', 'Oshodi-Isolo', 'Shomolu', 'Ikeja'], 
    'Badagry': ['Ojo', 'Amuwo-Odofin', 'Ajeromi-Ifelodun', 'Badagry'], 
    'Lagos/Eko': ['Lagos Island', 'Lagos Mainland', 'Surulere', 'Apapa', 'Eti-Osa'],
    'Epe': ['Epe', 'Ibeju-Lekki'], 
    'Ikorodu': ['Ikorodu']
}

# Location codes
location_code = {
    'Ikorodu': 'KD',
    'Badagry': 'BD',
    'Ikeja': 'KJ',
    'Lagos/Eko': 'LG',
    'Epe': 'EP'
}

def get_location_code(LGA):
    for location, lgas in location_division.items():
        if LGA in lgas:
            return location_code[location]
    return None


columns = ['Age', 'Gender', 'Own a car or truck', 'health insurance', 'Education']

def predict():
    if Marital_status=='Select marital status' or LGA == 'Select LGA' or not physical_address or not Phone_number or car=='select:' or Education=='select level of education' or insurance=='Do you have health insurance?' or Marital_status=='Select marital status' or Gender=='Select your gender' or not Name or DOB is None or Ibile =='Select IBILE division':
        st.error("Please fill all the fields correctly.")
    
    elif Age==0:
        st.write('Invalid Age / Age cannot be 0')
    
    elif len(Phone_number)!=11:
        st.error('Phone number has to be 11 digits')
    

    elif not Phone_number.isdigit():
        st.error("Letters can not be in Phone numbers")

    else:
        Age_int = int(Age)
        Gender_int = int(Gender)
        car_int = int(car)
        insurance_int = int(insurance)
        Education_int = int(Education)

        row = np.array([Age_int, Gender_int, car_int, insurance_int, Education_int])
        X = pd.DataFrame([row], columns=columns)
        prediction = model.predict(X)[0]

        if prediction==0:
            st.success(f'Eligible for subsidy')
            prediction='<50k'
        else:
            st.error('This user is not eligible for the IR subsidy')
            prediciton='>50k'

if st.button('Submit'):
    predict()
