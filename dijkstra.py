import math
import pygame
from queue import PriorityQueue
from node1 import Node

def recon_path(came_from, current, draw):
    """Reconstructs the path from end to start"""
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
        draw()

def dijkstra(draw, grid, start, end):
    """Dijkstra's algorithm for finding the shortest path"""
    vis = {node: False for row in grid for node in row}
    dist = {node: math.inf for row in grid for node in row}
    dist[start] = 0
    came_from = {}
    pri_queue = PriorityQueue()
    pri_queue.put((0, start))

    while not pri_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return []  # Return empty list on quit

        current = pri_queue.get()[1]

        if vis[current]:
            continue

        vis[current] = True

        if current == end:
            recon_path(came_from, end, draw)
            return get_path_from_came_from(came_from, start, end)  # Return path

        if current != start:
            current.make_visited()

        for nei in current.neighbors:
            weight = 1
            if dist[current] + weight < dist[nei]:
                came_from[nei] = current
                dist[nei] = dist[current] + weight
                pri_queue.put((dist[nei], nei))
            if nei != end and nei != start and not vis[nei]:
                nei.make_visiting()

        draw()

    return []  # Return empty list if no path found

def get_path_from_came_from(came_from, start, end):
    """Utility function to reconstruct path from came_from dictionary"""
    path = []
    current = end
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
