#Kieran Coppins

import random
import Queue
import tkinter as TK

#An enum class to use keywords to correspond to integers (used for tile types)
class TileTypesEnum():
	def __init__(self):
		self.floor = 0
		self.wall = 1

#Initialise the enum globally
TileTypes = TileTypesEnum()

#A class for map generation
class Map():
	def __init__(self, width, height, deathLimit, birthLimit, percentAreWalls, smoothLoops):
		#Save each variable in the class
		self.width = width
		self.height = height
		self.deathLimit = deathLimit
		self.birthLimit = birthLimit
		self.percentAreWalls = percentAreWalls
		self.smoothLoops = smoothLoops

		#Create an empty dictionary 
		self.tiles = {}


	#A method to initialise map generation
	def generateMap(self):
		#First Populate the map
		self.populateMap()
		#Smooth the map using the cellular automata rule set
		for i in range(self.smoothLoops):
			self.tiles = self.smoothMap(self.tiles)
		#Remove any isolated caves to ensure all sections of the map can be accessed
		self.removeIsolatedCaves()

	#A method to populate the map randomly depending on the percentage entered
	def populateMap(self):
		#loop through every row and column of the tile map
		for x in range(self.width):
			for y in range(self.height):
				keyword = "{0},{1}".format(x, y)
				#Generate a random number between 0 and 99
				chance = random.randint(0, 100)

				#If the random number is less than the percentage are walls, then create a floor tile in that coordinate
				if chance < self.percentAreWalls:
					self.tiles[keyword] = Tile(x, y, TileTypes.floor)
				else:
					#Otherwise create a wall
					self.tiles[keyword] = Tile(x, y, TileTypes.wall)

	#A function for running the tile map through a smoothing cycle
	def smoothMap(self, oldmap):
		#Create a new dictionary to store the new smoothed map
		newMap = {}
		#For each tile in the map
		for x in range(self.width):
			for y in range(self.height):
				keyword = "{0},{1}".format(x, y)
				#Get the amount of neighbouring floor tiles
				nbs = self.countFloorNeighbours(oldmap[keyword])
				#If the tile is around the border, force a wall tile
				if (x == 0 or y == 0 or x == self.width - 1 or y == self.height - 1):
					newMap[keyword] = Tile(x, y, TileTypes.wall)

				#Otherwise if the tile is a floor
				elif (oldmap[keyword].type == TileTypes.floor):
					#If the number of neighbouring floor tiles is less than the death limit
					if (nbs < self.deathLimit):
						#Make it a wall
						newMap[keyword] = Tile(x, y, TileTypes.wall)
					else:
						#Otherwise make it a floor
						newMap[keyword] = Tile(x, y, TileTypes.floor)
				else:
					#Otherwise if the tile is a wall and the birth limit is more than the neighbouring floor tile count
					if (nbs > self.birthLimit):
						#Make it a floor
						newMap[keyword] = Tile(x, y, TileTypes.floor)
					else:
						#Otherwise make it a wall
						newMap[keyword] = Tile(x, y, TileTypes.wall)
		#Return the new smoothed map
		return newMap


	#A function to count the amount of neighbouring tiles that are floors
	def countFloorNeighbours(self, tile):
		#Create a counter to start at 0
		count = 0
		#For each tile around the current tile
		for i in range(-1, 2):
			for j in range(-1, 2):
				x = tile.x + i
				y = tile.y + j
				keyword = "{0},{1}".format(x, y)
				#Check to make sure that the tile isnt the current tile and that the tile is in range
				if (i == 0 and j == 0):
					continue
				elif (x < 0 or x >= self.width or y < 0 or y >= self.height):
					continue
				#If the tile is a floor then increment the counter by 1
				elif (self.tiles[keyword].type == TileTypes.floor):
					count += 1
		#Return the counter
		return count

	#A method to display the map
	def displayMap(self, frame, path = []):
		highlightCoord = []
		for vertex in path:
			highlightX = vertex.x
			highlightY = vertex.y			
			keyword = "{0},{1}".format(highlightX, highlightY)
			highlightCoord.append(keyword)
		#Display the map to the map text box
		frame.map.config(state = "normal")
		frame.map.delete(0.0, TK.END)
		#Loop through the height and width of the map
		for y in range(self.height):
			for x in range(self.width):
				#frame.map.insert(TK.END, "{0:^2}".format(y))
				keyword = "{0},{1}".format(x, y)
				if keyword in highlightCoord:
					frame.map.insert(TK.END, self.tiles[keyword], "PathHighlight")
				else:
					frame.map.insert(TK.END, self.tiles[keyword])
			frame.map.insert(TK.END, "\n")
		frame.map.config(state = "disabled")

	def removeIsolatedCaves(self):
		#Create a list that will turn into a 2D array to store each cave
		caves = []
		#Loop through each tile in the map
		for tileKey in self.tiles:
			#If the map is of a floor tile type
			if self.tiles[tileKey].type == TileTypes.floor:
				#Create an empty list for the cave
				caveList = []
				#Flood fill the current tile
				caveList = floodFillIteration(self, tileKey)
				#Add the new cave to the list of caves
				caves.append(caveList)

		#Create an empty array for the biggest cave
		biggestCave = []
		#Loop through every cave in the list of caves
		for cave in caves:
			#If the currently checked cave is bigger than the currently selected biggest cave
			if len(cave) > len(biggestCave):
				#Reassign the biggest cave
				biggestCave = cave

		#print(biggestCave)
		#print(len(caves))
		#print(caves[0])
		#Remove the biggest cave from the list of caves
		caves.remove(biggestCave)
		#print(len(caves))
		#Go through the rest of the caves
		for caveList in caves:
			#Loop through every tile in that cave
			for tile in caveList:
				#Change their tile types to walls
				tile.type = TileTypes.wall

#A class to store information about each tile
class Tile():
	def __init__(self, x, y, type):
		#Stores the coordinates, type and if the tile has been checked in the flood fill algorithm
		self.x = x
		self.y = y
		self.type = type
		self.checked = False

	#Set it so when the object is displayed through "print" display the right symbol based on tile type
	def __str__(self):
		if self.type == TileTypes.floor:
			return "."
		else:
			return "#"

#I tried to use a recursion algorithm for flood fill, however I discovered that it went too deep into recursion and returned a memory error
#I then fell back on using the bellow iteration algorithm using a queue. However, the below algorithm would've worked otherwise.
#def floodFillRecursion(map, tileKey, tileList):
#	try:
#		tile = map.tiles[tileKey]
#	except:
#		return tileList
#	if tile.type == TileTypes.wall:
#		return tileList
#	if tile.checked:
#		return tileList
#	if tile in tileList:
#		return tileList
#	tileList.append(tile)
#	tile.checked = True
#	floodFill(map,"{0},{1}".format(tile.x, tile.y - 1), tileList)
#	floodFill(map,"{0},{1}".format(tile.x, tile.y + 1), tileList)
#	floodFill(map,"{0},{1}".format(tile.x - 1, tile.y), tileList)
#	floodFill(map,"{0},{1}".format(tile.x + 1, tile.y), tileList)
#	return tileList

def floodFillIteration(map, tileKey):
	#Test if the keyword entered is a legitamate tile
	try:
		tile = map.tiles[tileKey]
	except:
		return []
	#Check if the tile has already been checked
	if tile.checked:
		return []
	#Check if the tile is a wall as we dont want to be flood filling walls
	if tile.type == TileTypes.wall:
		return []

	#Create an empty Queue
	Q = Queue.Queue()
	#Make the current tile checked
	tile.checked = True
	#Add the current tile to the queue
	Q.Enqueue(tile)
	#Create an empty list to store all the tiles in the current flood fill cave
	cave = []
	#Loop through untill the Queue is exhausted
	while Q.isEmpty() == False:
		#Get the next item from the queue
		N = Q.Dequeue()
		#Check the west, east, north sides of the tile
		tile = checkTile(map, N.x - 1, N.y)
		#Check if the tile didnt return a none
		if tile != None:
			#This means its a legitamate tile, therefore add it to the queue
			Q.Enqueue(tile)
		tile = checkTile(map, N.x + 1, N.y)
		if tile != None:
			Q.Enqueue(tile)
		tile = checkTile(map, N.x, N.y + 1)
		if tile != None:
			Q.Enqueue(tile)
		tile = checkTile(map, N.x, N.y - 1)
		if tile != None:
			Q.Enqueue(tile)
		#Add the tile to the list of tiles for the current cave
		cave.append(N)
	#Return the current cave list
	return cave


def checkTile(map, x, y):
	#Get the keyword for the dictionary for the tile being accessed
	keyword = "{0},{1}".format(x, y)
	#print(keyword)
	#Check if its an existing tile
	try:
		tile = map.tiles[keyword]
	except:
		return None
	#Check if the tile is of a floor type and hasnt already been checked
	if tile.type == TileTypes.floor and tile.checked == False:
			#Check the tile and return it
			tile.checked = True
			return tile
	#If not then return None
	return None
