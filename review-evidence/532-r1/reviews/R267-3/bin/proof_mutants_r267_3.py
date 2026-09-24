#!/usr/bin/env python3
"""Independent mutants of scripts/act_slot_proof.sh, graded by its own --selftest.

Each mutant is a list of exact (old, new) substitutions; every `old` must occur
exactly once in the source, or the mutant is reported NOT-APPLICABLE. The
mutated copy runs `bash act_slot_proof.sh --selftest` inside sandbox.sh (no
network, no Docker socket, inert sudo), so the self-test's own `bash "$0"`
re-invocations grade the mutated proof. KILLED means the self-test failed;
the failing case names are listed so a kill can be attributed.

usage: proof_mutants_r267_3.py TREE OUT_DIR root|user [--jobs N] [--only ID,...]
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox.sh"

# id, what the mutant removes or weakens, [(old, new), ...]
MUTANTS: list[tuple[str, str, list[tuple[str, str]]]] = [
    ("Q00", "control: a comment line only", [
        ("set -euo pipefail\n", "set -euo pipefail\n# r267-3 control mutant\n")]),
    ("Q01", "slot-number check removed", [
        ('case "$number" in \'\'|*[!0-9]*) echo "slots are numbers: $number" >&2; exit 2 ;; esac',
         ":")]),
    ("Q02", "slots A and B may be equal", [
        ('if [ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ]', 'if [ "$slot_a" -eq 0 ]')]),
    ("Q03", "slot A may be 0", [
        ('[ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ] || [ "$slot_b" -eq 0 ]',
         '[ "$slot_a" -eq "$slot_b" ] || [ "$slot_b" -eq 0 ]')]),
    ("Q04", "slot B may be 0", [
        ('[ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ] || [ "$slot_b" -eq 0 ]',
         '[ "$slot_a" -eq "$slot_b" ] || [ "$slot_a" -eq 0 ]')]),
    ("Q05", "required-argument check removed (input validation)", [
        ('if [ -z "$required" ]; then usage >&2; exit 2; fi', ":")]),
    ("Q06", "runner digest not compared", [
        ('if [ "$actual" != "$sha" ] || [ -n "$(find',
         'if false || [ -n "$(find')]),
    ("Q07", "runner write-bit check removed", [
        ('|| [ -n "$(find "$runner" -maxdepth 0 -perm /0222)" ] \\', "\\")]),
    ("Q08", "non-root writability check removed (documented as unstaged)", [
        ('|| { [ "$(id -u)" -ne 0 ] && [ -w "$runner" ]; }; then', "; then")]),
    ("Q09", "non-empty log directory accepted", [
        ('if [ -n "$(ls -A "$logs")" ]; then', "if false; then")]),
    ("Q10", "interrupt gate ignores the runner's exit status", [
        ('  if (cd "$logs" && python3 -I "$runner" --interrupt-selftest',
         '  if { (cd "$logs" && python3 -I "$runner" --interrupt-selftest'),
        ('--slot-root "$slot_root_a") >"$log" 2>&1 \\',
         '--slot-root "$slot_root_a") >"$log" 2>&1 || true; } \\')]),
    ("Q11", "interrupt gate needs no PASS line", [
        ("    && grep -q '^interrupt-selftest: PASS ' \"$log\" \\", "    && true \\")]),
    ("Q12", "interrupt gate needs no slot teardown line", [
        ('    && grep -q "^interrupt-selftest: slot $slot_a: " "$log"; then', "    && true; then")]),
    ("Q13", "interrupt gate not run in slot A", [
        ('--sudo --slot "$slot_a" --slot-root "$slot_root_a")', "--sudo)")]),
    ("Q14", "complete: a FAILED run need not exit 1", [
        ('if [ "$actual" = "exit 1$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi',
         'if [ "${actual#exit ?}" = "$expected"$\'\\n\'"$name FAILED" ]; then return 0; fi')]),
    ("Q15", "complete: an all-PASS run need not exit 0", [
        ('  [ "$actual" = "exit 0$expected" ]', '  [ "${actual#exit ?}" = "$expected" ]')]),
    ("Q16", "complete: a prefix of the PASS lines is enough", [
        ('  [ "$actual" = "exit 0$expected" ]', '  [[ "exit 0$expected" == "$actual"* ]]')]),
    ("Q17", "complete always true", [
        ('  local actual expected="" name\n', '  return 0\n  local actual expected="" name\n')]),
    ("Q18", "serial reference always PASS", [
        ('  if complete "$1"; then', "  if true; then")]),
    ("Q19", "parallel comparison ignores completion", [
        ('  if ! complete "$1"; then', "  if false; then")]),
    ("Q20", "same_verdict always true", [
        ('  cmp -s "$logs/$1.verdict" "$logs/$2.verdict"', "  true")]),
    ("Q21", "parallel comparison ignores the verdict", [
        ('  elif same_verdict "$1" "$2"; then', "  elif true; then")]),
    ("Q22", "await_holder returns at once", [
        ('  while [ "$polls" -lt 720 ]; do', '  return 0\n  while [ "$polls" -lt 720 ]; do')]),
    ("Q23", "await_holder accepts the generic running marker for a slot", [
        ('  if [ "$slot" -ne 0 ]; then marker="act-ci: slot $slot: own daemon"; fi', "  :")]),
    ("Q24", "await_holder has no early exit on an ended run (liveness only)", [
        ('    if [ -e "$logs/$label.status" ]; then return 1; fi', "    :")]),
    ("Q25", "overlap: run A may have ended", [
        ("    && ! ended parallel-a && ! ended parallel-b; then", "    && ! ended parallel-b; then")]),
    ("Q26", "overlap: run B may have ended", [
        ("    && ! ended parallel-a && ! ended parallel-b; then", "    && ! ended parallel-a; then")]),
    ("Q27", "overlap: run B need not hold its slot", [
        ('  if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \\',
         '  if await_holder parallel-a "$slot_a" \\')]),
    ("Q28", "overlap: run A need not hold its slot", [
        ('  if await_holder parallel-a "$slot_a" && await_holder parallel-b "$slot_b" \\',
         '  if await_holder parallel-b "$slot_b" \\')]),
    ("Q29", "ended always false", [
        ("  grep -q -E '^act-ci: ([a-z-]+: (PASS|FAILED)|REFUSED)' \"$logs/$1.log\" 2>/dev/null",
         "  false")]),
    ("Q30", "ended ignores a refusal", [
        ("'^act-ci: ([a-z-]+: (PASS|FAILED)|REFUSED)'", "'^act-ci: ([a-z-]+: (PASS|FAILED))'")]),
    ("Q31", "ended ignores verdicts", [
        ("'^act-ci: ([a-z-]+: (PASS|FAILED)|REFUSED)'", "'^act-ci: REFUSED'")]),
    ("Q32", "collision: rival started without waiting for the holder (sequencing only)", [
        ('  if ! await_holder "collide-$slot-holder" "$slot"; then', "  if false; then")]),
    ("Q33", "collision: rival may be refused after the holder ended", [
        ('  if [ "$rival_early" -eq 1 ] && [ "$rival_status" = 2 ] \\',
         '  if [ "$rival_status" = 2 ] \\')]),
    ("Q34", "collision: rival exit status not checked", [
        ('  if [ "$rival_early" -eq 1 ] && [ "$rival_status" = 2 ] \\',
         '  if [ "$rival_early" -eq 1 ] \\')]),
    ("Q35", "collision: refusal reason not checked", [
        ('    && grep -q -E "$refusal" "$logs/collide-$slot-rival.log" \\', "    && true \\")]),
    ("Q36", "collision: holder need not complete", [
        ('    && complete "collide-$slot-holder" && same_verdict "collide-$slot-holder" serial-a; then',
         '    && same_verdict "collide-$slot-holder" serial-a; then')]),
    ("Q37", "collision: holder verdict not compared", [
        ('    && complete "collide-$slot-holder" && same_verdict "collide-$slot-holder" serial-a; then',
         '    && complete "collide-$slot-holder"; then')]),
    ("Q38", "slot-A collision accepts any refusal", [
        ('  collide "$slot_a" "is in use by another runner invocation"', '  collide "$slot_a" "REFUSED"')]),
    ("Q39", "slot-0 collision accepts any refusal", [
        ('  collide 0 "act-toolcache|already exist"', '  collide 0 "REFUSED"')]),
    ("Q40", "slot-0 collision removed", [
        ('  collide 0 "act-toolcache|already exist"', "  :")]),
    ("Q41", "slot-A collision removed", [
        ('  collide "$slot_a" "is in use by another runner invocation"', "  :")]),
    ("Q42", "isolation: the slot's own view not checked", [
        ('  if [ "$inside" = "container=refused published=refused internet=reached " ] \\',
         "  if true \\")]),
    ("Q43", "isolation: the host's view not checked", [
        ('    && [ "$outside" = "container=reached published=reached " ]; then', "    ; then")]),
    ("Q44", "isolation: the probe name need not answer", [
        ('  if [ "$inside" = "container=refused published=refused internet=reached " ] \\',
         '  if [ "${inside% internet=* }" = "container=refused published=refused" ] \\')]),
    ("Q45", "isolation: the published port may be reached from the slot", [
        ('  if [ "$inside" = "container=refused published=refused internet=reached " ] \\',
         '  if [[ "$inside" == "container=refused published="*" internet=reached " ]] \\')]),
    ("Q46", "isolation probed from the host namespace instead of the slot", [
        ('  inside=$(sudo -n nsenter "--net=/run/netns/milan-act-slot-$slot" -- env -i PATH=/usr/bin:/bin \\',
         "  inside=$(sudo -n env -i PATH=/usr/bin:/bin \\")]),
    ("Q47", "target start failure not recorded", [
        ('    record FAIL "isolation target: it could not be started on the default daemon (see isolation.log)"',
         "    :")]),
    ("Q48", "target start ignores a failed docker run", [
        ('--entrypoint python3 "$probe_image" -c "$LISTENER" >/dev/null || return 1',
         '--entrypoint python3 "$probe_image" -c "$LISTENER" >/dev/null || true')]),
    ("Q49", "target start: empty address check removed (masked by host reach)", [
        ('  [ -n "$target_gateway" ] && [ -n "$target_ip" ] && [ -n "$target_port" ]', "  true")]),
    ("Q50", "target removal ignores a surviving container", [
        ('  if [ -n "$containers$networks" ]; then', '  if [ -n "$networks" ]; then')]),
    ("Q51", "target removal ignores a surviving network", [
        ('  if [ -n "$containers$networks" ]; then', '  if [ -n "$containers" ]; then')]),
    ("Q52", "a failed container query reads as absent", [
        ("    || containers=unknown", '    || containers=""')]),
    ("Q53", "a failed network query reads as absent", [
        ("    || networks=unknown", '    || networks=""')]),
    ("Q54", "explicit target removal moved to the exit trap only", [
        ("  parallel\n  remove_target\n", "  parallel\n")]),
    ("Q55", "PROVED needs no FAIL-free summary (count only)", [
        ("  if grep -q '^FAIL' \"$logs/SUMMARY\" || [", "  if [")]),
    ("Q56", "PROVED needs no ten-PASS count (documented backstop)", [
        ("  if grep -q '^FAIL' \"$logs/SUMMARY\" || [ \"$(grep -c '^PASS' \"$logs/SUMMARY\")\" -ne 10 ]; then",
         "  if grep -q '^FAIL' \"$logs/SUMMARY\"; then")]),
    ("Q57", "a failed proof exits 0", [
        ("    exit 1\n  fi\n  record PROVED", "    exit 0\n  fi\n  record PROVED")]),
    ("Q58", "runner install never verified", [
        ("prove() {\n  verify_runner\n", 'prove() {\n  mkdir -p "$logs"\n')]),
    ("Q59", "runs are not pinned to the audited digest (runner-side check, not modelled)", [
        ('--worktree "$worktree" --trusted-install-sha256 "$sha" --act-bin "$act_bin"',
         '--worktree "$worktree" --act-bin "$act_bin"')]),
    ("Q60", "runs are not placed in their slots", [
        ('  if [ "$slot" -ne 0 ]; then slot_args=(--slot "$slot" --slot-root "$(slot_root "$slot")"); fi',
         "  :")]),
    ("Q61", "slot B's parallel verdict not compared with its serial reference", [
        ('  elif same_verdict "$1" "$2"; then', '  elif [ "$1" = parallel-b ] || same_verdict "$1" "$2"; then')]),
    ("Q62", "slot B's isolation view not checked", [
        ('  if [ "$inside" = "container=refused published=refused internet=reached " ] \\',
         '  if { [ "$slot" = "$slot_b" ] || [ "$inside" = "container=refused published=refused internet=reached " ]; } \\')]),
]


def apply(source: str, edits: list[tuple[str, str]]) -> str | None:
    """The mutated source, or None when an edit does not occur exactly once."""
    for old, new in edits:
        if source.count(old) != 1:
            return None
        source = source.replace(old, new, 1)
    return source


def run(mid: str, text: str, out: pathlib.Path, mode: str) -> tuple[str, int, list[str], str]:
    """Run one mutant's self-test in the sandbox; its id, rc, failed cases and last line."""
    work = out / "scratch" / mode / mid
    shutil.rmtree(work, ignore_errors=True)
    (work / "scripts").mkdir(parents=True)
    script = work / "scripts" / "act_slot_proof.sh"
    script.write_text(text, encoding="utf-8")
    script.chmod(0o755)
    proc = subprocess.run(
        [str(SANDBOX), mode, str(work), "--", "bash", "scripts/act_slot_proof.sh", "--selftest"],
        capture_output=True, text=True, timeout=900,
    )
    log = proc.stdout + proc.stderr
    (out / "logs" / mode).mkdir(parents=True, exist_ok=True)
    (out / "logs" / mode / f"{mid}.log").write_text(log, encoding="utf-8")
    failed = re.findall(r"^  FAIL (.*?): exit", log, flags=re.M)
    last = log.strip().splitlines()[-1] if log.strip() else ""
    shutil.rmtree(work, ignore_errors=True)
    return mid, proc.returncode, failed, last


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tree", type=pathlib.Path)
    parser.add_argument("out", type=pathlib.Path)
    parser.add_argument("mode", choices=("root", "user"))
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--only", default="")
    args = parser.parse_args()
    source_path = args.tree / "scripts" / "act_slot_proof.sh"
    source = source_path.read_text(encoding="utf-8")
    print(f"# source {source_path} sha256 {hashlib.sha256(source.encode()).hexdigest()} mode {args.mode}")
    only = set(filter(None, args.only.split(",")))
    jobs: dict[str, str] = {}
    described = {mid: what for mid, what, _ in MUTANTS}
    for mid, what, edits in MUTANTS:
        if only and mid not in only:
            continue
        text = apply(source, edits)
        if text is None:
            print(f"{mid}\tNOT-APPLICABLE\t-\t{what}")
            continue
        jobs[mid] = text
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run, mid, text, args.out, args.mode) for mid, text in jobs.items()]
        for future in concurrent.futures.as_completed(futures):
            mid, rc, failed, last = future.result()
            results[mid] = (rc, failed, last)
    for mid in jobs:
        rc, failed, last = results[mid]
        verdict = "SURVIVED" if rc == 0 else "KILLED"
        print(f"{mid}\t{verdict}\trc={rc}\t{described[mid]}\tfailed-cases={'; '.join(failed) or '-'}\t{last}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
