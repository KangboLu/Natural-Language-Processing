import math, collections

class BackoffModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.previousCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.totalCount = 0
    self.uniZeroCount = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """
    for sentence in corpus.corpus:
      for datumIndex in xrange(0, len(sentence.data)):
        self.totalCount += 1
        self.unigramCounts[sentence.data[datumIndex].word] +=1
        self.previousCounts[sentence.data[datumIndex-1].word] += 1
        self.bigramCounts[sentence.data[datumIndex].word + sentence.data[datumIndex-1].word] += 1

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # calculate not seen unigram for laplace smoothing
    for word in sentence:
      if word not in self.unigramCounts:
        self.uniZeroCount += 1

    # calculating score with backoff model
    score = 0.0
    for wordIndex in xrange(1, len(sentence)):
      # apply unsmooth bigram model
      if self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1]] and self.previousCounts[sentence[wordIndex-1]]:
        score += math.log(self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1]])
        score -= math.log(self.previousCounts[sentence[wordIndex-1]])
      else: # bigram not seen, apply smooth unigram model
        score += math.log(self.unigramCounts[sentence[wordIndex]]+1)
        score -= math.log(self.totalCount + self.uniZeroCount)
        score += math.log(0.5)
    return score