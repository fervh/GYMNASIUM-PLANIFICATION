#!/usr/bin/env python

import gymnasium as gym
import gymnasium_csv

import numpy as np
import heapq
import time
import csv

"""
# Coordinate Systems for `.csv` and `print(numpy)`

X points down (rows); Y points right (columns); Z would point outwards.

*--> Y (columns)
|
v
X (rows)
"""
UP = 0
UP_RIGHT = 1
RIGHT = 2
DOWN_RIGHT = 3
DOWN = 4
DOWN_LEFT = 5
LEFT = 6
UP_LEFT = 7

SIM_PERIOD_MS = 500.0

actions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def get_algorithm_choice():
    print("Choose algorithm:")
    print("1. BFS")
    print("2. A*")
    choice = input("Enter your choice (1/2): ")
    return int(choice)

def print_maze(maze, start, goal, path, explored):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if (i, j) == start:
                print(" O ", end="")
            elif (i, j) == goal:
                print(" O ", end="")
            elif (i, j) in path:
                print(" X ", end="")
            elif (i, j) in explored:
                print(" - ", end="")
            elif maze[i][j] == 1:
                print(" # ", end="")
            else:
                print("   ", end="")
        print()

# Función para cargar el laberinto desde el archivo CSV
def load_map(file_path):
    maze = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            maze.append([int(cell) for cell in row])
    return maze

# Función para obtener vecinos válidos de una celda
def get_neighbors(maze, cell):
    neighbors = []
    rows = len(maze)
    cols = len(maze[0])
    for action in actions:
        neighbor_row = cell[0] + action[0]
        neighbor_col = cell[1] + action[1]
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and maze[neighbor_row][neighbor_col] == 0:
            neighbors.append((neighbor_row, neighbor_col))
    return neighbors

# Función de heurística (distancia Manhattan)
def heuristic(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

# Función para encontrar la ruta óptima usando BFS
def bfs(maze, start, goal):
    frontier = []
    frontier.append(start)
    came_from = {}
    came_from[start] = None
    
    while frontier:
        current_cell = frontier.pop(0)
        
        if current_cell == goal:
            break
        
        for next_cell in get_neighbors(maze, current_cell):
            if next_cell not in came_from:
                frontier.append(next_cell)
                came_from[next_cell] = current_cell
        
        print_maze(maze, start, goal, [], came_from.keys())  # Print current state of the maze
        time.sleep(0.1)
    
    # Reconstruir el camino
    path = []
    current_cell = goal
    while current_cell != start:
        path.append(current_cell)
        current_cell = came_from[current_cell]
    path.append(start)
    path.reverse()
    
    return path

# Función para encontrar la ruta óptima usando A*
def astar(maze, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while frontier:
        current_cost, current_cell = heapq.heappop(frontier)
        
        if current_cell == goal:
            break
        
        for next_cell in get_neighbors(maze, current_cell):
            new_cost = cost_so_far[current_cell] + 1
            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + heuristic(next_cell, goal)
                heapq.heappush(frontier, (priority, next_cell))
                came_from[next_cell] = current_cell
        
        print_maze(maze, start, goal, [], came_from.keys())  # Print current state of the maze
        time.sleep(0.1)
    # Reconstruir el camino
    path = []
    current_cell = goal
    while current_cell != start:
        path.append(current_cell)
        current_cell = came_from[current_cell]
    path.append(start)
    path.reverse()
    
    return path


start = (1, 1)
goal = (14, 6)

env = gym.make('gymnasium_csv-v0',
               render_mode='human',  # "human", "text", None
               inFileStr='../assets/map1.csv',
               initX=start[0],
               initY=start[1],
               goalX=goal[0],
               goalY=goal[1])
observation, info = env.reset()
print("observation: "+str(observation)+", info: "+str(info))
env.render()
time.sleep(0.5)

ACTIONS = [UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT]
ACTION = ACTIONS[0]
PREVIOUS_ACTION = ACTIONS[0]
maze = load_map('../assets/map1.csv')
explored = set()
print("Maze:")
print_maze(maze, start, goal, [], explored)

choice = get_algorithm_choice()

while choice != 1 and choice != 2:
    print("Invalid choice. Please enter 1 or 2.")
    choice = get_algorithm_choice()

if choice == 1:
    path = bfs(maze, start, goal)
elif choice == 2:
    path = astar(maze, start, goal)
else:
    print("Invalid choice. Exiting...")
    exit()

print("\nOptimal Path:")
print_maze(maze, start, goal, path, explored)

path_copy = path.copy()

while True:
      if len(path) > 1:
            # Tomar una acción
            observation, reward, terminated, truncated, info = env.step(ACTION)
            
            # Renderizar y mostrar información después de tomar la acción
            env.render()
            print("Celda actual: ({}, {})".format(observation[0], observation[1]))
            if len(path_copy) > 1:
                  next_cell = path_copy[1]
                  dx = next_cell[0] - observation[0]
                  dy = next_cell[1] - observation[1]
                  path_copy.pop(0)
            else:
                  print("¡Llegaste a la meta!")
                  break
            print("Siguiente celda: ({}, {})".format(next_cell[0], next_cell[1]))
            print("observation: " + str(observation)+", reward: " + str(reward) + ", terminated: " +
                  str(terminated) + ", truncated: " + str(truncated) + ", info: " + str(info))
            time.sleep(SIM_PERIOD_MS/1000.0)
            if dx == -1 and dy == 0:
                  ACTION = UP
            elif dx == -1 and dy == 1:
                  ACTION = UP_RIGHT
            elif dx == 0 and dy == 1:
                  ACTION = RIGHT
            elif dx == 1 and dy == 1:
                  ACTION = DOWN_RIGHT
            elif dx == 1 and dy == 0:
                  ACTION = DOWN
            elif dx == 1 and dy == -1:
                  ACTION = DOWN_LEFT
            elif dx == 0 and dy == -1:
                  ACTION = LEFT
            elif dx == -1 and dy == -1:
                  ACTION = UP_LEFT
      else:
            print("¡Llegaste a la meta!")
            break