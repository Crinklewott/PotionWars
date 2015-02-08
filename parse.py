from enum import Enum
import ast
import difflib
import transExceptions
import parseTree

#Mapping from the command, to the number of arguments the command takes.
childrenCommands = {r'\childif':2, r'\childelif':2, r'\child':2, r'\continue':1, r'\continueNewPage':1}



#A mapping from latex commands to a tuple containing the start of the python code, and the number of arguments the latex command takes.




error = parseTree.color("Error", parseTree.bcolors.RED)

def color_line(lineNum):
    return parseTree.color_line(lineNum)

def open_scene(tokenIterator, parent):
    """
        Given an iterable of (token, line number) pairs, constructs the ParseTree associated with the openScene environment (which is raw Python code).
        Since I don't need to do anything with the code except print it to the file, the full bulk of python code is treated as a single node in the parse tree.
    """
    def compute_indent(codeLine):
        count = 0
        for char in codeLine:
            if char == ' ':
                count += 1
            else:
                return count
        return count

    count = 0
    pythonLine = ''
    pythonCode = []
    #parseNodes = []
    startLine = 0
    for token, lineNum in tokenIterator:
        if not startLine:
            #Note: The first token is the endline at the end of \begin{openScene}, so the environment starts on the same line as the first token in tokenIterator
            startLine = lineNum
        if parseTree.END_OPEN_SCENE == token:
            pythonCode = [line for line in pythonCode if line.strip()]
            #We use this to figure out what the top level indent is, and strip that away so that Python can parse the code properly.
            topLevelIndent = 1 if pythonCode[0][0] == '\t' else compute_indent(pythonCode[0])
            try:
                ast.parse(''.join(line[topLevelIndent:] for line in  pythonCode))
            except SyntaxError, e:
                raise transExceptions.TranslationError(' '.join([parseTree.color("Error:", parseTree.bcolors.RED), 'Error in Python code found in', parseTree.color('openScene',parseTree.bcolors.YELLOW),  
                    'environment. Environment start line:', parseTree.color(str(startLine), parseTree.bcolors.GREEN),  'Python error:\n\n', str(e)]))
            else:
                print(' '.join([parseTree.color("Success:", parseTree.bcolors.GREEN), "Parsed Python code in", parseTree.color("openScene", parseTree.bcolors.YELLOW), ":", color_line(startLine)]))
                #print(pythonCode)
                tree = parseTree.OpenScene(lineNum=startLine, parent=parent, data=pythonCode)
                #print(tree)
                return tree
        else:
            if token.strip(' \t') == '\n':
                pythonCode.append(pythonLine + token)
                pythonLine = ''
            else:
                pythonLine += token
    raise transExceptions.TranslationError(' '.join([error, color_line(startLine), ":", r"End of environment", parseTree.color("openScene", parseTree.bcolors.YELLOW), "not found."]))


def close_scene(tokenIterator, parent):
    data = []
    try:
        token, startLineNum = next(tokenIterator)
    except StopIteration:
        raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "End of close scene block not found."]))
    while token != parseTree.END_CLOSE_SCENE:
        try:
            token, startLine = next(tokenIterator)
        except StopIteration:
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "End of close scene block not found."]))
        else:
            if token != parseTree.END_CLOSE_SCENE:
                data.append(token)
    return parseTree.CloseScene(parent=parent, data=data)



def extract_args(tokenIterator, nodeType, numArgs):
    """
    Given an iterable of tokens, the type of the node, and the number of arguments, returns a pair:
    1. The line on which the arguments begin.
    2. A list of arguments.
    Note: This does not handle nested arguments.
    """
    args = [''] * numArgs
    startLine = 0
    numArgsProcessed = 0
    def translation_error_msg(startLine, numArgsProcessed):
        return ' '.join([error, color_line(startLine), "Argument", parseTree.color(str(numArgsProcessed + 1), parseTree.bcolors.BLUE), "of", parseTree.color(str(nodeType.__name__), parseTree.bcolors.GREEN), "missing", 
                        parseTree.color('}', parseTree.bcolors.YELLOW)])

    while numArgsProcessed < numArgs:
        try:
            token, lineNum = next(tokenIterator)
        except StopIteration:
                raise transExceptions.TranslationError(translation_error_msg(startLine, numArgsProcessed))
        else:
            if token == '{':
                while token != '}':
                    try:
                        token, lineNum = next(tokenIterator)
                    except StopIteration:
                        raise transExceptions.TranslationError(translation_error_msg(startLine, numArgsProcessed))
                    else:
                        if not startLine:
                            startLine = lineNum
                        if token != '}' and token.strip():
                            args[numArgsProcessed] = ' '.join([args[numArgsProcessed], token.strip()])
                numArgsProcessed += 1
    return (startLine, [arg.strip() for arg in args])

NUM_NODE_ARGS = 4
success = parseTree.color("Success:", parseTree.bcolors.GREEN)
def node(tokenIterator, parent):
    #The first sequence of tokens will be the arguments to node.
    startLine, args = extract_args(tokenIterator, parseTree.Node, NUM_NODE_ARGS)
    tree = parse_node(tokenIterator, parseTree.Node(parent=parent, data=args), startLine)      
    tree.data = args 
    print(' '.join([success, color_line(startLine), "Parsed node:", parseTree.color(args[0], parseTree.bcolors.BLUE)])) 
    return tree

def parse_node(tokenIterator, node, startLine):
    """
    Given a tokenIterator, a nodeType, and a line number at which the node begins, returns a parseTree for the node. This parseTree contains nothing as data, and has children that
    consist of paragraphs, and any code environments.
    """
    tree = node
    try:
        endToken = node.endToken
    except AttributeError:
        raise transExceptions.TranslationError(' '.join([error, "parse_node does not make any sense for the environment:", parseTree.color(tree.__class__.__name__, parseTree.bcolors.YELLOW), "Please inform Andrew Russell at sprpgs@gmail.com of",
            "this error. Please send him: this error message, and a copy of the tex that generated the error."]))
    paragraph = []
    startLine = 0
    previousLineNum = 0
    for token, lineNum in tokenIterator:
        if not startLine:
            startLine = lineNum
            tree.lineNum = startLine
        if token == parseTree.BEGIN_CODE:
            tree.children.append(code(tokenIterator, tree))
            continue
        elif token in parseTree.codeCommands:
            tree.children.append(code_command(token, tokenIterator, tree))
            continue
        #print((token, lineNum))
        if token.strip(' ') == '\n':
            #If the previous line number is strictly less than this one, then that means that the only token on this line is a new line, which means the line is blank, which means we're about to 
            #start a new paragraph. 
            if previousLineNum < lineNum:
                tree.children.append(parse_paragraph(((token, lineNum) for (token, lineNum) in paragraph if token.strip()), tree))
                paragraph = []
        elif token == endToken:
            return tree
        elif token == parseTree.BEGIN_OPEN_SCENE or token == parseTree.BEGIN_NODE or token == parseTree.BEGIN_CHILD_NODE:
            raise transExceptions.TranslationError(' '.join([error, color_line(startLine), "missing", parseTree.color(endToken, parseTree.bcolors.YELLOW), "for environment:", 
                parseTree.color(tree.__class__.__name__, parseTree.bcolors.BLUE)]))
        else:
            paragraph.append((token, lineNum))
        previousLineNum = lineNum
    else:
        raise transExceptions.TranslationError(' '.join([error, color_line(startLine), "missing", parseTree.color(endToken, parseTree.bcolors.YELLOW), "for environment:", 
            parseTree.color(tree.__class__.__name__, parseTree.bcolors.BLUE)]))

def parse_paragraph(tokenIterator, parent):
    """
    Given a tokenIterator iterating over a tokenized paragraph of text, and a ParseTree to serve as parent, returns a parseTree with the paragraph text parse, and the data element the name of the node in which
    the paragraph exists.
    """
    startLine = 0
    #DEBUG
    #tokenList = list(tokenIterator)
    #tokenIterator = iter(tokenList)
    tree = parseTree.Paragraph(parent=parent, data=parent.data, lineNum=parent.lineNum)
    #print("Start")
    #print(tokenList)
    #print("Done")
    for token, lineNum in tokenIterator:
        if not startLine:
            startLine = lineNum
            tree.lineNum = startLine
        if token in parseTree.inlineCommandsPlayer or token in parseTree.inlineCommands:
            tree.children.append(parse_command(token, lineNum, tokenIterator, tree))
        elif token in childrenCommands:
            return parse_children_command(token, lineNum, tokenIterator, parent)
        else:
            tree.children.append(parseTree.Text(lineNum, parent=tree, data=[token]))
    return tree
        

def parse_command(inlineCmd, startLineNum, tokenIterator, parent):
    """
    Given an inline tex command, the line number at which the command occurs, and an iterator through the tex file's list of tokens, returns a parse Tree whose data is the
    python code associated with the inline command, and whose children are the parsed arguments to the command.
    """
    #Only exists for debugging purposes. Delete for actually running this.
    #tokenList = list(tokenIterator)
    #Only exists for debugging purposes. Delete for actually running this.
    #tokenIterator = iter(tokenList)
    args = []
    data = [inlineCmd]
    numArgs = 0
    try:
        numArgs = parseTree.inlineCommands[inlineCmd][1]
    except KeyError:
        try:
            numArgs = parseTree.inlineCommandsPlayer[inlineCmd][1]
        except IndexError:
            r"""
            If we get an index error, then that means that the inlineCmd does not take any arguments, in which case, the commands are followed by empty curly brackets, i.e. \name{}. This gets tokenized into
            '\name', '{', '}' so we need to remove the curly brackets before moving on.
            """
            clearingBraces = 2
            while clearingBraces:
                try:
                    token, lineNum = next(tokenIterator)
                except StopIteration:
                    raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Missing", "brackets for", parseTree.color(inlineCmd, parseTree.bcolors.GREEN)]))
                if token == '{' or token == '}':
                    clearingBraces -= 1
                else:
                    raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Command", parseTree.color(inlineCmd, parseTree.bcolors.GREEN), "doesn't take any arguments."]))
    numOpenBraces = 0 
    argumentTokens = []
    tree = parseTree.InlineCommand(startLineNum, None, parent, data)
    while len(args) < numArgs:
        try:
            token, lineNum = next(tokenIterator)
        except StopIteration:
            #print(tokenList)
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Missing", parseTree.color(str(numArgs - len(args)), parseTree.bcolors.GREEN), "arguments for", 
                parseTree.color(inlineCmd, parseTree.bcolors.GREEN)]))
        if token == '{':
            numOpenBraces += 1
            #We don't want to include the outermost brace. Only braces that may show up inside the argument.
            if numOpenBraces == 1:
                token = ''
        elif token == '}':
            numOpenBraces -= 1
            if not numOpenBraces:
                #If we're looking at a cond, then the first command is supposed to code: Some sort of boolean expression, with the next two arguments text.
                if inlineCmd == r'\cond' and not args:
                    args.append(parseTree.Code(lineNum=lineNum, parent=tree, data=[' '.join(token for (token, lineNum) in argumentTokens)]))
                else:
                    args.append(parse_paragraph(iter(argumentTokens), tree))
                argumentTokens = []
        if numOpenBraces:
            argumentTokens.append((token, lineNum))
    tree.children = args
    return tree
           

def parse_children_command(cmd, startLineNum, tokenIterator, parent):
    """
    Given a command that affects node transitions (childif, childelif, child, or continue or continueNewPage) returns the ParseTree associated with this node.
    """
    try:
        numArgs = childrenCommands[cmd]
    except KeyError:
        raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), parseTree.color(cmd, parseTree.bcolors.GREEN), 'is not a valid node transition command.']))
    args = []
    argTokens = []
    tree = parseTree.Link(lineNum=startLineNum, parent=parent, data=parent.data + [cmd])
    if cmd == r'\childif' or cmd == r'\childelif':
       numOpenBraces = 0
       while len(args) < numArgs:
            try:
                token, lineNum = tokenIterator.next()
            except StopIteration:
                raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Command", parseTree.color(cmd, parseTree.bcolors.GREEN), "is missing", 
                    parseTree.color(str(numArgs - len(args)), parseTree.bcolors.GREEN), "arguments."]))
            if token == '{':
                if not numOpenBraces:
                    token = ''
                numOpenBraces += 1
            elif token == '}':
                numOpenBraces -= 1
                if numOpenBraces < 0:
                    raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(lineNum), "Too many", parseTree.color('}', parseTree.bcolors.GREEN)]))
                elif not numOpenBraces:
                    args.append(argTokens)
                    argTokens = []
            if numOpenBraces:
                argTokens.append(token)
       if numOpenBraces > 0:
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Too many", parseTree.color('{', parseTree.bcolors.GREEN)]))
       try:
           ast.parse(' '.join(args[0]).strip())
       except SyntaxError, e:
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error:", parseTree.bcolors.RED), 'Error in Python code found in', parseTree.color('childif',parseTree.bcolors.YELLOW),  'command on line:', 
                parseTree.color(str(lineNum), parseTree.bcolors.GREEN),  'Python error:\n\n', str(e)]))
       args = [parseTree.Code(lineNum=startLineNum, parent=tree, data=[' '.join(args[0])]), parseTree.Destination(lineNum=startLineNum, parent=tree, data=args[1])]
       """
       data = '\n'.join([''.join(['if ' if cmd == r'\childif' else 'elif', args[0], ':']),
                            'conversation.say_node(', args[1], ')',
                            parent.data, '.children = ', args[1], '.children',
                            parent.data, '.playerComments = ', args[1], '.playerComments'])
       """
    elif cmd == r'\child':
        numOpenBraces = 0 
        argTokens = []
        while len(args) < numArgs:
            try:
                token, lineNum = tokenIterator.next()
            except StopIteration:
                raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Command", parseTree.color(cmd, parseTree.bcolors.GREEN), "is missing", 
                    parseTree.color(str(numArgs - len(args)), parseTree.bcolors.GREEN), "arguments."]))
            if token == '{':
                if not numOpenBraces:
                    token = ''
                numOpenBraces += 1
            elif token == '}':
                numOpenBraces -= 1
                if numOpenBraces < 0:
                    raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(lineNum), "Too many", parseTree.color('}', parseTree.bcolors.GREEN)]))
            if numOpenBraces:
                argTokens.append((token, lineNum))
            else:
                #The first argument is parsed as a paragraph since it can have inline commands inside of it, but since the second is a static node name, the second is just treated as a Text node.
                if args:
                    args.append(parseTree.Destination(parent=tree, lineNum=lineNum, data=[token for (token, lineNum) in argTokens if token]))
                else:
                    args.append(parse_paragraph(iter(argTokens), tree))
                argTokens = []
        if numOpenBraces > 0:
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Too many", parseTree.color('{', parseTree.bcolors.GREEN)]))
    elif cmd == r'\continue' or cmd == r'\continueNewPage':
        numOpenBraces = 0
        argTokens = []
        while len(args) < numArgs:
            try:
                token, lineNum = tokenIterator.next()
            except StopIteration:
                raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Command", parseTree.color(cmd, parseTree.bcolors.GREEN), "is missing", 
                    parseTree.color(str(numArgs - len(args)), parseTree.bcolors.GREEN), "arguments."]))
            if token == '{':
                if not numOpenBraces:
                    token = ''
                numOpenBraces += 1
            elif token == '}':
                numOpenBraces -= 1
                if not numOpenBraces:
                    args.append(parseTree.Destination(lineNum, parent=tree, data=[token for (token, lineNum)in argTokens if token]))
                    argTokens = []
                elif numOpenBraces < 0:
                    raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(lineNum), "Too many", parseTree.color('}', parseTree.bcolors.GREEN)]))
            if numOpenBraces:
                argTokens.append((token, lineNum))
        if numOpenBraces > 0:
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "Too many", parseTree.color('{', parseTree.bcolors.GREEN)]))
    tree.children = args
    return tree
                             


NUM_CHILD_NODE_ARGS = 2
def child_node(tokenIterator, parent):
    startLine, args = extract_args(tokenIterator, parseTree.ChildNode, NUM_CHILD_NODE_ARGS)
    tree = parse_node(tokenIterator, parseTree.ChildNode(parent=parent, data=args), startLine)      
    tree.data = args
    print(' '.join([success, color_line(startLine), "Parsed node:", parseTree.color(args[0], parseTree.bcolors.BLUE)])) 
    return tree

class MadeUpException(Exception):
    pass


def code_command(command, tokenIterator, parent):
    tree = parseTree.CodeCommands(parent=parent)
    data = [command]
    try:
        #First token is {, which we don't want to include in our args.
        next(tokenIterator)
        token, lineNum = next(tokenIterator)
    except StopIteration:
        raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "LaTeX command:", command, "not terminated by a closing bracket '{'"])) 
    while token != '}':
        data.append(token)
        try:
            token, lineNum = next(tokenIterator)
        except StopIteration:
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(lineNum), "LaTeX command:", command, "not terminated by a closing bracket '{'"])) 
    tree.data = data
    return tree
    
    

def code(tokenIterator, parent):
    tree = parseTree.Code(parent=parent)
    data = []
    pythonLine = '' 
    try:
        token, startLineNum = next(tokenIterator)
    except StopIteration:
        raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "End of code block not found."]))
    while token != parseTree.END_CODE:
        try:
            token, lineNum = next(tokenIterator)
        except StopIteration:
            raise transExceptions.TranslationError(' '.join([parseTree.color("Error", parseTree.bcolors.RED), color_line(startLineNum), "End of code block not found."]))
        if token == parseTree.END_CODE:
            continue
        elif token == '\n':
            data.append(pythonLine)
            pythonLine = ''
        else:
            pythonLine += token
    tree.data = data
    tree.lineNum = startLineNum
    return tree


ENV_PROCESSORS = { 
'openScene': open_scene,
'closeScene': close_scene,
'node': node,
'childnode' : child_node,
'code' : code
}

#Used in errors. If we encounter an unrecognized token, we return a list of suggestions that are this similar.
MIN_STRING_DIFFERENCE = .7

def parse_environments(tokenIterator, root, startingNodeNum):
    """
    Given an iterable of (token, line number) pairs, generates the parse tree associated of the latex source.
    """
    #Group all error messages together, and print them together, so that the user can deal with them in batch, rather than one at a time.
    errorText = [] 
    currentScene = root
    parseTree.nodeNum = startingNodeNum
    for token, lineNum in tokenIterator:
        """
        This loop iterates through the tokens until it reaches an open environment. Then, it determines which environment is being opened, and passes control off to a function that processes that
        environment
        """
        if parseTree.BEGIN in token:
            try:
                env = token[token.index('{')+1:token.index('}')]
            except IndexError:
                try:
                    token.index('{')
                except IndexError:
                    raise transExceptions.TranslationError(' '.join([parseTree.color("Error Line:", parseTree.bcolors.RED), parseTree.color(str(lineNum), parseTree.bcolors.BLUE), "Missing", parseTree.color('{', parseTree.bcolors.YELLOW), "in token:", 
                        parseTree.color(token, parseTree.bcolors.YELLOW)]))
                else:
                    raise transExceptions.TranslationError(' '.join([parseTree.color("Error Line:", parseTree.bcolors.RED), parseTree.color(str(lineNum), parseTree.bcolors.BLUE), "Missing", parseTree.color('}', parseTree.bcolors.YELLOW), "in token:", 
                        parseTree.color(token, parseTree.bcolors.YELLOW)]))
            else:
                try:
                    newTree = ENV_PROCESSORS[env](tokenIterator, currentScene)
                except KeyError:
                    closeMatches = difflib.get_close_matches(env, ENV_PROCESSORS.keys(), 3, MIN_STRING_DIFFERENCE)
                    errorText.append(' '.join([parseTree.color("Error Line:", parseTree.bcolors.RED), parseTree.color(str(lineNum), parseTree.bcolors.BLUE), "Unrecognized environment:", parseTree.color(env, parseTree.bcolors.YELLOW), 
                        "\n Did you mean:\n" if closeMatches else "",
                        '\n'.join([parseTree.color(match, parseTree.bcolors.GREEN) for match in closeMatches])]))
                except transExceptions.TranslationError, e:
                    errorText.append(str(e))
                else:
                    #open and close scenes are treated as children to root, in order to ensure proper tabbing.
                    if env == 'closeScene' or env == 'openScene':
                        root.children.append(newTree)
                    else:
                        currentScene.children.append(newTree)
                    #This is ugly, and should probably be refactored into duck typing, but I'm too lazy to do that now. It's big enough refactoring node type into explicit subclasses (which I really should have done from the
                    #beginning).
                    if isinstance(newTree, parseTree.CloseScene):
                        currentScene = root
                    elif isinstance(newTree, parseTree.OpenScene) and currentScene == root:
                        currentScene = newTree
                    elif isinstance(newTree, parseTree.OpenScene):
                        errorText.append(' '.join([error, color_line(lineNum), "New scene started before previous scene ended. Please add a", parseTree.color("closeScene", parseTree.bcolors.YELLOW), 
                            "environment for previous scene."]))
        elif parseTree.END in token:
            errorText.append(' '.join([error, color_line(lineNum), "Environment end command:", parseTree.color(token, parseTree.bcolors.YELLOW), "seen without corresponding environment begin command."]))
    if errorText:
        raise transExceptions.TranslationError('\n'.join(errorText))
    return root

