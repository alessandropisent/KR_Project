import pandas as pd
import json

def is_valid_string(s):
    """
    Checks if a given value is a valid string.

    A valid string:
    - Is an instance of `str`
    - Does not contain any digits
    - Does not include the character '#'

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string is valid, False otherwise.
    """
    if isinstance(s, str) and not any(char.isdigit() for char in s) and '#' not in s:
        return True
    return False


def return_max_exploded_df():
    """
    Reads episode data from a JSON file and expands nested structures into a detailed Pandas DataFrame.

    This function:
    - Loads episode data from "GOT/episodes.json".
    - Explodes the 'scenes' column into separate rows.
    - Expands the scene dictionaries into separate columns.
    - Explodes character appearances within each scene.
    - Expands character details into separate columns.
    - Explodes weapon usage and extracts weapon details.
    - Merges all expanded data into a final structured DataFrame.

    Returns:
        pd.DataFrame: A fully expanded dataset containing detailed episode, scene, character, and weapon information.
    """
    with open("GOT/episodes.json","r")as file:
        data = json.load(file)


    #df = pd.DataFrame(data["episodes"])
    df = pd.json_normalize(data, record_path=['episodes'])
    df = df.explode(column="scenes").reset_index(drop=True)

    # Example: Assume df is your original DataFrame
    df_scenes_expanded = df['scenes'].apply(pd.Series)  # Expands the dictionary into separate columns

    # Now, merge this expanded data back with the original dataframe
    df_scenes = pd.concat([df.drop(columns=['scenes']), 
                           df_scenes_expanded.reset_index(drop=True)], axis=1)

    ## No do for characters
    df_scenes = df_scenes.explode(column="characters").reset_index(drop=True)

    df_charaters_expanded = df_scenes["characters"].apply(pd.Series)

    df_charaters = pd.concat([df_scenes.drop(columns=['characters']).reset_index(drop=True), 
                              df_charaters_expanded.reset_index(drop=True)], axis=1)
    
    #print("DF CHARACTERS")
    #print(df_charaters.columns)

    ## wapons
    
    df_charaters = df_charaters.explode(column="weapon").reset_index(drop=True)

    df_weapon_explanded = df_charaters["weapon"].apply(pd.Series)
    df_weapon_explanded ["weapon.action"] = df_weapon_explanded ["action"]
    df_weapon_explanded ["weapon.name"] = df_weapon_explanded ["name"]
    df_weapon_explanded  = df_weapon_explanded.drop(columns=["name","action"])

    df_final = pd.concat([df_charaters.drop(columns=['weapon']).reset_index(drop=True), 
                          df_weapon_explanded.reset_index(drop=True)], axis=1)
    
    return df_final


def return_df_weapons():
    """
    Extracts weapon usage details from the expanded episode dataset.

    This function:
    - Calls `return_max_exploded_df()` to get detailed scene data.
    - Groups data by weapon name, listing characters who wielded each weapon.
    - Filters out specific weapons that should be excluded.
    - Adds a column counting the number of unique wielders per weapon.

    Returns:
        pd.DataFrame: A dataset containing weapons and the characters who used them.
    """

    df_final = return_max_exploded_df()
    df_weapons = df_final.groupby("weapon.name")["name"].apply(set).reset_index()
    df_weapons["name"] = df_weapons["name"].apply(list)

    values_to_drop = ["Dawn", "Ice", 
                    "Valyrian Steel Dagger", 
                    "Vigilance", "Wildfire",
                    'Dragonglass', 'Dragonglass Axe', 
                    'Dragonglass Dagger', 'Dragonglass Staff', 
                    'Dragonglass Sword']

    df_weapons = df_weapons[~df_weapons['weapon.name'].isin(values_to_drop)].reset_index(drop=True)
    df_weapons["numberOfWielders"] = df_weapons["name"].apply(len)
    return df_weapons


def return_location_been_df():
    """
    Extracts location visit details from the expanded episode dataset.

    This function:
    - Calls `return_max_exploded_df()` to get detailed scene data.
    - Filters out invalid character names using `is_valid_string()`.
    - Groups data by sub-location, listing characters who have been in each location.

    Returns:
        pd.DataFrame: A dataset mapping sub-locations to the characters who have been there.
    """
    

    df_final = return_max_exploded_df()
    df_final = df_final[df_final["name"].apply(is_valid_string)]

    df_locations = df_final.groupby("subLocation")["name"].apply(set).reset_index()
    df_locations["name"] = df_locations["name"].apply(list)
    
    
    return df_locations


#df = return_max_exploded_df()
#print(df.columns)