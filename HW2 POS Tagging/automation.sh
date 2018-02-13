#!/bin/sh
echo 'trigram training...'
python train_trigram_hmm.py ptb.2-21.tgs ptb.2-21.txt > my.hmm # Train a bigram HMM tagger
echo 'viterbi tagging...'
python my_viterbi.py my.hmm ptb.22.txt > 22.out
echo 'evalue error rate...'
./tag_acc.pl ptb.22.tgs my.out # Evaluate:
echo -ne '\007' # notification sound