import pygame
from file_path import res

class UI(pygame.sprite.Sprite):
    def __init__(self, player_health, display_surface, player):
        super().__init__()
        self.player_health = player_health
        self.display_surface = display_surface
        self.player = player
        self.image = pygame.image.load(res('../graphics/ui/health_bar.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = (20,20))
        self.health_bar_rect = pygame.Rect(52, 48, self.player_health*1.55, 6)

    def update(self, player_health):
        self.health_bar_rect.width = player_health*1.55
        pygame.draw.rect(self.display_surface, 'red', self.health_bar_rect)
        pygame.draw.circle(self.display_surface, 'gold', (60, 120), 4 * self.player.ultra)
        pygame.draw.circle(self.display_surface, 'black', (60, 120), 40, 3)