#!/bin/sh
# Launch the reviewer's independent campaigns concurrently, each with its own
# log and rc file. usage: run_all.sh <clone> <packet>
set -u
clone=$1; pkt=$2
V=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
R=$pkt/receipts; S=$pkt/scratch
mkdir -p "$R" "$S/tmp"
export TMPDIR=$S/tmp PYTHONDONTWRITEBYTECODE=1
launch() {  # name, command...
  name=$1; shift
  ( "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) &
}
# 1. the exact-head dispatch campaign, every arm (53)
launch dispatch-campaign python3 -B "$clone/tb/pp_top/aecp_dispatch_mutants.py" \
  --output "$S/out-dispatch" --verilator "$V" --jobs 3
# 2. the exact-head decode standing controls, every arm (17)
launch decode-controls python3 -B "$clone/tb/aecp_cmds/mutants.py" \
  --output "$S/out-decode" --verilator "$V" --jobs 3
# 3. reviewer probe arms on the dispatch driver
launch probe-dispatch python3 -B "$pkt/scripts/probe_dispatch.py" "$clone" \
  "$pkt/probes/dispatch" "$S/out-probe-dispatch" "$V" 2
# 4. reviewer probe edits on the decode controls
launch probe-decode python3 -B "$pkt/scripts/probe_decode.py" "$clone" \
  "$S/out-probe-decode" "$V"
# 5. tb/pp_top main suite (all seven builds) and 6. docs gates, in a local copy
rm -rf "$S/copy-head"
git clone -q --no-hardlinks "$clone" "$S/copy-head" && git -C "$S/copy-head" checkout -q --detach 6aaec5dfc45e84c8842f3f31f76910bfa91a96e1
launch pp-top-run make -C "$S/copy-head/tb/pp_top" run VERILATOR="$V"
launch make-check-gates make -C "$S/copy-head" -k links matrix reqtags modmatrix params aecpcmd ids figures stale lint
wait
echo ALL-DONE > "$R/run_all.done"
