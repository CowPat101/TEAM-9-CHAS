import pygame
import time

clock = pygame.time.Clock()

pygame.init()

display_width = 800
display_height = 600

s1 = pygame.mixer.Sound("placeholder sounds/beep1.ogg")
s2 = pygame.mixer.Sound("placeholder sounds/beep2.ogg")
s3 = pygame.mixer.Sound("placeholder sounds/beep3.ogg")
s4 = pygame.mixer.Sound("placeholder sounds/beep4.ogg")
s5 = pygame.mixer.Sound("placeholder sounds/beep5.ogg")

pause = False

def quitgame():
	pygame.quit()
	quit()

def loop():
	paused = False
	
	pygame.mixer.music.load("placeholder sounds/simple-loop.ogg")
	pygame.mixer.music.play(-1)
	
	while not paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					pygame.mixer.Sound.play(s1)
				if event.key == pygame.K_s:
					pygame.mixer.Sound.play(s2)
				if event.key == pygame.K_d:
					pygame.mixer.Sound.play(s3)
				if event.key == pygame.K_f:
					pygame.mixer.Sound.play(s4)
				if event.key == pygame.K_g:
					pygame.mixer.Sound.play(s5)
				if event.key == pygame.K_p:
					if paused:
						pygame.mixer.music.unpause()
					if not paused:
						pygame.mixer.music.pause()
		
		pygame.display.update()
		clock.tick(240)

pygame.display.set_mode((display_width,display_height))
loop()
