import pygame
from laser import Laser
class boss(pygame.sprite.Sprite):
	def __init__(self,x,y, max_y = 0):
		super().__init__()
		file_path = 'picture\\boss.png'
		self.image = pygame.transform.scale(pygame.image.load(file_path).convert_alpha(), (500, 250))
		self.rect = self.image.get_rect(center = (x,y))
		self.max_y = max_y
		self.value = 999
		self.laser_time = 0
		self.laser_cooldown = 1000

	def update(self):
		if self.rect.y < self.max_y:
			self.rect.y += 1
		current_time = pygame.time.get_ticks()
		if current_time - self.laser_time >= self.laser_cooldown:
			self.laser_time = current_time
			return True
		return False
        