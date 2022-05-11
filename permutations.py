#! /user/env/python3
#make a quick iteration
import itertools

def read_word_list():
    #Read a list of words, one word per line of the file
    with open('sowpods.txt','r') as f:
        return f.read().split('\n')


out=list(itertools.permutations(["i","h","o","p","p"]))

perms=list()
words=list()

for i,item in enumerate(out):
    wordtry=""
    for j,letter in enumerate(item):
        wordtry=wordtry+letter

    perms.append(wordtry)

print(perms)
vocabulary = read_word_list()
for word in perms:
    if vocabulary.count(word)>0:
        words.append(word)

for word in words:
    print(word)
