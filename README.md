# Game Bot

A discord bot to help the playing of games over Discord

NOTE: This is a work in progress so any issues encounter please raise them; and I will fix them

## Invite Game Bot to your Discord server:

https://discord.com/api/oauth2/authorize?client_id=798650871403249694&permissions=522304&scope=bot

Invite as Admin: https://discord.com/api/oauth2/authorize?client_id=798650871403249694&permissions=8&scope=bot

## Using Game Bot

### Rolling

Use `/roll` to roll.  
You can roll multiple dice, add modifiers etc. to your rolls examples below and roll with advantage / disadvantage (D&D
term):

- `/roll dice:2d6`
- `/roll dice:1d8 + 1d6`
- `/roll dice:1d20 + 7`
- `/roll dice:2d20kh1 + 7` Roll keeping the highest result then adding 7
- `/roll dice:2d20kl1 + 8` Roll keeping the lowest result then adding 8
- `/roll dice:2d8*2 + 2` Roll 2d8 times the result by 2 and then add 2
- `/roll dice:3[2d6 + 5]` Repeat the action of rolling 2d6 and then adding 5

### Calculation

Basic calculation can be done by using `/c`: adding, subtracting, multiplication, division, and brackets

- `/c (5 + 3)*7`

### Flipping

Coins can be flipped using the `/flip` command:

- `flip number_of_flips:6` flips 6 coins
- `/flip_until face:Heads` keeps flipping coins until you get heads

### Magic the Gathering

#### Extra flipping functionality

- `/flip_until face:Heads with_thub:Yes` keeps flipping coins until you get heads with Krark's Thumb on the battlefield

#### Searching the Scryfall Database

To search the database surround the card name with `/card`  
Example: `/card name:lightning bolt`

The API uses fuzzy matching, so the card can be slightly misspelt and it should return the card.

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

To roll a die, type `/roll dice:` followed by any of the following:

- Boost Die = bd
- Set Back Die = sbd
- Difficulty Die = dd
- Proficiency Die = pd
- Challenge Die = cd
- Force Die = fd

To roll more than one of the same die put a number before your die `/roll dice:3fd`. To roll more than one of a differing dice
separate them by a "+" `/roll dice:2fd + 6sbd`

#### The total calculation

The game bot will calculate number of successes vs failures and threat vs advantage and "total" them up according to the
game rules of the Edge of the Empire roleplaying game.   
An example roll of `/roll dice:3ad + cd + sd`:

```
Ability Die = ✶℧, ✶, ✶
Challenge Die = ⎊
Setback Die = ▢
Total = 2✶, ℧, ⎊
```

Another example roll of `/roll dice:3ad + cd + sd + pd`:

```
Ability Die = ℧, ✶℧, ✶℧
Challenge Die = ▼⎔
Setback Die = ▼
Proficiency Die = ℧℧
Total = 4℧
```
