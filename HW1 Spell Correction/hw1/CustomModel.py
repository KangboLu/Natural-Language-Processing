import math, collections
class CustomModel:

  def __init__(self, corpus):
    """Initial custom language model and structures needed by this mode"""
    self.totalCount = 0
    self.uniZeroCount = 0 # V
    self.unigramCounts = collections.defaultdict(lambda: 0) # dictionary for unigram
    self.bigramCounts = collections.defaultdict(lambda: 0) # dictionary for bigram
    self.previousCounts = collections.defaultdict(lambda: 0)
    self.trigramCounts = collections.defaultdict(lambda: 0) # dictionary for trigram
    self.triPreviousCounts = collections.defaultdict(lambda: 0)
    self.train(corpus) # train the model

  def train(self, corpus):
    """ Takes a corpus and trains backoff language model with trigram, bigram, unigram.
    """ 
    for sentence in corpus.corpus:
      for index in xrange(0, len(sentence.data)):
        # count unigram
        self.unigramCounts[sentence.data[index].word] += 1
        self.totalCount += 1
        # count bigram
        if index > 0:
          self.bigramCounts[sentence.data[index].word + sentence.data[index-1].word] += 1
          self.previousCounts[sentence.data[index-1].word] += 1
          # count trigram
          if index > 1:
            self.trigramCounts[sentence.data[index].word + sentence.data[index-1].word + sentence.data[index-2].word] += 1
            self.triPreviousCounts[sentence.data[index-2].word + sentence.data[index-1].word] += 1

  def score(self, sentence):
    """ With list of strings, return the log-probability of the sentence with language model. Use
        information generated from train.
    """
    # calculate not seen unigram for laplace smoothing
    for word in sentence:
      if word not in self.unigramCounts:
        self.uniZeroCount += 1

    # calculating score with backoff model
    score = 0.0
    for wordIndex in xrange(0, len(sentence)):
      unigramCount = self.unigramCounts[sentence[wordIndex]] # count of unigram

      # conditionaly get count for bigram and trigram
      bigramCount = 0
      trigramCount = 0
      if wordIndex > 0:
        bigramCount = self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1]] # count of bigram
        previousCount = self.previousCounts[sentence[wordIndex-1]] # count of previous word
      if wordIndex > 1: # count of trigram
        trigramCount = self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1] + sentence[wordIndex-2]]
        triPreviousCount = self.triPreviousCounts[sentence[wordIndex-2] + sentence[wordIndex-1]]

      if trigramCount and triPreviousCount: # apply trigram model
        score += math.log(trigramCount)
        score -= math.log(triPreviousCount)
      elif bigramCount and previousCount: # apply bigram model
        score += math.log(bigramCount)
        score -= math.log(previousCount)
      else: # apply unigram model
        score += math.log(unigramCount+1)
        score -= math.log(self.totalCount + self.uniZeroCount)
        score += math.log(0.8)
    return score