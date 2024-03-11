import json
import re
import os
import sqlite3
import requests
import time
from config import us_states, countries, patterns, job_tiers, original_json_path, modified_json_path

# Keep track of the last request time
last_request_time = None

# load it from the file
with open(original_json_path, 'r') as file:
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

# PERFECT :)
def format_professional_title(title, patterns):
    # Use lookbehind and lookahead to ensure spaces are preserved around "IT" and "I.T."
    normalized_title = re.sub(r'(?<=\b)(it)(?=\b)', 'IT', title, flags=re.IGNORECASE)
    normalized_title = re.sub(r'(?<=\b)(i\.t\.)(?=\b)', 'I.T.', normalized_title, flags=re.IGNORECASE)

    extracted_numbers = []
    job_tier = "N/A"

    # Handling Roman numerals
    roman_numerals = {'III': 3, 'II': 2, 'I': 1}
    for roman, arabic in roman_numerals.items():
        if re.search(f'\\b{roman}\\b', normalized_title, re.IGNORECASE):
            extracted_numbers.append(arabic)
            normalized_title = re.sub(f'\\b{roman}\\b', '', normalized_title)  # Remove Roman numeral
            job_tier = str(arabic)

    # Extract numeric values directly from the title and patterns
    direct_numbers = re.findall(r'\b\d+\b', normalized_title)
    for number in direct_numbers:
        extracted_numbers.append(int(number))

    for pattern, replacement in patterns.items():
        if re.search(pattern, normalized_title, re.IGNORECASE):
            extracted_numbers.append(int(replacement))
            normalized_title = re.sub(pattern, '', normalized_title)  # Remove pattern
            job_tier = replacement

    # Determine the highest job tier from extracted numbers
    if extracted_numbers:
        highest_tier = max(extracted_numbers)
        job_tier = str(highest_tier)
        # Append the highest tier to the title if not already present
        if not normalized_title.endswith(job_tier):
            normalized_title = f"{normalized_title} {job_tier}".strip()

    normalized_title = re.sub(r'\s+', ' ', normalized_title).strip()  # Clean up extra spaces

    # Convert numbers back to strings for consistency in the returned list
    extracted_numbers_str = list(map(str, set(extracted_numbers)))

    return normalized_title, extracted_numbers_str, job_tier


def determine_job_tier(extracted_numbers):
    # Convert extracted strings to floats, filtering for valid tiers within the range 1 to 3
    valid_tiers = [float(num) for num in extracted_numbers if is_valid_tier(num)]

    # Determine the highest valid tier, converting it back to a string for consistency
    if valid_tiers:
        highest_tier = max(valid_tiers)
        # Convert to int if the highest tier is an integer, else keep as float
        highest_tier_str = str(int(highest_tier)) if highest_tier.is_integer() else str(highest_tier)
        return highest_tier_str
    else:
        return "N/A"

def is_valid_tier(num_str):
    """
    Check if the string represents a valid job tier number (within 1 to 3, inclusive).
    Accepts both integer and decimal representations.
    """
    try:
        num = float(num_str)
        return 1 <= num <= 3
    except ValueError:
        return False
    
def reformat_data(data, countries, us_states, job_tiers, patterns):
    reformatted_data = []

    for index, item in enumerate(data):
        original_location = item['location']
        country = get_country_from_location(original_location, countries, us_states)

        if country != "United States":
            city = original_location.replace(country, "").strip()
            state = "N/A"
        elif country == "UK":
            country = "United Kingdom"
        else:
            city, state, _ = format_us_location(original_location, us_states)

        pay = item.get('pay', '0')  # Default to '0' if 'pay' key does not exist
        pay_type = "unknown"
        if "annually" in pay.lower():
            pay_type = "Salary"
        elif "hourly" in pay.lower():
            pay_type = "Hourly"
        pay = re.sub(r'[^\d.]', '', pay)  # Clean 'pay' to only include numerical values and remove "$"

        # Correctly unpack all three values returned by format_professional_title
        formatted_title, all_extracted_numbers, job_tier = format_professional_title(item['title'].title(), patterns)

        # Update job_tiers with the index and job tier
        job_tiers[index] = job_tier

        reformatted_item = {
            "original_title": item['title'],
            "formatted_title": formatted_title,
            "job_tier": job_tier,  # Directly use job_tier here
            "city": city,
            "state": state,
            "country_region": country if country else "Unknown",
            "lat": item['lat'],
            "lon": item['lon'],
            "pay": pay,
            "pay_type": pay_type
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
    reformatted_data = reformat_data(data, countries, us_states, job_tiers, patterns)
    for index in range(len(reformatted_data)):
        reformatted_data[index] = guess_location_details(reformatted_data[index])
    return reformatted_data

# ## FOR TESTING (Printing output to terminal)
# # for item in processed_data:
# #     print(json.dumps(item, indent=4))

# Proceed to write the processed data
processed_data = process_data_with_guessing(data)
with open(modified_json_path, 'w') as file:
    json.dump(processed_data, file, indent=4)

################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# FINAL STEP, convert JSON to Sqlite for further analysis
def create_tables(conn):
    c = conn.cursor()
    # Create table for formatted titles
    c.execute('''CREATE TABLE IF NOT EXISTS formatted_responses (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 formatted_title TEXT, 
                 job_tier TEXT,
                 city TEXT, 
                 state TEXT, 
                 country_region TEXT, 
                 lat REAL, 
                 lon REAL, 
                 pay REAL, 
                 pay_type TEXT)''')
    conn.commit()
    
def insert_into_database(data, db_name="survey_responses.db"):
    current_dir = os.path.dirname(__file__)
    db_path = os.path.join(current_dir, "Data", db_name)
    conn = sqlite3.connect(db_path)
    create_tables(conn)
    c = conn.cursor()

    insert_stmt_formatted = '''INSERT INTO formatted_responses (formatted_title, job_tier, city, state, country_region, lat, lon, pay, pay_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    for index, item in enumerate(data):
        formatted_title, extracted_numbers, job_tier = format_professional_title(item['title'].title(), patterns)
        
        # Print statements to verify formatted_title and job_tier before insertion
        # print("Formatted Title:", formatted_title)
        # print("Job Tier:", job_level)

        # Retrieve job tier using the index from job_tiers dictionary
        job_tier = job_tiers.get(index, "N/A")

        values_formatted = (formatted_title, job_tier, item['city'], item['state'], item['country/region'], item['lat'], item['lon'], item['pay'], item['pay type'])
        c.execute(insert_stmt_formatted, values_formatted)

    conn.commit()
    conn.close()

def read_processed_data_and_insert(db_name="survey_responses.db"):
    # Define the modified file name and build the full path for the input file

    # Ensure the 'Data' directory exists or create it
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "Data")):
        os.makedirs(os.path.join(os.path.dirname(__file__), "Data"))

    # Read the processed data from the fixed JSON file
    with open(modified_json_path, 'r') as file:
        processed_data = json.load(file)
    
    # Insert the processed data into the SQLite database
    insert_into_database(processed_data, db_name)

# Call the function to read from the fixed JSON and insert into SQLite
read_processed_data_and_insert()
job_tiers.clear()