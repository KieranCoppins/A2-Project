#Kieran Coppinss
#A* Pathfinding algorithms

#Import math libary to create infinite numbers
import math

#A function to take the data given from the AStar algorithm and format it to a path that the map can read
def reconstructPath(cameFrom, current):
	path = [current]
	while current in cameFrom:
		current = cameFrom[current]
		path.append(current)
	return path

#Calculate the difference between two coords
def dist(x, y):
	#Take one away from the other
	dif = x - y
	#IF the difference is negative, then the coordinates must've been the wrong way round
	if dif < 0:
		#Multiply by negative 1 to make it possitive
		dif = dif * -1
	#Return the value
	return dif

#Use pythagoras theorem to generate an estimate on the distance from two nodes
def heuristicEstimate(n, target):
	x = dist(n.x, target.x)
	y = dist(n.y, target.y)
	est = (x * x) + (y * y)
	return est

def generatePath(graph, source, target):
	#List of nodes that have already been "checked"
	close = []
	#List of nodes that need to be "checked"
	open = [source]

	#Dictionary used to save a node with its closest neighbouring node as a keyword
	cameFrom = {}
	#Dictionary used to store the "cost" or "distance" between each node
	gScore = {}
	#Default all values at infinity
	for v in graph.vertices:
		gScore[graph.vertices[v]] = math.inf

	#Make the distance of the source, from the source 0
	gScore[source] = 0

	#Dictionary used to store the heuristic estimate of each the distance from the node to the target
	fScore = {}
	#Default all values at infinity
	for v in graph.vertices:
		fScore[graph.vertices[v]] = math.inf

	#Generate the heristic estimate of the source node to the target node
	fScore[source] = heuristicEstimate(source, target)

	#While there are nodes in the open list
	while len(open) > 0:
		#Set current to default none
		current = None
		#For each vertex in the open list
		for v in open:
			#If current doesnt have a value or the fScore of the current vertex is more than the checked vertex
			if current == None or fScore[current] > fScore[v]:
				#Update the current vertex to equal the vertex in the loop
				current = v
		#If the current vertex is our target, we can exit and reconstruct the path
		if current == target:
			return reconstructPath(cameFrom, current)

		#Remove the vertex from the open list and add it to the closed list
		open.remove(current)
		close.append(current)

		#loop through each neighbour in the current vertex
		for neighbour in current.neighbours:
			#If a neighbour of the current vertex is in the closed list, continue through the loop
			if neighbour in close:
				continue
			#Add the tile type cost of each tile to the g score to generate the tentative g score of the current vertex
			#As each tile cost is equal to the value of 1 (as each wall neighbour doesn't have an edge)
			#Allows for the added functionality of various tile types with a variety of "movement costs"
			tentativeGScore = gScore[current] + 1

			#If the neighbour isnt in open
			if not neighbour in open:
				#Add it to open
				open.append(neighbour)
			#If the tenative g score is targer than the g score of the neighbour then go back to the start of the list
			elif tentativeGScore >= gScore[neighbour]:
				continue

			#add the current vertex to the came from dictionary using the neighbour vertex as a keyword
			cameFrom[neighbour] = current
			#update the g score of the neighbour vertex with the tentative g score
			gScore[neighbour] = tentativeGScore
			#update the f score to be equal to the g score plus the heueristic estimate of the neighbour to the target
			fScore[neighbour] = gScore[neighbour] + heuristicEstimate(neighbour, target)