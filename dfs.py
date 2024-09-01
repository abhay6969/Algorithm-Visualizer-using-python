import pygame
from node1 import Node

def recon_path(came_from, current, draw):
    """Reconstructs the path from end to start"""
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
        draw()

def dfs(draw, grid, start, end):
    """Depth-First Search algorithm for finding the path."""
    stack = [start]
    came_from = {}
    visited = {node: False for row in grid for node in row}
    visited[start] = True

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return []  # Return empty list on quit

        current = stack.pop()

        if current == end:
            recon_path(came_from, end, draw)
            end.make_end()  # Draw the end node again to keep its appearance intact
            return get_path_from_came_from(came_from, start, end)  # Return path

        for neighbor in current.neighbors:
            if not visited[neighbor]:
                came_from[neighbor] = current
                stack.append(neighbor)
                visited[neighbor] = True
                if neighbor != start and neighbor != end:
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
