import streamlit as st
import pandas as pd
import seaborn as sns


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

    # Calculate the hourly incident count for the selected dates
    incident_count = augmented_df.groupby(['Date (YYYY-MM-DD)', 'Time of Day']).size().unstack()
    selected_dates = augmented_df['Date (YYYY-MM-DD)'].unique()

    # Plot a heatmap to visualise the hourly incident count
    ax = sns.heatmap(incident_count, cmap='coolwarm', annot=True, xticklabels=range(24), yticklabels=selected_dates)
    sns.set(font_scale=2.0)
    ax.title.set_text('Incident Count by Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Date')
    ax.figure.set_size_inches(20, 10)
    st.pyplot(ax.figure)

plot_data()
