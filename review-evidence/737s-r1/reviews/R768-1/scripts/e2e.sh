#!/usr/bin/env bash
# End-to-end LiteX leg probe in a disposable clone whose sw/litex members are stub passers.
# usage: e2e.sh <clone> <outdir>
# Runs the three legs through scripts/ci_litex_legs.py run (the generated step's command),
# then the union CLI and the elaborate aggregate verifier CLI; writes rc and stderr of each.
set -u
C="$1"; O="$2"; H="$(cd "$(dirname "$0")" && pwd)"; rm -rf "$O"; mkdir -p "$O/legs"
cd "$C" || exit 2
export MILAN_LITEX_PYTHON="$O/py"
printf '#!/bin/sh\nif [ "$1" = "-c" ] && [ "$2" = "import migen, litex" ]; then exit 0; fi\nexec python3 "$@"\n' > "$MILAN_LITEX_PYTHON"
chmod +x "$MILAN_LITEX_PYTHON"
for leg in 0 1 2; do
  python3 scripts/ci_litex_legs.py run $leg --receipt "$O/legs/litex-leg-$leg.json" -- \
    scripts/run_litex_sims.sh "$O/logs-$leg" > "$O/leg-$leg.out" 2>&1; echo $? > "$O/leg-$leg.rc"
done
python3 scripts/ci_litex_legs.py union --head "$(git rev-parse HEAD)" --tree "$(git rev-parse 'HEAD^{tree}')" \
  "$O"/legs/litex-leg-*.json > "$O/union.out" 2>&1; echo $? > "$O/union.rc"
needs="$(python3 "$H/mk_gate_root.py" "$C" "$O/legs" "$O/root" 2>"$O/mkroot.err")"
CI_GATE_NEEDS="$needs" python3 scripts/ci_gate_receipts.py verify --workflow elaborate --root "$O/root" \
  --head "$(git rev-parse HEAD)" --output "$O/gate-union.json" > "$O/verify.out" 2>&1; echo $? > "$O/verify.rc"
printf 'legs rc %s %s %s | union rc %s: %s | verify rc %s: %s\n' "$(cat "$O/leg-0.rc")" "$(cat "$O/leg-1.rc")" \
  "$(cat "$O/leg-2.rc")" "$(cat "$O/union.rc")" "$(tail -n1 "$O/union.out")" "$(cat "$O/verify.rc")" "$(grep -m1 "refused\|exactly once" "$O/verify.out" || tail -n1 "$O/verify.out")"
