#!/bin/bash
# Copy a measurement leg's receipts (driver log without its COMMAND lines, the results table, the build's identity,
# each group log's size and SHA-256) and its costs into the output directory. usage: collect_leg.sh NAME
set -u
N=$1 T=<scratch> O=<management>/2026-09-23/665s2b-a683ze/receipts/measure
san() { sed "s#<scratch>#<scratch>#g; s#<scratch24>#<scratch24>#g; s#<lane>#<lane>#g; s#<tools>#<tools>#g; s#<management>#<management>#g; s#<home>#<home>#g; s#<data>#<data>#g"; }
put() { local s=$1 d=$2; mkdir -p "$(dirname "$d")"
    if [ "$(stat -c %s "$s")" -lt 150000 ]; then san < "$s" > "$d"
    else { echo "# the last 300 lines of $(basename "$s"): $(stat -c %s "$s") bytes, sha256 $(sha256sum "$s" | cut -c1-64)"; tail -300 "$s" | cut -c1-600 | san; } > "$d.tail"; fi; }
L=$O/legs/$N; mkdir -p $L
grep -v "^COMMAND" $T/logs/$N.log > /tmp/a683ze-leg.log; put /tmp/a683ze-leg.log $L/driver.log; rm -f /tmp/a683ze-leg.log
[ -f $T/builds/$N/results/table.md ] && put $T/builds/$N/results/table.md $L/table.md
python3 -c "
import json; b=json.load(open('$T/builds/$N/build.json'))
print(json.dumps({k: b.get(k) for k in ('shape', 'interfaces', 'variant', 'mutation', 'fetch_l1', 'sys_hz', 'cpu_hz', 'commit', 'head', 'tree')}, indent=1))" > $L/build-summary.json
(cd $T/builds/$N/results && sha256sum *.log > $L/logs.sha256 && stat -c "%n %s" *.log > $L/logs.sizes)
python3 - "$T/builds/$N" "$L/image.txt" <<'PY'
import json, sys
from pathlib import Path
b = Path(sys.argv[1])
def find(o):
    if isinstance(o, dict):
        if 'rom' in o and isinstance(o['rom'], dict): return o['rom']
        for v in o.values():
            r = find(v)
            if r: return r
rom = find(json.loads((b / 'image/size.json').read_text()))
import hashlib, subprocess
elf = b / 'image/ctrl_app.elf'
subprocess.run(['<home>/br-milan-rv32/host/bin/riscv32-buildroot-linux-gnu-objcopy', '-O', 'binary', str(elf), '/tmp/a683ze-img.bin'], check=True)
data = Path('/tmp/a683ze-img.bin').read_bytes()
Path(sys.argv[2]).write_text(f"rom {rom['bytes']} bytes; image (objcopy -O binary) {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}\n")
PY
C=$O/costs/$N; mkdir -p $C
for f in $T/costs/$N/*; do put $f $C/$(basename $f); done
echo "collected $N"
