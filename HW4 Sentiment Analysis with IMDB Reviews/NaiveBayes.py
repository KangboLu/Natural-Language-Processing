import collections
import getopt
import math
import operator
import os
import sys

class NaiveBayes:
    class TrainSplit:
        """
        Set of training and testing data
        """
        def __init__(self):
            self.train = []
            self.test = []

    class Document:
        """
        This class represents a document with a label. classifier is 'pos' or 'neg' while words is a list of strings.
        """
        def __init__(self):
            self.classifier = ''
            self.words = []

    def __init__(self):
        """
        Initialization of naive bayes
        """
        self.stopList = set(self.readFile('data/english.stop'))
        self.bestModel = False
        self.stopWordsFilter = False
        self.naiveBayesBool = False
        self.numFolds = 10

        # TODO
        # Implement a multinomial naive bayes classifier and a naive bayes classifier with boolean features. The flag
        # naiveBayesBool is used to signal to your methods that boolean naive bayes should be used instead of the usual
        # algorithm that is driven on feature counts. Remember the boolean naive bayes relies on the presence and
        # absence of features instead of feature counts.

        # When the best model flag is true, use your new features and or heuristics that are best performing on the
        # training and test set.

        # If any one of the flags filter stop words, boolean naive bayes and best model flags are high, the other two
        # should be off. If you want to include stop word removal or binarization in your best performing model, you
        # will need to write the code accordingly.
        self.posDocumentCount = 0 # positive document count
        self.negDocumentCount = 0 # negative document count
        self.totalDocumentCount = 0 # total document count
        self.posWordCount = 0   # positive word count
        self.negWordCount = 0   # negative word count
        self.wordPosCount = collections.defaultdict(lambda: 0) # dictionary for word, classifer pair
        self.wordNegCount = collections.defaultdict(lambda: 0) # dictionary for word, classifer pair

        self.V = 0
        self.posWordDocCount = 0   # positive word count
        self.negWordDocCount = 0   # negative word count
        self.wordPosDocCount = collections.defaultdict(lambda: 0) # dictionary for word, classifer pair in document
        self.wordNegDocCount = collections.defaultdict(lambda: 0) # dictionary for word, classifer pair in document

    def classify(self, words):
        """
        Classify a list of words and return a positive or negative sentiment
        """
        # calculate probability for classifer
        Ppos = float(self.posDocumentCount) / (self.totalDocumentCount)
        Pneg = float(self.negDocumentCount) / (self.totalDocumentCount)
        Cpos = math.log(Ppos)
        Cneg = math.log(Pneg)

        # task 1, 2
        if self.stopWordsFilter:
            # find the value in the dictionary and computer Cj
            words = self.filterStopWords(words)
            for word in words:
                # update Cj value
                if self.wordPosCount[word] >= 0:
                    Cpos += math.log(float(self.wordPosCount[word]+1) / (self.posWordCount + 1 * self.V))
                if self.wordNegCount[word] >= 0:
                    Cneg += math.log(float(self.wordNegCount[word]+1) / (self.negWordCount + 1 * self.V))

        # task 3
        if self.naiveBayesBool == True:
            # find the value in the dictionary and computer Cj
            words = set(words)
            for word in words:      
                # update Cj value
                a = 4
                if self.wordPosDocCount[word] >= 0:
                    Cpos += math.log(float(self.wordPosDocCount[word] + a) / (self.posWordDocCount + a*self.V))
                if self.wordNegDocCount[word] >= 0:
                    Cneg += math.log(float(self.wordNegDocCount[word] + a) / (self.negWordDocCount + a*self.V))

        # task 4
        if self.bestModel == True:
            # find the value in the dictionary and computer Cj
            words = set(words)
            for word in words:      
                # update Cj value
                a = 6.8
                if self.wordPosDocCount[word] >= 0:
                    Cpos += math.log(float(self.wordPosDocCount[word] + a) / (self.posWordDocCount + a*self.V))
                if self.wordNegDocCount[word] >= 0:
                    Cneg += math.log(float(self.wordNegDocCount[word] + a) / (self.negWordDocCount + a*self.V))

        # return value
        if Cpos > Cneg: 
            return 'pos'
        return 'neg'

    def addDocument(self, classifier, words):
        """
        Train your model on a document with label classifier (pos or neg) and words (list of strings). You should
        store any structures for your classifier in the naive bayes class. This function will return nothing
        """
        # counting positive and negative document number
        if classifier == 'pos': 
            self.posDocumentCount += 1
        elif classifier == 'neg': 
            self.negDocumentCount += 1
        self.totalDocumentCount += 1

        # task 1, 2 with add one smoothing 
        if self.stopWordsFilter:
            # loop through words in reviews to count positive and negative words
            words = self.filterStopWords(words)
            for word in words:
                if word not in self.wordPosCount and word not in self.wordNegCount:
                    self.V += 1
                if classifier == 'pos': 
                    self.posWordCount += 1
                    self.wordPosCount[word] += 1
                if classifier == 'neg': 
                    self.negWordCount += 1
                    self.wordNegCount[word] += 1

        # task 3 binarized naive bayes
        if self.naiveBayesBool or self.bestModel:
            words = set(words)
            for word in words:
                if word not in self.wordPosDocCount and word not in self.wordNegDocCount:
                    self.V += 1
                if classifier == 'pos':
                    self.posWordDocCount += 1 # increment n
                    self.wordPosDocCount[word] += 1 # increment nk
                if classifier == 'neg':
                    self.negWordDocCount += 1 # increment n
                    self.wordNegDocCount[word] += 1 # increment nk

    def readFile(self, fileName):
        """
        Reads a file and segments.
        """
        contents = []
        f = open(fileName)
        for line in f:
            contents.append(line)
        f.close()
        str = '\n'.join(contents)
        result = str.split()
        return result

    def trainSplit(self, trainDir):
        """Takes in a trainDir, returns one TrainSplit with train set."""
        split = self.TrainSplit()
        posDocTrain = os.listdir('%s/pos/' % trainDir)
        negDocTrain = os.listdir('%s/neg/' % trainDir)
        for fileName in posDocTrain:
            doc = self.Document()
            doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
            doc.classifier = 'pos'
            split.train.append(doc)
        for fileName in negDocTrain:
            doc = self.Document()
            doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
            doc.classifier = 'neg'
            split.train.append(doc)
        return split

    def train(self, split):
        for doc in split.train:
            words = doc.words
            if self.stopWordsFilter:
                words = self.filterStopWords(words)
            self.addDocument(doc.classifier, words)

    def crossValidationSplits(self, trainDir):
        """Returns a lsit of TrainSplits corresponding to the cross validation splits."""
        splits = []
        posDocTrain = os.listdir('%s/pos/' % trainDir)
        negDocTrain = os.listdir('%s/neg/' % trainDir)
        # for fileName in trainFileNames:
        for fold in range(0, self.numFolds):
            split = self.TrainSplit()
            for fileName in posDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                doc.classifier = 'pos'
                if fileName[2] == str(fold):
                    split.test.append(doc)
                else:
                    split.train.append(doc)
            for fileName in negDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                doc.classifier = 'neg'
                if fileName[2] == str(fold):
                    split.test.append(doc)
                else:
                    split.train.append(doc)
            yield split

    def test(self, split):
        """Returns a list of labels for split.test."""
        labels = []
        for doc in split.test:
            words = doc.words
            if self.stopWordsFilter:
                words = self.filterStopWords(words)
            guess = self.classify(words)
            labels.append(guess)
        return labels

    def buildSplits(self, args):
        """
        Construct the training/test split
        """
        splits = []
        trainDir = args[0]
        if len(args) == 1:
            print '[INFO]\tOn %d-fold of CV with \t%s' % (self.numFolds, trainDir)

            posDocTrain = os.listdir('%s/pos/' % trainDir)
            negDocTrain = os.listdir('%s/neg/' % trainDir)
            for fold in range(0, self.numFolds):
                split = self.TrainSplit()
                for fileName in posDocTrain:
                    doc = self.Document()
                    doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                    doc.classifier = 'pos'
                    if fileName[2] == str(fold):
                        split.test.append(doc)
                    else:
                        split.train.append(doc)
                for fileName in negDocTrain:
                    doc = self.Document()
                    doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                    doc.classifier = 'neg'
                    if fileName[2] == str(fold):
                        split.test.append(doc)
                    else:
                        split.train.append(doc)
                splits.append(split)
        elif len(args) == 2:
            split = self.TrainSplit()
            testDir = args[1]
            print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
            posDocTrain = os.listdir('%s/pos/' % trainDir)
            negDocTrain = os.listdir('%s/neg/' % trainDir)
            for fileName in posDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (trainDir, fileName))
                doc.classifier = 'pos'
                split.train.append(doc)
            for fileName in negDocTrain:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (trainDir, fileName))
                doc.classifier = 'neg'
                split.train.append(doc)

            posDocTest = os.listdir('%s/pos/' % testDir)
            negDocTest = os.listdir('%s/neg/' % testDir)
            for fileName in posDocTest:
                doc = self.Document()
                doc.words = self.readFile('%s/pos/%s' % (testDir, fileName))
                doc.classifier = 'pos'
                split.test.append(doc)
            for fileName in negDocTest:
                doc = self.Document()
                doc.words = self.readFile('%s/neg/%s' % (testDir, fileName))
                doc.classifier = 'neg'
                split.test.append(doc)
            splits.append(split)
        return splits

    def filterStopWords(self, words):
        """
        Stop word filter
        """
        removed = []
        for word in words:
            if not word in self.stopList and word.strip() != '':
                removed.append(word)
        return removed


def test10Fold(args, stopWordsFilter, naiveBayesBool, bestModel):
    """
        Test when 1 command argv is given
    """
    nb = NaiveBayes()
    splits = nb.buildSplits(args)
    avgAccuracy = 0.0
    fold = 0
    for split in splits:
        classifier = NaiveBayes()
        classifier.stopWordsFilter = stopWordsFilter
        classifier.naiveBayesBool = naiveBayesBool
        classifier.bestModel = bestModel
        accuracy = 0.0
        for doc in split.train:
            words = doc.words
            classifier.addDocument(doc.classifier, words)

        for doc in split.test:
            words = doc.words
            guess = classifier.classify(words)
            if doc.classifier == guess:
                accuracy += 1.0

        accuracy = accuracy / len(split.test)
        avgAccuracy += accuracy
        print '[INFO]\tFold %d Accuracy: %f' % (fold, accuracy)
        fold += 1
    avgAccuracy = avgAccuracy / fold
    print '[INFO]\tAccuracy: %f' % avgAccuracy


def classifyFile(stopWordsFilter, naiveBayesBool, bestModel, trainDir, testFilePath):
    """
        Classify file with given parameters
    """
    classifier = NaiveBayes()
    classifier.stopWordsFilter = stopWordsFilter
    classifier.naiveBayesBool = naiveBayesBool
    classifier.bestModel = bestModel
    trainSplit = classifier.trainSplit(trainDir)
    classifier.train(trainSplit)
    testFile = classifier.readFile(testFilePath)
    print classifier.classify(testFile)


def main():
    stopWordsFilter = False
    naiveBayesBool = False
    bestModel = False

    # using command line option to modify naiver bayers behavior
    (options, args) = getopt.getopt(sys.argv[1:], 'fbm')
    if ('-f', '') in options:
        stopWordsFilter = True
    elif ('-b', '') in options:
        naiveBayesBool = True
    elif ('-m', '') in options:
        bestModel = True

    # using argv length to specify which function to call
    if len(args) == 2 and os.path.isfile(args[1]):
        classifyFile(stopWordsFilter, naiveBayesBool, bestModel, args[0], args[1])
    else:
        test10Fold(args, stopWordsFilter, naiveBayesBool, bestModel)

if __name__ == "__main__":
    main()
