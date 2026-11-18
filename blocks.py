import pygame
import window
import json

class Block:
    def __init__(self, x, y, width, height, image, order=0, layer=0):
        self.rect = pygame.Rect(x, y, width, height)
    
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height + 16))
        self.image_path = image

        self.order = order # 같은 레이어 내에서의 visible 우선순위를 나타내는 속성
        self.layer = layer # 블록의 레이어를 나타내는 속성

        self.count = 1
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def copy(self):
        new_block = Block(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.image_path,
            self.order,
            self.layer
        )
        return new_block

class Method_Block(Block):
    def __init__(self, x, y, width, height, image, order=0, layer=0, method=None):
        super().__init__(x, y, width, height, image, order, layer)
        self.method = method
    def execute_method(self):
        if callable(self.method):
            self.method()
    def copy(self):
        new_block = Method_Block(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            self.rect.height,
            self.image_path,
            self.order,
            self.layer,
            self.method
        )
        return new_block

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

def save_blocks(filename, block_manager):
    data = {"blocks": []}

    for block in block_manager.list:
        block_data = {
            "type": type(block).__name__,
            "x": block.rect.x,
            "y": block.rect.y,
            "width": block.rect.width,
            "height": block.rect.height,
            "image_path": block.image_path,
            "order": block.order,
            "layer": block.layer
        }
        data["blocks"].append(block_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_blocks(filename, window_manager, stnotice_window, storeitem_window):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    block_manager = BlockManager()

    for block_data in data["blocks"]:
        if block_data["type"] == "Block":
            block = Block(
                block_data["x"],
                block_data["y"],
                block_data["width"],
                block_data["height"],
                block_data["image_path"],
                block_data["order"],
                block_data["layer"]
            )
        elif block_data["type"] == "Method_Block":
            if block_data["image_path"] == "pictures/noti_block.png":
                block = Method_Block(
                    block_data["x"],
                    block_data["y"],
                    block_data["width"],
                    block_data["height"],
                    block_data["image_path"],
                    block_data["order"],
                    block_data["layer"],
                    lambda: window_manager.add_window(stnotice_window)
                )
            elif block_data["image_path"] == "pictures/store_block.png":
                block = Method_Block(
                    block_data["x"],
                    block_data["y"],
                    block_data["width"],
                    block_data["height"],
                    block_data["image_path"],
                    block_data["order"],
                    block_data["layer"],
                    lambda: window_manager.add_window(storeitem_window)
                )
            
        block_manager.add_block(block)

    return block_manager