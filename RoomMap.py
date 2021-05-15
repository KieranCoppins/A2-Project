#Kieran Coppins
#Import libaries needed
import random
import tkinter as TK
#Create Fake Enum as Python doesn't support Enumerators
class TileTypesEnum():
	def __init__(self):
		self.floor = 0
		self.wall = 1

TileTypes = TileTypesEnum()
#Room Object for each room of this map type
class Room():
	def __init__(self, x, y, width, height):
		#The co-ordinates of the room
		self.x = x
		self.y = y

		#The size of the room
		self.width = width
		self.height = height

		#Calculate the center of the map
		self.centerX = self.x + (self.width // 2)
		self.centerY = self.y + (self.height // 2)

		#All tile co-ordinates inside the room
		self.tileCoords = []

		#Check if the room is connected via corridor; default at false
		self.connected = False

	def create(self, map):
		#Start Coordinates of the room
		startX = self.x
		startY = self.y

		#End Coordinates of the room
		endX = self.x + self.width
		endY = self.y + self.height

		#If the room comes of the map return false
		if startX >= map.width:
			return False
		if startY >= map.height:
			return False

		#If the room is "backwards" flip it
		if endX >= map.width:
			endX = map.width - 1
			self.width = endX - startX
		if endY >= map.height:
			 endY = map.height - 1
			 self.height = endY - startY

		#If the room is flipped the width and height will be negative so make them positive
		if self.width < 0:
			self.width = self.width * -1
		if self.height < 0:
			self.height = self.height * -1

		#If the new sizes are smaller the minium room size then return false
		if self.width < map.minRoomSize or self.height < map.minRoomSize:
			return False
		#Calculate the center of the map again incase anything changed
		self.centerX = self.x + (self.width // 2)
		self.centerY = self.y + (self.height // 2)

		#Loop throygh the start and the end of the room and make the walls floors
		for x in range(startX, endX):
			for y in range(startY, endY):
				keyword = "{0},{1}".format(x,y)
				self.tileCoords.append(keyword)

		return True

	#A method to check if a room intersects with another room
	def intersects(self, otherRoom):
		#Loop through every coordinate in the current room
		for roomCoord in self.tileCoords:
			#Loop through every coordinate in the room that is being compared to
			for otherCoord in otherRoom.tileCoords:
				#If the coords are the same
				if roomCoord == otherCoord:
					return True
		return False


#Create Map object and generate graph from map
class Map():
	def __init__(self, width, height, minRoom, maxRoom, minRoomSize, maxRoomSize):
		#Size of the map from entered parameters
		self.width = width
		self.height = height

		#All the tiles in the map from dictionary using coordinates as a key word and tile objects
		self.tiles = {}

		self.rooms = []

		self.maxRoomsSize = maxRoomSize
		self.minRoomSize = minRoomSize

		self.minRooms = minRoom
		self.maxRooms = maxRoom
	
	def generateMap(self):
		#Populate the map with the wall tile type
		self.populateMap(TileTypes.wall)
		#Place the rooms into the map with randomised sizes
		self.placeRooms(random.randint(self.minRooms, self.maxRooms))
		#Generate the corridors to connect the rooms together
		self.joinDoors()

	def populateMap(self, tileType):
		for x in range(self.width):
			for y in range(self.height):
				keyword = "{0},{1}".format(x, y)
				self.tiles[keyword] = Tile(x, y, tileType)

	def placeRooms(self, roomCount):
		#Make sure that all rooms are cleared incase a previous generation has been made
		self.rooms = []

		#Make sure that the amount of rooms passed as a parameter are generated
		for r in range(roomCount):
			#Get a random co-ordinate for the room to be created
			roomX = random.randint(1, self.width - 1)
			roomY = random.randint(1, self.height - 1)

			#Get the randomised room size
			roomWidth = random.randint(self.minRoomSize, self.maxRoomsSize)
			roomHeight = random.randint(self.minRoomSize, self.maxRoomsSize)

			#Create the room object
			newRoom = Room(roomX, roomY, roomWidth, roomHeight)
			#Create the room in terms of the map
			success = newRoom.create(self)
			failed = False
			#Check if the room was successfully created
			if success:
				#Check if the room intersects with another room
				for otherRoom in self.rooms:
					#Check if the room intersects
					if newRoom.intersects(otherRoom):
						#If it does, break out of the loop and make failed true
						failed = True
						break

				#If the room doesnt intersect
				if not failed:
					#Update tile data
					self.createRoom(newRoom)
					#Add the room to the list of rooms saved
					self.rooms.append(newRoom)

	#A method to change the tile data of the map to create the room
	def createRoom(self, room):
		#Loop through every coordinate in the room and make them a floor
		for coord in room.tileCoords:
			self.tiles[coord].type = TileTypes.floor

	#A method to join the rooms together
	def joinDoors(self):
		#Loop through each room to connect them
		for room in self.rooms:
			#Check if the room is not connected
			if not room.connected:
				#Loop through other rooms to connect them
				for otherRoom in self.rooms:
					#Check if that room is also not connected
					if not otherRoom.connected:
						#Get the center coordinates of each room
						roomCoord = "{0},{1}".format(room.centerX, room.centerY)
						otherRoomCoord = "{0},{1}".format(otherRoom.centerX, otherRoom.centerY)
						#Create a path for the corridor
						path = self.generateCorridor(roomCoord, otherRoomCoord)
						#Create the corridor based on path data
						self.createCorridor(path)
						#Set the rooms to be connected
						room.connected = True
						otherRoom.connected = True


	def generateCorridor(self, roomA, roomB):
		#Seperate the coordinates of each room
		roomAX, roomAY = roomA.split(",")
		roomBX, roomBY = roomB.split(",")

		#Convert the coordinates into integers for mathmatical operations
		roomAX = int(roomAX)
		roomAY = int(roomAY)
		roomBX = int(roomBX)
		roomBY = int(roomBY)

		#Create an empty list to contain the coordinates of the corridor
		currentPath = []

		#Depending on the room position depends how the corridor is generated, see diagram
		if roomBX <= roomAX and roomBY >= roomAY:
			for x in range(roomBX, roomAX + 1):
				currentPath.append("{0},{1}".format(x, roomAY))

			for y in range(roomAY, roomBY + 1):
				currentPath.append("{0},{1}".format(roomBX, y))

		if roomBX >= roomAX and roomBY >= roomAY:
			for x in range(roomAX, roomBX + 1):
				currentPath.append("{0},{1}".format(x, roomBY))

			for y in range(roomAY, roomBY + 1):
				currentPath.append("{0},{1}".format(roomAX, y))

		if roomBX >= roomAX and roomBY <= roomAY:
			for x in range(roomAX, roomBX + 1):
				currentPath.append("{0},{1}".format(x, roomAY))

			for y in range(roomBY, roomAY + 1):
				currentPath.append("{0},{1}".format(roomBX, y))

		if roomBX <= roomAX and roomBY <= roomAY:
			for x in range(roomBX, roomAX + 1):
				currentPath.append("{0},{1}".format(x, roomBY))

			for y in range(roomBY, roomAY + 1):
				currentPath.append("{0},{1}".format(roomAX, y))

		#Return the path for further use
		return currentPath

	def createCorridor(self, path):
		#Loop through every coordinate in the path
		for coord in path:
			#Seperate the coordinates to check if the coordinate is in map range
			coordX, coordY = coord.split(",")
			#Create the coordinates into integers for mathmatically operations
			coordX = int(coordX)
			coordY = int(coordY)

			if coordX > 0 and coordX < self.width and coordY > 0 and coordY < self.height:
				#Make the coordinate a floor
				self.tiles[coord].type = TileTypes.floor


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
			frame.map.insert(TK.END, "{0:^2}".format(y))
			for x in range(self.width):
				#Get the dictionary key word
				keyword = "{0},{1}".format(x, y)
				if keyword in highlightCoord:
					#Display the tile graphic with highlighted colour
					frame.map.insert(TK.END, self.tiles[keyword], "PathHighlight")
				else:
					#Display the tile graphic normally
					frame.map.insert(TK.END, self.tiles[keyword])
				#print(self.tiles[keyword], end = "")
			#Enter a new line character to display the new 
			frame.map.insert(TK.END, "\n")			
		frame.map.config(state = "disabled")




#Class to save data about each tile
class Tile():
	def __init__(self, x, y, type):
		#Save coordinate data of the tile
		self.x = x
		self.y = y

		#Save the type of tile (wall or floor)
		self.type = type

	#Set so when the tile class is printed the corresponding symbol is displayed
	def __str__(self):
		if self.type == 0:
			return "."
		else:
			return "#"