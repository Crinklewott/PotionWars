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

conversationPartner = None
previousConversation = None
previousMode = None
maxIndex = 0
SPLIT = -50
def converse_with(person, previousModeIn):
    global conversationPartner
    conversationPartner = person
    print(conversationPartner.name)
    if person.litany is not None:
        litany = person.litany
    elif person.defaultLitany is not None:
        litany = person.defaultLitany
    else:
        litany = emptyLitany
    global previousMode
    previousMode = previousModeIn
    say_title(person.printedName)
    say_node(litany)


def say_node(litanyIndex):
    #This may appear redundant, but it's possible for a node's quip_function to immediately invoke a different node, without going through the player. In that case,
    #we need to make sure that the current litany of the conversationPartner is properly updated.
    global previousMode
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
            #universal.playedMusic.queue.clear()
            universal.say(litany.quip, justification=0, music=litany.music)
        else:
            universal.say(litany.quip, justification=0)
    if function == SPLIT:
        litany.quip_function = result[1]
        acknowledge(say_node, (litany))
        return
    elif litany.playerComments is not None and litany.playerComments is not []:
        universal.say('\p')
        universal.say('\n'.join([str(i) + '. ' + comment for (i, comment) in zip([i for i in range(1, len(litany.playerComments)+1)], litany.playerComments)]), justification=0)
        set_commands(['(#)Select a number.'])
        set_command_interpreter(converse_with_interpreter)
    elif litany.children is not None:
        playerComments = [child.comment for child in litany.children]
        universal.say('\p')
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
        if DEBUG:
            try:
                print(conversationPartner.litany.index)
            except AttributeError:
                pass
        if 0 < num and num <= len(allNodes[conversationPartner.litany].children):
            if DEBUG:
                global previousConversation
                previousConversation = conversationPartner.litany
            conversationPartner.litany = allNodes[conversationPartner.litany].children[num-1].index
            assert isinstance(conversationPartner.litany, int), "Problem node:%r" % previousConversation.litany
            converse_with(conversationPartner, previousMode)
    elif keyEvent.key == K_RETURN and (allNodes[conversationPartner.litany].children is None or 
        allNodes[conversationPartner.litany].children == []):
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


allNodes = {}
class Node(universal.RPGObject):
    def __init__(self, index):
        self.quip = ''
        self.children = None
        self.playerComments = None
        self.quip_function = None
        self.comment = None
        self.index = index
        self.music = None
        assert not index in allNodes, "Index %d is already taken." % index 
        allNodes[index] = self

    def add_child(self, child):
        if not child in self.children:
            self.children.append(child)

    def add_player_comment(self, comment):
        if not comment in self.playerComments:
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

