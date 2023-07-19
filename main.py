import pygame, sys
from player import *
from level import *
from settings import *
from ui import *
from menu import *
from debug import debug

pygame.init()

#setup
janela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Verdant')
janela_rect = janela.get_rect()
clock = pygame.time.Clock()
level = Level()
start_game = False
on_menu = True
pygame.mixer.music.load('./assets/music/menu-music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#GAMELOOP 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                on_menu = True

    # inicio do jogo
    janela.fill((0,0,0))  
    if start_game == False and on_menu == True:
        menu_principal(janela)
        pos = pygame.mouse.get_pos()
        if botao_jogar.rect.collidepoint(pos):
            botao_jogar.hover = True
            if pygame.mouse.get_pressed()[0] == 1 and botao_jogar.click == False:
                botao_jogar.click = True
                botao_jogar.click_sound.play()
                pygame.mixer.music.set_volume(0.2)
                start_game = True
        else:
            botao_jogar.hover = False

        if botao_sair.rect.collidepoint(pos):
            botao_sair.hover = True
            if pygame.mouse.get_pressed()[0] == 1 and botao_sair.click == False:
                botao_sair.click = True
                botao_sair.click_sound.play()
                pygame.quit()
                sys.exit()
        else:
            botao_sair.hover = False
        
        if botao_controles.rect.collidepoint(pos):
            botao_controles.hover = True
            if pygame.mouse.get_pressed()[0] == 1:
                botao_controles.click = True
                botao_controles.click_sound.play()
                on_menu = False
        else:
            botao_controles.hover = False
    
    elif on_menu == False:
        display_instructions(janela)

    else:
        level.run()
    
    if level.finished:
        menu_final(janela)
        pos = pygame.mouse.get_pos()  
        if botao_sair.rect.collidepoint(pos):
            botao_sair.hover = True
            if pygame.mouse.get_pressed()[0] == 1 and botao_sair.click == False:
                botao_sair.click = True
                botao_sair.click_sound.play()
                pygame.quit()
                sys.exit()
        else:
            botao_sair.hover = False


    #debug(level.player.status)

    # update
    pygame.display.update()
    camera_group.update()

    clock.tick(60)

    