#!/bin/sh
# Compare two directories of C sources token by token: comments removed by the
# compiler's own preprocessor (-fpreprocessed, directives kept), whitespace collapsed.
# Usage: token_identity.sh DIR_A DIR_B FILE...
set -eu
a=$1; b=$2; shift 2
rc=0
norm() { gcc -x c -fpreprocessed -dD -E -P "$1" 2>/dev/null | tr -s ' \t\n' '\n' | grep -v '^$'; }
for f in "$@"; do
    ha=$(norm "$a/$f" | sha256sum | cut -c1-16)
    hb=$(norm "$b/$f" | sha256sum | cut -c1-16)
    if [ "$ha" = "$hb" ]; then echo "SAME   $f tokens=$ha"; else echo "DIFFER $f $ha $hb"; rc=1; fi
done
exit $rc
