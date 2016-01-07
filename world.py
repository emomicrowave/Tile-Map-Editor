import spritesheet, tools, graphics
import json

class World:
	# Class variables:
	# world_id, grid, map_symbols

	# I CANT THINK OF ANOTHER WAY TO DRAG TO CHANGE TILES> DONT JUDGE ME!!11
	mouse_button_down = False

	def __init__(self, sizeX, sizeY, graphics):
		if sizeX < 10 and sizeX > 100 and sizeY < 10 and sizeY > 100:
			print "Minimum world size is 10x10. Max world size is 100x100"

		self.sizeX = sizeX
		self.sizeY = sizeY

		self.grid = [[0 for x in range(sizeX)] for x in range(sizeY)]
		self.entities_grid = [[0 for x in range(sizeX)] for x in range(sizeY)]
		self.tileInfo_grid = [[0 for x in range(sizeX)] for x in range(sizeY)]

		self.col = tools.Color()
		self.graphics = graphics

		self.mouse_button_down = False  # GOD HELP US

		self.already_colored_grass = False

	def allPlains(self):
		for x in range(0, len(self.grid)):
			for y in range(0, len(self.grid[x])):
				self.entities_grid[x][y] 	= None
				self.grid[x][y] 			= self.graphics.all_tiles[6*16]
				self.tileInfo_grid[x][y] 	= TileInfo(is_grass=False)


	def save_json(self):
		data = {}
		for x in range (0, len(self.grid)):
			for y in range (0, len(self.grid[x])):

				# color check
				if self.tileInfo_grid[x][y].is_grass:
					self.tileInfo_grid[x][y].color == self.col.s_light_green

				# id check
				if self.tileInfo_grid[x][y].entity_id is None:
					self.tileInfo_grid[x][y].entity_id = 0

				temp_dir = {
					"tile_id"		: self.tileInfo_grid[x][y].grid_id,
					"tile_color"	: self.tileInfo_grid[x][y].color,
					"entity_id"		: self.tileInfo_grid[x][y].entity_id,
					"entity_color"	: self.tileInfo_grid[x][y].entity_color,
					"is_grass"		: self.tileInfo_grid[x][y].is_grass
				}

				data[str((x,y))] = temp_dir

		with open("world.json", "w") as f:
			json.dump(data, f, sort_keys = True, indent = 4, ensure_ascii=False)

	def load_json(self):
		self.allPlains()
		with open("world.json", "r") as f:
			data = json.load(f)
			for x in range (0, len(self.grid)):
				for y in range (0, len(self.grid[x])):
					temp = data[str((x,y))]
					self.tileInfo_grid[x][y].grid_id		= temp["tile_id"]
					self.tileInfo_grid[x][y].color 			= temp["tile_color"]
					self.tileInfo_grid[x][y].entity_id 		= temp["entity_id"]
					self.tileInfo_grid[x][y].entity_color 	= temp["entity_color"]
					self.tileInfo_grid[x][y].is_grass		= temp["is_grass"]

					grid_id 	= self.tileInfo_grid[x][y].grid_id
					entity_id 	= self.tileInfo_grid[x][y].entity_id 

					if grid_id == 96:
						grid_id = 35

					grid_surf_copy 		= self.graphics.floor_tiles[grid_id].copy()
					entity_surf_copy 	= self.graphics.other_tiles[entity_id].copy()

					self.graphics.brute_force_colorize(grid_surf_copy, self.tileInfo_grid[x][y].color )
					self.graphics.brute_force_colorize(entity_surf_copy, self.tileInfo_grid[x][y].entity_color )

					self.grid[x][y]			= grid_surf_copy
					self.entities_grid[x][y]= entity_surf_copy


class TileInfo:

	def __init__(self, grid_id = 6*16, entity_id = 0, color = (255,255,255,255), is_grass = False, entity_color = (255,255,255,255)):
		self.grid_id = grid_id
		self.entity_id = entity_id
		self.color = color
		self.entity_color = entity_color
		self.is_grass = is_grass

