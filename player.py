import pygame

class Player:
    def __init__(self, x, y, width, height, image):
        self.width = width
        self.height = height
        self.direction = "down"
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
    def draw(self, surface):
        if self.direction == "up":
            self.image = pygame.image.load("./pictures/char_up.png")
        elif self.direction == "left":
            self.image = pygame.image.load("./pictures/char_left.png")
        elif self.direction == "right":
            self.image = pygame.image.load("./pictures/char_right.png")
        elif self.direction == "down":
            self.image = pygame.image.load("./pictures/char_down.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        surface.blit(self.image, self.rect)