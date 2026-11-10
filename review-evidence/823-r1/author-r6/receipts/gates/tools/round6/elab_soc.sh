#!/usr/bin/env bash
# elab_soc.sh <commit> <board config name for build.sh> <out dir>: elaborate one shipping SoC with no vendor run
# (milan_soc.py without --build) on a fresh clean clone of <commit>, then list every generated gateware file with
# its sha256. The launch line is build.sh's own (--dry-run), with the vendor settings, --build and the output
# directory replaced.
set -u
C=$1; B=$2; O=$3
L=<lane>
W=$O/wt
mkdir -p "$O"
git clone -q --shared --no-checkout "$L" "$W" && git -C "$W" fetch -q "$L" "$C" && git -C "$W" -c advice.detachedHead=false checkout -q --detach "$C" || exit 3
for dep in $(git -C "$W" config --blob "$C:.gitmodules" --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  if [ -e "$L/$dep/.git" ] && [ "$dep" != external ]; then
    git -C "$W" config "submodule.$dep.url" "$L/$dep"
    git -C "$W" -c protocol.file.allow=always submodule update -q --init --force "$dep" || exit 4
  fi
done
test -z "$(git -C "$W" status --porcelain)" || exit 5
export PATH=<litex-env>/venv/bin:/usr/local/bin:/usr/bin:/bin PYTHONHASHSEED=0 TMPDIR=$O/tmp
mkdir -p "$TMPDIR"
cd "$W" || exit 6
bash sw/litex/build.sh "$B" --dry-run > "$O/dry-run.log" 2>&1 || exit 7
line=$(grep 'exec python3 milan_soc.py' "$O/dry-run.log" | sed 's/.*exec python3 milan_soc.py //')
args=$(echo "$line" | sed 's/ --build / /; s/ --build$//; s/ --output-dir [^ ]*//')
echo "milan_soc.py $args --output-dir $O/build" > "$O/argv.txt"
cd sw/litex && python3 milan_soc.py $args --output-dir "$O/build" > "$O/elab.log" 2>&1
rc=$?; echo "$rc" > "$O/elab.rc"
cd "$O/build" 2>/dev/null && find gateware -type f | sort | while read -r f; do echo "$(sha256sum "$f" | cut -c1-64)  $(stat -c %s "$f")  $f"; done > "$O/gateware.sha256"
git -C "$W" status --porcelain > "$O/tree-after.txt"
echo "elab $C $B rc=$rc"
