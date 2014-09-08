import os.path
import sets

def gen_keywords(episodeFile):
    keywords = sets.Set()
    with open(episodeFile, 'r') as episode:
        for line in episode.readlines():
            if 'add_keyword(' in line:
                keyStart = line.find('add_keyword(') + len('add_keyword(') 
                keyEnd = line[keyStart:].find(')') + keyStart
                keywords.add(line[keyStart:keyEnd])
    keywordFileName = os.path.basename(episodeFile).split('.')[0]
    keywordFileName += '_keywords.txt'
    with open(keywordFileName, 'w') as keyFile:
        keyFile.write('\n'.join(keywords))

if __name__ == '__main__':
    gen_keywords('episode1.py')

