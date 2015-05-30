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
from __future__ import print_function
import transExceptions
import ast
import re


class bcolors:
        HEADER = '\033[95m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        ENDC = '\033[0m'

COLOR = True
def color(text, color):
    if COLOR:
        return color + text + bcolors.ENDC
    else:
        return text


def color_line(lineNum):
    return "Line " + color(str(lineNum), bcolors.BLUE)

TAB= ' ' * 4
BEGIN_OPEN_SCENE = r'\begin{openScene}'
END_OPEN_SCENE = r'\end{openScene}'
BEGIN_CLOSE_SCENE = r'\begin{closeScene}'
END_CLOSE_SCENE = r'\end{closeScene}'
BEGIN_CODE = r'\begin{code}'
END_CODE = r'\end{code}'
BEGIN_SCENE = r'openScene'
BEGIN_NODE = r'\begin{node}'
END_NODE = r'\end{node}'
BEGIN_CHILD_NODE = r'\begin{childnode}'
END_CHILD_NODE = r'\end{childnode}'

BEGIN = r'\begin'
END = 'r\end'

nodeNum = 0

codeCommands = {
        r'\keyword':('''pwutilities.add_keyword(''', 1),
        r'\music':("universal.say('\m') ; universal.playedMusic.put(", 1)
        }

inlineCommandsPlayer = {
    r'\hisher':("person.hisher()",),
    r'\HisHer':("person.HisHer()",),  
    r'\himher':("person.himher()",), 
    r'\HimHer':("person.HimHer()",),  
    r'\heshe':("person.heshe()",),  
    r'\HeShe':("person.HeShe()",),  
    r'\heshell':("person.heshell()",),  
    r'\HeShell':("person.HeShell()",),  
    r'\himselfherself':("person.himselfherself()",),  
    r'\HimselfHerself':("person.HimselfHerself()",),  
    r'\mistermiss':("person.mistermiss()",),  
    r'\MisterMiss':("person.MisterMiss()",),  
    r'\manwoman':("person.manwoman()",),  
    r'\ManWoman':("person.ManWoman()",),  
    r'\trousers':("universal.state.player.clothing_below_the_waist().name",),
    r'\hishers':("person.hishers()",),  
    r'\HisHers':("person.HisHers()",),  
    r'\boygirl':("person.boygirl()",),  
    r'\BoyGirl':("person.BoyGirl()",),  
    r'\manlady':("person.manlady()",),  
    r'\ManLady':("person.ManLady()",),  
    r'\kingqueen':("person.kingqueen()",),  
    r'\KingQueen':("person.KingQueen()",),  
    r'\lordlady':("person.lordlady()",),  
    r'\LordLady':("person.LordLady()",),  
    r'\brothersister':("person.brothersister()",),  
    r'\BrotherSister':("person.BrotherSister()",),  
    r'\menwomen':("person.menwomen()",),  
    r'\MenWomen':("person.MenWomen()",),  
    r'\sirmaam':("person.sirmaam()",),  
    r'\SirMaam':("person.SirMaam()",),  
    r'\underwearpanties':("person.underwearpanties()",  ),
    r'\bastardbitch':("person.bastardbitch()",  ),
    r'\BastardBitch':("person.BastardBitch()",  ),
    r'\weaponName':("universal.state.player.weapon().name",  ),
    r'\name':("universal.state.player.name",  ),
    r'\fakename':("universal.state.player.fakeName",  ),
    r'\names':('''universal.state.player.name, "'s"''',),
    r'\nickname':("universal.state.player.nickname",  ),
    r'\nicknames':("universal.state.player.nickname, 's'",),
    r'\weapon':("universal.state.player.weapon().name",),
    r'\player':("universal.state.player",),
    r'\cladbottom':("universal.state.player.clad_bottom(",),
    r'\muscleadj': ("universal.state.player.muscle_adj()",),
    r'\bumadj': ("universal.state.player.bum_adj()",),
    r'\quiver': ("universal.state.player.quiver()",),
    r'\quivering':("universal.state.player.quivering()",),
    r'\liftlower': ("items.liftlower(universal.state.player.lower_clothing()",),
    r'\lowerlift': ("items.lowerlift(universal.state.player.lower_clothing()",),
    r'\liftslowers': ("items.liftlower(universal.state.player.lower_clothing()",),
    r'\lowerslifts': ("items.lowerslifts(universal.state.player.lower_clothing()",),
    r'\pajamabottoms': ("universal.state.player.pajama_bottom().name",),
    r'\pajamas':("universal.state.player.pajama_top().name",),
    r'\underwear':("universal.state.player.underwear().name",),
    r'\shirt':("universal.state.player.shirt().name",),
    r'\speed':("universal.state.player.speed()",),
    r'\warfare':("universal.state.player.warfare()",),
    r'\magic':("universal.state.player.magic()",),
    r'\grapple':("universal.state.player.grapple()",),
    r'\resilience':("universal.state.player.resilience()",),
    r'\keywords':("universal.state.player.keywords",),
    r'\sondaughter':("person.sondaughter()",),
    r'\SonDaughter':("person.SonDaughter()",),
    r'\waistbandhem':("universal.state.player.lower_clothing().waistband_hem()",),
    r'\pjwaistbandhem':("universal.state.player.pajama_bottom().waistband_hem()",),
    r'\hemwaistband':("universal.state.player.lower_clothing().hem_waistband()",),
    r'\pjhemwaistband':("universal.state.player.pajama_bottom().hem_waistband()",),
    r'\pheight':("person.height_based_msg(universal.state.player, ", 4),
    r'\pbodytype':("person.bodytype_based_msg(universal.state.player, ", 4),
    r'\pmusculature':("person.musculature_based_msg(universal.state.player, ",3),
    r'\phairlength':("person.hair_length_based_msg(universal.state.player, ",4),
    r'\ppjtype': ("items.dropseat_based_msg(universal.state.player, ", 3),
    r'\pisliftedlowered':("items.liftlowered_based_msg(universal.state.player, ", 2),
    r'\pisloweredlifted':("items.loweredlifted_based_msg(universal.state.player, ", 2),
    r'\ptrousers':("items.wearing_trousers(universal.state.player, ", 3),
    r'\pdress':("items.wearing_dress(universal.state.player, ", 3),
    r'\pwearingunderwear':("items.wearing_underwear(universal.state.player, ", 2),
    #Note: This is not ideal, because it has itemspotionwars baked in. Need to figure out an alternative.
    r'\phasbelt':("itemspotionwars.has_belt(universal.state.player, )", 2),
    r'\pisbaring':("items.baring_underwear(universal.state.player.underwear(), ", 3),
    r'\pistight':("items.tight_msg(universal.state.player.lower_clothing(), ", 2),
    r'\pisloose':("items.loose_msg(universal.state.player.lower_clothing(), ", 2),
    r'\pwearingshirt':("items.wearing_shirt(universal.state.player, ", 3),
    r'\pwearingdress':("items.wearing_dress(universal.state.player, ", 3),
    r'\isfemale':("person.is_female_msg(universal.state.player, ", 2),
    r'\stageDirections':("pwutilities.stage_directions(", 1),
    r'\ppajamatype':("items.pajama_type_msg(universal.state.player,", 3),
    }

#The first line of all these commands is code: the person to apply the function to.
inlineCommands = {
    #r'\hisher':("person.hisher(universal.state.get_character(", 1),
    #r'\HisHer':("person.HisHer(universal.state.get_character(", 1),
    #r'\himher':("person.himher(universal.state.get_character(", 1), 
    #r'\HimHer':("person.HimHer(universal.state.get_character(", 1),
    #r'\heshe':("person.heshe(universal.state.get_character(", 1), 
    #r'\HeShe':("person.HeShe(universal.state.get_character(",  1),
    #r'\heshell':("person.heshell(universal.state.get_character(", 1),  
    #r'\HeShell':("person.HeShell(universal.state.get_character(", 1),  
    #r'\himselfherself':("person.himselfherself(universal.state.get_character(", 1),  
    #r'\HimselfHerself':("person.HimselfHerself(universal.state.get_character(", 1),  
    #r'\mistermiss':("person.mistermiss(universal.state.get_character(", 1),  
    #r'\MisterMiss':("person.MisterMiss(universal.state.get_character(", 1),  
    #r'\manwoman':("person.manwoman(universal.state.get_character(", 1),  
    #r'\ManWoman':("person.ManWoman(universal.state.get_character(", 1),  
    #r'\hishers':("person.hishers(universal.state.get_character(", 1),  
    #r'\HisHers':("person.HisHers(universal.state.get_character(", 1),  
    #r'\boygirl':("person.boygirl(universal.state.get_character(", 1),  
    #r'\BoyGirl':("person.BoyGirl(universal.state.get_character(", 1),  
    #r'\manlady':("person.manlady(universal.state.get_character(", 1),  
    #r'\ManLady':("person.ManLady(universal.state.get_character(", 1),  
    #r'\kingqueen':("person.kingqueen(universal.state.get_character(", 1),  
    #r'\KingQueen':("person.KingQueen(universal.state.get_character(", 1),  
    #r'\lordlady':("person.lordlady(universal.state.get_character(", 1),  
    #r'\LordLady':("person.LordLady(universal.state.get_character(", 1),  
    #r'\brothersister':("person.brothersister(universal.state.get_character(", 1),  
    #r'\BrotherSister':("person.BrotherSister(universal.state.get_character(", 1),  
    #r'\menwomen':("person.menwomen(universal.state.get_character(", 1),  
    #r'\MenWomen':("person.MenWomen(universal.state.get_character(", 1),  
    #r'\sirmaam':("person.sirmaam(universal.state.get_character(", 1),  
    #r'\SirMaam':("person.SirMaam(universal.state.get_character(", 1),  
    #r'\bastardbitch':("person.bastardbitch(universal.state.get_character(", 1),  
    #r'\BastardBitch':("person.BastardBitch(universal.state.get_character(", 1),  
    r'\oweaponName':("items.weapon_name(", 1),  
    r'\oweapon':("items.weapon_name(", 1),
    r'\ocladbottom': ("items.clad_bottom(", 1),
    r'\omuscleadj': ("person.muscle_adj(", 1),
    r'\obumadj': ("person.bum_adj(", 1),
    r'\oliftlower': ("items.liftlower(", 1),
    r'\olowerlift': ("items.lowerlift(", 1),
    r'\oliftslowers': ("items.liftslowers(", 1),
    r'\olowerslifts': ("items.lowerslifts(", 1),
    r'\ounderwear':("items.underwear_name(", 1),
    r'\otrousers': ("items.lower_clothing_name(", 1),
    r'\opajamabottoms': ("items.pajama_bottom_name(", 1),
    r'\ospeed': ("person.speed(", 1),
    r'\owarfare': ("person.warfare(", 1),
    r'\omagic': ("person.magic(", 1),
    r'\ograpple': ("person.grapple(", 1),
    r'\oresilience': ("person.resilience(", 1),
    r'\owaistbandhem': ("items.waistband_hem(", 1),
    r'\ohemwaistband': ("items.hem_waistband(", 1),
    r'\oheight':("person.height_based_msg(", 5),
    r'\obodyType':("person.bodytype_based_msg(",5),
    r'\omusculature':("person.musculature_based_msg(",4),
    r'\ohairlength':("person.hair_length_based_msg(",5),
    r'\opjtype': ("items.dropseat_based_msg(", 3),
    r'\oisliftedlowered':("items.liftlowered_based_msg(", 3),
    r'\oisloweredlifted':("items.loweredlifted_based_msg(", 3),
    r'\oisliftedlowered':("items.liftlowered_based_msg(", 3),
    r'\cond':("universal.cond(", 3),
    r'\bummarks':("pwutilities.bummarks(", 2),
    r'\opajamatype':("items.pajama_type_msg(", 4),
    r'\itthem':("items.itthem(", 1),
    r'\oshirt':("items.shirt_name(", 1)
    }




parseTreeNodeNum = 0

class ParseTree(object):
    """
    A parse tree is a recursive data structure that takes:
        1. lineNum: The line number in the original LaTeX file in which the token appears
        2. children: An iterable of ParseTrees that represent this node's children.
        3. parent: The node's parent.
        4. data: The data (if any) associated with this node. For example, a childnode type 
        tree would have the name of the node. A node would have the name of the node, 
            and the person you are conversing with. Text node, would have the text 
            associated with that node.
    """
    def __init__(self, episodeNum, lineNum=0, children=None, parent=None, data=None):
        self.lineNum = lineNum
        self.parent = parent
        self.children = children if children else []
        self.data = data if data else []
        self.episodeNum = episodeNum
        global parseTreeNodeNum
        self.parseTreeNodeNum = parseTreeNodeNum
        self.init_name = ''.join(['init_episode_', str(episodeNum)])
        parseTreeNodeNum += 1


    def __repr__(self):
        return '\n'.join([color('--------Start Node ' + str(self.parseTreeNodeNum) + '----------', bcolors.GREEN), color("nodeType: ", bcolors.GREEN) + str(self.__class__.__name__), color("data: ", bcolors.YELLOW) + str(self.data), 
            color("lineNum: ", bcolors.BLUE) + str(self.lineNum),
            color("parent: ", bcolors.RED) + str(self.parent.parseTreeNodeNum) if self.parent else 'None',
            color("children:\n", bcolors.RED) + '**********\n'.join("child " + str(n) + ":\n" + str(child) for (n, child) in zip(range(len(self.children)), self.children)), 
            color('---------End Node ' + str(self.parseTreeNodeNum) + '------------', bcolors.GREEN)])

    def node_name(self):
        return ''
                
    def translate(self):            
        """
        Returns an iterable of python lines that implement the parse tree rooted at this node.
        """
        raise NotImplementedError()


class Root(ParseTree):

    def __init__(self, episodeNum, charRoomsModuleName, lineNum=0, children=None, parent=None, data=None):
        super(Root, self).__init__(episodeNum, lineNum, children, parent, data)
        self.charRoomsModuleName = charRoomsModuleName

    def translate(self):
        code = [''.join(['def ', self.init_name, '():'])]
        code.append(''.join([TAB, self.charRoomsModuleName, '.build_chars()']))
        code.append(''.join([TAB, self.charRoomsModuleName, '.build_rooms()']))
        code.extend(''.join([TAB, 'init_scene_', str(sceneNum), '_episode_', str(self.episodeNum), '()']) for sceneNum in range(1, OpenScene.sceneNum))
        for child in self.children:
            code.extend(child.translate())
        return code


class OpenScene(ParseTree):

    sceneNum = 1

    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(OpenScene, self).__init__(parent.episodeNum, lineNum, children, parent)
        self.startToken = BEGIN_OPEN_SCENE
        self.endToken = END_OPEN_SCENE
        self.data = [''.join(['def start_scene_', str(OpenScene.sceneNum), '_episode_', str(self.episodeNum), '(loading=False):'])] + (data if data else [])
        self.sceneNum  = OpenScene.sceneNum
        OpenScene.sceneNum += 1


    def translate(self):
        openSceneCode = [line.replace('\n', '') for line in self.data]
        openSceneCode.extend([''.join(['\n\n', 'def init_scene_', str(self.sceneNum), '_episode_', str(self.episodeNum), '():'])])
        openSceneCode.extend([TAB + ('\n' + TAB).join(child.translate()) for child in self.children])
        return openSceneCode 


class CloseScene(ParseTree):

    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(CloseScene, self).__init__(parent.episodeNum, lineNum, children, parent)
        self.startToken = BEGIN_CLOSE_SCENE
        self.endToken = END_CLOSE_SCENE
        #Because close scene comes after open scene, the associated scene number for close scene will be one less than what is currently stored (because OpenScene.sceneNum increments every
        #time a new open scene node is created).
        self.data = [''.join(['def end_scene_', str(OpenScene.sceneNum-1), '_episode_', str(self.episodeNum), '():'])] + (data if data else [])
        

    def translate(self):
        closeSceneCode = [line.replace('\n', '') for line in self.data]
        closeSceneCode.extend([TAB + ('\n' + TAB).join(child.translate()) for child in self.children])
        return closeSceneCode 

class AbstractNode(ParseTree):

    def translate(self):
        nodeName = self.data[0].replace(' ', '_')
        if not re.match(re.compile(r'^\w+$'), nodeName):
            raise transExceptions.TranslationError(' '.join([color("Error", bcolors.RED), color_line(self.lineNum), "Invalid character in node name: ", color(self.data[0], bcolors.GREEN), 
                "Only alphanumeric characters and spaces allowed in node names."]))
        childrenCode = [child.translate() for child in self.children]
        nodeText = []
        linkCode = []
        buildNode = [''.join([nodeName, ' = conversation.Node(', str(self.nodeNum), ', ', "'''", self.data[0], "'''", ')']), '', '',
                ''.join(['def ', nodeName, '_qf():'])] 
        for childCode, codeType in childrenCode:
            if codeType == 'text':
                if childCode[0] != '[]':
                    nodeText.append(childCode)
            elif codeType == 'code':
                buildNode.extend(TAB + line for line in childCode)
            elif codeType == 'link':
                linkCode.extend([TAB + line for line in childCode])
        #This line is being generated solely so that the quip for the node is not zero. This is necessary to ensure that we show the children. It's a hack required by a hack required by episode 1.
        #Note: I REALLY need to simplify the conversation node structure. It is loaded with hacks and workarounds. The whole damn thing really needs to be simplified. I'll wait until I've 
        #transcribed episode 1 into 
        #latex though, first. Then, I can remove the .quip infrastructure that's complicating everything.
        buildNode.append(''.join([TAB, nodeName, '.quip = " "' ]))
        buildNode.extend([''.join([TAB, 'universal.say(universal.format_text_translate([', ', '.join(nodeText), ']), justification=0)'])])
        buildNode.extend(linkCode)
        buildNode.append(''.join([nodeName, '.quip_function = ', nodeName, '_qf']))
        return buildNode

    def node_name(self):
        return self.data[0].replace(' ', '_')

class Node(AbstractNode):

    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(Node, self).__init__(parent.episodeNum, lineNum=lineNum, children=children, parent=parent, data=data)
        self.startToken = BEGIN_NODE
        self.endToken = END_NODE
        global nodeNum
        self.nodeNum = nodeNum
        nodeNum += 1
        conversationPartner = self.data[2]
        ancestor = parent
        try:
            while ancestor.startToken != BEGIN_OPEN_SCENE:
                ancestor = ancestor.parent
        except AttributeError:
            raise TranslationError(' '.join([errorMsg, color_line(self.lineNum), "Node exists outside of a Scene. Either you've forgotten an open scene environment before this node, or you are including a node after the last close scene environment."]))

        #data[2] is the character with whom the player is speaking.
        if conversationPartner.lower() == 'self':
            ancestor.data.append(TAB + 'if not loading:')
            ancestor.data.extend([''.join([TAB*2, 'universal.state.player.litany = conversation.allNodes[', str(self.nodeNum), ']']),
                                  ''.join([TAB*2, 'conversation.converse_with(universal.state.player, townmode.town_mode)'])])
        else:
            ancestor.data.append(TAB + 'if not loading:')
            ancestor.data.append(''.join([TAB*2, data[2].lower(), ' = ', "universal.state.get_character('''",  data[2], ".person''')"]))
            ancestor.data.append(''.join([TAB*2, data[2].lower(), '.litany = conversation.allNodes[', str(self.nodeNum), ']']))


    
class ChildNode(AbstractNode):

    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(ChildNode, self).__init__(parent.episodeNum, lineNum=lineNum, children=children, parent=parent, data=data)
        self.startToken = BEGIN_CHILD_NODE
        self.endToken = END_CHILD_NODE
        global nodeNum
        self.nodeNum = nodeNum
        nodeNum += 1

errorMsg = color("Error", bcolors.RED)

class CodeCommands(ParseTree):
    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(CodeCommands, self).__init__(parent.episodeNum, lineNum, children, parent, data)

    def translate(self):
        command, numArgs = codeCommands[self.data[0]]
        return ([command + ','.join(self.data[1:numArgs+1]) + ')'], 'code')
    

class Code(ParseTree):

    def __init__(self, lineNum=None, children=None, parent=None, data=None):
        super(Code, self).__init__(parent.episodeNum, lineNum, children, parent, data)


    def translate(self):
        initialSpacing = ''
        count = 0 
        self.data = [line for line in self.data if line]
        fixedLines = []
        for line in self.data:
            newLines = line.splitlines()
            line = ''.join(line for line in newLines if line.strip())
            fixedLines.append(line)
        self.data = fixedLines
        try:
            char = self.data[count][0]
        except IndexError:
            char = ''
        while char.isspace():
            initialSpacing += char
            count += 1
            try:
                char = self.data[0][count]
            except IndexError:
                break
        code = [line.replace(initialSpacing, '', 1) for line in self.data]
        try:
            ast.parse('\n'.join(code))
        except SyntaxError, e:
            import sys
            global errorMsg
            raise transExceptions.TranslationError(' '.join([errorMsg, color_line(self.lineNum), "Invalid Python Syntax found in Python code:\n\n", '\n'.join(code), "Python error:\n\n", str(e)]))
        return (code, 'code')


PUNCTUATION_NO_SPACE_FOLLOWING = ['"("', '""', '"--"', '"-"']

PUNCTUATION_NO_SPACE_PRECEDING = ['"."', '","', '"!"', '"?"', '")"', '".)"', '"?)"', '"!)"', '"--"', '"-"']

QUOTE = "'\"'"

class Paragraph(ParseTree):
    """
        Represents a paragraph of text and/or inlineCommands, defined as chunks of text separated by two or more newlines.
    """

    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(Paragraph, self).__init__(parent.episodeNum, lineNum, children, parent, data)

    def translate(self):
        translatedText = [child.translate() for child in self.children]
        quoteSeen = False
        for i in range(len(translatedText)):
            text = translatedText[i]
            if not text:
                continue
            try:
                nextText = translatedText[i+1]
            except IndexError:
                nextText = ''
            if text.strip() == QUOTE:
                if quoteSeen:
                    translatedText[i] = ' '.join(["''.join([", text, ", ' '])"])
                else:
                    translatedText[i] = ' '.join(["''.join([", text, "])"])
                quoteSeen = not quoteSeen
            elif nextText.strip() == QUOTE:
                if not quoteSeen:
                    translatedText[i] = ' '.join(["''.join([", text, ", ' '])"])
                else:
                    translatedText[i] = ' '.join(["''.join([", text, "])"])
            elif text.strip() not in PUNCTUATION_NO_SPACE_FOLLOWING and nextText.strip() not in PUNCTUATION_NO_SPACE_PRECEDING: 
                translatedText[i] = ' '.join(["''.join([", text, ", ' '])"])
        return ('[' + ', '.join(translatedText) + ']', 'text')

class Text(ParseTree):
    "A node in the parse tree that contains a string of one or more words (where words are strings of any alphanumeric characters but whitespace)."

    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(Text, self).__init__(parent.episodeNum, lineNum, children, parent, data)

    def translate(self):
        text = ' '.join(self.data)
        if text == '"':
            return "'" + text + "'\n"
        else:
            return '"' + text + '"\n'

#This is returned when translating empty text.
EMPTY_TEXT_TRANSLATION = '[""]'

class InlineCommand(ParseTree):
    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(InlineCommand, self).__init__(parent.episodeNum, lineNum, children, parent, data)

    def translate(self):
        try:
            code = inlineCommandsPlayer[self.data[0]]
        except KeyError:
            code, numArgs = inlineCommands[self.data[0]]
        else:
            try:
                code, numArgs = code
            except ValueError:
                code = code[0]
                numArgs = 0
            else:
                assert(int(numArgs))
        numParens = code.count('(') - code.count(')')
        translatedChildren = [child.translate()[0] for child in self.children]
        translatedChildren = [translatedChild for translatedChild in translatedChildren if translatedChild != EMPTY_TEXT_TRANSLATION]
        if translatedChildren:
            check = ''
            if self.data[0] in inlineCommands:
            #Note: Since the first argument is code, the first argument is a list of lines of code, whose list contains a single line of code.
                check = translatedChildren[0][0]
                translatedChildren = translatedChildren[1:]
            translatedChildren = [check] + ["''.join(" + child + ")" for child in translatedChildren]
            return ''.join([code, ', '.join(child for child in translatedChildren if child.strip()), ')' * numParens])
        else:
            return code

class Destination(ParseTree):
    """
    Contains information on the destination node of a child command.
    """
    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(Destination, self).__init__(parent.episodeNum, lineNum=lineNum, children=children, parent=parent, data=data)

    def translate(self):
        return '_'.join([word.strip() for word in self.data if word.strip()])

class Link(ParseTree):
    """
    Handles commands that connect one node to another, i.e. \\child, \\childif, and \\continue.
    """
    def __init__(self, lineNum=0, children=None, parent=None, data=None):
        super(Link, self).__init__(parent.episodeNum, lineNum=lineNum, children=children, parent=parent, data=data)

    def translate(self):
        nodeName = '_'.join(self.data[0].split())
        cmd = self.data[-1]
        if cmd == r'\continue' or cmd == r'\continueNewPage':
            newPage = cmd == r'\continueNewPage'
            #import sys
            destination = self.extract_destination(0)
            destination = destination.replace("'''", '')
            linkCode = [''.join(['return conversation.continue_to_node(', nodeName, ', ', destination, ', ', str(newPage), ')'])]
            return (linkCode, 'link')
        elif cmd == r'\childif' or cmd == r'\childelif':
            #The test is a code node, and the translate of the code node returns a pair of text with code.
            test = ' '.join(self.children[0].translate()[0])
            destination = self.extract_destination(1)
            linkCode = [''.join([TAB, 'return conversation.continue_to_node(', nodeName, ', ', destination, ')'])]
            return ([''.join(['if ' if cmd == r'\childif' else 'elif ', test, ':'])] + linkCode, 'link')
        elif cmd == r'\child':
            playerComment = ''.join(['universal.format_line_translate(', self.children[0].translate()[0], ')'])
            destination = self.extract_destination(1)
            destination = destination.replace("'''", '')
            return ([''.join([nodeName, '.add_child(', destination, ')']),
                     ''.join([nodeName, '.add_player_comment(', playerComment, ')'])], 'link')
        else:
            raise transExceptions.TranslationError(' '.join([color("Error", bcolors.RED), color_line(self.lineNum), "Invalid linking command:", cmd]))

    def extract_destination(self, destinationArg):
        return self.children[destinationArg].translate()
        #Either the destination is a pair: ([list of words], 'code') if the link is a child, or
        #destination is a singleton list: [string].
