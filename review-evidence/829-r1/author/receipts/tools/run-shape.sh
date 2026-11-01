#!/usr/bin/env bash
# run-shape.sh <tree> <tag> [shape]: build one tracked Arty configuration inside a Vivado slot, from <tree>.
# Clears the entity gate with --write-rtl, takes the launch line build.sh prints, restores moved tracked files
# by name unless the tree is the scratch probe, then runs that line in the foreground so the exit status reaches a file.
set -u
tree=$1 tag=$2 shape=${3:-current}
scratch=$VALIDATION_STORAGE/829-a725b
cfg=configs/endstation_arty_$shape.yaml
rcfile=$scratch/rc/$tag.rc
mkdir -p $scratch/rc $scratch/logs
finish() { echo "$1" > "$rcfile"; echo "== END-OF-RUN tag=$tag rc=$1 $(date -Iseconds) $2"; exit "$1"; }
cd "$tree" || finish 3 "no tree"
echo "== START shape=$shape tag=$tag head=$(git rev-parse HEAD) $(date -Iseconds)"
git status --short > "$scratch/logs/before-$tag.txt"
python3 sw/builder/endstation_builder.py "$cfg" --write-rtl > "$scratch/logs/writertl-$tag.log" 2>&1 || finish 5 "write-rtl failed"
git status --short > "$scratch/logs/after-$tag.txt"
comm -13 <(sort "$scratch/logs/before-$tag.txt") <(sort "$scratch/logs/after-$tag.txt") | awk '{print $2}' > "$scratch/logs/moved-$tag.txt"
python3 scripts/check_entity_shape.py --built-config "$tree/$cfg" > "$scratch/logs/gate-$tag.log" 2>&1
gate=$?
echo "== entity gate rc=$gate; moved: $(tr '\n' ' ' < "$scratch/logs/moved-$tag.txt")"
(cd sw/litex && BUILD_CFG=$cfg TAG=$tag ./build.sh arty --dry-run) > "$scratch/logs/dry-$tag.log" 2>&1
dry=$?
xargs -r git checkout -- < "$scratch/logs/moved-$tag.txt"
[ "$gate" = 0 ] && [ "$dry" = 0 ] || finish 7 "gate=$gate dry=$dry"
grep -q REFUSED "$scratch/logs/dry-$tag.log" && finish 8 "dry run previews a refusal"
line=$(sed -n 's/^ *\(cd .* exec python3 milan_soc\.py .*\)$/\1/p' "$scratch/logs/dry-$tag.log")
[ -n "$line" ] || finish 9 "no launch line"
printf '%s\n' "$line" > "$scratch/logs/line-$tag.txt"
echo "== launch line: $line"
bash -c "$line"
finish $? "milan_soc.py exited"
