import pygame
import sys
import math
import random
import numpy as np
import solarsim

pygame.init()

subpixelsize = 3

shader = False

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h

screen = pygame.display.set_mode((width, height))

font = pygame.font.Font(None, 36)

wallpaperimage = pygame.image.load("wallpaper.png")
wallpaper = pygame.Surface((width / subpixelsize, height / subpixelsize))
wallpaperscale = max(wallpaper.get_width() / wallpaperimage.get_width(), wallpaper.get_height() / wallpaperimage.get_height())
wallpaper.blit(
    pygame.transform.scale(wallpaperimage, (int(wallpaperimage.get_width() * wallpaperscale), int(wallpaperimage.get_height() * wallpaperscale))),
    (int(-(wallpaperimage.get_width() * wallpaperscale - wallpaper.get_width()) / 2), int(-(wallpaperimage.get_height() * wallpaperscale - wallpaper.get_height()) / 2)))

subpixelshader = pygame.Surface((width,height))
viewport = pygame.Surface((width/subpixelsize, height/subpixelsize))

windows = {
    "paint": {
        "pos": (0, 0),
        "border": pygame.image.load("paintwindow.png"),
        "holding": "painting",
        "layer": 1,
    },
    "solar": {
        "pos": (0, 100),
        "border": pygame.image.load("solarwindow.png"),
        "holding": "solarmove",
        "layer": 0,
    }
}
for window in windows:
    windows[window]["localmousepos"] = (0, 0)
    windows[window]["lastmousepos"] = (0, 0)
    windows[window]["app"] = pygame.Surface((windows[window]["border"].get_width()-6, windows[window]["border"].get_height()-12), pygame.SRCALPHA)
    windows[window]["render"] = pygame.Surface((windows[window]["border"].get_width()+1, windows[window]["border"].get_height()+1), pygame.SRCALPHA)
    windows[window]["newlayer"] = windows[window]["layer"]
    windows[window]["enabled"] = True
    windows[window]["killed"] = False
    windows[window]["shadow"] = windows[window]["border"].copy()
    windows[window]["shadow"].set_alpha(100)
windows["paint"]["app"].fill((255, 255, 255))

solarsim.solarinit(windows["solar"]["app"].get_width(), windows["solar"]["app"].get_height())

pencolor = (0, 0, 0)
backlight = 40

if shader:
    tiled_mask = pygame.Surface((subpixelshader.get_width(), subpixelshader.get_height()))
    mask = pygame.image.load("subpixelmask.png").convert()
    for x in range(0, subpixelshader.get_width(), mask.get_width()):
        for y in range(0, subpixelshader.get_height(), mask.get_height()):
            tiled_mask.blit(mask, (x, y))
def subpixelate(window):
    window.fill((backlight, backlight, backlight), special_flags=pygame.BLEND_RGB_ADD)
    pygame.surfarray.blit_array(subpixelshader, np.minimum(pygame.surfarray.array3d(pygame.transform.scale(window, (subpixelshader.get_width(), subpixelshader.get_height()))), pygame.surfarray.array3d(tiled_mask)))

globalmousepos = (0, 0)
globalmouselastpos = (0, 0)
running = True
clock = pygame.time.Clock()
holding = ""
while running:
    clock.tick(60)
    viewport.blit (wallpaper, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION:
            for window in windows:
                windows[window]["localmousepos"] = (round(event.pos[0]/subpixelsize) - windows[window]["pos"][0], round(event.pos[1]/subpixelsize) - windows[window]["pos"][1])
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for layer in range(len(windows)):
                    for window in windows:
                        if windows[window]["layer"] == layer and windows[window]["enabled"]:
                            if windows[window]["localmousepos"][0] >= 3 and windows[window]["localmousepos"][1] >= 9 and windows[window]["localmousepos"][0] <= windows[window]["border"].get_width()-3 and windows[window]["localmousepos"][1] <= windows[window]["border"].get_height()-3:
                                holding = windows[window]["holding"]
                                if window == "paint" and windows["paint"]["layer"] == len(windows)-1:
                                   windows["paint"]["app"].set_at((windows["paint"]["localmousepos"][0]-3, windows["paint"]["localmousepos"][1]-9), pencolor)
                                for i in windows:
                                    if windows[i]["newlayer"] > windows[window]["newlayer"]:
                                        windows[i]["newlayer"] -= 1
                                windows[window]["newlayer"] = len(windows)-1
                            elif windows[window]["localmousepos"][0] >= 0 and windows[window]["localmousepos"][1] >= 0 and windows[window]["localmousepos"][0] <= windows[window]["border"].get_width()-22 and windows[window]["localmousepos"][1] <= 8:
                                holding = window
                                for i in windows:
                                    if windows[i]["newlayer"] > windows[window]["newlayer"]:
                                        windows[i]["newlayer"] -= 1
                                windows[window]["newlayer"] = len(windows)-1
            elif event.button == 4 or event.button == 5:
                if windows["solar"]["enabled"] and windows["solar"]["layer"] == len(windows)-1 and windows["solar"]["localmousepos"][0] >= 3 and windows["solar"]["localmousepos"][1] >= 9 and windows["solar"]["localmousepos"][0] <= windows["solar"]["border"].get_width()-3 and windows["solar"]["localmousepos"][1] <= windows["solar"]["border"].get_height()-3:
                    if event.button == 4:
                        for i in solarsim.planets:
                            solarsim.planets[i]["radius"] *= 1.2
                            solarsim.planets[i]["orbitdistance"] *= 1.2
                    elif event.button == 5:
                        for i in solarsim.planets:
                            solarsim.planets[i]["radius"] *= 0.8
                            solarsim.planets[i]["orbitdistance"] *= 0.8
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for layer in range(len(windows)):
                    for window in windows:
                        if windows[window]["layer"] == layer and windows[window]["enabled"]:
                            if windows[window]["localmousepos"][0] >= windows[window]["border"].get_width()-11 and windows[window]["localmousepos"][1] >= 0 and windows[window]["localmousepos"][0] <= windows[window]["border"].get_width() and windows[window]["localmousepos"][1] <= 8:
                                windows[window]["enabled"] = False
                                windows[window]["killed"] = True
                                windows[window]["newlayer"] = 0
                                for i in windows:
                                    if windows[i]["newlayer"] > windows[window]["newlayer"]+1:
                                        windows[i]["newlayer"] += 1
                            elif windows[window]["localmousepos"][0] >= windows[window]["border"].get_width()-21 and windows[window]["localmousepos"][1] >= 0 and windows[window]["localmousepos"][0] <= windows[window]["border"].get_width()-12 and windows[window]["localmousepos"][1] <= 8:
                                windows[window]["enabled"] = False
                                windows[window]["newlayer"] = 0
                                for i in windows:
                                    if windows[i]["newlayer"] > windows[window]["newlayer"]+1:
                                        windows[i]["newlayer"] += 1
                holding = ""
        elif event.type == pygame.MOUSEMOTION:
            globalmousepos = round(event.pos[0] / subpixelsize), round(event.pos[1] / subpixelsize)
            for window in windows:
                if windows[window]["enabled"]:
                    if holding == "painting" and window == "paint":
                        pygame.draw.line(windows["paint"]["app"], pencolor, (windows["paint"]["lastmousepos"][0]-3, windows["paint"]["lastmousepos"][1]-9), (windows["paint"]["localmousepos"][0]-3, windows["paint"]["localmousepos"][1]-9))
                    elif holding == window:
                        windows[window]["pos"] = (windows[window]["pos"][0] + globalmousepos[0] - globalmouselastpos[0], windows[window]["pos"][1] + globalmousepos[1] - globalmouselastpos[1])
            globalmouselastpos = globalmousepos
        if holding == "solarmove" and windows["solar"]["enabled"]:
            solarsim.planets["anchor"]["x"] += windows["solar"]["localmousepos"][0] - windows["solar"]["lastmousepos"][0]
            solarsim.planets["anchor"]["y"] += windows["solar"]["localmousepos"][1] - windows["solar"]["lastmousepos"][1]
        for window in windows:
            windows[window]["lastmousepos"] = windows[window]["localmousepos"]
    
    windows["solar"]["app"].blit(solarsim.solarupdate(windows["solar"]["app"].get_width(), windows["solar"]["app"].get_height()), (0, 0))
    for window in windows:
        windows[window]["layer"] = windows[window]["newlayer"]
    for layer in range(len(windows)):
        for window in windows:
            if windows[window]["layer"] == layer and windows[window]["enabled"]:
                windows[window]["render"].blit(windows[window]["shadow"], (1, 1))
                windows[window]["render"].blit(windows[window]["app"], (3, 9))
                windows[window]["render"].blit(windows[window]["border"], (0, 0))
                viewport.blit(windows[window]["render"], windows[window]["pos"])
    screen.fill((0, 0, 0))
    if shader:
        subpixelate(viewport)
        screen.blit(subpixelshader, (0, 0))
    else:
        screen.blit(pygame.transform.scale(viewport, (width, height)), (0, 0))
    
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    screen.blit(fps_text, (10, 0))
    
    subpixelshader.fill((0, 0, 0))
    pygame.display.update()

pygame.quit()
sys.exit()
