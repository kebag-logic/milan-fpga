#!/usr/bin/env bash
# m8a2_runs.sh STREAM: the split boot and NVM runs at the lane head, one log and one rc per run.
set -u
L=<lane>; S=<scratch>; R=$S/m8a2; mkdir -p "$R"
export PATH=<home>/br-milan-rv32/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tools>/pinned-verilator-5.050/verilator COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$S/tmp MAKEFLAGS="-j16 --no-print-directory"
mkdir -p "$TMPDIR"
PY=<home>/litex-milan/venv/bin/python3
cd "$L" || exit 3
run() { id=$1; shift; ( echo "# head $(git rev-parse HEAD) run $id: $*"; echo "# tree: $(git status --porcelain | tr '\n' ' ')"; date -Iseconds; bash -c "$*"; rc=$?; date -Iseconds; exit $rc ) > "$R/$id.log" 2>&1; echo $? > "$R/$id.rc"; }
case $1 in
  A)
    run boot-1x1-regrade "$PY -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-1x1 --regrade"
    run boot-8x8 "$PY -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-8x8 --shape endstation_ax7101_8x8"
    ;;
  C)
    run nvm_cosim "PATH=<tools>/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin make -C tb/verilator/nvm_cosim"
    for t in on off; do
      run nvm_capture_cpu-8x8-50-$t "$PY tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic $t --build-dir $S/nvmcap-8x8-50-$t"
    done
    ;;
  D)
    # the harness's recorded environment: the product interpreter first, host utilities before the SDK's
    for t in on off; do
      run nvm_capture_cpu-8x8-50-$t "PATH=<home>/litex-milan/venv/bin:<tools>/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin:<home>/br-milan-rv32/host/bin $PY -B tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic $t --build-dir $S/nvmcap-8x8-50-$t"
    done
    ;;
  B)
    run check_nvm_capture "/usr/bin/python3 scripts/check_nvm_capture.py"
    run nvm_split_target-8x8 "$PY -B tb/verilator/nvm_split_target/run.py --point 8x8 --build-dir $S/nvmt-8x8 --out $S/nvmt-8x8/out --jobs 8"
    run nvm_cosim "PATH=<tools>/pinned-verilator-5.050:/usr/local/bin:/usr/bin:/bin make -C tb/verilator/nvm_cosim"
    for t in on off; do
      run nvm_capture_cpu-8x8-50-$t "$PY tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 --traffic $t --build-dir $S/nvmcap-8x8-50-$t"
    done
    ;;
esac
echo done > "$R/DONE-$1"
