#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Licence acceptance probes on disposable exported copies; the checkout is never edited.
# Usage: licence_probes.sh <checkout> <scratch> <canonical-apache-text>
set -u
SRC=$(cd "$1" && pwd); SCR=$2; CANON=$3
BASE=a4cbe41de1c80d43f26e0d348cbdb45075273a4f; HEAD=f800a2bb920c543934d6286a47fe20dde3efa2c5
export PYTHONDONTWRITEBYTECODE=1
echo "== A1 byte identity"
cmp "$SRC/LICENSE" "$CANON"; echo "cmp head LICENSE vs canonical rc=$?"
git -C "$SRC" show "$BASE:LICENSE" > "$SCR/base-LICENSE"
cmp -s "$SCR/base-LICENSE" "$CANON"; echo "cmp base LICENSE vs canonical rc=$? (expect 1)"
tail -n +3 "$SCR/base-LICENSE" | cmp -s - "$CANON"; echo "base LICENSE minus first two lines vs canonical rc=$? (expect 0)"
echo "canonical blob $(git hash-object "$CANON"); head blob $(git -C "$SRC" rev-parse "$HEAD:LICENSE")"
echo "== A1 discriminating mutations (each must differ from canonical)"
m() { local n=$1; shift; "$@" > "$SCR/mut-$n"; cmp -s "$SCR/mut-$n" "$CANON"; echo "mutation $n: cmp rc=$? (expect 1)"; }
m spdx-readded sh -c "printf 'SPDX-License-Identifier: Apache-2.0\n\n'; cat '$CANON'"
m crlf sed 's/$/\r/' "$CANON"
m trailing-newline-dropped head -c -1 "$CANON"
m leading-blank-dropped tail -n +2 "$CANON"
echo "== A3 SPDX sweep (first 400 bytes) at base and head"
for rev in $BASE $HEAD; do
  n=0; miss=""
  for f in $(git -C "$SRC" ls-tree -r --name-only $rev); do
    n=$((n+1)); git -C "$SRC" show "$rev:$f" | head -c 400 | grep -q 'SPDX-License-Identifier: Apache-2.0' || miss="$miss $f"
  done
  echo "$rev files=$n missing-SPDX:${miss:- none}"
done
echo "changed paths: $(git -C "$SRC" diff --name-only $BASE $HEAD | tr '\n' ' ')"
echo "== Docs link rule: the LICENSE link is required and must resolve"
rm -rf "$SCR/probe-nolicense"; mkdir -p "$SCR/probe-nolicense"
git -C "$SRC" archive $HEAD | tar -x -C "$SCR/probe-nolicense"
rm "$SCR/probe-nolicense/LICENSE"
( cd "$SCR/probe-nolicense" && python3 doc/tools/check_links.py --local-only ) > "$SCR/probe-nolicense.log" 2>&1
echo "check_links with LICENSE removed rc=$? (expect nonzero)"; grep -E 'LICENSE|failures' "$SCR/probe-nolicense.log" | head -8
