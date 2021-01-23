# Game Bot
A discord bot to help the playing of games over Discord

NOTE: This is a work in progress so any issues encounter please raise them and I will fix them

## Invite Game Bot to your Discord server:
https://discord.com/api/oauth2/authorize?client_id=798650871403249694&permissions=522304&scope=bot

Invite as Admin: https://discord.com/api/oauth2/authorize?client_id=798650871403249694&permissions=8&scope=bot


## Using Game Bot

#### Rolling
Use `/r` to roll.  
You can roll multiple dice, add modifiers etc. to your rolls examples below and roll with advantage / disadvantage (D&D term):  
- `/r 2d6`
- `/r 1d8 + 1d6`
- `/r 1d20 + 7`
- `/r 2d20kh1 + 7` Roll keeping the highest result then adding 7
- `/r 2d20kl1 + 8` Roll keeping the lowest result then adding 8
- `/r 2d8*2 + 2` Roll 2d8 times the result by 2 and then add 2
- `/r 3[2d6 + 5]` Repeat the action of rolling 2d6 and then adding 5

#### Calculation
Basic calculation can be done by using `/c`: adding, subtracting, multiplication, division, and brackets
- `/c (5 + 3)*7`

#### Flipping
Coins can be flipped using the `/flip` command:
- `/flip` flips one coin
- `flip 6` flips 6 coins
- `/flip until heads` keeps flipping coins until you get heads

### Magic the Gathering
#### Extra flipping functionality
- `/flip until heads with thub` keeps flipping coins until you get heads with Krark's Thumb on the battlefield

#### Searching the Scryfall Database
To search the database surround the card name with double square brackets  
Example: `I really like [[lightning bolt]]`

Note that the card can be anywhere in the message and that you can put multiple cards in the message

Example: `I really like how [[exquisite blood]] and [[sanguine bond]] cards combo`

The API uses fuzzy matching, so the card can be slightly misspelt and it should return the card.

### Dungeons and Dragons
#### Searching for spells
You can search for a spell using `/s`
Example: `/s fireball`

### Star Wars: Edge of the Empire
#### Rolling
The following dice can be rolled:  
- Boost Die
- Set Back Die
- Difficulty Die
- Proficiency Die
- Challenge Die
- Force Die

The specialised symbols on these dice are as follows:  
- Success = ✶
- Fail = ▼
- Triumph = ⎈
- Advantage = ℧
- Despair = ⎊
- Threat = ⎔
- Light = ○
- Dark = ●
- Blank = ▢

To roll a die, type "/r" followed by any of the following:
- Boost Die = bd
- Set Back Die = sbd
- Difficulty Die = dd
- Proficiency Die = pd
- Challenge Die = cd
- Force Die = fd

To roll more than one of the same die put a number before your die `/r 3fd`.
To roll more than one of a differing dice separate them by a "+" `/r 2fd + 6sbd`
