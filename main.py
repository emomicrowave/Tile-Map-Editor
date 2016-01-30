import pygame, os
import tools, spritesheet, graphics, buttons
from tools import Color
from world import World
SCR_RESOLUTION = (1390,900)

pygame .init()
display = pygame.display.set_mode(SCR_RESOLUTION)
pygame.display.set_caption("Ascii Map Editor v 0.4")

exitGame = False

# Class constructors

graphics 	= graphics.Graphics()
col 		= Color()
world 		= World(50, 50, graphics) # Leave 50x50 for now
button 		= buttons.Buttons(world, graphics)

world.allPlains()

work_dir 	= os.getcwd()
clock 		= pygame.time.Clock()

while not exitGame:
	clock.tick(60)

	tools.event_handling(button, world)

	display.fill(col.black)
	display.fill(col.white, [0,70,1000,830])
	display.fill(col.s_light_blue, [1000, 70, 400, 830])

	button.draw_all(display)
	tools.drawWorld(display, world, col)

	tools.draw_button_grid(display, button.currentGrid, 1050, 150, 16, 16, 3)

	tools.current_button_preview(display, button, 1165, 430)
	button.priview_current_color(display, 1165, 505)

	#print world.grid[0][0].get_at((1,1))
	#print len(tools.button_grid)
	#print world.tileInfo_grid[0][0].color
	#print tools.rect_mouse_start

	pygame.display.update()

pygame.quit()
quit()
