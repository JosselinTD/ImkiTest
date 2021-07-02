# IMKI - Technical test

## Purpose

The purpose of this projet is to create a Dungeon Map Generator using a Q-Learning ML algorithm

The map is a 4x4 matrix with 3 "rooms" (starting point SP, tresor point TP, and ending point EP) and walls.

The algorithm must place rooms and create corridor leading to the rooms.

## Bias

It's not precised in the initial statement but we will train our algorithm to avoid create "white space" : there can be only corridor and no big empty space of 2x2 cases or more. It's for avoiding creating a completely empty space with only the 3 rooms and no corridor.

The map will begin with no rooms and walls everywhere.

The map will be define in 2 parts :

- Spaces in which can be added one of the three rooms : 16 spaces
- Walls dividing spaces : 24 walls

The available actions (A) will be as follow :

- Create SP on case 1
- Create SP on case 2
  ...
- Create SP on case 16

- Create TP on case 1
- Create TP on case 2
  ...
- Create TP on case 16

- Create EP on case 1
- Create EP on case 2
  ...
- Create EP on case 16

- Break wall 1
- Break wall 2
  ...
- Break wall 24

There will be a function to return a curated action list to avoid illegal action (creating an already existing room, destroying an already destroyed wall, creating a room in an already occupied space, creating a 2x2 or more white space)

The reward function will work following these criteria :

- Set maximum distance between rooms : +1 point for each case between rooms when placing them
- Connect two rooms : +5 points for achieving a path between two rooms not already connected
- Random path between rooms : +0 points for breaking a wall

## Technical needs

- A reward function
- A curate action function
- A map representation
- A Q-Function : (state, action) -> value based on a (state, action) -> value list with value = 0 when no info

### Map representation

A string of 40 (16+24) int. First 16 indexes are spaces, last 24 indexes are walls

```
0000000000000000000000000000000000000000 # Blank map

0000000000000000111111111111111111111111 # Full wall map

1000000002000003000010111001010110101110 # Map in screenshot
```
