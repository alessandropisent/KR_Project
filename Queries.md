# Intresting queries DL

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

# Open World assumption

## Retrieve Characters Who Are Royals and Have Male Allies
Character and (allies some (Royal and Male))

##  Retrieve Characters Who Are Royals and Do Not Have Male Allies
Character and (hasAlly only (Royal and not Male))
