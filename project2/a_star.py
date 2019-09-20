#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 19:35:06 2019

@author: sturlafr
"""

import Node
from MapSamfundet import Map_Obj 
import numpy as np


class A_star():
    
    
    
    def __init__(self, task):
        
        self.map_obj = Map_Obj(task = task)
        
        
    def manhattan_distance(self, position):
        
        goal_pos = self.map_obj.get_end_goal_pos()
        
        x_axsis = np.abs(position[0] - goal_pos[0])
        
        y_axsis = np.abs(position[1] - goal_pos[1])
        
        return x_axsis + y_axsis
        

    def A_star(self):
        
        Open = []
        Closed = []
        positions_expanded = {}
        
        start_pos = self.map_obj.get_start_pos()
        
        node_0 = Node.node(start_pos, self.manhattan_distance(start_pos))
        
        Open.append(node_0)
        
        positions_expanded[tuple(node_0.get_position())] = node_0
        
        while not Open == []:

            
            node = Open.pop()
            
            if node.position == self.map_obj.get_goal_pos():
                self.reconstruct_path_on_map(node)
                return self.reconstruct_path(node)
            
            Closed.append(node)
            
            
            succsesors_pos = self.generate_succsesors(node.position)
            
            for succ_pos in succsesors_pos:
                                
                if not (tuple(succ_pos) in positions_expanded):
                    
                    succ = Node.node(succ_pos, self.manhattan_distance(succ_pos))
                    
                    positions_expanded[tuple(succ_pos)] = succ
                    
                else:
                    
                    succ = positions_expanded[tuple(succ_pos)]
                
                node.set_succsesor(succ)
                
                arc_cost = self.map_obj.get_cell_value(succ_pos)
                
                if not Open.__contains__(succ) and not Closed.__contains__(succ):
                    
                    succ.attach_and_eval(node, arc_cost, self.manhattan_distance(succ_pos))
                    
                    Open.append(succ)
                    
                    Open.sort(key = Node.node.get_f_value, reverse = True)
                    
                elif node.get_g_value() + arc_cost < succ.get_g_value():
                    
                    succ.attach_and_eval(node, arc_cost, self.manhattan_distance(succ_pos))
                    
                    if Closed.__contains__(succ):
                    
                        self.propagate_path_improvements(succ)
        
        
                     
        return 'No solution found'
                    
                    
    def propagate_path_improvements(self, node):
        
        node_g_value = node.get_g_value()
        
        for kid in node.get_succsesors():
            
            arc_cost = self.map_obj.get_cell_value(kid.get_position())
            
            if node_g_value + arc_cost < kid.get_g_value():
                
                kid.attach_and_eval(node, arc_cost, kid.heuristic)
                
                self.propagate_path_improvements(kid)             
                
                    
    def generate_succsesors(self, position):
        
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
    
    
    def reconstruct_path(self, node):
        
        path = []
        
        while node != None:
            
            path.append(node.get_position())
            
            node = node.get_parent()
        
        return path
    
    def reconstruct_path_on_map(self, node):
        
        while node.get_parent() != None:
            
            self.map_obj.replace_map_values(node.get_position(), 5, self.map_obj.get_goal_pos())
            
            
            node = node.get_parent()
       
        self.map_obj.show_map()
            


