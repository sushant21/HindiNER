import os
import features
import string
import cPickle as pickle


def load(fileName):
    #Return a list of lists, each list corresponding to a sentence in the fileName
    #The list has the format (word,category,label) for each word in sentence, each label corresponding to
    #the entity of the word. For current training datasets, these are-
    #(Date-Date, Num-Number of tickets, Dest-Destination, Src-Source Location)
    #category is obtained from features.category() function
    listt=[]
    
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
        for i in range(0,len(x),2):
            line=x[i]
            label_line=x[i+1]
            label_dict={}
            labels=label_line.split(',')
            for label in labels:
                pos=label.find(':')
                label_dict[label[pos+1:]]=label[:label.find(':')]
            line_list=[]
            line=line.translate(None, string.punctuation)
            words=line.split(' ')
            for word in words:
                cat=features.category(word)
                if word in label_dict:
                    line_list.append([word,cat,label_dict[word]])
                else:
                    line_list.append([word,cat,'0'])
            listt.append(line_list)
    return listt

