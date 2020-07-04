import pygame
import slider
import sys

pygame.font.init()

class Grid:
    board = [
        [0, 9, 3, 1, 0, 5, 6, 4, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 5],
        [5, 0, 1, 2, 0, 9, 3, 0, 7],
        [2, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 3, 6, 9, 0, 7, 5, 2, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 1],
        [3, 0, 2, 4, 0, 8, 1, 0, 9],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 4, 7, 3, 0, 2, 8, 5, 0]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height,self.board[i][j]!=0) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def draw(self):
        # filling window with white colour
        self.win.fill((255, 255, 255))

        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    # start solving
    def solve_gui(self):
        global speed, board,TD
        events(speed, board)

        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        # trying number from 1 to 9 in each empty cell
        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(TD)

                if self.solve_gui():
                    return True

                # on backtracking
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(TD)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height,already):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.already=already

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if not(self.value == 0):
            # printing number
            text = fnt.render(str(self.value), 1, (0, 0, 0)if self.already else (255,100,0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

    def draw_change(self, win, g):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        # don't show if 0
        if not(self.value == 0):
            # printing number
            text = fnt.render(str(self.value), 1, (0, 0, 0) if self.already else (255,100,0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if g:
            # on not backtracking
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            # on backtracking
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
    def set(self, val):
        self.value = val

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

def valid(bo, num, pos):
    # Checking row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Checking column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Checking box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False
    return True


def events(speed,board):
    # execute the events
    global TD


    for event in pygame.event.get():
        # closing window
        if event.type == pygame.QUIT:
            sys.exit()

        # start solving
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.solve_gui()

        # updating slider circle
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if speed.button_rect.collidepoint(pos):
                speed.hit = True
        elif event.type == pygame.MOUSEBUTTONUP:
            speed.hit = False

    if speed.hit:
        speed.move()

    # refreshing slider
    speed.draw()

    pygame.display.update()
    TD=310-int(speed.val)

    return False

def main():
    global speed,board
    win = pygame.display.set_mode((540, 600))
    board = Grid(9, 9, 540, 540, win)
    pygame.display.set_caption("Sudoku")

    # creating slider
    speed = slider.Slider("Speed", 100, 300, 10, (230,545),win)

    while True:
        board.draw()
        events(speed,board)

main()