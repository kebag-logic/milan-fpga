#!/usr/bin/env bash
# boot.sh <shape> <build-dir>: the split boot at the head (S9's m8a2_runs.sh environment); its image-provisional and
# runtime archives are route_image.sh's stand-in inputs. Writes <build-dir>.rc.
S=<scratch>/r5fitP11
export PATH=<home>/br-milan-rv32/host/bin:<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
export VERILATOR=<tools>/pinned-verilator-5.050/verilator COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
export PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux TMPDIR=$S/tmp MAKEFLAGS="-j8 --no-print-directory"
cd $S/repo1x1 || exit 3
echo "head $(git rev-parse HEAD) tree: $(git status --porcelain | tr '\n' ' ')"
date -Iseconds
<home>/litex-milan/venv/bin/python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$2" --shape "$1"
rc=$?; date -Iseconds; echo $rc > "$2.rc"
