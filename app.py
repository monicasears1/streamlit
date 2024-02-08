import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Load the dataset directly from GitHub's raw content
file_url = 'https://raw.githubusercontent.com/monicasears1/streamlit/main/Power%201.csv'
df = pd.read_csv(file_url, parse_dates=['timestamp'])

# Convert timestamp to proper datetime and remove timezone info
df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)

# App title
st.title('In-Depth Blockchain Data Analysis App')

# Display a statistical summary
if st.checkbox('Show statistical summary'):
    st.write(df.describe())

# Time Filtering
st.sidebar.header('Time Filtering')
time_filter = st.sidebar.selectbox('Select Time Period', ['Today', 'Yesterday', 'Last 7 Days', 'Last 30 Days', 'Last Month'])

# Time filtering logic
today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
if time_filter == 'Today':
    start_date = today
elif time_filter == 'Yesterday':
    start_date = today - timedelta(days=1)
elif time_filter == 'Last 7 Days':
    start_date = today - timedelta(days=7)
elif time_filter == 'Last 30 Days':
    start_date = today - timedelta(days=30)
elif time_filter == 'Last Month':
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    start_date = first_day_last_month
    today = first_day_last_month + timedelta(days=(today.replace(day=1) - first_day_last_month).days - 1)

filtered_df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= today)]

# Site Level Filtering
st.sidebar.header('Site Level Filtering')
all_sites_option = "All Sites"
sites = [all_sites_option] + list(df['client_name'].unique())
site_to_filter = st.sidebar.selectbox('Which site to filter by?', sites)
if site_to_filter != all_sites_option:
    filtered_df = filtered_df[filtered_df['client_name'] == site_to_filter]

if st.sidebar.button('Apply Site and Time Filter'):
    st.write(filtered_df)
else:
    st.write(df)

# Data Visualization
st.header('Data Visualization')
chart_type = st.selectbox('Select chart type', ['Line Chart', 'Histogram', 'Box Plot', 'Heatmap', 'Correlation Chart'])

# Define custom color palette
custom_colors = ['dimgrey', 'mediumspringgreen', 'cyan', 'black', 'white']
sns.set_palette(custom_colors)

if chart_type == 'Line Chart':
    st.line_chart(filtered_df[['avg_power', 'active_miners', 'hash_rate']])
elif chart_type == 'Histogram':
    column_to_plot = st.selectbox('Select column to plot', ['avg_power', 'active_miners', 'hash_rate'])
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df[column_to_plot], kde=True, color='mediumspringgreen')
    st.pyplot(plt)
elif chart_type == 'Box Plot':
    column_to_plot = st.selectbox('Select column for box plot', ['avg_power', 'active_miners', 'hash_rate'])
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=filtered_df[column_to_plot], color='cyan')
    st.pyplot(plt)
elif chart_type == 'Heatmap':
    corr = filtered_df[['avg_power', 'active_miners', 'hash_rate']].corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap=sns.color_palette(custom_colors, as_cmap=True))
    st.pyplot(plt)
elif chart_type == 'Correlation Chart':
    # For the correlation chart, let's use a pairplot
    sns.pairplot(filtered_df[['avg_power', 'active_miners', 'hash_rate']], palette=custom_colors)
    st.pyplot(plt)






