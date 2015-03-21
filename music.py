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
import pygame
from universal import *
import tempfile
import os

currentMusic = None
currentMusicFileName = None
musicFiles = {}

def decrypt(fileName, songName):
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
        musicFiles[songName] = fileName
        return fileName
    else:
        musicFiles[songName] = None
        return None


def clean_up_music():    
    #Tests to make sure we're running the game as a bundled exe. If we're not, then we DO NOT want to delete the music files.
    try:
        test = sys._MEIPASS
    except Exception:
        return
    else:
        for name, song in musicFiles.items():
            try:
                os.remove(song)
            except (OSError, TypeError):
                continue

def set_theme(theme):
    global THEME
    THEME = decrypt(theme, 'theme')
def set_town(music):
    global TOWN
    TOWN = decrypt(music, 'town')
def set_combat(music):
    global COMBAT
    COMBAT = decrypt(music, 'combat')

def set_defeated(music):
    global DEFEATED
    DEFEATED = decrypt(music, 'defeated')

def set_victory(music):
    global VICTORY
    VICTORY = decrypt(music, 'victory')

def set_boss(music):
    global BOSS
    BOSS = decrypt(music, 'boss')

VICTORY = None
TOWN = None
THEME = None
DEFEATED = None
COMBAT = None
BOSS = None
import threading
lock = threading.Lock()
def play_music(fileObject, fadeoutTime=250, wait=False):
    """
    This function assumes we only have one (open) file object for each music file.
    """
    global currentMusic
    if fileObject is not None:
        if currentMusic != fileObject:
            fadeoutThread = threading.Thread(target=fadeout_thread, args=(fadeoutTime, fileObject))
            if currentMusic is not None:
                fadeoutThread.start()
                if wait:
                    fadeoutThread.join()
            else:
                pygame.mixer.music.load(fileObject)
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(-1)
            currentMusic = fileObject

def fadeout_thread(fadeoutTime, fileObject):
    lock.acquire()
    end_music([fadeoutTime, fileObject])
    lock.release()
    
def end_music(arglist):
    pygame.mixer.music.fadeout(arglist[0])
    pygame.mixer.music.load(arglist[1])
    pygame.mixer.music.play(-1)

def close_music_files():
    pass
