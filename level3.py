import pygame, sys
from player import Player
from obstacle import shield
from alien import *
from random import choice, randint
from laser import Laser, Laser_boss
from bosslevel3 import boss_3

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
		self.Boss = pygame.sprite.GroupSingle(boss_3(screen_width//2, -100,self.screen_width, 60))
		self.shield =  pygame.sprite.GroupSingle()
		self.value_shield = 0
		self.healthboss = 100
		# health and score setup
		self.lives = 3
		self.live_surf = pygame.image.load(f'picture\\player.png').convert_alpha()
		self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
		self.score = 0
		self.font = pygame.font.Font(f'font\\Pixeled.ttf',15)
		#Item and shield setup
		self.shield_surf = pygame.image.load(f'picture\\shield.png').convert_alpha()
		self.shield_x_start_pos = screen_width - (self.shield_surf.get_size()[0] * 3 + 20)
		self.Item_sprite = pygame.sprite.GroupSingle()
		self.Shield_sprite = pygame.sprite.GroupSingle()
		# Background setup
		self.background = pygame.transform.scale(pygame.image.load(f"picture/banckground.png"), (screen_width*2, screen_height))
		#boss laser, skill
		self.boss_lasers = pygame.sprite.Group()
		self.boss_skill = 0
		self.EVTSKILL = pygame.USEREVENT + 1
		self.EVTITEM = pygame.USEREVENT + 2
		pygame.time.set_timer(self.EVTITEM,15000)

		#audio
		self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
		self.laser_sound.set_volume(0.1)
		self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion_sound.set_volume(0.1)
		self.player_hit_sound = pygame.mixer.Sound('audio/playerhit.mp3')
		self.player_hit_sound.set_volume(0.5)
    

	def create_Item(self):
		x = randint(0, self.screen_width)
		y = 0
		Item_sprite = Item(x,y,self.screen_height, 2)
		self.Item_sprite.add(Item_sprite)

	def create_shield(self):
		x = self.player.sprite.rect.centerx
		y = self.player.sprite.rect.centery
		Shield = shield(x, y)
		self.Shield_sprite.add(Shield)

	def boss_shoot(self):
		if self.boss_skill == 1:
				laser_sprite = Laser_boss(self.Boss.sprite.rect.center,6,self.screen_height)
				self.boss_lasers.add(laser_sprite)
				self.laser_sound.play()
				return
		elif self.boss_skill == 2:
			n = choice((150, 300, 450))
			self.Boss.sprite.rect.centerx = n
			for i in range(10):
				x = n - 150 + i*30
				y = self.Boss.sprite.rect.centery
				laser_sprite = Laser_boss((x,y),6,self.screen_height)
				self.boss_lasers.add(laser_sprite)
			self.laser_sound.play()
			return
			
		n = randint(0, 100)
		if n <= 25:
			self.Boss.sprite.direction *= 4 
			self.Boss.sprite.attack_cooldown = 400
			self.boss_skill = 1
			pygame.time.set_timer(self.EVTSKILL,5000)
		elif n <= 50:
			self.Boss.sprite.direction = 0 
			self.Boss.sprite.attack_cooldown = 1000
			self.boss_skill = 2
			pygame.time.set_timer(self.EVTSKILL,3000)	
		elif n <= 75: 
			laser_sprite = Laser_boss(self.Boss.sprite.rect.center,6,self.screen_height)
			laser_sprite.resize(self.Boss.sprite.rect.center)
			self.boss_lasers.add(laser_sprite)
			self.laser_sound.play()
		elif n <= 100:
			laser_sprite = Laser_boss(self.Boss.sprite.rect.center,6,self.screen_height)
			self.boss_lasers.add(laser_sprite)
			self.laser_sound.play()

	def collision_checks(self):
		if self.Boss.sprite.rect.y < 50:
			return
		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				if pygame.sprite.spritecollide(laser,self.Boss,False):
					if laser.name == "crt":
						self.healthboss -= 3
					self.healthboss -= 1
					self.explosion_sound.play()
					laser.kill()
					if self.healthboss <= 0:
						self.victory_message(True)
		# boss lasers 
		if self.boss_lasers:
			for laser in self.boss_lasers:
				if pygame.sprite.spritecollide(laser,self.Shield_sprite,False):
					laser.kill()
					self.value_shield -= 1
					self.player_hit_sound.play()
					if self.value_shield == 0:
						self.Shield_sprite.empty()
				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					self.player_hit_sound.play()
					if self.lives <= 0:
						self.victory_message(False)
		if self.Item_sprite:
			if pygame.sprite.spritecollide(self.Item_sprite.sprite,self.player,False):
				self.Item_sprite.sprite.kill()
				self.create_shield()
				self.value_shield = 3

	def display_lives_shield(self):
		for live in range(self.lives - 1):
			x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
			self.screen.blit(self.live_surf,(x,8))
		for live in range(self.value_shield):
			x = self.shield_x_start_pos + (live * (self.shield_surf.get_size()[0] + 10))
			y = self.shield_surf.get_size()[1]
			self.screen.blit(self.shield_surf,(x,y))

	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,30))
		self.screen.blit(score_surf,score_rect)
		pygame.draw.rect(self.screen, "red", (200, 70, 200 - (100 - self.healthboss)*2, 20))
		pygame.draw.rect(self.screen, "black", (200, 70, 200, 20), 3)

	def victory_message(self, wingame):
		crt = CRT(self.screen, self.screen_width, self.screen_height)
		if wingame:
			self.endgame = True
			if self.score >= 5400:
				i = 1
			elif self.score >= 4900:
				i = 2 
			else:
				i = 3
			image = pygame.transform.scale(pygame.image.load(f"picture\\cup{i}.png").convert_alpha(), (150, 150))
			imagerect = image.get_rect(center = (self.screen_width/2, 200))
			status_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('You won!',False,'yellow')
			status_rect = status_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
			nextlv_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('End game!',False,'white')
			nextlv_rect = nextlv_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 100))
		else:
			status_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('You lose!',False,'red')
			status_rect = status_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2))
		
		replay_surf = pygame.font.Font(f'font\\Pixeled.ttf',30).render('Replay',False,'white')
		replay_rect = replay_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + 200))
		while True:
			self.screen.blit(self.background, (-self.screen_width//2,0))
			for event in pygame.event.get():
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
		self.screen.blit(self.background, (-self.screen_width//2,0))
		self.player.update()
		if self.Shield_sprite:
			self.Shield_sprite.sprite.update(self.player.sprite.rect.center)
		self.boss_lasers.update()
		self.Item_sprite.update()
		self.collision_checks()
		self.player.sprite.lasers.draw(self.screen)
		if self.Boss.sprite.update():
			self.boss_shoot()
		self.Boss.draw(self.screen)
		self.player.draw(self.screen)
		self.Item_sprite.draw(self.screen)
		self.Shield_sprite.draw(self.screen)
		self.boss_lasers.draw(self.screen)
		self.display_lives_shield()
		self.display_score()
	
	def resetgame(self):
		self.Item_sprite.empty()
		self.boss_lasers.empty()
		self.Shield_sprite.empty()
		self.healthboss = 100
		self.lives = 3
		self.score = 0
		self.value_shield = 0
		self.Boss.sprite.direction = 1
		self.Boss.sprite.attack_cooldown = 1500
		self.boss_skill = 0
		pygame.time.set_timer(self.EVTSKILL,0)
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


def map3(screen, width, height, clock):
	game = Game(screen, width, height, clock)
	crt = CRT(screen, width, height)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == game.EVTSKILL:
				if game.boss_skill == 1:
					game.Boss.sprite.direction /= 4
					game.Boss.sprite.attack_cooldown = 1500
					game.boss_skill = 0
					pygame.time.set_timer(game.EVTSKILL,0)
				elif game.boss_skill == 2:
					game.Boss.sprite.direction = 1
					game.Boss.sprite.attack_cooldown = 1500
					game.boss_skill = 0
					pygame.time.set_timer(game.EVTSKILL,0)
			if event.type == game.EVTITEM:
				game.create_Item()
		game.run()
		if game.endgame:
			return True
		crt.draw()  
		pygame.display.flip()
		clock.tick(60)


	