import re

class Datum:
    word = ''  # the correct word
    error = ''  # the error word (if any)

    def __init__(self):
        self.word = ''
        self.error = ''

    def __init__(self, word, error=''):
        self.word = word
        self.error = error

    def fixError(self):
        return Datum(self.word, '')

    def hasError(self):
        if self.error:
            return True
        else:
            return False

    def isValidTest(self):
        """Returns true if the error is within edit distance one and contains no numerics/punctuation."""
        if not self.hasError():
            return False
        distance = levenshtein(self.word, self.error)
        if (distance > 1):
            return False
        regex = '.*[^a-zA-Z].*'
        if re.match(regex, self.word) or re.match(regex, self.error):
            return False
        return True

    def __str__(self):
        """Format: word (error)?"""
        rep = self.word
        if self.hasError():
            rep = rep + " (" + self.error + ")"
        return rep


# Credit Michael Homer @ https://github.com/mwh
# MIT license.
def levenshtein(seq1, seq2):
    """Calculate the Damerau-Levenshtein distance between sequences.
    """
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        # Python lists wrap around for negative indices, so put the
        # leftmost column at the *end* of the list. This matches with
        # the zero-indexed strings and saves extra calculation.
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
            # This block deals with transpositions
            if (x > 0 and y > 0 and seq1[x] == seq2[y - 1]
                and seq1[x - 1] == seq2[y] and seq1[x] != seq2[y]):
                thisrow[y] = min(thisrow[y], twoago[y - 2] + 1)
    return thisrow[len(seq2) - 1]
