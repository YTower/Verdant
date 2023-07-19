import pygame
from settings import *


class UI:
    def __init__(self):
        self.display_suface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)
    

    def criar_barra(self, current_amount, max_amount, bg_rect, color):
        
        # draw background
        pygame.draw.rect(self.display_suface, UI_BG_COLOR, bg_rect, 0, 8)

        # convert stats to pixels
        ratio = current_amount / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # draw the bar
        pygame.draw.rect(self.display_suface, color, current_rect, 0, 8)
        pygame.draw.rect(self.display_suface, UI_BORDER_COLOR, bg_rect, 3, 8)


    def slot_arma_equipada(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_suface, UI_BG_COLOR, bg_rect, 0, 8)
        pygame.draw.rect(self.display_suface, UI_BORDER_COLOR, bg_rect, 3, 8)
        arma = pygame.image.load('./assets/UI/sword.png')
        self.display_suface.blit(arma, (left, top))

    def mostrar_elementos(self, player):
        self.criar_barra(player.vida, player.stats['vida'], self.health_bar_rect, HEALTH_BAR_COLOR)
        self.criar_barra(player.energia, player.stats['energia'], self.energy_bar_rect, ENERGY_BAR_COLOR)
        self.slot_arma_equipada(10, 380)

class TextBubble:
    def __init__(self, text, message_type):
        self.display_suface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.text = text
        self.message_type = message_type
        self.default_bg = pygame.Rect(90, HEIGHT//2 + 65, 450, 150)
        self.rendering_time_counter = 0
        self.display_time_counter = 0
        self.text_speed = 3
        self.done = False
        self.trigger = False

    def display(self):
        if self.done == False:

            if self.message_type == 'speech':
                # draw default background and its border
                pygame.draw.rect(self.display_suface, UI_BG_COLOR, self.default_bg, 0, 8)
                pygame.draw.rect(self.display_suface, UI_BORDER_COLOR, self.default_bg, 3, 8)
                
                # set timer
                if self.rendering_time_counter < self.text_speed * len(self.text):
                    self.rendering_time_counter += 1
                elif self.rendering_time_counter >= self.text_speed * len(self.text) and self.display_time_counter < 100:
                    self.display_time_counter += 1
                else:
                    self.done = True   

                # render text
                textsurf = self.font.render(self.text[0:self.rendering_time_counter//self.text_speed], True, UI_FONT_COLOR)

                # draw text on screen
                self.display_suface.blit(textsurf, (100, HEIGHT//2 + 85)) 


            if self.message_type == 'sign':
                if self.done == False:
                    # draw background
                    pygame.draw.rect(self.display_suface, UI_BG_COLOR, self.default_bg, 0, 8)
                    pygame.draw.rect(self.display_suface, UI_BORDER_COLOR, self.default_bg, 3, 8)

                    # set timer
                    if self.display_time_counter < 100:
                        self.display_time_counter += 1
                    else:
                        self.done = True 

                    # render text
                    textsurf = self.font.render(self.text, True, UI_FONT_COLOR)  

                    # draw text on screen
                    self.display_suface.blit(textsurf, (100, HEIGHT//2 + 85))