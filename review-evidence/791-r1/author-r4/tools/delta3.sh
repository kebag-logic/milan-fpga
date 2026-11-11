#!/usr/bin/env bash
# delta3.sh <chain>: round 3's gates on clean clones of the final head, each rc beside its log, and the
# netlist-identity runs at round 1's head in the same environment.
# chain a: test_ctrl_memory.py (its mutants and the guard shapes), the reviewer's guard and CpuPatches probes,
#          the product split export's decode at 1x1 and 8x8.
# chain b: the region-decode simulation's self-test, at the final head and at round 1's head.
# chain c: the all-fabric compare, base against the final head, every shipped config; the product split export's
#          decode at round 1's head.
set -u
S=/data-2/milan/tmp/791-a765c; F=$S/r3; C=$S/clones; PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
T=$MANAGEMENT/2026-09-23/791-a765c/tools
P=$MANAGEMENT/2026-09-23/791-r826-1/tools
P2=$MANAGEMENT/2026-09-23/791-r826-2/tools
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true PYTHONHASHSEED=0 PATH=$WORKSPACE_HOME/br-milan-rv32/host/bin:$PATH
mkdir -p "$F"
step() { local name=$1 cl=$2; shift 2; echo "$(date +%T) start $name"; ( cd "$cl" && "$@" ) > "$F/$name.log" 2>&1; echo $? > "$F/$name.rc"; echo "$(date +%T) $name rc $(cat "$F/$name.rc")"; }
SHAPES="endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8"
case $1 in
  a)
    rm -rf "$F/tcm-tmp"; mkdir -p "$F/tcm-tmp"; step tcm "$C/head3" env TMPDIR="$F/tcm-tmp" "$PY" -B sw/litex/test_ctrl_memory.py
    step guard-probe "$C/head3" "$PY" -I -B "$P/guard_probe.py" "$C/head3"
    step guard-probe2 "$C/head3" "$PY" -I -B "$P2/guard_probe2.py" "$C/head3"
    step cpupatches-probe "$C/head3" "$PY" -I -B "$P/cpupatches_probe.py" "$C/head3"
    rm -rf "$S/pd3" "$F/decode"; step product-decode "$C/head3-pd" "$PY" -B "$T/product_decode.py" "$C/head3-pd" "$S/pd3" "$F/decode" $SHAPES ;;
  b)
    rm -rf "$F/region-self"; step region-self-test "$C/head3" "$PY" -B tb/verilator/ctrl_region_decode/run.py --build-dir "$F/region-self" --self-test
    : the round-1-head self-test ran once, at 03447eaa, kept under r1/ ;;
  c)
    rm -rf "$S/allfabric3" "$F/allfabric-receipt"; step allfabric "$S" "$PY" "$T/allfabric_compare.py" "$C/base" "$C/head3-af" "$S/allfabric3" "$F/allfabric-receipt"
    : the round-1-head product decode ran once, at 03447eaa, kept under r1/ ;;
esac
echo "$(date +%T) chain $1 done"
