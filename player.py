import pygame
from support import *
from settings import *
from debug import debug
from entity import Entity

janela = pygame.display.set_mode((600,400))
janela_rect = janela.get_rect()

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('./assets/player/down-idle/down-idle.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.obstacle_sprites = obstacle_sprites

        #graphics
        self.import_player_assets()
        self.status = 'down'

        #movement
        self.speed = 3

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        #weapon
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        # print(self.weapon)

        #magic
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        
        #stats
        self.stats = {'vida': 180, 'energia': 60, 'ataque': 8, 'magia': 2, 'velocidade': 4}
        self.max_stats = {'vida': 300, 'energia': 140, 'ataque': 20, 'velocidade': 10}
        self.upgrade_cost = {'vida': 100, 'energia': 100, 'ataque': 100, 'velocidade': 100}
        self.vida = self.stats['vida']
        self.energia = self.stats['energia']
        self.exp = 500
        self.velocidade = self.stats['velocidade']

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        #sound
        self.attack_sound = pygame.mixer.Sound('./assets/sound-effects/swing.wav')
        self.attack_sound.set_volume(0.7)
        self.healing_sound = pygame.mixer.Sound('./assets/sound-effects/power-up.wav')
        self.healing_sound.set_volume(0.5)
        

    def import_player_assets(self):
        character_path = './assets/player/'
        self.animations = {'up': [], 'down': [], 'left': [],'right': [],
                            'up-idle': [], 'down-idle': [], 'left-idle': [], 'right-idle': [],
                            'up-attack': [], 'down-attack': [], 'left-attack': [], 'right-attack': []}
        
        for animation in self.animations.keys():
            full_path = character_path + '/' + animation
            self.animations[animation] = import_folder(full_path)

    def walk(self):
        if not self.attacking:
            teclado = pygame.key.get_pressed()

            #movement
            if teclado[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
                if self.rect.top <= janela_rect.y:
                    self.rect.y = janela_rect.y
            elif teclado[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
        
            if teclado[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif teclado[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
                if self.rect.left <= janela_rect.x:
                    self.rect.x = janela_rect.x
            else:
                self.direction.x = 0

            #attack
            if teclado[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.attack_sound.play()
            
            #magic
            if teclado[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(magic_data.keys())[self.magic_index]
                strenght = list(magic_data.values())[self.magic_index]['strenght'] + self.stats['magia']
                cost = list(magic_data.values())[self.magic_index]['cost']
                self.create_magic(style, strenght, cost)
                self.healing_sound.play()
   
    def get_status(self):

        #idle
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '-idle'
        
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('-idle', '-attack')
                else:
                    if 'attack' in self.status:
                        self.status = self.status + '-attack'
        else:
            self.status = self.status.replace('-attack', '')

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center
    
    def collision(self, direction):                                                                              
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:   #player is moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:   #player is moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:    #player is moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:    #player is moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown'] :
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['ataque']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage
    
    def energy_recovery(self):
        if self.energia < self.stats['energia']:
            self.energia += 0.01 * self.stats['magia']
        else:
            self.energia = self.stats['energia']

    def update(self):
        self.walk()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.rect.center += self.direction * self.speed
        self.energy_recovery()  