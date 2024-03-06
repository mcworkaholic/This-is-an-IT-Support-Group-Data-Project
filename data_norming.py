import json
import re
import googlemaps
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables from .env file
load_dotenv()

# Accessing the API key
google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')

us_states = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}



countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia",
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bhutan", "Bolivia","Bosnia", "Bosnia and Herzegovina", "Botswana", "Brazil","British Columbia","BC", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia",
    "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland",
    "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
    "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
    "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco",
    "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru",
    "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia",
    "Norway", "Oman", "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay",
    "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname",
    "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo",
    "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda",
    "Ukraine", "United Arab Emirates", "United Kingdom","UK", "United States of America", "Uruguay",
    "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

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

def reformat_data(data, countries, us_states):
    reformatted_data = []
    for item in data:
        original_location = item['location']
        country = get_country_from_location(original_location, countries, us_states)

        if country != "United States":
            city = original_location.replace(country, "").strip()
            state = "N/A"  # No state for non-U.S. locations
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

        reformatted_item = {
            "title": item['title'].title(),
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

def guess_location_details(json_object, google_maps_api_key):
    # Check if country is United States and state or city is empty
    if json_object["country/region"] == "United States" and (not json_object["state"] or not json_object["city"]):
        gmaps = googlemaps.Client(key=google_maps_api_key)
        lat, lon = json_object["lat"], json_object["lon"]
        
        # Reverse Geocoding using Google Maps API
        reverse_geocode_result = gmaps.reverse_geocode((lat, lon))
        
        for component in reverse_geocode_result[0]['address_components']:
            if "administrative_area_level_1" in component["types"] and not json_object["state"]:
                json_object["state"] = component["long_name"]
            elif "locality" in component["types"] and not json_object["city"]:
                json_object["city"] = component["long_name"]
    
    return json_object

# Integration into the data processing flow
def process_data_with_guessing(data, google_maps_api_key):
    reformatted_data = reformat_data(data, countries, us_states) 
    for item in reformatted_data:
        item = guess_location_details(item, google_maps_api_key)
    
    return reformatted_data

## FOR TESTING (Printing output to terminal)
# for item in processed_data:
#     print(json.dumps(item, indent=4))

# Build the full path for the output file
file_path_output = os.path.join(os.path.dirname(__file__), data_directory, modified_json_filename)

# Proceed to write the processed data
processed_data = process_data_with_guessing(data, google_maps_api_key)
with open(file_path_output, 'w') as file:
    json.dump(processed_data, file, indent=4)

################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################

# FINAL STEP, convert JSON to Sqlite for further analysis

def insert_into_database(data, db_name="survey_responses.db"):
    # Build the database path relative to the current file and the 'Data' directory
    current_dir = os.path.dirname(__file__)  # Get the directory of the current script
    db_path = os.path.join(current_dir, "Data", db_name)  # Append the 'Data' directory and database name

    # Connect to the SQLite database at the specified path
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table with appropriate data types
    c.execute('''CREATE TABLE IF NOT EXISTS responses
                 (title TEXT, city TEXT, state TEXT, country_region TEXT, lat REAL, lon REAL, pay REAL, pay_type TEXT)''')

    # Prepare insert statement, excluding 'original response' key
    insert_stmt = '''INSERT INTO responses (title, city, state, country_region, lat, lon, pay, pay_type) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''

    # Insert each record into the database
    for item in data:
        values = (item['title'], item['city'], item['state'], item['country/region'], 
                  item['lat'], item['lon'], item['pay'], item['pay type'])
        c.execute(insert_stmt, values)

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