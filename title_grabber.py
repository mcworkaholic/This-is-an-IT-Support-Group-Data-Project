# import sqlite3
# import re
# import os
# import csv
# from termcolor import colored

# # Construct the relative path to the database
# current_script_dir = os.path.dirname(os.path.realpath(__file__))  # Gets the directory where the script is located
# database_path = os.path.join(current_script_dir, "Data", "survey_responses.db")

# # Connect to the SQLite database
# conn = sqlite3.connect(database_path)

# # Create a cursor object using the cursor() method
# cursor = conn.cursor()

# # SQL query to select formatted titles
# sql_query = "SELECT formatted_title FROM formatted_responses;"

# try:
#     # Execute the SQL query
#     cursor.execute(sql_query)
    
#     # Fetch all the results
#     results = cursor.fetchall()
    
#     # Initialize an empty list to hold the titles
#     titles = []
    
#     # Loop through each result (tuple) and add the title to the list
#     for row in results:
#         # Assuming each row contains one title, accessed by row[0]
#         title = row[0]
#         # Add the whole title as a single item
#         titles.append(title)

#     # Print or process the list of titles as needed
#     print(titles)
    
# except sqlite3.Error as error:
#     print("Error while executing the SQL query", error)
# finally:
#     # Close the cursor and connection to SQLite database
#     cursor.close()
#     conn.close()

# # Define the path to the CSV file
# csv_file_path = os.path.join(current_script_dir, "Data", "professional_titles.csv")

# # Open the CSV file in write mode
# with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
#     # Create a CSV writer object
#     writer = csv.writer(file)
    
#     # Write the header row
#     writer.writerow(['Professional Titles'])
    
#     # Loop through the list of titles and write each as a row
#     for title in titles:
#         writer.writerow([title])

# print()
# print()
# print(colored("CSV file has been created successfully.", 'green'))
# print()
# print()

import sqlite3
import re
import os
import csv
from termcolor import colored

# Construct the relative path to the database
current_script_dir = os.path.dirname(os.path.realpath(__file__))  # Gets the directory where the script is located
database_path = os.path.join(current_script_dir, "Data", "survey_responses.db")

# Connect to the SQLite database
conn = sqlite3.connect(database_path)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# SQL query to select formatted titles
sql_query = "SELECT formatted_title FROM formatted_responses;"

try:
    # Execute the SQL query
    cursor.execute(sql_query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Initialize an empty list to hold the titles
    titles = []
    
    # Loop through each result (tuple) and add the title to the list
    for row in results:
        # Assuming each row contains one title, accessed by row[0]
        title = row[0]
        # Add the whole title as a single item
        titles.append(title)

except sqlite3.Error as error:
    print("Error while executing the SQL query", error)
finally:
    # Close the cursor and connection to SQLite database
    cursor.close()
    conn.close()

# Print titles separated by a space
print(' '.join(titles))
print("\n" * 4)

# Define the path to the CSV file
csv_file_path = os.path.join(current_script_dir, "Data", "professional_titles.csv")

# Open the CSV file in write mode
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    # Create a CSV writer object
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['Professional Titles'])
    
    # Loop through the list of titles and write each as a row
    for title in titles:
        writer.writerow([title])
    
    print(titles)

# Add spacing before the final confirmation message
print("\n" * 2)
print(colored("CSV file has been created successfully.", 'green'))
print("\n" * 2)

