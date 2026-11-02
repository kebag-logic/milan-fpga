#!/bin/sh
# Falsification probes for the round-4 delta. All trees and pages are under PACKET/scratch.
# Usage: run_probes.sh CLONE PACKET PYTHON
set -u
C=$1; P=$2; PY=$3
S=$P/scratch; R=$P/receipts/probes; mkdir -p "$S" "$R"
export PATH="$P/bin:$PATH"
cd "$C" || exit 2
PAGE=docs/reference/REGISTER_MAP.md
RTL=hdl/common/csr/milan_csr.sv

# Pages swept by the head's sweep.
git show e90284bd:$PAGE > "$S/page_e90284bd.md"
"$PY" - "$PAGE" "$S/page_plant_rows.md" "$S/page_plant_clause.md" <<'EOF'
import sys
src, rows_out, clause_out = sys.argv[1:]
t = open(src, encoding="utf-8").read()
fresh = " and the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write"
plants = [
    # A: STRMW_SRP's STRM_SEL[9] row without its freshness clause.
    ("| the selected stream exists and `STRM_SEL[9]` is 1" + fresh + " |",
     "| the selected stream exists and `STRM_SEL[9]` is 1 |"),
    # B: RENDER_STAT's previous, shipping-only row.
    ("| the selected stream exists and `STRM_SEL[8]` selects a listener | the fields above |\n| any other case | `0x00000000` |\n\n## 0x8E0",
     "| `STRM_SEL[8]` selects a listener and the stream index `STRM_SEL[3:0]` is 0 | the fields above |\n| any other case | `0x00000000` |\n\n## 0x8E0"),
    # C: CHMAP_LOOP's two values swapped.
    ("| `CHMAP_SNAP[1]` is 1 | the fields above |\n| `CHMAP_SNAP[1]` is 0 | `0xDEADDEAD` |",
     "| `CHMAP_SNAP[1]` is 1 | `0xDEADDEAD` |\n| `CHMAP_SNAP[1]` is 0 | the fields above |"),
]
r = t
for old, new in plants:
    assert r.count(old) == 1, old
    r = r.replace(old, new)
open(rows_out, "w", encoding="utf-8").write(r)
# D: a clause the sweep has no reading of (the previous SRP wording).
old = "the SRP table answered a poll since the last `STRM_SEL`/`STRMW_CTRL` write | `i_srp_ctx_rd_sid[31:0]`"
assert t.count(old) == 1
open(clause_out, "w", encoding="utf-8").write(t.replace(old, "the SRP table answered since the last selection | `i_srp_ctx_rd_sid[31:0]`"))
EOF

# Generator mutants of the RENDER_STAT selection loop, each in its own tree copy.
mk() { rm -rf "$S/$1"; rsync -a --exclude=.git "$C/" "$S/$1/"; }
mk gen_step2; mk gen_le
sed -i 's/for (int unsigned s = 0; s < N_LISTENERS_P; s++) begin/for (int unsigned s = 0; s < N_LISTENERS_P; s += 2) begin/' "$S/gen_step2/$RTL"
sed -i 's/for (int unsigned s = 0; s < N_LISTENERS_P; s++) begin/for (int unsigned s = 0; s <= N_LISTENERS_P; s++) begin/' "$S/gen_le/$RTL"
diff "$C/$RTL" "$S/gen_step2/$RTL" > "$R/gen_step2.rtl.diff"
diff "$C/$RTL" "$S/gen_le/$RTL" > "$R/gen_le.rtl.diff"

run() { name=$1; shift; "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc"; }
gen() { name=$1; cd "$S/$name" && "$PY" scripts/gen_register_reference.py --write > "$R/$name.write.log" 2>&1;
        echo $? > "$R/$name.write.rc"; diff "$C/$PAGE" "$S/$name/$PAGE" > "$R/$name.page.diff"; echo $? > "$R/$name.page.diff.rc"; }
run sweep_e90284bd "$PY" scripts/register_read_sweep.py --page "$S/page_e90284bd.md" --work "$S/w_old" &
run sweep_plant_rows "$PY" scripts/register_read_sweep.py --page "$S/page_plant_rows.md" --work "$S/w_rows" &
run sweep_plant_clause "$PY" scripts/register_read_sweep.py --page "$S/page_plant_clause.md" --work "$S/w_clause" &
gen gen_step2 &
gen gen_le &
wait
cd "$C"
# The step-2 mutant at 2x2, swept against the head page: the RTL change the generator left unprinted.
run sweep_step2_rtl "$PY" "$S/gen_step2/scripts/register_read_sweep.py" --page "$C/$PAGE" --work "$S/w_step2"
for f in "$R"/*.rc; do echo "$(basename "$f" .rc) rc=$(cat "$f")"; done
