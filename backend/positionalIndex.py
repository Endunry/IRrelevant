import operator
from AbstractIndexer import AbstractIndexer, Tokenizer
from invertedIndex import InvertedIndex

class PositionalIndexItem:
    docPositions = {}
    def __init__(self, term, docId = None, position = None):
        self.term = term
        self.docPositions = {}
        if docId is not None and position is not None:
            self.addDoc(docId, position)
        
    def addDoc(self, docId, position):
        if docId not in self.docPositions:
            self.docPositions[docId] = []
        self.docPositions[docId].append(position)
        
    def getDocPositions(self, docId):
        if docId in self.docPositions:
            return self.docPositions[docId]
        return []
    
    def __str__(self):
        return f'<{self.term}, {len(self.docPositions)}: {self.docPositions}>'
        
        
class PositionalIndex(AbstractIndexer):
    def __init__(self, tokens):
        self.tokens = tokens
        self.positionalIndex = {}
        self.docCount = 0
        self.index()
    
    def index(self):
        self.markDocIds()
        
        # sort by terms and then docId
        self.tokens.sort(key = operator.itemgetter(0))
        
        documentPosition = 0
        self.docCount = 0
        for token in self.tokens:
            if '#' in token[1]:
                documentPosition = 0
                self.docCount += 1
                continue
            if token[1] in self.positionalIndex:
                self.positionalIndex[token[1]].addDoc(token[0], documentPosition)
            else:   
                item = PositionalIndexItem(token[1], token[0], documentPosition)
                self.positionalIndex[token[1]] = item
            documentPosition += 1
    
    def markDocIds(self):
        currentDocId = 0
        for index,token in enumerate(self.tokens):
            if '#' in token:
                currentDocId = int(token[1:])
                self.tokens[index] = (currentDocId, '#')
            else:
                self.tokens[index] = (currentDocId, token)
                
    def query(self, _query):
        if _query == '':
            return (list(range(1, self.docCount + 1)),{})
        finalResult = []
        positions = {}
        for orQuery in _query.split('|'):
            # merge the results of the queries
            tokens = Tokenizer.tokenize(orQuery, True)
            try:   
                (orResult, orPositions) = self.phraseQuery(tokens)
            except KeyError:
                orResult = []
                orPositions = {}
            finalResult = list(set(finalResult + orResult))
            for newDocs in orPositions:
                if newDocs not in positions:
                    positions[newDocs] = orPositions[newDocs]
                else:
                    positions[newDocs].extend(orPositions[newDocs])
                    # remove duplicates
                    positions[newDocs] = list(set(positions[newDocs]))
        return (finalResult, positions)
    
    def phraseQuery(self, tokens):
        importantDocIds = None
        positions = {}
        if len(tokens) == 0:
            return (list(range(1, self.docCount + 1)), {})
        elif tokens[0] == '*':
            return (self.phraseQuery(tokens[1:]),{})
        else:
            importantDocIds = self.positionalIndex[tokens[0]].docPositions.keys()
        result = []
        for docId in importantDocIds:
            for firstPosition in self.positionalIndex[tokens[0]].getDocPositions(docId):
                tempPositions = [firstPosition]
                for token in tokens[1:]:
                    if token != '*':
                        if firstPosition + 1 not in self.positionalIndex[token].getDocPositions(docId):
                            break
                    tempPositions.append(firstPosition + 1)
                    firstPosition += 1
                else:
                    result.append(docId)
                    positions[docId] = tempPositions
                    break
        return (result, positions)

    def save(self, file_name):
        with open(file_name, 'w') as f:
            for term in self.positionalIndex:
                f.write(f'{self.positionalIndex[term]}\n')
    
    def readInFile(self, file_name):
        pass