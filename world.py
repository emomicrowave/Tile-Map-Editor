import spritesheet, tools

class World:
	# Class variables:
	# world_id, grid, map_symbols

	# I CANT THINK OF ANOTHER WAY TO DRAG TO CHANGE TILES> DONT JUDGE ME!!11
	mouse_button_down = False

	def __init__(self, sizeX, sizeY):
		if sizeX < 10 and sizeX > 100 and sizeY < 10 and sizeY > 100:
			print "Minimum world size is 10x10. Max world size is 100x100"

		self.sizeX = sizeX
		self.sizeY = sizeY

		self.grid = [[0 for x in range(sizeX)] for x in range(sizeY)]
		self.entities_grid = [[0 for x in range(sizeX)] for x in range(sizeY)]
		self.tileInfo_grid = [[0 for x in range(sizeX)] for x in range(sizeY)]

		self.ss = spritesheet.SpriteSheet("graphics/basic2.png")
		self.graphics = self.ss.load_all_to_list(16, 16, 16, 16, (128, 128, 128, 255))
		self.floor_tiles = self.define_floor_tiles((128, 128, 128, 255))
		self.other_tiles = self.define_other_tiles((128, 128, 128, 255))

		self.col = tools.Color()

		self.mouse_button_down = False  # GOD HELP US

		self.already_colored_grass = False

	def allPlains(self):
		if not self.already_colored_grass:
			tools.remove_bad_pixels(self.graphics[6*16], (128,128,128,255))
			tools.brute_force_colorize(self.graphics[6*16], self.col.s_light_green)
			self.floor_tiles.append(self.graphics[6*16])
			self.already_colored_grass = True

		for x in range(0, len(self.grid)):
			for y in range(0, len(self.grid[x])):
				self.entities_grid[x][y] = None
				self.grid[x][y] = self.graphics[6*16]
				#self.tileInfo_grid[x][y] = TileInfo(color = self.col.s_light_green, is_grass=True)
				self.tileInfo_grid[x][y] = TileInfo(is_grass=True)

	def save(self):
		f = open('world.txt', "w")

		for x in range (0, len(self.grid)):
			for y in range (0, len(self.grid[x])):
				f.write(str(self.tileInfo_grid[x][y].grid_id)+"=")

				if self.tileInfo_grid[x][y].is_grass:
					self.tileInfo_grid[x][y].color == self.col.s_light_green
				f.write(str(self.tileInfo_grid[x][y].color) + ";")

				if self.tileInfo_grid[x][y].entity_id is 0 or self.tileInfo_grid[x][y].entity_id is None:
					f.write("NA=")
				else:
					f.write(str(self.tileInfo_grid[x][y].entity_id) + "=")
				f.write(str(self.tileInfo_grid[x][y].entity_color))
				f.write("|")
			f.write("\n")
		f.close()

	def load(self):
		f = open('world.txt', "r")
		self.allPlains()
		lines = f.readlines()
		lines_two = []

		grid_ids = []
		entity_ids = []

		grid_colors = []
		entity_colors = []

		for line in lines:
			line = line.strip('\n')
			line = line[:-1]
			lines_two.append(line)


		for line in lines_two:
			infos = line.split('|')
			for info in infos:
				temp_info = info.split(';')
				grid_info = temp_info[0]
				entity_info = temp_info[1]

				temp_grid_info = grid_info.split('=')
				grid_ids.append(int(temp_grid_info[0]))
				grid_colors.append(self.string_to_color(temp_grid_info [1]))

				temp_entity_info = entity_info.split('=')
				if temp_entity_info[0] == "NA":
					entity_ids.append(0)
				else:
					entity_ids.append(int(temp_entity_info[0]))
				entity_colors.append(self.string_to_color(temp_entity_info[1]))

		for x in range(0, self.sizeX):
			for y in range(0, self.sizeY):
				current_index = x*50 +y

				grid_id = grid_ids[current_index]
				entity_id = entity_ids[current_index]

				grid_color = grid_colors[current_index]
				entity_color = entity_colors[current_index]

				#Fix grass indexing
				if grid_id == 96:
					grid_id = 35

				grid_surf_copy = self.floor_tiles[grid_id].copy()
				entity_surf_copy = self.other_tiles[entity_id].copy()

				tools.brute_force_colorize(grid_surf_copy, grid_color)
				tools.brute_force_colorize(entity_surf_copy, entity_color)

				self.grid[x][y] = grid_surf_copy
				self.entities_grid[x][y] = entity_surf_copy

				self.tileInfo_grid[x][y] = TileInfo(color = grid_color, entity_color = entity_color)
				self.tileInfo_grid[x][y].grid_id = grid_id
				self.tileInfo_grid[x][y].entity_id = entity_id
				self.tileInfo_grid[x][y].is_grass = False


	def define_floor_tiles(self, colorkey = None):
		rekt_list = []
		tile_list = []

		coords = [
			(7,11), (8,11), (9,11), (10,11), (11,11), (12,11), (13,11), (14,11),
			  (8,12), (9,12), (10,12), (11,12), (12,12), (13,12), (14,12),
				 (3,13), (4,13), (5,13), (6,13)]

		# 16 tiles
		rekt_list.append([7*16, 2*16, 16, 16])
		rekt_list.append([11*16, 2*16, 16, 16])
		rekt_list.append([12*16, 2*16, 16, 16])
		rekt_list.append([14*16, 2*16, 16, 16])
		rekt_list.append([13*16, 3*16, 16, 16])
		rekt_list.append([14*16, 3*16, 16, 16])
		rekt_list.append([0*16, 6*16, 16, 16])
		rekt_list.append([14*16, 7*16, 16, 16])
		rekt_list.append([13*16, 8*16, 16, 16])
		rekt_list.append([14*16, 8*16, 16, 16])
		rekt_list.append([0*16, 11*16, 16, 16])
		rekt_list.append([1*16, 11*16, 16, 16])
		rekt_list.append([2*16, 11*16, 16, 16])
		rekt_list.append([13*16, 13*16, 16, 16])
		rekt_list.append([4*16, 15*16, 16, 16])
		rekt_list.append([7*16, 15*16, 16, 16])

		for rekt in rekt_list:
			tile_list.append(self.ss.image_at(rekt, colorkey))

		for tile in tile_list:
			tools.remove_bad_pixels(tile, (128,128,128,255))

		for i in range(len(coords)):
			tile_list.append(self.ss.image_at([coords[i][0]*16, coords[i][1]*16, 16, 16], colorkey))

		return tile_list

	def define_other_tiles(self, colorkey = None):
		tile_list = []
		coords = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0), (9,0), (10,0), (11,0), (12,0), (13,0), (14,0), (15,0),
				  (2,1), (3,1), (4,1), (5,1), (6,1), (7,1), (8,1), (9,1), (10,1), (11,1), (12,1), (13,1),
				  (2,2), (3,2), (4,2), (5,2), (6,2), (10,2),
				  (10,3), (11,3), (12,3), (0,4), (14,5), (15,7),
				  (0,8), (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (13,8), (14,8), (15,8),
				  (0,9), (1,9), (2,9), (3,9), (4,9), (5,9), (6,9), (7,9), (8,9), (9,9), (10,9), (11,9), (12,9), (13,9), (15,9),
				  (0,10), (1,10), (2,10), (3,10), (4,10), (5,10), (6,10), (7,10), (8,10), (9,10), (10,10), (11,10), (12,10), (13,10),
				  (5,11), (6,11), (7,11), (8,11), (9,11), (10,11), (11,11), (12,11), (13,11), (14,11),
				  (5,12), (6,12), (8,12), (9,12), (10,12), (11,12), (12,12), (13,12), (14,12),
				  (1,13), (3,13), (4,13), (5,13), (6,13), (7,13), (8,13),
				  (0,14), (1,14), (2,14), (3,14), (4,14), (5,14), (6,14), (7,14), (8,14), (9,14), (10,14), (11,14), (12,14), (13,14), (14,14), (15,14),
				  (2,15), (3,15), (8,15), (9,15), (11,15), (12,15), (13,15), (14,15), (15,15), ]

		for i in range(len(coords)):
			tile_list.append(self.ss.image_at([coords[i][0]*16, coords[i][1]*16, 16, 16], colorkey))

		# Make an empty entity object
		tools.make_completely_transparent(tile_list[0])

		return tile_list

	def string_to_color(self, str):
		str = str.strip(" ")
		str = str.strip("(")
		str = str.strip(")")
		str = str.strip("[")
		str = str.strip("]")

		color_ints = str.split(',')

		return (int(color_ints[0]), int(color_ints[1]), int(color_ints[2]), int(color_ints[3]))

class TileInfo:

	def __init__(self, grid_id = 6*16, entity_id = 0, color = (255,255,255,255), is_grass = False, entity_color = (255,255,255,255)):
		self.grid_id = grid_id
		self.entity_id = entity_id
		self.color = color
		self.entity_color = entity_color
		self.is_grass = is_grass

