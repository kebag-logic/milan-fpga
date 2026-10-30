#!/usr/bin/env bash
# Planted-drift probes for the inventory gate at an exact head.
# usage: plant.sh <source-repo> <work-dir> <head-sha>   (work-dir is disposable)
set -u
SRC=$1; W=$2; HEAD=$3
rm -rf "$W"; git clone -q --no-checkout "$SRC" "$W" && git -C "$W" checkout -q --detach "$HEAD" || exit 2
cd "$W" || exit 2
inv() { python3 scripts/check-doc-inventory.py 2>&1 | grep -E 'INVENTORY FAIL|inventory:' | head -4; return "${PIPESTATUS[0]}"; }
lnk() { python3 scripts/check-links.py 2>&1 | grep -viE '^ok|^links: ' | head -3; return "${PIPESTATUS[0]}"; }
py() { python3 -I -c "$@" || APPLY=bad; }
APPLY=ok
sub() { py "import sys;p='$1';t=open(p,encoding='utf-8').read();o=sys.argv[1];n=sys.argv[2];assert o in t,(p,o);open(p,'w',encoding='utf-8').write(t.replace(o,n,1))" "$2" "$3"; }
run() { # name expect(fail|pass) gate(inv|lnk|both) ; mutation already applied
  if [ "$APPLY" != ok ] || git diff --quiet && [ -z "$(git status --porcelain)" ] && [ "${1#C}" = "$1" ] && [ "${1#S}" = "$1" ]; then
    printf '%s\tAPPLY-FAILED\n' "$1"; APPLY=ok; git checkout -q -- . && git clean -qfd >/dev/null; return; fi
  local out rc; if [ "$3" = lnk ]; then out=$(lnk); rc=$?; else out=$(inv); rc=$?; fi
  if [ "$3" = both ]; then o2=$(lnk); r2=$?; out="$out | links: $o2"; [ $r2 -ne 0 ] && rc=1; fi
  local got=pass; [ $rc -ne 0 ] && got=fail
  printf '%s\texpect=%s\tgot=%s\trc=%s\t%s\n' "$1" "$2" "$got" "$rc" "$(echo "$out" | tr '\n' ' ' | cut -c1-400)"
  git checkout -q -- . && git clean -qfd >/dev/null
}
H6=docs/architecture/06_aecp_engine.md; CP=IEEE_1722_1_Hardware_Protocol_Processor.md; GL=docs/GLOSSARY.md
python3 scripts/check-doc-inventory.py --selftest >/tmp/st.$$ 2>&1; echo -e "S0 selftest\texpect=pass\tgot=$([ $? -eq 0 ] && echo pass || echo fail)\t$(tail -1 /tmp/st.$$)"; rm -f /tmp/st.$$
run C0-clean-inventory pass inv
run C1-clean-links pass lnk
py "
p='$H6';t=open(p,encoding='utf-8').read();i=t.index('**µISA (30 operations)**');j=t.index('\n|',t.index('|---',i));k=t.index('\`',j);open(p,'w',encoding='utf-8').write(t[:k]+'\`FAKE_OP\`, '+t[k:])"
run M1-fake-op-in-06-table fail inv
sub $H6 '**µISA (30 operations)**' '**µISA (29 operations)**'; run M2-wrong-heading-count fail inv
sub $H6 '**µISA (30 operations)** —' '**µISA (30 operations)** (a 30-operation ISA) —'; run M3-count-restated-on-heading-line fail inv
sub $CP 'a different ISA, the `ucpu_op_e` enum in' 'a different 29-operation ISA in'; run M4-banner-29-restored fail inv
sub $CP 'a different ISA, the `ucpu_op_e` enum in' 'a different 30-operation ISA, the `ucpu_op_e` enum in'; run M5-banner-true-30 fail inv
printf '\nThe µISA has 30 operations.\n' >> $GL; run M6-current-page-count fail inv
sub docs/10_RESOURCE_AND_EFFORT.md 'lists 29 operations' 'lists 31 operations'; run M7-control-retired-body pass inv
py "
p='hdl/aecp/ucpu_pkg.sv';t=open(p).read();import re;m=re.search(r'(OP_SHIFT_R\s*=\s*5.d29)',t);open(p,'w').write(t[:m.end()]+',\n    OP_FAKE = 5\'d30'+t[m.end():]) if 'OP_FAKE' not in t else None"; git diff --stat | tail -1 >&2; run M8-op-added-to-enum fail inv
sub docs/architecture/09_verification.md '| `inventory` |' '| `inventoryX` |'; run M9-09-target-row-dropped fail inv
rm hdl/aecp/ucpu_pkg.sv; run M10-defining-file-dropped fail both
rm tb/timer_map/shape_elab.sh; run M11-linked-target-file-dropped fail lnk
rm tb/srp_admission/Makefile; run M12-linked-makefile-dropped fail lnk
py "
import re;p='$H6';t=open(p,encoding='utf-8').read();m=re.search(r'^## 8\..*$',t,re.M);print(m.group(0),file=__import__('sys').stderr);open(p,'w',encoding='utf-8').write(t[:m.start()]+'## 8. Renamed section'+t[m.end():])"; run M13-banner-anchor-dropped fail lnk
sub tb/srp_top/README.md '## Timer-arm FIFOs at every store shape' '## Timer-arm FIFOs at each store shape'; run M14-srp_top-anchor-dropped fail lnk
# limits of the line-local matcher (expected to pass; recorded, not claimed as defects of the head)
printf '\nThe µCPU ISA has\n30 operations.\n' >> $GL; run G1-count-wrapped-to-next-line pass inv
printf '\nIt decodes 30 µISA operations.\n' >> $GL; run G2-count-before-uisa-word pass inv
printf '\nA thirty-operation ISA.\n' >> $GL; run G3-count-spelled pass inv
printf '\nThe ISA has 30 instructions.\n' >> $GL; run G4-instructions-word pass inv
# the round-2 gate on the round-2 banner text
git show 0ea635e:scripts/check-doc-inventory.py > scripts/check-doc-inventory.py; sub $CP 'a different ISA, the `ucpu_op_e` enum in' 'a different 29-operation ISA in'; run R2-old-gate-on-old-banner pass inv
