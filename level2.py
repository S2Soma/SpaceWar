import pygame, sys
from player import Player
import obstacle
from alien import *
from random import choice, randint
from laser import Laser, Laser_boss
from bosslevel2 import boss

class Background(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, speed = 2):
		super().__init__()
		self.image = pygame.transform.scale(pygame.image.load(f'picture\\background.webp').convert_alpha(), (width + 400, height))
		self.rect = self.image.get_rect(topleft = (x,y))
		self.pos = (0,height*(-1))
		self.max_y = height*2
		self.speed = speed
	def update(self):
		self.rect.y += self.speed
		if self.rect.y >= self.max_y:
			self.rect.topleft = self.pos

class Game:
	def __init__(self, screen, screen_width, screen_height, clock):
		# Player setup
		self.screen = screen
		self.clock = clock
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.endgame = False
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5, screen_height, 2)
		self.player = pygame.sprite.GroupSingle(player_sprite)
		self.Boss = pygame.sprite.GroupSingle(boss(screen_width//2, -100, 0))
		self.healthboss = 50
		# health and score setup
		self.lives = 3
		self.live_surf = pygame.image.load(f'picture\\player.png').convert_alpha()
		self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
		self.score = 0
		self.font = pygame.font.Font(f'font\\Pixeled.ttf',15)

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()

		# Extra setup
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)
		# Background setup
		self.backgrounds = pygame.sprite.Group()
		self.create_background()
		self.scoreflag = 3500
		self.checkboss = False

		#audio
		self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
		self.laser_sound.set_volume(0.1)
		self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion_sound.set_volume(0.1)
		self.player_hit_sound = pygame.mixer.Sound('audio/playerhit.mp3')
		self.player_hit_sound.set_volume(0.5)
    
	def create_background(self):
		bg1 = Background(0, (-1)*self.screen_height, self.screen_width, self.screen_height)
		self.backgrounds.add(bg1)
		bg2 = Background(0, 0, self.screen_width, self.screen_height)
		self.backgrounds.add(bg2)
		bg3 = Background(0, self.screen_height, self.screen_width, self.screen_height)
		self.backgrounds.add(bg3)

	def create_alien(self):
		x = randint(0, self.screen_width)
		y = randint(0, self.screen_height//2 + 100)
		select = ["gray", "blue", "red"]
		alien_sprite = Alien_level2(choice(select),x,y, choice((1, -1)))
		self.aliens.add(alien_sprite)
	
	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= self.screen_width:
				alien.direction = -1
			elif alien.rect.left <= 0:
				alien.direction = 1


	def alien_shoot(self):
		if self.aliens.sprites():
			random_alien = choice(self.aliens.sprites())
			laser_sprite = Laser(random_alien.rect.center,6,self.screen_height)
			self.alien_lasers.add(laser_sprite)
			self.laser_sound.play()

	def extra_alien_timer(self):
		self.extra_spawn_time -= 1
		if self.extra_spawn_time <= 0:
			self.extra.add(Extra(choice(['right','left']),self.screen_width))
			self.extra_spawn_time = randint(400,800)

	def collision_checks(self):

		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# alien collisions
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					self.explosion_sound.play()
					if laser.name == "crt":
						continue
					laser.kill()
					
				elif self.checkboss:
					if pygame.sprite.spritecollide(laser,self.Boss,False):
						if laser.name == "crt":
							self.healthboss -= 3
						self.healthboss -= 1
						self.explosion_sound.play()
						laser.kill()
						if self.healthboss <= 0:
							self.victory_message(True)
				# extra collision
				if pygame.sprite.spritecollide(laser,self.extra,True):
					self.score += 500
					laser.kill()
					self.explosion_sound.play()
		if self.score >= self.scoreflag:
			self.checkboss = True
		# alien lasers 
		if self.alien_lasers:
			for laser in self.alien_lasers:
				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					self.player_hit_sound.play()
					if self.lives <= 0:
						self.victory_message(False)

		# aliens
		if self.aliens:
			for alien in self.aliens:
				if pygame.sprite.spritecollide(alien,self.player,False):
					self.victory_message(False)
	
	def display_lives(self):
		for live in range(self.lives - 1):
			x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
			self.screen.blit(self.live_surf,(x,8))

	def display_score(self):
		scoreflag_surf = self.font.render(f'Boss score: {self.scoreflag}',False,'yellow')
		scoreflag_rect = scoreflag_surf.get_rect(topleft = (10,0))
		self.screen.blit(scoreflag_surf,scoreflag_rect)
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,30))
		self.screen.blit(score_surf,score_rect)
		if self.checkboss:
			pygame.draw.rect(self.screen, "red", (200, 70, 200 - (50 - self.healthboss)*4, 20))
			pygame.draw.rect(self.screen, "black", (200, 70, 200, 20), 3)

	def victory_message(self, wingame):
		crt = CRT(self.screen, self.screen_width, self.screen_height)
		background = pygame.transform.scale(pygame.image.load(f'picture\\background.webp').convert_alpha(), (1020, self.screen_height))
		if wingame:
			self.endgame = True
			if self.score == 5400:
				i = 1
			elif self.score == 4900:
				i = 2 
			else:
				i = 3
			image = pygame.transform.scale(pygame.image.load(f"picture\\cup{i}.png").convert_alpha(), (150, 150))
			imagerect = image.get_rect(center = (self.screen_width/2, 200))
			status_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('You won!',False,'yellow')
			status_rect = status_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
			nextlv_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('Next level',False,'white')
			nextlv_rect = nextlv_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 100))
		else:
			status_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('You lose!',False,'red')
			status_rect = status_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
		
		replay_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('Replay',False,'white')
		replay_rect = replay_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 200))
		while True:
			for event in pygame.event.get():
				self.screen.blit(background, (0,0))
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			if wingame:
				self.screen.blit(image, imagerect)
				if nextlv_rect.collidepoint(pygame.mouse.get_pos()):
					nextlv_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('Next level',False,'red')
					if pygame.mouse.get_pressed(num_buttons=3)[0]:
						return
				else:
					nextlv_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('Next level',False,'white')
				self.screen.blit(nextlv_surf,nextlv_rect)
			self.screen.blit(status_surf,status_rect)
			if replay_rect.collidepoint(pygame.mouse.get_pos()):
				replay_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('Replay',False,'red')
				if pygame.mouse.get_pressed(num_buttons=3)[0]:
					self.resetgame()
					self.endgame = False
					return
			else:
				replay_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('Replay',False,'white')
			self.screen.blit(replay_surf,replay_rect)
			crt.drawlines()
			pygame.display.flip()
			self.clock.tick(60)

	def run(self):
		self.backgrounds.update()
		self.backgrounds.draw(self.screen)
		self.player.update()
		self.alien_lasers.update()
		self.extra.update()
		self.aliens.update()
		self.alien_position_checker()
		self.extra_alien_timer()
		self.collision_checks()
		self.player.sprite.lasers.draw(self.screen)
		if self.checkboss:
			if self.Boss.sprite.update():
				rand_rect = (self.Boss.sprite.rect.centerx +choice([1, -1])*randint(0, 150), self.Boss.sprite.rect.centery)
				laser_sprite = Laser_boss(rand_rect,6,self.screen_height)
				self.alien_lasers.add(laser_sprite)
			self.Boss.draw(self.screen)
		self.player.draw(self.screen)
		self.aliens.draw(self.screen)
		self.alien_lasers.draw(self.screen)
		self.extra.draw(self.screen)
		self.display_lives()
		self.display_score()
	
	def resetgame(self):
		self.aliens.empty()
		self.alien_lasers.empty()
		self.healthboss = 50
		self.checkboss = False
		self.lives = 3
		self.score = 0
		self.checkboss = False
		self.player.sprite.lasers.empty()
		self.Boss.sprite.rect.center = (self.screen_width / 2, -100)
		self.player.sprite.rect.center = (self.screen_width / 2,self.screen_height)

class CRT:
	def __init__(self,screen, screen_width, screen_height):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.screen = screen
		self.tv = pygame.image.load(f'picture\\tv.png').convert_alpha()
		self.tv = pygame.transform.scale(self.tv,(self.screen_width,self.screen_height))

	def create_crt_lines(self):
		line_height = 3
		line_amount = int(self.screen_height / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.tv,'black',(0,y_pos),(self.screen_width,y_pos),1)

	def draw(self):
		self.tv.set_alpha(randint(75,90))
		self.create_crt_lines()
		self.screen.blit(self.tv,(0,0))
	
	def drawlines(self):
		line_height = 3
		line_amount = int(self.screen_height / line_height)
		for line in range(line_amount):
			y_pos = line * line_height
			pygame.draw.line(self.screen,'black',(0,y_pos),(self.screen_width,y_pos),1)

def map2(screen, width, height, clock):
	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER,800)
	CREATEALIEN = pygame.USEREVENT
	pygame.time.set_timer(CREATEALIEN,2000)
	game = Game(screen, width, height, clock)
	crt = CRT(screen, width, height)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == ALIENLASER:
				game.alien_shoot()
			elif event.type == CREATEALIEN:
				if len(game.aliens) == 10:
					continue
				game.create_alien()
		game.run()
		if game.endgame:
			return True
		crt.draw()  
		pygame.display.flip()
		clock.tick(60)


	