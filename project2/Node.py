#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 18:41:08 2019

@author: sturlafr
"""
from typing import List

class node():
    """
    A class for representing each position on the map, and the distance 
    from the initial position, and estimated distance to goal.
    
    Fields:
        position - [x, y], the position on the map
        heuristic - the estimated distance from this node to the goal
        g_value - the cost of getting from the initial position to this node
        f_value - heuristic + g_value
        parent (node) - the best parent of this node, can be updated during search
        succsesors - a list of succsesors of this node, or neigbours
    """
        
    #A list of the succsesors of this node
    succsesors = []
    
    def __init__(self, position: List[int], heuristic, g_value = 0, parent = None):
        self.position = position
        self.parent = parent
        self.g_value = g_value
        self.heuristic = heuristic
        self.f_value = self.g_value + self.heuristic

    def get_parent(self):
        return self.parent
    

    def set_parent(self, parent) -> None:
        self.parent = parent

    
    def set_succsesor(self, nodes) -> None:
        self.succsesors.append(nodes)
        
        
    def get_succsesors(self) -> List:
        return self.succsesors
    
    
    def get_g_value(self) -> int:
        """
        Returns the cost of getting from the initial position to the 
        position of this node.
        """
        
        return self.g_value
    
    
    def get_position(self) -> List[int]:
        """
        Returns the position of this node.
        
        Return:
            A list [x, y] representing a position on the map
        """
        
        return self.position
    
    
    def get_f_value(self) -> int:
        """
        Returns the estimated distance from the position 
        of this node to the goal.
        """
        
        return self.f_value
    
    def attach_and_eval(self, parent, arc_cost):
        """
        This function updates the parent if a better parent is found, 
        and updates the cost.
        
        Parameters:
            parent (node) - the new better parent-node
            arc_cost - the cost to get from the parent to this node
        """
        
        self.set_parent(parent)
        
        self.g_value = parent.get_g_value() + arc_cost
        
        self.f_value = self.get_g_value() + self.heuristic
    
    
