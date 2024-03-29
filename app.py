import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    descriptive_stats = df[numeric_cols].describe().T
    skew = df[numeric_cols].skew().rename('skew')
    kurt = df[numeric_cols].kurt().rename('kurt')
    descriptive_stats = descriptive_stats.join(skew).join(kurt)
    st.write(descriptive_stats)
    for col in numeric_cols:
        plt.figure(figsize=(10, 4))
        sns.histplot(df[col], kde=True, color='cyan')
        plt.title(f'Distribution of {col}')
        st.pyplot(plt)

# Time Filtering
st.sidebar.header('Time Filtering')
time_filter = st.sidebar.selectbox('Select Time Period', ['Today', 'Yesterday', 'Last 7 Days', 'Last 30 Days', 'Last Month'])

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
chart_type = st.selectbox('Select chart type', ['Line Chart', 'Histogram', 'Box Plot', 'Heatmap'])

sns.set(style="whitegrid")
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

if chart_type == 'Line Chart':
    fig, ax = plt.subplots()
    ax.plot(filtered_df['timestamp'], filtered_df['avg_power'], color='cyan', label='Average Power')
    ax.plot(filtered_df['timestamp'], filtered_df['active_miners'], color='cyan', label='Active Miners', linestyle='--')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    ax.tick_params(axis='x', colors='white', rotation=45)
    ax.tick_params(axis='y', colors='white')
    plt.legend(loc='upper right', frameon=False, fontsize='small', labelcolor='green')
    st.pyplot(fig)
elif chart_type == 'Histogram':
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_df['avg_power'], color='cyan', kde=True)
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    st.pyplot(plt)
elif chart_type == 'Box Plot':
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=filtered_df, y='avg_power', color='cyan')
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    st.pyplot(plt)
elif chart_type == 'Heatmap':
    corr = filtered_df[['avg_power', 'active_miners', 'hash_rate']].corr()
    plt.figure(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='cool')
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    st.pyplot(plt)










