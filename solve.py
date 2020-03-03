import pygame
from sudoku import valid, solve
pygame.font.init()

class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected = None
    
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
    

    def draw(self, win):
        # Draw Grid lines
        gap = self.width // 9

        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(win, (0, 0, 0), (0, i*gap), (self.width, i*gap), thickness)
            pygame.draw.line(win, (0, 0, 0), (i*gap, 0), (i*gap, self.height), thickness)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def place(self, val, row, col):
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row,col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def select(self, row, col):
        for i in range(9):
            for j in range(9):
                self.cubes[i][j].selected = False
        
        self.cubes[row][col].selected = True

class Cube:
    row = 9
    col = 9

    def __init__(self, value, row, col, width, height):
        self.row = row
        self.col = col
        self.value = value
        self.width = width
        self.height = height
        self.selected = False
        self.temp = 0
    
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width // 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x+5, y+5))
        elif not self.value == 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + int((gap/2 - text.get_width()/2)), y + int((gap/2 - text.get_height()/2))))

        if self.selected:
            # Green color
            color = (0, 255, 0)
            pygame.draw.rect(win, color, (x, y, gap, gap), 3)
        
    def set(self, val):
        self.value = val
    
    def set_temp(self, val):
        self.temp = val

def redraw_Window(win, board):
    win.fill((255, 255, 255))
    board.draw(win)
    


# Main loop
def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    
    board = Grid(9, 9, 540, 540)


    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
        for i in range(9):
            for j in range(9):
                for val in range(1, 10):
                    if board.cubes[i][j].temp != 0:
                        board.select(i, j)
                        if board.place(board.cubes[i][j].temp, i, j):
                            print("Solved")
                            
                            # Checks is the board is solved
                            if board.is_finished:
                                run = False

                    
                    redraw_Window(win, board)
                    pygame.display.update()

                    board.cubes[i][j].temp = val
                    board.cubes[i][j].selected = False
            
main()
pygame.quit()
