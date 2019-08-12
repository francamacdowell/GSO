# -*- coding: utf-8 -*-

import random
import numpy as np
import math
import time
from shapely.geometry import Polygon
from shapely.geometry.point import Point
from shapely.ops import cascaded_union
from build import create_base_stations
from build import create_city
from build import create_base_stations_points
from build import create_city_points
from build import run_pygame


def calculate_fitness(worm, radius, city):
    circles = []
    for center in worm:
        point = Point(center[0], center[1])
        circles.append(point.buffer(radius))
    
    base_stations_polygon = cascaded_union(circles)
    intersection_area = base_stations_polygon.intersection(city).area
    return base_stations_polygon.intersection(city).area / city.area


def GSO(low_boundary, upper_boundary, dimension, population, iterations, radius, D, city, city_centers, show, luciferin_enhancement, ray, step):

    print("low boundary", low_boundary)
    print("upper boundary", upper_boundary)
    print("dimension", dimension)
    print("population", population)
    print("iterations", iterations)

    # Initialize the positions of search agents
    best_fitness = -999999
    Positions = []
    Luciferin = []

    for i in range(population):
        Positions.append(np.zeros(dimension))
        Luciferin.append(random.random())
    
    for i in range(population):
        Positions[i][:, 0] = np.random.uniform(
            0, 1, dimension[0]) * (upper_boundary - low_boundary) + low_boundary
        Positions[i][:, 1] = np.random.uniform(
            0, 1, dimension[0]) * (upper_boundary - low_boundary) + low_boundary
   
    Convergence_curve = np.zeros(iterations)
    
    # Loop counter
    print("GSO is optimizing")
    worm_pos = []
    # Main loop
    for l in range(iterations):

        for i in range(population):
            
            # Calculate objective function for each search agent
            fitness = calculate_fitness(Positions[i], radius, city)
            
            if fitness > best_fitness:
                best_fitness = fitness
                worm_pos = Positions[i].copy()

            # Lucinferin update phase:
            Luciferin[i] = (1 - random.random()) * Luciferin[i] + luciferin_enhancement * fitness

        # Movement Phase:
        for i in range(population):

            # Select neighbours with more luciferin inside the range
            neighbours = []
            for j in range(population):
                
                if i != j:
                    distance = np.linalg.norm(abs(Positions[j] - Positions[i]))
                    
                    if distance <= ray and Luciferin[j] >= Luciferin[i]:
                        neighbours.append(j)
            
            # Selecting random glowworm to follow
            best_worm = -7
            if len(neighbours) != 0:
                best_worm = random.choice(neighbours)
            
            # Update position phase
            d = np.linalg.norm(Positions[j] - Positions[i])

            Positions[i] += step * d

        if (l % 1 == 0):
            print(['At iteration ' + str(l+1) +
                   ' the best fitness is ' + str(best_fitness)])
            if show:
                run_pygame(create_city_points(city_centers, D),
                           create_base_stations_points(worm_pos, radius))

    if not show:
        run_pygame(create_city_points(city_centers, D),
                   create_base_stations_points(worm_pos, radius))
    print(best_fitness)
    return best_fitness
