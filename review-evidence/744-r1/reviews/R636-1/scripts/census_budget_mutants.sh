#!/usr/bin/env bash
# Mutants of census_budget_step in a tree (restored from the backup at the end); each must
# make scripts/ci_gate_workflows_selftest.py fail. Usage: census_budget_mutants.sh <tree> <backup-file> <log-dir>; restores the file from the backup.
set -u
copy="$1"; logs="${3:?log dir}"
target="$copy/scripts/ci_runtime_workflows.py"
orig="${2:?backup path}"; cp "$target" "$orig"
mutate() {  # name, python expression rewriting text
  local name="$1" expr="$2"
  cp "$orig" "$target"
  python3 -I -c "import sys; p=sys.argv[1]; t=open(p).read(); n=$expr; assert n!=t, 'mutant did not apply'; open(p,'w').write(n)" "$target" || { echo "$name: NOT APPLIED"; return; }
  (cd "$copy" && python3 scripts/ci_gate_workflows_selftest.py > "$logs/mutant-$name.log" 2>&1)
  local rc=$?
  echo "$name: selftest rc=$rc $( [ $rc -ne 0 ] && echo KILLED || echo SURVIVED ) :: $(grep -m1 -E 'AssertionError|Error' "$logs/mutant-$name.log" | cut -c1-160)"
}
mutate no-headroom      "t.replace('memory * 2 / (3 * ', 'memory / (1 * ')"
mutate leaf-only        "t.replace('if [ \"\$cgroup\" = /sys/fs/cgroup ]; then break; fi', 'break')"
mutate max-not-min      "t.replace('if [ \"\$limit\" -lt \"\$memory\" ]', 'if [ \"\$limit\" -gt \"\$memory\" ]')"
mutate no-nproc-cap     "t.replace('census=\$(( census < cpus ? census : cpus ))\n', '')"
mutate no-floor-one     "t.replace('census=\$(( census > 0 ? census : 1 ))\n', '')"
mutate garbage-ignored  "t.replace(\"''|*[!0-9]*) echo\", \"''|*[!0-9]*) ;; x) echo\")"
mutate memtotal-ignored "t.replace('memory=\$(( kib * 1024 ))', 'memory=999999999999999')"
mutate step-not-added   "t.replace('job[\"steps\"].insert(checkout + 2, census_budget_step())', 'pass')"
mutate step-after-census "t.replace('job[\"steps\"].insert(checkout + 2, census_budget_step())', 'job[\"steps\"].append(census_budget_step())')"
# Behavioural variant of leaf-only that keeps the planted-path count intact.
mutate leaf-only-walk  "t.replace('  cgroup=\"\${cgroup%/*}\"\ndone', '  break\ndone')"
cp "$orig" "$target"
