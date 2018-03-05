#!/bin/sh
perl cfggen.pl --text 10 grammar1 lexicon > generate1.out
echo 'done grammar1 generation'
perl cfggen.pl --text 10 grammar2 lexicon > generate2.out
echo 'done grammar2 generation'
perl cfggen.pl --text 10 grammar1 grammar1 lexicon > generate1n2.out
echo 'done grammar1n2 generation'