#!/bin/sh
perl cfggen.pl --text 10 grammar1 grammar1 lexicon > generate1n2.out
#python text_process.py generate1n2.out > generate1n2.sen
echo 'see generate1n2.out generation'

perl cfggen.pl --text 10 my_grammar my_lexicon > my_gen.out
#python text_process.py my_gen.out > my_gen.sen
echo 'see my_gen.out generation processing'
