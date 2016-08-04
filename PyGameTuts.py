import pygame

white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)
grey = pygame.Color(100, 100, 100)
silver = pygame.Color(200, 200, 200)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

class Block(pygame.sprite.Sprite):

	def __init__(self, color=blue, width=64, height=64):
		super(Block, self).__init__()
		self.image = pygame.Surface((width, height))
		self.image.fill(color)
		self.hspeed = 0
		self.vspeed = 0
		self.set_properties()

	def set_position(self, x, y):
		self.rect.x = x
		self.rect.y = y

	def snap_to(self, loc_lst):
		def dist(x, y): #distace formula sans the sqrt
			return ((self.rect.x - x) ** 2 + (self.rect.y - y) ** 2)

		c_point = None
		min_d = float("INF")
		for item in loc_lst:
			d = dist(item[0], item[1])
			if d < min_d:
				c_point = item
				min_d = d
		if c_point:
			self.rect.x = c_point[0]
			self.rect.y = c_point[1]

	def set_image(self, filename=None):
		if filename:
			self.image = pygame.image.load(filename)
			self.set_properties()

	def set_properties(self):
		self.rect = self.image.get_rect()
		self.origin_x = self.rect.centerx
		self.origin_y = self.rect.centery

	def change_speed(self, hspeed, vspeed):
		self.hspeed += hspeed
		self.vspeed += vspeed

	def update(self, collidable=pygame.sprite.Group(), x_offset=0, y_offset=0):
		mouse_x, mouse_y = pygame.mouse.get_pos()
		colliding_left = colliding_right = colliding_up = colliding_down = False

		self.rect.x += self.hspeed
		
		collision_list = pygame.sprite.spritecollide(self, collidable, False)

		for thing in collision_list:
			if thing is self: continue
			if self.hspeed > 0:
				#Right Direction
				self.rect.right = thing.rect.left
				colliding_right = True
			if self.hspeed < 0:
				#Left Direction
				self.rect.left = thing.rect.right
				colliding_left = True

		self.rect.y += self.vspeed

		collision_list = pygame.sprite.spritecollide(self, collidable, False)

		for thing in collision_list:
			if thing is self: continue
			if self.vspeed > 0:
				#Down Direction
				self.rect.bottom = thing.rect.top
				colliding_down = True
			if self.vspeed < 0:
				#Up Direction
				self.rect.top = thing.rect.bottom
				colliding_up = True

		change = mouse_x - self.rect.x - x_offset
		if colliding_left:
			if change > 0:
				self.hspeed = change
		elif colliding_right:
			if change < 0:
				self.hspeed = change
		else:
			self.hspeed = change

		change = mouse_y - self.rect.y - y_offset
		if colliding_up:
			if change > 0:
				self.vspeed = change
		elif colliding_down:
			if change < 0:
				self.vspeed = change
		else:
			self.vspeed = change

#if (__name__ == "__main__"):
pygame.init()

#Create and setup window
window_size = window_width, window_height = 640, 480
window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
pygame.display.set_caption("Klotski")

window.fill(white)

#Set up clock for framerate
clock = pygame.time.Clock()
f_p_s = 60

#Adds sprites to a sprite group and draws them to the window
block_group = pygame.sprite.Group()
a_block = Block(blue, 64, 128)
a_block.set_image("facetall.png")
a_block.set_position(10, 10)

win_block = Block(red, 128, 128)
win_block.set_image("face128.png")
win_block.set_position(74, 10)

b_block = Block(green, 64, 128)
b_block.set_image("facetall.png")
b_block.set_position(202, 10)

c_block = Block(grey, 64, 128)
c_block.set_image("facetall.png")
c_block.set_position(10, 138)

d_block = Block(silver, 128, 64)
d_block.set_image("facewide.png")
d_block.set_position(74, 138)

e_block = Block(black, 64, 128)
e_block.set_image("facetall.png")
e_block.set_position(202, 138)

f_block = Block(black, 64, 64)
f_block.set_image("face.png")
f_block.set_position(10, 266)

g_block = Block(black, 64, 64)
g_block.set_image("face.png")
g_block.set_position(202, 266)

h_block = Block(black, 64, 64)
h_block.set_image("face.png")
h_block.set_position(74, 202)

i_block = Block(black, 64, 64)
i_block.set_image("face.png")
i_block.set_position(138, 202)	

board_locs = [(10, 10), (10, 74), (10, 138), (10, 202), (10, 266),
			  (74, 10), (74, 74), (74, 138), (74, 202), (74, 266),
			  (138, 10), (138, 74), (138, 138), (138, 202), (138, 266),
			  (202, 10), (202, 74), (202, 138), (202, 202), (202, 266)]

block_group.add(a_block, b_block, c_block, d_block, \
	e_block, win_block, f_block, g_block, h_block, i_block)

top_side = Block(black, 257, 1)
top_side.set_position(10, 9)

bottom_side = Block(black, 257, 1)
bottom_side.set_position(10, 330)

left_side = Block(black, 1, 322)
left_side.set_position(9, 9)

right_side = Block(black, 1, 320)
right_side.set_position(266, 10)

board_group = pygame.sprite.Group()
board_group.add(top_side, bottom_side, left_side, right_side)

block_group.draw(window)
board_group.draw(window)

collidable_blocks = pygame.sprite.Group()
for block in block_group:
	collidable_blocks.add(block)
for block in board_group:
	collidable_blocks.add(block)

#Sound for fun!
start_sound = pygame.mixer.Sound("bwaa.wav")
start_sound.play()

#Fonts and text rendering!
font = pygame.font.SysFont("Times New Roman, Arial", 30)
message = "A shitty version of Klotski!"
text = font.render(message, True, black)
text_place = 300, 40

Target = None
mouse_press = mouse_up = mouse_down = False
x_offset = y_offset = 0
previous_pos = (0, 0)

running = True

while running:

	mousex, mousey = pygame.mouse.get_pos()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_press = True
			mouse_down = True
		if event.type == pygame.MOUSEBUTTONUP:
			mouse_up = True
			mouse_down = False

	if mouse_press:
		for item in block_group: # search all items
			if mousex >= (item.rect.x) and \
	                mousex <= (item.rect.x + item.rect.width) and \
	                mousey >= (item.rect.y) and \
	                mousey <= (item.rect.y + item.rect.height) : # inside the bounding box
				Target = item # "pick up" item
				x_offset = mousex - item.rect.x
				y_offset = mousey - item.rect.y
				previous_pos = (item.rect.x, item.rect.y)


	if mouse_up and Target:
		Target.hspeed = 0
		Target.vspeed = 0
		if Target.rect.x < 10 or Target.rect.x > 265 \
				or Target.rect.y < 10 or Target.rect.y > 329:
			Target.rect.x = previous_pos[0]
			Target.rect.y = previous_pos[1]
		else:
			Target.snap_to(board_locs)
		Target = None

	clock.tick(f_p_s)

	if mouse_down and Target:
		Target.update(collidable_blocks, x_offset, y_offset)

	mouse_press = False
	mouse_up = False

	window.fill(white)
	
	block_group.draw(window)
	board_group.draw(window)

	window.blit(text, text_place)

	pygame.display.update()

pygame.quit()

