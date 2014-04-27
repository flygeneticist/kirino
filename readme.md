#Kirino v0.0.8c
  
Basic console based dungeon crawler. 

##Release notes

This week's update added the possibility of attacking and destroying mobs. While this gets the whole thing closer to July's goal, it introduces a new problem: Balance. Doing 200 damage to a 20HP zombie after 10 floors is far from balanced, and the future item tiers and different mobs and bosses will only make the entire thing more difficult to balance and adjust. 

If you feel certain items need 'fixing', feel free to change the stats yourself. The item files are reasonably explained and you should have no problems. For now the mob data is generated in the mob class constructor. If you want to share your numbers, you can do so.

##How to use

run launch.py

Grab loot, kill zombies, explore dungeons. Help provided in game via the help menu (In the main menu and in the options menu during the game)

If you experience a crash, bug or any weird or unexpected behaviour that is not in the bugs file (`./info/bugs`), please consider reporting it. Suggestions and opinions are also welcome.

**Note**: All the files in the `./player` folder are just examples to show how are those files structured and formatted. After downloading or cloning the repo, it's safe (And recommended) to delete them.

##OS specific information

* Debian: Works as is, just type `python /path_to_file/launch.py` in the terminal.
* Ubuntu: Untested, but it should work as in Debian.
* Other linux distributions: Should work as long as python is installed (Untested).
* OSX: Untested.
* Windows: Kirino can't be used in windows' command prompt. You can play it in this platform using a terminal emulator like [MobaXterm](http://mobaxterm.mobatek.net/) with a python plugin. Different emulators may have different requirements to run python files, so read their documentation first.  
You may have some issues with the output formatting, but overall the game is playable.

##List of files/folders:

* data:               Files containing data for generators
  * inventory:          Inventory files
    * `atk_def_mod`:      List of attack/def modifiers
    * `attr_mod`:         List of basic attribute modifiers
    * `items_XX`:         List of items and basic stats
  * npcs:               NPC data
    * `appearance`        List of visual adjectives
    * `firstnames_female` List of female names
    * `firstnames_male`   List of male names
    * `jobs`              List of jobs
    * `personality`       List of psychological adjectives
    * `secondnames`       List of second names
    * `things`            List of things
  * parser:             Data filer for the word parser
    * `errors`:           List of generic error messages
    * `words`:            Word data for the parser
  * player:             Player files
    * `classes`:          List of player classes
    * `names`:            List of names
    * `races`:            List of player races
  * tutorial:           Files for the tutorial (Maps, etc)
    * `tutorial_1`
* docs:               Documentation folder (pydoc generated html files)
* info:               Information files
  * `bugs`:             List of bugs and weird behaviours to fix
  * `notes`:            Temporary notes on feature implementation
  * `todo`:             Ideas and stuff
* player:             Player files
  * `cemetery`:         Example cemetery file
  * `config`:           Example configuration file
  * `save`:             Example save file
* source:             Source file folder
  * `common.py`:        Common functions and procedures
  * `config.py`:        Configuration class
  * `dungeon.py`:       Dungeon class
  * `help.py`:          Help and tutorial
  * `item.py`:          Item class
  * `launch.py`:        Main menus and procedures.
  * `mob.py`:           Giant enemy class
  * `npc.py`:           NPC class
  * `parser.py`:        Word parser module
  * `player.py`:        Player class
* `readme.md`:        This file

##Changelog

####**v0.0.8** (2014-04-25):
* New features:
  * Combat system
  * [0.0.8b] Windows support
* Bugs fixed:
  * Some item messages not showing
  * HP and HP changing when opening sheet and loading characters
* Others:
  * Increased mob information
  * [0.0.8c] Charisma and vendor relationship influences price
  
####**v0.0.7** (2014-04-18):
* New features:
  * Word parser
  * NPC generator
  * Peddlers and vendors 
  * [0.0.7b] buying and selling items
* Bugs fixed:
  * [0.0.7b] Getting stuck at (0,0) when loading character
  * [0.0.7b] Crash when typing some invalid commands
  * [0.0.7c] Buying expensive items and ending with negative balance
  * [0.0.7c] Crash when pressing enter in trade menus
* Others:
  * Depurated code
  * Removed white spaces

####**v0.0.6** (2014-04-11):
* Bugs fixed:
  * Increasing stats also increases MP (Similar to bug fixed in v0.0.5)
* Others:
  * Save file is now deleted when dying
  * Depurated code
  * [0.0.6b] Improved message output

####**v0.0.5** (2014-04-04):
* Bugs fixed:
  * Increasing stats also increases HP
* Others:
  * Increased picked items/loot verbosity
  * Item attribute boost now appears in inventory
  * [v0.0.5b] Enabled white spaces

####**v0.0.4** (2014-03-28):
* New features:
  * Dead characters are now saved in a cemetery file
  * Added key mapping help screen
* Bugs fixed:
  * Fixed crash when executing `launch.py` from another directory
* Others:
  * A random name is now chosen if it's left empty when asked
  * Items can be saved and loaded with the player
  * The total number of floors explored is now saved with the character
  * When reporting a dungeon, the user is prompted for a message
  * [0.0.4b] Race can now be selected
  * [0.0.4c] Class can now be selected

####**v0.0.3** (2014-03-21):
* New features: 
  * Tutorial
* Bugs fixed
  * [0.0.3b] Fixed typo in error handling causing crashes
* Others:
  * Added diagonal movement
  * Restructured configuration code
  * Added config.py

####**v0.0.2** (2014-03-14):
* New features:
  * Keyboard events
  * Fog
  * Item enchanting
  * In-game help
  * Zombies
* Bugs fixed:
  * Minimap showing phantom halls
  * Various list index out of range errors in inventory and menus
  * Price of non-boosted items being zero
  * `nwse` being showed as the movement keys despite the configuration
  * Player stats remaining boosted after unequipping items
  * Objects being removed from the ground even if they were not picked up
  * Equipped items not modifying player's secondary attributes
  * Unequipped objects being destroyed
  * Total attack and defense stats stacking when switching items
  * [0.0.2b] Zombies attacking from a long distance
  * [0.0.2c] Non-standard keys (Arrows etc) being accepted in options
  * [0.0.2c] Fixed input errors with empty strings
  * [0.0.2c] Mob movement causing indexErrors
* Others:
  * Cleaned code
  * Increased feedback in less obvious functions
  * Going to the next floor now levels the player up as many times as possible (Not just one)
  * Added more items, races and classes
  * Attribute boost from items now showing in crawl screen and character sheet
  * Going to the next floor now requires user input
  * Items in the inventory can be destroyed
  * [0.0.2c] Other visual adjustments

####**v0.0.1** (2014-03-07):
  First versioned release.