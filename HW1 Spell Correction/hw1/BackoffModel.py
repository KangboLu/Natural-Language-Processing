import math, collections

class BackoffModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    # variables for bigram
    self.bigramCounts = collections.defaultdict(lambda: 0) # dictionary for bigram
    self.previousCounts = collections.defaultdict(lambda: 0) # dictionary for unigram of current word
    self.biZeroCount = 0

    # variables for unigram
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.totalCount = 0
    self.uniZeroCount = 0

    # train the backoff model
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    for sentence in corpus.corpus:
      for datumIndex in xrange(1, len(sentence.data)):
        datum = sentence.data
        bigram = datum[datumIndex].word + datum[datumIndex-1].word # get bigram string
        previousWord = datum[datumIndex-1].word # get previous word
        unigram = datum[datumIndex].word # get unigram string
        self.bigramCounts[bigram] += 1 # count number of bigram
        self.previousCounts[previousWord] += 1 # count number of previous word
        self.unigramCounts[unigram] +=1 # count number of unigram
        self.totalCount += 1 # total count for unigram model

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 # initialize score

    # calculate not seen unigram for laplace smoothing
    for word in sentence:
      if word not in self.unigramCounts:
        self.uniZeroCount += 1

    # calculating score with backoff model
    for wordIndex in xrange(1, len(sentence)):
      bigramCount = self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1]] # count of bigram
      previousCount = self.previousCounts[sentence[wordIndex-1]] # count of previous word
      unigramCount = self.unigramCounts[sentence[wordIndex]] # count of unigram

      # apply bigram model
      if bigramCount and previousCount > 0:
        score += math.log(bigramCount)
        score -= math.log(previousCount)
      else: # bigram not seen, apply unigram model
        score += math.log(unigramCount+1)
        score -= math.log(self.totalCount + self.uniZeroCount)
        score += math.log(0.7)
    return score