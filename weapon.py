import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)

        self.sprite_type = 'weapon'
        
        #direction
        direction = player.status.split('_')[0]

        #graphic
        path = './assets/invisible-sprite.png'
        self.image = pygame.image.load(path).convert_alpha()

        #position
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 5))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 5))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-5, 0))
        elif direction == 'up':
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-5, 0))
        else:
            self.rect = self.image.get_rect(center = player.rect.center)