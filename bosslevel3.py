import pygame
from laser import Laser
class boss_3(pygame.sprite.Sprite):
	def __init__(self, x, y, max_x, max_y = 0):
		super().__init__()
		file_path = 'picture\\boss3.png'
		self.image = pygame.transform.scale(pygame.image.load(file_path).convert_alpha(), (300, 200))
		self.rect = self.image.get_rect(center = (x,y))
		self.max_y = max_y
		self.max_x = max_x
		self.value = 7777
		self.attack_time = 0
		self.attack_cooldown = 1500
		self.direction = 1

	def update(self):
		if self.rect.y < self.max_y:
			self.rect.y += 1
			return False
		else:
			if (self.rect.x <= -self.rect.width//2) or (self.rect.x >= self.max_x - self.rect.width//2):
				self.direction *= (-1)
			self.rect.x += self.direction
		current_time = pygame.time.get_ticks()
		if current_time - self.attack_time >= self.attack_cooldown:
			self.attack_time = current_time
			return True
		return False
        