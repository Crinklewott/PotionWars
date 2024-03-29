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

def register(fileName, songName):
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
    THEME = theme
    musicFiles['theme'] = THEME


def set_town(music):
    global TOWN
    TOWN = music
    musicFiles['town'] = music


def set_combat(music):
    global COMBAT
    COMBAT = music
    musicFiles['combat'] = COMBAT

def set_catfight(music):
    global CATFIGHT
    CATFIGHT = music
    musicFiles['catfight'] = CATFIGHT

def set_defeated(music):
    global DEFEATED
    DEFEATED = music
    musicFiles['defeated'] = music

def set_victory(music):
    global VICTORY
    VICTORY = music
    musicFiles['victory'] = music

def set_boss(music):
    global BOSS
    BOSS = music
    musicFiles['boss'] = music

VICTORY = None
TOWN = None
THEME = None
DEFEATED = None
COMBAT = None
CATFIGHT = None
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

def stop_music():
    pygame.mixer.stop()

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


