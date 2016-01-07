import spritesheet, pygame

class Graphics:

	def __init__(self):
		self.ss = spritesheet.SpriteSheet("graphics/basic2.png")

		self.already_colored_grass = False

		self.all_tiles    = []
		self.floor_tiles = []
		self.other_tiles = []

		self.load_graphics()

	def load_graphics(self):

		self.all_tiles 		= self.ss.load_all_to_list(16, 16, 16, 16, (128, 128, 128, 255))
		self.floor_tiles 	= self.define_floor_tiles((128, 128, 128, 255))
		self.other_tiles 	= self.define_other_tiles((128, 128, 128, 255))

		# Add colored grass to the tileset
		if not self.already_colored_grass:
				self.remove_bad_pixels(self.all_tiles[6*16], (128,128,128,255))
				self.brute_force_colorize(self.all_tiles[6*16], (105, 255, 84, 255))
				self.floor_tiles.append(self.all_tiles[6*16])
				self.already_colored_grass = True

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
				self.remove_bad_pixels(tile, (128,128,128,255))

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
		self.make_completely_transparent(tile_list[0])
		return tile_list


	def remove_bad_pixels(self, tile_surface, remove_color):
		for x in range (tile_surface.get_size()[0]):
			for y in range (tile_surface.get_size()[1]):
				current_color = tile_surface.get_at((x,y))
				if current_color[0] == remove_color[0] and current_color[1] == remove_color[1] and current_color[2] == remove_color[2]:
					tile_surface.set_at((x,y), (current_color[0]-1, current_color[1]-1, current_color[2]-1, 255))
				else:
					banana = 5

	def make_completely_transparent(self, surface, colorkey = (128,128,128,255)):
		for x in range (surface.get_size()[0]):
			for y in range (surface.get_size()[1]):
				surface.set_at((x,y), colorkey)

	def brute_force_colorize(self, surface, target_color):
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

