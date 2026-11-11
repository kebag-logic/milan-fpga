#!/bin/bash
# check_ids.sh <clone> <rev>...: check-ID prefixes of tb/verilator/mbx/suite.hpp and suite_face.hpp per rev, and the shared ones.
set -u
c=$1; shift
for r in "$@"; do
  echo "== $r ($(git -C "$c" rev-parse "$r"))"
  for f in suite.hpp suite_face.hpp; do
    git -C "$c" show "$r:tb/verilator/mbx/$f" | grep -oE '"[A-Z][0-9]+ ' | tr -d '" ' | sort -u > "/tmp/ids.$$.$f"
    echo "$f: $(tr '\n' ' ' < /tmp/ids.$$.$f)"
  done
  echo "shared: $(comm -12 /tmp/ids.$$.suite.hpp /tmp/ids.$$.suite_face.hpp | tr '\n' ' ')"
  echo "U0 label lines: $(git -C "$c" show "$r:tb/verilator/mbx/suite.hpp" | grep -c '"U0 ')  H0 label lines: $(git -C "$c" show "$r:tb/verilator/mbx/suite.hpp" | grep '"H0 ' | sed 's/^ *//' | tr '\n' '|')"
  rm -f /tmp/ids.$$.*
done
echo "== PR lines touching an F or T label in either file, 1d6bf555..a69fc0f5:"
git -C "$c" diff 1d6bf555 a69fc0f5 -- tb/verilator/mbx/suite_face.hpp tb/verilator/mbx/suite.hpp | grep -cE '^[+-].*"(F|T)[0-9]+ '
