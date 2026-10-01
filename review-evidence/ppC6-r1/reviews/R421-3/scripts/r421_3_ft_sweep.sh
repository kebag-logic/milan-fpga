#!/bin/sh
# R421-3: sweep the departure phase of tb/aecp_notify section FT (full
# timebase, 100,000 clocks per ms) and record the lower-bound margins.
# Usage: r421_3_ft_sweep.sh TREE VERILATOR OUT   (TREE: a scratch export)
set -e
T=$1; V=$2; OUT=$3
cd "$T/tb/aecp_notify"
python3 - <<'PY'
from pathlib import Path
p = Path("sim_main.cpp"); t = p.read_text()
for i, ph in ((1, "END"), (2, "START"), (3, "END"), (4, "END")):
    old = f"  const Frame f{i} = frame({ph});\n"
    assert t.count(old) == 1, old
    t = t.replace(old, f'  const Frame f{i} = frame(getenv("R421_PH{i}") ? strtoull(getenv("R421_PH{i}"), nullptr, 0) : {ph});\n')
t = "#include <cstdlib>\n" + t
p.write_text(t)
PY
make identify-build VERILATOR="$V" > "$OUT.build.log" 2>&1
: > "$OUT"
for ph in 0 1 2 3 50000 99996 99997 99998 99999; do
  R421_PH1=$ph R421_PH2=$ph R421_PH3=$ph R421_PH4=$ph ./obj_idn/Vaecp_notify_idn > "$OUT.ph$ph.log" 2>&1 || true
  g12=$(sed -n 's/.*frame 2 presented \([0-9]*\) clocks later.*/\1/p' "$OUT.ph$ph.log")
  g23=$(sed -n 's/.*frame 3 presented \([0-9]*\) clocks later.*/\1/p' "$OUT.ph$ph.log")
  t14=$(sed -n 's/.*next burst presented \([0-9]*\) clocks after.*/\1/p' "$OUT.ph$ph.log")
  ok=PASS
  [ "$g12" -ge 15000000 ] && [ "$g23" -ge 15000000 ] && [ "$t14" -ge 100000000 ] || ok=FAIL
  echo "phase $ph: depart->next-present g12=$g12 g23=$g23 first->rearm t14=$t14 lower-bounds $ok" >> "$OUT"
done
cat "$OUT"
