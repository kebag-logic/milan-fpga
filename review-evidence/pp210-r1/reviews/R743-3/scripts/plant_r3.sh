#!/usr/bin/env bash
# Plant one drift at a time in a disposable clone of the exact head, run the
# inventory gate (self-test, then main) and the link gate, record rc and the
# findings, and restore the clone to the head after each plant.
# usage: plant_r3.sh <head-clone> <out-file>
set -u
c=$1; out=$2; cd "$c" || exit 2
head=$(git rev-parse HEAD)
: >"$out"; echo "clone head $head" >>"$out"
run() {  # name, then a shell snippet that plants the drift
  local name=$1 snip=$2
  bash -c "$snip"
  python3 scripts/check-doc-inventory.py --selftest >/tmp/st.$$ 2>&1; local st=$?
  python3 scripts/check-doc-inventory.py >/tmp/inv.$$ 2>&1; local inv=$?
  python3 scripts/check-links.py >/tmp/lk.$$ 2>&1; local lk=$?
  {
    echo "=== $name"
    echo "plant: $snip"
    echo "diffstat: $(git status --porcelain | tr '\n' ' ')"
    echo "selftest rc=$st ($(tail -1 /tmp/st.$$))"
    echo "inventory rc=$inv"; grep -E 'INVENTORY FAIL|^inventory:' /tmp/inv.$$ | cut -c1-240
    echo "links rc=$lk"; grep -viE '^(ok|links?:? .*ok)' /tmp/lk.$$ | tail -4 | cut -c1-240
  } >>"$out"
  git checkout -q -- . && git clean -qfd && git reset -q --hard "$head"
  [ -z "$(git status --porcelain)" ] || { echo "RESTORE FAILED" >>"$out"; exit 3; }
}
S06=docs/architecture/06_aecp_engine.md; PKG=hdl/aecp/ucpu_pkg.sv; CON=IEEE_1722_1_Hardware_Protocol_Processor.md
run "C0 control, unmodified" "true"
run "T1 fake op added to the 06 table" "sed -i '/^| Data |/s/\`SHIFT_R\`/\`SHIFT_R\`, \`FAKE_OP\`/' $S06"
run "T2 fake op added to the enum" "sed -i 's/^\(\s*\)OP_SHIFT_R\(\s*\)= 5.d29/\1OP_FAKE_OP   = 5'\"'\"'d30,\n\1OP_SHIFT_R\2= 5'\"'\"'d29/' $PKG"
run "H1 heading count made 29" "sed -i 's/^\*\*µISA (30 operations)\*\*/**µISA (29 operations)**/' $S06"
run "H2 wrong count restated on the heading line" "sed -i 's/^\(\*\*µISA (30 operations)\*\*\) —/\1 (an ISA of 29 ops) —/' $S06"
run "H3 true count restated on the heading line, other form" "sed -i 's/^\(\*\*µISA (30 operations)\*\*\) —/\1, a 30-operation ISA, —/' $S06"
run "H4 count restated on 06's next line" "sed -i '1428s/^/The ISA has 30 operations. /' $S06"
run "B1 concept banner back to 29-operation" "sed -i 's/a different ISA, the/a different 29-operation ISA, the/' $CON"
run "B2 concept banner given the true count" "sed -i 's/a different ISA, the/a different 30-operation ISA, the/' $CON"
run "B3 retired body count changed (control, history)" "sed -i '1098s/~20–30 instructions/29 operations, the ISA/' $CON"
run "R1 current page restates, one line" "sed -i '5s/µISA before/µISA (30 operations) before/' tb/ucpu/README.md"
run "R2 current page heading-form restatement" "printf '\n**µISA (30 operations)**\n' >> docs/guides/hdl-engineer.md"
run "L1 06 §8 heading renamed (concept banner and inventory link target)" "sed -i 's/^## 8\. µcode architecture/## 8. µcode machine/' $S06"
run "L2 srp_top heading renamed (its own link target)" "sed -i 's/^## Timer-arm FIFOs at every store shape (issue #230)/## Timer-arm FIFOs per store shape (issue #230)/' tb/srp_top/README.md"
run "L3 timer_map shape_elab.sh removed" "git rm -q tb/timer_map/shape_elab.sh"
run "L4 nvm_port measure_figures.py removed" "git rm -q tb/nvm_port/measure_figures.py"
run "L5 acmp_nvm Makefile removed" "git rm -q tb/acmp_nvm/Makefile"
run "L6 inventory dropped from the check rule" "sed -i 's/^\(check:.*\) inventory /\1 /' Makefile"
run "L7 defining file ucpu_pkg.sv removed" "git rm -q $PKG"
run "G1 limit: restatement wrapped across two lines" "sed -i '5s/µISA before/µISA, all 30\noperations of it, before/' tb/ucpu/README.md"
run "G2 limit: count spelled out" "sed -i '5s/µISA before/µISA (thirty operations) before/' tb/ucpu/README.md"
run "G3 limit: 30-op ISA" "sed -i '5s/µISA before/µISA, a 30-op ISA, before/' tb/ucpu/README.md"
run "G4 limit: 30 opcodes" "sed -i '5s/µISA before/µISA and its 30 opcodes before/' tb/ucpu/README.md"
run "G5 limit: micro-ISA count without the word ISA (µcode, 30 operations)" "sed -i '5s/µISA before/µcode set of 30 operations before/' tb/ucpu/README.md"
echo "final head $(git rev-parse HEAD) status [$(git status --porcelain)]" >>"$out"
