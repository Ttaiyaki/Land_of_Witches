import pygame
from pygame.locals import *
import math
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

#load images
bg = pygame.image.load('img/bg.jpg')
ground_img = pygame.image.load('img/new_ground.png')
ground_width = ground_img.get_width()

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
tiles = math.ceil(screen_width / ground_width) + 1
print(tiles)

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
				self.vel = -10
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

witch_group = pygame.sprite.Group()

flappy = Witch(100, int(screen_height / 2))

witch_group.add(flappy)


run = True
while run:
    #กำหนดอัตราการแสดงผล fps = 60 frame / 1 second
	clock.tick(fps)

	#draw background
	screen.blit(bg, (0,0))

	witch_group.draw(screen) #
	witch_group.update() #

#draw and scroll the ground
	for i in range(0, tiles):
		screen.blit(ground_img, (i * ground_width + ground_scroll, 540))

	#check if witch hit the ground
	if flappy.rect.bottom > 540:
		game_over = True
		flying = False

	if game_over == False:
	#scroll ground_img
		ground_scroll -= scroll_speed
		#reset scroll
		if abs(ground_scroll) > ground_width:
			ground_scroll = 0


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	pygame.display.update()
#คำสั่งปิดการทำงานของpygame
pygame.quit()
