import re
import math
import matplotlib.pyplot as plt
from porterstemmer import PorterStemmer
gramMap = {}
gramCountmap = {}
currentDocId = 0
gramBuffer = []

ps = PorterStemmer()

def processLineNGramm(line, n=1):
    global gramMap
    global gramCountmap
    global currentDocId
    
    if '.W' in line:
        gramBuffer.clear()
        return
    
    if '.I' in line:
        currentDocId = int(line[3:])
        return
    
    # remove all commas and periods, colons, semicolons and slashes
    line = re.sub(r'[,\.:;/?!\n]', '', line)
    
    # split up a concatenated word by - into two words
    line = re.sub(r'(\w+)-(\w+)', r'\1 \2', line)

    # flatten the list
    words = line.split()
    for word in words:
        ps.stem(word, 0, len(word) - 1)
        gramBuffer.append(word)
        if len(gramBuffer) == n:
            word = ' '.join(gramBuffer)
            if word in gramMap:
                gramMap[word].add(currentDocId)
                gramCountmap[word] += 1
            else:
                gramMap[word] = set([currentDocId])
                gramCountmap[word] = 1
            gramBuffer.pop(0)

def main():
    global gramMap
    global gramCountmap
    global currentDocId
    
    with open('MED.ALL', 'r') as medall:
        # Read the file line by line
        with open('1.txt', 'w') as out:
            for line in medall:
                processLineNGramm(line);
            out.write(f'### Unigramm ###\n')
            out.write(f'Gesamtvokabular: {len(gramMap)}\n')
            out.write(f'Gesamtanzahl der Woerter: {sum(gramCountmap.values())}\n')
            out.write(f'Gesamttokens: {len(gramMap)}\n')
            twenthyMostFrequentWords = sorted(gramCountmap, key=gramCountmap.get, reverse=True)[:20]
            out.write(f'Die 20 häufigsten Woerter:\n')
            for word in twenthyMostFrequentWords:
                out.write(f'{word} ({gramCountmap[word]})\n')
                
    with open('MED.ALL', 'r') as medall:
        # Read the file line by line
        gramMap = {}
        gramCountmap = {}
        currentDocId = 0
        with open('2.txt', 'w') as out:
            for line in medall:
                processLineNGramm(line,2);
            out.write(f'### Bigramm ###\n')
            out.write(f'Gesamtvokabular: {len(gramMap)}\n')
            out.write(f'Gesamtanzahl der Woerter: {sum(gramCountmap.values())}\n')
            out.write(f'Gesamttokens: {len(gramMap)}\n')
            twenthyMostFrequentWords = sorted(gramCountmap, key=gramCountmap.get, reverse=True)[:20]
            out.write(f'Die 20 häufigsten Woerter:\n')
            for word in twenthyMostFrequentWords:
                out.write(f'{word} ({gramCountmap[word]})\n')
                
    with open('MED.ALL', 'r') as medall:
        # Read the file line by line
        gramMap = {}
        gramCountmap = {}
        currentDocId = 0
        with open('3.txt', 'w') as out:
            for line in medall:
                processLineNGramm(line,3);
            out.write(f'### Trigramm ###\n')
            out.write(f'Gesamtvokabular: {len(gramMap)}\n')
            out.write(f'Gesamtanzahl der Woerter: {sum(gramCountmap.values())}\n')
            out.write(f'Gesamttokens: {len(gramMap)}\n')
            twenthyMostFrequentWords = sorted(gramCountmap, key=gramCountmap.get, reverse=True)[:20]
            out.write(f'Die 20 häufigsten Woerter:\n')
            for word in twenthyMostFrequentWords:
                out.write(f'{word} ({gramCountmap[word]})\n')
                
        
    #calculate the relative frequency of the words
    
    # sort the wordmap by the count of the words
    sortedCountMap = sorted(gramCountmap, key=gramCountmap.get, reverse=True)
    relativeFrequency = []
    
    for wordCount in sortedCountMap:
        relativeFrequency.append(gramCountmap[wordCount] / len(gramMap))
    
    # plt.plot(range(1, len(sortedCountMap) + 1), relativeFrequency)
    
    zipf = [1 / (i + 1) for i in range(len(sortedCountMap))]
    
    # plt.plot(range(1, len(sortedCountMap) + 1), zipf)
    # plt.xlabel('Rang')
    # plt.axes().set_xscale('log', base=10)
    # plt.axes().set_yscale('log', base=10)
    # plt.yscale('log', base=10)
    # plt.xscale('log', base=10)
    # plt.ylabel('relative Häufigkeit')
    # plt.show()    


if __name__ == "__main__":
    main()