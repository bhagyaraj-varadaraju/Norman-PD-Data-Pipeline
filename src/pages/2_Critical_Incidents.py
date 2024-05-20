import streamlit as st
import pandas as pd


st.set_page_config(layout="wide", page_title="Plotting Demo", page_icon="🚔")
st.title("Bar graph")

def plot_data():
    # Read the augmented data from the session state
    if st.session_state.augmented_data:
        augmented_df = pd.DataFrame(st.session_state.augmented_data, columns=["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Location", "Location Rank", "Incident Nature", "Incident Rank"])
        st.info("This plot visualises the top 10 incident natures by the frequency of their occurence during the dates you selected. You can select additional incident natures to compare them against the top 10 incident types.")
    else:
        st.error("Please download the data to visualize the incident frequency by nature for the selected dates.")
        return

    # Get incident natures sorted by the frequency of occurrence
    incident_freq_by_nature = augmented_df['Incident Nature'].value_counts()

    # Use a multiselect widget to select the incident natures
    selected_natures = st.multiselect('Select additional Incident Natures:', incident_freq_by_nature.index.tolist(), incident_freq_by_nature.index.tolist()[:10])

    if not selected_natures:
        st.error("Please select at least one incident nature.")
        return

    # Plot the selected incident natures along with the default incident natures
    selected_incident_freq_by_nature = incident_freq_by_nature[selected_natures]
    ax = selected_incident_freq_by_nature.plot(kind='bar', color='skyblue')
    ax.set_title('Incident Frequency by Nature')
    ax.set_xlabel('Nature of the Incident')
    ax.set_ylabel('Frequency')
    st.bar_chart(selected_incident_freq_by_nature, height=600)

plot_data()
