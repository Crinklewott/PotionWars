#!/usr/bin/python
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

#TODO: This only works when the player is the only character with dynamic clothing.
#Before the second episode is done, we'll need to implement a way to call liftlower, etc. on
#other characters.

#TODO: Handle \child, handle \continue

"""
Usage notes:
    In order to use this translation program, you need two things:
    1. A latex source file using the sprpgs.sty file that contains the transcript for the episode.
    2. A python file that contains the character and room definitions (these SHOULD NOT be added to the file generated by this program, because the generated file WILL BE OVERWRITTEN every time
    you run this script).
"""


import string
import re

class TranslateError(Exception):
    pass

IMPORTS = ['import universal', 'import textCommandsMusic', 'import person', 'import items', 'import pwenemies', 'import dungeonmode', 'import itemspotionwars', 'import random', 'import conversation',
        'import episode', 'import townmode']

inlineCommandsPlayer = {
    r'\hisher':"person.hisher()",  
    r'\HisHer':"person.HisHer()",  
    r'\himher':"person.himher()",  
    r'\HimHer':"person.HimHer()",  
    r'\heshe':"person.heshe()",  
    r'\HeShe':"person.HeShe()",  
    r'\heshell':"person.heshell()",  
    r'\HeShell':"person.HeShell()",  
    r'\himselfherself':"person.himselfherself()",  
    r'\HimselfHerself':"person.HimselfHerself()",  
    r'\mistermiss':"person.mistermiss()",  
    r'\MisterMiss':"person.MisterMiss()",  
    r'\manwoman':"person.manwoman()",  
    r'\ManWoman':"person.ManWoman()",  
    r'\trousers':"universal.state.player.lower_clothing().name",
    r'\hishers':"person.hishers()",  
    r'\HisHers':"person.HisHers()",  
    r'\boygirl':"person.boygirl()",  
    r'\BoyGirl':"person.BoyGirl()",  
    r'\manlady':"person.manlady()",  
    r'\ManLady':"person.ManLady()",  
    r'\kingqueen':"person.kingqueen()",  
    r'\KingQueen':"person.KingQueen()",  
    r'\lordlady':"person.lordlady()",  
    r'\LordLady':"person.LordLady()",  
    r'\brothersister':"person.brothersister()",  
    r'\BrotherSister':"person.BrotherSister()",  
    r'\menwomen':"person.menwomen()",  
    r'\MenWomen':"person.MenWomen()",  
    r'\sirmaam':"person.sirmaam()",  
    r'\SirMaam':"person.SirMaam()",  
    r'\underwearpanties':"person.underwearpanties()",  
    r'\bastardbitch':"person.bastardbitch()",  
    r'\BastardBitch':"person.BastardBitch()",  
    r'\weaponName':"universal.state.player.weapon().name",  
    r'\name':"universal.state.player.name",  
    r'\names':'''universal.state.player.name, "'s"''',
    r'\nickname':"universal.state.player.nickname",  
    r'\nicknames':"universal.state.player.nickname, 's'",
    r'\weapon':"universal.state.player.weapon().name",
    r'\player':"universal.state.player",
    r'\cladbottom': "universal.state.player.clad_bottom(",
    r'\muscleadj': "universal.state.player.muscle_adj()",
    r'\bumadj': "universal.state.player.bum_adj()",
    r'\quiver': "universal.state.player.quiver()",
    r'\quivering': "universal.state.player.quivering()",
    r'\liftlower': "items.liftlower(universal.state.player.lower_clothing())",
    r'\lowerlift': "items.lowerlift(universal.state.player.lower_clothing())",
    r'\liftslowers': "items.liftlower(universal.state.player.lower_clothing())",
    r'\lowerslifts': "items.lowerslifts(universal.state.player.lower_clothing())",
    r'\pajamabottoms': "universal.state.player.pajama_bottom().name",
    r'\pajamas': "universal.state.player.pajama_top().name",
    r'\underwear':"universal.state.player.underwear().name",
    r'\shirt':"universal.state.player.shirt().name",
    r'\stealth': "universal.state.player.stealth()",
    r'\warfare': "universal.state.player.warfare()",
    r'\magic': "universal.state.player.magic()",
    r'\grapple': "universal.state.player.grapple()",
    r'\resilience': "universal.state.player.resilience()",
    r'\keywords': "universal.state.player.keywords",
    r'\sondaughter': "person.sondaughter()",
    r'\SonDaughter': "person.SonDaughter()",
    r'\waistbandhem': "universal.state.player.lower_clothing().waistband_hem()",
    r'\pjwaistbandhem': "universal.state.player.pajama_bottom().waistband_hem()",
    r'\hemwaistband': "universal.state.player.lower_clothing().hem_waistband()",
    r'\pjhemwaistband': "universal.state.player.pajama_bottom().hem_waistband()",
    r'\pheight':("person.height_based_msg(universal.state.player, ", 4),
    r'\pbodytype':("person.bodytype_based_msg(universal.state.player, ", 4),
    r'\pmusculature':("person.musculature_based_msg(universal.state.player, ",3),
    r'\phairlength':("person.hair_length_based_msg(universal.state.player, ",4),
    r'\ppjtype': ("items.dropseat_based_msg(universal.state.player, ", 2),
    r'\pisliftedlowered':("items.liftlowered_based_msg(universal.state.player, ", 2),
    r'\pisloweredlifted':("items.loweredlifted_based_msg(universal.state.player, ", 2),
    }

#A mapping from latex commands to a tuple containing the start of the python code, and the number of arguments the latex command takes.
inlineCommands = {
    r'\hisher':("person.hisher(universal.state.get_character(", 1),
    r'\HisHer':("person.HisHer(universal.state.get_character(", 1),
    r'\himher':("person.himher(universal.state.get_character(", 1), 
    r'\HimHer':("person.HimHer(universal.state.get_character(", 1),
    r'\heshe':("person.heshe(universal.state.get_character(", 1), 
    r'\HeShe':("person.HeShe(universal.state.get_character(",  1),
    r'\heshell':("person.heshell(universal.state.get_character(", 1),  
    r'\HeShell':("person.HeShell(universal.state.get_character(", 1),  
    r'\himselfherself':("person.himselfherself(universal.state.get_character(", 1),  
    r'\HimselfHerself':("person.HimselfHerself(universal.state.get_character(", 1),  
    r'\mistermiss':("person.mistermiss(universal.state.get_character(", 1),  
    r'\MisterMiss':("person.MisterMiss(universal.state.get_character(", 1),  
    r'\manwoman':("person.manwoman(universal.state.get_character(", 1),  
    r'\ManWoman':("person.ManWoman(universal.state.get_character(", 1),  
    r'\hishers':("person.hishers(universal.state.get_character(", 1),  
    r'\HisHers':("person.HisHers(universal.state.get_character(", 1),  
    r'\boygirl':("person.boygirl(universal.state.get_character(", 1),  
    r'\BoyGirl':("person.BoyGirl(universal.state.get_character(", 1),  
    r'\manlady':("person.manlady(universal.state.get_character(", 1),  
    r'\ManLady':("person.ManLady(universal.state.get_character(", 1),  
    r'\kingqueen':("person.kingqueen(universal.state.get_character(", 1),  
    r'\KingQueen':("person.KingQueen(universal.state.get_character(", 1),  
    r'\lordlady':("person.lordlady(universal.state.get_character(", 1),  
    r'\LordLady':("person.LordLady(universal.state.get_character(", 1),  
    r'\brothersister':("person.brothersister(universal.state.get_character(", 1),  
    r'\BrotherSister':("person.BrotherSister(universal.state.get_character(", 1),  
    r'\menwomen':("person.menwomen(universal.state.get_character(", 1),  
    r'\MenWomen':("person.MenWomen(universal.state.get_character(", 1),  
    r'\sirmaam':("person.sirmaam(universal.state.get_character(", 1),  
    r'\SirMaam':("person.SirMaam(universal.state.get_character(", 1),  
    r'\bastardbitch':("person.bastardbitch(universal.state.get_character(", 1),  
    r'\BastardBitch':("person.BastardBitch(universal.state.get_character(", 1),  
    r'\weaponName':("items.weapon_name(", 1),  
    r'\weapon':("items.weapon_name(", 1),
    r'\cladbottom': ("items.clad_bottom(", 1),
    r'\muscleadj': ("person.muscle_adj(", 1),
    r'\bumadj': ("person.bum_adj(", 1),
    r'\liftlower': ("items.liftlower(", 1),
    r'\lowerlift': ("items.lowerlift(", 1),
    r'\liftslowers': ("items.liftslowers(", 1),
    r'\lowerslifts': ("items.lowerslifts(", 1),
    r'\underwear':("items.underwear_name(", 1),
    r'\trousers': ("items.lower_clothing_name(", 1),
    r'\pajamabottoms': ("items.pajama_bottom_name(", 1),
    r'\stealth': ("person.stealth(", 1),
    r'\warfare': ("person.warfare(", 1),
    r'\magic': ("person.magic(", 1),
    r'\grapple': ("person.grapple(", 1),
    r'\resilience': ("person.resilience(", 1),
    r'\waistbandhem': ("items.waistband_hem(", 1),
    r'\hemwaistband': ("items.hem_waistband(", 1),
    r'\height':("person.height_based_msg(", 5),
    r'\bodyType':("person.bodytype_based_msg(",5),
    r'\musculature':("person.musculature_based_msg(",4),
    r'\hairlength':("person.hair_length_based_msg(",5),
    r'\pjtype': ("items.dropseat_based_msg(", 3),
    r'\isliftedlowered':("items.liftlowered_based_msg(", 3),
    r'\isloweredlifted':("items.loweredlifted_based_msg(", 3),
    r'\isliftedlowered':("items.liftlowered_based_msg(", 3)
    }

                          #Removes comments | splits around spaces, and save the spacing | split around commands that begin an environment | split around commands that end an environment | 
                          #split around bracket | ditto | split around command names, and saves those names
tokenizer = re.compile(r'%.*|(\n)|(\s+)|(\\begin\{\w+\})|(\\end\{\w+\})|(\{)|(\})|(\\\w+$)')

START_ENV = r'\begin{openScene}'
END_ENV = r'\end{openScene}'
START_CODE = r'\begin{code}'
END_CODE = r'\end{code}'
BEGIN_SCENE = r'openScene'
BEGIN_NODE = r'\begin{node}'
END_NODE = r'\end{node}'
BEGIN_CHILD_NODE = r'\begin{childnode}'
END_CHILD_NODE = r'\end{childnode}'

def translate(fileName, startingNodeNum, episodeName, episodeNum, titleCardTheme, imports=None):
    tokens = []
    firstSceneFound = False
    lineNum = 1
    with open(fileName, 'r') as texFile:
        for line in texFile:
            firstSceneFound = firstSceneFound or 'openScene' in line
            if firstSceneFound:
                tokens.extend([(token, lineNum) for token in re.split(tokenizer, line) if token])
            lineNum += 1
    for token in tokens:
        #&&&





DEBUG = True
if DEBUG:
    import os
    pyCode = translate(os.path.join('transcripts', 'episode2.tex'), 327, 'Back Alleys', 2, "textCommandsMusic.LUCILLA", imports=IMPORTS + ['import episode2CharRooms'])
    #with open('episode2.py', 'w') as episode2:
    #    episode2.write('\n'.join(pyCode))


    




