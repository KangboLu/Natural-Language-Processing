#!/usr/local/bin/perl

# Noah Smith
# 3/2/08

# usage:  cfgparse.pl [options] [grammar files] < [sentences]

# This script implements a probabilistic CKY parser.  It does the following:
#
# - loads a weighted CFG in a simple format X -> Y ... Z prob
#   (make sure the symbols do not include special character '_')
# - makes sure all rules are binary or unary, transforming as needed
# - renormalizes the probabilities so rules with the same left-hand 
#   nonterminal sum to one
# - runs the CKY algorithm on sentences read in to STDIN (one sentence
#   per line, with whitespace separating words); this CKY handles
#   unary rules, but will not pursue cycles; this CKY does not handle
#   epsilon rules (rules with empty right-hand sides)
# - the CKY inside algorithm is run alongside the "best tree" algorithm
# - for each sentence, writes out the probability of the best derivation,
#   the probability of the sentence, the probability of the best derivation
#   given the sentence, and the parse


$OOV_symbol = "OOV";
$ROOT_symbol = "ROOT";

$VERBOSE = 0;
$PRETTYPRINT = 0;

while($ARGV[0] =~ m/\-\-/) {
    if($ARGV[0] eq "--pretty") { $PRETTYPRINT = 1; shift; }
    else { die "unknown option:  $ARGV[0]"; }
}

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
		$Unary{$r[0]}{$lhs} += $p;
		$Tot{$lhs} += $p;
	    }
	    elsif(scalar(@r) == 2) {
		$Binary{$r[0]}{$r[1]}{$lhs} += $p;
		$Tot{$lhs} += $p;
	    }
	    elsif(scalar(@r) > 2) {
		$x = $r[-2] . "_" . $r[-1];
		$y = $r[-2];
		$z = $r[-1];
		for($i = scalar(@r) - 3; $i >= 0; --$i) {
		    $Binary{$y}{$z}{$x} += 1.0;
		    $Tot{$x} += 1.0;
		    $z = $x;
		    $x = $r[$i] . "_" . $x;
		    $y = $r[$i];
		}
		$Binary{$y}{$z}{$lhs} += $p;
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
	    $Binary{$y}{$x}{$z} = log($Binary{$y}{$x}{$z}) - log($Tot{$z});
#	    print "$z -> $y $x $Binary{$y}{$x}{$z}\n";
	}
    }
}
foreach $y (keys %Unary) {
    foreach $x (keys %{$Unary{$y}}) {
	$Unary{$y}{$x} = log($Unary{$y}{$x}) - log($Tot{$x});
#	print "$x -> $y $Unary{$y}{$x}\n";
    }
}

while(<>) {
    %C = ();
    %B = ();
    %I = ();
    s/^\s*//; s/\s*$//;
    @W = split /\s+/;
    $n = scalar(@W);
    for($i = 0; $i < $n; ++$i) {
	$w = $W[$i];
	$w = $OOV_symbol unless(defined $Symbol{$w});
	$C{$i}{$i + 1}{$w} = 0.0;
	$I{$i}{$i + 1}{$w} = 0.0;
    }
    for($l = 1; $l <= $n; ++$l) {

	for($i = 0; $i <= $n - $l; ++$i) {
	    $k = $i + $l;
	    for($j = $i + 1; $j < $k; ++$j) {
		foreach $Y (keys %{$C{$i}{$j}}) {
		    $q = $C{$i}{$j}{$Y};
		    $qI = $I{$i}{$j}{$Y};
		    foreach $Z (keys %{$C{$j}{$k}}) {
			$r = $C{$j}{$k}{$Z};
			$rI = $I{$j}{$k}{$Z};
			foreach $X (keys %{$Binary{$Y}{$Z}}) {
			    $p = $Binary{$Y}{$Z}{$X} + $q + $r;
			    $pI = $Binary{$Y}{Z}{$X} + $qI + $rI;
			    if(!(defined $C{$i}{$k}{$X}) or $p > $C{$i}{$k}{$X}) {
				$C{$i}{$k}{$X} = $p;
				$B{$i}{$k}{$X} = "$Y\t$Z\t$j";
				print "$i $k $X $p\n" if($VERBOSE);
			    }
			    if(defined $I{$i}{$k}{$X}) {
				$I{$i}{$k}{$X} = logadd($I{$i}{$k}{$X}, $p);
			    }
			    else {
				$I{$i}{$k}{$X} = $p;
			    }
			}
		    }
		}
	    }
	    do {
		$changes = 0;
		foreach $Y (keys %{$C{$i}{$k}}) {
		    $q = $C{$i}{$k}{$Y};
		    $qI = $I{$i}{$k}{$Y};
		    foreach $X (keys %{$Unary{$Y}}) {
			$p = $Unary{$Y}{$X} + $q;
			$pI = $Unary{$Y}{$X} + $qI;
			if(!(defined $C{$i}{$k}{$X}) or $p > $C{$i}{$k}{$X}) {
			    $C{$i}{$k}{$X} = $p;
			    $B{$i}{$k}{$X} = $Y;
			    ++$changes;
			    print "$i $k $X $p\n" if($VERBOSE);
			}
			if(defined $I{$i}{$k}{$X}) {
			    $t = $I{$i}{$k}{$X};
			    $I{$i}{$k}{$X} = logadd($I{$i}{$k}{$X}, $p);
			}
			else {
			    $I{$i}{$k}{$X} = $p;
			}
		    }
		}
	    } while($changes > 0);
	}
    }
    if(defined $C{0}{$n}{$ROOT_symbol}) {
	print sprintf("%3.3e %3.3e %3.3f", exp($C{0}{$n}{$ROOT_symbol}),
		      exp($I{0}{$n}{$ROOT_symbol}),
		      exp($C{0}{$n}{$ROOT_symbol} - $I{0}{$n}{$ROOT_symbol}));
	print backtrace(0, $n, $ROOT_symbol, 0);
	print "\n";
    }
    else {
	print "(failure)\n";
    }
}

sub backtrace {
    my $i = shift;
    my $k = shift;
    my $X = shift;
    my $indent = shift;
    my $ret = "";
#    print "bt($i, $k, $X)\n";
    my @l;
    my $pfx = ($PRETTYPRINT ? "\n" . (" " x $indent) : " ");
    $ret .= "$pfx($X" unless($X =~ m/\_/);
    if($X eq $W[$i] or $X eq $OOV_symbol) {
	return " " . $W[$i];
    }
    else {
	die "backtrace error ($i, $k, $X)" unless(defined $B{$i}{$k}{$X});
	@l = split /\t/, $B{$i}{$k}{$X};
	if(scalar(@l) == 1) {
	    $ret .= backtrace($i, $k, $l[0], $indent + 2);
	}
	else {
	    $ret .= backtrace($i, $l[2], $l[0], $indent + 2);
	    $ret .= backtrace($l[2], $k, $l[1], $indent + 2);
	}
    }
    $ret .= ")" unless($X =~ m/\_/);
#    print "returning $ret\n";
    return $ret;
}

sub logadd {
    my $lx = shift;
    my $ly = shift;
    if($lx eq '-inf') { return $ly; }
    if($ly eq '-inf') { return $lx; }
    my $d = $lx - $ly;
    if($d >= 0.0) {
	return $lx if($d > 745);
	return $lx + log(1.0 + exp(-$d));
    }
    else {
	return $ly if($d < -745);
	return $ly + log(1.0 + exp($d));
    }
}
