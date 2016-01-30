import pygame
import random
import math
import tools

BUTTON_FONTNAME = "consolas"
BUTTON_FONTSIZE = 14
BUTTON_RECT_SIZE = pygame.Rect([20,20,80,20])

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
			world.load_json()
		if self.clicked(event, self.saveWorldButton.rect):
			print "*DAS CLICKSTEIN"
			world.save_json()

		# Color options
		if self.clicked(event, self.redButton.rect):
			self.red_button_clicked()

		if self.clicked(event, self.greenButton.rect):
			self.green_button_clicked()

		if self.clicked(event, self.blueButton.rect):
			self.blue_button_clicked()

		if self.clicked(event, self.applyColor.rect):
			c = self.rgb
			self.g.brute_force_colorize(self.currentMapTile, (c[0], c[1], c[2], c[3]))
			self.currentTileColored = True

		# Color options
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

		# Tile options
		if self.clicked(event, self.floorTiles.rect):
			tools.button_grid = []
			tools.walkable = True
			tools.wall_check = False

			self.currentGrid = self.g.floor_tiles
			self.currentDrawGrid = world.grid

			self.click(self.floorTiles)
			self.unclick(self.otherTiles)
			self.unclick(self.wallTiles)

		if self.clicked(event, self.otherTiles.rect):
			tools.button_grid = []
			tools.wall_check = False

			self.currentGrid = self.g.other_tiles
			self.currentDrawGrid = world.entities_grid

			self.unclick(self.floorTiles)
			self.click(self.otherTiles)
			self.unclick(self.wallTiles)

		if self.clicked(event, self.wallTiles.rect):
			tools.button_grid = []
			tools.walkable = False
			tools.wall_check = True

			self.currentGrid = self.g.wall_tiles
			self.currentDrawGrid = world.grid

			self.unclick(self.floorTiles)
			self.unclick(self.otherTiles)
			self.click(self.wallTiles)

		# Brush options
		if self.clicked(event, self.brushDraw.rect):
			tools.draw_method = "brush"

			self.click(self.brushDraw)
			self.unclick(self.rektDraw)
			self.unclick(self.fillDraw)


		if self.clicked(event, self.rektDraw.rect):
			tools.draw_method = "rect"
			tools.rect_mouse_start = (0,0)

			self.unclick(self.brushDraw)
			self.click(self.rektDraw)
			self.unclick(self.fillDraw)


		if self.clicked(event, self.fillDraw.rect):
			tools.draw_method = "fill"
			tools.rect_mouse_start = (0,0)

			self.unclick(self.brushDraw)
			self.unclick(self.rektDraw)
			self.click(self.fillDraw)

		# Other options
		if self.clicked(event, self.show_walkable.rect):
			if tools.show_walkable_tiles:
				tools.show_walkable_tiles = False
				self.unclick(self.show_walkable)
			else:
				tools.show_walkable_tiles = True
				self.click(self.show_walkable)



	def __init__(self, world, graphics):
		self.c = tools.Color()
		self.g = graphics

		self.myfont = pygame.font.SysFont(BUTTON_FONTNAME, BUTTON_FONTSIZE)

		self.currentMapTile = self.g.all_tiles[random.randint(0, len(self.g.all_tiles))]
		self.currentTileColored = False
		self.currentTileId = 0

		self.currentTileCopy = self.currentMapTile.copy()
		self.modify_which_color_value = 0
		self.currentColor = (255, 255, 255)

		self.currentGrid = self.g.floor_tiles
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
		self.show_walkable = SmallButton(self, "Show Unwalkable", 840, 100, backColor=self.c.dark_blue, textColor=self.c.white)

		self.floorTiles = SmallButton(self, "Floor Tiles", 1020, 100, backColor=self.c.dark_blue, textColor=self.c.white, buttonSizeX=110)
		self.wallTiles = SmallButton(self, "Wall Tiles", 1140, 100, backColor=self.c.dark_blue, textColor=self.c.white, buttonSizeX=110)
		self.otherTiles = SmallButton(self, "Other Tiles", 1260, 100, backColor=self.c.dark_blue, textColor=self.c.white, buttonSizeX=110)

		self.brushDraw = SmallButton(self, "Brush draw", 1030,670, backColor=self.c.dark_blue, textColor=self.c.white)
		self.rektDraw = SmallButton(self, "Rect draw", 1030,710, backColor=self.c.dark_blue, textColor=self.c.white)
		self.fillDraw = SmallButton(self, "Fill", 1030,750, backColor=self.c.dark_blue, textColor=self.c.white)

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
		self.drawButton(self.show_walkable, display)

		self.drawButton(self.floorTiles, display)
		self.drawButton(self.otherTiles, display)
		self.drawButton(self.wallTiles, display)

		self.drawButton(self.brushDraw, display)
		self.drawButton(self.rektDraw, display)
		self.drawButton(self.fillDraw, display)

	def drawButton(self, smallButton, display):
		display.fill(smallButton.backColor, smallButton.rect)
		display.blit(smallButton.font, (smallButton.font_locationX, smallButton.font_locationY))

	def priview_current_color(self, display, posX, posY):
		c = self.rgb
		display.fill((c[0], c[1], c[2]), [posX, posY, 64, 64])

	def click(self, button):
		button.textColor = self.c.black
		button.backColor = self.c.light_red

	def unclick(self, button):
		button.textColor = self.c.white
		button.backColor = self.c.dark_blue

	def update_button_text(self):
		self.redButton.font = self.redButton.buttonInstance.myfont.render("Red " + str(self.rgb[0]), 1, self.redButton.textColor)
		self.greenButton.font = self.greenButton.buttonInstance.myfont.render("Green " + str(self.rgb[1]), 1, self.greenButton.textColor)
		self.blueButton.font = self.blueButton.buttonInstance.myfont.render("Blue " + str(self.rgb[2]), 1, self.blueButton.textColor)

		self.update_button_reuse(self.floorTiles)
		self.update_button_reuse(self.wallTiles)
		self.update_button_reuse(self.otherTiles)

		self.update_button_reuse(self.rektDraw)
		self.update_button_reuse(self.brushDraw)
		self.update_button_reuse(self.fillDraw)

		self.update_button_reuse(self.show_walkable)

	def update_button_reuse(self, button):
		button.font = button.buttonInstance.myfont.render(button.text, 1, button.textColor)

	def red_button_clicked(self):
		self.modify_which_color_value = 0

		self.click (self.redButton)
		self.unclick (self.greenButton)
		self.unclick (self.blueButton)

	def green_button_clicked(self):
		self.modify_which_color_value = 1

		self.unclick (self.redButton)
		self.click (self.greenButton)
		self.unclick (self.blueButton)

	def blue_button_clicked(self):
		self.modify_which_color_value = 2

		self.unclick (self.redButton)
		self.unclick (self.greenButton)
		self.click (self.blueButton)



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