####################################################
# Names: Joseph Torii, Ghar Pautz, Cade Newell
# Professor: Zhang
# Class: CPSC 447
# Date: 17 April 2021
# Description: A Python program for Prim's Minimum Spanning Tree (MST) algorithm.
#      The program is for adjacency matrix representation of the graph
####################################################

import sys # Library for INT_MAX
import networkx as nx
from matplotlib import pyplot, patches
import numpy as np

def enter_int():
	"""Helper function for getting user input
	"""
	num = input()
	return int(num)

def get_num_vertices():
	"""Gets user input for number of vertices in graph
	"""
	print("Enter how many vertices: ")
	num = enter_int()
	return num

class Graph():
	"""Graph class that is used to assign vertices and edges.
	"""

	def __init__(self):
		"""Initializer for Graph.

		Parameters:
			V (num): number of vertices in graph
			graph (list of list of num): Adjacency matrix representation of graph
			parent (list of num): list of length V that stores what vertex each vertex 
				in the MST is connected to.
		"""
		self.V = get_num_vertices()
		self.graph = [[0 for column in range(self.V)] for row in range(self.V)]
		self.parent = None
	
	def input_edges(self):
		"""Inputs the edges into the graph using user input.
		"""
		print("How many edges (0 -", self.V * self.V - 1, "): ")
		num = enter_int()
		for _ in range(num):
			print("Start vertex: ")
			u = enter_int()
			print("End vertex: ")
			v = enter_int()
			print ("Weight: ")
			weight = enter_int()
			self.set_edge(u, v, weight)

	def set_edge(self, u, v, weight):
		"""Sets the edge in the graph given the input
		
		Parameters:
			u (num): The start vertex
			v (num): The end vertex
			weight (num): The weight of the edge
		"""
		self.graph[u][v] = weight
		self.graph[v][u] = weight

	# A utility function to print the constructed MST stored in parent[]
	def printMST(self, parent):
		"""Displays the edges and weights in MST to console
		
		Parameters:
			parent (list of num): list of length V that stores what vertex each vertex 
				in the MST is connected to.
		"""
		print("Edge \tWeight")
		for i in range(1, self.V):
			print(parent[i], "-", i, "\t", self.graph[i][ parent[i] ])

	def minKey(self, key, mstSet):
		"""A utility function to find the vertex with minimum distance value, from the set of vertices
			 not yet included in shortest path tree
		"""

		# Initilaize min value
		min = sys.maxsize

		for v in range(self.V):
			if key[v] < min and mstSet[v] == False:
				min = key[v]
				min_index = v

		return min_index

	# Function to construct and print MST for a graph represented using adjacency matrix representation
	def primMST(self):
		"""Prim's algorithm for finding minimum spanning tree
		"""

		# Key values used to pick minimum weight edge in cut
		key = [sys.maxsize] * self.V
		parent = [None] * self.V # Array to store constructed MST
		# Make key 0 so that this vertex is picked as first vertex
		key[0] = 0
		mstSet = [False] * self.V

		parent[0] = -1 # First node is always the root of

		for cout in range(self.V):

			# Pick the minimum distance vertex from the set of vertices not yet processed.
			# u is always equal to src in first iteration
			u = self.minKey(key, mstSet)

			# Put the minimum distance vertex in the shortest path tree
			mstSet[u] = True

			# Update dist value of the adjacent vertices of the picked vertex only if the current
			# distance is greater than new distance and the vertex in not in the shotest path tree
			for v in range(self.V):

				# graph[u][v] is non zero only for adjacent vertices of m mstSet[v] is false 
                # for vertices not yet included in MST
				# Update the key only if graph[u][v] is smaller than key[v]
				if self.graph[u][v] > 0 and mstSet[v] == False and key[v] > self.graph[u][v]:
						key[v] = self.graph[u][v]
						parent[v] = u
		
		self.parent = parent
		self.printMST(parent)

	def make_label_dictionary(self):
		"""Makes the dictionary used to assign labels to edges
		"""
		labels = {}
		for col in range(0, len(self.graph)):
			for row in range(0, len(self.graph[0])):
				if (row, col) not in labels or (col, row) not in labels:
					edge = (row, col)
					if self.graph[col][row] != 0:
						labels[edge] = self.graph[col][row]
		
		return labels
	
	def draw_network(self):
		"""Draws plain graph with labels, no colored edges
		"""
		G = nx.from_numpy_matrix(np.array(self.graph))  
		pos = nx.spring_layout(G)
		nx.draw(G, pos, with_labels=True)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=self.make_label_dictionary())
	
	def assign_colors_to_MST(self, edges):
		"""Assigns colors and weights to the edges in the graph. If an edge is part of the MST,
		then it's color is red and weight is thicker.
		"""
		colors = []
		weights = []
		for u,v in edges:
			if self.parent[v] == u:
				colors.append('r')
				weights.append(6)
			else:
				colors.append('black')
				weights.append(1)
		return colors, weights

	def prims_MST(self):
		"""Calculates minimum spanning tree using Prim's algorithm and stores parent in 
		Graph object. Then visualizes the minimum spanning tree.
		"""
		self.primMST()
		G = nx.from_numpy_matrix(np.array(self.graph))  
		edges = G.edges()
		# print("edges:", edges)
		colors, weights = self.assign_colors_to_MST(edges)
		pos = nx.spring_layout(G)
		nx.draw(G, pos, edges=edges, edge_color=colors, width=weights, with_labels=True)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=self.make_label_dictionary())