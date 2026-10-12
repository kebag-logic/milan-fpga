#!/bin/sh
# usage: run_mutant.sh PACKET GITLABEL(256|243) MUTANT  -- copy the base tree, apply MUTANT, run the pin controls.
P=$1; G=$2; M=$3; S=$P/scratch; D=$S/mut/$G-$M
rm -rf "$D" && mkdir -p "$S/mut" && cp -a "$S/tree" "$D" || exit 9
python3 -I "$P/scripts/mutate.py" "$D" "$M" > "$S/mut/$G-$M.log" 2>&1 || { echo 8 > "$S/mut/$G-$M.rc"; exit 0; }
if [ "$G" = 243 ]; then PATH=$S/git243/prefix/bin:$PATH; export PATH; fi
cd "$D" && timeout 1200 python3 -B "$P/scripts/run_pin_controls.py" "$D" "$S/mut/work-$G-$M" >> "$S/mut/$G-$M.log" 2>&1
echo $? > "$S/mut/$G-$M.rc"
rm -rf "$D" "$S/mut/work-$G-$M"
