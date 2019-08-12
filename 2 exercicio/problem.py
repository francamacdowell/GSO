# -*- coding: utf-8 -*-
from GSO import GSO
import argparse
import sys
from shapely.geometry import Polygon
from shapely.geometry.point import Point
from shapely.ops import cascaded_union
from build import run_pygame
from build import create_base_stations
from build import create_points_2_poly
from build import create_city
import math


centers_1 = [(219, 287), (219, 393), (312, 234), (312, 234),
             (312, 340), (312, 448), (405, 287), (405, 393)]

centers_2 = [(127,124), (127,231), (127,340), (127,448),
            (220,178), (220,286), (220,394), (220,502),
            (312,124), (312,231), (312,340), (312,448),
            (406,178), (406,286), (406,394), (406,502),
            (499,124), (499,231), (499,340), (499,448)]


centers_3 = [(127,231), (127,340), (127,448), (220,178), (220,286),
            (220,394), (312,124), (312,231), (406,178), (406,286),
            (406,394), (499,231), (499,340), (499,448)]

K = [7, 3, 6]

D = [63, 63, 63]

R = [63, 170, 126]

centers = [centers_1, centers_2, centers_3]


def main():
    parser = argparse.ArgumentParser(
        description='GSO for optimizing basement problem')
    parser.add_argument('-p', '--population', default=100, type=int,
                        help='Population size')
    parser.add_argument('-it', '--iterations', type=int,
                        default=100,
                        help='Number of iterations')
    parser.add_argument('-i', '--input', type=int,
                        default=1,
                        help='Input instace of the problem')
    parser.add_argument('-l', '--luciferin', type=float,
                        default=0.2,
                        help='Luciferin Enhancement coeficient')
    parser.add_argument('-r', '--ray', type=int,
                        default=1000,
                        help='Ray range distance')
    parser.add_argument('--step', type=float,
                        default=0.5,
                        help='Step coeficient')
    parser.add_argument('-s', '--show', type=bool,
                        default=False,
                        help='Show bases station')

    args = parser.parse_args(sys.argv[1:])

    print("**************************************")
    print("*  GSO for optimizing base stations  *")
    print("**************************************")


    if args.input < 1 or args.input > 3 :
        print("The instance input doesn't exists")
        return 
    
    low_boundary = 0 + R[args.input-1]
    
    upper_boundary = 625 - R[args.input-1]
    
    city = create_city(centers[args.input-1], D[args.input-1])
    
    center_base_stations = GSO(low_boundary, upper_boundary, (K[args.input-1], 2), args.population, args.iterations, R[args.input-1], D[args.input-1], city, centers[args.input-1], args.show, args.luciferin, args.ray, args.step)

if __name__ == "__main__":
    main()