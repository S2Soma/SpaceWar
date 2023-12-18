import pygame
import sys
from level1 import map1, CRT
from level2 import map2
from level3 import map3
def start_game(screen, width, height, clock):
	music = pygame.mixer.Sound('audio/music.wav')
	music.set_volume(0.1)
	music.play(loops = -1)
	crt = CRT(screen, width, height)
	background = pygame.transform.scale(pygame.image.load(f'picture\\background.webp').convert_alpha(), (1020, height))
	btStartGame = pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Start game", False,'white')
	btSGrect = btStartGame.get_rect(center = ((width//2, height//2 + btStartGame.get_height())))
	title = pygame.font.Font(f'font\\Pixeled.ttf',60).render(f"name", False,'white')
	recttitle = title.get_rect(center = (width//2, 0))
	while True:
		if recttitle.y < 100:
			recttitle.y += 2
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		if btSGrect.collidepoint(pygame.mouse.get_pos()):
			btStartGame = pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Start game", False,'red')
			if pygame.mouse.get_pressed(num_buttons=3)[0]:
				if map1(screen, width, height, clock):
					if map2(screen, width, height, clock):
						if map3(screen, width, height, clock):
							endgame(screen, width, height, clock)
		else:
			btStartGame = pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Start game", False,'white')
		screen.blit(background, (0,0))
		screen.blit(title, recttitle)
		screen.blit(btStartGame, btSGrect)
		crt.draw()
		pygame.display.update()
		clock.tick(60)

def endgame(screen, width, height, clock):
	crt = CRT(screen, width, height)
	background = pygame.transform.scale(pygame.image.load(f'picture\\background.webp').convert_alpha(), (1020, height))
	text = []
	text_rect = []
	text.append(pygame.font.Font(f'font\\Pixeled.ttf',35).render(f"CONGRATULATIONS!", False,'white'))
	text_rect.append(text[0].get_rect(center = (width//2, 0)))
	text.append(pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Game developers: ", False,'white'))
	text_rect.append(text[0].get_rect(center = (width//2+ 30, height)))
	text.append(pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Phan Hoang Minh", False,'white'))
	text_rect.append(text[0].get_rect(center = (width//2+ 30, height + 50)))
	text.append(pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Vo Le Men", False,'white'))
	text_rect.append(text[0].get_rect(center = (width//2+ 30, height + 100)))
	text.append(pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Do Dinh Nam", False,'white'))
	text_rect.append(text[0].get_rect(center = (width//2+ 30, height + 150)))
	text.append(pygame.font.Font(f'font\\Pixeled.ttf',20).render(f"Friend M", False,'white'))
	text_rect.append(text[0].get_rect(center = (width//2 + 30, height + 200)))
	btreturn = pygame.font.Font(f'font\\Pixeled.ttf',10).render(f"Return", False,'white')
	btRTrect = btreturn.get_rect(center = ((width - 100, height + 200)))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
		screen.blit(background, (0,0))
		for i in range(len(text)):
			if i == 0:
				if text_rect[i].y < 150:
					text_rect[i].y += 2
			else:
				if text_rect[i].y > height/2 - 50 + (i - 1)*50:
					text_rect[i].y -= 2
			screen.blit(text[i], text_rect[i])
		if btRTrect.y > height - 50:
			btRTrect.y -= 2
		if btRTrect.collidepoint(pygame.mouse.get_pos()):
			btreturn = pygame.font.Font(f'font\\Pixeled.ttf',15).render(f"Return", False,'red')
			if pygame.mouse.get_pressed(num_buttons=3)[0]:
				return
		else:
			btreturn = pygame.font.Font(f'font\\Pixeled.ttf',15).render(f"Return", False,'white')
		screen.blit(btreturn, btRTrect)
		crt.draw()
		pygame.display.update()
		clock.tick(60)
if __name__ == '__main__':
	pygame.init()
	screen_width = 600
	screen_height = 600
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	start_game(screen, screen_width, screen_height, clock)
	  