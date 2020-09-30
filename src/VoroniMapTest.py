# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 10:40:00 2020

@author: SGE
"""
"voroni model implementation for warbot"
"starting with scipy library implementation"

"import labrary for test and plot"

import numpy as np
import matplotlib.pyplot as pltlib
import random
from scipy.spatial import Voronoi, voronoi_plot_2d

random.seed(23)
X_range = 100;
Y_renge = 100;
size= 20;

#random.uniform(0, 1)
#Generate 5 random numbers between 10 and 30
random_X = random.sample(range(1, X_range), size)
random_Y = random.sample(range(1, Y_renge), size)
#print(randomlist)
#points = np.array([[0, 2], [1, 1], [1, 2],[3, 3], [5, 1], [1, 0]])
points = np.array([[0, 1], [1, 2], [2,3],[3, 2], [5, 1], [1, 0], [1, 1], [1, 2],[6, 3], [5, 1], [1, 0]])

#random_points = tuple(randomlist)
random_array_x = np.array(random_X)
random_array_y = np.array(random_Y)


random_array=np.vstack((random_array_x,random_array_y))
random_array=np.transpose(random_array)

vor = Voronoi(random_array,furthest_site=False,incremental=True)
"region indeces to check if it returns neibourghs"
regions = vor.regions 
"actual vertex of the close shapes generated"
vertex  = vor.vertices
"index"
ridge = vor.ridge_points
"index"
rridge = vor.ridge_vertices
rridge = vor.ridge_vertices

import matplotlib.pyplot as plt

fig = voronoi_plot_2d(vor)

plt.show()


selected_state = regions

# for i in range(len(selected_state),2):
#     print(i)
#     if -1 in selected_state[i-1]:
#         selected_state.remove(selected_state[i-1])


regions_array = np.array(regions)

# for i in range(len(regions_array),2):
#     for l in range(len(regions_array[i]))
#         if -1 in regions_array[i][j]:
#             regions_array.remove(regions_array[i])