import streamlit as st
import pandas as pd
import altair as alt


st.set_page_config(layout="wide", page_title="Critical Incidents | Norman PD Incident Management", page_icon="🚔")
st.title("Bar graph")

if "augmented_data" not in st.session_state:
    st.session_state.augmented_data = []

def plot_data():
    # Read the augmented data from the session state
    if st.session_state.augmented_data:
        augmented_df = pd.DataFrame(st.session_state.augmented_data, columns=["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Location", "Location Rank", "Incident Nature", "Incident Rank"])
        st.info("This plot visualises the top 10 incident natures by the frequency of their occurence during the dates you selected. You can select additional incident natures to compare them against the top 10 critical incident types.")
    else:
        st.error("Please download the data to visualize the incident frequency by nature for the selected dates.")
        return

    # Get incident natures sorted by the frequency of occurrence
    incident_freq_by_nature = augmented_df['Incident Nature'].value_counts().reset_index().rename(columns={'count': 'Frequency'})

    # Use a multiselect widget to select the incident natures
    selected_natures = st.multiselect('Select additional Incident Natures:', incident_freq_by_nature['Incident Nature'].tolist(), incident_freq_by_nature['Incident Nature'].tolist()[:10])

    if not selected_natures:
        st.error("Please select at least one incident nature.")
        return

    # Plot the selected incident natures along with the default incident natures
    selected_incident_freq_by_nature = incident_freq_by_nature[incident_freq_by_nature['Incident Nature'].isin(selected_natures)]

    bar_graph = alt.Chart(selected_incident_freq_by_nature, title='Incident frequency by nature', height=500).mark_bar().encode(
        x='Incident Nature',
        y='Frequency',
        color=alt.value('#FF6464')
    ).configure_title(
        fontSize=25, anchor='middle'
    ).configure_axis(
        labelFontSize=12, titleFontSize=15
    )

    st.altair_chart(bar_graph, use_container_width=True)

plot_data()
