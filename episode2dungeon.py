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

import dungeonmode
import pwutilities


    #               0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19
slumsLevel1Map = (
                 ( "___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___", "_"),
                 ("|   ","___","___","   ","___"," .,","   ","___","___","___",".,", "___","___","___","___","___","___","___","___","   ","|" ), #19
                 ("|   ","|.,",";.,","|  ","|.,",";__","|  ","|__",";  ","___","   ","___","   ",";__","|.,",";.,",";.,",";__","|.,","|  ","|" ), #18
                 ("|   ","|.,",";.,","|  ","|__","|.,","   ","|__",";  ",";__","|  ",";__","|  ",";__","|.,",";__",";__","|  ","|__",";  ","|" ), #17
                 ("|   ","|.,",";.,","|  ",";__","|__","|  ","|__",";__",";__","|.,",";__","|__",";__","|__","___","   ","___","   ","___","|" ), #16 
                 ("|   ",";.,",";.,","|  ",";__","|.,","   ","___","___","   ","___","___","|__",";  ","||.,",";.","|  ",";.,","|  ","|.,","|" ), #15
                 ("|   ","|.,",";.,","|  ","|.,",";.,","|  ","|  ","   ","|  ","|__",";__",";__","   ","|.,",";.,",";  ","|__","|  ",";__","|" ), #14
                 ("|   ","|.,",";.,","|  ","|.,",";.,","|  ","|  ","   ","|  ","|  ","   ","   ","|  ","|__",";__","|  ",";__","|  ",";.,","|" ), #13
                 ("|   ","|.,",";.,","|  ","|__",";.,","|  ",";  ","   ","|  ",";  ","   ","   ","|__","___","   ","   ","   ","   ","|__","|" ), #12
                 ("|   ","|__",";__",";__","., ","|__","|  ","|__","___","|  ",";  ","   ","   ","|__",";__",";  ","   ","., ","   ",";.,","|" ), #11
                 ("|   ","   ","   ","|.,",";.,",";.,","|  ","|.,","|.,","|.,","|__","___","___","|__","   ","., ","., ",";.,",";.,","|__","|" ), #10
                 ("|   ","___","   ","|.,",";.,",";.,","|  ","|.,",";__",";__",";__",";__",";__","|__",";  ","|__","|__",";__",";__","|.,","|" ), #9
                 ("|___","|  ","|  ","|.,",";.,",";.,","|  ","|.,","|  ","   ","   ","   ","   ","., ","., ","___","., ","___","   ",";.,","|" ), #8
                 ("|___","___","|  ","|__",";__",";__","|  ","|__","|  ","   ","   ","   ","   ","|__","|__","|__",";__",";__","|., ","|__","|" ), #7
                 ("|   ","   ","   ","___","___","___","___","___","   ","   ","   ","   ","   ","., ","___","., ","   ","___","|__","|.,","|" ), #6
                 ("|   ","., ","   ","|  ","   ","   ","   ","|__",";  ","   ","   ","   ","   ","|.,",";.,","|.,","|  ",";__","|.,",";.,","|" ), #5
                 ("|   ","|.,","|  ","|  ","   ","   ","   ","|__",";  ","___","___","___","   ","|__","|__","|__","|  ","., ",";__",";__","|" ), #4
                 ("|   ","|.,","|  ","|  ","   ","   ","   ","|__",";  ","|.,",";.,",";.,",";.,",";.,","|  ","|.,","|  ","|__","   ","|.,","|" ), #3
                 ("|   ","|.,","|.,","|  ","   ","   ","   ","___",";  ","|__",";__",";.,",";__",";__","|  ",";.,",";__","|.,",";__",";.,","|" ), #2
                 ("|   ","|__",";__","|__","___","___","___","|.,","|  ","___","___","___","   ",";__",";__","|  ","|.,","|.,","|.,","|  ","|" ), #1  
                 ("|s__","___","___","___","___","___","___","___","___",";__","___","___","|__","___","___","___","___","___","___","___","|" )  #0
                 )

def e1_0_0():
    if 'ep2Toll' in pwutilities.keywords():
        return False
    else:
        pwutilities.add_keyword('ep2Toll')
        pwutilities.trigger_event("ep2 dungeon toll", "Thugs")
        return True

def e1_10_6():
    if 'ep2Marketplace' in pwutilities.keywords():
        return False
    else:
        pwutilities.add_keyword('ep2Marketplace')
        pwutilities.trigger_event("ep2 marketplace", "Marketplace")
        return True

def e1_16_11():
    if 'ep2ChaseEditaEvent1' in pwutilities.keywords():
        return False
    elif 'ep2ChasingEdita' in pwutilities.keywords():
        pwutilities.add_keyword('ep2ChaseEditaEvent1')
        pwutilities.trigger_event('ep2 chase edita event 1', "Two Girls")
        return True
    else:
        return False


slumsLevel1Events = (
                   #0    1    2   3     4   5    6    7     8   9    10   11   12   13  14    15   16   17   18   19
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #19
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #18
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #17
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #16
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #15
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #14
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #13
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #12
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,e1_16_11,None,None,None), #11
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #10
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #9
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #8
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #7
                 (None,None,None,None,None,None,None,None,None,None,e1_10_6,None,None,None,None,None,None,None,None,None), #6
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #5
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #4
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #3
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #2
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #1
                 (e1_0_0,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #0
                 )

slumEvents = [slumsLevel1Events]
allegriasDomain = dungeonmode.Dungeon("Allegria's Domain", [slumsLevel1Map], slumEvents, bgMusic=pwutilities.TAIRONAN,
        enemies=None)
