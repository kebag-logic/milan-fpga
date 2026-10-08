#!/usr/bin/env bash
# Lane A: notify campaign arms graded by tb/aecp_notify and the withdraw arms,
# at the exported head tree. Args: TREE OUTDIR LOG
set -uo pipefail
TREE=$1; OUT=$2
cd "$TREE" || exit 2
ARMS=$(python3 -I - "$TREE" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location('nm', sys.argv[1] + '/tb/pp_top/notify_mutants.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(' '.join(mu.name for mu in m.MUTANTS
               if mu.suite.directory == 'tb/aecp_notify' or '--withdraw-only' in mu.suite.run))
PY
)
echo "arms: $ARMS"
python3 tb/pp_top/notify_mutants.py --output "$OUT" --verilator verilator --jobs 1 --only $ARMS
