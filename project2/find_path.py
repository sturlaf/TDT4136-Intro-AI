#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 22:25:07 2019

@author: sturlafr
"""

import a_star


def solve_task(task_num: int) -> None:
    """Solves the map problem"""
    
    task = a_star.A_star(task_num)
    
    task.A_star()
    

#Solve the four tasks
for i in range(1, 5):
    solve_task(i)
    
