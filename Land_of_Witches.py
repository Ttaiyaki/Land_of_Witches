import pygame
from pygame.locals import *
import math
import random

#เรียกlibraryเริ่มต้นทำงาน
pygame.init()

#สร้างตัวแปรตั้งเวลา
clock = pygame.time.Clock()

#ตัวตั้งเวลาใน PyGame เป็นส่วนนของการทำงานเพื่อให้มีการอัพเดตหน้าจอตามอัตราการแสดงภาพ (frame rate) ต่อ 1 วินาที หรือที่เรียกว่า fps (frames per second)
fps = 60

#กำหนดขนาดหน้าจอ
screen_width = 1000
screen_height = 600

#แสดงหน้าจอขนาด 800x600
screen = pygame.display.set_mode((screen_width, screen_height))
#titleหน้าจอ
pygame.display.set_caption('Land of Witches')

#โหลดรูปภาพ
bg = pygame.image.load('img/bg.jpg')
ground_img = pygame.image.load('img/new_ground.png')
ground_width = ground_img.get_width()
re_button_img = pygame.image.load('img/restart.png')
over_button_img = pygame.image.load('img/imggameover.png')
start_button_img = pygame.image.load('img/start.png')

#เพิ่มเสียง
bgm_sound = pygame.mixer.music.load('sound/ghost-waltz-120538.mp3')
pygame.mixer.music.play(-1)
jump_sfx = pygame.mixer.Sound('sound/jumping-2043.wav')
over_sfx = pygame.mixer.Sound('sound/game-over-213.wav')
restart_sfx = pygame.mixer.Sound('sound/restart-212.wav')

#ตัวแปรกำหนดฟอนต์และขนาด (Fonts and Size)
font = pygame.font.SysFont('Bauhaus 93', 60)

#ตัวแปรกำหนดสีฟอนต์ (Font's color)
white = (255, 255, 255)


#กำหนดตัวแปรภายในเกม
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
hasPlayedGameOverSound = False
obstable_gap = 150
obstacle_frequency = 1500 #milliseconds
last_obstacle = pygame.time.get_ticks() - obstacle_frequency

#การตั้งค่าคะแนนให้เป็น 0 ตอนแรกเริ่ม 
#และเพิ่มตัว trigger เข้ามาสำหรับการนับคะแนน
score = 0
pass_pipe = False


tiles = math.ceil(screen_width / ground_width) + 1
print(tiles)

#Function ฟอนต์ (Font) 
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def reset_game():
    obstacle_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    return score
    
#สร้างตัวละคร
class Witch(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		#สร้าง loop เพื่อให้ตัวละครขยับได้
		for num in range(1, 4):
			img = pygame.image.load(f'img/witch{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	def update(self):
		if flying == True:
			#gravity
			self.vel += 0.5
			#ถ้าโดดเกินความสูงของหน้าจอ8 จะโดดไม่สูงสุดเกิน 8
			if self.vel > 8:
				self.vel = 8
			#ถ้าล้นลงเกินความสูงของหน้าจอ540 จะล้นไม่เกิน 540
			if self.rect.bottom < 540:
				self.rect.y += int(self.vel)

		if game_over == False:
			#กระโดด
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -7
				jump_sfx.play()
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			#handle the animation
			self.counter += 1
			flap_cooldown = 5

			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]
		
			#rotate the witch
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -1)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)


class obstacle(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('img/wood.png')
		self.rect = self.image.get_rect()
		#position 1 is from the top(อุปสรรคอยู่ด้านบน), -1 is from the bottom(อุปสรรคอยู่ด้านล่าง)
		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(obstable_gap / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(obstable_gap / 2)]

	def update(self):
		self.rect.x -= scroll_speed
		if self.rect.right < 0:
			self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    def draw(self):
        action = False
        #ตำแหน่งของmouse
        pos = pygame.mouse.get_pos()
        
        #check ว่า mouse อยู่ตรงปุ่มไหม
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        #สร้างปุ่ม
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        return action

witch_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()


flappy = Witch(100, int(screen_height / 2))

witch_group.add(flappy)

#สร้างปุ่ม start
button_start = Button(screen_width // 2 - 190, screen_height // 2 - 100, start_button_img)

#สร้างปุ่ม game over
button_gameover = Button(screen_width // 2 - 410, screen_height // 2 - 180, over_button_img)

#สร้างปุ่ม restart
button_restart = Button(screen_width // 3 - (-40), screen_height // 1 - 200, re_button_img)

run = True
while run:
	screen.blit(bg, (0,0))
	button_start.draw()

	for event in pygame.event.get():
		#คำสั่งปิดการทำงานของpygame
		if event.type == QUIT:
			pygame.quit()

		#เมื่อกดปุ่ม start จะเริ่มเล่นเกม
		if event.type == pygame.MOUSEBUTTONDOWN:
			if button_start.draw() == True:
				run = True

				while run:
					#กำหนดอัตราการแสดงผล fps = 60 frame / 1 second
					clock.tick(fps)

					#draw background
					screen.blit(bg, (0,0))

					witch_group.draw(screen) #
					witch_group.update() #
					obstacle_group.draw(screen) #

					#draw and scroll the ground
					for i in range(0, tiles):
						screen.blit(ground_img, (i * ground_width + ground_scroll, 540))

					#การเช็คคะแนน
					#โดยการเช็คจะแนนจะเริ่มทำงานตอนที่มีอุปสรรคปรากฎขึ้นมาบนจอของผู้เล่น
					if len(obstacle_group) > 0:
						#เป็นการเช็คว่าตัวของแม่มดเคลื่อนที่ถึงตัวอุปสรรคแล้วหรือยัง
						if witch_group.sprites()[0].rect.right < obstacle_group.sprites()[0].rect.right\
							and pass_pipe == False:
							pass_pipe = True
						if pass_pipe == True:
							#แต่ตัวคะแนนจะนับเพิ่ม 1คะแนน ก็ต่อเมื่อระยะทางด้านซ้ายของตัวแม่มดนั้นเคลื่อนผ่านบริเวณด้านขวาของตัวอุปสรรคแล้วเท่านั้น
							if witch_group.sprites()[0].rect.left > obstacle_group.sprites()[0].rect.right:
								score += 1
								pass_pipe = False

					#ตำแหน่งของฟอนต์ (Font's position)
					draw_text(str(score), font, white, int(screen_width / 2), 20)

					#look for collision
					if pygame.sprite.groupcollide(witch_group, obstacle_group, False, False) or flappy.rect.top < 0:
						game_over = True

					#check if witch hit the ground
					if flappy.rect.bottom >= 540:
						game_over = True
						flying = False

					if game_over == False and flying == True:
						#generate new obstacles
						time_now = pygame.time.get_ticks()
						if time_now - last_obstacle > obstacle_frequency:
							obstacle_height = random.randint(-100, 100)
							btm_obstacle = obstacle(screen_width, int(screen_height / 2) + obstacle_height, -1)
							top_obstacle = obstacle(screen_width, int(screen_height / 2) + obstacle_height, 1)
							obstacle_group.add(btm_obstacle)
							obstacle_group.add(top_obstacle)
							last_obstacle = time_now

						#scroll ground_img
						ground_scroll -= scroll_speed
						#reset scroll
						if abs(ground_scroll) > ground_width:
							ground_scroll = 0

						obstacle_group.update()
				
					#check ว่า game over แล้ว reset
					if game_over == True:
						if not hasPlayedGameOverSound:
							over_sfx.play()
							hasPlayedGameOverSound = True
						button_gameover.draw()
						if button_restart.draw() == True:
							game_over = False
							score = reset_game()
							restart_sfx.play()
							hasPlayedGameOverSound = False
				
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							run = False
						if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
							flying = True

					pygame.display.update()
	pygame.display.update()
