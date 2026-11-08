import pygame

class Block:
    def __init__(self, x, y, width, height, image, order=0, layer=0):
        self.rect = pygame.Rect(x, y, width, height)
    
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height + 16))
        self.image_path = image

        self.order = order # 같은 레이어 내에서의 visible 우선순위를 나타내는 속성
        self.layer = layer # 블록의 레이어를 나타내는 속성
    def draw(self, surface):
        surface.blit(self.image, self.rect)


class BlockManager:
    def __init__(self):
        self.list = []
    def add_block(self, block):
        self.list.append(block)
    def remove_block(self, block):
        if block in self.list:
            self.list.remove(block)
    def sort_blocks(self):
        self.list.sort(key=lambda block: (block.layer, block.order), reverse=True)
    def draw_blocks(self, surface):
        for block in self.list:
            block.draw(surface)