import os
import string
import word_lists as wl

def isdigit(word):
    return word.isdigit()

def frequencies(fileName):
    #return a dictionary of word frequencies in the file
    dict={}
    with open(fileName,'r') as file:
        y=file.read()
        y=y.splitlines()
        for x in y:
            x=x.translate(None, string.punctuation)
            x=x.split(' ')
            for i in x:
                if i in dict:
                    dict[i]+=1
                else:
                    dict[i]=1
    return dict

def category(word):
    if word in wl.noun_list:
        return 'N'
    if word in wl.verb_list:
        return 'V'
    if word in wl.adverb_list:
        return 'AV'
    if word in wl.adjective_list:
        return 'AJ'
    return 'X'
    #category is retreived from the Hindi WordNet database (text file),return N for noun,
    #V for verb,AV for adverb and AJ for adjective. Return X if not found in the database
    
    pass