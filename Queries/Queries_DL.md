# Intresting queries DL

## 1. Kings Guards
Male and MemberOfKingsGuard
Female and MemberOfKingsGuard

## 2. List of characters that belong to Stark
Character and (belongsToHouse value Stark)

## 3. Dragons/Dogs that belog to House
Mythical_Creatures and belongsToHouse some
Animal and belongsToHouse some

## 4. Dragons/dog that belong to house and killed someone
Animal and (belongsToHouse some) and (killed some)

## 5. Find Characters Who Are Allies of House Stark:
Character and (allies some (belongsToHouse value Stark))

## 6. Houses that have a member that is an allies to the Stark house
House and (hasMember some (allies some (belongsToHouse value Stark)))

## 7. Find Houses with Members Who Are Royals and Allies of House Stark:
House and (hasMember some (Royal and (allies some (belongsToHouse value Stark))))

## 8. Find someone that has been to the north of the wall and is a stark
Person and hasBeenTo some North_of_the_Wall and belongsToHouse value Stark

## 9. Someone killed by whitewalkers
Character and (isParentOf some (killedBy some White_Walkers))

## 10. Weapon wieldedBy somene that killed a dragon
beenWieldedBy some (killed some Dragon)

## 11. Find the house of someone that has been abducted
House and (hasMember some (abductedBy some))

## 12. Houses Killedby and Killed someone that belong to house Stark
House and (hasMember some (killed some (belongsToHouse value Stark))) and (hasMember some (killedBy some (belongsToHouse value Stark)))

## 13. VERY COMPLICATED
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