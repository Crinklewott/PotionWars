
"""
Copyright 2014 Andrew Russell

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
import pygame
from universal import *
import tempfile
import os

currentMusic = None
currentMusicFileName = None
musicFiles = []
def decrypt(fileName):
    """
    We'll have to encrypt our music files once it's time to release the game, and decrypt
    them as a temporary file. This function
    will decrypt the music before attempting to play it.
    Note: This function will need to use the tempfile python module in order to create the 
    temporary file to maintain security, in particular mkstemp. However, Pygame doesn't
    like it if we return a file object, so this has to return the path to the unencrypted
    file.
    If key is None, that means this code is being released, in which case, the music can't be played (since we can't reveal the key). By returning None, we ensure that
    the game won't try to play it.
    
    #if key is None:
        return None
    else:
        with open(fileName, 'rb') as f:
            ciph = ''.join(f.readlines())
        plain = obj.decrypt(ciph)
        musicFiles.append(tempfile.mkstemp(suffix='.wav')[1])
        with open(musicFiles[-1], 'wb') as f:
            f.write(plain)
        return musicFiles[-1]
    """
    if os.path.exists(fileName):
        return fileName
    else:
        return None


def clean_up_music():    
    for f in musicFiles:
        os.remove(f)

def set_theme(theme):
    global THEME
    THEME = decrypt(theme)
def set_town(music):
    global TOWN
    TOWN = decrypt(music)
def set_combat(music):
    global COMBAT
    COMBAT = decrypt(music)

def set_defeated(music):
    global DEFEATED
    DEFEATED = decrypt(music)

def set_victory(music):
    global VICTORY
    VICTORY = decrypt(music)

def set_boss(music):
    global BOSS
    BOSS = decrypt(music)

VICTORY = None
TOWN = None
THEME = None
DEFEATED = None
COMBAT = None
BOSS = None
def play_music(fileObject, fadeoutTime=250, wait=False):
    """
    This function assumes we only have one (open) file object for each music file.
    """
    print(fileObject)
    global currentMusic
    import threading
    def fadeout_thread(fadeoutTime, currentMusic, fileObject):
        pygame.mixer.music.fadeout(fadeoutTime)
        pygame.mixer.music.load(fileObject)
        pygame.mixer.music.play(-1)
    if fileObject is not None:
        if currentMusic != fileObject:
            if currentMusic is not None:
                fadeoutThread = threading.Thread(target=fadeout_thread, args=(fadeoutTime, currentMusic, fileObject))
                fadeoutThread.start()
                if wait:
                    fadeoutThread.join()
            else:
                pygame.mixer.music.load(fileObject)
                pygame.mixer.music.play(-1)
            currentMusic = fileObject

def close_music_files():
    pass
