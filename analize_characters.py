import pandas as pd
import json


def return_df_characters():
    with open("GOT/characters.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    df = pd.DataFrame(data["characters"])

    #print(df.columns)
    #print(len(df))

    house = set()
    for i in  df["houseName"] : 
        if isinstance(i,list):
            for j in i:
                #print(j)
                house.add(j)
        else:
            #print(i)
            house.add(i) 
    #print("HOUSES")
    #print(house)

    allies = set()
    for i in  df["houseName"] : 
        if isinstance(i,list):
            for j in i:
                #print(j)
                allies.add(j)
        else:
            #print(i)
            allies.add(i) 
    #print("Allies")
    #print(allies)

    with open("ranges.txt","w") as f:
        for col in ["servedBy", "marriedEngaged", "serves", "guardedBy", "guardianOf", "allies", "abductedBy", "abducted", "sibling"]:
            set_values = set()
            for i in df[col] : 
                if isinstance(i,list):
                    for j in i:
                        #print(j)
                        set_values.add(j)
                else:
                    #print(i)
                    set_values.add(i) 
            
            f.write(f"# {col}\n\n\n")
            for v in set_values:
                f.write(f"- {v}\n")
            f.write("\n\n")

    for col in df.columns:
        values = [i for i in df[col]]
        if True in values:
            #print(f"bool : {col}")
            pass
        
    count = 0
    for index, character in df.iterrows():
        
        if character["kingsguard"] == True:
            #print(character["characterName"])
            count +=1

    #print(f"TOTAL OF {count} kingsguards")

    count = 0
    for index, character in df.iterrows():
        
        if character["royal"] == True:
            #print(character["characterName"])
            count +=1

    #print(f"TOTAL OF {count} Royal")

    #print(df[df["characterName"]=="Jon Snow"])
        
    #df.to_excel("characters.xlsx")

    def count_list(el):
        if isinstance(el,str):
            return 1
        elif isinstance(el,list):
            return len(el)
        return el

    def join_all_characters():
        with open("GOT/characters-gender-all.json", "r", encoding="utf-8") as file:
            data_gender = json.load(file)

        df_male = pd.DataFrame(data_gender["male"], columns=["characterName"])
        df_male["gender"] = "male"
        df_female = pd.DataFrame(data_gender["female"], columns=["characterName"])
        df_female["gender"] = "female"
        df_gender = pd.concat([df_female,df_male], ignore_index=True)

        #print(df_gender.columns)
        #print(f"len before merge {len(df)}")
        # Perform left join
        characters = df.merge(df_gender, on='characterName', how='left')
        #print(f"len after {len(characters)}")
        #characters.to_excel("characters.xlsx")
        return characters

    def join_characters():
        with open("GOT/characters-gender.json", "r", encoding="utf-8") as file:
            data_gender = json.load(file)
        df_gender = pd.DataFrame(data_gender["gender"])
        df_gender = df_gender.rename(columns={"characters":"characterName"})
        df_gender = df_gender.explode(column="characterName")
        #print(df_gender)
        #print(f"len before merge {len(df)}")
        characters = df.merge(df_gender, on='characterName', how='left')
        #print(f"len after {len(characters)}")
        characters.to_excel("characters.xlsx")
        
    df_direwolfs = pd.DataFrame({"characterName":["Grey Wind", "Lady", "Nymeria", "Shaggydog", "Summer", "Ghost"]})
    df_direwolfs["type"] = "Direwolf"

    df_monsters = pd.DataFrame({"characterName":["Mag the Mighty Wight", "The Night King", "White Walker", "Wight Wildling Girl", "Wun Wun Wight"]})
    df_monsters["type"] = "White_Walkers"
    df = join_all_characters()

    df_dragons = pd.DataFrame({"characterName":["Drogon","Rhaegal","Viserion"]})
    df_dragons["type"] = "Dragon"

    df_types = pd.concat([df_direwolfs,df_monsters,df_dragons])

    # Adding wolfs, white_walkers and Dragons
    df = df.merge(df_types, on="characterName", how="left")

    df["hasChildren"] = df["parentOf"].apply(count_list)
    df["hasSiblings"] = df["parentOf"].apply(count_list)
    df["hasAllies"] = df["allies"].apply(count_list)
    df["hasKilled"] = df["killed"].apply(count_list)




    #mask = df["actorName"].all() and df["actorLink"].notna() and 

    characters_to_remove = ["Dothraki Bloodrider #1", 
                            "Dothraki Bloodrider #2", 
                            "Drowned Priest", 
                            "Goldcloak", 
                            "Great Master #1", 
                            "Great Master #2", 
                            "Great Master #3", 
                            "Great Master #4", 
                            "Great Master #5", 
                            "Great Master #6", 
                            "Great Master #7", 
                            "Handmaid", 
                            "King's Landing Rioter #1", 
                            "King's Landing Rioter #2", 
                            "King's Landing Rioter #3", 
                            "Little Bird #3", 
                            "Little Bird #4", 
                            "Little Bird #5", 
                            "Little Bird #6", 
                            "Little Bird #7", 
                            "Loyal Night's Watchman #1", 
                            "Loyal Night's Watchman #2", 
                            "Musician #1", 
                            "Musician #1", 
                            "Musician #2", 
                            "Musician #2", 
                            "Musician #3", 
                            "Musician #3", 
                            "Musician #4", 
                            "Musician #5", 
                            "Night's Watch Deserter", 
                            "Night's Watch Messenger", 
                            "Night's Watch Officer", 
                            "Night's Watch Officer", 
                            "Night's Watchman", 
                            "Night's Watchman", 
                            "Night's Watchman", 
                            "Night's Watchman #1", 
                            "Night's Watchman #2", 
                            "Night's Watchman #2", 
                            "Northman Rioter", 
                            "Old Woman Prisoner", 
                            "Stark Guard",
                            "White Walker"]

    mask = df["houseName"].notna() |\
        df['royal'].notna() | \
        df['parents'].notna() |\
        df['siblings'].notna() |\
        df['killedBy'].notna() |\
        df['nickname'].notna() |\
        df['killed'].notna() |\
        df['servedBy'].notna() |\
        df['parentOf'].notna() |\
        df['marriedEngaged'].notna() |\
        df['serves'].notna() |\
        df['kingsguard'].notna() |\
        df['guardedBy'].notna() |\
        df['guardianOf'].notna() |\
        df['allies'].notna() |\
        df['abductedBy'].notna() |\
        df['abducted'].notna() |\
        df['sibling'].notna() |\
        df['type'].notna() |\
        df['hasChildren'].notna() |\
        df['hasSiblings'].notna() |\
        df['hasAllies'].notna() |\
        df['hasKilled'].notna()

    #print(mask)

    df = df[mask]
    df = df[~df['characterName'].isin(characters_to_remove)]
    df = df.reset_index(drop=True)
    
    return df

#df = return_df_characters()

#print(df)


#with open("names.txt","w") as f:
#    for i,row in df.iterrows():
#        f.write(f"{i+1}. {row["characterName"]}\n")
#
#df.to_csv("characters.csv")
#
