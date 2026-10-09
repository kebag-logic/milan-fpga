#!/bin/sh
# Failure paths of the second L11b fence, reusing the extraction made by
# probe_l11b_commands.sh in <outdir>: (a) the stub vivado fails for vexmin,
# expecting the loop to stop with that rc, record vexmin.rc and skip pico;
# (b) WORK is not fresh, expecting mkdir to fail before any vivado call.
# Usage: probe_l11b_failure_paths.sh <outdir-of-probe_l11b_commands>
set -u
out=$1
f=$out/fail; rm -rf "$f"; mkdir -p "$f/bin" "$f/work"
for t in bash flock cat mkdir; do ln -s "$(command -v "$t")" "$f/bin/$t"; done
cat > "$f/bin/vivado" <<'STUB'
#!/bin/bash
core=; while [ $# -gt 0 ]; do [ "$1" = -tclargs ] && core=$2; shift; done
echo "$core" >> "$WORK/called.txt"
[ "$core" = vexmin ] && exit 3
exit 0
STUB
chmod +x "$f/bin/vivado"
cp "$out/work/price_core.tcl" "$f/work/"
rc=0; env -i PATH="$f/bin" WORK="$f/work" /bin/sh "$out/block2.sh" >/dev/null 2>&1 || rc=$?
echo "(a) failing vexmin: fence rc=$rc called=$(tr '\n' ' ' < "$f/work/called.txt") vexmin.rc=$(cat "$f/work/vexmin/vexmin.rc") pico_dir=$([ -e "$f/work/pico" ] && echo present || echo absent)"
rm -f "$f/work/called.txt"
rc=0; env -i PATH="$f/bin" WORK="$f/work" /bin/sh "$out/block2.sh" >/dev/null 2>&1 || rc=$?
echo "(b) non-fresh WORK (vexii exists): fence rc=$rc vivado_calls=$( [ -e "$f/work/called.txt" ] && wc -l < "$f/work/called.txt" || echo 0)"
