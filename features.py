import os
import string

#def isdigit(word):
 #   pass

def frequencies(fileName):
    #return a dictionary of word frequencies in the file
    dict={}
    with open(filename,'r') as file:
    #     while True:
        y=file.read()
        y=y.splitlines()
    #         x.rstrip()
        for x in y:
            x=x.translate(None, string.punctuation)
    #         x=x.split(' ')
    #         if x=='':
    #             break
            x=x.split(' ')
    #         print x
    #         y=[]
    #         for i in x:
    #           y.append(i.encode('utf-8'))
    #         print x[0]
            for i in x:
                if i in dict:
                    dict[i]+=1
                else:
                    dict[i]=1
    return dict

def category(word):
    if word in noun_list:
        return 'N'
    if word in verb_list:
        return 'V'
    if word in adverb_list:
        return 'AV'
    if word in adjective_list:
        return 'AJ'
    return 'X'
    #category is retreived from the Hindi WordNet database (text file),return N for noun,
    #V for verb,AV for adverb and AJ for adjective. Return X if not found in the database
    
    pass