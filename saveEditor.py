import os
import dill
import universal
import person
import spells_PotionWars

"""
The following set of functions are used to directly edit a Potion Wars savegame, primarily for debugging purposes. The functions assume that this script are in the same directory as the 
executable. Furthermore, there is no UI, all the functions must be invoked from the interpreter.
"""

state = None
save = None

def backup(saveName):
    """
    Creates a backup of save/saveName.sav, called save/saveName.bak. It is HIGHLY recommended that this function is called before doing anything. That way, you can restore the save file if/when you
    fuck up.
    """
    print(' '.join(['backing up', saveName]))
    with open(os.path.join('save', saveName + '.sav'), 'rb') as saveFile:
        with open(os.path.join('save', saveName + '.bak'), 'wb+') as backupFile:
            backupFile.writelines(saveFile.readlines())
    print(' '.join(['done backing up', saveName]))

def load(saveName):
    """
        Loads save/saveName.sav for modification.
    """
    global state, save
    backup(saveName)
    print('loading ' + saveName)
    save = saveName 
    with open(os.path.join('save', saveName + '.sav'), 'rb') as saveFile:
        state = dill.load(saveFile)
    print('****************Done Loading ' + saveName + '***********************')

def commit():
    """
    Writes the modified state to the currently being modified save file.
    """
    print('committing changes')
    with open(os.path.join('save', save + '.sav'), 'wb') as saveFile:
        dill.dump(state, saveFile) 


def restore(saveName=None):
    """
    Given the name of a file, finds the associated save/saveName.bak file, and replaces save/saveName.sav with save/saveName.sav. Use this to revert any and all changes.
    If no saveName is given, the game defaults to the last loaded save file.
    """
    if saveName is None:
        saveName = save
    print(' '.join(['restoring', saveName]))
    with open(os.path.join('save', saveName + '.bak'), 'rb') as backupFile:
        with open(os.path.join('save', saveName + '.sav'), 'wb') as saveFile:
            saveFile.writelines(backupFile.readlines())

def list_keywords():
    print('keywords:')
    print('\n'.join(state.player.keywords))
def add_keyword(keyword):
    """
    Adds the specified keyword to the player's list of keywords.
    """
    print('adding keyword ' + keyword)
    state.player.add_keyword(keyword)

def remove_keyword(keyword):
    """
    Removes the specified keyword from the player's list of keywords.
    """
    print('removing keyword ' + keyword)
    state.player.remove_keyword(keyword)

if __name__ == '__main__':
    load('endepisode')
    list_keywords()
    #remove_keyword('boarding_with_Maria')
    add_keyword('extrovert')
    commit()



