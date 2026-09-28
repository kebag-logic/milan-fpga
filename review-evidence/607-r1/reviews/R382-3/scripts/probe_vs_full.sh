#!/usr/bin/env bash
# Item (2): the shipping probe must read the same generated build files a real, unmodified
# Builder would write. For each shipping config and port, elaborate twice on the same
# interpreter and tree:
#   probe: sw/builder/test_shipping_clock_constraints.py --config --port --output-dir
#          (InspectBuilder, include step with with_bios=False, firmware-data guard)
#   full:  sw/litex/milan_soc.py with the same builder argv, --eth-port, --no-compile-software,
#          --no-compile-gateware, --vivado-max-threads 16 (stock Builder, BIOS includes on)
# then compare the normalised gateware alinx_ax7101.{tcl,xdc,v} and the whole output file list.
# The full run needs LiteX's firmware data packages; SHIM (optional) is a PYTHONPATH directory
# exposing them to an interpreter that lacks them (full run only; the probe never gets SHIM).
# Usage: probe_vs_full.sh <tree> <python> <workdir> [shim]
set -uo pipefail
T=$1; PY=$2; W=$3; SHIM=${4:-}
export PYTHONHASHSEED=0 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false
mkdir -p "$W/tmp"; export TMPDIR="$W/tmp"
echo "python: $("$PY" --version)  shim: ${SHIM:-none}"
for cfg in ax7101_1x1_tdm8 ax7101_8x8; do
  for port in e1 e2; do
    P=$W/probe-$cfg-$port; F=$W/full-$cfg-$port; rm -rf "$P" "$F"
    (cd "$T/sw/litex" && "$PY" -B "$T/sw/builder/test_shipping_clock_constraints.py" \
        --config "$cfg" --port "$port" --output-dir "$P" > "$P.log" 2>&1)
    prc=$?
    ARGV=$(cd "$T" && "$PY" -c "import json;print(' '.join(json.load(open('sw/builder/out/endstation_$cfg/soc_params.json'))['argv']))")
    (cd "$T/sw/litex" && PYTHONPATH="$SHIM" "$PY" -B milan_soc.py $ARGV \
        --entity-gen-dir "$T/configs/generated/endstation_$cfg" --eth-port "$port" \
        --no-compile-software --no-compile-gateware --vivado-max-threads 16 \
        --output-dir "$F" > "$F.log" 2>&1)
    frc=$?
    echo "== $cfg $port: probe rc=$prc ($(grep -c '^\[constraints\] shipping .* PASS$' "$P.log") PASS line), full rc=$frc"
    for ext in tcl xdc v; do
      a=$P/gateware/alinx_ax7101.$ext; b=$F/gateware/alinx_ax7101.$ext
      if [ ! -f "$a" ] || [ ! -f "$b" ]; then echo "  $ext: MISSING (probe $( [ -f "$a" ] && echo y || echo n ) full $( [ -f "$b" ] && echo y || echo n ))"; continue; fi
      sed -e "s#$P#<OUT>#g" "$a" | grep -v '^// Date' > "$a.norm"
      sed -e "s#$F#<OUT>#g" "$b" | grep -v '^// Date' > "$b.norm"
      if cmp -s "$a.norm" "$b.norm"; then r=IDENTICAL; else r="DIFFERS ($(diff "$a.norm" "$b.norm" | grep -c '^[<>]') lines)"; fi
      echo "  alinx_ax7101.$ext probe vs full: $r  sha256(probe,normalised)=$(sha256sum "$a.norm" | cut -c1-16)"
    done
    (cd "$P" && find . -type f ! -name '*.norm' | sort) > "$W/files-probe-$cfg-$port"
    (cd "$F" && find . -type f ! -name '*.norm' | sort) > "$W/files-full-$cfg-$port"
    echo "  files only in full output: $(comm -13 "$W/files-probe-$cfg-$port" "$W/files-full-$cfg-$port" | tr '\n' ' ')"
    echo "  files only in probe output: $(comm -23 "$W/files-probe-$cfg-$port" "$W/files-full-$cfg-$port" | tr '\n' ' ')"
    echo "  common files: $(comm -12 "$W/files-probe-$cfg-$port" "$W/files-full-$cfg-$port" | wc -l)"
    for g in software/include/generated/csr.h software/include/generated/soc.h software/include/generated/mem.h csr.json; do
      if [ -f "$P/$g" ] && [ -f "$F/$g" ]; then
        if cmp -s <(sed -e "s#$P#<OUT>#g" "$P/$g") <(sed -e "s#$F#<OUT>#g" "$F/$g"); then echo "  $g: IDENTICAL"; else echo "  $g: DIFFERS"; fi
      fi
    done
  done
done
