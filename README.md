# HindiNER
Entity recognition in Hindi sentences

A tool to recognize pre-defined entities in hindi sentences. Uses a crf for this purpose, with a bunch of hand-crafted features. 

Instructions on how to use this module-
1. Clone the repo.
2. Install dependencies in requirements.txt ('pip install requirements.txt')
3. In your python app, import crf_NER
4. The syntax for training on your dataset is- train(<file location of train.txt>,<file location of test.txt>,verbose=True)
(test.txt and verbose arguments are optional)
  Example- trained_model=train('train.txt','test.txt',verbose=True)
5. The returned object can be used to make predictions on new sentences using object.predict_sent method.
  Example- trained_model.predict_sent('Hindi sentence here')
  This returns a string with sequence of entity labelings. '0' is default for None.

The format of 'train.txt' and 'test.txt' must be sentence followed by (in the next line) entity labelings.
For example, in the training data provided with this repo ('train.txt'), we have classified sentence words into entities source ('S'), destination ('D'), time ('T'), number of bookings ('N'). Hence the entities are specified as- D:<word>,N:<word>,T:<word>

Thanks to CFILT, IIT Bombay for the Hindi Wordnet database.
