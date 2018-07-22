#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Imports decimal module to assure precision
from decimal import *


# Sets the trap just to assure consistency in operations
getcontext().traps[FloatOperation] = True


# Constants
CONSTANT_X = 'ConstantX'  # Key for the constant X's in lines dict
CONSTANT_Y = 'ConstantY'  # Key for the constant Y's in lines dict


# Variables
n = 100      # N given in the problem
points = []  # Holds the generated points
lines = {}   # Holds lines


def Sn_generator():
    '''Sn generator as described in the problem'''

    Sn = Decimal(290797)

    while True:
        Sn = (Sn ** 2) % Decimal(50515093)
        yield Sn


def Tn_generator():
    '''Tn generator as described in the problem'''

    for Sn in Sn_generator():
        yield (Sn % Decimal(2000)) - Decimal(1000)


def get_coefficients(p1, p2):
    '''Given a pair of points, returns the angular and linear coefficients'''

    dx = p2[0] - p1[0]  # Delta X of the points
    dy = p2[1] - p1[1]  # Delta Y of the points

    # If dx is 0, it is a vertical line
    if dx == 0:
        return (CONSTANT_X, p1[0])
    # If dy is 0, it is a horizontal line
    elif dy == 0:
        return (CONSTANT_Y, p1[1])

    a = dy / dx             # Angular coefficient
    b = -a * p1[0] + p1[1]  # Linear coefficient

    return (a, b)


def get_equation(a, b):
    '''Given the coefficients, returns the line equation for pretty printing'''

    if a == CONSTANT_X:
        return 'X = {:0.6f}'.format(b)
    elif a == CONSTANT_Y:
        return 'Y = {:0.6f}'.format(b)

    signal = '-' if b < 0 else '+'

    return 'Y = {:0.6f}X {} {:0.6f}'.format(a, signal, abs(b))


def M():
    '''Returns the number of unique lines'''

    return sum(map(len, lines.values()))


def S():
    '''Returns the sum of all intersection counts'''

    m = M()                              # All lines count
    cx = len(lines.get(CONSTANT_X, []))  # Constant X count
    cy = len(lines.get(CONSTANT_Y, []))  # Constant Y count
    nc = m - cx - cy                     # Non-constant lines count

    s = nc * (nc - 1)  # All non-constant intersects each other
    s += cx * nc * 2   # All constant X intersects with all non-constant
    s += cy * nc * 2   # All constant Y intersects with all non-constant
    s += cx * cy * 2   # All constant X intersects with all constant Y

    print(m, s)

    return


# Creates our Tn generator
tn_gen = Tn_generator()

# Generates N points
for i in range(n):
    tn = next(tn_gen)   # Gets the X value of the point
    tn1 = next(tn_gen)  # Gets the Y value of the point

    point = (tn, tn1)   # Creates the point

    # Adds the point to the points array, if it is a new one
    if point not in points:
        points.append(point)
    # Otherwise shows a warning message
    else:
        print('Duplicated point:', point)

# Generates the lines
for i, p1 in enumerate(points[:-1]):
    for p2 in points[i + 1:]:
        # Gets the coefficients
        # a is the angular coefficient
        # b is the linear coefficient
        a, b = get_coefficients(p1, p2)

        # Creates the array for the angular coefficient if it doesn't exist
        if a not in lines:
            lines[a] = []

        # Adds the linear coefficient to the angular coefficient array
        # if it is a new one
        if b not in lines[a]:
            lines[a].append(b)
        else:
            # Runs a lot faster if not print to console
            # Gets the equation for pretty print
            equation = get_equation(a, b)

            print('Duplicated line:', equation)
            print('Points:', (p1, p2))
            print()

S()
