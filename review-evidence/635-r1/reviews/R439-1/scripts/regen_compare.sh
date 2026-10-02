#!/bin/bash
# Re-run each pin-derived record's generator in write mode at the head, compare
# with the committed bytes, and restore. Usage: regen_compare.sh <clone> <outdir> <pinned-verilator-dir>
set -u
C=$1; O=$2; V=$3; export PATH="$V:$PATH"; mkdir -p "$O"; cd "$C"
( cd syn/yosys && OOC_TMP="$O/ooc_tmp" ./ooc.sh --record-rom-digests ) > "$O/rom_record.log" 2>&1; echo "rom_record rc=$?" > "$O/rom_record.rc"
git diff --exit-code --stat syn/yosys/rom_digests.tsv > "$O/rom_record.diff" 2>&1; echo "rom diff rc=$?" >> "$O/rom_record.rc"
python3 docs/diagrams/submodule_boundaries.gen.py > "$O/boundary_write.log" 2>&1; echo "boundary_write rc=$?" > "$O/boundary.rc"
git status --porcelain docs/diagrams > "$O/boundary.status"; echo "boundary dirty lines=$(wc -l < "$O/boundary.status")" >> "$O/boundary.rc"
python3 scripts/check_port_contracts.py --write-budget > "$O/port_write.log" 2>&1; echo "port_write rc=$?" > "$O/port.rc"
git diff --exit-code scripts/port_docs.budget > "$O/port.diff" 2>&1; echo "port diff rc=$?" >> "$O/port.rc"
python3 scripts/measure_naming.py --write-budget > "$O/naming_write.log" 2>&1; echo "naming_write rc=$?" > "$O/naming.rc"
git diff --exit-code scripts/naming.budget > "$O/naming.diff" 2>&1; echo "naming diff rc=$?" >> "$O/naming.rc"
git checkout -q -- syn/yosys/rom_digests.tsv docs/diagrams scripts/port_docs.budget scripts/naming.budget
