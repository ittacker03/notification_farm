import pygame
import json

class Player:
    def __init__(self, x, y, width, height, image, direction="down"):
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image_path = image
        self.direction = direction
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

# Class Player을 상속,
class User(Player):
    def __init__(self, x, y, width, height, image, direction="down", noti_seed=0):
        super().__init__(x, y, width, height, image, direction)
        self.noti_seed = noti_seed
    def add_noti_seed(self, amount):
        self.noti_seed += amount
    def subtract_noti_seed(self, amount):
        self.noti_seed -= amount
    def get_noti_seed(self):
        return self.noti_seed
    
def save_player(filename, player):
    data = {
        "type": type(player).__name__,
        "x": player.rect.x,
        "y": player.rect.y,
        "width": player.width,
        "height": player.height,
        "image": player.image_path,
        "direction": player.direction
    }
    if isinstance(player, User):
        data["noti_seed"] = player.noti_seed

    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=4))

def load_player(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    if data["type"] == "User":
        player = User(data["x"], data["y"], data["width"], data["height"], data.get("image", ""), data.get("direction", "down"), data["noti_seed"])
    else:
        player = Player(data["x"], data["y"], data["width"], data["height"], data.get("image", ""), data.get("direction", "down"))
    return player