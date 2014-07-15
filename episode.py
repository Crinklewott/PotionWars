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
import conversation
import abc
import music
import person

allEpisodes = {}
postTitleCardFunction = None
postTitleCardFuncArgs = None

def set_post_title_card(postTitleCardFunctionIn, postTitleCardFuncArgsIn):
    global postTitleCardFunction, postTitleCardFuncArgs
    postTitleCardFunction = postTitleCardFunctionIn
    postTitleCardFuncArgs = postTitleCardFuncArgsIn

class Episode(universal.RPGObject):
    def __init__(self, num, name, nextEpisode=None, scenes=None, currentSceneIndex=0, titleTheme=None):
        self.num = num
        self.name = name
        self.scenes = scenes
        self.currentSceneIndex = 0
        self.nextEpisode = nextEpisode
        self.titleTheme = titleTheme
        universal.state.add_episode(self)

    def start_episode(self, *startingSceneArgs):
        global postTitleCardFunction, postTitleCardFuncArgs
        universal.get_screen().fill(universal.DARK_GREY)
        music.play_music(self.titleTheme)
        universal.display_text('Episode ' + str(self.num) + ':\n' + self.name, universal.get_world_view(), universal.get_world_view().midleft, isTitle=True)
        """
        if startingSceneArgs is None:
            startingSceneArgs = (self,)
        else:
            startingSceneArgs = (self,) + startingSceneArgs
        """
        #print('printing starting scene args')
        universal.acknowledge(self.initialize_episode, *startingSceneArgs)

    def initialize_episode(self, *startingSceneArgs):       
        conversation.maxIndex = 0
        print('starting scene currentSceneIndex: ')
        print(self.currentSceneIndex)
        if startingSceneArgs is ():
            self.scenes[self.currentSceneIndex].startScene()
        else:
            self.scenes[self.currentSceneIndex].startScene(*startingSceneArgs)
        try:
            print(postTitleCardFuncArgs)
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
        universal.state.player.currentEpisode = self.nextEpisode
        universal.state.player.currentEpisode.start_episode()

    def next_scene(self, previousSceneArgs=(), startingSceneArgs=()):
        if self.scenes[self.currentSceneIndex].endScene is not None:
            if previousSceneArgs is ():
                self.scenes[self.currentSceneIndex].previousSceneArgs()      
            else:
                self.scenes[currentSceneIndex].endScene(*previousSceneArgs)
        self.currentSceneIndex += 1
        if startingSceneArgs is ():
            self.scenes[self.currentSceneIndex].startScene()
        else:
            self.scenes[self.currentSceneIndex].startScene(*startingSceneArgs)

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(loadData):
        raise NotImplementedError()

allScenes = None
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
        universal.state.add_scene(self)

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(loadData):
        raise NotImplementedError()

