#!/usr/bin/env bash
# Plant drifts against the inventory gate's derived checks (06 §8 µISA from
# ucpu_pkg.sv, 09 §7 target table from the Makefile's check rule) in a
# disposable clone of the head, run the gate, and restore the clone each time.
# usage: plant_derived.sh <head-clone> <out-file> <old-rev-for-06>
set -u
c=$1; out=$2; old=$3; cd "$c" || exit 2
: >"$out"
pkg=hdl/aecp/ucpu_pkg.sv; p06=docs/architecture/06_aecp_engine.md
p09=docs/architecture/09_verification.md
restore() { git checkout -q -- . ; git clean -qfd -e .venv-wavedrom; }
gate() { python3 -I scripts/check-doc-inventory.py >"$out.tmp" 2>&1; local rc=$?
         { echo "rc=$rc"; sed 's/^/    /' "$out.tmp"; } >>"$out"; rm -f "$out.tmp"; }
plant() { echo "== $1" >>"$out"; }

plant "D0 control: unmodified head"; gate; restore

plant "D1 fake operation OP_FAKE = 5'd30 appended to the enum"
python3 -I - "$pkg" <<'EOF'
import sys,re;p=sys.argv[1];s=open(p).read()
s=re.sub(r"(OP_SHIFT_R\s*=\s*5'd29)", r"\1,\n    OP_FAKE      = 5'd30", s,1);open(p,"w").write(s)
EOF
grep -n "OP_FAKE\|OP_SHIFT_R" "$pkg" | sed 's/^/    planted: /' >>"$out"; gate; restore

plant "D2 the stale row dropped from the 09 §7 target table"
sed -i '/^| `stale` | `Makefile` |/d' "$p09"; gate; restore

plant "D3 the inventory row dropped from the 09 §7 target table"
sed -i '/^| `inventory` | `scripts\/check-doc-inventory.py`/d' "$p09"; gate; restore

plant "D4 a target (newgate) added to the check rule"
sed -i 's/^check: \(.*\)$/check: \1 newgate/' Makefile; grep -n '^check:' Makefile | sed 's/^/    planted: /' >>"$out"; gate; restore

plant "D5 06 restored to its 18a4dc1 text"
git show "$old:$p06" >"$p06"; gate; restore

plant "D6 SHIFT_R removed from the Ops cell, still named in the Notes cell"
sed -i 's/`SET_MASKED`, `SHIFT_R` |/`SET_MASKED` |/' "$p06"; grep -n '^| Data |' "$p06" | sed 's/^/    planted: /' >>"$out"; gate; restore

plant "D7 µISA heading count off by one (31)"
sed -i 's/^\*\*µISA (30 operations)\*\*/**µISA (31 operations)**/' "$p06"; gate; restore

plant "D8 an operation named twice (MOVE added to Flow)"
sed -i 's/^| Flow | `NOP`,/| Flow | `NOP`, `MOVE`,/' "$p06"; gate; restore

plant "D9 make check with D1 planted (rc of the make target)"
python3 -I - "$pkg" <<'EOF'
import sys,re;p=sys.argv[1];s=open(p).read()
s=re.sub(r"(OP_SHIFT_R\s*=\s*5'd29)", r"\1,\n    OP_FAKE      = 5'd30", s,1);open(p,"w").write(s)
EOF
make inventory >"$out.tmp" 2>&1; echo "make inventory rc=$?" >>"$out"; tail -3 "$out.tmp" | sed 's/^/    /' >>"$out"; rm -f "$out.tmp"; restore

plant "L1 limit: a second check rule line adds a prerequisite (make merges both)"
printf '\ncheck: newgate\nnewgate:\n\t@true\n' >>Makefile
make -n check 2>/dev/null | grep -c . | sed 's/^/    make -n check lines: /' >>"$out"
make -pn check 2>/dev/null | grep -m1 '^check:' | sed 's/^/    make database: /' >>"$out"; gate; restore

plant "L2 limit: the check rule continued with a backslash"
sed -i 's/^check: lint /check: lint \\\n  /' Makefile; grep -n -A1 '^check:' Makefile | sed 's/^/    planted: /' >>"$out"; gate; restore

plant "L3 limit: the µISA count restated elsewhere (concept page banner says 29-operation)"
grep -n '29-operation' IEEE_1722_1_Hardware_Protocol_Processor.md | sed 's/^/    present at head: /' >>"$out"; gate; restore

echo "== end state" >>"$out"; { git rev-parse HEAD; git status --porcelain; } | sed 's/^/    /' >>"$out"
