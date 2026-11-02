#!/bin/sh
# Usage: probe_mutants_all_listings.sh <clone> <packet> NAME...
# Builds each named MUTANTS entry with the clone's own mutant_tree and runs probe_all_listings.py on it.
clone=$1; packet=$2; shift 2
mkdir -p "$packet/scratch/mt"
for name in "$@"; do
  rm -rf "$packet/scratch/mt/$name"
  python3 -I -B -c "import sys; sys.path.insert(0, sys.argv[1] + '/scripts'); from pathlib import Path; \
import process_test_support as s; s.mutant_tree(Path(sys.argv[2]), sys.argv[3])" "$clone" "$packet/scratch/mt" "$name"
  echo "=== $name"
  (cd "$packet/scratch" && timeout 300 python3 -I -B "$packet/probe_all_listings.py" "$packet/scratch/mt/$name" 2>&1 \
     | grep -E '^(RED|listings|Traceback|[A-Za-z]*Error)' )
done
