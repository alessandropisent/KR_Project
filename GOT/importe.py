import json
import re

def sanitize(text):
    """
    Remove non-alphanumeric characters to create a valid ID.
    """
    return re.sub(r'\W+', '', text)

# 1. Read the JSON file
with open("characters.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 2. Get all unique keys (columns)
unique_keys = set()
for char in data.get("characters", []):
    unique_keys.update(char.keys())

print("Unique keys found in the file:")
for key in sorted(unique_keys):
    print(f"- {key}")

# 3. Generate OWL instances for each character
owl_header = '''<?xml version="1.0"?>
<rdf:RDF xmlns="http://example.com/GameOfThronesOntology#"
         xml:base="http://example.com/GameOfThronesOntology"
         xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:owl="http://www.w3.org/2002/07/owl#"
         xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
         xmlns:xsd="http://www.w3.org/2001/XMLSchema#">
  <!-- OWL Individuals generated from characters.json -->
'''

owl_footer = "\n</rdf:RDF>"

individuals = []

for char in data.get("characters", []):
    # Use the characterName as the identifier (sanitize it to form a valid ID)
    char_name = char.get("characterName", "Unknown")
    individual_id = sanitize(char_name)
    
    # Begin the owl:NamedIndividual element
    individual_str = f'  <owl:NamedIndividual rdf:about="#{individual_id}">\n'
    # Declare that this individual is of type Character
    individual_str += '    <rdf:type rdf:resource="#Character"/>\n'
    # Add the character name using the hasName property
    individual_str += f'    <hasName rdf:datatype="xsd:string">{char_name}</hasName>\n'
    
    # Iterate over the rest of the keys to add properties
    for key, value in char.items():
        # Skip the characterName as we already processed it
        if key == "characterName":
            continue

        # Create a property name by sanitizing the key (remove spaces and non-alphanumerics)
        prop_name = sanitize(key)
        
        # If the value is a list, join the items with a comma.
        if isinstance(value, list):
            value_str = ", ".join(str(item) for item in value)
        else:
            value_str = str(value)
        
        # Add this property as a datatype property (for simplicity, using xsd:string)
        individual_str += f'    <{prop_name} rdf:datatype="xsd:string">{value_str}</{prop_name}>\n'
    
    # Close the individual element
    individual_str += "  </owl:NamedIndividual>\n"
    
    individuals.append(individual_str)

# Combine everything into the final OWL content
owl_content = owl_header + "\n".join(individuals) + owl_footer

# Write the OWL content to a file
with open("characters.owl", "w", encoding="utf-8") as owl_file:
    owl_file.write(owl_content)

print("OWL file 'characters.owl' generated successfully.")
