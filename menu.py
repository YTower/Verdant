import pygame, sys
from settings import *

img_jogar_1 = pygame.image.load('./assets/UI/jogar-1.png')
img_sair_1 = pygame.image.load('./assets/UI/sair-1.png')
img_jogar_2 = pygame.image.load('./assets/UI/jogar-2.png')
img_sair_2 = pygame.image.load('./assets/UI/sair-2.png')
img_controles_1 = pygame.image.load('./assets/UI/controles-1.png')
img_controles_2 = pygame.image.load('./assets/UI/controles-2.png')

class Button:
    def __init__(self, x, y, img, hover_img):
        self.img = img
        self.hover_img = hover_img
        self.hover = False
        self.pos = pygame.mouse.get_pos()
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.click = False
        self.click_sound = pygame.mixer.Sound('./assets/sound-effects/click.wav')
        self.click_sound.set_volume(0.6)
    
    def draw(self, display_surface):              
        if self.hover == True:
            display_surface.blit(self.hover_img, (self.rect.x, self.rect.y))
        else:
            display_surface.blit(self.img, (self.rect.x, self.rect.y))


botao_jogar = Button(325, 275, img_jogar_1, img_jogar_2)
botao_controles = Button(325, 325, img_controles_1, img_controles_2)
botao_sair = Button(325, 375, img_sair_1, img_sair_2)


def menu_principal(display_surface):
    background = pygame.image.load('./assets/UI/menu-background.png')
    background_pos = (0,0)
    display_surface.blit(background, background_pos)

    botao_jogar.draw(display_surface)
    botao_controles.draw(display_surface)
    botao_sair.draw(display_surface)


def menu_final(display_surface):
    background = pygame.image.load('./assets/UI/menu-final-background.png')
    background_pos = (0,0)
    display_surface.blit(background, background_pos)
    botao_sair.draw(display_surface)


def display_instructions(display_surface):
    img = pygame.image.load('./assets/UI/instruct.png')
    img_pos = (0,0)
    display_surface.blit(img, img_pos)        
        