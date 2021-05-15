#Kieran Coppins
#Import modules
import tkinter as TK
import sys

#Create the root class for other screens to be children of
#Inherit tkinter's root class
class Main(TK.Tk):
	def __init__(self):
		TK.Tk.__init__(self)
		#Set the title of the root
		self.title("Pathfinding Invenstigation")
		#Create the mainframe for other frames to live inside of
		mainframe =	TK.Frame(self)
		mainframe.pack(fill="both", expand = True)
		mainframe.grid_rowconfigure(0, weight = 1)
		mainframe.grid_columnconfigure(0, weight = 1)

		#Dictionary containing each frame in the interface
		self.frames = {MainMenu : MainMenu(mainframe, self),
				 Simulation : Simulation(mainframe, self)}

		#Set the grid configuration for each frame in the dictionary
		for frame in self.frames:
			self.frames[frame].grid(row = 0, column = 0, sticky = "NSEW")

		self.ShowFrame(MainMenu)

	#A method to display the given frame
	def ShowFrame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()
		
#A class to hold the main menu frame
#Inherit tkinter's frame class
class MainMenu(TK.Frame):
	def __init__(self, parent, controller):
		TK.Frame.__init__(self, parent)

		#Create a title label
		self.titleLabel = TK.Label(self, text = "Main Menu")
		self.titleLabel.pack(fill="both", expand = True)

		#Create a Simulation button to navigate the user to the Simulation Frame
		self.simulationButton = TK.Button(self, text = "Simulation", command = lambda:controller.ShowFrame(Simulation))
		self.simulationButton.pack(fill = "both", expand = True)

		#Create an exit button to allow the user to exit the application
		self.ExitButton = TK.Button(self, text = "Exit", command = sys.exit)
		self.ExitButton.pack(fill="both", expand = True)

#A class to hold the simulation frame
#Inherit tkinter's frame class
class Simulation(TK.Frame):
	def __init__(self, parent, controller):
		TK.Frame.__init__(self, parent)

		#Create a Map Title
		self.mapTitle = TK.Label(self, text = "+---- Map ----+")
		self.mapTitle.grid(row = 0, column = 0)
		#Create the Map Display
		self.map = TK.Text(self, height = 30, width = 70)
		self.map.grid(row = 1, column = 0, rowspan = 10)
		self.map.config(state = "disabled")

		self.map.tag_configure("PathHighlight", background = "white", foreground = "cyan")


		#Create a Map Title
		self.consoleTitle = TK.Label(self, text = "+---- Console ----+")
		self.consoleTitle.grid(row = 11, column = 0, columnspan = 5)

		#Create Console to Update the user what the program is doing
		self.consoleTextBox = TK.Text(self, width = 110, height = 10)
		self.consoleTextBox.grid(row = 12, column = 0, columnspan = 5, rowspan = 2)
		self.consoleTextBox.config(state = "disabled")

		#Create Map Preferences Title
		self.mapPreferencesTitle = TK.Label(self, text = "+---- Map Preferences ----+")
		self.mapPreferencesTitle.grid(row = 0, column = 1, columnspan = 4)
		
		#Create Map width label and input
		self.mapWidthLbl = TK.Label(self, text = "Map Width:")
		self.mapWidthLbl.grid(row = 1, column = 1, columnspan = 2)
		self.mapWidthIput = TK.Entry(self, width = 15)
		self.mapWidthIput.grid(row = 1, column = 3, columnspan = 2)
		
		#Create Map height label and input
		self.mapHeightLbl = TK.Label(self, text = "Map Height:")
		self.mapHeightLbl.grid(row = 2, column = 1, columnspan = 2)
		self.mapHeightIput = TK.Entry(self, width = 15)
		self.mapHeightIput.grid(row = 2, column = 3, columnspan = 2)

		#Create Drop down menu for mapType
		#Create String Variable
		self.mapTypeOptions = ["Rooms With Corridors", "Cave System"]
		self.mapTypeVar = TK.StringVar()
		self.mapTypeVar.set(self.mapTypeOptions[0])
		#Create the drop down menu
		self.mapTypeOptionMenu = TK.OptionMenu(self, self.mapTypeVar, *self.mapTypeOptions)
		self.mapTypeOptionMenu.grid(row = 3, column = 1, columnspan = 4)
		
		#Create Pathfinding preferences Title
		self.pathPreferencesTitle = TK.Label(self, text = "+---- Pathfinding Preferences ----+")
		self.pathPreferencesTitle.grid(row = 4, column = 1, columnspan = 4)

		#Create Dropdown meny for Pathfinding algorithm
		#Create String Variable
		self.pathAlgorithms = ["A* Algorithm", "Dijkstra's Algorithm"]
		self.pathAlgorithm = TK.StringVar()
		self.pathAlgorithm.set(self.pathAlgorithms[0])
		#Create the drop down menu
		self.pathAlgorithmOM = TK.OptionMenu(self, self.pathAlgorithm, *self.pathAlgorithms)
		self.pathAlgorithmOM.grid(row = 5, column = 1, columnspan = 4)

		#Create Start X label and input
		self.startXLbl = TK.Label(self, text = "Start X:")
		self.startXLbl.grid(row = 6, column = 1)
		self.startXIput = TK.Entry(self, width = 3)
		self.startXIput.grid(row = 6, column = 2)

		#Create Start Y label and input
		self.startYLbl = TK.Label(self, text = "Start Y:")
		self.startYLbl.grid(row = 6, column = 3)
		self.startYIput = TK.Entry(self, width = 3)
		self.startYIput.grid(row = 6, column = 4)

		#Create End X label and input
		self.endXLbl = TK.Label(self, text = "End X:")
		self.endXLbl.grid(row = 7, column = 1)
		self.endXIput = TK.Entry(self, width = 3)
		self.endXIput.grid(row = 7, column = 2)

		#Create End Y label and input
		self.endYLbl = TK.Label(self, text = "End Y:")
		self.endYLbl.grid(row = 7, column = 3)
		self.endYIput = TK.Entry(self, width = 3)
		self.endYIput.grid(row = 7, column = 4)

		#Create Dropdown menu for 4-way or 8-way movement
		#Create String Variable
		self.movementOptions = ["4-Way Movement", "8-Way Movement"]
		self.movementOption = TK.StringVar()
		self.movementOption.set(self.movementOptions[0])
		#Create the drop down menu
		self.movementOM = TK.OptionMenu(self, self.movementOption, *self.movementOptions)
		self.movementOM.grid(row = 8, column = 1, columnspan = 4)

		#Create a Results Title
		self.resultsTitle = TK.Label(self, text = "+---- Results ----+")
		self.resultsTitle.grid(row = 9, column = 1, columnspan = 4)

		#Create Textbox to display results of the test
		self.results = TK.Text(self, width = 40, height = 10)
		self.results.grid(row = 10, column = 1, columnspan = 4)
		self.results.config(state = "disabled")

		#Create back button
		self.back = TK.Button(self, text = "Back", command = lambda:controller.ShowFrame(MainMenu))
		self.back.grid(row = 11, column = 1)

		#Create run simulation button
		self.runSim = TK.Button(self, text = "Run Simulation")
		self.runSim.grid(row = 11, column = 4)

		#Generate map button
		self.genMap = TK.Button(self, text = "Generate Map")
		self.genMap.grid(row = 11, column = 2, columnspan = 2)

class roomPopUP(TK.Toplevel):
	def __init__(self, parent):
		#print("Popping up")
		TK.Toplevel.__init__(self)
		self.title("Map Preferences")

		titleLabel = TK.Label(self, text = "Room Data")
		titleLabel.grid(row = 1, column = 1, columnspan = 4)

		#Create Map Room amount
		self.minRoomLbl = TK.Label(self, text = "Min Rooms:")
		self.minRoomLbl.grid(row = 2, column = 1)
		self.minRoomIput = TK.Entry(self, width = 3)
		self.minRoomIput.grid(row = 2, column = 2)

		self.maxRoomLbl = TK.Label(self, text = "Max Rooms:")
		self.maxRoomLbl.grid(row = 2, column = 3)
		self.maxRoomIput = TK.Entry(self, width = 3)
		self.maxRoomIput.grid(row = 2, column = 4)

		self.minRoomLblSize = TK.Label(self, text = "Min Room Size:")
		self.minRoomLblSize.grid(row = 3, column = 1)
		self.minRoomIputSize = TK.Entry(self, width = 3)
		self.minRoomIputSize.grid(row = 3, column = 2)

		self.maxRoomLblSize = TK.Label(self, text = "Max Room Size:")
		self.maxRoomLblSize.grid(row = 3, column = 3)
		self.maxRoomIputSize = TK.Entry(self, width = 3)
		self.maxRoomIputSize.grid(row = 3, column = 4)

		#Submit data button
		self.submitButton = TK.Button(self, text = "Submit")	
		self.submitButton.grid(row = 4, column = 1, columnspan = 4)

class cavePopUp(TK.Toplevel):
	def __init__(self, parent):
		#print("Popping up")
		TK.Toplevel.__init__(self)
		self.title("Map Preferences")

		titleLabel = TK.Label(self, text = "Room Data")
		titleLabel.grid(row = 1, column = 1, columnspan = 4)

		#Create Map Room amount
		self.floorPercLbl = TK.Label(self, text = "Percentage of Floors:")
		self.floorPercLbl.grid(row = 2, column = 1)
		self.floorPercIput = TK.Entry(self, width = 3)
		self.floorPercIput.grid(row = 2, column = 2)

		self.deathLimLbl = TK.Label(self, text = "Death Limit:")
		self.deathLimLbl.grid(row = 2, column = 3)
		self.deathLimIput = TK.Entry(self, width = 3)
		self.deathLimIput.grid(row = 2, column = 4)

		self.birthLimLbl = TK.Label(self, text = "Birth Limit:")
		self.birthLimLbl.grid(row = 3, column = 1)
		self.birthLimIput = TK.Entry(self, width = 3)
		self.birthLimIput.grid(row = 3, column = 2)

		self.smoothLbl = TK.Label(self, text = "Smooth Loops:")
		self.smoothLbl.grid(row = 3, column = 3)
		self.smoothIput = TK.Entry(self, width = 3)
		self.smoothIput.grid(row = 3, column = 4)

		#Submit data button
		self.submitButton = TK.Button(self, text = "Submit")	
		self.submitButton.grid(row = 4, column = 1, columnspan = 4)
