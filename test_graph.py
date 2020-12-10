# RANDOMLY GENERATE AN ADJACENCY MATRIX/LIST USING undirected_graph class
# random graph creator

import random
import numpy
import undirected_graph as UD

class Test_Graph:

    # runs all the Test_Graph methods to fully create a random graph
    def __init__(self, num_nodes, edge_probability):

        # same constructor arguments as attributes
        self.num_nodes = num_nodes # number nodes in graph
        self.edge_probability = edge_probability #probability that an edge exists

        # itialize nodes to None
        for i in range(num_nodes):
            exec("self.v_" + str(i) + " = None")

        # add the notes
        self.add_nodes()

        # create the vertices where an edge exists with some input probability
        self.create_vertices(self.edge_probability)

        # create an undirected graph object using the Vertex class in undriected_graph.py
        self.g = UD.Graph()

        # finish up the nodes
        self.finish_nodes()


    # this method addes nodes creating a Vertex object per node
    def add_nodes(self):  

        for i in range(self.num_nodes):
            exec("self.v_" + str(i) + " = UD.Vertex('V_" + str(i) + "')")


    # this method creates the edges between vertices by some edge probability
    # adds neighbors
    def create_vertices(self, edge_probability):

        for i in range(self.num_nodes):
            neighborhood = []

            for j in range(self.num_nodes):

                if i != j:
                    x = numpy.random.choice(2, 1, p=edge_probability)

                    if x:
                        exec("self.v_" + str(i) + ".add_neighbors([self.v_" + str(j) +  "])")

    # this method finishes verices by adding them to the graph object    
    def finish_nodes(self):
        vertices = []

        for i in range(self.num_nodes):
            exec("vertices.append(self.v_" + str(i) + ")")
        
        self.g.add_vertices(vertices)

    # get the random test graph object
    def get_test(self):
        return(self.g)

    # get the adj matrix representation of the graph
    # this is the method we want to access
    def adjMatrix(self):
        return (self.g.adjacency_matrix)