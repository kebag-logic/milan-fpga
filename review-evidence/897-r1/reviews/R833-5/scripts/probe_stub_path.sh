#!/usr/bin/env bash
# Plant: the answering-ports arm's path port reverted to the stub that answers an empty sequence at once (the port
# before arm_path.py). Run the harness self-test and the record classes' own controls on the planted tree, record
# whether anything refuses it, then restore the exact head bytes.
# usage: probe_stub_path.sh CLONE OUTDIR
set -u
clone=$1; out=$2
mkdir -p "$out"
f="$clone/tb/verilator/ctrl_service_budget/build.py"
cp "$f" "$out/build.py.orig"
python3 -I - "$f" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
old = "         + arm_path.B_PATH +\n"
new = ("         'static bool b_path(void *ctx, unsigned i, uint16_t n, uint64_t *v, size_t cap, size_t *count)\\n'\n"
       "         '{ (void)ctx; (void)i; (void)n; (void)v; (void)cap; *count = 0; return true; }\\n'\n")
assert s.count(old) == 1
open(p, 'w').write(s.replace(old, new))
EOF
cd "$clone/tb/verilator/ctrl_service_budget" || exit 2
python3 -B run.py --self-test > "$out/stub-path-selftest.log" 2>&1; echo $? > "$out/stub-path-selftest.rc"
python3 -I record_classes.py --selftest > "$out/stub-path-record-classes.log" 2>&1; echo $? > "$out/stub-path-record-classes.rc"
cp "$out/build.py.orig" "$f"
cd "$clone" && git diff --quiet -- tb/verilator/ctrl_service_budget/build.py && echo "restored" > "$out/stub-path-restored.txt"
echo "self-test rc $(cat "$out/stub-path-selftest.rc"); record_classes rc $(cat "$out/stub-path-record-classes.rc"); $(cat "$out/stub-path-restored.txt" 2>/dev/null || echo NOT-RESTORED)"
