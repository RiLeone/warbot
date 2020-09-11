# WarBot

A sort of autonomous, simulated game of Risiko in Python3.

## Acronyms
|Acronym | Meaning|
|:-------|:-------|
|TBI     | To be implemented |
|WIP     | Work in progress |


## Contributing Guidelines

Please review the guidelines reported in CONTRIBUTING before starting to work on
this project.


## Game Description

The world was at peace. Before the beginning, no battles were occurring. States
were secretly getting ready, growing and building infrastructure.
Suddenly, on a nice sunny day, complete mayhem broke out. States started
battling each other, everyone wanted to conquer the world... Silly states. But
so the story goes and eventually a new overlord imposed itself and reigned ever
since. This is, in a nutshell, what happens during a game.


### First Things First: Before the Beginning

A peaceful but tense **world** exists at the beginning. This is a collection
of **states**. A state has an **area**, a **population**, a **growth rate** (TBI),
a **shape** (TBI), and **neighbors**. Neighbors are problematic. No state wants
neighbors. The only solution: conquer everybody else. The world is fully defined
by a (set of) JSON files and the user can choose in which realm they want to
play.


### Could Not Care Less About What is About to go Down: Time and Turns

To spare the user from complete chaos there is but one thing: time. Time does
not care about the states. It goes on, turn by turn. Battles can only occur
during a **turn**. A turn is the elementary time unit in this bizarre world. At
each turn, at least one battle is guaranteed to occur.
* At the beginning of a turn: battling pairs are picked (randomly);
* During a turn:
  * Battles take place;
  * Resting states grow (TBI);
* At the end of a turn: the states are updated based on the growth and battle outcomes.


### After the End: Last State Standing

After a set of (max) turns or when a single overlord remains (and no insurgences
are allowed (TBI)) the game ends in void. Like in the real world, it started from
nothing and will (possibly) end in nothing. Here though you get something as you
survive the end of it: the knowledge of how it ended and statistics (TBI)
about what happened.


### Example Turn Visualization

The following images describe more than what thousands of words ever could, how
a turn goes down.

![Initial condition](img/initial_condition.png)
The world is (seamingly) at peace.

![What happens under the hood](img/turn_illustrated.png)
C and G clash! It is a fierce battle determined purely by a pseudorandom number
generator... While the two fight, the others grow.

![After the dust has set](img/end_of_turn.png)
The turn is over. C won the battle and thus is now in control of what formerly
known as G. Who knows if the fierce Gers will revolt in the future? New
neighbors have been devined for (all) the states. The game can continue - what
will happen next?
