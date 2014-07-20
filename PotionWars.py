import episode1
import sp_rpg_engine
import logging, logging.handlers

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is when this event was logged')
errorLog = logging.getLogger("errors")

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
