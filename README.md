# IMKI - Technical test

## Purpose

The purpose of this projet is to create a Dungeon Map Generator using a Q-Learning ML algorithm

The map is a 4x4 matrix with 3 "rooms" (starting point SP, tresor point TP, and ending point EP) and walls.

The algorithm must place rooms and create corridor leading to the rooms.

## Bias

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

There will be a function to return a curated action list to avoid illegal action (creating an already existing room, destroying an already destroyed wall, creating a room in an already occupied space)

The reward function will work following these criteria :

- Create a room : +1 point
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

![wall-indexes](https://user-images.githubusercontent.com/1528493/124257075-4655bc80-db2c-11eb-9774-86340027642b.png)

```
0000000000000000000000000000000000000000 # Blank map

0000000000000000444444444444444444444444 # Full wall map

1000000002000003000040444004040440404440 # Map in screenshot
```

![map](https://user-images.githubusercontent.com/1528493/124257068-45bd2600-db2c-11eb-9223-3cc1bb62ab89.png)

## Project structure

### Environment class

Represent the map with which the agent will interact. It provide 3 public methods :

- reward(state, action) : the direct reward associated to an action in a certain state
- curatedActions(state) : the curated action list from a state
- updateState(state, action) : the new state from a state and an action

### QAgent class

Represent the agent using the Q-Learning algorithm, based on a "Q-Map" associating (state, action) -> value. It provide 2 methods :

- train : train the algorithm by repetedly generating map and improving the Q-Map
- generate : generate a map without updating the Q-Map

Ideally, two other methods should be available :

- save : export the Q-Map in a file
- load : import the Q-Map from a file

The Q-Map is a dict of dict. First level will have state as keys, and second level will have actions as key with value = cumulated value. By default, every value will be 0
