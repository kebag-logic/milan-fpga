#!/usr/bin/env bash
# Disposable mutation probes for the R636-3 delta. Usage: mutants.sh <exact-head clone> <scratch dir> <receipt dir>
# Each mutant runs in its own copy; the clone is never written.
set -u
src=$1; scratch=$2; out=$3
old=43a25fa7
mkdir -p "$scratch" "$out"
copy() { rm -rf "$scratch/$1"; cp -a "$src" "$scratch/$1"; }
run_bm() { (cd "$scratch/$1" && python3 scripts/check_baremetal_only.py --selftest > "$out/$1.log" 2>&1; echo $? > "$out/$1.rc"); }
run_census() { (cd "$scratch/$1" && python3 -c 'import sys; sys.path.insert(0, "scripts"); import ci_gate_workflows_selftest as t; t.census_controls(); print("census_controls PASS")' > "$out/$1.log" 2>&1; echo $? > "$out/$1.rc"); }
pool='merged[path] = re.compile(("" if known is None else known.pattern + "|") + declared_line_mask(tuple(l for ls in declared.values() for l in ls)))'
# M1: every declared file accepts every declared line (pooled), new arms present
copy m1-pooled; python3 - "$scratch/m1-pooled/scripts/check_baremetal_only.py" "$pool" <<'PY'
import sys; p, new = sys.argv[1], sys.argv[2]; s = open(p).read()
old = 'merged[path] = re.compile(("" if known is None else known.pattern + "|") + declared_line_mask(lines))'
assert s.count(old) == 1; open(p, "w").write(s.replace(old, new))
PY
# M1-old: same mutant with the delta's cross-file arms removed (the pre-delta arm set)
copy m1-pooled-old-arms; cp "$scratch/m1-pooled/scripts/check_baremetal_only.py" "$scratch/m1-pooled-old-arms/scripts/"
python3 - "$scratch/m1-pooled-old-arms/scripts/check_baremetal_only.py" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
assert s.count("                *others,\n") == 1; open(p, "w").write(s.replace("                *others,\n", ""))
PY
# M2: an unreadable limit is swallowed and refused later as non-numeric (another stated reason)
copy m2-swallow; python3 - "$scratch/m2-swallow/scripts/ci_runtime_workflows.py" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
old = '    if ! limit="$(cat "$cgroup/memory.max")"; then\n      echo "unreadable memory limit in $cgroup" >&2; exit 1\n    fi\n'
new = '    limit="$(cat "$cgroup/memory.max" 2>/dev/null || true)"\n'
assert s.count(old) == 1; open(p, "w").write(s.replace(old, new))
PY
# M3: the CPU and MemTotal refusals lose their stated reasons (pre-delta shell)
copy m3-silent; python3 - "$scratch/m3-silent/scripts/ci_runtime_workflows.py" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
for old, new in (('test "$cpus" -gt 0 || { echo "no CPUs: nproc printed $cpus" >&2; exit 1; }', 'test "$cpus" -gt 0'),
                 ('test "$kib" -gt 0 || { echo "no MemTotal in kB" >&2; exit 1; }', 'test "$kib" -gt 0')):
    assert s.count(old) == 1; s = s.replace(old, new)
open(p, "w").write(s)
PY
# M2-old / M3-old: the same mutants against the pre-delta census controls
for m in m2-swallow m3-silent; do
  copy "$m-old-test"; cp "$scratch/$m/scripts/ci_runtime_workflows.py" "$scratch/$m-old-test/scripts/"
  git -C "$src" show "$old:scripts/ci_gate_workflows_selftest.py" > "$scratch/$m-old-test/scripts/ci_gate_workflows_selftest.py"
done
run_bm m1-pooled & run_bm m1-pooled-old-arms &
run_census m2-swallow & run_census m3-silent & run_census m2-swallow-old-test & run_census m3-silent-old-test &
wait
for m in m1-pooled m1-pooled-old-arms m2-swallow m3-silent m2-swallow-old-test m3-silent-old-test; do
  echo "$m rc=$(cat "$out/$m.rc")"
done
