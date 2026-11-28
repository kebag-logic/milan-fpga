#!/bin/bash
# ratchet_probes.sh PACKET REPO COPY: COPY is measure.sh's output for REPO's head (COPY/src exported tree, COPY/build after ctest).
# Regenerate the ratchet there and compare bytes with the committed file; then run the coverage gate against edited ratchets.
P=$1; R=$2; B=$3/build; W=$3
. "$P/scripts/env.sh" "$P"
cd "$W/src" || exit 2
echo "head $(git -C "$R" rev-parse HEAD)"
rm tests/coverage.ratchet; python3 scripts/coverage.py "$B" --write > "$W/write.log" 2>&1; echo "coverage.py --write rc $?"
cmp tests/coverage.ratchet <(git -C "$R" show HEAD:tests/coverage.ratchet) && echo "regenerated ratchet is byte-identical to the committed one"
sha256sum tests/coverage.ratchet
probe() { # label, sed expression on the committed ratchet
  git -C "$R" show HEAD:tests/coverage.ratchet | sed -E "$2" > tests/coverage.ratchet
  python3 scripts/coverage.py "$B" > "$W/probe.log" 2>&1; rc=$?
  echo "probe [$1]: rc $rc : $(grep -v -E '(after exclusions|%)' "$W/probe.log" | tr '\n' ' ')"
}
probe "committed ratchet" 's/^$//'
git -C "$R" show 5a07d9b7d87298f04b15aa28f0304ec88b0aef81:tests/coverage.ratchet > tests/coverage.ratchet
python3 scripts/coverage.py "$B" > "$W/probe.log" 2>&1; echo "probe [base ratchet 205/97 813/424 at head's measurement]: rc $? (fraction compare: record-only change)"
probe "adp row removed" '/^src\/adp.c/d'
probe "adp row recorded at 216/216 96/96 (not the measurement)" 's#^src/adp.c .*#src/adp.c  lines 216/216  branches 96/96#'
probe "adp branches floor above measurement as a fraction (95/94)" 's#branches 95/95#branches 95/94#'
probe "extra file row" '$a src/extra.c  lines 1/1  branches 0/0'
