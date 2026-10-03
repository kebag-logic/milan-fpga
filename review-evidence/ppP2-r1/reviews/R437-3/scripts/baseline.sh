#!/usr/bin/env bash
# R437-3 baseline runs at the exact head, each on its own git-archive export
# (or, for make check, a disposable local clone). usage: baseline.sh REPO PKT VERILATOR WHAT
set -u
REPO=$1; PKT=$2; V=$3; WHAT=$4
HEAD=527662d659b4ead97675744d12a43af1ea92b9b3
S=$PKT/scratch/base_$WHAT; R=$PKT/receipts
rm -rf "$S"; mkdir -p "$S" "$R"
export VERILATOR=$V PATH="$(dirname "$(readlink -f "$V")"):$PATH"
if [ "$WHAT" = figures_clone ]; then
  git clone -q --no-hardlinks "$REPO" "$S/clone" && git -C "$S/clone" checkout -q --detach $HEAD
  ( make -C "$S/clone/tb/nvm_port" VERILATOR="$V" figures ) > "$R/figures_gate.log" 2>&1; echo $? > "$R/figures_gate.rc"
  git -C "$S/clone" status --porcelain --ignored > "$R/figures_gate_clone_status.txt"; exit 0
fi
if [ "$WHAT" = check ]; then
  git clone -q --no-hardlinks "$REPO" "$S/clone" && git -C "$S/clone" checkout -q --detach $HEAD
  ( cd "$S/clone" && make check ) > "$R/make_check.log" 2>&1; echo $? > "$R/make_check.rc"; exit 0
fi
git -C "$REPO" archive $HEAD | tar -x -C "$S"
case $WHAT in
  nvm_port) ( make -C "$S/tb/nvm_port" VERILATOR="$V" ) > "$R/nvm_port_make.log" 2>&1; echo $? > "$R/nvm_port_make.rc" ;;
  acmp_nvm) ( make -C "$S/tb/acmp_nvm" VERILATOR="$V" ) > "$R/acmp_nvm_make.log" 2>&1; echo $? > "$R/acmp_nvm_make.rc" ;;
  figures)  ( make -C "$S/tb/nvm_port" VERILATOR="$V" figures ) > "$R/figures_gate_export_nogit.log" 2>&1; echo $? > "$R/figures_gate_export_nogit.rc" ;;
esac
# (figures in a clone: the gate's pre-fix matrix reads git history, which an export lacks)
