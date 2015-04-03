
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
    def __init__(self, name, humiliating, maintainability, description):
        self.name = name
        self.humiliating = humiliating
        self.maintainability = maintainability
        #We're going to eliminate the reversability stat. So we do that by setting it to 0 so we don't have to affect the reversability calculations at all.
        self.reversability = 0
        self.description = description
        allPositions[self.name] = self

    def display(self):
        return '\n'.join([self.description, 'humiliating: ' + rating(self.humiliating), 'maintainability: ' + rating(self.maintainability)])

    def __eq__(self, other):
        return self.name == other.name

    def _save(self):
        raise NotImplementedError("Shouldn't be saving positions. These are constant.")

    @staticmethod
    def _load(data):
        raise NotImplementedError("Shouldn't be loading positions. These are constant.")

overTheKnee = Position('over the knee', 2, 0, "Positions in this class involve the spanker turning the spankee over her knee. This position is very humiliating, but difficult to maintain.")

standing = Position('standing', 1, 1, "The spanker remains standing when administering the spanking. Positions in this class include: grabbing the spankee's arm, underarm, and over the shoulder, amongst others. These positions are are balanced. They're both moderately humiliating and moderately easy to maintain..")

onTheGround = Position('on the ground', 0, 2, "Positions in this class involve the spankee being on the ground. Such positions include but are not limited to, diaper, reverse riding, and waist between legs. These positions are not very humiliating, but they are very easy to maintain. These can be devastating against enemies with a relatively low grapple.")

