import streamlit as st
import pandas as pd

# Load the dataset
data = pd.read_csv('Crop_recommendation.csv')

# Group data by crop type and calculate the mean values for each feature
ideal_conditions = data.groupby('label').mean()

# Function to get the ideal values for a given crop
def get_ideal_values(crop_label):
    if crop_label in ideal_conditions.index:
        values = ideal_conditions.loc[crop_label]
        return values
    else:
        return None

# Streamlit app
st.title('Ideal Crop Growing Conditions')

# Dropdown for selecting crop
crop_label = st.selectbox('Select a Crop', ideal_conditions.index)

# Get ideal values for the selected crop
ideal_values = get_ideal_values(crop_label)

if ideal_values is not None:
    st.write(f"Ideal values for {crop_label}:")
    st.write(f"N: {ideal_values['N']:.2f}")
    st.write(f"P: {ideal_values['P']:.2f}")
    st.write(f"K: {ideal_values['K']:.2f}")
    st.write(f"Temperature: {ideal_values['temperature']:.2f}°C")
    st.write(f"Humidity: {ideal_values['humidity']:.2f}%")
    st.write(f"pH: {ideal_values['ph']:.2f}")
    st.write(f"Rainfall: {ideal_values['rainfall']:.2f} mm")
else:
    st.write("Crop label not found")
