PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX got: <http://www.semanticweb.org/aless/ontologies/2025/2/GameOfThronesOnotology#>

# 0. hasMember
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX got: <http://www.semanticweb.org/aless/ontologies/2025/2/GameOfThronesOnotology#>

SELECT ?house ?member
WHERE {
	?house got:hasMember ?member
}

(hasMember some)

PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX got: <http://www.semanticweb.org/aless/ontologies/2025/2/GameOfThronesOnotology#>

SELECT  ?member ?house
WHERE {
	?member got:belongsToHouse ?house
}


# 1. Kings Guards (Male and Female)
SELECT ?character WHERE {
    ?character rdf:type got:MemberOfKingsGuard .
    ?character rdf:type got:Male .
}

SELECT ?character WHERE {
    ?character rdf:type got:MemberOfKingsGuard .
    ?character rdf:type got:Female .
}

SELECT ?character WHERE {
   ?character rdf:type got:MemberOfKingsGuard .
   ?character rdf:type ?gender.
   VALUES ?gender {got:Male got:Female}
}

# 2. Characters that belong to Stark
SELECT ?character WHERE {
    ?character rdf:type got:Character .
    ?character got:belongsToHouse got:Stark .
}

# 3. Dragons/Dogs that belong to a House
SELECT ?creature WHERE {
    ?creature rdf:type got:Mythical_Creatures .
    ?creature got:belongsToHouse ?house .
}

SELECT ?animal WHERE {
    ?animal rdf:type got:Animal .
    ?animal got:belongsToHouse ?house .
}

# 4. Dragons/Dogs that belong to a House and killed someone
SELECT ?animal WHERE {
    ?animal rdf:type got:Animal .
    ?animal got:belongsToHouse ?house .
    ?animal got:killed ?victim .
}

# 5. Characters that killed some Animal
SELECT ?character WHERE {
    ?character rdf:type got:Character .
    ?character got:killed ?animal .
    ?animal rdf:type got:Animal .
}

# 6. Characters that killed some Mythical Creatures
SELECT ?character WHERE {
    ?character rdf:type got:Character .
    ?character got:killed ?creature .
    ?creature rdf:type got:Mythical_Creatures .
}

# 7. Houses that have a member who is an ally of House Stark
SELECT ?house WHERE {
    ?house rdf:type got:House .
    ?house got:hasMember ?member .
    ?member got:allies ?ally .
    ?ally got:belongsToHouse got:Stark .
}

# 8. Find Characters Who Are Allies of House Stark
SELECT ?character WHERE {
    ?character rdf:type got:Character .
    ?character got:allies ?ally .
    ?ally got:belongsToHouse got:Stark .
}

# 9. Find Houses with Members Who Are Royals and Allies of House Stark
SELECT ?house WHERE {
    ?house rdf:type got:House .
    ?house got:hasMember ?member .
    ?member rdf:type got:Royal .
    ?member got:allies ?ally .
    ?ally got:belongsToHouse got:Stark .
}

# 10. Find someone who has been to the north of the wall and is a Stark
SELECT ?person WHERE {
    ?person rdf:type got:Person .
    ?person got:hasBeenTo got:North_of_the_Wall .
    ?person got:belongsToHouse got:Stark .
}

# 11. Retrieve Characters Who Are Royals and Have Male Allies
SELECT ?character WHERE {
    ?character rdf:type got:Character .
    ?character got:allies ?ally .
    ?ally rdf:type got:Royal .
    ?ally rdf:type got:Male .
}

# 12. Retrieve Characters Who Are Royals and Do Not Have Male Allies
SELECT ?character WHERE {
    ?character rdf:type got:Character .
    ?character got:hasAlly ?ally .
    FILTER NOT EXISTS {
        ?ally rdf:type got:Male .
    }
}


#### ----
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX got: <http://www.semanticweb.org/aless/ontologies/2025/2/GameOfThronesOnotology#>

SELECT ?individual ?label
WHERE {
  ?individual rdfs:label ?label.
}
ORDER BY ASC(?individual)