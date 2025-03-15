import pandas as pd
from owlready2 import get_ontology
from analize_characters import return_df_characters

df = return_df_characters()

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
        
        if pd.isna(row["type"]):
        
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
        
        elif row["type"] == "Direwolf":
            char = onto.Direwolf(character_name_underscore)
        elif row["type"] == "Dragon":
            char = onto.Dragon(character_name_underscore)
        elif row["type"] == "White_Walkers":
            char = onto.White_Walker(character_name_underscore)
            
        
            
    # if i need i add it to characters generic    
    if not char:
        #Character = onto.search_one(iri="*Character")
        #char = Character(character_name_underscore)
        char = onto.Person(character_name_underscore)
    
    return char

with onto:
    ##### CHARACTERS
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
        
        ### ---- Siblings 
        # Process sibling (assumed to be a list) and not str        
        if not isinstance(row["sibling"],str) and isinstance(row["sibling"],(list,tuple)):
            
            for sibling in row["sibling"]:
                
                sibling_obj = search_or_create_character(sibling,df)
                
                # Add the isSiblingOf relationship if not already present
                if sibling_obj not in char.isSiblingOf:
                    char.isSiblingOf.append(sibling_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["sibling"]) and isinstance(row["sibling"],str):
                
           
            sibling_obj = search_or_create_character(row["sibling"],df)
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
        
        #### ----- ServedBy
        # Process ServedBy (assumed to be a list) and not str        
        if not isinstance(row["servedBy"],str) and isinstance(row["servedBy"],(list,tuple)):
            
            for obj_i in row["servedBy"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the servedBy relationship if not already present
                if char_obj not in char.servedBy:
                    char.servedBy.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["servedBy"]) and isinstance(row["servedBy"],str):
                
           
            char_obj = search_or_create_character(row["servedBy"],df)
            # Add the servedBy relationship if not already present
            if char_obj not in char.servedBy:
                char.servedBy.append(char_obj)
        
        #### ----- serves
        # Process Serves (assumed to be a list) and not str        
        if not isinstance(row["serves"],str) and isinstance(row["serves"],(list,tuple)):
            
            for obj_i in row["serves"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the serves relationship if not already present
                if char_obj not in char.serves:
                    char.serves.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["serves"]) and isinstance(row["serves"],str):
                
           
            char_obj = search_or_create_character(row["serves"],df)
            # Add the serves relationship if not already present
            if char_obj not in char.serves:
                char.serves.append(char_obj)
        
        #### ----- marriedEngaged
        # Process Spouses (assumed to be a list) and not str        
        if not isinstance(row["marriedEngaged"],str) and isinstance(row["marriedEngaged"],(list,tuple)):
            
            for obj_i in row["marriedEngaged"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the Spouses relationship if not already present
                if char_obj not in char.isSpouseOf:
                    char.isSpouseOf.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["marriedEngaged"]) and isinstance(row["marriedEngaged"],str):
                
           
            char_obj = search_or_create_character(row["marriedEngaged"],df)
            # Add the isSpouseOf relationship if not already present
            if char_obj not in char.isSpouseOf:
                char.isSpouseOf.append(char_obj)
        
        #### ----- guardedBy
        # Process guardedBy (assumed to be a list) and not str        
        if not isinstance(row["guardedBy"],str) and isinstance(row["guardedBy"],(list,tuple)):
            
            for obj_i in row["guardedBy"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the Spouses relationship if not already present
                if char_obj not in char.guardedBy:
                    char.guardedBy.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["guardedBy"]) and isinstance(row["guardedBy"],str):
                
           
            char_obj = search_or_create_character(row["guardedBy"],df)
            # Add the guardedBy relationship if not already present
            if char_obj not in char.guardedBy:
                char.guardedBy.append(char_obj)
        
        #### ----- guardianOf
        # Process guardianOf (assumed to be a list) and not str        
        if not isinstance(row["guardianOf"],str) and isinstance(row["guardianOf"],(list,tuple)):
            
            for obj_i in row["guardianOf"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the Spouses relationship if not already present
                if char_obj not in char.guardianOf:
                    char.guardianOf.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["guardianOf"]) and isinstance(row["guardianOf"],str):
                
           
            char_obj = search_or_create_character(row["guardianOf"],df)
            # Add the guardianOf relationship if not already present
            if char_obj not in char.guardianOf:
                char.guardianOf.append(char_obj)
        
        #### ----- allies
        # Process allies (assumed to be a list) and not str        
        if not isinstance(row["allies"],str) and isinstance(row["allies"],(list,tuple)):
            
            for obj_i in row["allies"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the Spouses relationship if not already present
                if char_obj not in char.allies:
                    char.allies.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["allies"]) and isinstance(row["allies"],str):
                
           
            char_obj = search_or_create_character(row["allies"],df)
            # Add the allies relationship if not already present
            if char_obj not in char.allies:
                char.allies.append(char_obj)
        
        #### ----- abductedBy
        # Process abductedBy (assumed to be a list) and not str        
        if not isinstance(row["abductedBy"],str) and isinstance(row["abductedBy"],(list,tuple)):
            
            for obj_i in row["abductedBy"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the Spouses relationship if not already present
                if char_obj not in char.abductedBy:
                    char.abductedBy.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["abductedBy"]) and isinstance(row["abductedBy"],str):
                
           
            char_obj = search_or_create_character(row["abductedBy"],df)
            # Add the abductedBy relationship if not already present
            if char_obj not in char.abductedBy:
                char.abductedBy.append(char_obj)
        
        #### ----- abducted
        # Process abducted (assumed to be a list) and not str        
        if not isinstance(row["abducted"],str) and isinstance(row["abducted"],(list,tuple)):
            
            for obj_i in row["abducted"]:
                
                char_obj = search_or_create_character(obj_i,df)
                
                # Add the Spouses relationship if not already present
                if char_obj not in char.abducted:
                    char.abducted.append(char_obj)
        
        # then it is a string [since is not none]         
        elif not pd.isna(row["abducted"]) and isinstance(row["abducted"],str):
                
           
            char_obj = search_or_create_character(row["abducted"],df)
            # Add the abducted relationship if not already present
            if char_obj not in char.abducted:
                char.abducted.append(char_obj)
        
        ###########################################
        #### DATAPROPERITY
        
        #########################
        
        # hasChildren
        if not pd.isna(row["hasChildren"]):
            char.hasChildren = int(row["hasChildren"])
        # hasSiblings
        if not pd.isna(row["hasSiblings"]):
            char.hasSiblings = int(row["hasSiblings"])
        
        # hasAllies
        if not pd.isna(row["hasAllies"]):
            char.hasAllies = int(row["hasAllies"])
        
        # hasKilled
        if not pd.isna(row["hasKilled"]):
            char.hasKilled = int(row["hasKilled"])
        
        
        #if i >= 10:
        #    break

# Changes are now part of the ontology
onto.save("modified_ontology.owl")