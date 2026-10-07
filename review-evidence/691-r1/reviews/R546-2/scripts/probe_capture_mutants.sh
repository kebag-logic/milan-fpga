#!/usr/bin/env bash
# Source-level mutation probes for sw/litex/test_gmii_rx_capture.py.
# Usage: probe_capture_mutants.sh <repo-at-head> <patched-liteeth-tree> <venv-python> <work-dir>
# Each mutant edits a private copy of liteeth/phy/gmii.py (never the input tree),
# runs the test with that copy first on sys.path, and expects a non-zero exit.
set -u
REPO=$1; LITEETH=$2; PY=$3; WORK=$4
mkdir -p "$WORK"
run_mutant() {
    local name=$1 from=$2 to=$3 dir="$WORK/$1"
    mkdir -p "$dir"
    cp -a "$LITEETH/." "$dir/"
    python3 - "$dir/liteeth/phy/gmii.py" "$from" "$to" <<'EOF'
import sys
p, a, b = sys.argv[1:]
s = open(p).read()
assert s.count(a) == 1, ("anchor", a, s.count(a))
open(p, "w").write(s.replace(a, b))
EOF
    (cd /tmp && PYTHONPATH="$dir" "$PY" -I -c "import sys; sys.path.insert(0, '$dir'); sys.argv=['t']; import runpy; runpy.run_path('$REPO/sw/litex/test_gmii_rx_capture.py', run_name='__main__')") > "$WORK/$name.log" 2>&1
    local rc=$?
    local loaded
    loaded=$(cd /tmp && "$PY" -I -c "import sys; sys.path.insert(0, '$dir'); import liteeth.phy.gmii as g; print(g.__file__)")
    if [ $rc -ne 0 ]; then verdict=CAUGHT; else verdict=SURVIVED; fi
    echo "$verdict $name rc=$rc module=${loaded#$WORK/} reason=$(grep -m1 -E 'AssertionError|Error' "$WORK/$name.log" | cut -c1-120)"
}
run_mutant valid_reset_restored "rx_dv = Signal(reset_less=True)" "rx_dv = Signal()"
run_mutant data_reset_restored "rx_data = Signal(8, reset_less=True)" "rx_data = Signal(8)"
run_mutant live_reset_mask "source.valid.eq(rx_dv & ~rx_reset)," "source.valid.eq(rx_dv & ~ResetSignal()),"
run_mutant data_mask_dropped "source.data.eq(Mux(rx_reset, 0, rx_data))," "source.data.eq(rx_data),"
run_mutant last_from_raw_dv "source.last.eq(~pads.rx_dv & source.valid)," "source.last.eq(~pads.rx_dv & rx_dv),"
run_mutant reset_initial_zero "rx_reset = Signal(reset=1, reset_less=True)" "rx_reset = Signal(reset=0, reset_less=True)"
