import pygame, random, math, buttons

MAP_FONTNAME = "courier"
MAP_FONTSIZE = 14

MAP_TILE_SIZE = (16,16)
MAP_MARIGIN = 3

BASE_MAP_OFFSET_Y = 80

COLOR_KEY_SKIP = (128, 128, 128, 255)

clickable_rectangles = []
button_grid = []

walkable 			= True
show_walkable_tiles = False
wall_check			= False
draw_method			= "brush"

rect_mouse_start = (0,0)

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





def event_handling(button, world):
	global rect_mouse_start

	if draw_method == "brush":
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

			if draw_method == "rect":
				mouse_rekt = pygame.Rect(pygame.mouse.get_pos(), (2,2))
				result = mouse_rekt.collidelist(clickable_rectangles)	

				if rect_mouse_start == (0,0) and result != (-1):
					rect_mouse_start = pygame.mouse.get_pos()
				else:
					rect_draw(world, button, pygame.mouse.get_pos())
					rect_mouse_start = (0,0)

		if event.type == pygame.MOUSEBUTTONUP:
			world.mouse_button_down = False

def rect_draw(world, button, mouse_pos):
	c = button.rgb
	backup_grid = world.grid

	start_rekt = pygame.Rect(rect_mouse_start, (2,2))
	start_result = start_rekt.collidelist(clickable_rectangles)
	st_x = int(start_result/world.sizeX)
	st_y = start_result % world.sizeX

	mouse_rekt = pygame.Rect(pygame.mouse.get_pos(), (2,2))
	result = mouse_rekt.collidelist(clickable_rectangles)		
	x = int(result/world.sizeX)
	y = result % world.sizeX

	for i in range(min(st_x, x), max(st_x, x)):
		for j in range (min (st_y, y), max (st_y, y)):
			if button.currentDrawGrid is not world.entities_grid:
				button.currentDrawGrid[i][j] = button.currentMapTile
				world.tileInfo_grid[i][j].walkable = walkable
				world.tileInfo_grid[i][j].is_grass = False
				world.tileInfo_grid[i][j].grid_id = button.currentTileId
				if button.currentTileColored:
					world.tileInfo_grid[i][j].color = (c[0], c[1], c[2], c[3])



def mouse_drag_to_draw(world, button):
	c = button.rgb

	if world.mouse_button_down:
		mouse_pos = pygame.mouse.get_pos()
		mouse_rekt = pygame.Rect(mouse_pos, (2,2))

		result = mouse_rekt.collidelist(clickable_rectangles)
		if result != -1:
			x = int(result/world.sizeX)
			y = result % world.sizeX

			world.tileInfo_grid[x][y].dir_wall  = False
			#wall_placement(x,y, world, button)
			button.currentDrawGrid[x][y] = button.currentMapTile
			world.tileInfo_grid[x][y].walkable  = walkable


			if button.currentDrawGrid == world.entities_grid:
				world.tileInfo_grid[x][y].entity_id = button.currentTileId
				if button.currentTileColored:
					world.tileInfo_grid[x][y].entity_color = (c[0], c[1], c[2], c[3])

			else:
					
				world.tileInfo_grid[x][y].is_grass = False
				world.tileInfo_grid[x][y].grid_id = button.currentTileId
				if button.currentTileColored:
					world.tileInfo_grid[x][y].color = (c[0], c[1], c[2], c[3])
				else:
					world.tileInfo_grid[x][y].color = (255,255,255,255)



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

def wall_placement(x, y, world, button):
	top = False
	bot = False
	left = False
	right = False

	grid = world.tileInfo_grid

	if wall_check and button.currentTileId == button.currentGrid[17]:
		if grid[x-1][y].dir_wall and x-1 >= 0:
			left = True
		if grid [x+1][y].dir_wall and x+1 <= world.sizeX:
			right = True
		if grid [x][y-1].dir_wall and y-1 <= 0:
			top = True
		if grid [x][y+1].dir_wall and y+1 >= world.sizeY:
			bot = True

		if top and bot and left and right:
			choose_wall_tile(17)
		elif not top and not bot and not left and not right:
			choose_wall_tile(17)

		elif top and bot and left and not right:
			choose_wall_tile(8)
		elif top and bot and not left and right:
			choose_wall_tile(15)

		world.tileInfo_grid[x][y].dir_wall = True

def choose_wall_tile(n):
	button.currentMapTile = button.currentGrid[n].copy()
	button.currentTileId = n
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

			if show_walkable_tiles:
				show_walkable(display, world.tileInfo_grid[x][y], posX, posY, color)

			if str(type(world.entities_grid[x][y])) == "<type 'pygame.Surface'>":
				display.blit(world.entities_grid[x][y], rect)

		posY = BASE_MAP_OFFSET_Y
		posX += MAP_TILE_SIZE[0]

def show_walkable(display, tile_info, posX, posY, color):
	if not tile_info.walkable:
		display.fill(color.light_red, [posX, posY, 16,16])

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


def is_square(apositiveint):
	x = apositiveint//2
	seen = set([x])
	while x * x is not apositiveint:
		x = (x + (apositiveint //2)) // 2
		if x in seen: return False
		seen.add(x)
	return True

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
