import os

# Filenames and directories
data_directory = "Data"
image_directory = "Images"
original_json_filename = "IT Professional Survey Responses.json"
modified_json_filename = "IT Professional Survey Responses - Fixed.json"

# Build the file paths
original_json_path = os.path.join(os.path.dirname(__file__), data_directory, original_json_filename)
modified_json_path = os.path.join(os.path.dirname(__file__), data_directory, modified_json_filename)
database_path = os.path.join(os.path.dirname(__file__), data_directory, "survey_responses.db")
IT_image_path = os.path.join(os.path.dirname(__file__), image_directory, "good_head.png")

# Construct the relative path 
current_script_dir = os.path.dirname(os.path.realpath(__file__))  # Gets the directory where the script is located

# Define the path to the CSV and TXT file
csv_file_path = os.path.join(current_script_dir, "Data", "professional_titles.csv")
txt_file_path = os.path.join(current_script_dir, "Data", "professional_titles.txt")

# Data Structures
us_states = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey',
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio',
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'PR': 'Puerto Rico', 'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
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

patterns = {
    " II ": " 2 ", " Ii ": " 2 ", " III ": " 3 ", " Iii ": " 3 ", " II": " 2 ", " Ii": " 2 ", " III": " 3 ", " Iii": " 3 ",
    "L1 ": " 1 ", "L2 ": " 2 ", "L3 ": " 3 ", " L1 ": " 1 ", " L2 ": " 2 ", " L3 ": " 3 ", " L1": " 1 ", " L2": " 2 ", " L3": " 3 ",
    " Level 1 ": " 1 ", " Level 2 ": " 2 ", " Level 3 ": " 3 ", " Level 1": " 1 ", " Level 2": " 2 ", " Level 3": " 3 ",
    " Level 1 & 2 ": " 1 & 2 ", " Level 1 & 2": " 1 & 2 ", " Level 2 & 3 ": " 2 & 3 ", " Level 2 & 3": " 2 & 3 ",
    " Tier 1 ": " 1 ", " Tier 2 ": " 2 ", " Tier 3 ": " 3 ", "Tier 1 ": " 1 ", "Tier 2 ": " 2 ", "Tier 3 ": " 3 ",
    " Tier 1": " 1 ", " Tier 2": " 2 ", " Tier 3": " 3 ", " T1 ": " 1 ", " T2 ": " 2 ", " T3 ": " 3 ", "T1 ": " 1 ",
    "T2 ": " 2 ", "T3 ": " 3 ", " T1": " 1 ", " T2": " 2 ", " T3": " 3 ", " Teir 1 ": " 1 ", " Teir 2 ": " 2 ", " Teir 3 ": " 3 ",
    "Teir 1 ": " 1 ", "Teir 2 ": " 2 ", "Teir 3 ": " 3 ", " Teir 1": " 1 ", " Teir 2": " 2 ", " Teir 3": " 3 ",
    " Lvl 1 ": " 1 ", " Lvl 1.5 ": " 1.5 ", " Lvl 2 ": " 2 ", " Lvl 2.5 ": " 2.5 ", " Lvl 3 ": " 3 ",
    "Lvl 1 ": " 1 ", "Lvl 1.5 ": " 1.5 ", "Lvl 2 ": " 2 ", "Lvl 2.5 ": " 2.5 ", "Lvl 3 ": " 3 ",
    " Lvl 1": " 1 ", " Lvl 1.5": " 1.5 ", " Lvl 2": " 2 ", " Lvl 2.5": " 2.5 ", " Lvl 3": " 3 ",
    " Junior ": " 1 ", "Junior ": " 1 ", "Jr ": " 1 ", "Jr. ": " 1 ", " Senior ": " 3 ", "Senior ": " 3 ",
    "Sr ": " 3 ", "Sr. ": " 3 ", "1St Line ": " 1 ", "2Nd Line ": " 2 ", "3Rd Line ": " 3 ", "Intermediate ": " 2 ",
    " Intermediate": " 2 ", "mid ": " 2 ", "mid-level ": " 2 ", " mid ": " 2 ", " mid-level ": " 2 ", " mid": " 2 ", " mid-level": " 2 ",
}

job_tiers = {}