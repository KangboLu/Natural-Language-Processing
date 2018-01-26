import math, collections

class SmoothUnigramModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.totalCount = 0
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.zeroCount = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    for sentence in corpus.corpus:
      for datum in sentence.data:  
        self.unigramCounts[datum.word] += 1
        self.totalCount += 1
  # P(current) for unigram model
  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0

    # count each incremented word
    for word in sentence:
      if word not in self.unigramCounts:
        self.zeroCount += 1

    # apply laplace smoothing to unigram model
    for word in sentence:
      count = self.unigramCounts[word]
      score += math.log(count + 1)
      score -= math.log(self.totalCount + self.zeroCount)
    return score
