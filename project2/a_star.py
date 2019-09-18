#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 19:35:06 2019

@author: sturlafr
"""

from __pycache__ import Node
from MapSamfundet import Map_Obj 
import numpy as np


class a_star():
    
    
    
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
        
        node_0 = Node(start_pos, self.manhattan_distance(start_pos))
        
        Open += node_0
        
        while True:
            
            if Open == []:
                return "No solution"
            
            node = Open.pop()
            
            if self.manhattan_distance(node.position) == 0:
                return "Succses"
            
            Closed += node
            
            succsesors_pos = self.generate_succsesors(node.position)
            
            for succ_pos in succsesors_pos:
                                
                if not positions_expanded.has_key(succ_pos):
                    
                    succ = Node(succ_pos, self.manhattan_distance(succ_pos))
                    
                    positions_expanded[succ_pos] = succ
                    
                else:
                    succ = positions_expanded[succ_pos]
                
                node.set_succsesor(succ)
                
                arc_cost = self.map_obj.get_cell_value(succ_pos)
                
                if not Open.__contains__(succ) and not Closed.__contains__(succ):
                    
                    succ.attach_and_eval(node, arc_cost, self.manhattan_distance(succ_pos))
                    
                    Open += succ
                    
                    Open.sort(key = get_f_value)
                    
                else:
                    
                    succ.attach_and_eval(node, arc_cost, self.manhattan_distance(succ_pos))
                    
                    if Closed.__contains__(succ):
                    
                        self.propagate_path_improvements(succ)
                    
                    
                    
    def propagate_path_improvements(self, node):
        
        node_g_value = node.get_g_value()
        
        for kid in node.get_succsesors():
            
            arc_cost = self.map_obj.get_cell_value(kid.get_position())
            
            if node_g_value + arc_cost < kid.get_g_value():
                
                kid.attach_and_eval(node, arc_cost, self.manhattan_distance(kid.get_position()))
                
                self.propagate_path_improvements(kid)             
                
                    
    def generate_succsesors(self, position):
        
        succsesors_pos = []
        
        x_pos = position[0]
        y_pos = position[1]
        
        if self.map_obj.get_cell_value([x_pos, y_pos + 1]) != -1:
            succsesors_pos += [x_pos, y_pos + 1]
        
        if self.map_obj.get_cell_value([x_pos + 1, y_pos]) != -1:
            succsesors_pos += [x_pos + 1, y_pos]
            
        if self.map_obj.get_cell_value([x_pos, y_pos - 1]) != -1:
            succsesors_pos += [x_pos, y_pos - 1]
            
        if self.map_obj.get_cell_value([x_pos - 1, y_pos]) != -1:
            succsesors_pos += [x_pos - 1, y_pos]
    
        return succsesors_pos
    
    
    def sort_by_f_value(node):
        return node.get_f_value()
    