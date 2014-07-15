
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
import universal
from universal import *

MAX_RATING = 3

def rating(num):
    return ''.join([str(num), '/', str(MAX_RATING)])

class Position(universal.RPGObject):
    """
    Defines the spanking positions
    """
    def __init__(self, name, difficulty, maintainability, reversability, description):
        self.name = name
        self.difficulty = difficulty
        self.maintainability = maintainability
        self.reversability = reversability
        self.description = description
        universal.state.add_position(self)

    def display(self):
        return '\n'.join([self.description, 'difficulty: ' + rating(self.difficulty), 'maintainability: ' + rating(self.maintainability), 
            'reversability: ' + rating(self.reversability)])

    def __eq__(self, other):
        return self.name == other.name

    def _save():
        raise NotImplementedError("Shouldn't be saving positions. These are constant.")
    def _load(data):
        raise NotImplementedError("Shouldn't be loading positions. These are constant.")

overTheKnee = Position('over the knee', 1, 1, 1, "The spanker sits down on her heels, and yanks the spankee across her lap. This is the position to which all other positions are compared. It is relatively easy to pull off successfully, the spanker can maintain the position for a fair amount of time, and her opponent has a fair chance of reversing.")

frontalOverLap = Position('frontal over lap', 1, 2, 2, "The spanker sits down on her heels, spreads her knees, and yanks the spankee down over her lap so that the spankee is facing (roughly) the opposite direction as the spanker. The spanker then wraps her non-spanking arm around the spankee's torso to hold her in place while administering the spanking. Frontal over the lap has a higher chance of getting reversed than OTK. However, it is also easier to maintain.")

overOneKnee = Position('over one knee', 0, 0, 1, "The spanker goes down into a lunge position,  one knee on the ground, with the other leg in front of her at right angles. At the same time, the spanker pulls the spankee across the proferred knee. It is more unstable than the other two over the knee positions, and therefore harder to maintain. However, it also has a lower chance of being successfully reversed.")

underarm = Position('underarm', 1, 2, 2, "The spanker forces the spankee to bend over. Then the spanker wraps her arm around the spankee's waist, leaving the bottom vulnerable to a proper thrashing. This position is of moderate difficulty, and is very maintainable. However, because the position doesn't really do much to throw the spankee off-balance, there is a very high risk of a reversal.")

headBetweenLegs = Position('head between legs', 2, 3, 1, "The spanker forces the spankee to bend down practically to her toes, and then locks her legs around the spankee's head and neck. This is one of the most difficult positions to get an opponent into, however once there, there isn't much the spankee can do to break out. Furthermore, because of the tremendously awkward positioning, it is difficult for the spankee to successfully reverse.")

standing = Position('standing', 0, 0, 0, "The spanker grabs the spankee's arm, and either spins the spankee around, or pivots around the spankee, and lands a few smacks. Getting an opponent into the spanking position is exceptionally easy, and at the same time the position is very hard to reverse. However, the standing position is in no way maintainable.")

reverseRiding = Position('reverse riding', 1, 3, 3, "The spanker knocks the spankee to the ground, and then sits on her, facing backward so that she has access to the spankee's backside. This position isn't particularly difficult, and is very maintainable. However, it is also very easy to reverse...")

waistBetweenLegs = Position('waist between legs', 2, 3, 2, "The spanker forces the spankee onto hands and knees, then locks her legs around the spankee's torso. Waist between legs is easier than head between legs, and harder than reverse riding, but almost as maintainable as both. However, it has a relatively high reversability, double that of head between legs, though not quite as bad as reverse riding.")

diaper = Position('diaper', 3, 3, 1, "The spanker shoves the spankee onto her back, then lifts the spankee's legs up perpendicular to the spankee's torso. This is one is very similar to head between legs in that it is difficult to execute, but is easily maintained and is difficult to reverse. The primary difference is that it is slightly easier than head between legs, is slightly harder to maintain, and has a slightly lower chance of being reversed.")
