import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('Power 1.csv')

# App title
st.title('In-Depth Data Analysis App')

# Display a statistical summary
if st.checkbox('Show statistical summary'):
    st.write(df.describe())

# Data Visualization
st.sidebar.header('Visualization Settings')
chart_type = st.sidebar.selectbox('Select chart type', ['Line Chart', 'Histogram', 'Box Plot'])

if chart_type == 'Line Chart':
    st.line_chart(df.select_dtypes(include=['float', 'int']))
elif chart_type == 'Histogram':
    column_to_plot = st.sidebar.selectbox('Select column to plot', df.columns)
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column_to_plot], kde=True)
    st.pyplot(plt)
elif chart_type == 'Box Plot':
    column_to_plot = st.sidebar.selectbox('Select column for box plot', df.columns)
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=df[column_to_plot])
    st.pyplot(plt)

# Filtering Data
st.sidebar.header('Filter Data')
column_to_filter = st.sidebar.selectbox('Which column to filter?', df.columns)
filter_value = st.sidebar.text_input('Value to filter by:', '')

if st.sidebar.button('Apply Filter'):
    filtered_df = df[df[column_to_filter] == filter_value]
    st.write(filtered_df)
else:
    st.write(df)
