#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 18:41:08 2019

@author: sturlafr
"""


class node():
    
    
    succsesors = []
    
    def __init__(self, position, heuristic, g_value = 0, parent = None):
        self.position = position
        self.parent = parent
        self.g_value = g_value
        self.heuristic = heuristic
        self.f_value = self.g_value + self.heuristic

    def get_parent(self):
        return self.parent
    

    def set_parent(self, parent):
        self.parent = parent

    
    def set_succsesor(self, nodes):
        self.succsesors.append(nodes)
        
        
    def get_succsesors(self):
        return self.succsesors
    
    
    def get_g_value(self):
        return self.g_value
    
    
    def get_position(self):
        return self.position
    
    
    def get_f_value(self):
        return self.f_value
    
    def attach_and_eval(self, parent, arc_cost, heuristic):
        
        self.set_parent(parent)
        
        self.g_value = parent.get_g_value() + arc_cost
        
        self.f_value = self.get_g_value() + heuristic
    
    
