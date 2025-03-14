import pandas as pd
import json
from owlready2 import get_ontology


with open("GOT/characters.json", "r", encoding="utf-8") as file:
    data = json.load(file)

df = pd.DataFrame(data["characters"])

print(df.columns)
print(len(df))

house = set()
for i in  df["houseName"] : 
    if isinstance(i,list):
        for j in i:
            #print(j)
            house.add(j)
    else:
        #print(i)
        house.add(i) 
print("HOUSES")
print(house)

for col in df.columns:
    values = [i for i in df[col]]
    if True in values:
        print(f"bool : {col}")
    
count = 0
for index, character in df.iterrows():
    
    if character["kingsguard"] == True:
        #print(character["characterName"])
        count +=1

print(f"TOTAL OF {count} kingsguards")

count = 0
for index, character in df.iterrows():
    
    if character["royal"] == True:
        #print(character["characterName"])
        count +=1

print(f"TOTAL OF {count} Royal")

#print(df[df["characterName"]=="Jon Snow"])
    
#df.to_excel("characters.xlsx")

def join_all_characters():
    with open("GOT/characters-gender-all.json", "r", encoding="utf-8") as file:
        data_gender = json.load(file)

    df_male = pd.DataFrame(data_gender["male"], columns=["characterName"])
    df_male["gender"] = "male"
    df_female = pd.DataFrame(data_gender["female"], columns=["characterName"])
    df_female["gender"] = "female"
    df_gender = pd.concat([df_female,df_male], ignore_index=True)

    #print(df_gender.columns)

    # Perform left join
    characters = df.merge(df_gender, on='characterName', how='left')
    #characters.to_excel("characters.xlsx")
    return characters

def join_characters():
    with open("GOT/characters-gender.json", "r", encoding="utf-8") as file:
        data_gender = json.load(file)
    df_gender = pd.DataFrame(data_gender["gender"])
    df_gender = df_gender.rename(columns={"characters":"characterName"})
    df_gender = df_gender.explode(column="characterName")
    #print(df_gender)
    characters = df.merge(df_gender, on='characterName', how='left')
    characters.to_excel("characters.xlsx")
    

df = join_all_characters()

onto = get_ontology("GameOfThrones.owl").load()

def search_or_create_character(name, df):
    # Create a mask to get the row for witch we have the right character
    mask = df["characterName"] == name
    
    # if we have found the character in the dataframe
    if mask.any():
        row = df[mask].iloc[0]
    
    #print(row)
    character_name_underscore = name.replace(" ", "_")
     # Check if character already exists in the ontology
    char = onto.search_one(iri="*" + character_name_underscore)
    
    # if already exit return it
    if char:
        return char      
    
    # Create new character instance according to gender
    # if there is such character in the dataframe as primary
    elif mask.any():
        
        ## First we add the character, if it has some gender, to the corresping class
        if row["gender"] == "male":
            char = onto.Male(character_name_underscore)
        elif row["gender"] == "female":
            char = onto.Female(character_name_underscore)
        
        if row["royal"] == True:
            if char:
                char.is_a.append(onto.Royal)
            else:
                char = onto.Royal(character_name_underscore)
        
        if row["kingsguard"] == True:
            if char:
                char.is_a.append(onto.MemberOfKingsGuard)
            else:
                char = onto.MemberOfKingsGuard(character_name_underscore)
            
    # if i need i add it to characters generic    
    if not char:
        Character = onto.search_one(iri="*Character")
        char = Character(character_name_underscore)
    
    return char

"""def create_relation_funtional( subject,
                               predicate,
                               object_in_table,
                               df):
    # first check that is not NaN
    if not pd.isna(object_in_table):
        # If it a list of string, do a for
        if not isinstance(object_in_table,str) and isinstance(object_in_table,(list,tuple)):
            for obj_i in object_in_table:
                o = search_or_create_character(obj_i,df)
                # Add the isSiblingOf relationship if not already present
                if o not in subject.predicate:
                    subject.predicate.append(o)
        #else if it is a string do onece
        elif isinstance(object_in_table,str):
            o = search_or_create_character(object_in_table,df)
            # Add the isSiblingOf relationship if not already present
            if o not in subject.predicate:
                subject.predicate.append(o)"""


with onto:
    
    for i ,row in df.iterrows():
        #print(row)
        character_name_underscore = row["characterName"].replace(" ", "_")

        char = search_or_create_character(row["characterName"],df)
        
        ## Then if it has a nickname we add it
        if not pd.isna(row["nickname"]):
            char.label = [row["characterName"]].append(row["nickname"])

        if isinstance(row["houseName"],(list,tuple)) and not isinstance(row["houseName"],str):
            for h in row["houseName"]:
                    char.belongsToHouse.append(onto[h])
        elif not pd.isna(row["houseName"]) and isinstance(row["houseName"],str):
            #print(row["houseName"])
            # if is not a str, it is a list of houses so we put each house to it
            char.belongsToHouse.append(onto[row["houseName"]])
        
        ### ---- Siblings 
        # Process siblings (assumed to be a list) and not str        
        if not isinstance(row["siblings"],str) and isinstance(row["siblings"],(list,tuple)):
            
            for sibling in row["siblings"]:
                
                sibling_obj = search_or_create_character(sibling,df)
                
                # Add the isSiblingOf relationship if not already present
                if sibling_obj not in char.isSiblingOf:
                    char.isSiblingOf.append(sibling_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["siblings"]) and isinstance(row["siblings"],str):
                
           
            sibling_obj = search_or_create_character(row["siblings"],df)
            # Add the isSiblingOf relationship if not already present
            if sibling_obj not in char.isSiblingOf:
                char.isSiblingOf.append(sibling_obj)
        
        ## ----- Parents
        # Process parents (assumed to be a list) and not str        
        if not isinstance(row["parents"],str) and isinstance(row["parents"],(list,tuple)):
            
            for obj_i in row["parents"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the isChildOf relationship if not already present
                if char_obj not in char.isChildOf:
                    char.isChildOf.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["parents"]) and isinstance(row["parents"],str):
                
           
            char_obj = search_or_create_character(row["parents"],df)
            # Add the isChildOf relationship if not already present
            if char_obj not in char.isChildOf:
                char.isChildOf.append(char_obj)
        
        ## ----- Parents of 
        # Process parents Of (assumed to be a list) and not str        
        if not isinstance(row["parentOf"],str) and isinstance(row["parentOf"],(list,tuple)):
            
            for obj_i in row["parentOf"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the isParentOf relationship if not already present
                if char_obj not in char.isParentOf:
                    char.isParentOf.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["parentOf"]) and isinstance(row["parentOf"],str):
                
           
            char_obj = search_or_create_character(row["parentOf"],df)
            # Add the isParentOf relationship if not already present
            if char_obj not in char.isParentOf:
                char.isParentOf.append(char_obj)
        
        ## ---- KilledBy
        # Process KilledBy (assumed to be a list) and not str        
        if not isinstance(row["killedBy"],str) and isinstance(row["killedBy"],(list,tuple)):
            
            for obj_i in row["killedBy"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the iskilledBy relationship if not already present
                if char_obj not in char.killedBy:
                    char.killedBy.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["killedBy"]) and isinstance(row["killedBy"],str):
                
           
            char_obj = search_or_create_character(row["killedBy"],df)
            # Add the killedBy relationship if not already present
            if char_obj not in char.killedBy:
                char.killedBy.append(char_obj)
        
        ## ---- Killed
        # Process Killed (assumed to be a list) and not str        
        if not isinstance(row["killed"],str) and isinstance(row["killed"],(list,tuple)):
            
            for obj_i in row["killed"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the iskilled relationship if not already present
                if char_obj not in char.killed:
                    char.killed.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["killed"]) and isinstance(row["killed"],str):
                
           
            char_obj = search_or_create_character(row["killed"],df)
            # Add the killed relationship if not already present
            if char_obj not in char.killed:
                char.killed.append(char_obj)
        
        
        
        #if i >= 10:
        #    break

# Changes are now part of the ontology
onto.save("modified_ontology.owl")