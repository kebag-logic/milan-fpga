#!/usr/bin/env bash
# Reviewer-owned gate probes on a disposable clone at the exact head.
# usage: gate_probes.sh CLONE PRBODY EVIDENCE SUITESLOG
# Each probe edits the clone, runs the named check, records rc and the named
# line(s), then restores the clone with git checkout/clean. Probes are
# independent of the gate's own self-test plants.
set -u
C=$1; PRBODY=$2; EVID=$3; SUITES=$4
cd "$C" || exit 99
HEAD=4bee75b2e647507a71ece50359fceb135c334757
restore() { git checkout -q -- . && git clean -qfdx -e .venv-wavedrom >/dev/null; }
probe() { # name, expected rc pattern, grep words, command...
  local name=$1 want=$2 words=$3; shift 3
  local out; out=$("$@" 2>&1); local rc=$?
  local hit; hit=$(printf '%s\n' "$out" | grep -F -- "$words" | head -3)
  local verdict=MISS
  if [[ "$rc" =~ ^($want)$ ]] && { [ -z "$words" ] || [ -n "$hit" ]; }; then verdict=AS-EXPECTED; fi
  echo "PROBE $name rc=$rc expect_rc=$want verdict=$verdict"
  [ -n "$hit" ] && printf '%s\n' "$hit" | sed 's/^/    named: /'
  [ "$verdict" = MISS ] && printf '%s\n' "$out" | tail -8 | sed 's/^/    tail: /'
}
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "not at head"; exit 98; }
restore

# 0. head is clean: gate, F06.14/registry regeneration is a no-op, PR field reference agrees
probe head-gate 0 "OK" python3 -B scripts/check_aecp_commands.py
python3 -B scripts/check_aecp_commands.py --write >/dev/null 2>&1; echo "regen rc=$?"
echo "regen diff (empty = generated sections current):"; git status --porcelain | sed 's/^/    /'
restore
probe pr-body-field-reference 0 "" python3 -B scripts/check_aecp_commands.py --pr-body "$PRBODY"
probe reqtags-static 0 "OK" python3 -B scripts/check-req-tags.py

# 1. R608-3 echo-hide, exact file edit (EAVL's three BUILD_FLD words NOPed, EAVL exempted)
python3 - <<'EOF'
import json, pathlib
p = pathlib.Path("hdl/aecp/ucode/gen_ucode.py"); t = p.read_text()
old = ("    u('BUILD_FLD', ra=3, fmt=FMT_D),             # flags                  @24\n"
       "    u('BUILD_FLD', ra=2, fmt=FMT_Q),             # acquired_controller_id @28\n"
       "    u('BUILD_FLD', ra=1, fmt=FMT_Q),             # locked_controller_id   @36\n")
assert t.count(old) == 1; p.write_text(t.replace(old, "    u('NOP'),\n" * 3))
q = pathlib.Path("hdl/aecp/ucode/aecp_commands.json"); d = json.loads(q.read_text())
d["echo_entries"].append("EAVL"); q.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
EOF
probe echo-hide 1 "echo_entries: EAVL" python3 -B scripts/check_aecp_commands.py
# 1b. same, with EAVL also declared shared, so membership passes: SUCCESS size must still fail
python3 - <<'EOF'
import json, pathlib
q = pathlib.Path("hdl/aecp/ucode/aecp_commands.json"); d = json.loads(q.read_text())
d["shared_entries"]["EAVL"] = "probe"; q.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
EOF
probe echo-hide-shared 1 "EAVL" python3 -B scripts/check_aecp_commands.py
restore

# 2. a stale input digest: KL_aecp_engine.sv's pre-merge digest put back in decode.json
sed -i 's/4b59126375de76fa699bc1b2a214e618619fcd176b6e7cd75194c43333e998c6/4fd2385ca43edbbb355e0f8c80d1869af7e2017a19e78225709dd97554e4662d/' tb/aecp_cmds/decode.json
git diff --quiet tb/aecp_cmds/decode.json && echo "digest probe did not apply"
probe stale-engine-digest 1 "KL_aecp_engine.sv" python3 -B scripts/check_aecp_commands.py
restore

# 3. an opcode renumbered in the table only (held field commands[].opcode)
python3 - <<'EOF'
import json, pathlib
q = pathlib.Path("hdl/aecp/ucode/aecp_commands.json"); d = json.loads(q.read_text())
c = next(c for c in d["commands"] if c["name"] == "GET_STREAM_INFO"); c["opcode"] = "0x%04X" % (int(c["opcode"], 16) + 0x40)
q.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
EOF
probe opcode-table-only 1 "GET_STREAM_INFO" python3 -B scripts/check_aecp_commands.py
restore

# 4. the generated 09 section 8.11 registry block hand-edited (generated reference drift)
python3 - <<'EOF'
import pathlib
p = pathlib.Path("docs/architecture/09_verification.md"); t = p.read_text()
old = "- commands[].opcode: held."; assert t.count(old) == 1
p.write_text(t.replace(old, "- commands[].opcode: held to nothing."))
EOF
probe registry-block-hand-edit 1 "" python3 -B scripts/check_aecp_commands.py
restore

# 5. the REQ-VER-002 Arch cell hand-edited (this PR's generated Arch text)
sed -i 's/Generated references: gate docstring, 09 §8.11 and PR field reference./Generated references: gate docstring, 09 §8.10 and PR field reference./' docs/00_MILAN_COMPLIANCE_REVIEW.md
git diff --quiet docs/00_MILAN_COMPLIANCE_REVIEW.md && echo "arch probe did not apply"
probe arch-cell-stale-section 1 "" python3 -B scripts/check_aecp_commands.py
restore

# 6. traceability: the REQ-VER-002 Cov cell given the PR's pre-merge form
sed -i 's/| design | A; no check | \[GAP-11\](#gap-11) | <!-- AECP ARCH -->/| design | A (the tree: P, per Arch) | [GAP-11](#gap-11) | <!-- AECP ARCH -->/' docs/00_MILAN_COMPLIANCE_REVIEW.md
git diff --quiet docs/00_MILAN_COMPLIANCE_REVIEW.md && echo "cov probe did not apply"
probe cov-pre-merge-form 1 "COV RECORD REQ-VER-002" python3 -B scripts/check-req-tags.py
restore

# 7. traceability: the tag's check name no longer the test it heads
sed -i 's/"ObservedCommands.test_sweep")/"ObservedCommands.test_other")/' tb/aecp_cmds/check_observed.py
probe tag-name-mismatch 1 "check_observed.py" python3 -B scripts/check-req-tags.py
restore

# 8. traceability: REQ-VER-002 removed from the coverage table's lint row
sed -i 's/^| no check | lint | REQ-REU-002, REQ-VER-002, REQ-DOC-001 |$/| no check | lint | REQ-REU-002, REQ-DOC-001 |/' docs/architecture/09_verification.md
git diff --quiet docs/architecture/09_verification.md && echo "coverage probe did not apply"
probe coverage-row-drop 1 "COVERAGE RECORD no check lint" python3 -B scripts/check-req-tags.py
restore

# 9. executed half on the reviewer's subset run, filtered to tb/aecp_cmds' tag:
#    as recorded, and with its evidence line removed (DEAD TAG by name)
grep ' check_observed.py:' "$EVID" | sed 's/^/    evidence: /'
python3 -I -B "$(dirname "$0")/exec_probe.py" "$C" "$SUITES" "$EVID" aecp_cmds
restore
echo "restored: $(git status --porcelain | wc -l) changes; head $(git rev-parse HEAD)"
