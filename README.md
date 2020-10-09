# Caves & Catacombs
Text-based hack & slash python challenge project. 
* Battle monsters
  * Monsters spawn with random name and stats
  * Monster difficulty scales with player's level

* Loot system
  * Player can seach for items at any time
  * Each item has a limited quantity
  * Items have negative and positive alignment
  * Failed looting decreases the player's HP
  * Equipment found is automatically equipped

* Spells
  * Fire spell is unlocked at level 3
  * Wind spell is unlocked at level 6
  * Spells have limited uses
  * Fire regens 1 per level-up
  * Wind regens 1 per every second level-up

* Level up
  * Leveling up increases player's stats and refills HP

* Progress bar displays player traveling from level 1 to 20

* Boss battle at level 20
  * Defeating the boss ends game

### Installation Notes:
* Playsound library is required to run, please install with:
`python3 -m pip install playsound`
* Playsound on Mac OS may need pyobjc to be installed:
`python3 -m pip install pyobjc`
* Playsound on Linux may need gstreamer installed
`sudo apt-get install gstreamer-1.0`

### AWS Cloud9 Notes:
* Please use the cloud9.py file to run the game if launching from Cloud9 Terminal
