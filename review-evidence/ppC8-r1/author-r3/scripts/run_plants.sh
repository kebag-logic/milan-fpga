#!/bin/bash
# usage: run_plants.sh <commit> <label>; exports the commit and runs every
# reviewer plant script, unchanged, from the read-only packets.
set -u
commit=$1; label=$2
base=$VALIDATION_STORAGE/c8-a501/campaign/$label
rm -rf "$base"; mkdir -p "$base/tree" "$base/work434" "$base/work435" "$base/work434t" "$base/work434r1"
if [ "$commit" = WORKTREE ]; then
  (cd $LANES/ppC8-desc-lint && git ls-files -z --cached --others --exclude-standard | tar --null -T - -cf -) | tar -x -C "$base/tree"
else
  git -C $LANES/ppC8-desc-lint archive "$commit" | tar -x -C "$base/tree"
fi
P434=$REVIEWS/ppC8-r434-2-packet/scripts
P435=$REVIEWS/ppC8-r435-2-packet/scripts
names434=$(python3 -c "import importlib.util,sys;s=importlib.util.spec_from_file_location('p','$P434/r2/plant_r2.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(' '.join(m.PLANTS))")
namesr1=$(python3 - <<PY
import re
t=open('$P434/r1/plant.py').read()
body=t.split('PLANTS = {')[1].split('\n}\n')[0]
print(' '.join(re.findall(r'^ "([^"]+)":', body, re.M)))
PY
)
namest="T-cap45 T-rates7 T-crf-ge1 T-aaf-ge1 T-waiver-anytype T-waiver-anycfg T-entity-cfg T-iface-subset"
( printf '%s\n' $names434 | xargs -P 12 -I{} python3 -B $P434/r2/plant_r2.py "$base/tree" "$base/work434" {} ) > "$base/r434_plant_r2.txt" 2>&1
( printf '%s\n' $namest | xargs -P 8 -I{} python3 -B $P434/r2/plant_r435_titles.py "$base/tree" "$base/work434t" {} ) > "$base/r434_plant_r435_titles.txt" 2>&1
( printf '%s\n' $namesr1 | xargs -P 12 -I{} python3 -B $P434/r1/plant.py "$base/tree" "$base/work434r1" {} ) > "$base/r434_r1_plant.txt" 2>&1
python3 -B $P435/r2_plants.py "$base/tree" "$base/work435" --jobs 12 > "$base/r435_r2_plants.txt" 2>&1
echo "r435 rc=$?" >> "$base/r435_r2_plants.txt"
for f in r434_plant_r2 r434_plant_r435_titles r434_r1_plant; do
  echo "$f: $(grep -c ' KILLED' $base/$f.txt) KILLED, $(grep -c ' SURVIVED' $base/$f.txt) SURVIVED, $(grep -c ' BADPLANT' $base/$f.txt) BADPLANT of $(wc -l < $base/$f.txt)"
done > "$base/summary.txt"
tail -2 "$base/r435_r2_plants.txt" >> "$base/summary.txt"
rm -rf "$base/work434" "$base/work435" "$base/work434t" "$base/work434r1"
echo done
