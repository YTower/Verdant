import pygame
from settings import *

class MagicPlayer:
	def __init__(self, animation_manager):
		self.animation_manager = animation_manager

	def heal(self, player, strenght, cost):
		if player.energia >= cost:
			player.vida += strenght
			player.energia -= cost
			if player.vida >= player.stats['vida']:
				player.vida = player.stats['vida']
