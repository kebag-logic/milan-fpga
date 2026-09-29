#!/bin/bash
# One-off extra place-directive draws (same BASE as sweep.sh, different
# directives) for when the standard asl/eto/eppo trio misses timing on a
# luck-bound cone. Usage: sweep_extra.sh [--dry-run] <arty|ax7101> <tag>
# --dry-run may stand anywhere; any other option, and a missing or extra
# argument, is refused before anything launches.
# Seeds: exp=Explore, asm=AltSpreadLogic_medium, enl=ExtraNetDelay_low.
set -euo pipefail
# Clock and entity inputs follow the selected tracked shape, as in sweep.sh,
# one argv token per line. SWEEP_CFG selects another configuration; --dry-run
# prints without launching. A launch first rebuilds the configuration, as
# sweep.sh's entity_defs does: the SoC reads its builder output and includes
# its generated entity definition, whose directory the builder names.
config_options() {
  python3 - "$R" "$CFG" "$BOARD" "$DRY" <<'PY_CONFIG'
from pathlib import Path
import sys
sys.path.insert(0, str(Path(sys.argv[1]) / "sw/builder"))
import endstation_builder as eb
path = Path(sys.argv[1]) / sys.argv[2]
cfg = eb.load_config(path)
if cfg["board_target"] != sys.argv[3]:
    raise SystemExit("sweep_extra: configuration board does not match requested board")
gen = eb.ROOT / eb.GEN_CONFIG_DIR / cfg["name"]
if sys.argv[4] == "0":
    built = Path(eb.build(path)["paths"]["cfg_adp_shape_svh"]).parent.parent
    if built != gen:
        raise SystemExit(f"sweep_extra: {path} wrote its entity definition to {built}, not {gen}")
c = cfg["constraints"]
print("--sys-clk-freq", c["sys_clk_hz"], "--milan-clk-freq", c["milan_clk_hz"],
      "--entity-gen-dir", gen, sep="\n")
PY_CONFIG
}

usage() {
  echo "sweep_extra: $1; usage: sweep_extra.sh [--dry-run] <arty|ax7101> <tag>" >&2
  exit 2
}

parse_args() {
  DRY=0
  local arg
  local positional=()
  for arg in "$@"; do
    case "$arg" in
      --dry-run) DRY=1;;
      -*) usage "unknown option $arg";;
      *) positional+=("$arg");;
    esac
  done
  [ "${#positional[@]}" -eq 2 ] || usage "expected a board and a tag, got ${#positional[@]} argument(s)"
  BOARD=${positional[0]}; TAG=${positional[1]}
  [ -n "$TAG" ] || usage "empty tag"
}

launch() {
  local dir="$W/build_${BOARD}_${1}_${TAG}"
  # BASE is an array, so a configuration path keeps its spaces as one argument.
  setsid nohup "${BASE[@]}" --place-directive "$2" --output-dir "$dir" > "$dir.launch.log" 2>&1 < /dev/null &
  echo "LAUNCHED [${BOARD}_${1}_${TAG}] pid=$!"
}
main() {
  parse_args "$@"
  R="$(cd "$(dirname "$(realpath "$0")")/../.." && pwd)"
  W=$HOME/litex-milan/work
  # The build interpreter reads the configuration too, as in sweep.sh's setup_env.
  export PATH="$HOME/litex-milan/venv/bin:$PATH"
  case "$BOARD" in
    arty)   CFG="${SWEEP_CFG:-configs/endstation_arty_4x4.yaml}"; OPTS=(--board arty);;
    ax7101) CFG="${SWEEP_CFG:-configs/endstation_ax7101_1x1_tdm8.yaml}"
            OPTS=(--board ax7101 --gtx-tx-invert --floorplan);;
    *) usage "unknown board $BOARD";;
  esac
  # Check the substitution's status before appending; a missing/invalid
  # configuration must never fall back to the SoC's implicit clock.
  local config
  config=$(config_options)
  mapfile -t -O "${#OPTS[@]}" OPTS <<< "$config"
  # #259: bare-metal only, with no cache or alternate flash manifest.
  BASE=(python3 "$R/sw/litex/milan_soc.py" "${OPTS[@]}" --cpu vexiiriscv
        --software-profile baremetal --fabric-gptp --xlen 32
        --full --with-spiflash --flashboot baremetal --timing-opt
        --l2-bytes 0 --uart-baudrate 115200
        --cpu-count 1 --vivado-max-threads 32 --build)
  if [ "$DRY" -eq 1 ]; then
    # Shell-quoted, so the preview reads back as the argv a launch passes.
    local preview
    printf -v preview '%q ' "${BASE[@]}"
    echo "${preview% }"
    return
  fi
  source "$HOME/Xilinx/2026.1/Vivado/settings64.sh"
  cd "$W"
  rm -rf "build_${BOARD}_exp_${TAG}" "build_${BOARD}_asm_${TAG}" "build_${BOARD}_enl_${TAG}"
  launch exp Explore;               sleep 90
  launch asm AltSpreadLogic_medium; sleep 90
  launch enl ExtraNetDelay_low
}
main "$@"
