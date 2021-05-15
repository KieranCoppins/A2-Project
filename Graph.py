#Kieran Coppins

#Assume that the graph is unweighted and all edges are bi-directional
class Graph():
	def __init__(self):
		#Create an empty dictionary on initialisation
		self.vertices = {}

	#A method to convert a tile map object to a graph
	def convertMapToGraph(self, map, movementType):
		#Get each tile in the map and create a vertex
		for keyword in map.tiles:
			tile = map.tiles[keyword]
			newVertex = Vertex(tile.x, tile.y)
			self.vertices[keyword] = newVertex

		#Check every tile and its neighbouring tile and create the corresponding edges to each vertex
		for keyword in map.tiles:			
			tile = map.tiles[keyword]
			if tile.type == 0:
				currentVertex = self.vertices[keyword]
				if tile.x > 0:
					otherKeyword = "{0},{1}".format(tile.x - 1, tile.y)
					if map.tiles[otherKeyword].type == 0:
						self.addEdge(currentVertex, self.vertices[otherKeyword])
				if tile.y > 0:					
					otherKeyword = "{0},{1}".format(tile.x, tile.y - 1)
					if map.tiles[otherKeyword].type == 0:
						self.addEdge(currentVertex, self.vertices[otherKeyword])
				if tile.x < map.width - 1:					
					otherKeyword = "{0},{1}".format(tile.x + 1, tile.y)
					if map.tiles[otherKeyword].type == 0:
						self.addEdge(currentVertex, self.vertices[otherKeyword])
				if tile.y < map.height - 1:
					otherKeyword = "{0},{1}".format(tile.x, tile.y + 1)
					if map.tiles[otherKeyword].type == 0:
						self.addEdge(currentVertex, self.vertices[otherKeyword])
				if movementType == "8-Way Movement":
					if tile.x > 0 and tile.y > 0:
						otherKeyword = "{0},{1}".format(tile.x - 1, tile.y - 1)
						if map.tiles[otherKeyword].type == 0:
							self.addEdge(currentVertex, self.vertices[otherKeyword])
					if tile.y > 0 and tile.x < map.width - 1:					
						otherKeyword = "{0},{1}".format(tile.x + 1, tile.y - 1)
						if map.tiles[otherKeyword].type == 0:
							self.addEdge(currentVertex, self.vertices[otherKeyword])
					if tile.x < map.width - 1 and tile.y < map.height - 1:					
						otherKeyword = "{0},{1}".format(tile.x + 1, tile.y + 1)
						if map.tiles[otherKeyword].type == 0:
							self.addEdge(currentVertex, self.vertices[otherKeyword])
					if tile.x > 0 and tile.y < map.height - 1:
						otherKeyword = "{0},{1}".format(tile.x - 1, tile.y + 1)
						if map.tiles[otherKeyword].type == 0:
							self.addEdge(currentVertex, self.vertices[otherKeyword])
	
	#A function to check if two vertices are adjacent to eachother
	def adjacent(self, vertexX, vertexY):
		#Checks every vertex in the list of neighbours in the current vertex
		for vertex in vertexX.neighbours:
			#If the other vertex exists in the neighbouring list then they are adjacent
			if vertex == vertexY:
				return True
			else:
				False

	#A method to add an edge between two verticies
	def addEdge(self, vertexX, vertexY):
		#Checks if the verticies are adjacent
		if not self.adjacent(vertexX, vertexY):
			#If they are not, add eachother to eachothers neighbouring list
			vertexX.neighbours.append(vertexY)
			vertexY.neighbours.append(vertexX)

	#A method to remove an edge between two verticies
	def removeEdge(self, vertexX, vertexY):
		#Checks if the two vertices are adjacent
		if self.adjacent(vertexX, vertexY):
			#If they are, remove eachother from eachothers neighbouring list
			vertexX.neighbours.remove(vertexY)
			vertexY.neighbours.remove(vertexX)

#A class to store data about each vertex in the graph
class Vertex():
	def __init__(self, x, y):
		#Stores the x and y coordinates as well as neighbouring vertices
		self.x = x
		self.y = y
		self.neighbours = []
