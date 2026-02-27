# pydrivingsim/crossing_vehicle.py
import pygame
import random
from pydrivingsim import VirtualObject, World

class CrossingVehicleSprite(pygame.sprite.Sprite):
    def __init__(self, obj):
        super().__init__()
        sprite = pygame.image.load("imgs/car.png").convert_alpha()
        angle = 90 if obj.direction > 0 else -90
        sprite = pygame.transform.rotate(sprite, angle)
        w, h = sprite.get_size()

        scale = (World().scaling_factor * obj.L) / h
        self.image_fix = pygame.transform.smoothscale(sprite, (int(w * scale), int(h * scale)))

        self.image = self.image_fix
        self.rect = self.image.get_rect()
        self.obj = obj

    def update(self):
        self.rect.center = [
            (self.obj.pos[0] - World().get_world_pos()[0]) * World().scaling_factor + World().screen_world_center[0],
            (World().get_world_pos()[1] - self.obj.pos[1]) * World().scaling_factor + World().screen_world_center[1],
        ]


class CrossingVehicle(VirtualObject):
    __metadata = {"dt": 0.05}
    # change y_limit depending on v_max
    def __init__(self, x_cross=60.0, y_limit=60.0, v_min=8.0, v_max=8.0, direction=1):
        super().__init__(self.__metadata["dt"])

        self.length = 4.5
        self.width = 1.5
        self.L = 1.54

        self.x_cross = x_cross
        self.y_limit = y_limit
        self.direction = direction
        self.pos = (self.x_cross, 0.0)

        self.v_min = v_min
        self.v_max = v_max
        self.vel = 0.0

        self.sprite = CrossingVehicleSprite(self)
        self.group = pygame.sprite.Group()
        self.group.add(self.sprite)

        self.active = False

        self.reset()

    def reset(self):
        self.active = False
        self.vel = 0.0

        # start off-road depending on the position
        y0 = -self.y_limit if self.direction > 0 else self.y_limit
        self.pos = (self.x_cross, y0)

    def object_freq_compute(self):
        dt = self.__metadata["dt"]

        if not self.active:
            speed = random.uniform(self.v_min, self.v_max)
            self.vel = self.direction * speed
            self.active = True

        x, y = self.pos
        y = y + self.vel * dt
        self.pos = (x, y)

        if abs(y) > random.uniform(self.y_limit, self.y_limit + self.y_limit / 3):
            self.reset()

    def render(self):
        self.sprite.update()
        self.group.draw(World().screen)
