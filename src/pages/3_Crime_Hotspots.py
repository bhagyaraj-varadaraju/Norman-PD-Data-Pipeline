import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(layout="wide", page_title="Plotting Demo", page_icon="🚔")
st.title("Bar chart")

def plot_data():
    # Read the augmented data from the session state
    if st.session_state.augmented_data:
        augmented_df = pd.DataFrame(st.session_state.augmented_data, columns=["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Location", "Location Rank", "Incident Nature", "Incident Rank"])
        st.info("This graph illustrates the incident frequency by the location of the incident during the selected dates. You can select additional locations to compare them against the top 25 hotspots.")
    else:
        st.error("Please download the data to visualize the incident frequency by location for the selected dates.")
        return

    # Get the incident frequency sorted by the location of the incident
    incident_freq_by_location = augmented_df['Location'].value_counts().reset_index().rename(columns={'Location': 'Incident Location', 'count': 'Frequency'})

    # Use a multiselect widget to select the locations
    selected_locations = st.multiselect('Select additional Locations:', incident_freq_by_location['Incident Location'].tolist(), incident_freq_by_location['Incident Location'].tolist()[:25])

    if not selected_locations:
        st.error("Please select at least one location.")
        return

    # Plot the incident frequency by the location of the incident
    selected_incident_freq_by_location = incident_freq_by_location[incident_freq_by_location['Incident Location'].isin(selected_locations)]

    bar_chart = alt.Chart(selected_incident_freq_by_location, title='Incident frequency by location', height=500).mark_bar().encode(
        x='Incident Location',
        y='Frequency',
        color=alt.value('#FFC864')
    ).configure_title(
        fontSize=25, anchor='middle'
    ).configure_axis(
        labelFontSize=12, titleFontSize=15
    )

    st.altair_chart(bar_chart, use_container_width=True)

plot_data()
