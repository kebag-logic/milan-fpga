#!/bin/sh
# Extract the two fenced sh blocks under "### Reproduce L11b core pricing" from
# a given revision of docs/design/MARK_II_AREA_PLAN.md and run them in a plain
# POSIX shell whose PATH holds only bash, flock, cat, mkdir and a stub vivado.
# Usage: probe_l11b_commands.sh <repo> <rev> <outdir>
# Probe substitution: the host lock path $VIVADO_LOCK is replaced by
# a lock inside <outdir> so the probe never waits on a real Vivado run.
set -eu
repo=$1 rev=$2 out=$3
rm -rf "$out"; mkdir -p "$out/bin" "$out/work"
git -C "$repo" show "$rev:docs/design/MARK_II_AREA_PLAN.md" > "$out/page.md"
awk -v dir="$out" '
  /^### Reproduce L11b core pricing$/ {sec=1; next}
  sec && /^### / {sec=0}
  sec && /^```sh$/ {n++; f=dir "/block" n ".sh"; inb=1; next}
  inb && /^```$/ {inb=0; close(f); next}
  inb {print > f}
' "$out/page.md"
for b in "$out"/block1.sh "$out"/block2.sh; do test -s "$b"; done
sed -i "s#$VIVADO_LOCK#$out/probe.lock#" "$out/block2.sh"
for t in bash flock cat mkdir; do ln -s "$(command -v "$t")" "$out/bin/$t"; done
cat > "$out/bin/vivado" <<'STUB'
#!/bin/bash
# Stub: records its argv, checks the Tcl exists, writes the -log file.
set -eu
printf '%s\n' "$*" >> "$WORK/vivado_argv.txt"
log= src= core=
while [ $# -gt 0 ]; do case $1 in -log) log=$2; shift;; -source) src=$2; shift;; -tclargs) core=$2; shift;; esac; shift; done
test -s "$src"
echo "stub PRICED $core" > "$log"
STUB
chmod +x "$out/bin/vivado"
rc1=0 rc2=0
env -i PATH="$out/bin" WORK="$out/work" CPU_VEXII_DIR=/x CPU_VEXMIN_DIR=/x CPU_PICO_DIR=/x \
  /bin/sh "$out/block1.sh" > "$out/block1.out" 2>&1 || rc1=$?
env -i PATH="$out/bin" WORK="$out/work" CPU_VEXII_DIR=/x CPU_VEXMIN_DIR=/x CPU_PICO_DIR=/x \
  /bin/sh "$out/block2.sh" > "$out/block2.out" 2>&1 || rc2=$?
echo "rev=$rev block1_rc=$rc1 block2_rc=$rc2"
echo "--- block1 stderr/stdout"; cat "$out/block1.out"
echo "--- block2 stderr/stdout"; cat "$out/block2.out"
if [ -s "$out/work/price_core.tcl" ]; then
  echo "tcl_sha256=$(sha256sum < "$out/work/price_core.tcl" | cut -c1-64) lines=$(wc -l < "$out/work/price_core.tcl")"
else echo "tcl=absent"; fi
for c in vexii vexmin pico; do
  printf '%s rc=%s log=%s\n' "$c" "$(cat "$out/work/$c/$c.rc" 2>/dev/null || echo none)" "$(cat "$out/work/$c/$c.log" 2>/dev/null || echo none)"
done
echo "--- vivado argv"; cat "$out/work/vivado_argv.txt" 2>/dev/null || echo none
