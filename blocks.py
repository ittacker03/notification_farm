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
    def __init__(self, x, y, width, height, image, order=0, layer=0, method=None, auto=False, delay=3000):
        super().__init__(x, y, width, height, image, order, layer)
        self.method = method

        self.auto = auto
        self.delay = delay
        self.created_at = pygame.time.get_ticks()
        self.executed = False
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
    def update(self):
        current_time = pygame.time.get_ticks()
        if self.auto and not self.executed and current_time - self.created_at >= self.delay:
            self.execute_method()
            self.executed = True

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
    def update_blocks(self):
        for block in self.list:
            if isinstance(block, Method_Block):
                block.update()

def save_blocks(filename, block_manager):
    data = {"blocks": [],
            "method_blocks": []}

    for block in block_manager.list:
        if isinstance(block, Method_Block):
            block_data = {
            "type": type(block).__name__,
            "x": block.rect.x,
            "y": block.rect.y,
            "width": block.rect.width,
            "height": block.rect.height,
            "image_path": block.image_path,
            "order": block.order,
            "layer": block.layer,
            "auto": block.auto,
            "delay": block.delay
            }
            data["method_blocks"].append(block_data)
        else:
            block_data = {
            "type": type(block).__name__,
            "x": block.rect.x,
            "y": block.rect.y,
            "width": block.rect.width,
            "height": block.rect.height,
            "image_path": block.image_path,
            "order": block.order,
            "layer": block.layer,
            }
            data["blocks"].append(block_data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_blocks(filename, window_manager, stnotice_window, storeitem_window):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    block_manager = BlockManager()

    for block_data in data["blocks"]:
        block = Block(
            block_data["x"],
            block_data["y"],
            block_data["width"],
            block_data["height"],
            block_data["image_path"],
            block_data["order"],
            block_data["layer"]
        )
        block_manager.add_block(block)

    for method_block_data in data["method_blocks"]:
        if method_block_data["image_path"] == "pictures/noti_block.png":
            block = Method_Block(
                method_block_data["x"],
                method_block_data["y"],
                method_block_data["width"],
                method_block_data["height"],
                method_block_data["image_path"],
                method_block_data["order"],
                method_block_data["layer"],
                lambda: window_manager.add_window(stnotice_window)
            )
        elif method_block_data["image_path"] == "pictures/store_block.png":
            block = Method_Block(
                method_block_data["x"],
                method_block_data["y"],
                method_block_data["width"],
                method_block_data["height"],
                method_block_data["image_path"],
                method_block_data["order"],
                method_block_data["layer"],
                lambda: window_manager.add_window(storeitem_window)
            )
        elif method_block_data["image_path"] == "pictures/noti_seed_planted.png":
            block = Method_Block(
                method_block_data["x"],
                method_block_data["y"],
                method_block_data["width"],
                method_block_data["height"],
                method_block_data["image_path"],
                method_block_data["order"],
                method_block_data["layer"],
                lambda: planted2growing(block, block_manager),
                method_block_data["auto"],
                method_block_data["delay"]
            )
        elif method_block_data["image_path"] == "pictures/noti_seed_growing.png":
            block = Method_Block(
                method_block_data["x"],
                method_block_data["y"],
                method_block_data["width"],
                method_block_data["height"],
                method_block_data["image_path"],
                method_block_data["order"],
                method_block_data["layer"],
                lambda: growing2grown(block, block_manager),
                method_block_data["auto"],
                method_block_data["delay"]
            )
        elif method_block_data["image_path"] == "pictures/noti_seed_grown.png":
            block = Method_Block(
                method_block_data["x"],
                method_block_data["y"],
                method_block_data["width"],
                method_block_data["height"],
                method_block_data["image_path"],
                method_block_data["order"],
                method_block_data["layer"],
                lambda: grown2grass(block, block_manager),
                method_block_data["auto"],
                method_block_data["delay"]
            )
        block_manager.add_block(block)
        block_manager.sort_blocks()

    return block_manager

### Block state transition functions ###

def replace_block(old_block, new_block, block_manager):
    block_manager.remove_block(old_block)
    block_manager.add_block(new_block)
    block_manager.sort_blocks()

def grown2grass(grown, block_manager):
    grass = Block(grown.rect.x, grown.rect.y, grown.rect.width, grown.rect.height, "pictures/grass_block.png", grown.order, grown.layer)
    replace_block(grown, grass, block_manager)

def growing2grown(growing, block_manager):
    grown = Method_Block(growing.rect.x, growing.rect.y, growing.rect.width, growing.rect.height, "pictures/noti_seed_grown.png", growing.order, growing.layer, method=lambda: grown2grass(grown, block_manager))
    replace_block(growing, grown, block_manager)

def planted2growing(planted, block_manager):
    growing = Method_Block(planted.rect.x, planted.rect.y, planted.rect.width, planted.rect.height, "pictures/noti_seed_growing.png", planted.order, planted.layer, method=lambda: growing2grown(growing, block_manager), auto=True, delay=3000)
    replace_block(planted, growing, block_manager)

def grass2planted(grass, block_manager):
    planted = Method_Block(grass.rect.x, grass.rect.y, grass.rect.width, grass.rect.height, "pictures/noti_seed_planted.png", grass.order, grass.layer, method=lambda: planted2growing(planted, block_manager), auto=True, delay=3000)
    replace_block(grass, planted, block_manager)