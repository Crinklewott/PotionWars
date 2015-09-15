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

import collections
import dungeonmode
import pwutilities


    #                0     1     2     3     4     5     6     7     8     9    10     11    12    13    14    15    16    17    18    19
slumsLevel1Map = (
                 ( "___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___", "_"),
                 ("|   ","___","_x_","   ","___"," .,","   ","___","___","_*_",".,*", "_*_","___"," .,","___"," .,","__x"," .,"," .,","   ","|" ), #19
                 ("|   ","|.,*",";.,!","|  ","|.,",";__","|  ","|__",";  ","   "," * ","   ","   ",";__","|.,",";.,",";.,",";__","|.,*","|  ","|" ), #18
                 ("| x ","|.,*",";.,x","|  ","|__","|.,","   ","|__","   ","___","   ","___","|  ",";__","|.,",";__",";__","|  ","|__",";  ","|" ), #17
                 ("|   ","|.,x",";.,x","|  ",";__","|__","|  ","|__",";__",";__","|.,",";*_","|__",";__","|__","___","   ","___","   ","__x","|" ), #16 
                 ("|   ",";.,x",";.,x","|  ",";__","|.,","   ","___","___","   ","___","___","|__",";  ","||.,",";.","|  ",";.,","|  ","|.,","|" ), #15
                 ("|   ","|.,x",";.,x","|  ","|.,",";.,","|  ","|  ","   ","|  ","|__",";__",";__","   ","|.,",";.,",";  ","|__","|  ",";_x","|" ), #14
                 ("|   ","|.,x",";.,x","|  ","|.,",";.,","|  ","|  ","   ","|  ","|  ","   ","   ","|  ","|__",";__","|  ",";__","|  ",";.,","|" ), #13
                 ("|   ","|.,x",";.,x","|  ","|__",";.,","|  ",";  ","   ","|  ",";  ","   ","   ","|__","___","   ","   ","   ","   ","|_x","|" ), #12
                 ("|   ","|_*",";_*",";__","., ","|__","|  ","|__","___","|  ",";  ","   ","   ","|__",";__",";  "," * ","., "," x ",";.,","|" ), #11
                 ("|   ","   ","   ","|.,",";.,",";.,","|  ","|.,","|.,","|.,","|__","___","___","|__","   ","., ",".,*",";.,",";.,","|__","|" ), #10
                 ("|   ","___","   ","|.,",";.,",";.,","|  ","|.,",";__",";__",";__",";__",";__","|__",";  ","|__","|x_",";__",";__","|.,","|" ), #9
                 ("|___","|  ","|  ","|.,",";.,",";.,","|  ","|.,","|  ","   ","   ","   ","   ","., ","., ","___","., ","___","   ",";.,","|" ), #8
                 ("|___","___","|  ","|__",";__",";__","|  ","|__","|  ","   ","   ","   ","   ","|__","|__","|__",";__",";__","|.,x","|__","|" ), #7
                 ("| x ","   ","   ","___","___","___","___","___","   ","   "," * ","   ","   ","., ","___","., ","   ","___","|_x","|.,x","|" ), #6
                 ("|   ","., ","   ","|  ","   ","   ","   ","|__",";  ","   ","   ","   ","   ","|.,",";.,","|.,","|  ",";__","|.,",";.,x","|" ), #5
                 ("|   ","|.,","|  ","|  ","   ","   ","   ","|__",";  ","___","___","___","   ","|__","|__","|__","|x ","., ",";__",";_x","|" ), #4
                 ("|   ","|.,","|  ","|  ","   ","   ","   ","|__",";  ","|.,",";.,",";.,",";.,",";.,","|  ","|.,","|  ","|__","   ","|.,","|" ), #3
                 ("|   ","|.,","|.,","|  ","   ","   ","   ","___",";  ","|__",";x_",";.,",";x_",";__","|  ",";.,",";__","|.,",";__",";.,","|" ), #2
                 ("|   ","|__",";__","|__","___","___","___","|.,","|  ","___","___","___","x  ",";__",";__","|  ","|.,x","|.,","|.,","| x","|" ), #1  
                 ("|s__","___","___","___","___","___","___","___","__x",";__","___","x__","|__","___","___","___","___","___","___","___","|" )  #0
                 )
slumsLevel1Events = {i:collections.defaultdict(pwutilities.none) for i in 
        range(len(slumsLevel1Map))}

def e1_0_0():
    if 'ep2Toll' in pwutilities.keywords():
        return False
    else:
        pwutilities.add_keyword('ep2Toll')
        pwutilities.trigger_event("ep2 dungeon toll", "Thugs")
        return True
slumsLevel1Events[0][0] = e1_0_0

def e1_10_6():
    if 'ep2Marketplace' in pwutilities.keywords():
        return False
    else:
        pwutilities.add_keyword('ep2Marketplace')
        pwutilities.trigger_event("ep2 marketplace", "Marketplace")
        return True
slumsLevel1Events[10][6] = e1_10_6

def e1_16_11():
    if 'ep2ChaseEditaEvent1' in pwutilities.keywords():
        return False
    elif 'ep2ChasingEdita' in pwutilities.keywords():
        pwutilities.add_keyword('ep2ChaseEditaEvent1')
        pwutilities.trigger_event('ep2 chase edita event 1', "Two Girls")
        return True
    else:
        return False

slumsLevel1Events[16][11] = e1_16_11

def e1_18_18():
    if 'ep2ChasingEditaEvent2' in pwutilities.keywords():
        return False
    elif 'ep2ChasingEdita' in pwutilities.keywords():
        pwutilities.add_keyword('ep2ChasingEditaEvent2')
        pwutilities.trigger_event('ep2 chase edita event 2', "Busy Street")
        return True
    else:
        return False

slumsLevel1Events[18][18] = e1_18_18


def e1_9_19():
    if 'ep2ChasingEditaEvent3' in pwutilities.keywords() and universal.state.party.defeated():
        pwutilities.trigger_event('ep2 javier defeat rest at brothel')
        universal.state.location.coordinates = (1, 10, 19)
        return True
    else:
        return False

slumsLevel1Events[9][19] = e1_9_19

def e1_11_19():
    return e1_9_19()

slumsLevel1Events[11][19] = e1_11_19

def e1_10_19():
    if 'ep2ChasingEditaEvent3' in pwutilities.keywords():
        return False
    elif 'ep2ChasingEdita' in pwutilities.keywords():
        pwutilities.add_keyword('ep2ChasingEditaEvent3')
        pwutilities.remove_keyword('ep2ChasingEdita')
        pwutilities.trigger_event('ep2 chase edita event 3')
        return True
    else:
        return False

slumsLevel1Events[10][19] = e1_10_19

def e1_10_18():
    if 'ep2ChasingEditaEvent3' in pwutilities.keywords():
        pwutilities.add_keyword('ep2MeetMagola')
        pwutilities.trigger_event('ep2 meet magola')
        return True
    elif 'ep2MeetMagola' in pwutilities.keywords():
        return False
    else:
        pwutilities.trigger_event('ep2 magola busy')
        return True

slumsLevel1Events[10][18] = e1_10_18

       
def e1_11_16():
    if ('ep2BrothelMorning' in pwutilities.keywords() and 
            not 'ep2BrothelMorningDone' in pwutilities.keywords()):
        pwutilities.add_keyword('ep2BrothelMorningDone')
        pwutilities.trigger_event('ep2 brothel common room morning')
        return True
    else:
        return False
slumsLevel1Events[11][16] = e1_11_16

def e1_2_11():
    if not 'ep2VisitedSquatters' in pwutilities.keywords():
        pwutilities.add_keyword('ep2VisitedSquatters')
        pwutilities.trigger_event('ep2 visited squatters')
        return True
    else:
        return False
slumsLevel1Events[2][11] = e1_2_11

def e1_1_17():
    if ('ep2BrothelMorning' in pwutilities.keywords() and 
            not 'ep2FamilySquatterFight' in pwutilities.keywords() and
            not 'ep2FoundEdita' in pwutilities.keywords()):
        pwutilities.add_keyword('ep2FamilySquatterFight')
        pwutilities.trigger_event('ep2 squatter family')
slumsLevel1Events[1][17] = e1_1_17

def e1_1_18():
    if ('ep2BrothelMorning' in pwutilities.keywords() and
            not 'ep2FoundEdita' in pwutilities.keywords()):
        pwutilities.add_keyword('ep2FoundEdita')
        pwutilities.trigger_event('ep2 squatter edita')
slumsLevel1Events[2][11] = e1_2_11

def e1_1_18():
    return pwutilities.play_event('ep2SquatterEdita', 'ep2 squatter edita')

slumsLevel1Events[1][18] = e1_1_18

slumEvents = [slumsLevel1Events]

allegriasDomain = dungeonmode.Dungeon(
    "Allegria's Domain", 
    [slumsLevel1Map], 
    slumEvents, 
    bgMusic=pwutilities.TAIRONAN,
    enemies=None
)
