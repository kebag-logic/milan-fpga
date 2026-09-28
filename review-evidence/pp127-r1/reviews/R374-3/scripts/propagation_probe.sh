#!/usr/bin/env bash
# Usage: propagation_probe.sh <processor-clone> <scratch-dir> <out-dir>
# Disposable copies of the exact head; each trims the committed arm table to one
# arm and runs the hdl.yml step body under `bash -e` (the hosted default shell),
# with the pinned simulator first on PATH. Every variant must make the step fail.
#  cover-gap : one real arm (killed) -> family coverage incomplete -> nonzero
#  no-apply  : the arm's patch context no longer matches -> git apply --check fails
#  survivor  : the arm's patch edits only a comment -> UNPROVEN -> nonzero
set -u
here=$(cd "$(dirname "$0")" && pwd); pp=$(cd "$1" && pwd); s=$2; out=$(mkdir -p "$3" && cd "$3" && pwd)
export REAL_VERILATOR=${REAL_VERILATOR:-$VALIDATION_STORAGE/pp127-manager-0404675d/pinned-tool-bin/verilator} VJOBS=2
probe() {
  v=$1; t=$s/prop-$v; rm -rf "$t"; git clone -q "$pp" "$t"; git -C "$t" checkout -q 0404675dcd8788d29cb15a831a8c182438bf1c92
  python3 - "$t" "$v" <<'PY'
import sys, re; from pathlib import Path
t, v = Path(sys.argv[1]), sys.argv[2]
d = t / "tb/srp_top/mutants.py"; s = d.read_text()
s = re.sub(r"MUTANTS = \[\n.*?\n\]", "MUTANTS = [\n    ('bad-listener-length', 'srp_top', 'phases', 'K12:'),\n]", s, flags=re.S)
d.write_text(s)
p = t / "tb/srp_top/mutations/bad-listener-length.patch"; lines = p.read_text().splitlines(True)
if v == "no-apply":
    i = next(k for k, l in enumerate(lines) if l.startswith(" ") and l.strip()); lines[i] = " // drifted context\n"
    p.write_text("".join(lines))
PY
  if [ "$v" = survivor ]; then
    f=$(sed -n 's|^+++ b/||p' "$t/tb/srp_top/mutations/bad-listener-length.patch" | head -1)
    ( cd "$t" && cp "$f" "$f.orig" && sed -i '1s|$| // survivor probe|' "$f" && git diff --no-index "$f.orig" "$f" | sed "s|a/$f.orig|a/$f|; s|b/$f|b/$f|" > tb/srp_top/mutations/bad-listener-length.patch; mv "$f.orig" "$f" )
  fi
  git -C "$t" diff --stat | tail -1
  ( cd "$t" && PATH="$here:$PATH" TMPDIR="$here/../scratch/tmp" bash -e -c 'export PATH="$HOME/verilator/bin:$PATH"; make -C tb/srp_top mutants MUTANT_OUTPUT="'"$out/prop-$v"'"' ) > "$out/prop-$v.log" 2>&1
  echo "STEP_RC=$?" >> "$out/prop-$v.log"; echo "== $v: $(grep -E 'KILLED|UNPROVEN|coverage|checks:|CalledProcessError|Error [0-9]' "$out/prop-$v.log" | tr '\n' ' ' | cut -c1-300) $(tail -1 "$out/prop-$v.log")"
}
mkdir -p "$here/../scratch/tmp"
for v in ${VARIANTS:-cover-gap no-apply survivor}; do probe $v & done; wait
