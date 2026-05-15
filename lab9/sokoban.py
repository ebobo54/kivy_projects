import pygame, sys, os
from pygame.locals import *

## Helper functions for movement
def get_offset(d, w):
    """Get the displacement in the map for the movement"""
    if d == 'l':  # left
        return -1
    elif d == 'r':  # right
        return 1
    elif d == 'u':  # up
        return -w
    elif d == 'd':  # down
        return w
    return 0

def move_man(level, pos):
    """Move the player to a position"""
    if level[pos] == '-':
        level[pos] = '@'
    elif level[pos] == '.':
        level[pos] = '+'

def move_floor(level, pos):
    """Reset a position to floor"""
    if level[pos] == '@' or level[pos] == '+':
        if level[pos] == '@':
            level[pos] = '-'
        else:
            level[pos] = '.'

def move_box(level, pos):
    """Move a box to a position"""
    if level[pos] == '-':
        level[pos] = '$'
    elif level[pos] == '.':
        level[pos] = '*'

class Sokoban:
    ## Initialize the Sokoban game
    def __init__(self):
        ## Set the map
        self.level = list(
            "----#####----------"
            "----#---#----------"
            "----#$--#----------"
            "--###--$##---------"
            "--#--$-$-#---------"
            "###-#-##-#---######"
            "#---#-##-#####--..#"
            "#-$--$----------..#"
            "#####-###-#@##--..#"
            "----#-----#########"
            "----#######--------")

        ## Set the width and height of the map and the position of the player in the map
        self.w = 19
        self.h = 11
        self.man = 163
        
        ## Initialize solution tracking
        self.solution = []
        self.todo = []
        self.push = 0

    ## Draw the map on the pygame window based on the map level
    def draw(self, screen, skin):
        ## Get the width of each image element
        w = skin.get_width() / 4

        ## Iterate through each character element in the map level
        for i in range(0, self.w):
            for j in range(0, self.h):
                ## Get the character at the j-th row and i-th column in the map
                item = self.level[j*self.w + i]

                ## Display as a wall(#) at this position
                if item == '#':
                    screen.blit(skin, (i*w, j*w), (0,2*w,w,w))
                ## Display as a space(-) at this position
                elif item == '-':
                    screen.blit(skin, (i*w, j*w), (0,0,w,w))
                ## Display as a player(@) at this position
                elif item == '@':
                    screen.blit(skin, (i*w, j*w), (w,0,w,w))
                ## Display as a box($) at this position
                elif item == '$':
                    screen.blit(skin, (i*w, j*w), (2*w,0,w,w))
                ## Display as a target point(.) at this position
                elif item == '.':
                    screen.blit(skin, (i*w, j*w), (0,w,w,w))
                ## Display as the player on a target point effect
                elif item == '+':
                    screen.blit(skin, (i*w, j*w), (w,w,w,w))
                ## Display as the box placed on a target point effect
                elif item == '*':
                    screen.blit(skin, (i*w, j*w), (2*w,w,w,w))

    ## Internal move function
    def _move(self, d):
    ## Get the displacement in the map for the movement
        h = get_offset(d, self.w)

    ## If the target area of the movement is empty space or a target point, only the player needs to move
        if self.level[self.man + h] == '-' or self.level[self.man + h] == '.':
            ## Move the player to the target position
            move_man(self.level, self.man + h)
            ## Set the original position of the player after movement
            move_floor(self.level, self.man)
            ## The new position of the player
            self.man += h
            ## Add the move operation to the solution
            self.solution.append(d)

    ## If the target area of the movement is a box, both the box and the player need to move
        elif self.level[self.man + h] == '*' or self.level[self.man + h] == '$':
        ## The displacement of the box and the player's position
            h2 = h * 2
        ## The box can only be moved if the next position is empty space or a target point
            if self.level[self.man + h2] == '-' or self.level[self.man + h2] == '.':
            ## Move the box to the target point
                move_box(self.level, self.man + h2)
            ## ne ОЧИЩАЕМ старую позицию ящика (этого не хватало!)
                move_floor(self.level, self.man + h)
            ## Move the player to the target point
                move_man(self.level, self.man + h)
            ## Reset the current position of the player
                move_floor(self.level, self.man)
            ## Set the player's new position
                self.man += h
            ## Mark the move operation as an uppercase character
                self.solution.append(d.upper())
            ## Increment the number of steps for pushing the box
                self.push += 1

    ## Undo operation
    def undo(self):
        ## Check if there is a movement record
        if len(self.solution) > 0:
            ## Store the movement record in the todo list for redo operation
            self.todo.append(self.solution[-1])
            ## Delete the movement record
            self.solution.pop()

            ## Get the offset to be moved for the undo operation
            h = get_offset(self.todo[-1].lower(), self.w) * -1

            ## Check if this operation only moves the character without pushing a box
            if self.todo[-1].islower():
                ## Move the character back to its original position
                move_man(self.level, self.man + h)
                ## Set the current position of the character
                move_floor(self.level, self.man)
                ## Set the position of the character on the map
                self.man += h
            else:
                ## If this step pushes a box, move the character, box, and perform related operations
                move_floor(self.level, self.man - h)
                move_box(self.level, self.man)
                move_man(self.level, self.man + h)
                self.man += h
                self.push -= 1

    ## Redo operation
    def redo(self):
        ## Check if there is an undo operation recorded
        if len(self.todo) > 0:
            ## Move back the undone steps
            self._move(self.todo[-1].lower())
            ## Delete this record
            self.todo.pop()

## Initialize pygame
pygame.init()

## Set the size of the pygame display window
screen = pygame.display.set_mode((400, 300))

## Load image elements from a single file
skinfilename = os.path.join('borgar.png')

try:
    skin = pygame.image.load(skinfilename)
except pygame.error as msg:
    print('cannot load skin')
    raise SystemExit(msg)

skin = skin.convert()

## Create game instance
game = Sokoban()

## Set the background color
screen.fill(skin.get_at((0, 0)))

clock = pygame.time.Clock()
pygame.key.set_repeat(200, 50)

## Game main loop
while True:
    clock.tick(60)
    
    ## Get game events
    for event in pygame.event.get():
        ## Quit game event
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        ## Keyboard operation
        elif event.type == KEYDOWN:
            ## Move left
            if event.key == K_LEFT:
                game._move('l')
            ## Move up
            elif event.key == K_UP:
                game._move('u')
            ## Move right
            elif event.key == K_RIGHT:
                game._move('r')
            ## Move down
            elif event.key == K_DOWN:
                game._move('d')
            ## Undo operation
            elif event.key == K_BACKSPACE:
                game.undo()
            ## Redo operation
            elif event.key == K_SPACE:
                game.redo()
    
    ## Draw the game
    screen.fill(skin.get_at((0, 0)))
    game.draw(screen, skin)
    pygame.display.flip()