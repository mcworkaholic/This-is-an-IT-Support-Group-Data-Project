import json
import os

# Specify the path to your original JSON file
original_file_path = 'it_certifications.json'  # Replace 'data.json' with your actual file path

# Load the original JSON data
with open(original_file_path, 'r') as file:
    data = json.load(file)

# Extract and sort the certifications list
certifications = data['certifications']
sorted_certifications = sorted(certifications, key=lambda x: x['name'])

# Prepare the new filename by appending "_sorted" before the ".json" extension
file_dir, file_name = os.path.split(original_file_path)
name_part, extension = os.path.splitext(file_name)
new_file_path = os.path.join(file_dir, f"{name_part}_sorted{extension}")

# Write the sorted data back to a new JSON file
with open(new_file_path, 'w') as file:
    json.dump({'certifications': sorted_certifications}, file, indent=4)

print(f"Sorted certifications have been saved to: {new_file_path}")
