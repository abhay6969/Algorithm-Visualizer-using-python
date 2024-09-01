import pygame
import math
from queue import PriorityQueue
from node1 import Node

def recon_path(came_from, current, draw):
    """Reconstructs the path from end to start"""
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
        draw()

def h_function(i_node, end_node):
    """Heuristic function: Manhattan distance"""
    x1, y1 = i_node
    x2, y2 = end_node
    return abs(x1 - x2) + abs(y1 - y2)

def aStar(draw, grid, start, end):
    """A* pathfinding algorithm"""
    count = 0
    priority_queue = PriorityQueue()
    priority_queue.put((0, count, start))
    came_from = {}
    g_score = {node: math.inf for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: math.inf for row in grid for node in row}
    f_score[start] = h_function(start.get_pos(), end.get_pos())
    open_set = {start}

    while not priority_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return []  # Return empty list on quit

        current = priority_queue.get()[2]
        open_set.remove(current)

        if current == end:
            recon_path(came_from, end, draw)
            return get_path_from_came_from(came_from, start, end)  # Return path

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h_function(
                    neighbor.get_pos(), end.get_pos()
                )
                if neighbor not in open_set:
                    count += 1
                    priority_queue.put((f_score[neighbor], count, neighbor))
                    open_set.add(neighbor)
                    if neighbor != end:
                        neighbor.make_visiting()

        draw()
        if current != start:
            current.make_visited()

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
