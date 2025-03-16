Person and not MemberOfKingsGuard
Person and MemberOfKingsGuard

In neither of them we get Jon Snow, 

### SPARQL 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX got: <http://www.semanticweb.org/aless/ontologies/2025/2/GameOfThronesOnotology#>


## not in the king guard (show)

SELECT ?person WHERE {
  ?person rdf:type got:Male .
  FILTER(?person = got:Jon_Snow) .
  FILTER NOT EXISTS {
    ?person rdf:type got:MemberOfKingsGuard .
  }
}

## in the kings guard (no show)
SELECT ?person WHERE {
  ?person rdf:type got:Male .
  FILTER (?person = got:Jon_Snow)
  ?person rdf:type got:MemberOfKingsGuard .
}