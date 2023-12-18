import pygame 

class Laser(pygame.sprite.Sprite):
	def __init__(self,pos,speed,screen_height, crt_bullet = False):
		super().__init__()
		self.name = "normal"
		if crt_bullet:
			self.name = "crt"
			self.image = pygame.image.load('picture\\crtbulletresize.png')
		else:
			self.image = pygame.Surface((4,20))
			self.image.fill('white')
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_constraint = screen_height

	def destroy(self):
		if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.destroy()

class Laser_boss(pygame.sprite.Sprite):
	def __init__(self,pos,speed,screen_height):
		super().__init__()
		self.image = pygame.image.load(f"picture\\bossbullet1.png")
		self.rect = self.image.get_rect(center = pos)
		self.speed = speed
		self.height_y_constraint = screen_height

	def resize(self, pos):
		self.image = pygame.transform.scale(self.image, (150, 350))
		self.rect = self.image.get_rect(center = pos)

	def destroy(self):
		if self.rect.y >= self.height_y_constraint + 50:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.destroy()