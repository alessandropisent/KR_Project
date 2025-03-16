import pandas as pd
import json
import numpy as np

def remove_nan(el):
    """
    Removes empty string values from a list.

    Args:
        el (list): A list of elements.

    Returns:
        list: A new list without empty string values.
    """
    ret = []
    for e in el:
        if e != "":
            ret.append(e)

    return ret

locations = ['North of the Wall', 'The Wall', 
             'The North', 'The Vale', 
             'The Iron Islands', 'The Westerlands', 
             'The Riverlands', 'The Crownlands', 
             'The Stormlands', 'The Reach', 
             'Dorne', 'Pentos', 'Volantis', 
             'Valyria', 'The Dothraki Sea', 
             'Meereen', 'Yunkai', 'Astapor', 
             'The Red Waste', 'Qarth']

duplicate = [{"location"}]

def delete_duplicates_main(row):
    """
    Removes known major locations from a list of sub-locations.

    Args:
        row (list): A list of sub-locations.

    Returns:
        list: A filtered list without known major locations.
    """
    return [sub for sub in row if sub not in locations]



def return_df_locations(explode=True):
    """
    Reads location data from a JSON file and processes it into a Pandas DataFrame.

    This function:
    - Loads location data from "GOT/locations.json".
    - Removes empty sub-locations.
    - Filters out duplicates and known major locations.
    - Groups sub-locations by their main region.
    - Optionally explodes the grouped data into separate rows.

    Args:
        explode (bool, optional): If True, returns an exploded DataFrame with each sub-location as a row. 
                                  If False, keeps sub-locations grouped as lists. Defaults to True.

    Returns:
        pd.DataFrame: A processed DataFrame mapping major locations to their sub-locations.
    """
    with open("GOT/locations.json", "r", encoding="utf-8") as file:
        data = json.load(file)


    df = pd.DataFrame(data["regions"])

    #print(df)
    df["subLocation"] = df["subLocation"].apply(remove_nan)

    df = df[df["subLocation"].apply(lambda x: len(x)>0)]

    df["subLocation"] = df["subLocation"].apply(delete_duplicates_main)
    

    df = df.explode(column="subLocation")
    df = df.drop_duplicates(keep="first",subset="subLocation")
    df = df.groupby("location")["subLocation"].apply(list).reset_index()
    
    
    if explode:
        df = df.explode(column="subLocation")
    
    return df


#df = return_df_locations(explode=True)
#duplicates = df[df.duplicated(subset='subLocation', keep=False)]
#
#print(df)
#print(len(df))
#print(duplicates)
#print(len(duplicates))