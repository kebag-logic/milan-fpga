#!/bin/sh
# List every $(shell ...) in a tracked make file (parent and checked-out
# submodules) that runs make, and flag any without --no-print-directory.
# Usage: scan_nested_make.sh <repo-root>
cd "$1" || exit 2
{ git ls-files; git submodule foreach -q 'git ls-files | sed "s|^|$sm_path/|"'; } |
  grep -E '(^|/)(GNUmakefile|[Mm]akefile)$|\.(mk|mak|make)$' | sort -u > /tmp/.scan_$$
echo "make files scanned: $(wc -l < /tmp/.scan_$$)"
xargs -d '\n' grep -nE '\$\(shell[^#]*(\$\(MAKE\)|\$\{MAKE\}|(^|[^a-z_-])make[[:space:]])' < /tmp/.scan_$$ |
  grep -vE "^[^:]+:[0-9]+:[[:space:]]*#" |
  while IFS= read -r l; do
    case $l in *--no-print-directory*) echo "ok      $l";; *) echo "MISSING $l";; esac
  done
rm -f /tmp/.scan_$$
# Wider net: any non-recipe, non-comment line that names make, so a $(shell
# split across a continuation line is still seen.
echo "--- non-recipe, non-comment lines naming make (review by eye):"
{ git ls-files; git submodule foreach -q 'git ls-files | sed "s|^|$sm_path/|"'; } |
  grep -E '(^|/)(GNUmakefile|[Mm]akefile)$|\.(mk|mak|make)$' | sort -u |
  xargs -d '\n' grep -nE '\$\(MAKE\)|\$\{MAKE\}|(^|[^a-zA-Z_./-])make[[:space:]]+-' |
  grep -vE '^[^:]+:[0-9]+:(	|[[:space:]]*#)'
