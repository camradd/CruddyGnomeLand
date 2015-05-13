# Cruddy Gnome Land! ® 2015

Welcome to Cruddy Gnome Land! A customizable, tile-based, biologically-inspired, ERL (Evolutionary Reinforcement Learning), world simulation library written in Python.

Created by Cameron Rudd and Avinoam Henig.

## Setup Dependancies

### Python 2.7

This library requires Python 2.7.

### CONX

This library requires Conx (it's included in the repo).

### Pyglet

This library requires Pyglet.

	pip install pyglet
	pip install --upgrade https://bitbucket.org/pyglet/pyglet/get/tip.zip

### MongoDB and MongoEngine

The database saving feature requires MongoDB and MongoEngine. If you do not install MongoEngnine the library will fallback gracefully and simply not save to the database.


MongoDB can either be installed with Homebrew: `brew install mongodb`, or through their downloads page: <https://www.mongodb.org/downloads>.

After installation run the following terminal commands to setup the data directory:

	sudo mkdir -p /data/db
	sudo chmod 777 /data/db

To install MongoEngine run the following:

	pip install mongoengine
	pip install pymongo==2.8

Start MongoDB with the following terminal command: `mongod`.

## Running Cruddy Gnome Land

### Managing Universes (Simulation Runs) Through the CLI

To open the Cruddy Gnome Land CLI (Command Line Interface), change to the source directory and:

	python -i run.py

The CLI should greet you and give you a list of commands.

The `run` function takes in a name (string) and an option settings dictionary. This creates a new universe, which is simply a simulation run, with the provided settings (any non-specified settings will take on default values). If you have MongoEngine installed it will automatically save data about this run in a MongoDB database named `cruddy_gnome_land`.

The `enter` function allows you to enter an interactive python shell for each universe. You can have multiple universes running at the same time, as they each run in a seperate python process. Inside a universe's interactive python shell the variable `u` refers to the universe, and `w` is a shorthand for `u.world`. You can call `u.show()` to show a visulization of the universe, and `u.hide()` to hide it. You can change the speed by calling `u.setStepTime(t)`, where `t` is the wait between steps in seconds (defaults to 0.1; larger numbers are slower). If you set the step time to 0 it will run the fastest, but the interactive shell will become much less responsive (however it will respond, just give it 10-20 seconds; this is something we would like to improve in the future and have an idea of how to do it). Typing `exit` will exit the universe's interactive shell.

Exiting the entire CLI (`Ctrl-D`) will stop all running universe processes. In the future you will be able to resume running universes from the database, but this capability has not been fully implemented yet.

### Universe Settings

Here are the possible settings you can pass into the `run` function:

	{
		'world': {
			'width': 75,				# Width of the world (in tiles)
			'height': 45,				# Height of the world (in tiles)
			# Probability of TileObject appearing in a tile during initialization.
			#						plain, Food, Tree, Creature
			'tileObjectProbs': [97,    0.8,  1.7,  0.5]
			'creature': {
				'mutationRate': 0.3, # Probability of mutating single weight
										 # in creature during mutation.
				'minMutation': -0.5, # Minimum weight muation.
				'maxMutation': 0.5,  # Maximum weight mutation.
				'orgy': True         # Allow more than 2 parents.
			}
		}
	}

## Code Explanation

Each Universe contains a single World, which is made up of many tiles (the default size is 75x45). Each Tile can have multiple TileObjects (plain, Tree, Food, Creature, or your own custom classes). The TileObject's can coexist in a tile according to certain rules that are defined in each TileObject subclass. Only the Universe, World, and Creature classes are currently stored in the database.

### TileObject

On each timestep each TileObject subclass's `step` function is called. The order in which each tile is stepped is determined randomly for each time step. After all the TileObjects in the World have been stepped, `stepFinished` is called on each of them.