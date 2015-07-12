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
import sp_rpg_engine
import logging, logging.handlers
import universal
import titleScreen
import pygame
import episode1
import episode2CharRooms
import episode2
import os
import os.path
import sys

abspath = os.path.abspath(sys.argv[0])
dname = os.path.dirname(abspath)
os.chdir(dname)

universal.set_author('Andrew Russell')
universal.set_programmer('Andrew Russell')
universal.set_author_email('sprpgs@gmail.com')
universal.set_programmer_email('sprpgs@gmail.com')
universal.set_author_email_bugs(universal.authorEmail + '+PWBugs')
universal.set_programmer_email_bugs(universal.programmerEmail + '+PWBugs')
universal.set_name('Potion Wars')

titleScreen.title('Pandemonium Cycle')
titleScreen.subtitle('The Potion Wars')
titleScreen.set_title_image(universal.resource_path('PotionWarsTitleScreen'),
        'png', 6)

#Clears out errors.log every time the game begins. If I didn't do this, then
# the errors.log
#file would eventually become absurdly huge, since it's logging all the battle
# data.
open('errors.log', 'a').close()
for i in range(4, 0, -1):
    open('errors_' + str(i) + '.log', 'a').close()
for i in range(4, 0, -1):
    try:
        with open(''.join(["errors_", str(i), ".log"]), 'r') as errorI:
            with open(''.join(["errors_", str(i+1), ".log"]), 'w') as errorIPlusOne:
                for line in errorI:
                    errorIPlusOne.write(line)
    except IOError:
        pass

try:
    with open("errors.log", 'r') as f:
        with open("errors_1.log", 'w') as g:
            for line in f:
                g.write(line)
except IOError:
    pass

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged')
errorLog = logging.getLogger("errors")


pygame.init()

errorLog.setLevel(logging.NOTSET)
#episode1.episode1.nextEpisode = episode1.episode2
episode1.episode1.nextEpisode = episode2.episode2
episode2.episode2.scenes.append(episode2CharRooms.episode2Scene2)
episode2.episode2.nextEpisode = episode2CharRooms.episode3
with open("errors.log", 'w') as f:
    pass
errorLog.addHandler(logging.FileHandler("errors.log"))
if __name__ == '__main__':
    try:
        sp_rpg_engine.begin_game(episode1.episode1)
    except Exception, e:
        errorLog.exception("My life is pain!")
        raise
