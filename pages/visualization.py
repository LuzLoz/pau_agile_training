import streamlit as st
import sqlite3
import pandas as pd

# Set up the Streamlit app configuration
st.set_page_config(page_title="Data Visualization App", initial_sidebar_state="collapsed")

# Connect to the SQLite database
conn = sqlite3.connect('data/agile_training.db')
cursor = conn.cursor()

# Fetch data from the database
query = "SELECT * FROM your_table"
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()

# Process the data (example: calculate summary statistics)
summary = df.describe()

# Display the data and summary statistics
st.write("Data from SQLite Database")
st.dataframe(df)
st.write("Summary Statistics")
st.dataframe(summary)

# Generate and display visualizations
st.write("Data Visualization")
st.line_chart(df)  # Example: Line chart

# You can also use other visualization libraries like Matplotlib or Plotly
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(df['column_name'])  # Replace 'column_name' with your actual column name
st.pyplot(fig)