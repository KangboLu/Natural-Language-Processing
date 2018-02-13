#!/bin/sh
echo 'Training trigram...'
python train_trigram_hmm.py jv.train.tgs jv.train.txt > jv.hmm # Train a bigram HMM tagger
echo 'Tagging data...'
python my_viterbi.py jv.hmm jv.test.txt > jv.out # Run the Viterbi algorithm to tag data:
echo 'Evalue score...'
./tag_acc.pl jv.test.tgs jv.out # Evaluate:
echo -ne '\007' # notification sound