# Intresting queries DL

#### VERY COMPLICATED
find the weapon that has been wieldad by :
1. Has been to The North.
2. Belongs to a house that has a member allied with the Baratheon house.

 (beenWieldedBy some ((hasBeenTo some The_North) and (belongsToHouse some ( hasMember some( allies some (belongsToHouse value Baratheon))))))

SELECT ?weapon
WHERE {
  ?weapon :beenWieldedBy ?wielder .
  ?wielder :hasBeenTo :The_North .
  ?wielder :belongsToHouse ?house .
  ?house :hasMember ?member .
  ?member :allies ?ally .
  ?ally :belongsToHouse :Baratheon .
}

[Obvs do not work beacuse hasMember is all done by reasoner]

### Houses Killedby and Killed someone that belong to house Stark
House and (hasMember some (killed some (belongsToHouse value Stark))) and (hasMember some (killedBy some (belongsToHouse value Stark)))

## Kings Guards
Male and MemberOfKingsGuard
Female and MemberOfKingsGuard

## List of characters that belong to Stark
Character and (belongsToHouse value Stark)

## Dragons/Dogs that belog to House
Mythical_Creatures and belongsToHouse some
Animal and belongsToHouse some

## Dragons/dog that belong to house and killed someone
Animal and (belongsToHouse some) and (killed some)

## Characters that killed some animal
Character and killed some Animal

## Characters that killed some Mystical Chreatures
Character and killed some Mythical_Creatures

## Houses that have a member that is an allies to the Stark house
House and (hasMember some (allies some (belongsToHouse value Stark)))

## Find Characters Who Are Allies of House Stark:
Character and (allies some (belongsToHouse value Stark))

## Find Houses with Members Who Are Royals and Allies of House Stark:
House and (hasMember some (Royal and (allies some (belongsToHouse value Stark))))

## Find someone that has been to the north of the wall and is a stark
Person and hasBeenTo some North_of_the_Wall and belongsToHouse value Stark

## Someone killed by whitewalkers
Character and (isParentOf some (killedBy some White_Walkers))

## Weapon wieldedBy somene that killed a dragon
beenWieldedBy some (killed some Dragon)

## Find the house of someone that has been abducted
House and (hasMember some (abductedBy some))

# Open World assumption

## Retrieve Characters Who Are Royals and Have Male Allies
Character and (allies some (Royal and Male))

##  Retrieve Characters Who Are Royals and Do Not Have Male Allies
Character and (hasAlly only (Royal and not Male))


