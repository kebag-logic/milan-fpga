#!/bin/bash
# Run inside one exclusive acquisition of the Vivado lock: candidate route, base route, xvlog gate.
root=$SCRATCH
export PATH=$XILINX/2026.1/Vivado/bin:$LITEX_ENV/venv/bin:$PATH
export TMPDIR=$root/tmp PYTHONDONTWRITEBYTECODE=1
log=$root/vendor/driver.log
echo "$(date -Is) lock acquired" >> $log
run() {
  name=$1; dir=$2; shift 2
  echo "$(date -Is) START $name" >> $log
  (cd "$dir" && "$@") > "$root/vendor/$name.log" 2>&1
  rc=$?
  echo "$rc" > "$root/vendor/$name.rc"
  echo "$(date -Is) END $name: rc $rc" >> $log
  python3 $root/scripts/verify_images.py $root/res/base/ax7101/gateware/baseline_images.json $root/res/cand/ax7101/gateware/baseline_images.json > "$root/vendor/$name-images.log" 2>&1
  echo "$?" > "$root/vendor/$name-images.rc"
}
run route-1x1-cand $root/res/cand/ax7101/gateware vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log
run route-1x1-base $root/res/base/ax7101/gateware vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log
run xvlog-cand $root/exp-cand python3 scripts/xvlog_gate.py --check
echo "$(date -Is) releasing lock" >> $log
