

import operator

from AbstractIndexer import AbstractIndexer, Tokenizer

class InvertedIndex(AbstractIndexer):
    
    invIndex: dict[str, list[int]] = {}
    def __init__(self, tokens):
        self.tokens = tokens
        self.index()
    
    def readInFile(self, file_name):
        self.invIndex = {}
        with open(file_name, 'r') as f:
            for line in f:
                # split the line into the word and the docIds
                line = line.split(':')
                # remove the curly braces
                line[1] = line[1][1:-2]
                # split the docIds into a list
                line[1] = line[1].split(',')
                # convert the docIds to integers
                if '' in line[1]:
                    print(line)
                line[1] = [int(docId) for docId in line[1]]
                # add the word and the docIds to the inverted index
                self.invIndex[line[0]] = line[1]
            
        print(f'Inverted index loaded from {file_name}: {len(self.invIndex)} terms')
                
    def index(self):
        self.markDocIds()
        
        # sort by terms and then docId
        self.tokens.sort(key = operator.itemgetter(1,0))
        
        for token in self.tokens:
            if '.' in token[1]:
                continue
            if token[1] in self.invIndex:
                self.invIndex[token[1]].add(token[0])
            else:
                self.invIndex[token[1]] = set([token[0]])
        
    def markDocIds(self):
        currentDocId = 0
        for index,token in enumerate(self.tokens):
            if '.' in token:
                currentDocId = int(token[2:])
                self.tokens[index] = (currentDocId, '.')
            else:
                self.tokens[index] = (currentDocId, token)
    
    def query(self, word):
        word = Tokenizer.prepareString(word)
        queryWords: list = word.split()
        returnValue = set()
        for word in queryWords:
            if word not in self.invIndex:
                return set()
            if len(returnValue) == 0:
                returnValue = set(self.invIndex[word])
            else:
                returnValue.intersection_update(set(self.invIndex[word]))
        
        return returnValue
    
    def save(self, file_name):
        with open(file_name, 'w') as f:
            for word in self.invIndex:
                f.write(f'{word}:{self.invIndex[word]}\n')