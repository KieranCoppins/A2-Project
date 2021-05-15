#Kieran Coppins
#Import libaries needed
import Interface as UI
import RoomMap
import CaveGeneration
import tkinter as TK
import Graph
import Dijkstras
import AStar

#Event called when generate map is clicked
def inputMapValues(frame):
	#Get what map is chosen in the drop down menu
	mapType = frame.mapTypeVar.get()
	#If the map is rooms with corridors
	if mapType == frame.mapTypeOptions[0]:
		#Generate the right popUp Menu
		popUp = UI.roomPopUP(Interface)
		#Configure the submit button of the popup menu to a local method
		popUp.submitButton.config(command = lambda:generateRoomMap(frame, popUp))

	else:
		#Otherwise it is a cave map type therefore genereate the cave pop up
		popUp = UI.cavePopUp(Interface)		
		popUp.submitButton.config(command = lambda:generateCaveMap(frame, popUp))


#A method for generating a cave map type
def generateCaveMap(frame, popUp):
	#Output to the interface console text box
	frame.consoleTextBox.config(state = "normal")
	frame.consoleTextBox.insert(TK.END, "----------Creating New Map----------\n")
	frame.consoleTextBox.insert(TK.END, "Getting map parameters... \n")
	#Get the global variable
	global map
	#Get all the values entered
	deathLimit = popUp.deathLimIput.get()
	birthLimit = popUp.birthLimIput.get()
	smoothLoop = popUp.smoothIput.get()
	percFloors = popUp.floorPercIput.get()
	width = frame.mapWidthIput.get()
	height = frame.mapHeightIput.get()
	#Validate values
	try:
		width = int(width)
		height = int(height)
		deathLimit = int(deathLimit)
		birthLimit = int(birthLimit)
		smoothLoop = int(smoothLoop)
		percFloors = int(percFloors)
	except:		
		frame.consoleTextBox.insert(TK.END, "[ERROR] Invalid Map Parameters! \n")
		return

	if width > 67 or height > 29:
		frame.consoleTextBox.insert(TK.END, "[ERROR] Map Size Too Big (Max Width: 67, Max Height 29)! \n")
		return
	if width <= 0 or height <= 0:		
		frame.consoleTextBox.insert(TK.END, "[ERROR] Map Size Must have a size of at least 1! \n")
		return

	#Update the console to tell the user that the map is being generated
	frame.consoleTextBox.insert(TK.END, "Generating map with values ({0}, {1}, {2}, {3}, {4}, {5})...\n".format(width, height, deathLimit, birthLimit, percFloors, smoothLoop))
	#Initialise the map object
	map = CaveGeneration.Map(int(width), int(height), int(deathLimit), int(birthLimit), int(percFloors), int(smoothLoop))
	#Run the generate map method in the map object
	map.generateMap()
	#Display the map
	frame.consoleTextBox.insert(TK.END, "Displaying map...\n")
	map.displayMap(frame)	
	#Destroy the pop up after everything is completed
	popUp.destroy()	
	#Update Console
	frame.consoleTextBox.insert(TK.END, "Done!\n")
	frame.consoleTextBox.config(state = "disabled")
	

def generateRoomMap(frame, popUp):
	#Update the console so the user knows whats happening
	frame.consoleTextBox.config(state = "normal")
	frame.consoleTextBox.insert(TK.END, "----------Creating New Map----------\n")
	frame.consoleTextBox.insert(TK.END, "Getting map parameters... \n")
	#We're using the map global variable here
	global map
	#Get all the values entered in the pop up window
	minRooms = popUp.minRoomIput.get()
	maxRooms = popUp.maxRoomIput.get()
	minRoomSize = popUp.minRoomIputSize.get()
	maxRoomSize = popUp.maxRoomIputSize.get()
	width = frame.mapWidthIput.get()
	height = frame.mapHeightIput.get()
	#Validate all values
	try:
		minRooms = int(minRooms)
		maxRooms = int(maxRooms)
		minRoomSize = int(minRoomSize)
		maxRoomSize = int(maxRoomSize)
		height = int(height)
		width = int(width)
	except:		
		frame.consoleTextBox.insert(TK.END, "[ERROR] Invalid Map Parameters! \n")
		return

	if width > 67 or height > 29:
		frame.consoleTextBox.insert(TK.END, "[ERROR] Map Size Too Big (Max Width: 67, Max Height 29)! \n")
		return
	if width <= 0 or height <= 0:		
		frame.consoleTextBox.insert(TK.END, "[ERROR] Map Size Must have a size of at least 1! \n")
		return


	#Update the console
	frame.consoleTextBox.insert(TK.END, "Generating map with values ({0}, {1}, {2}, {3}, {4}, {5})...\n".format(width, height, minRooms, maxRooms, minRoomSize, maxRoomSize))
	#Create an instance of the map object and save it in the global map variable
	map = RoomMap.Map(int(width), int(height), int(minRooms), int(maxRooms), int(minRoomSize), int(maxRoomSize))
	#Start the map generation method
	map.generateMap()
	#Update the console
	frame.consoleTextBox.insert(TK.END, "Displaying map...\n")
	#Display the map on the UI
	map.displayMap(frame)
	#Close the popup window
	popUp.destroy()	
	#Update Console
	frame.consoleTextBox.insert(TK.END, "Done!\n")
	frame.consoleTextBox.config(state = "disabled")


def runSim(frame):
	#Update the console
	frame.consoleTextBox.config(state = "normal")
	frame.results.config(state = "normal")
	frame.consoleTextBox.insert(TK.END, "----------Running Simulation----------\n")
	#Get the global variable
	global map
	#Make sure a map exists
	if map == None:
		#print("No map generated")
		frame.consoleTextBox.insert(TK.END, "No map generated, generate a map before applying a pathfinding algorithm!\n")
		return	
	#Get the movement type
	movementType = frame.movementOption.get()
	frame.consoleTextBox.insert(TK.END, "Generating Graph from Map....\n")
	#Generate a graph object
	graph = Graph.Graph()
	#Run the tile map to graph conversion function
	graph.convertMapToGraph(map, movementType)
	#Validate coordinates entered
	try:
		sourceX = int(frame.startXIput.get())
		sourceY = int(frame.startYIput.get())
		targetX = int(frame.endXIput.get())
		targetY = int(frame.endYIput.get())		
		source = graph.vertices["{0},{1}".format(sourceX, sourceY)]
		target = graph.vertices["{0},{1}".format(targetX, targetY)]
	except:
		#print("Invalid Coordinates")		
		frame.consoleTextBox.insert(TK.END, "Coordinates entered are invalid, please check again\n")
		return
	#Get the chosen algorithm
	pathfindAlgorithm = frame.pathAlgorithm.get()
	frame.consoleTextBox.insert(TK.END, "Pathfinding from ({0}, {1}) to ({2},{3})...\n".format(sourceX, sourceY, targetX, targetY))
	#Run the corresponding path
	if pathfindAlgorithm == frame.pathAlgorithms[1]:
		path = Dijkstras.GenereatePath(graph, source, target)		
		frame.consoleTextBox.insert(TK.END, "Updating display...\n")
		map.displayMap(frame, path)
	else:
		path = AStar.generatePath(graph, source, target)
		map.displayMap(frame, path)

	#Update Results
	frame.results.insert(TK.END, "----------{0:^20}----------\n".format(pathfindAlgorithm))
	frame.results.insert(TK.END, "Path Distance = {0}\n".format(len(path)))
	#Update Console
	frame.consoleTextBox.insert(TK.END, "Done!\n")
	frame.consoleTextBox.config(state = "disabled")
	frame.results.config(state = "disabled")

#Create an instance of the Main object within the UI file
Interface = UI.Main()
#Configure a button to call a local method
Interface.frames[UI.Simulation].genMap.config(command = lambda:inputMapValues(Interface.frames[UI.Simulation]))
Interface.frames[UI.Simulation].runSim.config(command = lambda:runSim(Interface.frames[UI.Simulation]))
#Define a global variable which will be used later
map = None

#Keep the UI in loop
Interface.mainloop()