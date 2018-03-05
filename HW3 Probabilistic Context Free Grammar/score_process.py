import math
import sys

INPUT_FILE = sys.argv[1]
scores = list()

with open(INPUT_FILE) as inputfile:
  for line in inputfile.read().splitlines():
    # handle parse failure
    if line[0] == '(':
      scores.append(10000000000)
      continue

    start_index = 0
    end_index = 0
    for i in xrange(0, len(line)):
      if line[i] == ' ' and line[i+1] != ' ':
        start_index = i+1
        for j in xrange(start_index, len(line)):
          if line[j] == ' ':
            end_index = j-1
            break
        break
    score = -math.log(float(line[start_index:end_index+1]))
    scores.append(score)
score_sum = sum(scores)
print("Score is ", (score_sum/len(scores)))