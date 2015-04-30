
"""
Copyright 2014, 2015 Andrew Russell

This file is part of PotionWars.
PotionWars is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PotionWars is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PotionWars.  If not, see <http://www.gnu.org/licenses/>.
"""
import universal
from universal import *
import pygame
import sys
from pygame.locals import *
import titleScreen
import music
import os
"""
Here is where we have the basic interaction mode of the program. It displays the 
current options, and requests a response. 
NOTE: Currently this is in the same directory as the game itself. Once we get a 
reasonably working version, we'll move it into the package, and create the package.
"""

pygame.init()
defaultFont = pygame.font.SysFont(universal.FONT_LIST, universal.DEFAULT_SIZE)

def set_font(fontIn):
    global font
    defaultFont = fontIn

def begin_game(episode):
    global displayedText
    global commands
    global screen
    global font
    import os
    if '.init.sav' in os.listdir('save'):
        os.remove(os.path.join('save', '.init.sav'))
# Initialise screen
    #commandText = textrect.render_textrect(' '.join(commands), font, commandView, LIGHT_GREY, DARK_GREY, 1)
    #commandTextPos = commandText.get_rect()
    #commandTextPos.centerx, commandTextPos.centery = commandView.center;
    # Blit everything to the screen
    defaultFont = pygame.font.SysFont(universal.FONT_LIST, universal.DEFAULT_SIZE)
    titleFont = pygame.font.SysFont(universal.FONT_LIST_TITLE, universal.TITLE_SIZE)
    universal.init_game()
    background = universal.get_background()
    screen = universal.get_screen()
    screen.blit(background, (0, 0))
    commandView = universal.get_command_view()
    worldView = universal.get_world_view()
    #commandSurface = pygame.Surface((commandView.width, commandView.height))
    #commandSurface.fill((255, 0, 0))
    #commandSurface.fill(DARK_GREY)
    #commandSurface.fill(LIGHT_GREY)
    #pygame.display.flip()
    leftCommandView = universal.get_left_command_view()
    rightCommandView = universal.get_right_command_view()
    middleCommandView = universal.get_middle_command_view()
    dirtyRects = titleScreen.title_screen(episode)
    #screen.blit(commandSurface, commandView.topleft)
    #screen.blit(background, (0,))
    # Event loop
    #fps = 30
    #clock = pygame.time.Clock()
    while True:
        #screen.blit(commandSurface, commandView.topleft)
        #pygame.draw.rect(commandSurface, LIGHT_GREY, commandView, 5)
        #Technically, this for loop is silly now, because I'm only allowing one event in
        #queue at a time. (Search for CLEAR) 
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_LSUPER or event.key == K_RSUPER: 
                    pygame.display.iconify()
                else:
                    #CLEAR
                    #This will have to be changed if I ever implement something that requires rapid key combinations.
                    pygame.event.clear()
                    newDirtyRects = universal.get_command_interpreter()(event)
                    try:
                        dirtyRects.extend(newDirtyRects)
                    except TypeError:
                        pass
            elif event.type == QUIT:
                music.close_music_files()
                import os
                if '.init.sav' in os.listdir('save'):
                    os.remove(os.path.join('save', '.init.sav'))
                music.clean_up_music()
                return
            if universal.get_text_to_display() != '':
                if universal.get_title_text() != '':
                    position = (worldView.topleft[0], worldView.topleft[1] + titleFont.get_linesize())
                    textRect = worldView.copy()
                    textRect.height = textRect.height - titleFont.get_linesize()
                    universal.display_text(universal.get_title_text(), worldView, position, isTitle=True)
                displayPosition = (worldView.topleft[0], worldView.topleft[1] + 2 * titleFont.get_linesize())
                textRect = worldView.copy()
                dirtyRects.append(textRect)
                textRect.height = textRect.height - 2 * titleFont.get_linesize()
                universal.display_text(universal.get_text_to_display(), textRect, displayPosition, isTitle=False)
                universal.clear_text_to_display()
                #if DEBUG:
                    #pygame.draw.rect(background, (250, 250, 250), textpos, 5)
                #background.blit(text, textpos)
                #screen.blit(background, (0, 0))
        #The following is a bit of command position fiddling to make everything look nice and balanced.
        universal.display_commands()
        pygame.draw.rect(screen, universal.LIGHT_GREY, pygame.Rect(commandView.topleft, commandView.size), universal.COMMAND_VIEW_LINE_WIDTH)
        #pygame.display.flip()
        #clock.tick_busy_loop(fps)
        newDirtyRects = []
        #Bonemouth was having a strange error where the game would crash when trying to save, apparently because the game only takes one list of dirty rects? Not sure, and couldn't replicate it,
        #and of course the error message doesn't actually print the value of dirty rects :-/, so I can't figure out what dirty rects look like when the bug is thrown. So I'm assuming for some
        #strange reason I'm ending up with a nested list. So I flatten it first. Note that since every atomic element is a rectangle, and those aren't iterable, we don't need to worry about 
        #accidentally flattening tuples or strings.
        for maybeList in dirtyRects:
            if isinstance(maybeList, pygame.Rect):
                newDirtyRects.append(maybeList)
            else:
                newDirtyRects.extend(maybeList)
        newDirtyRects.append(get_command_view())
        #Wine doesn't play nice with the dirty rects approach, so if we are running under Wine, then we update everything forever.
        if universal.playOnMac:
            pygame.display.flip()
            dirtyRects = []
        elif dirtyRects:
            pygame.display.update(newDirtyRects)
        dirtyRects = []


