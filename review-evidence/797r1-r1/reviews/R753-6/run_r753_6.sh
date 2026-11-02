#!/bin/sh
# Round R753-6 sweeps for #797: the exact head, four RTL mutants, the round 4
# page wording planted back, and m4 against the parent (ef7dc985) sweep script.
# Usage: run_r753_6.sh <clone at 2c500d0a> <dir holding m1 m2 m4 m5 .rtl.diff and round4_wording.page.diff> <out> <scratch>
# Needs Verilator 5.050 first on PATH and a C++ compiler. Runs two sweeps at a
# time (each builds with -j 8). Writes sweep_<name>.log and .rc under <out>.
set -u
C=$1; Q=$2; O=$3; S=$4
mkdir -p "$O" "$S"
verilator --version > "$O/verilator_version.txt"
for n in head m1 m2 m4 m5; do
  mkdir -p "$S/$n"
  git -C "$C" archive HEAD hdl/common/csr configs/generated scripts docs/reference | tar -x -C "$S/$n"
  [ "$n" = head ] || (cd "$S/$n" && patch -p1 -s < "$Q/$n.rtl.diff")
done
cp "$S/head/docs/reference/REGISTER_MAP.md" "$S/page_round4.md"
(cd "$S" && patch -s page_round4.md < "$Q/round4_wording.page.diff")
mkdir -p "$S/m4parent"
git -C "$C" archive ef7dc985 scripts/register_read_sweep.py | tar -x -C "$S/m4parent"
cp -r "$S/m4/hdl" "$S/m4/configs" "$S/m4/docs" "$S/m4parent/"
one() {
  n=$1
  case $n in
    head)     set -- "$S/head/scripts/register_read_sweep.py" ;;
    round4)   set -- "$S/head/scripts/register_read_sweep.py" --page "$S/page_round4.md" ;;
    m4parent) set -- "$S/m4parent/scripts/register_read_sweep.py" ;;
    *)        set -- "$S/$n/scripts/register_read_sweep.py" ;;
  esac
  python3 -I -B "$@" --work "$S/w/$n" > "$O/sweep_$n.log" 2>&1
  echo $? > "$O/sweep_$n.rc"
}
for pair in "head m4" "m1 m2" "m5 round4" "m4parent"; do
  for n in $pair; do one "$n" & done
  wait
done
for n in head m4 m1 m2 m5 round4 m4parent; do echo "sweep_$n rc=$(cat "$O/sweep_$n.rc") $(tail -1 "$O/sweep_$n.log")"; done
