#!/usr/bin/env bash
# rsweep.sh <clone> <work> [names..]: the #649 resource map's builder and SoC steps in a fresh clone, as the findings
# page's recipe runs them: yosys_sweep.py shapes (the tree export and every variant shape), then soc_sweep.py export
# of the named SoC variants (all when none), with the lane's LiteX venv and the pinned RV32 SDK. Before the export it
# records whether any platform image exists in the export tree or the clone, so a pass cannot lean on one.
set -u
C=$1; W=$2; shift 2
source <scratch>/bin/env.sh
cd "$C"
echo "head $(git rev-parse HEAD) porcelain $(git status --porcelain --untracked-files=all | wc -l) $(date -Iseconds)"
rm -rf "$W"; mkdir -p "$W"
python3 -B syn/resmap/yosys_sweep.py --work "$W" shapes; rs=$?
echo "shapes rc=$rs"
echo "platform images before export: $(find "$C/sw/builder" "$W" -name ctrl_app.elf 2>/dev/null | wc -l)"
python3 -B syn/resmap/soc_sweep.py --work "$W" --litex-python "$(command -v python3)" --sdk "$SDK/host" export "$@"; re=$?
echo "export rc=$re"
python3 - "$W/soc/exports.json" <<'EOF'
import json, sys
for name, r in sorted(json.load(open(sys.argv[1])).items()):
    print(f"  {name}: rc={r['rc']} expected={r['expected']} {r['refusal'] or r['cpu_netlist']}")
EOF
for d in "$W"/soc/*/export/gateware; do [ -f "$d/alinx_ax7101.v" ] && echo "  $(basename "$(dirname "$(dirname "$d")")") top $(sha256sum < "$d/alinx_ax7101.v" | cut -c1-16)"; done
echo "END shapes=$rs export=$re $(date -Iseconds)"
