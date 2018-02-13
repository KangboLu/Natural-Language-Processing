#!/usr/bin/perl

# Noah A. Smith
# 2/21/08
# Calculates and prints out error rate (word-level and sentence-level) 
# of a POS tagger.

# Usage:  tag_acc.pl gold-tags hypothesized-tags

# Tags should be separated by whitespace, no leading or trailing spaces, 
# one sentence per line.  There's no error handling if things don't line
# up!

use bytes;

$gold = shift;
$hypo = shift;

open(G, "<$gold") or die "can't open file $gold";
open(H, "<$hypo") or die "can't open file $hypo";

while($g = <G> and $h = <H>) {
    chomp($g);
    chomp($h);
    @G = split /\s+/, $g;
    @H = split /\s+/, $h;
    for($i = 0; $i < scalar(@G); ++$i) {
	++$tag_errors if($G[$i] ne $H[$i]);
	++$tag_tot;
	++$curr_tot if($G[$i] ne $H[$i]);
    }
    ++$sent_errors if($curr_tot > 0);
    ++$sent_tot;
    $curr_tot = 0;
}
print "error rate by word:      ", $tag_errors/$tag_tot, " ($tag_errors errors out of $tag_tot)\n";
print "error rate by sentence:  ", $sent_errors/$sent_tot, " ($sent_errors errors out of $sent_tot)\n";
