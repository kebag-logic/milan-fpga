#!/usr/bin/env bash
# Generator and judge mutants against the fast Yosys tool judges at one exact head.
# Usage: probe_bind_mutants.sh <clean clone at head> <scratch dir> <receipt dir>
# Each mutant: export the head tree, apply one edit, regenerate the workflows (as an author would, so the
# file-equality check passes by construction), then run the fast-tool controls, the generator check and the
# event-contract check. A generator mutant is CAUGHT when any of the three exits non-zero.
set -u
CLONE=$1 SCR=$2 OUT=$3
mkdir -p "$SCR" "$OUT"
BASE="$SCR/base"
rm -rf "$BASE"; mkdir -p "$BASE"; git -C "$CLONE" archive HEAD | tar -x -C "$BASE"

G=scripts/ci_gate_workflows.py
J=scripts/ci_fast_tool_selftest.py
# name|file|python edit applied to that file's text (variable s)
MUTANTS=$(cat <<'EOF'
control|scripts/ci_gate_workflows.py|s=s
B01_drop_selftest|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n    c = workflow["jobs"][FAST_TOOL_CONSUMER]["steps"]\n    c[:] = [x for x in c if x.get("name") != "Prove the result cache refuses a planted entry"]\n',1)
B02_tool_env_after|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n    workflow["jobs"][FAST_TOOL_JOB]["env"] = {"CXXFLAGS": "-O0"}\n',1)
B03_build_rewrite_after|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n    b = next(x for x in workflow["jobs"][FAST_TOOL_JOB]["steps"] if x.get("name") == YOSYS_BUILD_STEPS[1])\n    b["run"] = b["run"] + "true\\n"\n',1)
B04_restore_no_failmiss|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n        step["with"].pop("fail-on-cache-miss", None)\n',1)
B05_tool_timeout_raised|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n    workflow["jobs"][FAST_TOOL_JOB]["timeout-minutes"] = 45\n',1)
B06_consumer_needs_dropped|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n    workflow["jobs"][FAST_TOOL_CONSUMER]["needs"] = ["changes"]\n',1)
B07_other_job_step|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n    workflow["jobs"]["verilator-lint"]["steps"].pop()\n',1)
B08_workflow_concurrency|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n    workflow["permissions"] = {"contents": "write"}\n',1)
B09_hashfiles_dropped|scripts/ci_gate_workflows.py|s=s.replace('    if reads:\n        recipe +=', '    if False:\n        recipe +=',1)
B10_digest_empty|scripts/ci_gate_workflows.py|s=s.replace('recipe = "recipe-" + recipe_digest(inputs)', 'recipe = "recipe-" + recipe_digest({})',1)
B11_restore_other_digest|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe if job_id == FAST_TOOL_JOB else "recipe-" + "1" * 64)\n',1)
B12_restore_fallback|scripts/ci_gate_workflows.py|s=s.replace('        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n', '        step["with"]["key"] = step["with"]["key"].replace(FAST_TOOL_RECIPE, recipe)\n        step["with"]["restore-keys"] = "yosys-"\n',1)
J01_no_jobkey_compare|scripts/ci_fast_tool_selftest.py|s=s.replace('            findings.append("emitted " + job_id + "\'s job keys differ from the transformed derivation\'s")', '            pass',1)
J02_no_recipe_set|scripts/ci_fast_tool_selftest.py|s=s.replace('    if len(recipes) > 1:', '    if False:',1)
J03_no_tops|scripts/ci_fast_tool_selftest.py|s=s.replace('    if tops:\n', '    if False:\n',1)
J04_no_emitted_steps|scripts/ci_fast_tool_selftest.py|s=s.replace('        findings.extend(step_findings("emitted " + job_id, job["steps"], actual["steps"], "steps"))', '        pass',1)
J05_replay_is_emitted|scripts/ci_fast_tool_selftest.py|s=s.replace('    emitted = copy.deepcopy(generated)\n', '    emitted = copy.deepcopy(generated)\n    staged = copy.deepcopy(generated)\n',1)
EOF
)
while IFS='|' read -r name file edit; do
  W="$SCR/m/$name"; rm -rf "$W"; mkdir -p "$W"; cp -a "$BASE/." "$W/"
  python3 -I - "$W/$file" "$edit" <<'PY'
import sys
path, edit = sys.argv[1], sys.argv[2]
s = open(path).read(); before = s
exec(edit)
if edit != "s=s" and s == before:
    sys.exit("edit did not apply")
open(path, "w").write(s)
PY
  [ $? -eq 0 ] || { echo "$name EDIT-FAILED" >> "$OUT/probe_summary.txt"; continue; }
  (
    cd "$W"
    python3 scripts/ci_gate_workflows.py > "$OUT/$name.regen.log" 2>&1; regen=$?
    python3 -I -c 'import sys; sys.path.insert(0, "scripts"); from ci_fast_tool_selftest import fast_tool_controls; fast_tool_controls()' > "$OUT/$name.controls.log" 2>&1; ctl=$?
    python3 scripts/ci_gate_workflows.py --check > "$OUT/$name.check.log" 2>&1; chk=$?
    python3 scripts/ci_events.py --check > "$OUT/$name.events.log" 2>&1; ev=$?
    first=$(grep -m1 -E "AssertionError|Error" "$OUT/$name.controls.log" | cut -c1-240)
    echo "$name regen=$regen controls=$ctl check=$chk events=$ev :: $first" >> "$OUT/probe_summary.txt"
  ) &
  while [ "$(jobs -rp | wc -l)" -ge 16 ]; do wait -n; done
done < <(printf '%s\n' "$MUTANTS")
wait
sort "$OUT/probe_summary.txt" -o "$OUT/probe_summary.txt"
cat "$OUT/probe_summary.txt"
