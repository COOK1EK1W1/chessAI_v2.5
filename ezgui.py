import pygame
import sys
from pygame.locals import *


class Screen:
    def __init__(self, x, y, title="Window"):
        self.buttons = []

        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((x, y), 0, 32)
        pygame.display.set_caption(title)
        self.font = pygame.font.Font('freesansbold.ttf', 42)

        self.background_colour = (255, 255, 255)
        self.DISPLAYSURF.fill(self.background_colour)

    def update_options(self, font=None, background_colour=None):
        if font is not None:
            self.font = pygame.font.Font(font[0], font[1])
        if background_colour is not None:
            self.background_colour = background_colour
            self.DISPLAYSURF.fill(self.background_colour)
        pygame.display.update()

    def run(self, main_func):
        while True:
            mousepos = pygame.mouse.get_pos()
            main_func()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:  # click
                    for i in self.buttons:
                        i.click(mousepos[0], mousepos[1])

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

    def text(self, text, x, y, c=(0, 0, 0)):
        text = self.font.render(text, True, c)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.DISPLAYSURF.blit(text, textRect)

    def rect(self, x, y, width, height, colour=(0, 0, 0)):
        pygame.draw.rect(self.DISPLAYSURF, colour, (x, y, width, height))

    def circle(self, x, y, radius, colour=(0, 0, 0)):
        pygame.draw.circle(self.DISPLAYSURF, colour, (x, y), radius)

    def add_button(self, x, y, width, height, name=None, func=None, colour=(0, 0, 0), toggle=None, toggle_colour=False):
        if name is None:
            self.buttons.append(Button(self, x, y, width, height, len(
                self.buttons), func, colour, toggle, toggle_colour))
        else:
            self.buttons.append(Button(
                self, x, y, width, height, name, func, colour, toggle, toggle_colour))


class Button:
    def __init__(self, screen, x, y, width, height, name, func=False, colour=(0, 0, 0), toggle=None, toggle_colour=False):
        self.screen = screen
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.colour = colour
        self.current_colour = colour

        self.toggle_colour = toggle_colour
        self.toggle = toggle

        self.function = func
        self.screen.rect(x, y, width, height, self.current_colour,)

    def click(self, x, y):
        if x > self.x and x < self.x + self.width and y > self.y and y < self.y + self.height:
            if self.toggle is not None:
                if not self.toggle:
                    if self.toggle_colour is not False:
                        self.current_colour = self.toggle_colour
                    self.toggle = True
                else:
                    if self.toggle_colour is not False:
                        self.current_colour = self.colour
                    self.toggle = False
                self.update(self.current_colour)
            if self.function is not None:
                self.function()

    def update(self, new_colour):
        self.current_colour = new_colour
        pygame.draw.rect(self.screen.DISPLAYSURF, self.current_colour,
                         (self.x, self.y, self.width, self.height))


'''
def a():
    print("hey")

def b():
    print("wassup")


def main():
    print("hello")

screen = Screen(600, 600)
screen.add_button(50,50,100,100, toggle=False)
screen.add_button(200,50,100,100, func=b)
screen.add_button(450,50,100,100, name="jesff")
screen.rect(50, 200, 200, 200)

screen.run(main)
'''
