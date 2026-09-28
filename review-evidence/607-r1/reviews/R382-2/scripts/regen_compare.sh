#!/usr/bin/env bash
# Item (5): show that no timing-relevant generated constraint text changed between the round-1
# head (whose sweep is the acceptance-4 evidence) and the round-2 head. For each head, a copy of
# the clone is set to that head's tracked content for the delta's files, the shipping AX7101
# configs are elaborated through the builder argv (no vendor run, no firmware compile), and the
# generated alinx_ax7101.{tcl,xdc,v} are normalised (copy root and output dir -> tokens; the
# .v date stamp line dropped) and compared.
# Usage: regen_compare.sh <clean-clone> <scratch-dir> <litex-python> <old-sha> <new-sha>
set -uo pipefail
SRC=$1; WORK=$2; PY=$3; OLD=$4; NEW=$5
export PYTHONHASHSEED=0 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
export PATH="$(dirname "$PY"):/usr/bin:/bin"
mkdir -p "$WORK/tmp"
for sha in "$OLD" "$NEW"; do
  D=$WORK/src-$sha; rm -rf "$D"; mkdir -p "$D"
  (cd "$SRC" && tar --exclude=sw/builder/out -cf - .) | (cd "$D" && tar -xf -)
  (cd "$D" && git diff --name-only "$OLD" "$NEW" | while read -r f; do
      if git cat-file -e "$sha:$f" 2>/dev/null; then git show "$sha:$f" > "$f"; else rm -f "$f"; fi
    done)
  for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    O=$WORK/out-$sha-$cfg; rm -rf "$O"
    (cd "$D" && TMPDIR=$WORK/tmp "$PY" sw/builder/endstation_builder.py "configs/$cfg.yaml" >/dev/null)
    ARGV=$(cd "$D" && "$PY" -c "import json;print(' '.join(json.load(open('sw/builder/out/$cfg/soc_params.json'))['argv']))")
    (cd "$D/sw/litex" && TMPDIR=$WORK/tmp "$PY" milan_soc.py $ARGV --entity-gen-dir "$D/configs/generated/$cfg" \
        --no-compile-software --vivado-max-threads 16 --output-dir "$O" > "$O.log" 2>&1) || { echo "$sha $cfg elaboration FAILED"; tail -3 "$O.log"; }
    for ext in tcl xdc v; do
      f=$O/gateware/alinx_ax7101.$ext
      [ -f "$f" ] || continue
      sed -e "s#$D#<SRC>#g" -e "s#$O#<OUT>#g" "$f" | grep -v '^// Date' > "$O.norm.$ext"
    done
  done
done
for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for ext in tcl xdc v; do
    a=$WORK/out-$OLD-$cfg.norm.$ext; b=$WORK/out-$NEW-$cfg.norm.$ext
    if cmp -s "$a" "$b"; then r=IDENTICAL; else r="DIFFERS ($(diff "$a" "$b" | grep -c '^[<>]') lines)"; fi
    echo "$cfg alinx_ax7101.$ext ${OLD:0:8} vs ${NEW:0:8}: $r  sha256(new,normalised)=$(sha256sum "$b" | cut -c1-16)"
  done
done
