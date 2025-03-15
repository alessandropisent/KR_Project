import pandas as pd
import json


def return_max_exploded_df():
    with open("GOT/episodes.json","r")as file:
        data = json.load(file)


    #df = pd.DataFrame(data["episodes"])
    df = pd.json_normalize(data, record_path=['episodes'])
    df = df.explode(column="scenes")

    # Example: Assume df is your original DataFrame
    df_scenes_expanded = df['scenes'].apply(pd.Series)  # Expands the dictionary into separate columns

    # Now, merge this expanded data back with the original dataframe
    df_scenes = pd.concat([df.drop(columns=['scenes']), df_scenes_expanded], axis=1)

    ## No do for characters
    df_scenes = df_scenes.explode(column="characters")

    df_charaters_expanded = df_scenes["characters"].apply(pd.Series)

    df_charaters = pd.concat([df_scenes.drop(columns=['characters']), df_charaters_expanded], axis=1)

    ## wapons
    df_charaters = df_charaters.explode(column="weapon")

    df_weapon_explanded = df_charaters["weapon"].apply(pd.Series)
    df_weapon_explanded ["weapon.action"] = df_weapon_explanded ["action"]
    df_weapon_explanded ["weapon.name"] = df_weapon_explanded ["name"]
    df_weapon_explanded  = df_weapon_explanded.drop(columns=["name","action"])

    df_final = pd.concat([df_charaters.drop(columns=['weapon']), df_weapon_explanded], axis=1)
    
    return df_final


def return_df_weapons():

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
    

    df_final = return_max_exploded_df()


    df_locations = df_final.groupby("subLocation")["name"].apply(set).reset_index()
    df_locations["name"] = df_locations["name"].apply(list)
    
    return df_locations


#df = return_df_weapons()


#print(df)