#!/bin/sh
echo 'Training trigram...'
python train_trigram_hmm.py btb.train.tgs btb.train.txt > btb.hmm # Train a bigram HMM tagger
echo 'Tagging data...'
python my_viterbi.py btb.hmm btb.test.txt > btb.out # Run the Viterbi algorithm to tag data:
echo 'Evalue score...'
./tag_acc.pl btb.test.tgs btb.out # Evaluate:
echo -ne '\007' # notification sound