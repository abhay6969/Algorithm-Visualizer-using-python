import pygame
import math
from queue import Queue
from node1 import Node

def recon_path(came_from, current, draw):
    """Reconstructs the path from end to start."""
    path = []
    while current and current in came_from:
        path.append(current)
        current = came_from[current]
    if current:
        path.append(current)  # Append the start or end node
    
    # Draw the path nodes
    for node in reversed(path):
        if node and not node.is_start() and not node.is_end():
            node.make_path()
        draw()

def bidirectional_search(draw, grid, start, end):
    """Bidirectional Search algorithm for finding the path."""
    if start == end:
        return [start]

    # Initialize queues for both searches
    queue_start = Queue()
    queue_end = Queue()

    queue_start.put(start)
    queue_end.put(end)

    # Initialize dictionaries for tracking paths and visited nodes
    came_from_start = {start: None}
    came_from_end = {end: None}

    visited_start = {start: True}
    visited_end = {end: True}

    while not queue_start.empty() and not queue_end.empty():
        # Process nodes from start queue
        current_start = queue_start.get()
        if current_start in visited_end:
            meet_node = current_start
            recon_path(came_from_start, meet_node, draw)
            recon_path(came_from_end, meet_node, draw)
            return get_path_from_came_from(came_from_start, start, meet_node) + get_path_from_came_from(came_from_end, meet_node, end)[1:]

        for neighbor in current_start.neighbors:
            if neighbor not in visited_start:
                came_from_start[neighbor] = current_start
                visited_start[neighbor] = True
                queue_start.put(neighbor)
                if neighbor != end:
                    neighbor.make_visiting()

        draw()
        if current_start != start:
            current_start.make_visited()

        # Process nodes from end queue
        current_end = queue_end.get()
        if current_end in visited_start:
            meet_node = current_end
            recon_path(came_from_start, meet_node, draw)
            recon_path(came_from_end, meet_node, draw)
            return get_path_from_came_from(came_from_start, start, meet_node) + get_path_from_came_from(came_from_end, meet_node, end)[1:]

        for neighbor in current_end.neighbors:
            if neighbor not in visited_end:
                came_from_end[neighbor] = current_end
                visited_end[neighbor] = True
                queue_end.put(neighbor)
                if neighbor != start:
                    neighbor.make_visiting()

        draw()
        if current_end != end:
            current_end.make_visited()

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
