import pygame
from pytmx.util_pygame import load_pygame
from player import *
from settings import *
from support import *
from weapon import Weapon
from ui import UI, TextBubble
from vfx import AnimationManager
from enemy import Enemy
from magic import MagicPlayer

class Objeto(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type='obstacle', surface= pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0,-10)
        

class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.warning_message = TextBubble("Estou cercado de monstros!", 'speech')
        self.finished = False
        self.death_count = 0
        
        # sprite groups
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # tmx data
        self.tmx_data = load_pygame('./map-editing/new-world.tmx')

        #attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()   

        # particles
        self.animation_manager = AnimationManager()

        self.magic_player = MagicPlayer(self.animation_manager)

    def create_map(self):
        layouts = {
                'boundary': import_csv_layout('./map-editing/new-world_Boundaries.csv'),
                'entities': import_csv_layout('./map-editing/new-world_Entities.csv')
        }

        for style, layout in layouts.items():
            for row_index,row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Objeto((x,y), [self.obstacle_sprites], 'invisible')
                        if style == 'entities':
                            if col == '38':
                                 self.player = Player(
                                                (x,y),
                                                [self.visible_sprites],
                                                self.obstacle_sprites,
                                                self.create_attack,
                                                self.destroy_attack,
                                                self.create_magic)

                            else:
                                if col == '0': monster_name = 'slime'
                                else: monster_name = 'boss'
                                Enemy(monster_name,
                                      (x,y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_exp)
                                
        for obj in self.tmx_data.objects:
            if obj.type == 'sign':
                pos = obj.x,obj.y
                Objeto(pos, [self.obstacle_sprites, self.visible_sprites], 'sign', obj.image) 
            else:
                pos = obj.x,obj.y
                Objeto(pos, [self.obstacle_sprites, self.visible_sprites], 'obstacle', obj.image) 

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
    
    def create_magic(self, style, strenght, cost):
        if style == 'heal':
            self.magic_player.heal(self.player, strenght, cost)
    
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.vida -= amount
            if self.player.vida - amount < 0:
                self.player.vida = 0
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            #self.animation_manager.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particle_type):
        self.animation_manager.create_particles(particle_type, pos, self.visible_sprites)
        self.death_count += 1
        if self.death_count == 13:
                self.finished = True

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.mostrar_elementos(self.player)
        self.warning_message.display()

    def add_exp(self, amount):
        self.player.exp += amount       

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        #camera offset setup
        self.offset = pygame.math.Vector2()

        #ground setup
        self.ground_surface = pygame.image.load('./assets/map/new-world-ground.png').convert_alpha()
        self.ground_rect = self.ground_surface.get_rect(topleft = (0,0))
        
        
    def custom_draw(self, target):      
        #get offset
        self.offset.x = target.rect.centerx - self.half_width
        self.offset.y = target.rect.centery - self.half_height

        #draw ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surface, ground_offset)

        #draw other elements
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)    

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
            

camera_group = CameraGroup()
           