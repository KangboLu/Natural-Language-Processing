import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)   # dictionary for bigram
    self.previousCounts = collections.defaultdict(lambda: 0) # dictionary for unigram of current word
    self.zeroCount = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """
    # count bigram and previous word
    for sentence in corpus.corpus:
      for datumIndex in xrange(1, len(sentence.data)):
        bigram = sentence.data[datumIndex].word + sentence.data[datumIndex-1].word
        previousWord = sentence.data[datumIndex-1].word
        self.bigramCounts[bigram] += 1
        self.previousCounts[previousWord] += 1

  # P(current | previous) for bigram model
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # calculate not seen bigram for V from laplace smoothing
    for wordIndex in xrange(1, len(sentence)):
      if sentence[wordIndex] + sentence[wordIndex-1] not in self.bigramCounts:
        self.zeroCount += 1

    # apply laplace smoothing to the bigram model
    score = 0.0
    for wordIndex in xrange(1, len(sentence)):
      score += math.log(self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1]] + 1)
      score -= math.log(self.previousCounts[sentence[wordIndex-1]] + self.zeroCount)
    return score