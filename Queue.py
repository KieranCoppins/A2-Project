#Kieran Coppins

#A custom queue data structure
class Queue():
	def __init__(self):
		#Store information on the front and back pointer
		self.frontPointer = 0
		self.backPointer = 0
		#Create an empty dictionary
		self.dict = {}

	#A method to add an item to the queue
	def Enqueue(self, value):
		#Add the value to the queue using the current back pointer value as the keyword
		self.dict[self.backPointer] = value
		#Increment the back pointer by one
		self.backPointer += 1

	#A function to get the next item in the queue
	def Dequeue(self):
		#Try to get the value at the current front pointer and increment the front pointer and return the value
		try:
			value = self.dict[self.frontPointer]
			self.frontPointer += 1
			return value
		#IF not possible then there must not be another value
		except:
			None

	#A function to check if the queue is empty
	def isEmpty(self):
		#If the front and back pointer are equal, then the queue is empty
		if self.frontPointer == self.backPointer:
			return True
		else:
			return False