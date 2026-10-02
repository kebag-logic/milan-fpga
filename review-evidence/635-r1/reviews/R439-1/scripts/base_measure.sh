#!/bin/bash
# Measure the naming and port-contract ratchets at the base (parent cdf49d1a,
# processor b2db3a97) inside the clone, then restore the exact head and pin.
# Usage: base_measure.sh <clone> <outdir>
set -u
C=$1; O=$2; cd "$C"
git checkout -q cdf49d1a28527562888f0a903de51b6b15b1244f
git -C protocol-processor checkout -q b2db3a970cedbbff2f8ba813acb96122c442bc58
python3 scripts/measure_naming.py --check > "$O/base_naming.log" 2>&1; echo rc=$? >> "$O/base_naming.log"
python3 scripts/check_port_contracts.py > "$O/base_port.log" 2>&1; echo rc=$? >> "$O/base_port.log"
python3 scripts/check_port_contracts.py --write-budget > /dev/null 2>&1; cp scripts/port_docs.budget "$O/base_port_docs.budget.regen"
python3 scripts/measure_naming.py --write-budget > /dev/null 2>&1; cp scripts/naming.budget "$O/base_naming.budget.regen"
git checkout -q -- scripts/port_docs.budget scripts/naming.budget
git checkout -q 3370c6cbd5e4b096167c19ca709556a40207e538
git -C protocol-processor checkout -q 631eeb342ca1e3fa80e734077a56a943aee76ff1
