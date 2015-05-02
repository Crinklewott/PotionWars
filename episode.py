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
import conversation
import abc
import music
import person

allEpisodes = {}
postTitleCardFunction = None
postTitleCardFuncArgs = None

def set_post_title_card(postTitleCardFunctionIn, postTitleCardFuncArgsIn=None):
    global postTitleCardFunction, postTitleCardFuncArgs
    postTitleCardFunction = postTitleCardFunctionIn
    postTitleCardFuncArgs = postTitleCardFuncArgsIn

class Episode(universal.RPGObject):
    def __init__(self, num, name, nextEpisode=None, scenes=None, currentSceneIndex=0, titleTheme=None, init=None):
        self.num = num
        self.name = name
        self.scenes = scenes
        self.currentSceneIndex = 0
        self.nextEpisode = nextEpisode
        self.titleTheme = titleTheme
        self.init = init
        allEpisodes[name] = self


    def start_episode(self, *startingSceneArgs):
         global postTitleCardFunction, postTitleCardFuncArgs
         universal.get_screen().fill(universal.DARK_GREY)
         music.play_music(self.titleTheme)
         universal.state.player.clear_marks()
         self.init()
         universal.display_text('Episode ' + str(self.num) + ':\n' + self.name, universal.get_world_view(), universal.get_world_view().midleft, isTitle=True)
         universal.acknowledge(self.initialize_episode, *startingSceneArgs)

    def initialize_episode(self, *startingSceneArgs):
         conversation.maxIndex = 0
         if startingSceneArgs is ():
             self.scenes[self.currentSceneIndex].startScene()
         else:
             self.scenes[self.currentSceneIndex].startScene(*startingSceneArgs)
             try:
                 postTitleCardFunction(*postTitleCardFuncArgs)
             except TypeError:
                 try:
                     postTitleCardFunction()
                 except TypeError:
                     pass


    def end_episode(self, endingSceneArgs=()):
        if endingSceneArgs is ():
            self.scenes[self.currentSceneIndex].endScene()
        else:
            self.scenes[self.currentSceneIndex].endScene(*endingSceneArgs)
        universal.state.player.currentEpisode = self.nextEpisode.name
        #set_post_title_card(allEpisodes[universal.state.player.currentEpisode].init)
        universal.state.clear_one_time_encounters()
        allEpisodes[universal.state.player.currentEpisode].start_episode()

    def next_scene(self, previousSceneArgs=(), startingSceneArgs=()):
        if self.scenes[self.currentSceneIndex].endScene:
            if previousSceneArgs is ():
                self.scenes[self.currentSceneIndex].endScene()      
            else:
                self.scenes[currentSceneIndex].endScene(*previousSceneArgs)
        self.currentSceneIndex += 1
        try:
            if self.scenes[self.currentSceneIndex].init_scene:
                self.scenes[self.currentSceneIndex].init_scene()
        except IndexError:
           import pwutilities
           pwutilities.exitLeft(universal.state.player, universal.state.location)
           end_content_mode()
        else:
            if startingSceneArgs is ():
                self.scenes[self.currentSceneIndex].startScene()
            else:
                self.scenes[self.currentSceneIndex].startScene(*startingSceneArgs)

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(loadData):
        raise NotImplementedError()

def end_content_mode():
    universal.say(universal.format_line(['''That's the end of the content, I hope you've enjoyed playing this far. If you have any comments, criticisms, questions, bug reports, or anything else, either comment on my blog''',
            '''spankingrpgs.blogspot.com, or send me an e-mail at sprpgs@gmail.com (please post bug reports on the blog however, so that others can see them). Criticisms are welcome, however please keep them constructive. Saying "This game''',
            '''sucks!" tells me nothing except that you didn't like it. Saying "Your combat system felt unbalanced. The magic was way too powerful." tells  me much much more.''']), justification=0)
    universal.set_commands(['(Esc) To exit'])
    universal.set_command_interpreter(quit_interpreter)

allScenes = {}


class Scene(universal.RPGObject):
    """
        A scene has a name, a startFunction, and an endFunction.
        The startFunction is a function that is invoked when the scene begins.
        The endFunction is a function that is invoked when the scene ends.
        Note that the functions can have arbitrary arguments, however you need to make sure to pass the correct arguments to the
        next_scene() method of the current episode.
    """
    def __init__(self, name, startScene, endScene):
        self.name = name
        self.startScene = startScene
        self.endScene = endScene
        allScenes[name] = self
        self.init_scene = None

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(loadData):
        raise NotImplementedError()

