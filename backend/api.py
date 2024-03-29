from AbstractIndexer import AbstractIndexer, Tokenizer, LinguisticModel
from invertedIndex import InvertedIndex
import sys
from flask import Flask, request, jsonify
from positionalIndex import PositionalIndex
import re
import json
import copy
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
    medcorpus = []
    with open('MED.ALL', 'r') as f:
        formattedString = Tokenizer.readableFormatter(f.read())
        corpusdoc = re.split(r'#\d+', formattedString)
        corpusdoc = corpusdoc[1:]
        element = {}
        for i in range(len(corpusdoc)):
            element['id'] = i+1
            element['text'] = corpusdoc[i].strip()
            medcorpus.append(element)
            element = {}

loadCorpusObject()
loadCorpusIndex()

def markPositions(text: str, positions: list[int]):
    # positions are word positions
    # 'non-esterified fatty acids in maternal and fetal plasma in intact, alloxan-diabetic and x-ray-irradiated rats . determinations of the non-esterified fatty acids in the plasma
    # go through all the letters one by one and count the words without punctuation
    # if the word count is in the positions list, mark it up
    text = text.strip()
    wordCount = -1
    markedUpText = ''
    currentlyMarking = False
    sow = True
    for i in range(len(text)):
        # if the character is a whitespace, increment the word count
        if sow:
            if text[i].isalpha() or text[i].isdigit():
                sow = False
                wordCount += 1
                if wordCount in positions:
                    markedUpText += '<span class="marked">'
                    currentlyMarking = True
                markedUpText += text[i]
            else:
                if not currentlyMarking:
                    markedUpText += text[i]
        else:
            if text[i] in [' ', '-', '.', ',', ';', ':', '!', '?', '\\']:
                if text[i] in ['.', ','] and i < len(text) - 1 and text[i+1].isdigit() and text[i-1].isdigit():
                    pass
                else:
                    sow = True
                if currentlyMarking:
                    markedUpText += '</span>'
                    currentlyMarking = False
                markedUpText += text[i]
            else:
                markedUpText += text[i]

    return markedUpText

# print(markPositions(' non-esterified fatty acids in maternal and fetal plasma in intact, alloxan-diabetic and x-ray-irradiated rats . determinations of the non-esterified fatty acids in the plasma.', [3,24]))

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
    (search_ids, positions) = medIndex.query(search_term)
    # filter the documents
    filtered_documents = [doc for doc in medcorpus if doc['id'] in search_ids]
    # get the paginated documents
    paginated_documents = copy.deepcopy(filtered_documents[start:end])
    # mark up the positions
    if search_term != '':
        for doc in paginated_documents:
            doc['text'] = markPositions(doc['text'], positions[doc['id']])
    # return the response
    return jsonify({"data": paginated_documents, "total": len(filtered_documents)})
        