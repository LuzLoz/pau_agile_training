import pandas as pd
import sqlite3
import os

def excel_to_sqlite(data_path, db_name):
    # Iterate through files in the data_path folder
    for file_name in os.listdir(data_path):
        # Check if the file is an Excel file
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        # Construct the full file path
            excel_file = os.path.join(data_path, file_name)
            try:
                # Read the Excel file with openpyxl engine
                xls = pd.ExcelFile(excel_file, engine='openpyxl')
                
                # Connect to SQLite database (it will create the database if it doesn't exist)
                conn = sqlite3.connect(db_name)
                
                # Iterate through each sheet in the Excel file
                for sheet_name in xls.sheet_names:
                    # Read the sheet into a DataFrame
                    df = pd.read_excel(xls, sheet_name)
                    
                    # Write the DataFrame to a SQLite table
                    df.to_sql(sheet_name, conn, if_exists='replace', index=False)
                
                # Close the connection
                conn.close()
            except Exception as e:
                print(f"file {excel_file} An error occurred: {e}")

def query_sqlite(db_name, query):
    # Connect to SQLite database
    conn = sqlite3.connect(db_name)
    
    # Execute the query and fetch the results
    results = conn.execute(query).fetchall()
    
    # Close the connection
    conn.close()
    
    return results

data_path = 'data'
db_name = 'data/agile_training.db'
# excel_to_sqlite(data_path, db_name)
query = 'SELECT * FROM AgileAssesment;'
results = query_sqlite(db_name, query)
print(results)

