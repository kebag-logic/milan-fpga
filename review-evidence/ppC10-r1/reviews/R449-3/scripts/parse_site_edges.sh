#!/usr/bin/env bash
# R449-3: edge cases for run.sh's parse_site(), extracted verbatim from the tree
# under review, over a synthetic all.v. Runs it under the default awk and, when
# available, under `gawk --posix` and busybox awk (stand-ins for a strict awk).
# usage: parse_site_edges.sh <tree>
set -uo pipefail
tree=$1; w=$(mktemp -d); trap 'rm -rf "$w"' EXIT; cd "$w"
sed -n '/^parse_site() {/,/^}/p' "$tree/syn/yosys/run.sh" > fn.sh
# shellcheck disable=SC1091
. ./fn.sh
cat > all.v <<'V'
module KL_a (a);
  input wire a;
endmodule
module automatic KL_b (a);
  input wire a;
endmodule
(* keep_hierarchy = "yes" *) (* x = 1 *) module KL_c (a);
  input wire a;
endmodule
  stray_token_between_modules ;
(* s = "a*b" *) module static KL_d #(parameter P = 1) (a);
  input wire a;
endmodule
module \KL$e (a);
  input wire a;
endmodule
macromodule KL_f(a);
endmodule
V
# line : expected name ('' = none)
cases='2:KL_a 4:KL_b 5:KL_b 7:KL_c 8:KL_c 10: 11:KL_d 12:KL_d 15:KL$e 17:KL_f 1:KL_a 3:KL_a'
mkdir -p shim
run_with() {
  local label=$1 fail=0 c n want got
  for c in $cases; do
    n=${c%%:*}; want=${c#*:}
    got="$(parse_site "all.v:$n: ERROR: syntax error")"
    if [ "$got" = "$want" ]; then r=ok; else r=MISMATCH; fail=1; fi
    printf '%-14s line %-3s want %-6s got %-6s %s\n' "$label" "$n" "'$want'" "'$got'" "$r"
  done
  return $fail
}
rc=0
run_with default-awk || rc=1
if command -v gawk >/dev/null; then
  printf '#!/bin/sh\nexec gawk --posix "$@"\n' > shim/awk; chmod +x shim/awk
  PATH="$PWD/shim:$PATH" run_with gawk-posix || rc=1
fi
if command -v busybox >/dev/null && busybox awk 'BEGIN{}' 2>/dev/null; then
  printf '#!/bin/sh\nexec busybox awk "$@"\n' > shim/awk; chmod +x shim/awk
  PATH="$PWD/shim:$PATH" run_with busybox-awk || rc=1
fi
echo "parse_site_edges rc=$rc"
exit $rc
