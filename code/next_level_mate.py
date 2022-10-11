import pygame

class Next_level_mate(pygame.sprite.Sprite):
    def __init__(self, stat, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('../graphics/player/level_2/running/0.png').convert_alpha()
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(toplest = pos)

        self.stat = stat

    def update(self, shift_speed):
        self.rect.x += shift_speed
