import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
 
class Game:
	def __init__(self, screen, screen_width, screen_height, clock):
		# Player setup
		self.screen = screen
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.clock = clock
		self.endgame = False
		player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
		self.player = pygame.sprite.GroupSingle(player_sprite)

		# health and score setup
		self.lives = 3
		self.live_surf = pygame.image.load(f'picture\\player.png').convert_alpha()
		self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 + 20)
		self.score = 0
		self.font = pygame.font.Font(f'font\\Pixeled.ttf',20)

		# Obstacle setup
		self.shape = obstacle.shape
		self.block_size = 6
		self.blocks = pygame.sprite.Group()
		self.obstacle_amount = 4
		self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = 45, y_start = 480)     

		# Alien setup
		self.aliens = pygame.sprite.Group()
		self.alien_lasers = pygame.sprite.Group()
		self.alien_setup(rows = 5, cols = 6)
		self.alien_direction = 1

		# Extra setup
		self.extra = pygame.sprite.GroupSingle()
		self.extra_spawn_time = randint(40,80)

		#Audio
		self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
		self.laser_sound.set_volume(0.1)
		self.explosion_sound = pygame.mixer.Sound('audio/explosion.wav')
		self.explosion_sound.set_volume(0.1)
		self.player_hit_sound = pygame.mixer.Sound('audio/playerhit.mp3')
		self.player_hit_sound.set_volume(0.5)

	def create_obstacle(self, x_start, y_start,offset_x):
		for row_index, row in enumerate(self.shape):
			for col_index,col in enumerate(row):
				if col == 'x':
					x = x_start + col_index * self.block_size + offset_x
					y = y_start + row_index * self.block_size
					block = obstacle.Block(self.block_size,(241,79,80),x,y)
					self.blocks.add(block)

	def create_multiple_obstacles(self,*offset,x_start,y_start):
		for offset_x in offset:
			self.create_obstacle(x_start,y_start,offset_x)

	def alien_setup(self,rows,cols,x_distance = 80,y_distance = 60,x_offset = 70, y_offset = 100):
		for row_index, row in enumerate(range(rows)):
			for col_index, col in enumerate(range(cols)):
				x = col_index * x_distance + x_offset
				y = row_index * y_distance + y_offset
				
				if row_index == 0: alien_sprite = Alien('gray',x,y)
				elif 1 <= row_index <= 2: alien_sprite = Alien('blue',x,y)
				else: alien_sprite = Alien('red',x,y)
				self.aliens.add(alien_sprite)

	def alien_position_checker(self):
		all_aliens = self.aliens.sprites()
		for alien in all_aliens:
			if alien.rect.right >= self.screen_width:
				self.alien_direction = -1
				self.alien_move_down(2)
			elif alien.rect.left <= 0:
				self.alien_direction = 1
				self.alien_move_down(2)

	def alien_move_down(self,distance):
		if self.aliens:
			for alien in self.aliens.sprites():
				alien.rect.y += distance

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
		if len(self.aliens) == 0:
			self.victory_message(True)
		# player lasers 
		if self.player.sprite.lasers:
			for laser in self.player.sprite.lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					if laser.name == "crt":
						continue
					laser.kill()
					
				# alien collisions
				aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
				if aliens_hit:
					for alien in aliens_hit:
						self.score += alien.value
					if laser.name == "crt":
						continue
					laser.kill()
					self.explosion_sound.play()

				# extra collision
				if pygame.sprite.spritecollide(laser,self.extra,True):
					self.score += 500
					laser.kill()
					self.explosion_sound.play()
		# alien lasers 
		if self.alien_lasers:
			for laser in self.alien_lasers:
				# obstacle collisions
				if pygame.sprite.spritecollide(laser,self.blocks,True):
					laser.kill()

				if pygame.sprite.spritecollide(laser,self.player,False):
					laser.kill()
					self.lives -= 1
					self.score -= 500
					self.player_hit_sound.play()
					if self.lives <= 0:
						self.victory_message(False)

		# aliens
		if self.aliens:
			for alien in self.aliens:
				pygame.sprite.spritecollide(alien,self.blocks,True)
				if pygame.sprite.spritecollide(alien,self.player,False):
					self.victory_message(False)
	
	def display_lives(self):
		for live in range(self.lives - 1):
			x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
			self.screen.blit(self.live_surf,(x,8))

	def display_score(self):
		score_surf = self.font.render(f'score: {self.score}',False,'white')
		score_rect = score_surf.get_rect(topleft = (10,-10))
		self.screen.blit(score_surf,score_rect)

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
		self.player.update()
		self.alien_lasers.update()
		self.extra.update()
		
		self.aliens.update(self.alien_direction)
		self.alien_position_checker()
		self.extra_alien_timer()
		self.collision_checks()
		
		self.player.sprite.lasers.draw(self.screen)
		self.player.draw(self.screen)
		self.blocks.draw(self.screen)
		self.aliens.draw(self.screen)
		self.alien_lasers.draw(self.screen)
		self.extra.draw(self.screen)
		self.display_lives()
		self.display_score()

	def resetgame(self):
		self.aliens.empty()
		self.alien_lasers.empty()
		self.extra.empty()
		self.player.sprite.lasers.empty()
		self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = 45, y_start = 480)
		self.alien_setup(rows = 5, cols = 6)
		self.lives = 3
		self.score = 0

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

def map1(screen, width, height, clock):
	background = pygame.transform.scale(pygame.image.load(f'picture\\background.webp').convert_alpha(), (1020, height))
	ALIENLASER = pygame.USEREVENT + 1
	pygame.time.set_timer(ALIENLASER,800)
	game = Game(screen, width, height, clock)
	crt = CRT(screen, width, height)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == ALIENLASER:
				game.alien_shoot()

		screen.blit(background, (0,0))
		game.run()
		if game.endgame:
			return True
		crt.draw()  
		pygame.display.flip()
		clock.tick(60)


	