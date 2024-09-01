import pygame
from node1 import Node
from astar import aStar
from dijkstra import dijkstra
from dfs import dfs
from bi_directional import bidirectional_search  # Import the bidirectional search function

HEIGHT, WIDTH = 900, 900
ROWS = 30  # Adjust this for larger or smaller boxes

# Colors
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

# Initialize fonts
font = pygame.font.SysFont('Arial', 24)

def buildGrid(rows, width):
    grid = []
    node_width = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i, j, node_width, rows))
    return grid

def drawGridLines(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(window, GREY, (i * gap, 0), (i * gap, width))

def drawPath(window, path):
    if len(path) > 1:
        for i in range(len(path) - 1):
            start_pos = (path[i].x + path[i].width // 2, path[i].y + path[i].width // 2)
            end_pos = (path[i + 1].x + path[i + 1].width // 2, path[i + 1].y + path[i + 1].width // 2)
            pygame.draw.line(window, PURPLE, start_pos, end_pos, 2)

def draw(window, grid, rows, width, path=[]):
    window.fill(WHITE)  # Clear the window before drawing

    # Draw the grid and nodes
    for row in grid:
        for node in row:
            node.draw(window)
    
    drawGridLines(window, rows, width)

    # Draw the path
    drawPath(window, path)

    # Display the message at the top center of the window
    message = "Press A for A* | Press D for Dijkstra | Press B for DFS | Press E for Bidirectional | Press C to Clear"
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(width // 2, 20))  # Top center
    pygame.draw.rect(window, WHITE, text_rect.inflate(10, 10))  # Background rectangle for text
    window.blit(text, text_rect)

    pygame.display.update()

def getClickedPosition(position, rows, width):
    gap = width // rows
    x, y = position
    row, column = x // gap, y // gap
    return (row, column)

def main(window, WIDTH):
    grid = buildGrid(ROWS, WIDTH)

    start, end = None, None
    path = []  # Initialize path as an empty list

    run = True
    while run:
        draw(window, grid, ROWS, WIDTH, path)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                position = pygame.mouse.get_pos()
                row, column = getClickedPosition(position, ROWS, WIDTH)
                node = grid[row][column]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                position = pygame.mouse.get_pos()
                row, column = getClickedPosition(position, ROWS, WIDTH)
                node = grid[row][column]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    path = aStar(lambda: draw(window, grid, ROWS, WIDTH, path), grid, start, end)
                    
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    path = dijkstra(lambda: draw(window, grid, ROWS, WIDTH, path), grid, start, end)
                    
                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    path = dfs(lambda: draw(window, grid, ROWS, WIDTH, path), grid, start, end)
                    
                if event.key == pygame.K_e and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    path = bidirectional_search(lambda: draw(window, grid, ROWS, WIDTH, path), grid, start, end)
                    
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = buildGrid(ROWS, WIDTH)
                    path = []  # Reset path
                    draw(window, grid, ROWS, WIDTH, path)

    pygame.quit()

main(window, WIDTH)
