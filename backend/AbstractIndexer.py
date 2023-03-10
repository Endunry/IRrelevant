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
            ps.stem(tokens[i], 0, len(tokens[i]) - 1)
        # remove stop words
        tokens = [token for token in tokens if token not in stopWords]
        return tokens

class Tokenizer:
    
    @staticmethod 
    def readInFile(file_name):
        with open(file_name, 'r') as f:
            return Tokenizer.tokenize(f.read())
    
    @staticmethod
    def  tokenize(string:str, query:bool = False):
        string = Tokenizer.prepareString(string, query)
        return string.split()
    
    @staticmethod
    def prepareString(string:str, query:bool = False):
        # split up a concatenated word by - into two words
        string = re.sub(r'(\w+)-(\w+)', r'\1 \2', string)
        
        # handle split up words with a newline
        string = re.sub(r'(\w+)-\n(\w+)', r'\1\2', string)
        
        # remove punctuation but keep lines with the pattern .I 0-9
        string = re.sub(r'.W', '', string)
        string = re.sub(r'(.I)\s', '.I', string)
        string = re.sub(r'(\,|\.(?!I[0-9]+)|\?|\!|\:|\;|\'|\"|\\|\/|\+|\-|\(|\))|\%|\>|\<|\=', '', string)
        
        if not query:
            string = re.sub(r'\*', '', string) # dont remove * in queries
            
            
        # remove unnecessary whitespace
        string = re.sub(r'\s+', ' ', string)
        

        # normalize
        string = re.sub(r'\&', 'and', string)
        # all lowercase
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