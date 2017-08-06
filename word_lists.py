import os
import cPickle as pickle

    ##### change this code so that pickle file is loaded minimum number of times
pickle_file = 'list_of_words.pickle'
with open(pickle_file, 'rb') as f:
  save = pickle.load(f)
  noun_list=save['noun']
  adverb_list=save['adverb']
  verb_list=save['verb']
  adjective_list=save['adjective']
  del save  # hint to help gc free up memory