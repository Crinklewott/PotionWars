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

conversationPartner = None
previousConversation = None
previousMode = None
maxIndex = 0
SPLIT = -50

def continue_to_node(origin, destination, newPage=False):
    """
    Given two nodes, invokes the quip function of destination, and sets the children and playerComments of destination to be used by origin.
    Note that this is transitive.

    Furthermore, because this is being used by auto-generated code, it doesn't deal with any of the weirdly complicated cases that have afflicted say_node over the course of
    episode 1.
    """
    if newPage:
        universal.say('\p', justification=0)
    else:
        universal.say('\n\n', justification=0)
    result = destination.quip_function()
    origin.children = destination.children
    origin.playerComments = destination.playerComments
    return result


def converse_with(person, previousModeIn=None):
    global conversationPartner
    conversationPartner = person
    if person.litany is not None:
        litany = person.litany
    elif person.defaultLitany is not None:
        litany = person.defaultLitany
    else:
        litany = emptyLitany
    global previousMode
    if previousModeIn:
        previousMode = previousModeIn
    say_title(person.printedName)
    say_node(litany)


def say_node(litanyIndex):
    """
    litanyIndex is a terrible argument name and should be changed. It can be either the natural number that is the node's index, or it can be the node itself.
    """
    #import traceback
    #traceback.print_stack()
    global previousMode
    #This may appear redundant, but it's possible for a node's quip_function to immediately invoke a different node, without going through the player. In that case,
    #we need to make sure that the current litany of the conversationPartner is properly updated.
    conversationPartner.litany = litanyIndex
    try:
        litany = allNodes[litanyIndex]
    except KeyError:
        try:
            litany = allNodes[litanyIndex.index]
        except KeyError:
            say("There is nothing to be said.")
            acknowledge(previousMode, ())
            return
        else:
            conversationPartner.litany = litanyIndex.index
    function = None
    args = None
    executeImmediately = False
    if litany.quip_function is not None:
        result = litany.quip_function()
        if result is not None:
            function = result[0]
            assert function
            args = result[1]
            try:
                executeImmediately = result[2]
            except IndexError:
                pass
    if litany.quip == '':
        if args is not None and function is not None:
            function(*args)
        elif function is not None:
            function()
        return
    else:
        if litany.music is not None:
            universal.say(litany.quip, justification=0, music=litany.music)
        else:
            universal.say(litany.quip, justification=0)
    if function == SPLIT:
        litany.quip_function = result[1]
        acknowledge(say_node, (litany))
        return
    elif litany.playerComments:
        universal.say('\p', justification=0)
        universal.say('\n'.join([str(i) + '. ' + comment for (i, comment) in zip([i for i in range(1, len(litany.playerComments)+1)], litany.playerComments)]), justification=0)
        set_commands(['(#)Select a number.'])
        set_command_interpreter(converse_with_interpreter)
    elif litany.children:
        playerComments = [child.comment for child in litany.children]
        universal.say('\p', justification=0)
        try:
            universal.say('\n'.join([str(i) + '. ' + comment for (i, comment) in zip([i for i in range(1, len(playerComments)+1)], playerComments)]), justification=0)
        except TypeError:
            raise TypeError
        set_commands(['(#)Select a number.'])
        set_command_interpreter(converse_with_interpreter)
    else:
        conversationPartner.litany = conversationPartner.defaultLitany
        if function is not None and function == acknowledge:
            if args is not None and args != []:
                function(*args)
            else:
                function()
        elif function is not None:
            if args is not None and args != [] and executeImmediately:
                function(*args)
            elif executeImmediately:
                function()
            elif args is not None and args != []:  
                acknowledge(function, *args)
            else:
                acknowledge(function, ())
        else:
            acknowledge(previousMode, True)

def set_litany(person, litany):
    person.litany = litany

def converse_with_interpreter(keyEvent):
    global conversationPartner
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if 0 < num and num <= len(allNodes[conversationPartner.litany].children):
            if DEBUG:
                global previousConversation
                previousConversation = conversationPartner.litany
            conversationPartner.litany = allNodes[conversationPartner.litany].children[num-1].index
            assert isinstance(conversationPartner.litany, int), "Problem node:%r" % previousConversation.litany
            converse_with(conversationPartner, previousMode)
    elif keyEvent.key == K_RETURN and (allNodes[conversationPartner.litany].children is None or allNodes[conversationPartner.litany].children == []):
        previousMode()
    #Note: This DOES NOT attempt to maintain any sort of consistent state. It's merely to allow the debugger to easily look at all the text in the conversation. In order
    #to ensure that the states are being modified correctly, one needs to play the conversations normally (i.e. without backtracking).
    if DEBUG:
        if keyEvent.key == K_ESCAPE:
            pass
            #quit()
        elif keyEvent.key == K_BACKSPACE:
            conversationPartner.litany = previousConversation
            converse_with(conversationPartner, previousMode)


#A mapping from litany numbers to the actual litanies. Note: We use a map rather than array because there could be holes in the integers (i.e. because we didn't load a particular scene).
allNodes = {}
#A mapping from the name of each litany to the actual litany.
allNodeNames = {}
def empty_quip_function():
    pass
class Node(universal.RPGObject):
    def __init__(self, index, name=''):
        self.quip = ''
        self.children = []
        self.playerComments = []
        self.quip_function = empty_quip_function
        self.comment = None
        self.index = index
        self.music = None
        self.name = name
        if name:
            #assert not name in allNodeNames, "Name '''%s''' is already taken." % name
            allNodeNames[name] = self
        #assert not index in allNodes, "Index %d is already taken." % index 
        allNodes[index] = self

    def add_child(self, child):
        if not self.children:
            self.children = [child]
        elif not child in self.children:
            self.children.append(child)

    def add_player_comment(self, comment):
        if not self.playerComments:
            self.playerComments = [comment]
        elif not comment in self.playerComments:
            self.playerComments.append(comment)

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(dataList):
        raise NotImplementedError()

    def add_song(self, song):
        try:
            self.music.append(song)
        except AttributeError:
            if self.music is None:
                self.music = [song]
            else:
                self.music = [self.music, song]


emptyLitany = Node(0)
emptyLitany.quip = '''There is nothing more to be said.'''
emptyLitany.quip_function = empty_quip_function 

