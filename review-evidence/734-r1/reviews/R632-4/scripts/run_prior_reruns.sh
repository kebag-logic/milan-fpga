#!/usr/bin/env bash
# Re-run the prior public reviewers' probes UNCHANGED (scripts taken from the
# published evidence tree beeb9d6c:review-evidence/734-r1/reviews) against this
# head, plus the R632-3 runner mutations inside a bubblewrap boundary and the
# five linked-image rebuild.  One log + rc per job; jobs run concurrently.
# Usage: run_prior_reruns.sh <packet> <reviews-dir> <full-clone-at-head> <python-with-yaml>
set -u
P="$1"; RV="$2"; REPO="$3"; PY="$4"; S="$P/scratch"; O="$P/receipts/prior"; mkdir -p "$O"
HEAD=59354ffe75697e17a16fd117d9ba853e104394bc; DEV=a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0
export PYTHONDONTWRITEBYTECODE=1
job() { local n="$1"; shift; ( "$@" ) > "$O/$n.log" 2>&1; echo $? > "$O/$n.rc"; }
# R632-1 probe_scope.py unchanged (hard-coded round-1 head), and its unchanged
# functions with HEAD rebound to this head via R632-2's unchanged wrapper.
rm -rf "$S/p1a" "$S/p1b" "$S/r1a" "$S/r1b"; mkdir -p "$S/p1a" "$S/p1b"
git clone --quiet --no-hardlinks "$REPO" "$S/r1a"; git clone --quiet --no-hardlinks "$REPO" "$S/r1b"
for r in "$S/r1a" "$S/r1b"; do git -C "$r" fetch --quiet "$REPO" 6c810c45ac4ac7d5b45797430753020c9ea31d86 f1b2489f5b1c929e81eeae79a469b2b27c47e340 49da9fd974e8805d56c90e29dcfcb67994c2c430; done
job r632-1-probe-unchanged "$PY" -I "$RV/R632-1/scripts/probe_scope.py" "$S/r1a" "$S/p1a" &
job r632-1-probe-rebound-head "$PY" -I "$RV/R632-2/rerun_prior_probe_at_head.py" "$RV/R632-1/scripts/probe_scope.py" "$S/r1b" "$S/p1b" "$HEAD" &
# R632-2 probe unchanged against this head's shipping tree.
rm -rf "$S/p2"; mkdir -p "$S/p2"
job r632-2-probe-unchanged "$PY" -I "$RV/R632-2/probe_r632_2.py" "$REPO" "$S/p2" &
# R632-3 real-lane and rename probes unchanged.
rm -rf "$S/p3" "$S/p3r"; mkdir -p "$S/p3" "$S/p3r"
job r632-3-real-lanes bash -c "bash '$RV/R632-3/build_real_lanes.sh' '$REPO' '$S/p3' 49da9fd974e8805d56c90e29dcfcb67994c2c430 $DEV $HEAD && '$PY' -I '$RV/R632-3/probe_r632_3.py' '$REPO' '$REPO' '$S/p3' '$S/p3/cases.json'" &
job r632-3-rename bash -c "bash '$RV/R632-3/build_rename_cases.sh' '$REPO' '$S/p3r' && mkdir -p '$S/p3r/scratch' && '$PY' -I '$RV/R632-3/probe_r632_3.py' '$S/p3r/src' '$REPO' '$S/p3r/scratch' '$S/p3r/cases.json'" &
rm -rf "$S/p3h"; mkdir -p "$S/p3h"
job r632-3-hostile-env bash "$RV/R632-3/hostile_env_check.sh" "$REPO" "$S/p3h" &
# R632-3 runner mutations R01-R03 in both invocation forms, inside bubblewrap.
for id in R01_wiring_removed R02_sibling_import_outside_scope_event R03_sibling_import_in_scope_event; do
  rm -rf "$S/mut-$id"
  python3 -I "$RV/R632-3/apply_mutation.py" "$REPO" "$S/mut-$id" "$RV/R632-3/mutations_runner.json" "$id" > "$O/mut-$id.apply.log" 2>&1
  for mode in ordinary flat; do
    job "mut-$id-$mode" bash "$RV/R632-3/run_act_selftest_boxed.sh" "$S/mut-$id" "$S/box-$id-$mode" "$mode" &
  done
done
# Five linked images: base a0f39ad4 vs this head, pinned SDK, network-less boundary.
rm -rf "$S/images"; mkdir -p "$S/images"
cp $VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz "$S/images/sdk.tar.xz"
job images bwrap --unshare-all --die-with-parent --new-session --ro-bind / / --dev /dev --proc /proc \
  --tmpfs /tmp --tmpfs /home --tmpfs /run --bind "$S/images" /work --ro-bind "$REPO" /candidate \
  --setenv HOME /tmp/home --setenv TMPDIR /tmp --setenv PYTHONDONTWRITEBYTECODE 1 \
  bash -euc 'mkdir -p /tmp/home; git clone --quiet --shared /candidate /work/tree
    git -C /work/tree -c protocol.file.allow=always -c submodule.protocol-processor.url=/candidate/protocol-processor -c submodule.gptp-processor.url=/candidate/gptp-processor -c submodule.third_party/verilog-axis.url=/candidate/third_party/verilog-axis submodule update --quiet --init protocol-processor gptp-processor third_party/verilog-axis
    git -C /work/tree rev-parse HEAD
    python3 /work/tree/scripts/ci_rv32_sdk.py --archive /work/sdk.tar.xz --destination /work/sdk
    export MILAN_RV32_CC=/work/sdk/bin/riscv32-linux-gcc; cd /work/tree
    python3 sw/firmware/ctrl/test/ctrl_image.py --shape endstation_arty_4x4 --shape endstation_arty_8ch --shape endstation_arty_current --shape endstation_ax7101_1x1_tdm8 --shape endstation_ax7101_8x8 --base a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0 --out /work/build' &
wait
