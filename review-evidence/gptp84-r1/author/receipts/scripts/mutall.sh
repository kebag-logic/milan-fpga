#!/bin/sh
# usage: mutall.sh <tree> <logdir> <nslices> <first> <last>
# (runs slices first..last inclusive of an <nslices> split)
# Runs the tree's whole engine mutation arm as <nslices> parallel slices of
# mutslice.py, one log each, then prints every slice's rc and tally.
tree=$1; logdir=$2; n=$3; first=$4; last=$5
export PATH=<pinned-tools>:$PATH
export TMPDIR=<scratch>/tmpdir
mkdir -p "$logdir"
total=$(cd "$tree/tb/verilator/engine" && python3 -c 'import mutants; print(len(mutants.MUTATIONS))')
per=$(( (total + n - 1) / n ))
i=$first
start=$(date +%s)
while [ $i -le $last ]; do
  s=$(( i * per )); e=$(( s + per ))
  ( cd "$tree/tb/verilator/engine" && python3 <scratch>/scripts/mutslice.py "$tree" $s $e > "$logdir/mut-$i.log" 2>&1; echo "slice $i [$s:$e] rc=$?" > "$logdir/mut-$i.rc" ) &
  i=$((i + 1))
done
wait
end=$(date +%s)
echo "mutations listed: $total, slices: $n, secs: $((end - start))" > "$logdir/mut-summary.txt"
for f in "$logdir"/mut-*.rc; do cat "$f" >> "$logdir/mut-summary.txt"; done
grep -h "checks:" "$logdir"/mut-*.log >> "$logdir/mut-summary.txt"
grep -h "^\[FAIL\]" "$logdir"/mut-*.log >> "$logdir/mut-summary.txt"
cat "$logdir/mut-summary.txt"
