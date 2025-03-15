from owlready2 import get_ontology


onto = get_ontology("GameOfThrones.owl").load()



#onto
print("\n\n Classes : ")
for c in onto.classes():
    print(c)

print("\n\nIndividuals : ")
for i in onto.individuals():
    print(i)

# Print available namespaces
#print("Namespaces:", list(onto.namespace_world.ontologies))
# Search for the Character class
Character = onto.search_one(iri="*Character")
test = Character("test")
