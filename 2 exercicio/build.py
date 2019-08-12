from shapely.geometry import Polygon
from shapely.geometry.point import Point
from shapely.ops import cascaded_union
import pygame
import sys
from pygame.locals import *
import math


def createPoints2Poly(side, center, radius):
    angle = 2*math.pi/side
    points = []
    for i in range(side):
        x = center[0] + radius*math.cos((i)*angle)
        y = center[1] + radius*math.sin((i)*angle)
        points.append((x, y))

    return tuple(points)


def create_city_points(centers, d) :
    Hx = []
    for center in centers :
        Hx.append(createPoints2Poly(6, center, d))

    return Hx

def create_city(centers, d) :
    Hx = []
    
    for center in centers :
        Hx.append(Polygon(createPoints2Poly(6, center, d)))

    return cascaded_union(Hx)

def create_base_stations_points(centers, radius) :
    Bx = []
    for center in centers :
        point = Point(center[0], center[1])
        circle = point.buffer(radius)
        Bx.append(circle)

    return Bx

def create_base_stations(centers, radius) :
    Bx = []

    for center in centers :
        point = Point(center[0], center[1])
        circle = point.buffer(radius)
        Bx.append(circle)

    return cascaded_union(Bx)


def run_pygame(city, base_stations) :    
    
    # inicia o pygame
    pygame.init()
    
    # inicia a janela
    windowSurface = pygame.display.set_mode((625, 625), 0, 32)
    # inicia as cores utilizadas
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (127, 127, 127)
    # inicia as fontes
    basicFont = pygame.font.SysFont(None, 48)
    # desenha o fundo branco
    windowSurface.fill(GREEN)
    # desenha um poligono verde na superficie
    
    for H in city :
        pygame.draw.polygon(windowSurface, GRAY, H)

    for B in base_stations :
        x,y = B.exterior.coords.xy
        points_base_stations = []
        for i in range(len(x)) :
            points_base_stations.append([x[i], y[i]])
            
        pygame.draw.polygon(windowSurface, BLUE, points_base_stations)    
                
    # desenha a janela na tela
    pygame.display.update()
    # roda o loop do jogo
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return