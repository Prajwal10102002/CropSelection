import streamlit as st
import requests
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

# Function to retrieve data from ThingSpeak
def get_thingspeak_data():
    # Replace <CHANNEL_ID> and <READ_API_KEY> with your ThingSpeak channel ID and read API key
    url = f'https://api.thingspeak.com/channels/2468491/feeds.json?api_key=XKLRPAN06TDQ9UBH&results=1'
    response = requests.get(url)
    data = response.json()
    feeds = data['feeds']
    df = pd.DataFrame(feeds)
    return df

# Streamlit app
st.title('Crop Recommendation and Conditions Comparison')

# Header for selecting crop
st.header('Select a Crop')

# Dropdown for selecting crop
crop_label = st.selectbox('Select a Crop', ideal_conditions.index)

# Get ideal values for the selected crop
ideal_values = get_ideal_values(crop_label)

# Retrieve data from ThingSpeak
thingspeak_data = get_thingspeak_data()

if ideal_values is not None:
    # Header for ideal values
    st.header(f"Ideal values for {crop_label}:")
    st.write(f"- N: {ideal_values['N']:.2f}")
    st.write(f"- P: {ideal_values['P']:.2f}")
    st.write(f"- K: {ideal_values['K']:.2f}")
    st.write(f"- Temperature: {ideal_values['temperature']:.2f}°C")
    st.write(f"- Humidity: {ideal_values['humidity']:.2f}%")
    st.write(f"- pH: {ideal_values['ph']:.2f}")
    st.write(f"- Rainfall: {ideal_values['rainfall']:.2f} mm")

    if not thingspeak_data.empty:
    # Header for latest ThingSpeak data
        st.header("Latest ThingSpeak Data:")
        st.write(f"- N: {float(thingspeak_data['field1'].iloc[0]):.2f}")
        st.write(f"- P: {float(thingspeak_data['field2'].iloc[0]):.2f}")
        st.write(f"- K: {float(thingspeak_data['field3'].iloc[0]):.2f}")
        st.write(f"- Temperature: {float(thingspeak_data['field4'].iloc[0]):.2f}°C")
        st.write(f"- Humidity: {float(thingspeak_data['field5'].iloc[0]):.2f}%")
        st.write(f"- Soil Moisture: {float(thingspeak_data['field6'].iloc[0]):.2f}")


        # Soil management tips based on comparison
# Soil management tips based on comparison
# Soil management tips based on comparison
    st.header("Soil Management Tips:")
    for nutrient, field_name in zip(['N', 'P', 'K'], ['field1', 'field2', 'field3']):
        if field_name in thingspeak_data.columns:
            if float(thingspeak_data[field_name].iloc[0]) < ideal_values[nutrient]:
                st.write(f"⚠️ Increase {nutrient} levels: Apply fertilizers rich in {nutrient}.")
            elif float(thingspeak_data[field_name].iloc[0]) > ideal_values[nutrient]:
                st.write(f"⚠️ Decrease {nutrient} levels: Avoid over-application of {nutrient}-rich fertilizers.")
        else:
            st.write(f"⚠️ No data available for {nutrient}.")





    

else:
    st.write("Crop label not found")
