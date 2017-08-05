import os
import features
import string


def load(fileName):
    #Return a list of lists, each list corresponding to a sentence in the fileName
    #The list has the format (word,category,label) for each word in sentence, each label corresponding to
    #the entity of the word. For current training datasets, these are-
    #(Date-Date, Num-Number of tickets, Dest-Destination, Src-Source Location)
    #category is obtained from features.category() function
    list=[]
    
    ##### change this code so that pickle file is loaded minimum number of times
    pickle_file = 'list_of_words.pickle'
    with open(pickle_file, 'rb') as f:
      save = pickle.load(f)
      noun_list=save['noun']
      adverb_list=save['adverb']
      verb_list=save['verb']
      adjective_list=save['adjective']
      del save  # hint to help gc free up memory
    with open(fileName,'r') as file:
        x=file.read()
        x=x.splitlines()
        for line in x:
            line_list=[]
            line=line.translate(None, string.punctuation)
            words=x.split(' ')
            for word in words:
                cat=category(word)
                
                line_list.append([word,cat,label])
            list.append(line_list)
    return line_list

