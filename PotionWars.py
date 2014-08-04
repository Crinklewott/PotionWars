import sp_rpg_engine
import logging, logging.handlers
import universal
import titleScreen
import textCommands
import pygame
import episode1
import episode2

universal.set_author('Andrew Russell')
universal.set_programmer('Andrew Russell')
universal.set_author_email('sprpgs@gmail.com')
universal.set_programmer_email('sprpgs@gmail.com')
universal.set_author_email_bugs(universal.authorEmail + '+PWBugs')
universal.set_programmer_email_bugs(universal.programmerEmail + '+PWBugs')
universal.set_name('Potion Wars')

titleScreen.title('Pandemonium Cycle')
titleScreen.subtitle('The Potion Wars')
titleScreen.set_title_image(universal.resource_path('PotionWarsTitleScreen'), 'png', 6)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged')
errorLog = logging.getLogger("errors")


pygame.init()

errorLog.setLevel(logging.ERROR)
with open("errors.log", 'a') as f:
    pass
errorLog.addHandler(logging.FileHandler("errors.log"))
if __name__ == '__main__':
    try:
        sp_rpg_engine.begin_game(episode1.episode1)
    except Exception:
        errorLog.exception("My life is pain!")
        raise
