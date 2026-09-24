#!/usr/bin/env bash
# Re-run the source lane's gPTP pin asymmetry searches at the gitlink the
# composed candidate actually pins, and compare the two pins' text for the
# terms the #511 record's claims depend on.
#   pin_asymmetry_recheck.sh <repo>
set -u
repo=$1
cd "$repo" || exit 2
old=c1b617435824929a790739ea8585c3fe1a328cc0
new=$(git ls-tree HEAD gptp-processor | awk '{print $3}')
echo "# candidate HEAD $(git rev-parse HEAD) gitlink gptp-processor $new"
echo "# PR source 70f2c50d gitlink $(git ls-tree 70f2c50d45550f65c9d71ed0f5b0d70dc48acdb6 gptp-processor | awk '{print $3}')"
g() { git -C gptp-processor "$@"; }
printf '$ merge-base --is-ancestor %s %s; ' "$old" "$new"
g merge-base --is-ancestor "$old" "$new"; echo "exit=$?"
echo "\$ log --oneline $old..$new"; g log --oneline "$old..$new"
echo "\$ diff --stat $old $new"; g diff --stat "$old" "$new"
for rev in "$old" "$new"; do
  echo
  echo "## pin $rev"
  echo "\$ grep -I -i -w delayAsymmetry|delay_asymmetry|asymmetry|asym|cfg_asym|bench_uart_tune|uart_tune outside docs/history and svg"
  g grep -n -I -i -w -E "delayAsymmetry|delay_asymmetry|asymmetry|asym|cfg_asym|bench_uart_tune|uart_tune" "$rev" -- . ":!*.svg" ":!docs/history/**"; echo "exit=$?"
  echo "\$ grep -I -i asym substring outside docs/history and svg"
  g grep -n -I -i "asym" "$rev" -- . ":!*.svg" ":!docs/history/**"; echo "exit=$?"
  echo "\$ files naming asymmetr (all paths)"
  g grep -l -I -i "asymmetr" "$rev" -- . ":!*.svg" | sed "s/^$rev://"; echo "exit=$?"
done
echo
echo "## terms in the pin-bump diff itself"
for t in asym uart tune latch ingress egress; do
  n=$(g diff "$old" "$new" | grep -E '^[+-]' | grep -ci "$t")
  echo "changed lines naming '$t': $n"
done
echo "\$ diff --name-only $old $new -- hdl bench"; g diff --name-only "$old" "$new" -- hdl bench
