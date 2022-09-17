import pygame

class UI(pygame.sprite.Sprite):
    def __init__(self, player_health, display_surface):
        super().__init__()
        self.player_health = player_health
        self.display_surface = display_surface
        self.image = pygame.image.load('../graphics/ui/health_bar.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (20,20))
        self.health_bar_rect = pygame.Rect(52, 48, self.player_health*1.55, 6)

    def update(self, player_health):
        self.health_bar_rect.width = player_health*1.55
        pygame.draw.rect(self.display_surface, 'red', self.health_bar_rect)
