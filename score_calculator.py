import numpy as np
from stop_list import closed_class_stop_words
import copy
import math



raw_queries = []
raw_abstracts = []

with open('cran.qry','r') as fin:
    for line in fin:
       raw_queries.append(line.split())
fin.close()
    
with open('cran.all.1400','r') as fin:
    for line in fin:
       raw_abstracts.append(line.split())
fin.close()



queries = {}
queries_line = []
line_words = []
queries_word = []
for i,line in enumerate(raw_queries):
    if(line[0] != '.I' and line[0] != '.W' ):
        for word in line:
            if(word.isalnum() and not word.isdigit() and (word not in closed_class_stop_words)):
                line_words.append(word)
    if(line[0] == '.I'):
        if line_words != []:
            queries_line.append(line_words)
            queries_word.append(sorted(set(line_words),key=line_words.index))
            line_words = []
queries_line.append(line_words)
queries_word.append(sorted(set(line_words),key=line_words.index))

for line in queries_word:
    for word in line:
        if(word not in queries):
            queries[word] = 1
        elif(word in queries):
            queries[word] += 1

query_scores = []
scores = []
for i in range(225):
    scores = []
    for word in queries_word[i]:
        idf = math.log(225/queries[word])
        tf = queries_line[i].count(word)
        scores.append(tf*idf)
    query_scores.append(scores)

    
    
abstracts = {}
abstract_lines = []
line_words = []
abstract_words = []
for i,line in enumerate(raw_abstracts):
    if(line[0] != '.I' and line[0] != '.W' and line[0] != '.T' and line[0] != '.A' and line[0] != '.B'):
        for word in line:
            if(word.isalnum() and not word.isdigit() and (word not in closed_class_stop_words)):
                line_words.append(word)
    if(line[0] == '.I'):
        if line_words != []:
            abstract_lines.append(line_words)
            abstract_words.append(sorted(set(line_words),key=line_words.index))
            line_words = []
    if((i != len(raw_abstracts)) and raw_abstracts[i][0] == '.W' and raw_abstracts[i+1][0] == '.I'):
        abstract_lines.append([])
abstract_lines.append(line_words)
abstract_words.append(sorted(set(line_words),key=line_words.index))

for line in abstract_words:
    for word in line:
        if(word not in abstracts):
            abstracts[word] = 1
        elif(word in abstracts):
            abstracts[word] += 1

            
            
abstract_similarity = []
similarity = []
indexes =[]
for j in range(225):
    similarity = []
    for i in range(1400):
        abstract_scores = []
        for word in queries_word[j]:
            if word not in abstracts:
                idf = 0
                tf = 0
            else:
                idf = math.log(1400/abstracts[word])
                tf = abstract_lines[i].count(word)
            abstract_scores.append(tf*idf)
        if(np.dot(query_scores[j],abstract_scores) == 0):
           sim = 0
        else:
            sim = (np.dot(query_scores[j],abstract_scores)) / (math.sqrt((np.dot(query_scores[j], query_scores[j]))*(np.dot(abstract_scores, abstract_scores))))
        similarity.append(sim)
    index = sorted(range(len(similarity)), key=lambda k: similarity[k], reverse=True)
    similarity.sort(reverse=True)
    abstract_similarity.append(similarity)
    indexes.append(index)
    
with open('output.txt','w') as fout:
    for i in range(225):
        for j in range(1400):
            fout.write(str(i+1) + ' ' + str(indexes[i][j]+1) + ' ' + str(abstract_similarity[i][j]) + '\n')
fout.close()