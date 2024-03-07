import json
import re
import os
import sqlite3
import requests
import time
from config import us_states, countries, patterns

# Keep track of the last request time
last_request_time = None

data_directory = "Data"

# Define the new, modified file name
modified_json_filename = "IT Professional Survey Responses - Fixed.json"

# Step 1: Read the JSON file
filename = "IT Professional Survey Responses.json"

# Build the relative path
file_path = os.path.join(os.path.dirname(__file__), data_directory, filename)

# load it from the file
with open(file_path, 'r') as file:
    data = json.load(file)

# The regex pattern for matching any variation of "United States"
# All variations should be replaced with the string "United States"
United_States_pattern = re.compile(r'\b(USA|US|United\s+States(\s+of\s+America)?)\b', re.IGNORECASE)
# Enhanced regex pattern to include state names and abbreviations for flexible matching
state_patterns = [f"\\b{re.escape(code)}\\b|\\b{re.escape(full_name)}\\b" for code, full_name in us_states.items()]
state_regex = re.compile("|".join(state_patterns), re.IGNORECASE)


def format_us_location(location, us_states):
    # Initialize variables
    city = location
    state = ""
    country = "Unknown"

    # Attempt to detect and map both state abbreviation and full state name
    for abbr, full_name in us_states.items():
        # Use regular expressions to check for state abbreviation or full name
        pattern_abbr = re.compile(r'\b' + re.escape(abbr) + r'\b', re.IGNORECASE)
        pattern_full_name = re.compile(r'\b' + re.escape(full_name) + r'\b', re.IGNORECASE)

        if pattern_abbr.search(location):
            state = full_name
            city = pattern_abbr.sub("", location).strip()
            country = "United States"
            break
        elif pattern_full_name.search(location):
            state = full_name
            city = pattern_full_name.sub("", location).strip()
            country = "United States"
            break

    # Remove any common country identifiers from the city string
    city = re.sub(United_States_pattern, "", city).strip(", ").strip()

    # Further ensure the city does not have lingering state names, abbreviations, or "US" variations
    if state:
        city = re.sub(r'\b' + re.escape(state) + r'\b', '', city, flags=re.IGNORECASE).strip()
    
    city = city.replace("USA", "").replace("US", "").replace("United States", "").strip(", ").strip()

    return city, state, country

def reformat_us_data(data, us_states):
    reformatted_data = []
    for item in data:
        city, state, country = format_us_location(item['location'], us_states)
        
        reformatted_item = {
            "title": item['title'],
            "city": city,
            "state": state,
            "country": country,
            "lat": item['lat'],
            "lon": item['lon'],
            "pay": item['pay']
        }
        reformatted_data.append(reformatted_item)
    return reformatted_data

def get_country_from_location(location, countries, us_states):
    # Check if any part of the location matches a known country
    for country in countries:
        if country in location:
            return country
    # Check for state abbreviations as an indicator of the United States
    for state_abbr in us_states.keys():
        if f" {state_abbr}" in location.upper():  # Space added before the abbreviation to prevent partial matches
            return "United States"
    # Existing checks for USA
    if 'USA' in location.upper() or 'US' in location.upper() or 'United States' in location:
        return "United States"
    return "Unknown"

def format_professional_title(title):
    # Capitalize occurrences of " it " and " i.t. " surrounded by spaces
    title = re.sub(r'\b(it)\b', 'IT', title, flags=re.IGNORECASE)
    title = re.sub(r'\b(i\.t\.)\b', 'I.T.', title, flags=re.IGNORECASE)

    extracted_numbers = []

    for pattern, replacement in patterns.items():
        # Check start
        if title.startswith(pattern.strip()):
            extracted_numbers.append(replacement.strip())
            title = title.replace(pattern, " ", 1)
        # Check end
        elif title.endswith(pattern.strip()):
            extracted_numbers.append(replacement.strip())
            title = title[:title.rfind(pattern)] + title[title.rfind(pattern):].replace(pattern, " ", 1)

        # Check middle occurrences with space padding
        padded_pattern = " " + pattern.strip() + " "
        if padded_pattern in title:
            extracted_numbers.append(replacement.strip())
            title = title.replace(padded_pattern, " ", 1)

        # Remove additional occurrences carefully
        while pattern in title:
            if pattern.strip() in title:
                extracted_numbers.append(replacement.strip())
                title = title.replace(pattern, " ", 1)
            else:
                break  # Avoid infinite loop if no exact match is found

    # Clean up any extra spaces and append extracted numbers not previously in the title
    title = " ".join(title.split())  # Removes extra spaces
    if extracted_numbers:
        # Append extracted numbers, ensuring no duplicates and maintaining order
        title += " " + " ".join(sorted(set(extracted_numbers), key=extracted_numbers.index))

    return title.strip()

def reformat_data(data, countries, us_states):
    reformatted_data = []
    for item in data:
        original_location = item['location']
        country = get_country_from_location(original_location, countries, us_states)

        if country != "United States":
            city = original_location.replace(country, "").strip()
            state = "N/A"  # No state for non-U.S. locations
        elif country == "UK":
            country = "United Kingdom"
        else:
            city, state, _ = format_us_location(original_location, us_states)

        # Ensure 'pay' is defined within item before accessing it
        pay = item.get('pay', '0')  # Default to '0' if 'pay' key does not exist

        # Determine pay type based on the content of 'pay'
        pay_type = "unknown"
        if "annually" in pay.lower():
            pay_type = "Salary"
        elif "hourly" in pay.lower():
            pay_type = "Hourly"

        # Clean 'pay' to only include numerical values and remove "$"
        pay = re.sub(r'[^\d.]', '', pay)

        # Format the title
        formatted_title = format_professional_title(item['title'].title())

        reformatted_item = {
            "title": formatted_title,
            "city": city,
            "state": state,
            "country/region": country if country else "Unknown",
            "lat": item['lat'],
            "lon": item['lon'],
            "pay": pay,
            "pay type": pay_type
        }
        reformatted_data.append(reformatted_item)
    return reformatted_data

def guess_location_details(json_object):
    global last_request_time
    
    # Nominatim usage policy suggests at least 1 second between requests
    request_interval = 1  # seconds

    # Check if country is United States and state or city is empty
    if json_object["country/region"] == "United States" and (not json_object["state"] or not json_object["city"]):
        lat, lon = json_object["lat"], json_object["lon"]
        
        # Enforce rate limiting
        if last_request_time is not None:
            elapsed_time = time.time() - last_request_time
            if elapsed_time < request_interval:
                time.sleep(request_interval - elapsed_time)
        
        # Update the last request time
        last_request_time = time.time()

        # Construct the URL for the Nominatim API reverse geocoding request
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        
        # Make the request to the Nominatim API
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = response.json()
        
        # Extract state and city information from the response
        address = data.get('address', {})
        state = address.get('state')
        city = address.get('city', address.get('town', address.get('village')))
        
        # Update the JSON object with the state and city if they were found
        if state and not json_object["state"]:
            json_object["state"] = state
        if city and not json_object["city"]:
            json_object["city"] = city

    return json_object

# Integration into the data processing flow
def process_data_with_guessing(data):
    reformatted_data = reformat_data(data, countries, us_states) 
    for item in reformatted_data:
        item = guess_location_details(item)  
    
    return reformatted_data

## FOR TESTING (Printing output to terminal)
# for item in processed_data:
#     print(json.dumps(item, indent=4))

# Build the full path for the output file
file_path_output = os.path.join(os.path.dirname(__file__), data_directory, modified_json_filename)

# Proceed to write the processed data
processed_data = process_data_with_guessing(data)
with open(file_path_output, 'w') as file:
    json.dump(processed_data, file, indent=4)

################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# FINAL STEP, convert JSON to Sqlite for further analysis
def create_tables(conn):
    c = conn.cursor()
    ## FOR TESTING
    # # Create table for original titles
    # c.execute('''CREATE TABLE IF NOT EXISTS original_responses (
    #              id INTEGER PRIMARY KEY AUTOINCREMENT,
    #              title TEXT, 
    #              city TEXT, 
    #              state TEXT, 
    #              country_region TEXT, 
    #              lat REAL, 
    #              lon REAL, 
    #              pay REAL, 
    #              pay_type TEXT)''')

    # Create table for formatted titles
    c.execute('''CREATE TABLE IF NOT EXISTS formatted_responses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 formatted_title TEXT, 
                 city TEXT, 
                 state TEXT, 
                 country_region TEXT, 
                 lat REAL, 
                 lon REAL, 
                 pay REAL, 
                 pay_type TEXT)''')
    conn.commit()

def insert_into_database(data, db_name="survey_responses.db"):
    # Build the database path relative to the current file and the 'Data' directory
    current_dir = os.path.dirname(__file__)  # Get the directory of the current script
    db_path = os.path.join(current_dir, "Data", db_name)  # Append the 'Data' directory and database name

    # Connect to the SQLite database at the specified path
    conn = sqlite3.connect(db_path)

    # Create the tables
    create_tables(conn)

    c = conn.cursor()
    ## FOR TESTING
    # # Prepare insert statement for original titles
    # insert_stmt_original = '''INSERT INTO original_responses (title, city, state, country_region, lat, lon, pay, pay_type) 
    #                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    # Prepare insert statement for formatted titles
    insert_stmt_formatted = '''INSERT INTO formatted_responses (formatted_title, city, state, country_region, lat, lon, pay, pay_type) 
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    # Insert each record into the respective database table
    for item in data:
        ## FOR TESTING
        # # Insert original title record
        # values_original = (item['title'], item['city'], item['state'], item['country/region'], 
        #                    item['lat'], item['lon'], item['pay'], item['pay type'])
        # c.execute(insert_stmt_original, values_original)

        # Format the title and insert formatted title record
        formatted_title = format_professional_title(item['title'].title())
        values_formatted = (formatted_title, item['city'], item['state'], item['country/region'], 
                            item['lat'], item['lon'], item['pay'], item['pay type'])
        c.execute(insert_stmt_formatted, values_formatted)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def read_processed_data_and_insert(db_name="survey_responses.db"):
    # Define the modified file name and build the full path for the input file
    file_path_input = os.path.join(os.path.dirname(__file__), data_directory, modified_json_filename)

    # Ensure the 'Data' directory exists or create it
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "Data")):
        os.makedirs(os.path.join(os.path.dirname(__file__), "Data"))

    # Read the processed data from the fixed JSON file
    with open(file_path_input, 'r') as file:
        processed_data = json.load(file)
    
    # Insert the processed data into the SQLite database
    insert_into_database(processed_data, db_name)

# Call the function to read from the fixed JSON and insert into SQLite
read_processed_data_and_insert()