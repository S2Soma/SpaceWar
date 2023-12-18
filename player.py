import pygame
from random import randint 
from laser import Laser

class Player(pygame.sprite.Sprite):
	def __init__(self,pos, max_x,speed, max_y = 700, level = 1):
		super().__init__()
		self.level = level
		self.image = pygame.image.load(f'picture\\player21.png').convert_alpha()
		self.rect = self.image.get_rect(midbottom = pos)
		self.speed = speed
		self.max_x = max_x
		self.max_y = max_y
		self.ready = True
		self.laser_time = 0
		self.laser_cooldown = 600

		self.lasers = pygame.sprite.Group()

		# self.laser_sound = pygame.mixer.Sound('../audio/laser.wav')
		# self.laser_sound.set_volume(0.5)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
			# self.laser_sound.play()

	def get_input_level2(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed
		elif keys[pygame.K_LEFT]:
			self.rect.x -= self.speed
		elif keys[pygame.K_UP]:
			self.rect.y -= self.speed
		elif keys[pygame.K_DOWN]:
			self.rect.y += self.speed

		if keys[pygame.K_SPACE] and self.ready:
			self.shoot_laser()
			self.ready = False
			self.laser_time = pygame.time.get_ticks()
	
	def recharge(self):
		if not self.ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_cooldown:
				self.ready = True

	def constraint(self):
		if self.rect.left <= 0:
			self.rect.left = 0
		if self.rect.right >= self.max_x:
			self.rect.right = self.max_x
		if self.rect.top <= 300:
			self.rect.top = 300
		elif self.rect.bottom >= self.max_y:
			self.rect.bottom = self.max_y

	def shoot_laser(self):
		if self.level != 0:
			n = randint(0, 100)
			if n <= 100:
				self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom, True))
				return
		self.lasers.add(Laser(self.rect.center,-8,self.rect.bottom))

	def update(self):
		if self.level == 1:
			self.get_input()
		else:
			self.get_input_level2()
		self.constraint()
		self.recharge()
		self.lasers.update()
	