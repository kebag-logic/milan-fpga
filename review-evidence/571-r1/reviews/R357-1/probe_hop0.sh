#!/usr/bin/env bash
# R357-1 hop-0 propagation: copy a tree, give the include-selected per-config
# header distinct unit counts (AUDIO_UNIT=2, CLOCK_DOMAIN=3, CONTROL=4 when the
# header has it), elaborate milan_datapath with --json-only through the repo's
# own source emitter, and report the processor-side values.
# Usage: probe_hop0.sh <verilator> <tree> <copy-dir> <mdir> <receipt>
set -eu
V=$1; T=$(cd "$2" && pwd); C=$3; M=$4; R=$5
rm -rf "$C" "$M"; cp -a "$T" "$C"; C=$(cd "$C" && pwd); mkdir -p "$M"; M=$(cd "$M" && pwd)
EMIT=$(cd "$C" && bash syn/yosys/run.sh --emit milan_datapath 2>/dev/null)
INC=$(echo "$EMIT" | awk -F= '$1=="incdir"{print $2; exit}')
H="$INC/gen/adp_shape_defaults.svh"
sed -i -E 's/(AEM_N_AUDIO_UNIT_C = )1;/\12;/; s/(AEM_N_CLKDOM_C     = )1;/\13;/; s/(AEM_N_CONTROL_C    = )1;/\14;/' "$H"
A=$(echo "$EMIT" | awk -F= '$1=="incdir"{printf "+incdir+%s ", $2} $1=="define"{printf "-D%s ", $2} $1=="src"{printf "%s ", $2}')
(cd "$C" && timeout 1500 "$V" --json-only -Wno-fatal --top-module milan_datapath --Mdir "$M" $A) > "$M/log.txt" 2>&1
{ echo "== tree $(cd "$T" && git rev-parse HEAD 2>/dev/null); first incdir header: ${H#$C/}"
  grep -n 'AEM_N_' "$H"
  echo "included header(s):"; grep -o '"[^"]*adp_shape_defaults.svh"' "$M/Vmilan_datapath.tree.meta.json" | sort -u | sed "s#$C/##"
  python3 "$(dirname "$0")/probe_json_params.py" "$M/Vmilan_datapath.tree.json"; } | tee -a "$R"
