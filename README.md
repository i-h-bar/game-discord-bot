# Game Bot
A discord bot to help the playing of games over Discord

NOTE: This is a work in progress so any issues encounter please raise them and I will fix them

## Invite Game Bot to your Discord server:
https://discord.com/api/oauth2/authorize?client_id=798650871403249694&permissions=522304&scope=bot

Invite as Admin: https://discord.com/api/oauth2/authorize?client_id=798650871403249694&permissions=8&scope=bot


## Using Game Bot
If at anytime you need help type: `!help` or `/help`

At the moment these are the games that Game Bot supports:
- Magic the Gathering
- Dungeons & Dragons
- Star Wars: Edge of the Empire

### To set which game you want to play use the `!set` command example: `!set mtg`

- mtg = Magic the Gathering
- dnd = Dungeons & Dragons
- edge = Star Wars: Edge of the Empire

### Magic the Gathering

#### Rolling
Use `/r` to roll.  
You can roll multiple dice, add modifiers etc. to your rolls examples below and roll with advantage / disadvantage (D&D term):  
- `/r 2d6`
- `/r 1d8 + 1d6`
- `/r 1d20 + 7`
- `/r 2d20kh1 + 7` Roll keeping the highest result then adding 7
- `/r 2d20kl1 + 8` Roll keeping the lowest result then adding 8
- `/r 2d8*2 + 2` Roll 2d8 times the result by 2 and then add 2

#### Calculation
Basic calculation can be done by using `/c`: adding, subtracting, multiplication, division, and brackets
- `/c (5 + 3)*7`

#### Flipping
Coins can be flipped using the `/flip` command:
- `/flip` flips one coin
- `flip 6` flips 6 coins
- `/flip until heads` keeps flipping coins until you get heads
- `/flip until heads with thub` keeps flipping coins until you get heads with Krark's Thumb on the battlefield

#### Searching the Scryfall Database
To search the database use `/s`
Example: `/s lightning bolt`

The API uses fuzzy matching, so the card can be slightly misspelt and it should return the card.

### Dungeons and Dragons
#### Searching for spells
You can search for a spell using `/s`
Example: `/s fireball`

#### Rolling
Use `/r` to roll.  
You can roll multiple dice, add modifiers etc. to your rolls examples below and roll with advantage / disadvantage (D&D term):  
- `/r 2d6`
- `/r 1d8 + 1d6`
- `/r 1d20 + 7`
- `/r 2d20kh1 + 7` Roll keeping the highest result then adding 7
- `/r 2d20kl1 + 8` Roll keeping the lowest result then adding 8
- `/r 2d8*2 + 2` Roll 2d8 times the result by 2 and then add 2

#### Calculation
Basic calculation can be done by using `/c`: adding, subtracting, multiplication, division, and bracket s
- `/c (5 + 3)*7`

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

To roll more than one of the same die put a number before your die "/r 3fd".
To roll more than one of a differing dice separate them by a "+" "/r 2fd + 6sbd"

For help at any time type "/help" and the bot will give you instructions

### Not Setting a Game
Some basic functionality exists if you don't set a game
- rolling
- calculator
- searches

#### Rolling
Use `/r` to roll.  
You can roll multiple dice, add modifiers etc. to your rolls examples below and roll with advantage / disadvantage (D&D term):  
- `/r 2d6`
- `/r 1d8 + 1d6`
- `/r 1d20 + 7`
- `/r 2d20kh1 + 7` Roll keeping the highest result then adding 7
- `/r 2d20kl1 + 8` Roll keeping the lowest result then adding 8
- `/r 2d8*2 + 2` Roll 2d8 times the result by 2 and then add 2

#### Calculator
Basic calculation can be done by using `/c`: adding, subtracting, multiplication, division, and bracket s
- `/c (5 + 3)*7`

#### Searching SRD or Scryfall
You can still search the SRD or Scryfall without setting a game.
- For Magic the Gathering use: `/s mtg`
- For Dungeons & Dragons use: `/s dnd`  
examples: `/s dnd fireball` or `/s mtg lightning bolt`


