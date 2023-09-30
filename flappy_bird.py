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
ground_img = pygame.image.load('img/dry_bush_ground_v2.png')
ground_width = ground_img.get_width()

#define game variables
ground_scroll = 0
scroll_speed = 4
tiles = math.ceil(screen_width / ground_width) + 1
print(tiles)


run = True
while run:
    #กำหนดอัตราการแสดงผล fps = 60 frame / 1 second
	clock.tick(fps)

	#draw background
	screen.blit(bg, (0,0))

	#draw and scroll the ground
	for i in range(0, tiles):
		screen.blit(ground_img, (i * ground_width + ground_scroll, 400))

	#scroll ground_img
	ground_scroll -= scroll_speed

	#reset scroll
	if abs(ground_scroll) > ground_width:
		ground_scroll = 0


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()
#คำสั่งปิดการทำงานของpygame
pygame.quit()