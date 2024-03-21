"""
Autor: Fernando Vela Hidalgo (https://github.com/fervh)
Asignatura: Simuladores de Robots
Universidad: Universidad Carlos III de Madrid (UC3M)
Fecha: Marzo 2024

Generador de laberintos para Gymnasium.
"""

from lxml import etree
from numpy import genfromtxt
import argparse
import random
import csv

# VARIABLES
altura_caja_píxel = 1.0
resolution = 1  # Just to make similar to MATLAB [pixel/meter]
metro_por_píxel = 1 / resolution  # [meter/pixel]

# Función para generar un laberinto con las dimensiones basadas en el nombre y apellido dados.
def generate_maze(name, surname, obstacle_density, multiplication):
    rows = len(name) * multiplication - 2
    cols = len(surname) * multiplication - 2
    maze = []
    maze.append([1] * (cols + 2))
    for _ in range(rows):
        row = [1]
        for _ in range(cols):
            if random.random() < obstacle_density:
                row.append(1)  # Obstacle
            else:
                row.append(0)  # Empty space
        row.append(1)
        maze.append(row)
    maze.append([1] * (cols + 2))
    return maze

# Función para guardar el laberinto en un archivo CSV.
def save_maze_to_csv(maze, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in maze:
            writer.writerow(row)



# Función principal del programa.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--map", type=str, required=True, help="Nombre del archivo CSV del laberinto")
    parser.add_argument("--name", type=str, required=True, help="Tu nombre para determinar las dimensiones del laberinto")
    parser.add_argument("--surname", type=str, required=True, help="Tu apellido para determinar las dimensiones del laberinto")
    parser.add_argument("--obstacle-density", type=float, default=0.2, help="Densidad de obstáculos en el laberinto (valor entre 0 y 1)")
    parser.add_argument("--multiplication", type=int, default=1, help="Factor de multiplicación para el laberinto")
    args = parser.parse_args()
    if not 0 <= args.obstacle_density <= 1:
        print("Error: La densidad de obstáculos debe estar entre 0 y 1.")
        return
    maze = generate_maze(args.name, args.surname, args.obstacle_density, args.multiplication)
    save_maze_to_csv(maze, args.map)

    print(f"Laberinto generado con dimensiones: {len(maze)}x{len(maze[0])}")

if __name__ == "__main__":
    main()


