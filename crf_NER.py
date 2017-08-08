

from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite

import features #functions defining word features
import data_parser #function(s) to load train and test data from .txt files
import cPickle as pickle
#import pprint
from collections import Counter

freq={}
def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))

def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-6s %s" % (weight, label, attr)) 
class hindiNER(pycrfsuite.Tagger):
    @staticmethod
    def word2features(sent, i):
        word = sent[i][0]
        category = sent[i][1]
        if(word not in freq): freq[word]=0
        feat = {
            'bias':1,
            #'word=' + word,
            'word.isdigit':features.isdigit(word),
            'category':str(category),
            'freq':float(freq[word]),
            'BOS':'0',
            'EOS':'0',
        }
        if i > 0:
            word1 = sent[i-1][0]
            if(word1 not in freq): freq[word1]=0
            category1 = sent[i-1][1]
            feat.update({
                '-1:word':word1,
                '-1:word.isdigit':features.isdigit(word1),
                '-1:category':str(category1),
                '-1:freq':float(freq[word1]),
            })
        else:
            feat.update({'BOS':'1'})

        if i < len(sent)-1:
            word1 = sent[i+1][0]
            if(word1 not in freq): freq[word1]=0
            category1 = sent[i+1][1]
            feat.update({
                '+1:word':word1,
                '+1:word.isdigit':features.isdigit(word1),
                '+1:category':str(category1),
                '+1:freq':float(freq[word1]),
            })
        else:
            feat.update({'EOS':'1'})

        return feat

    @staticmethod
    def sent2features(sent):
        return [hindiNER.word2features(sent, i) for i in range(len(sent))]

    @staticmethod
    def sent2labels(sent):
        return [label for word, category, label in sent]

    @staticmethod
    def sent2tokens(sent):
        return [word for word,postag,label in sent]
    
    def predict_sent(self,sent):
        return self.tag(hindiNER.sent2features([(i,features.category(i)) for i in sent.split(' ')]))

def train(fileName,testFile=None,verbose=False):
    global freq
    freq=features.frequencies(fileName) #returns a dictionary of word frequencies in the file
    train_sents=data_parser.load(fileName)
    if(testFile is not None):
        test_sents=data_parser.load(testFile)
        X_test = [hindiNER.sent2features(s) for s in test_sents]
        y_test = [hindiNER.sent2labels(s) for s in test_sents]
    #sents is a list of lists, each list corresponding to a sentence in the 'train.txt'
    #The list has the format (word,category,label) for each word in sentence, each label corresponding to
    #the entity of the word. For current training datasets, these are-
    #(Date-Date, Num-Number of tickets, Dest-Destination, Src-Source Location)
    #category is retreived from the Hindi WordNet database,return N for noun,
    #V for verb,AV for adverb and AJ for adjective. Return X if not found in the database 


    #sent2features(train_sents[0])[0]


    X_train = [hindiNER.sent2features(s) for s in train_sents]
    y_train = [hindiNER.sent2labels(s) for s in train_sents]

    trainer = pycrfsuite.Trainer(verbose=False)

    for xseq, yseq in zip(X_train, y_train):
        trainer.append(xseq, yseq)


    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
        })

    trainer.train('hindiNER.crfsuite') #train and save model to file 'hindiNER.crfsuite'")


    #tagger = pycrfsuite.Tagger()
    tagger=hindiNER()
    tagger.open('hindiNER.crfsuite')
    
    if(testFile is not None): 
        for i in test_sents:
            example_sent = i#test_sents[0]
            print(' '.join(hindiNER.sent2tokens(example_sent)))
            print("Predicted:", ' '.join(tagger.tag(hindiNER.sent2features(example_sent))))
            print("Correct:  ", ' '.join(hindiNER.sent2labels(example_sent)))


    #y_pred = [tagger.tag(xseq) for xseq in X_test]

    #Evaluate model performance


    # Let us check what the classifier learnt
    info = tagger.info()

    if(verbose is True):
        print("Top likely transitions:")
        print_transitions(Counter(info.transitions).most_common(15))

        print("\nTop unlikely transitions:")
        print_transitions(Counter(info.transitions).most_common()[-15:])   

        print("Top positive:")
        print_state_features(Counter(info.state_features).most_common(20))

        print("\nTop negative:")
        print_state_features(Counter(info.state_features).most_common()[-20:])
    
    return tagger




