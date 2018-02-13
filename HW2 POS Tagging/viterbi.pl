#!/usr/bin/perl

# Noah A. Smith
# 2/21/08
# Runs the Viterbi algorithm (no tricks other than logmath!), given an
# HMM, on sentences, and outputs the best state path.

# Usage:  viterbi.pl hmm-file < text > tags

# The hmm-file should include two kinds of lines.  One is a transition:
# trans Q R P
# where Q and R are whitespace-free state names ("from" and "to," 
# respectively) and P is a probability.  The other kind of line is an 
# emission:
# emit Q S P
# where Q is a whitespace-free state name, S is a whitespace-free
# emission symbol, and P is a probability.  It's up to you to make sure
# your HMM properly mentions the start state (named init by default),
# the final state (named final by default) and out-of-vocabulary
# symbols (named OOV by default).

# If the HMM fails to recognize a sequence, a blank line will be written.
# Change $verbose to 1 for more verbose output.

# special keywords:
#  $init_state   (an HMM state) is the single, silent start state
#  $final_state  (an HMM state) is the single, silent stop state
#  $OOV_symbol   (an HMM symbol) is the out-of-vocabulary word

use bytes;

$init_state = "init";
$final_state = "final";
$OOV_symbol = "OOV";

$verbose = 0;

# read in the HMM and store the probabilities as log probabilities

$hmmfile = shift;
open(HMM, "<$hmmfile") or die "could not open $hmmfile";
while(<HMM>) {
    if(($qq, $q, $p) = (m/trans\s+(\S+)\s+(\S+)\s+(\S+)/)) {
	$A{$qq}{$q} = log($p);
	$States{$qq} = 1;
	$States{$q} = 1;
    }
    elsif(($q, $w, $p) = (m/emit\s+(\S+)\s+(\S+)\s+(\S+)/)) {
	$B{$q}{$w} = log($p);
	$States{$q} = 1;
	$Voc{$w} = 1;
    }
}
close(HMM);

while(<>) { # read in one sentence at a time
    chomp;
    @w = split;
    $n = scalar(@w);
    unshift @w, "";
    %V = ();
    %Backtrace = ();
    $V{0}{$init_state} = 0.0;  # base case of the recurisve equations!
    for($i = 1; $i <= $n; ++$i) {     # work left to right ...
	# if a word isn't in the vocabulary, rename it with the OOV symbol
	unless(defined $Voc{$w[$i]}) {
	    print STDERR "OOV:  $w[$i]\n" if($verbose);
	    $w[$i] = $OOV_symbol;
	}
	foreach $q (keys %States) { # consider each possible current state
	    foreach $qq (keys %States) { # each possible previous state
		if(defined $A{$qq}{$q}  # only consider "non-zeros"
		   and defined $B{$q}{$w[$i]} 
		   and defined $V{$i - 1}{$qq}) 
		{
		    $v = $V{$i - 1}{$qq} + $A{$qq}{$q} + $B{$q}{$w[$i]};
		    if(!(defined $V{$i}{$q}) or $v > $V{$i}{$q}) {
			# if we found a better previous state, take note!
			$V{$i}{$q} = $v;  # Viterbi probability
			$Backtrace{$i}{$q} = $qq; # best previous state
		    }
		}
	    }
	    print STDERR "V[$i, $q] = $V{$i}{$q} ($B{$i}{$q})\n" if($verbose);
	}
    }
    # this handles the last of the Viterbi equations, the one that brings
    # in the final state.
    $foundgoal = 0;
    foreach $qq (keys %States) { # for each possible state for the last word
	if(defined $A{$qq}{$final_state} and defined $V{$n}{$qq}) {
	    $v = $V{$n}{$qq} + $A{$qq}{$final_state};
	    if(!$foundgoal or $v > $goal) {
		# we found a better path; remember it
		$goal = $v;
		$foundgoal = 1;
		$q = $qq;
	    }
	}
    }
    
    # this is the backtracking step.
    if($foundgoal) {
	@t = ();
	for($i = $n; $i > 0; --$i) {
	    unshift @t, $q;
	    $q = $Backtrace{$i}{$q};
	}
    }
    print STDERR exp($goal), "\n" if($verbose);
    if($foundgoal) { print join " ", @t; }
    print "\n";
}
