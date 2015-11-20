import pygame, random, math

BUTTON_FONTNAME = "consolas"
BUTTON_FONTSIZE = 14
BUTTON_RECT_SIZE = pygame.Rect([20,20,80,20])

MAP_FONTNAME = "courier"
MAP_FONTSIZE = 14

MAP_TILE_SIZE = (16,16)
MAP_MARIGIN = 3

BASE_MAP_OFFSET_Y = 80

COLOR_KEY_SKIP = (128, 128, 128, 255)

clickable_rectangles = []
button_grid = []

class Color:

	def __init__(self):
		self.black = (0, 0, 0, 255)
		self.white = (255, 255, 255, 255)

		self.red = (255, 0, 0, 255)
		self.green = (0, 255, 0, 255)
		self.blue = (0, 0, 255, 255)
		self.grey = (79, 79, 79, 255)

		self.yellow = (255,255,0, 255)

		self.light_red = (255, 204, 204, 255)
		self.s_light_blue = (204, 229, 255, 255)
		self.s_light_grey = (224,224,224, 255)
		self.s_light_green = (105, 255, 84, 255)

		self.dark_blue = (0, 0, 183, 255)
		self.dark_grey = (23, 23, 23, 255)

		self.dark_green = (0, 128, 0, 255)


class Buttons:
	myfont = None

	def clicked(self, event, rect):
		# Use the Rectangle object from PYGAME

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			if rect.collidepoint(mouse_pos):
				return True
		else:
			return False

	# Event handling for clicking
	def functions_event_handling(self, event, world):
		global button_grid

		if self.clicked(event, self.newWorldButton.rect):
			print "Click!"
			world.allPlains()
		if self.clicked(event, self.loadWorldButton.rect):
			print "*le Click!"
			world.load()
		if self.clicked(event, self.saveWorldButton.rect):
			print "*DAS CLICKSTEIN"
			world.save()

		if self.clicked(event, self.redButton.rect):
			self.red_button_clicked()

		if self.clicked(event, self.greenButton.rect):
			self.green_button_clicked()

		if self.clicked(event, self.blueButton.rect):
			self.blue_button_clicked()

		if self.clicked(event, self.applyColor.rect):
			c = self.rgb
			brute_force_colorize(self.currentMapTile, (c[0], c[1], c[2], c[3]))
			self.currentTileColored = True


		if self.clicked(event, self.plusOne.rect):
			if self.rgb[self.modify_which_color_value] + 1 <= 255:
				self.rgb[self.modify_which_color_value] += 1
		if self.clicked(event, self.plusTen.rect):
			if self.rgb[self.modify_which_color_value] + 10 <= 255:
				self.rgb[self.modify_which_color_value] += 10

		if self.clicked(event, self.minusOne.rect):
			if self.rgb[self.modify_which_color_value] -1 >= 0:
				self.rgb[self.modify_which_color_value] -= 1
		if self.clicked(event, self.minusTen.rect):
			if self.rgb[self.modify_which_color_value] -10 >= 0:
				self.rgb[self.modify_which_color_value] -= 10

		if self.clicked(event, self.floorTiles.rect):
			button_grid = []

			self.currentGrid = world.floor_tiles
			self.currentDrawGrid = world.grid

			self.floorTiles.backColor = self.c.light_red
			self.otherTiles.backColor = self.c.dark_blue

			self.floorTiles.textColor = self.c.black
			self.otherTiles.textColor = self.c.white

		if self.clicked(event, self.otherTiles.rect):
			button_grid = []

			self.currentGrid = world.other_tiles
			self.currentDrawGrid = world.entities_grid

			self.floorTiles.backColor = self.c.dark_blue
			self.otherTiles.backColor = self.c.light_red

			self.floorTiles.textColor = self.c.white
			self.otherTiles.textColor = self.c.black

	def __init__(self, world):
		self.c = Color()

		self.myfont = pygame.font.SysFont(BUTTON_FONTNAME, BUTTON_FONTSIZE)

		self.currentMapTile = world.graphics[random.randint(0, len(world.graphics))]
		self.currentTileColored = False
		self.currentTileId = 0

		self.currentTileCopy = self.currentMapTile.copy()
		self.modify_which_color_value = 0
		self.currentColor = (255, 255, 255)

		self.currentGrid = world.floor_tiles
		self.currentDrawGrid = world.grid

		# Using a list because 'tuple' doesn't support assingment
		self.rgb = [255, 255, 255, 255]

		# ADD BUTTONS HERE - Define button properties here. Also add them to "draw_all()"
		self.newWorldButton = SmallButton(self, "New world", 30,20)
		self.loadWorldButton = SmallButton(self, "Load world", 150, 20)
		self.saveWorldButton = SmallButton(self, "Save world", 270, 20)

		self.redButton = SmallButton(self, "Red " + str(self.rgb[0]), 1025, 450, backColor=self.c.dark_blue, textColor=self.c.white)
		self.greenButton = SmallButton(self, "Green " + str(self.rgb[1]), 1025, 500, backColor=self.c.dark_blue, textColor=self.c.white)
		self.blueButton = SmallButton(self, "Blue " + str(self.rgb[2]), 1025, 550, backColor=self.c.dark_blue, textColor=self.c.white)

		self.plusOne = SmallButton(self, "+1", 1270, 430, backColor=self.c.dark_blue, textColor=self.c.white)
		self.plusTen = SmallButton(self, "+10", 1270, 470, backColor=self.c.dark_blue, textColor=self.c.white)
		self.minusOne = SmallButton(self, "-1", 1270, 530, backColor=self.c.dark_blue, textColor=self.c.white)
		self.minusTen = SmallButton(self, "-10", 1270, 570, backColor=self.c.dark_blue, textColor=self.c.white)

		self.applyColor = SmallButton(self, "Apply Color", 1143, 585, backColor=self.c.dark_blue, textColor=self.c.white)

		self.floorTiles = SmallButton(self, "Floor Tiles", 1050, 100, backColor=self.c.dark_blue, textColor=self.c.white, buttonSizeX=110)
		self.otherTiles = SmallButton(self, "Other Tiles", 1200, 100, backColor=self.c.dark_blue, textColor=self.c.white, buttonSizeX=110)

		#self.brushDraw = SmallButton(self, "Brush draw", 1030,670, backColor=c.dark_blue, textColor=c.white)
		#self.rektDraw = SmallButton(self, "Rect draw", 1030,710, backColor=c.dark_blue, textColor=c.white)

	def draw_all(self, display):
		self.drawButton(self.newWorldButton, display)
		self.drawButton(self.loadWorldButton, display)
		self.drawButton(self.saveWorldButton, display)

		self.drawButton(self.redButton, display)
		self.drawButton(self.greenButton, display)
		self.drawButton(self.blueButton, display)

		self.drawButton(self.plusOne, display)
		self.drawButton(self.plusTen, display)
		self.drawButton(self.minusOne, display)
		self.drawButton(self.minusTen, display)

		self.drawButton(self.applyColor, display)

		self.drawButton(self.floorTiles, display)
		self.drawButton(self.otherTiles, display)

		#self.drawButton(self.brushDraw, display)
		#self.drawButton(self.rektDraw, display)

	def drawButton(self, smallButton, display):
		display.fill(smallButton.backColor, smallButton.rect)
		display.blit(smallButton.font, (smallButton.font_locationX, smallButton.font_locationY))

	def priview_current_color(self, display, posX, posY):
		c = self.rgb
		display.fill((c[0], c[1], c[2]), [posX, posY, 64, 64])

	def update_button_text(self):
		self.redButton.font = self.redButton.buttonInstance.myfont.render("Red " + str(self.rgb[0]), 1, self.redButton.textColor)
		self.greenButton.font = self.greenButton.buttonInstance.myfont.render("Green " + str(self.rgb[1]), 1, self.greenButton.textColor)
		self.blueButton.font = self.blueButton.buttonInstance.myfont.render("Blue " + str(self.rgb[2]), 1, self.blueButton.textColor)

		self.floorTiles.font = self.floorTiles.buttonInstance.myfont.render(self.floorTiles.text, 1, self.floorTiles.textColor)
		self.otherTiles.font = self.otherTiles.buttonInstance.myfont.render(self.otherTiles.text, 1, self.otherTiles.textColor)

	def red_button_clicked(self):
		self.modify_which_color_value = 0

		self.redButton.backColor = self.c.light_red
		self.greenButton.backColor = self.c.dark_blue
		self.blueButton.backColor = self.c.dark_blue

		self.redButton.textColor = self.c.black
		self.greenButton.textColor = self.c.white
		self.blueButton.textColor = self.c.white

	def green_button_clicked(self):
		self.modify_which_color_value = 1

		self.redButton.backColor = self.c.dark_blue
		self.greenButton.backColor = self.c.light_red
		self.blueButton.backColor = self.c.dark_blue

		self.redButton.textColor = self.c.white
		self.greenButton.textColor = self.c.black
		self.blueButton.textColor = self.c.white

	def blue_button_clicked(self):
		self.modify_which_color_value = 2

		self.redButton.backColor = self.c.dark_blue
		self.greenButton.backColor = self.c.dark_blue
		self.blueButton.backColor = self.c.light_red

		self.redButton.textColor = self.c.white
		self.greenButton.textColor = self.c.white
		self.blueButton.textColor = self.c.black


class SmallButton:
	# Class variables:
	# font, rect, text, locationX, locationY, textColor, backColor, font_locationX, font_locationY

	def __init__(self, buttonInstance, text, locationX, locationY, font_locationX = 0, font_locationY = 0, backColor = (255, 204, 204), textColor = (0, 0, 0), buttonSizeX = 100, buttonSizeY = 30):
		self.text = text
		self.buttonInstance = buttonInstance

		self.textColor = textColor
		self.backColor = backColor

		self.font = buttonInstance.myfont.render(self.text, 1, textColor)

		self.rect = pygame.Rect(locationX, locationY, buttonSizeX, buttonSizeY)

		# Default text position
		if font_locationX == 0:
			self.font_locationX = locationX + 10
		else:
			self.font_locationX = font_locationX

		if font_locationY == 0:
			self.font_locationY = locationY + 8
		else:
			self.font_locationY = font_locationY


def event_handling(button, world):
	mouse_drag_to_draw(world, button)
	button.update_button_text()
	button.currentTileCopy = button.currentMapTile.copy()

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			# This is what the buttons do
			button.functions_event_handling(event, world)
			choose_current_tile(world, button)

			world.mouse_button_down = True

		if event.type == pygame.MOUSEBUTTONUP:
			world.mouse_button_down = False


def mouse_drag_to_draw(world, button):
	c = button.rgb

	if world.mouse_button_down:
		mouse_pos = pygame.mouse.get_pos()
		mouse_rekt = pygame.Rect(mouse_pos, (2,2))

		result = mouse_rekt.collidelist(clickable_rectangles)
		if result != -1:
			if result == 0:
				button.currentDrawGrid[0][0] = button.currentMapTile

				if button.currentDrawGrid == world.entities_grid:
					world.tileInfo_grid[0][0].entity_id = button.currentTileId
					if button.currentTileColored:
						world.tileInfo_grid[0][0].entity_color = (c[0], c[1], c[2], c[3])

				else:
					world.tileInfo_grid[0][0].grid_id = button.currentTileId
					world.tileInfo_grid[0][0].is_grass = False
					if button.currentTileColored:
						world.tileInfo_grid[0][0].color = (c[0], c[1], c[2], c[3])
					elif not button.currentTileColored and world.tileInfo_grid[0][0].is_grass:
						world.tileInfo_grid[0][0].color = Color().s_light_green

			else:
				x = int(result/world.sizeX)
				y = result % world.sizeX

				button.currentDrawGrid[x][y] = button.currentMapTile

				if button.currentDrawGrid == world.entities_grid:
					world.tileInfo_grid[x][y].entity_id = button.currentTileId
					if button.currentTileColored:
						world.tileInfo_grid[x][y].entity_color = (c[0], c[1], c[2], c[3])

				else:
					world.tileInfo_grid[x][y].is_grass = False
					world.tileInfo_grid[x][y].grid_id = button.currentTileId
					if button.currentTileColored:
						world.tileInfo_grid[x][y].color = (c[0], c[1], c[2], c[3])



def choose_current_tile(world, button):
	mouse_pos = pygame.mouse.get_pos()
	mouse_rekt = pygame.Rect(mouse_pos, (1,1))

	result = mouse_rekt.collidelist(button_grid)
	if result is not -1:
		if result == 0:
			button.currentMapTile = button.currentGrid[0].copy()
			button.currentTileId = 0
			button.currentTileColored = False
		else:
			button.currentMapTile = button.currentGrid[result].copy()
			button.currentTileId = result
			button.currentTileColored = False

def drawWorld(display, world, color):

	posX = 20
	posY = BASE_MAP_OFFSET_Y

	for x in range (0, len(world.grid)):
		for y in range (0, len(world.grid[x])):
			posY += MAP_TILE_SIZE[1]

			rect = pygame.Rect(posX, posY, MAP_TILE_SIZE[0], MAP_TILE_SIZE[1])

			hundred_square(world, posX, posY)
			display.blit(world.grid[x][y], rect)
			if str(type(world.entities_grid[x][y])) == "<type 'pygame.Surface'>":
				display.blit(world.entities_grid[x][y], rect)

		posY = BASE_MAP_OFFSET_Y
		posX += MAP_TILE_SIZE[0]

# Colliders for the map_editor itself.
def hundred_square(world, posX, posY):
	rekt = pygame.Rect([posX-3, posY+2,MAP_TILE_SIZE[0], MAP_TILE_SIZE[1]-1])
	if len(clickable_rectangles) < world.sizeX * world.sizeY:
		clickable_rectangles.append(rekt)


# Colliders for the BUTTONS in the map_editor.
def clickable_button_grid(posX, posY, sizeX, sizeY, grid_length):
	if len(button_grid) < grid_length:
		rekt = pygame.Rect([posX, posY, sizeX, sizeY])
		button_grid.append(rekt)


def draw_button_grid(display, grid, posX, posY, sizeX, sizeY, marigin):
	old_pos_y = posY

	i = 0

	if is_square(len(grid)):
		grid_size = int(math.sqrt(len(grid)))
	else:
		grid_size = int(math.sqrt(len(grid))) + 1

	for x in range (0, grid_size):
		for y in range (0, grid_size):
			if i <= len(grid):
				try:
					rekt = [posX, posY, sizeX, sizeY]
					clickable_button_grid(posX, posY, sizeX, sizeY, len(grid))
					display.blit(grid[x*grid_size + y], rekt)
					posY += sizeY + marigin
				except IndexError:
					break
			else:
				break
		posX += sizeX + marigin
		posY = old_pos_y


def current_button_preview(display, button, posX, posY):
	priview = pygame.Surface([64,64])
	pygame.transform.scale(button.currentMapTile, (64, 64), priview)
	display.blit(priview, [posX,posY,16,16])

def brute_force_colorize(surface, target_color):
	for x in range (surface.get_size()[0]):
		for y in range (surface.get_size()[1]):
			current_color = surface.get_at([x, y])
			if current_color[0] is not 128 and current_color[1] is not 128 and current_color[2] is not 128:
				alpha_percent = current_color[3]*100/255
				white_intensity = []
				white_intensity.append(current_color[0]*100/255)
				white_intensity.append(current_color[1]*100/255)
				white_intensity.append(current_color[2]*100/255)

				new_color = [0,0,0,0]

				for i in range(0,3):
					new_color[i] = target_color[i] * white_intensity[i]/100 * alpha_percent/100
				new_color[3] = current_color[3]  # set alpha

				surface.set_at([x,y], new_color)
			else:
				banana = 5


def is_square(apositiveint):
	x = apositiveint//2
	seen = set([x])
	while x * x is not apositiveint:
		x = (x + (apositiveint //2)) // 2
		if x in seen: return False
		seen.add(x)
	return True

def remove_bad_pixels(tile_surface, remove_color):
	for x in range (tile_surface.get_size()[0]):
		for y in range (tile_surface.get_size()[1]):
			current_color = tile_surface.get_at((x,y))
			if current_color[0] == remove_color[0] and current_color[1] == remove_color[1] and current_color[2] == remove_color[2]:
				tile_surface.set_at((x,y), (current_color[0]-1, current_color[1]-1, current_color[2]-1, 255))
			else:
				banana = 5

def make_completely_transparent(surface, colorkey = (128,128,128,255)):
	for x in range (surface.get_size()[0]):
		for y in range (surface.get_size()[1]):
			surface.set_at((x,y), colorkey)

"""

!!!!!!!!!!
UNUSED METHODS. THERE FOR SAFEKEEPING
!!!!!!!!!!

"""

def color_surface(surface, red, green, blue):
	# Took this from StackOverflow. Link to post: -put link here-
	arr = pygame.surfarray.pixels3d(surface)
	print arr[2,2,2]
	arr[:,:,0] = red
	arr[:,:,1] = green
	arr[:,:,2] = blue


def colorize(image, newColor):
	"""
	Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
	original).
	:param image: Surface to create a colorized copy of
	:param newColor: RGB color to use (original alpha values are preserved)
	:return: New colorized Surface instance
	"""
	image = image.copy()

	# zero out RGB values
	image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
	# add in new RGB values
	image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
	return image
