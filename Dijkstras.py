#Kieran Coppins
#Dijksta's pathfinding algorithm
import math

#A function to generate the path using Dijkstra's algoithm
def GenereatePath(graph, source, target):
	#Dictionary used to store the distance betwwen each node using the node as keyword
	dist = {}
	#Dictionary used to store the node of which came from the keyword node
	prev = {}

	#A list to store the next verticies that need to be visited
	unvisited = []

	#Default the distance to the source vertex as 0
	dist[source] = 0
	#Default the previous vertex to the source vertex as 0
	prev[source] = None

	#for each vertex in the graph
	for keyword in graph.vertices:
		v = graph.vertices[keyword]
		#As long as the vertex wasn't the source
		if v != source:
			#Default the distance to be infinity
			dist[v] = math.inf
			#Default the previous vertex as none
			prev[v] = None
		#Add the vertex to the unvisited list
		unvisited.append(v)

	#Whilst there are items in the unvisited list
	while len(unvisited) > 0:
		#Default U as none
		u = None

		#Loop through each vertex in unvisited
		for possibleU in unvisited:
			#If there is no U or the distance between the current U is less than the distance between the possible U
			if u == None or dist[possibleU] < dist[u]:
				#Make the possible U the new U
				u = possibleU

		#If U is the target vertex, then we have reached our destination
		if u == target:
			break

		#Remove U from unvisited
		unvisited.remove(u)

		#For each vertex in U's neighours
		for v in u.neighbours:
			#Calculate the distance to U including "tile cost" (all tiles cost 1)
			alt = dist[u] + 1
			#Even if that is smaller
			if alt < dist[v]:
				#update the distance to the neighbouring vertex to that value
				dist[v] = alt
				#update the prevous vertex of the neighbour V to the current vertex being visited U
				prev[v] = u
	

	#If target doesnt have a previous, something went wrong, just return
	if prev[target] == None:
		return

	#Create a list for the current path
	currentPath = []
	#Start with the target
	curr = target

	#While the current vertex is not none
	while curr != None:
		#Add the current vertex to the current path
		currentPath.append(curr)
		#Get the previous vertex to the current vertex
		curr = prev[curr]

	#Reverse the path list to make it the right order
	currentPath.reverse()
	#Return the path
	return currentPath