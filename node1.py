import pygame

HEIGHT,WIDTH = 900,900

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
CYAN = (0, 255, 255)

class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
    def get_pos(self):
        return self.row,self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_visiting(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == CYAN
    
    def reset(self):
        self.color = WHITE
     
    def make_closed(self):
        self.color = RED
            
    def make_visiting(self):
        self.color = GREEN 
        
    def make_barrier(self):
        self.color = BLACK
        
    def make_start(self):
        self.color = ORANGE
        
    def make_end(self):
        self.color = CYAN
    
    def make_visited(self):
        self.color = RED
        
    def make_path(self):
        self.color = PURPLE
        
    def draw(self,win):
        # if self.is_start():
        #     pygame.draw.circle(win, self.color, (self.x + self.width // 2, self.y + self.width // 2), self.width // 2)
        # elif self.is_end():
        #     pygame.draw.polygon(win, self.color, [
        #         (self.x + self.width // 2, self.y),  # Top
        #         (self.x + self.width, self.y + self.width),  # Bottom right
        #         (self.x, self.y + self.width)  # Bottom left
        #     ])
        if self.is_start():
            # Draw an arrow pointing to the right
            pygame.draw.polygon(win, self.color, [
                (self.x + self.width * 0.2, self.y + self.width * 0.4),  # Left-middle
                (self.x + self.width * 0.6, self.y + self.width * 0.4),  # Middle
                (self.x + self.width * 0.6, self.y + self.width * 0.2),  # Top-middle
                (self.x + self.width * 0.8, self.y + self.width * 0.5),  # Tip of the arrow
                (self.x + self.width * 0.6, self.y + self.width * 0.8),  # Bottom-middle
                (self.x + self.width * 0.6, self.y + self.width * 0.6),  # Back to middle
                (self.x + self.width * 0.2, self.y + self.width * 0.6)   # Left-bottom
            ])
        elif self.is_end():
            # Draw a double circle
            pygame.draw.circle(win, self.color, (self.x + self.width // 2, self.y + self.width // 2), self.width // 3)
            pygame.draw.circle(win, self.color, (self.x + self.width // 2, self.y + self.width // 2), self.width // 2, 2)  # Outer ring
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbors(self, grid):
            self.neighbors = []
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
                self.neighbors.append(grid[self.row + 1][self.col])

            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])

            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
                self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self,other):
        return False