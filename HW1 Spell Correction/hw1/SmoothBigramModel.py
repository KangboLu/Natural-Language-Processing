import math, collections

class SmoothBigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0) # dictionary for bigram
    self.previousCounts = collections.defaultdict(lambda: 0) # dictionary for unigram of current word
    self.zeroCount = 0
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
        self.bigramCounts[bigram] += 1 # count number of bigram
        self.previousCounts[previousWord] += 1 # count number of previous word

  # P(current | previous) for bigram model
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0 # initialize score

    # calculate not seen bigram for V for laplace smoothing
    for wordIndex in xrange(1, len(sentence)):
      bigram = sentence[wordIndex] + sentence[wordIndex-1]
      if bigram not in self.bigramCounts:
        self.zeroCount += 1

    # apply laplace smoothing to the bigram model
    for wordIndex in xrange(1, len(sentence)):
      bigramCount = self.bigramCounts[sentence[wordIndex] + sentence[wordIndex-1]] # count bigram
      previousCount = self.previousCounts[sentence[wordIndex-1]] # count previous word

      # calculate P(current | previous)
      score += math.log(bigramCount + 1)
      score -= math.log(previousCount + self.zeroCount)
    return score
