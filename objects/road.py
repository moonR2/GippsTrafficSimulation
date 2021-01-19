import networkx as nx
from math import atan2
from numpy import rad2deg


class road():
    def __init__(self, edge, nodes, ith):
        self.nodes = nodes
        self.edge = edge
        self.ith = ith
        self.start = nodes[edge[0]]
        self.end = nodes[edge[1]]
        self.angle = self.get_angle()
        self.plat = []

    def get_angle(self):
        delta_x = self.end[0] - self.start[0]
        delta_y = self.end[1] - self.start[1]
        theta = atan2(delta_y, delta_x)
        return rad2deg(theta)
    
# Class storing all the roads in the graph
class street():
    def __init__(self):
        self.streets = []

    def add_street(self,road):
        self.streets.append(road)
    
