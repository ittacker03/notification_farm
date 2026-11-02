from cmath import rect

import pygame

class Block:
    def __init__(self, x, y, width, height, image, order=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height + 16))

        self.layer = 0 # 블록의 레이어를 나타내는 속성, 기본값은 0
        self.order = order # 같은 레이어 내에서의 visible 우선순위를 나타내는 속성, 기본값은 0
    def draw(self, surface):
        surface.blit(self.image, self.rect)