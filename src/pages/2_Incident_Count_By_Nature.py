import streamlit as st
import pandas as pd


st.set_page_config(page_title="Plotting Demo", page_icon="📈")
st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

def plot_data():
    # Read the augmented data from the csv file
    augmented_df = pd.read_csv("../resources/normanpd_augmented.csv", sep="\t")

    # Plot the incident frequency by the nature of the incident
    incident_freq_by_nature = augmented_df['Incident Nature'].value_counts()
    ax = incident_freq_by_nature.plot(kind='bar', color='skyblue')
    ax.set_title('Incident Frequency by Nature')
    ax.set_xlabel('Nature of the Incident')
    ax.set_ylabel('Frequency')
    st.bar_chart(incident_freq_by_nature)

plot_data()
