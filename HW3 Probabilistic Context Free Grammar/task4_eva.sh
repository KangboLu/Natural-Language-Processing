#!/bin/sh
# evaluate merged grammar1 and grammar2
perl cfgparse.pl grammar1 grammar2 lexicon < examples.sen > grammar1n2.score
echo "-merged grammar1n2 score-"
python score_process.py grammar1n2.score

# evaluate my_grammar
perl cfgparse.pl my_grammar my_lexicon < examples.sen > my_grammar.score
echo "-my grammar score-"
python score_process.py my_grammar.score