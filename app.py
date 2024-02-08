import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Load the dataset
df = pd.read_csv('Power 1.csv', parse_dates=['timestamp'])

# Convert timestamp to proper datetime (assuming the timestamps are UTC)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# App title
st.title('In-Depth BTC Blockchain Data Analysis App')

# Display a statistical summary
if st.checkbox('Show statistical summary'):
    st.write(df.describe())

# Time Filtering
st.sidebar.header('Time Filtering')
time_filter = st.sidebar.selectbox('Select Time Period', ['Yesterday', 'Last 7 Days', 'Last 30 Days', 'Last Month'])

today = datetime.now()
if time_filter == 'Yesterday':
    filtered_df = df[(df['timestamp'] >= today - timedelta(days=1)) & (df['timestamp'] < today)]
elif time_filter == 'Last 7 Days':
    filtered_df = df[(df['timestamp'] >= today - timedelta(days=7)) & (df['timestamp'] < today)]
elif time_filter == 'Last 30 Days':
    filtered_df = df[(df['timestamp'] >= today - timedelta(days=30)) & (df['timestamp'] < today)]
elif time_filter == 'Last Month':
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = first_day_last_month + timedelta(days=(today.replace(day=1) - first_day_last_month).days)
    filtered_df = df[(df['timestamp'] >= first_day_last_month) & (df['timestamp'] < last_day_last_month)]

# Site Level Filtering
st.sidebar.header('Site Level Filtering')
site_to_filter = st.sidebar.selectbox('Which site to filter by?', df['client_name'].unique())
filtered_df = filtered_df[filtered_df['client_name'] == site_to_filter]

if st.sidebar.button('Apply Site and Time Filter'):
    st.write(filtered_df)
else:
    st.write(df)

# Data Visualization
st.header('Data Visualization')
chart_type = st.selectbox('Select chart type', ['Line Chart', 'Histogram', 'Box Plot', 'Heatmap'])

if chart_type == 'Line Chart':
    st.line_chart(filtered_df[['avg_power', 'active_miners', 'hash_rate']])
elif chart_type == 'Histogram':
    column_to_plot = st.selectbox('Select column to plot', ['avg_power', 'active_miners', 'hash_rate'])
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df[column_to_plot], kde=True)
    st.pyplot(plt)
elif chart_type == 'Box Plot':
    column_to_plot = st.selectbox('Select column for box plot', ['avg_power', 'active_miners', 'hash_rate'])
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=filtered_df[column_to_plot])
    st.pyplot(plt)
elif chart_type == 'Heatmap':
    corr = filtered_df[['avg_power', 'active_miners', 'hash_rate']].corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True)
    st.pyplot(plt)

