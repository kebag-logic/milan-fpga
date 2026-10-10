#!/bin/sh
# N9 diagnostic: split N9's combined name check into its parts (store entries
# via the lane tap, GET_NAME, restore outcome) for the head and for the
# debt-hold-dropped defect, at the 1x1 bound capacity (39), case "debt".
# Only a scratch copy of sim_main.cpp gains printf lines; no assertion changes.
set -u; . "$(dirname "$0")/env.sh"
for arm in golden mutant; do
  t="$SCRATCH/debtdiag-$arm"; extract "$t/src"
  python3 - "$t/src" "$arm" <<'PY'
import sys, pathlib
root, arm = pathlib.Path(sys.argv[1]), sys.argv[2]
sim = root / "tb/name_state/sim_main.cpp"
s = sim.read_text()
old = "    CHECK(entries && gets,\n"
new = ("    { unsigned bad_e=0,bad_g=0; for (const auto& n : named) {"
       " bad_e += table_entry(n.ordinal)!=defaults[n.ordinal]; }\n"
       "      for (const auto& n : named) bad_g += !get_reads(n, defaults[n.ordinal]);\n"
       "      printf(\"DIAG N9 entries_not_default=%u gets_not_default=%u of %zu; done=%ld closed=%ld rb=%u cause=%u owed=%ld\\n\","
       " bad_e, bad_g, named.size(), b.done, b.closed, unsigned(x.d->restore_rb_o), unsigned(x.d->rs_cause_o), owed); }\n"
       + old)
assert s.count(old) == 1; sim.write_text(s.replace(old, new))
if arm == "mutant":
    w = root / "hdl/aecp/KL_aecp_nvm_writer.sv"; t = w.read_text()
    a = "          if (rb_min_r && !desc_debt_i) ws_r <= W_RELOC;"
    assert t.count(a) == 1; w.write_text(t.replace(a, "          if (rb_min_r) ws_r <= W_RELOC;"))
PY
  mkdir -p "$t/work"
  python3 - "$t/src" "$t/work" "$VERILATOR" > "$t/debtdiag.log" 2>&1 <<'PY'
import sys, pathlib, subprocess
root, work, v = map(pathlib.Path, sys.argv[1:4])
sys.path.insert(0, str(root / "tb/name_state"))
from run import build, capacity
from fixture import fixture, packer
binary = build(root, work, str(v), capacity(39))
img = work / "names-1.bin"; img.write_bytes(packer(root).build(fixture(1), lint=False)[0])
r = subprocess.run([str(binary), str(img), "1", "debt"], cwd=work, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print(r.stdout, end=""); print(f"rc={r.returncode}")
PY
  grep -E '^(DIAG|FAIL|[0-9]+ checks|rc=)' "$t/debtdiag.log" > "$RCPT/debtdiag-$arm.txt"
done
