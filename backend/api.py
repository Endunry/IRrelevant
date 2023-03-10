from AbstractIndexer import AbstractIndexer, Tokenizer, LinguisticModel
from invertedIndex import InvertedIndex
import sys
from flask import Flask, request, jsonify
from positionalIndex import PositionalIndex
import re
import json
import time
from flask_cors import CORS, cross_origin
medcorpus = []
medIndex = None

def loadCorpusIndex():
    global medIndex
    tokens = Tokenizer.readInFile('MED.ALL')
    modified_tokens = LinguisticModel.modify_tokens(tokens)
    medIndex = PositionalIndex(modified_tokens)
    # medIndex.save('MED.POSITIONALINDEX');

def main_cli():
    # get the start arguments
    if len(sys.argv) != 2:
        print('Usage: python api.py <x.ALL | x.INVERTEDINDEX>')
        return
    indexer : AbstractIndexer = None

    if '.ALL' in sys.argv[1]:
        tokens = Tokenizer.readInFile(sys.argv[1])
        modified_tokens = LinguisticModel.modify_tokens(tokens)
        indexer = PositionalIndex(modified_tokens)
        indexer.save('MED.POSITIONALINDEX');
        
    while True:
        query = input('Query: ')
        if query == 'exit':
            break
        print(indexer.query(query))
def loadCorpusObject():
    global medcorpus
    with open('MED.ALL', 'r') as f:
        document = None
        for line in f:
            if '.I' in line:
                if document:
                    medcorpus.append(document)
                document = {}
                document['id'] = int(line[3:].strip())
            elif '.W' in line:
                continue
            else:
                if 'text' not in document:
                    document['text'] = ''
                document['text'] += re.sub(r'\s+', ' ', line.strip())

loadCorpusObject()
loadCorpusIndex()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@app.route('/load/med', methods=['GET'])
@cross_origin()
def load_med():
    # wait 4 seconds
    global medcorpus, medIndex
    # get pagination parameters
    first = request.args.get('first', 0, type=int)
    rows = request.args.get('rows', 10, type=int)
    # get the start and end index
    start = first
    end = first + rows
    
    # get the search term
    search_term = request.args.get('phrase', '')
    search_ids = medIndex.query(search_term)
    # filter the documents
    filtered_documents = [doc for doc in medcorpus if doc['id'] in search_ids]
    # get the paginated documents
    paginated_documents = filtered_documents[start:end]
    # return the response
    return jsonify({"data": paginated_documents, "total": len(filtered_documents)})
        