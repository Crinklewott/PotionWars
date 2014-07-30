
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
import items
import random
import universal
import person

LEATHER_STRAP_SEVERITY = 4
CANE_SEVERITY = 6

allSpankingPositions = {}

def spanking_string(top, bottom):
    spankingStrings = [universal.format_line(
        [top.printedName, '''grabs''', bottom.printedName + "'s", '''arm, and hauls''', person.himher(bottom), '''over''', person.hisher(top), 
            '''knee.''', top.printedName, '''lands a few quick smacks to''', bottom.printedName + "'s", bottom.muscle_adj(), '''bottom, before''', bottom.printedName, 
            '''amanges to roll off,''', top.printedName + "'s", '''knee,''', person.hisher(bottom), '''face bright red.''']),

        universal.format_line([top.printedName, '''spins''', bottom.printedName, '''around and lands a few quick smacks to''', bottom.printedName + "'s", bottom.bum_adj(), 
            '''bottom.''',bottom.printedName, '''squirms back around and elbows''', top.printedName, '''in the gut.''']),

        universal.format_line([top.printedName, '''rams''', bottom.printedName, '''onto''', person.hisher(bottom), '''back.''', bottom.printedName, '''spins around onto''', 
            person.hisher(bottom), '''hands and knees,''', person.hisher(bottom), bottom.bum_adj(), '''bottom briefly pointed towards''', top.printedName + ".", 
            top.printedName, '''leans forward and lands a few quick slaps to''', bottom.printedName + "'s", bottom.muscle_adj(), '''bottom.''', bottom.printedName, 
            '''quickly regains''', person.hisher(bottom), '''feet,''', person.hisher(bottom), '''eyes narrowed angrily.'''])
        ]

    return random.choice(spankingStrings)

def reversed_spanking(top, bottom):
    spankingStrings = [universal.format_line(
        [top.printedName, '''grabs''', bottom.printedName + "'s", '''arm and tries to haul''', person.himher(bottom), '''over''', person.hisher(top), '''knee. However,''',
            bottom.printedName, '''sweeps''', top.printedName + "'s", '''foot out from under''', person.himher(top) + ".", '''While''', top.printedName, '''faceplants,''',
            '''and then tries to scramble back to''', person.hisher(top), '''feet,''', bottom.printedName, '''lands a few hard spanks to''', person.hisher(top),
            top.bum_adj(), '''bottom.''']),

        universal.format_line([top.printedName, '''starts to spin''', bottom.printedName, '''around. However,''', bottom.printedName, '''grabs''', top.printedName + "'s", 
            '''arm, and spins''',
            '''into a lunge position.''', person.HeShe(bottom), '''yanks''', top.printedName, '''over''', person.hisher(bottom), '''knee and lands several quick, hard''',
            '''smacks to''', top.printedName + "'s", top.muscle_adj(), '''bottom, before''', top.printedName, '''manages to roll off of''', bottom.printedName + "'s", 
            '''knee and regain''', person.hisher(top), '''feet.''']),

        universal.format_line([top.printedName, '''tries to ram''', bottom.printedName, '''onto''', person.hisher(bottom), '''back. However,''', bottom.printedName, 
            '''turns with the push''',
            '''and yanks''', top.printedName + "'s", '''head down.''', top.printedName, '''bends over and stumbles forward, trying to maintain''', person.hisher(top),
            '''balance.''', bottom.printedName, '''lands a quick series of sharp slaps to''', top.printedName + "'s", top.muscle_adj(), '''bottom.''', top.printedName,
            '''twists free of''', bottom.printedName + "'s", '''grasp and straightens,''', person.hisher(top), '''face coloring in embarassment.'''])
        ]

    return random.choice(spankingStrings)

def failed_spanking(top, bottom):
    spankingStrings = [universal.format_line(
        [top.printedName, '''tries to grab''', bottom.printedName + "'s", '''arm, but''', person.heshe(top), '''can't quite get a good grip.''']),

        universal.format_line([top.printedName, '''tries to find leverage to spin''', bottom.printedName, '''around, but''', bottom.printedName, '''is struggling with too much''',
            '''intensity.''']),

        universal.format_line([top.printedName, '''rams''', bottom.printedName, '''who stumbles, but manages to keep''', person.hisher(bottom), '''feet.'''])
        ]
    return random.choice(spankingStrings)
            

class SpankingPosition(object):
    def __init__(self, name, description, difficulty=1, maintainability=1, reversalRate=1):
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.maintainability = maintainability
        self.reversalRate = reversalRate
        global allSpankingPositions
        allSpankingPositions[name] = self

    def _save(self):
        return NotImplementedError()

    def _load(dataList):
        return NotImplementedError()


class Implement(items.Item):
    """
    Spanking implements. Once (if) I've implemented the ability to use an implement in combat, severity will give a bonus to the duration of the Humiliation status.
    """
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, severity=0):
        super(Implement, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense)
        self.severity = severity


    def display(self):
        displayString = super(Implement, self).display()    
        return '\n'.join([displayString, 'severity: ' + str(self.severity)])

    def is_combat_implement(self):
        return False

class CombatImplement(Implement):
    """
    Implements that can be used in combat (e.g. the wooden spoon). Some implements (such as the cane) just wouldn't work in the close quarters grappling that a combat
    spanking consists of.
    """
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, severity=0):
        super(CombatImplement, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, severity)
            
    def is_combat_implement(self):
        return True



