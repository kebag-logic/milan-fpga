#!/bin/bash
# One-off extra place-directive draws (same BASE as sweep.sh, different
# directives) for when the standard asl/eto/eppo trio misses timing on a
# luck-bound cone. Usage: sweep_extra.sh <arty|ax7101> <tag> [--dry-run]
# Seeds: exp=Explore, asm=AltSpreadLogic_medium, enl=ExtraNetDelay_low.
set -euo pipefail
# Clock inputs follow the selected tracked shape, as in sweep.sh.
# SWEEP_CFG selects another configuration; --dry-run prints without launching.
clock_options() {
  python3 - "$R" "$CFG" "$BOARD" <<'PY_CLOCK'
from pathlib import Path
import sys
sys.path.insert(0, str(Path(sys.argv[1]) / "sw/builder"))
import endstation_builder as eb
cfg = eb.load_config(Path(sys.argv[1]) / sys.argv[2])
if cfg["board_target"] != sys.argv[3]:
    raise SystemExit("sweep_extra: configuration board does not match requested board")
c = cfg["constraints"]
print(f"--sys-clk-freq {c['sys_clk_hz']} --milan-clk-freq {c['milan_clk_hz']}")
PY_CLOCK
}

launch() {
  local dir="$W/build_${BOARD}_${1}_${TAG}"
  # $BASE is a command LINE, not a path: the word split is what turns it back
  # into argv, so it stays unquoted - quoting it would hand milan_soc.py one
  # 200-character argument. The directive rides on the command's own line
  # (check_sh_idiom reads it per line), which is why the redirections fold up.
  setsid nohup $BASE --place-directive "$2" --output-dir "$dir" > "$dir.launch.log" 2>&1 < /dev/null &  # shellcheck disable=SC2086
  echo "LAUNCHED [${BOARD}_${1}_${TAG}] pid=$!"
}
main() {
  BOARD=${1:?board}; TAG=${2:?tag}
  R="$(cd "$(dirname "$(realpath "$0")")/../.." && pwd)"
  W=$HOME/litex-milan/work
  case "$BOARD" in
    arty)   CFG="${SWEEP_CFG:-configs/endstation_arty_4x4.yaml}"; OPTS="--board arty";;
    ax7101) CFG="${SWEEP_CFG:-configs/endstation_ax7101_1x1_tdm8.yaml}"
            OPTS="--board ax7101 --gtx-tx-invert --floorplan";;
    *) echo "unknown board $BOARD" >&2; exit 2;;
  esac
  # Check the substitution's status before appending; a missing/invalid
  # configuration must never fall back to the SoC's implicit clock.
  local clocks
  clocks=$(clock_options)
  OPTS="$OPTS $clocks"
  # #259: bare-metal only, with no cache or alternate flash manifest.
  BASE="python3 $R/sw/litex/milan_soc.py $OPTS --cpu vexiiriscv \
 --software-profile baremetal --fabric-gptp --xlen 32 \
 --full --with-spiflash --flashboot baremetal --timing-opt \
 --l2-bytes 0 --uart-baudrate 115200 \
 --cpu-count 1 --vivado-max-threads 32 --build"
  if [ "${3:-}" = "--dry-run" ]; then
    echo "$BASE"
    return
  fi
  export PATH="$HOME/litex-milan/venv/bin:$PATH"
  source "$HOME/Xilinx/2026.1/Vivado/settings64.sh"
  cd "$W"
  rm -rf "build_${BOARD}_exp_${TAG}" "build_${BOARD}_asm_${TAG}" "build_${BOARD}_enl_${TAG}"
  launch exp Explore;               sleep 90
  launch asm AltSpreadLogic_medium; sleep 90
  launch enl ExtraNetDelay_low
}
main "$@"
