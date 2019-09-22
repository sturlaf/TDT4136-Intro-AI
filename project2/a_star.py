#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 19:35:06 2019

@author: sturlafr
"""

import Node
import MapSamfundet
import numpy as np
from typing import List


class A_star():
    """
    A class for solving the shorthest path problem for task 1, 2, 3, 4.
    
    Fields:
        map_object - a object representing the map with start and goal position
    """
    
    
    def __init__(self, task: int):
        """
        The task selected, initializes the map with the correct start and goal positions.
        
        Parameters:
            task - a number between 1-4, specifying the initial conditions of the map
        """
        
        self.map_obj = MapSamfundet.Map_Obj(task = task)
        
    
    
    def manhattan_distance(self, position: List[int]) -> int:
        """
        Computes the manhattan distance between a given position and the goal position.
        
        Parameters:
            position - [x, y] specyfying the place on the map
        """
        
        goal_pos = self.map_obj.get_end_goal_pos()
        
        x_axsis = np.abs(position[0] - goal_pos[0])
        
        y_axsis = np.abs(position[1] - goal_pos[1])
        
        return x_axsis + y_axsis
        


    def A_star(self):
        """
        The A* algorithm. Finds the shorthest path using 
        the manhattan distance as heuristic.
        """
        
        Open = []
        Closed = []
        
        #A dictionary to check if a position on the map already has been explored.
        positions_expanded = {}
        
        #The initial starting position.
        start_pos = self.map_obj.get_start_pos()
        
        #Generates a initial node, with no parents at the starting position.
        node_0 = Node.node(start_pos, self.manhattan_distance(start_pos))
        
        
        Open.append(node_0)
        
        positions_expanded[tuple(node_0.get_position())] = node_0
        
        while not Open == []:

            #Pick the node with the lowest estimated distance to goal
            node = Open.pop()
            
            #Check if this node is the goal_node
            if node.position == self.map_obj.get_goal_pos():
                
                #If goal is reached: Draw and list the shorthest path
                self.reconstruct_path_on_map(node)
                return self.reconstruct_path(node)
            
            Closed.append(node)
            
            #Generate the position of the neigbours of this node
            succsesors_pos = self.generate_succsesors(node.get_position())
            
            #For all the neigbours of this node, check if a better path is found
            for succ_pos in succsesors_pos:
                                
                #Check if this node has been generated before
                if not (tuple(succ_pos) in positions_expanded):
                    
                    #If the position has not been visited before, create a new node representing this position
                    succ = Node.node(succ_pos, self.manhattan_distance(succ_pos))
                    
                    #Add the new node to the dictonary of previosly expanded positions
                    positions_expanded[tuple(succ_pos)] = succ
                    
                else:
                    
                    #If the position already exist as a node, use this
                    succ = positions_expanded[tuple(succ_pos)]
                
                #Succ is now a child of node
                node.set_succsesor(succ)
                
                #Get the cost of moving from node to succ
                arc_cost = self.map_obj.get_cell_value(succ_pos)
                
                #If the node is not allready closed, and not yet in open, then add succ to open.
                if not (succ in Open or succ in Closed):
                    
                    #Set the parent and the estimated distance for succ.
                    succ.attach_and_eval(node, arc_cost)
                    
                    #Push succ onto open.
                    Open.append(succ)
                    
                    #Sort open by f_values. The last should the most promising, such that it is expanded first.
                    Open.sort(key = Node.node.get_f_value, reverse = True)
                    
                #If a better path is found to succ, update the graph
                elif node.get_g_value() + arc_cost < succ.get_g_value():
                    
                    succ.attach_and_eval(node, arc_cost)
                    
                    if succ in Closed:
                    
                        self.propagate_path_improvements(succ)
        
        
                     
        return 'No solution found'
                    
                    
    def propagate_path_improvements(self, node: Node.node) -> None:
        """ 
        If there is found a less costly path to node, this function pass this 
        path down to the succsesors of the node
        
        Parameters:
            node - the node where a better path is found
            
        """
        
        node_g_value = node.get_g_value()
        
        #Every succsesor could possibly need to update their distance from the initial node
        for kid in node.get_succsesors():
            
            arc_cost = self.map_obj.get_cell_value(kid.get_position())
            
            if node_g_value + arc_cost < kid.get_g_value():
                
                kid.attach_and_eval(node, arc_cost)
                
                self.propagate_path_improvements(kid)             
                
                    
    def generate_succsesors(self, position: List[int]) -> List[List[int]]:
        """
        This function generates all posible moves from the given position.
        If the value on the map is -1, then it represents a wall and should be avoided
        
        Parameters:
            position - the position from where to search from
            
        Return:
            A list with all possible succsesors
        """
        
        succsesors_pos = []
        
        x_pos = position[0]
        y_pos = position[1]
        
        if self.map_obj.get_cell_value([x_pos, y_pos + 1]) != -1:
            succsesors_pos.append([x_pos, y_pos + 1])
        
        if self.map_obj.get_cell_value([x_pos + 1, y_pos]) != -1:
            succsesors_pos.append([x_pos + 1, y_pos])
            
        if self.map_obj.get_cell_value([x_pos, y_pos - 1]) != -1:
            succsesors_pos.append([x_pos, y_pos - 1])
            
        if self.map_obj.get_cell_value([x_pos - 1, y_pos]) != -1:
            succsesors_pos.append([x_pos - 1, y_pos])
    
        return succsesors_pos
    
    
    def reconstruct_path(self, node: Node.node) -> List[int]:
        """
        A function that reconstructs the shorthest path found by the algorithm.
        
        Parameters:
            node - the last node in the path
            
        Return:
            A list with all the positions the path runs through
        """
        
        path = []
        
        #Find the parents to each node. The initial node is reached when the parent is None
        while node != None:
            
            path.append(node.get_position())
            
            node = node.get_parent()
        
        #The list is now backwars, with the last move first, so returns the reverse of this
        return path.reverse()
    
    
    def reconstruct_path_on_map(self, node: Node.node) -> None:
        """
        A function that draws a map of the shorthest path found by the algorithm
        
        Parameters:
            node - the last node of the path
        """
        
        #Find the parents to each node. The initial node is reached when the parent is None
        while node.get_parent() != None:
            
            self.map_obj.replace_map_values(node.get_position(), 5, self.map_obj.get_goal_pos())
            
            
            node = node.get_parent()
       
        #Use a function from MapSamfundet to display map
        self.map_obj.show_map()
            


