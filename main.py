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

class Graph():

	def __init__(self, vertices):
		self.V = vertices
		self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
		self.parent = None

	# A utility function to print the constructed MST stored in parent[]
	def printMST(self, parent):
		print("Edge \tWeight")
		for i in range(1, self.V):
			print(parent[i], "-", i, "\t", self.graph[i][ parent[i] ])

	# A utility function to find the vertex with minimum distance value, from the set of vertices
	# not yet included in shortest path tree
	def minKey(self, key, mstSet):

		# Initilaize min value
		min = sys.maxsize

		for v in range(self.V):
			if key[v] < min and mstSet[v] == False:
				min = key[v]
				min_index = v

		return min_index

	# Function to construct and print MST for a graph represented using adjacency matrix representation
	def primMST(self):

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
		labels = {}
		for col in range(0, len(self.graph)):
			for row in range(0, len(self.graph[0])):
				if (row, col) not in labels or (col, row) not in labels:
					edge = (row, col)
					if self.graph[col][row] != 0:
						labels[edge] = self.graph[col][row]
		
		return labels
	
	# def assign_colors_to_MST(self):
	# 	colors = []
		
	# 	for col in range(0, len(self.graph)):
	# 		for row in range(0, len(self.graph[0])):
	# 			if self.parent[col] == row:
	# 				colors.append('r')
	# 			else:
	# 				colors.append('b')
	# 	print(len(colors))
	# 	print(colors)
	# 	return colors
	
	def draw_adjacency_matrix(self):
		"""
		- G is a netorkx graph
		- node_order (optional) is a list of nodes, where each node in G
			appears exactly once
		- partitions is a list of node lists, where each node in G appears
			in exactly one node list
		- colors is a list of strings indicating what color each
			partition should be
		If partitions is specified, the same number of colors needs to be
		specified.
		"""
		G = nx.from_numpy_matrix(np.array(self.graph))  
		pos = nx.spring_layout(G)
		nx.draw(G, pos, with_labels=True)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=self.make_label_dictionary())
	
	def assign_colors_to_MST(self, edges):
		colors = []
		for u,v in edges:
			if self.parent[v] == u:
				colors.append('r')
			else:
				colors.append('black')
		print("colors:", colors)
		return colors

	def draw_MST(self):
		"""
		- G is a netorkx graph
		- node_order (optional) is a list of nodes, where each node in G
			appears exactly once
		- partitions is a list of node lists, where each node in G appears
			in exactly one node list
		- colors is a list of strings indicating what color each
			partition should be
		If partitions is specified, the same number of colors needs to be
		specified.
		"""
		G = nx.from_numpy_matrix(np.array(self.graph))  
		edges = G.edges()
		print("edges:", edges)
		colors = self.assign_colors_to_MST(edges)
		pos = nx.spring_layout(G)
		nx.draw(G, pos, edges=edges, edge_color=colors, with_labels=True)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=self.make_label_dictionary())
