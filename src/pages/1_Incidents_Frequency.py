import streamlit as st
import pandas as pd
import seaborn as sns


st.set_page_config(layout="wide", page_title="Plotting Demo", page_icon="🚔")
st.title("Heatmap")

def plot_data():
    # Read the augmented data from the session state
    if st.session_state.augmented_data:
        augmented_df = pd.DataFrame(st.session_state.augmented_data, columns=["Date (YYYY-MM-DD)", "Day of the Week", "Time of Day", "Location", "Location Rank", "Incident Nature", "Incident Rank"])
        st.info("This plot illustrates the incident count by hour for the selected dates.")
    else:
        st.error("Please download the data to visualize the incident frequency by hour for the selected dates.")
        return

    # Calculate the hourly incident count for the selected dates
    incident_count = augmented_df.groupby(['Date (YYYY-MM-DD)', 'Time of Day']).size().unstack()
    selected_dates = augmented_df['Date (YYYY-MM-DD)'].unique()

    if incident_count.empty:
        st.error("No data available for the selected dates.")
        return

    # Plot a heatmap to visualise the hourly incident count
    ax = sns.heatmap(incident_count, cmap='coolwarm', annot=True, xticklabels=range(24), yticklabels=selected_dates)
    sns.set_theme(font_scale=0.75)
    ax.title.set_text('Incident Count by Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Date')
    st.pyplot(ax.get_figure())

plot_data()
