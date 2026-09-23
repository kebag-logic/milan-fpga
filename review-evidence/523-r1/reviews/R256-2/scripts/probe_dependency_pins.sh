#!/usr/bin/env bash
# Reviewer probe: real-tree pinned dependency refusals of the production driver.
# Usage: probe_dependency_pins.sh COPY  (each case restored before the next)
set -u
copy="$1"; drv="$copy/tb/verilator/gptp_shadow/mutants.py"
run() {
  local out rc
  out=$(cd "$copy/tb/verilator/gptp_shadow" && env -u GIT_EDITOR PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 "$drv" 2>&1); rc=$?
  printf '%s\t%s\t%s\n' "$1" "$rc" "$(printf '%s\n' "$out" | grep -m1 -E 'REFUSED|RESULT|CANCELLED' | sed "s#$copy#<copy>#g")"
}
pin=$(git -C "$copy" ls-tree HEAD gptp-processor | awk '{print $3}')
parent=$(git -C "$copy/gptp-processor" rev-parse -q --verify "$pin^" || true)
if [ -n "$parent" ]; then
  git -C "$copy/gptp-processor" checkout -q "$parent"; run "gptp-processor checked out at parent of pin"
  git -C "$copy/gptp-processor" checkout -q "$pin"
else
  printf 'gptp-processor parent\tunavailable in shallow module\t-\n'
fi
mv "$copy/third_party/verilog-axis" "$copy/axis-saved"; mkdir "$copy/third_party/verilog-axis"
run "verilog-axis uninitialised (empty directory)"
rmdir "$copy/third_party/verilog-axis"
cp -r "$copy/axis-saved" "$copy/third_party/verilog-axis"; rm -f "$copy/third_party/verilog-axis/.git"
run "verilog-axis cp -r lane copy with .git removed"
rm -rf "$copy/third_party/verilog-axis"; mv "$copy/axis-saved" "$copy/third_party/verilog-axis"
printf '// local\n' >> "$copy/gptp-processor/hdl/top/KL_gptp_engine.sv"
run "dirty gptp-processor build input"
git -C "$copy/gptp-processor" checkout -q -- hdl/top/KL_gptp_engine.sv
printf 'x\n' > "$copy/gptp-processor/docs-only-untracked.txt"
run "untracked file outside copied dependency scope"
rm -f "$copy/gptp-processor/docs-only-untracked.txt"
