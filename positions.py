
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
import universal
from universal import *

MAX_RATING = 2

OTK = 0
STANDING = 1
ON_THE_GROUND = 2

def rating(num):
    return ''.join([str(num), '/', str(MAX_RATING)])

allPositions = {}
class Position(universal.RPGObject):
    """
    Defines the spanking positions
    """
    def __init__(self, name, difficulty, maintainability, description):
        self.name = name
        self.difficulty = difficulty
        self.maintainability = maintainability
        #We're going to eliminate the reversability stat. So we do that by setting it to 0 so we don't have to affect the reversability calculations at all.
        self.reversability = 0
        self.description = description
        allPositions[self.name] = self

    def display(self):
        return '\n'.join([self.description, 'difficulty: ' + rating(self.difficulty), 'maintainability: ' + rating(self.maintainability)])

    def __eq__(self, other):
        return self.name == other.name

    def _save(self):
        raise NotImplementedError("Shouldn't be saving positions. These are constant.")

    @staticmethod
    def _load(data):
        raise NotImplementedError("Shouldn't be loading positions. These are constant.")

overTheKnee = Position('over the knee', 1, 1, "Positions in this class involve the spanker turning the spankee over her knee. This is the position to which all other positions are compared. It is relatively easy to pull off successfully, and the spanker can maintain the position for a fair amount of time.")

standing = Position('standing', 0, 0, "The spanker remains standing when administering the spanking. Positions in this class include: grabbing the spankee's arm, underarm, and over the shoulder, amongst others. These positions are relatively easy to get into, but they're very hard to maintain. Useful against enemies with a relatively high grapple.")

onTheGround = Position('on the ground', 2, 2, "Positions in this class involve the spankee being on the ground. Such positions include but are not limited to, diaper, reverse riding, and waist between legs. These positions are relatively difficult to get into, but are relatively easy to maintain. These can be devastating against enemies with a relatively low grapple.")

