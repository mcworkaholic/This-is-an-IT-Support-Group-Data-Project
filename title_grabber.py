
# import sqlite3
# import csv
# from termcolor import colored
# from config import database_path, csv_file_path, txt_file_path

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

# except sqlite3.Error as error:
#     print("Error while executing the SQL query", error)
# finally:
#     # Close the cursor and connection to SQLite database
#     cursor.close()
#     conn.close()

# # Print titles separated by a space
# print(' '.join(titles))
# print("\n" * 4)

# # Open the CSV file in write mode
# with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
#     # Create a CSV writer object
#     writer = csv.writer(file)
    
#     # Write the header row
#     writer.writerow(['Professional Titles'])
    
#     # Loop through the list of titles and write each as a row
#     for title in titles:
#         writer.writerow([title])
    
#     print(titles)

# # Add spacing before the final confirmation message
# print("\n" * 2)
# print(colored("CSV file has been created successfully.", 'green'))
# print("\n" * 2)

import sqlite3
import csv
from termcolor import colored
from config import database_path, csv_file_path, txt_file_path

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

# Open the text file in write mode
with open(txt_file_path, mode='w', encoding='utf-8') as txt_file:
    # Write each title to the text file
    for title in titles:
        txt_file.write(title + '\n')

print(colored("Text file has been created successfully.", 'green'))


