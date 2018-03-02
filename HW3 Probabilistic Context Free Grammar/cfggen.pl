#!/usr/local/bin/perl

# Noah Smith
# 3/5/08

# usage:  cfggen.pl [options] N [grammar files] 

# This script samples from a probabilistic CFG.  It does the following:
#
# - loads a weighted CFG in a simple format X -> Y ... Z prob
#   (make sure the symbols do not include special character '_')
# - makes sure all rules are binary or unary, transforming as needed
# - renormalizes the probabilities so rules with the same left-hand 
#   nonterminal sum to one
# - samples N trees (N given on the command line) from the grammar
#   and outputs the trees (optionally in "pretty" format), or the strings

$ROOT_symbol = "ROOT";

$PRETTYPRINT = 0;
$TEXTONLY = 0;

while($ARGV[0] =~ m/\-\-/) {
    if($ARGV[0] eq "--pretty") { $PRETTYPRINT = 1; shift; }
    elsif($ARGV[0] eq "--text") { $TEXTONLY = 1; shift; }
    else { die "unknown option:  $ARGV[0]"; }
}
$N = shift;

while($grammar = shift) {
    open(G, "<$grammar");


    while(<G>) {
	s/\#.*//;
	if(($lhs, $rhs, $p) = (m/^\s*(\S+)\s*\-\>\s*(\S.*)\s+(\S+)\s*$/)) {
	    die "invalid probability $p on line $. (must be positive)" if($p <= 0.0);
	    die "invalid symbol ($lhs -> $rhs contains '_')" if($lhs =~ m/\_/ or $rhs =~ m/\_/);
	    
	    @r = split /\s+/, $rhs;
	    foreach $s (@r) { $Symbol{$s} = 1;}
	    $Symbol{$lhs} = 1;
	    if(scalar(@r) == 1) {
		$Unary{$lhs}{$r[0]} += $p;
		$Tot{$lhs} += $p;
	    }
	    elsif(scalar(@r) == 2) {
		$Binary{$lhs}{$r[0]}{$r[1]} += $p;
		$Tot{$lhs} += $p;
	    }
	    elsif(scalar(@r) > 2) {
		$x = $r[-2] . "_" . $r[-1];
		$y = $r[-2];
		$z = $r[-1];
		for($i = scalar(@r) - 3; $i >= 0; --$i) {
		    $Binary{$x}{$y}{$z} += 1.0;
		    $Tot{$x} += 1.0;
		    $z = $x;
		    $x = $r[$i] . "_" . $x;
		    $y = $r[$i];
		}
		$Binary{$lhs}{$y}{$z} += $p;
		$Tot{$lhs} += $p;
	    }
	    else {
		die "bad rule:  $_";
	    }
	}
    }
    close(G);
}

foreach $y (keys %Binary) {
    foreach $x (keys %{$Binary{$y}}) {
	foreach $z (keys %{$Binary{$y}{$x}}) {
	    $Binary{$y}{$x}{$z} = $Binary{$y}{$x}{$z} / $Tot{$y};
	}
    }
}
foreach $y (keys %Unary) {
    foreach $x (keys %{$Unary{$y}}) {
	$Unary{$y}{$x} = $Unary{$y}{$x} / $Tot{$y};
    }
}

for($i = 1; $i <= $N; ++$i) {
    print "$i:  ";
    sample_and_print($ROOT_symbol, 0);
    print "\n";
}


sub sample_and_print {
    my $sym = shift;
    my $indent = shift;
    my $r = rand;
    my $s = 0;
    if(defined $Binary{$sym}) {
	foreach $y (keys %{$Binary{$sym}}) {
	    foreach $z (keys %{$Binary{$sym}{$y}}) {
		$s += $Binary{$sym}{$y}{$z};
		if($s >= $r) {
		    unless($TEXTONLY) {
			my $pfx = ($PRETTYPRINT ? "\n" . (" " x $indent) : "");
			print $pfx, "($sym " unless($sym =~ m/\_/);
		    }
		    sample_and_print($y, $indent + 2);
		    print " ";
		    sample_and_print($z, $indent + 2);
		    unless($TEXTONLY) {
			print ")" unless($sym =~ m/\_/);
		    }
		    return;
		}
	    }
	}
    }
    if(defined $Unary{$sym}) {
	foreach $y (keys %{$Unary{$sym}}) {
	    $s += $Unary{$sym}{$y};
	    if($s >= $r) {
		unless($TEXTONLY) {
		    my $pfx = ($PRETTYPRINT ? "\n" . (" " x $indent) : "");
		    print $pfx, "($sym " unless($sym =~ m/\_/);
		}
		sample_and_print($y, $indent + 2);
		unless($TEXTONLY) {
		    print ")" unless($sym =~ m/\_/);
		}
		return;
	    }
	}
    }
    print "$sym";
}
	    
