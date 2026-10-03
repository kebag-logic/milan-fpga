#!/usr/bin/env bash
# Drive run.sh's parse_site() (extracted verbatim from the tree under review)
# over a synthetic all.v, as sv2v writes it, for three header layouts.
# usage: parse_site_unit.sh <tree>
set -uo pipefail
tree=$1; w=$(mktemp -d); trap 'rm -rf "$w"' EXIT; cd "$w"
sed -n '/^parse_site() {/,/^}/p' "$tree/syn/yosys/run.sh" > fn.sh
# shellcheck disable=SC1091
. ./fn.sh
printf '%s\n' 'module KL_first (a);' '  input wire a;' 'endmodule' \
  'module automatic KL_auto (a);' '  input wire a;' 'endmodule' \
  '(* keep_hierarchy = "yes" *) module KL_attr (a);' '  input wire a;' 'endmodule' > all.v
for n in 2 5 8; do
  echo "error at all.v:$n (inside $(sed -n "$((n-1))p" all.v | grep -oE 'KL_[A-Za-z_]+')) -> parse_site names: '$(parse_site "all.v:$n: ERROR: syntax error")'"
done
