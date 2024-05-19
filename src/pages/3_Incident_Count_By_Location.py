import streamlit as st
import pandas as pd


st.set_page_config(layout="wide", page_title="Plotting Demo", page_icon="🚔")
st.markdown("# Bar Chart")
st.write("""This bar graph illustrates the incident frequency by the location of the incident during the selected dates.""")

def plot_data():
    # Read the augmented data from the csv file
    try:
        augmented_df = pd.read_csv("./resources/normanpd_augmented.csv", sep="\t")
    except FileNotFoundError:
        st.error("Please download the data first.")
        return

    # Get the incident frequency sorted by the location of the incident
    incident_freq_by_location = augmented_df['Location'].value_counts()

    # Use a multiselect widget to select the locations
    selected_locations = st.multiselect('Select additional Locations:', incident_freq_by_location.index.tolist(), incident_freq_by_location.index.tolist()[:30])

    if not selected_locations:
        st.error("Please select at least one location.")
        return

    # Plot the incident frequency by the location of the incident
    selected_incident_freq_by_location = incident_freq_by_location[selected_locations]
    ax = selected_incident_freq_by_location.plot(kind='bar', color='Green')
    ax.set_title('Incident Frequency by Location')
    ax.set_xlabel('Location of the Incident')
    ax.set_ylabel('Frequency')
    st.bar_chart(selected_incident_freq_by_location, height=600)

plot_data()
