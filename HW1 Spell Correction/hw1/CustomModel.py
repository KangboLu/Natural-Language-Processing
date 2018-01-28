import math, collections
class CustomModel:

  def __init__(self, corpus):
    """Initial custom language model and structures needed by this mode"""
    # variables for trigram
    self.trigramCounts = collections.defaultdict(lambda: 0) # dictionary for trigram

    # variables for bigram
    self.bigramCounts = collections.defaultdict(lambda: 0) # dictionary for bigram
    self.previousCounts = collections.defaultdict(lambda: 0) # dictionary for unigram of current word

    # variables for unigram
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.totalCount = 0
    self.uniZeroCount = 0

    # train the backoff model
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
    """  
    # TODO your code here
    for sentence in corpus.corpus:
      for datumIndex in xrange(0, len(sentence.data)):
        datum = sentence.data

        # count unigram
        unigram = datum[datumIndex].word # get unigram string
        self.unigramCounts[unigram] +=1 # count number of unigram
        self.totalCount += 1 # total count for unigram model

        # count bigram
        if datumIndex > 0:
          bigram = datum[datumIndex].word + datum[datumIndex-1].word # get bigram string
          previousWord = datum[datumIndex-1].word # get previous word
          self.bigramCounts[bigram] += 1 # count number of bigram
          self.previousCounts[previousWord] += 1 # count number of previous word

        # count trigram
        if datumIndex > 1:
          trigram = datum[datumIndex].word + datum[datumIndex-1].word + datum[datumIndex-2].word

  def score(self, sentence):
    """ With list of strings, return the log-probability of the sentence with language model. Use
        information generated from train.
    """
    # TODO your code here
    score = 0.0 # initialize score

    # calculate not seen unigram for laplace smoothing
    for word in sentence:
      if word not in self.unigramCounts:
        self.uniZeroCount += 1

    # calculating score with backoff model
    for wordIndex in xrange(0, len(sentence)):
      bigramCount = 0
      trigramCount = 0
      unigramCount = self.unigramCounts[sentence[wordIndex]] # count of unigram
      if wordIndex > 0:
        bigramCount = self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1]] # count of bigram
        previousCount = self.previousCounts[sentence[wordIndex-1]] # count of previous word
        if wordIndex > 1: # count of trigram
          trigramCount = self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1] + sentence[wordIndex-2]]

      # apply trigram model
      if trigramCount and bigramCount > 0:
        score += math.log(trigramCount)
        score -= math.log(bigramCount)
      # apply bigram model
      elif bigramCount and previousCount > 0:
        score += math.log(bigramCount)
        score -= math.log(previousCount)
      else: # apply unigram model
        score += math.log(unigramCount+1)
        score -= math.log(self.totalCount + self.uniZeroCount)
        score += math.log(0.8)
    return score
