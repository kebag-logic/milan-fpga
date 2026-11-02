#!/usr/bin/env bash
# Disposable probes for review round R753-5 of PR #825 (#797).
# Usage: probe_r753_5.sh <clone-at-exact-head> <packet-dir> <verilator-bin-dir>
# Builds one extracted copy per probe under <packet>/scratch, applies one
# change, runs scripts/register_read_sweep.py and records its exit status.
set -u
SRC=$1; PKT=$2; VBIN=$3
export PATH="$VBIN:$PATH"
OLD='the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write'
NEW="the SRP table's latest answer to the window was a poll, after the last \`STRM_SEL\`/\`STRMW_CTRL\` write, with no other master using the table since"
RTL=hdl/common/csr/milan_csr.sv
mk() {  # mk <name>: extract the exact-head files the sweep reads
  local d=$PKT/scratch/$1; rm -rf "$d"; mkdir -p "$d"
  git -C "$SRC" archive HEAD hdl/common/csr configs/generated/endstation_ax7101_1x1_tdm8 \
    configs/generated/endstation_arty_4x4 docs/reference/REGISTER_MAP.md scripts/register_read_sweep.py | tar -x -C "$d"
  echo "$d"
}
run() {  # run <name>: sweep the copy, keep log and rc
  local d=$PKT/scratch/$1
  (cd "$d" && python3 -I scripts/register_read_sweep.py --work "$d/work" > "$PKT/receipts/$1.log" 2>&1; echo $? > "$PKT/receipts/$1.rc")
}
# P0 baseline: exact head unchanged
mk p0_head >/dev/null
# P1 the replaced wording planted back on the page (all four rows)
d=$(mk p1_oldwording); OLD="$OLD" NEW="$NEW" python3 -I -c '
import os,sys; p=sys.argv[1]; t=open(p).read(); n=t.count(os.environ["NEW"]); t=t.replace(os.environ["NEW"],os.environ["OLD"]); open(p,"w").write(t); print("P1 replaced",n)' "$d/docs/reference/REGISTER_MAP.md"
# RTL mutants, one clear case removed each
mut() {  # mut <name> <exact line text> <replacement>
  local d; d=$(mk "$1")
  python3 -I -c '
import sys; p,a,b=sys.argv[1:4]; t=open(p).read(); assert t.count(a)==1,(p,a,t.count(a)); open(p,"w").write(t.replace(a,b)); print(sys.argv[4],"mutated")' \
    "$d/$RTL" "$2" "$3" "$1"
}
mut p2_nosteal  'if (i_srp_ctx_stolen) srp_fresh_r <= 1'"'"'b0;' '/* mutant: stolen clear removed */'
mut p3_nowrans  'srp_fresh_r   <= 1'"'"'b0;          //! snapshot predates the write: re-poll' '/* mutant: write-answer clear removed */'
mut p4_noprov   'srp_fresh_r    <= 1'"'"'b0;
      end' '/* mutant: STRMW_CTRL clear removed */
      end'
mut p5_nosel    'if (sel_wr_w) srp_fresh_r <= 1'"'"'b0;' '/* mutant: STRM_SEL clear removed */'
for p in p0_head p1_oldwording p2_nosteal p3_nowrans p4_noprov p5_nosel; do run $p & done
wait
for p in p0_head p1_oldwording p2_nosteal p3_nowrans p4_noprov p5_nosel; do
  printf '%s rc=%s\n' "$p" "$(cat "$PKT/receipts/$p.rc")"
done
