# GYMNASIUM-PLANIFICATION

Este proyecto incluye herramientas para generar mapas tipo laberinto y convertirlos a un formato compatible con el entorno de simulación Gymnasium. Y contine distintos algoritmos para la planificación de rutas en formato.

**Autor: Fernando Vela Hidalgo** (GitHub: [github.com/fervh](https://github.com/fervh))
Este proyecto es parte de la asignatura "Simuladores de Robots" en la Universidad Carlos III de Madrid (UC3M).

## Generador de Mapas

El generador de mapas funciona mediante la creación de un laberinto a partir del nombre y apellido proporcionados, junto con una densidad de obstáculos especificada.

### Uso
Para generar un laberinto, ejecuta el script `generador_mapas.py` con los siguientes parámetros:

- `--map`: Nombre del archivo CSV para guardar el laberinto.
- `--name`: Tu nombre para determinar las dimensiones del laberinto.
- `--surname`: Tu apellido para determinar las dimensiones del laberinto.
- `--obstacle-density`: Densidad de obstáculos en el laberinto (valor entre 0 y 1).
- `--multiplication`: Factor de multiplicación para las dimensiones del laberinto.

----
----

## Algoritmos:


## Algoritmo A* (A STAR)
Este algoritmo permite que un robot en Gymnasium se mueva hacia una meta utilizando una ruta óptima calculada con el algoritmo A*.

## Algoritmo BFS (Breadth-First Search)
Este algoritmo permite que un robot en Gymnasium se mueva hacia una meta utilizando una ruta óptima calculada con el algoritmo BFS.

## Funcionalidades

- Carga un laberinto desde un archivo CSV que representa el entorno.
- Implementa el algoritmo para encontrar la ruta óptima desde el punto de inicio hasta la meta.
- Controla el robot en Gymnasium para que siga la ruta óptima generada por el algoritmo.
- Muestra por consola la casilla actual y la siguiente en todo momento para comprobar el funcionamiento del algoritmo.

