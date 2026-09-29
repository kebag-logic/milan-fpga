#!/usr/bin/env bash
# Round-5 fault probes for census_sentence_r5.py, on scratch copies only.
# Usage: mutate_r5.sh <archived author dir> <pr-body.md> <scratch dir>
# Each mutant must make census_sentence_r5.py exit non-zero (KILLED);
# the unmodified control C0 must exit 0.
set -u
A=$1; B=$2; S=$3
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$S/mut"; mkdir -p "$S/mut"
run() { # name archive body expect(0|1)
  python3 -B "$here/census_sentence_r5.py" "$2" "$3" > "$S/mut/$1.out" 2>&1; rc=$?
  if [ "$4" = 0 ]; then v=$([ $rc = 0 ] && echo PASSED || echo UNEXPECTED-FAIL)
  else v=$([ $rc != 0 ] && echo KILLED || echo SURVIVED); fi
  echo "$1 rc=$rc $v :: $(grep -c '^FAIL' "$S/mut/$1.out") FAIL lines"; }
body() { # name sed-expr
  sed "$2" "$B" > "$S/mut/$1.md"
  if cmp -s "$B" "$S/mut/$1.md"; then echo "$1 NO-OP mutation (sed matched nothing)"; return 1; fi; }
run C0 "$A" "$B" 0
body B1 's/(105 `CONNECT_RX`, /(104 `CONNECT_RX`, /' && run B1 "$A" "$S/mut/B1.md" 1
body B2 's/210 state-changing ACMP commands/211 state-changing ACMP commands/' && run B2 "$A" "$S/mut/B2.md" 1
body B3 's/210 state-changing ACMP commands/210 ACMP commands/' && run B3 "$A" "$S/mut/B3.md" 1
body B4 "s/), all to the peer's input/), all to the DUT's input/" && run B4 "$A" "$S/mut/B4.md" 1
body B5 's/The 210 `CONNECT_RX` and `DISCONNECT_RX` went/The 200 `CONNECT_RX` and `DISCONNECT_RX` went/' && run B5 "$A" "$S/mut/B5.md" 1
body B6 's/ and no state-changing command addressed one\././' && run B6 "$A" "$S/mut/B6.md" 1
body B7 's/105 `DISCONNECT_RX`), all/105 `DISCONNECT_RX`), and 4 GET_TX_STATE; 214 ACMP commands all/' && run B7 "$A" "$S/mut/B7.md" 1
# archive mutants: copy, then change one transaction record
f=bind/unbind-4/unbind.jsonl
for m in A1 A2; do rm -rf "$S/mut/$m"; cp -r "$A" "$S/mut/$m"; done
python3 - "$S/mut/A1/$f" <<'EOF'
import sys; p=sys.argv[1]; t=open(p).read()
ls=t.splitlines(True); i=next(k for k,l in enumerate(ls) if '"kind":"transaction"' in l)
ls[i]=ls[i].replace('"listener_uid":8', '"listener_uid":1', 1); open(p,"w").write("".join(ls))
EOF
cmp -s "$A/$f" "$S/mut/A1/$f" && echo "A1 NO-OP" || run A1 "$S/mut/A1" "$B" 1
python3 - "$S/mut/A2/$f" <<'EOF'
import sys; p=sys.argv[1]; ls=open(p).read().splitlines(True)
tx=[l for l in ls if '"kind":"transaction"' in l and '"mt":8' in l][0]
open(p,"w").write("".join(ls)+tx.replace('"mt":8','"mt":6',1))
EOF
cmp -s "$A/$f" "$S/mut/A2/$f" && echo "A2 NO-OP" || run A2 "$S/mut/A2" "$B" 1
