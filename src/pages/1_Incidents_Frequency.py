import streamlit as st
import pandas as pd
import altair as alt


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
    incident_count.fillna(0, inplace=True)

    if incident_count.empty:
        st.error("No data available for the selected dates.")
        return

    # Plot a heatmap to visualise the hourly incident count
    chart_data = incident_count.reset_index().melt('Date (YYYY-MM-DD)', var_name='Time of Day', value_name='Incident Count')

    heatmap = alt.Chart(chart_data, title='Incident count by hour', height=500).mark_rect().encode(
        x='Time of Day:O',
        y='Date (YYYY-MM-DD):O',
        color=alt.Color('Incident Count:Q', scale=alt.Scale(scheme='blueorange')))

    text = heatmap.mark_text(baseline='middle'
    ).encode(text='Incident Count:Q', color=alt.value('black'), size=alt.value(16))

    chart = alt.layer(heatmap, text
    ).configure_title(
        fontSize=25, anchor='middle'
    ).configure_axis(
        labelFontSize=12, titleFontSize=15
    ).configure_legend(
        labelFontSize=12, titleFontSize=15, gradientThickness=30, gradientLength=300, titleAnchor='middle'
    )

    st.altair_chart(chart, use_container_width=True)

plot_data()
