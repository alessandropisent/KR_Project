import pandas as pd
import json
import numpy as np

def remove_nan(el):
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
    return [sub for sub in row if sub not in locations]



def return_df_locations(explode=True):
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


df = return_df_locations(explode=True)
duplicates = df[df.duplicated(subset='subLocation', keep=False)]

print(df)
print(len(df))
print(duplicates)
print(len(duplicates))