import pygame

class Alien(pygame.sprite.Sprite):
	def __init__(self,color,x,y):
		super().__init__()
		file_path = 'picture\\enemy' + color + '1.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))
		if color == 'red': self.value = 100
		elif color == 'blue': self.value = 200
		else: self.value = 300

	def update(self,direction):
		self.rect.x += direction

class Extra(pygame.sprite.Sprite):
	def __init__(self,side,screen_width):
		super().__init__()
		self.image = pygame.image.load(f'picture\\extra.png').convert_alpha()
		
		if side == 'right':
			x = screen_width + 50
			self.speed = - 3
		else:
			x = -50
			self.speed = 3

		self.rect = self.image.get_rect(topleft = (x,80))

	def update(self):
		self.rect.x += self.speed

class Alien_level2(pygame.sprite.Sprite):
	def __init__(self,color,x,y, direction):
		super().__init__()
		self.direction = direction
		file_path = 'picture\\enemy' + color + '1.png'
		self.image = pygame.image.load(file_path).convert_alpha()
		self.rect = self.image.get_rect(topleft = (x,y))
		if color == 'red': self.value = 100
		elif color == 'blue': self.value = 200
		else: self.value = 300

	def update(self):
		self.rect.x += self.direction
        
class Item(pygame.sprite.Sprite):
	def __init__(self,x,y,max_y,speed = 1):
		super().__init__()
		self.image = pygame.image.load(f"picture/item.png")
		self.rect = self.image.get_rect(center = (x,y))
		self.max_y = max_y
		self.speed = speed

	def destroy(self):
		if self.rect.y >= self.max_y:
			self.kill()

	def update(self):
		self.rect.y += self.speed
		self.destroy()

		