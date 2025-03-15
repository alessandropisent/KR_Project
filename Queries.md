# Intresting queries DL

## Kings Guards
Male and MemberOfKingsGuard
Female and MemberOfKingsGuard

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