import re
from porterstemmer import PorterStemmer
from abc import ABC, abstractmethod

class LinguisticModel:
    @staticmethod
    def modify_tokens(tokens:list[str], stopWords:list[str] = []):        
        # stem
        ps = PorterStemmer()
        for i in range(len(tokens)):
            if '.' in tokens[i]: # dont manipulate the doc id markers
                continue
            else:
                ps.stem(tokens[i], 0, len(tokens[i]) - 1)
        # remove stop words
        tokens = [token for token in tokens if token not in stopWords]
        return tokens

class Tokenizer:
    
    @staticmethod 
    def readInFile(file_name):
        with open(file_name, 'r') as f:
            return Tokenizer.tokenize(f.read())
    
    # used to get the later position in text to mark it up
    @staticmethod
    def readableFormatter(string:str):
        # mark the ids
        string = re.sub(r'(\.I\s)(\d+)', r'#\2', string)
        
        # delete .W
        string = re.sub(r'\.W\n', '', string)
        
        # delete every non word, but keep the id markers and punctuation
        
        string = re.sub(r'(\s+)', ' ', string)
        
        string = re.sub(r'(\w)- ', r'\1', string)
        return string
    
    @staticmethod
    def  tokenize(string:str, query:bool = False):
        string = Tokenizer.prepareString(string, query)
        return string.split()
    
    @staticmethod
    def prepareString(string:str, query:bool = False):
        
        string = Tokenizer.readableFormatter(string)
        string = re.sub(r'(\w+)-(\w+)', r'\1 \2', string)
    
        # remove punctuation
        string = re.sub(r'[^\w\s#&%]', '', string)
        
        
        
        if not query:
            string = re.sub(r'\*', '', string) # dont remove * in queries

        # "normalize"
        string = re.sub(r'\&', ' and ', string)
        string = re.sub(r'\%', ' percent ', string)
        string = re.sub(r'\s+', ' ', string)
        string = string.lower()
        return string
    
class AbstractIndexer(ABC):
    
    @abstractmethod
    def __init__(self, tokens):
        pass
    
    @abstractmethod
    def index(self):
        pass

    @abstractmethod 
    def query(self, _query:str):
        pass

    @abstractmethod
    def readInFile(self, file_name):
        pass
    
    @abstractmethod
    def save(self, file_name):
        pass