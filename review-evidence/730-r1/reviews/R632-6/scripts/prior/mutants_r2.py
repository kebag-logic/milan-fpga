"""Reviewer mutation campaign for PR #731 round 2: each mutant must fail the runner's self-test.

Usage: python3 -I mutants_r2.py <packet-dir> <pristine-tree> [--jobs N]

For each mutant: hard-link copy <pristine-tree> to <packet>/scratch/mut/<id>,
replace scripts/act_ci.py with the mutated text (the anchor must occur exactly
once), then run `act_ci.py --selftest` and, for the record-logic mutants, the
reviewer probe, both through <packet>/scripts/sandbox.sh (no network, no
Docker socket). Prints one line per mutant and a tally.
"""

from __future__ import annotations

import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

PACKET = pathlib.Path(sys.argv[1]).resolve()
PRISTINE = pathlib.Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
SANDBOX = PACKET / "scripts" / "sandbox.sh"
PROBE = PACKET / "scripts" / "probe_r2.py"

STOP_OLD = '''        try:
            seams.terminate_group(
                process,
                use_sudo=context.use_sudo,
                primary=Refusal("the CPU-range monitor is stopping"),
            )
        except BaseException as exc:
            failures.append(exc)
        if reader is not None and reader.ident is not None:
            failure = join_job_cpu_reader(reader, record, process.pid)
            if failure is not None:
                failures.append(failure)
'''
STOP_SWAPPED = '''        if reader is not None and reader.ident is not None:
            failure = join_job_cpu_reader(reader, record, process.pid)
            if failure is not None:
                failures.append(failure)
        try:
            seams.terminate_group(
                process,
                use_sudo=context.use_sudo,
                primary=Refusal("the CPU-range monitor is stopping"),
            )
        except BaseException as exc:
            failures.append(exc)
'''

# (id, probe too?, what it breaks, anchor, replacement)
MUTANTS = [
    ("K01", True, "die frees a range",
     '        if action == "destroy":\n            self.release(container_id)',
     '        if action in ("destroy", "die"):\n            self.release(container_id)'),
    ("K02", True, "a timed-out move releases its range",
     "        except Refusal as exc:\n            failure = str(exc)\n        else:",
     "        except Refusal as exc:\n            self.release(container_id)\n            return\n        else:"),
    ("K03", True, "a refused move releases its range",
     '                failure = detail[-1] if detail else f"exit status {result.returncode}"\n',
     '                self.release(container_id)\n                return\n'),
    ("K04", False, "no inspect after the move; counted moved on the CLI's word",
     "        self.check(container_id, moved_now=True, failure=failure)",
     '        self.outcome[container_id] = "moved"'),
    ("K05", True, "free ranges ignore reservations",
     "        taken = set(self.held.values())", "        taken = set()"),
    ("K06", False, "no re-inspection of holders when every range is held",
     "            for holder in list(self.held):\n                self.check(holder)",
     "            pass"),
    ("K07", True, "an unreadable inspect releases the range",
     "        except Refusal as exc:\n            self.problems.append(\n                f\"cannot read job container",
     "        except Refusal as exc:\n            self.release(container_id)\n            self.problems.append(\n                f\"cannot read job container"),
    ("K08", True, "an off-target inspect releases the range",
     '        elif moved_now or self.outcome[container_id] == "moved":\n            self.problems.append(',
     '        elif moved_now or self.outcome[container_id] == "moved":\n            self.release(container_id)\n            self.problems.append('),
    ("K09", False, "a containment (reap) failure skips the reader join",
     "        except BaseException as exc:\n            failures.append(exc)\n        if reader is not None",
     "        except BaseException as exc:\n            raise\n        if reader is not None"),
    ("K10", False, "the reader is never joined",
     "            failure = join_job_cpu_reader(reader, record, process.pid)",
     "            failure = None"),
    ("K11", False, "the reader is joined before the stream is contained", STOP_OLD, STOP_SWAPPED),
    ("K12", False, "a failed join is not retried",
     "        if not reader.is_alive():\n            return failure",
     "        if failure is not None or not reader.is_alive():\n            return failure"),
    ("K13", False, "the bounded join gives up on a live reader",
     "        if timeout is not None:\n            timeout = None",
     "        if timeout is not None:\n            return failure"),
    ("K14", False, "the event pipe is never closed",
     "                process.stdout.close()", "                pass"),
    ("K15", False, "slot 0 falls back silently on a small host",
     '    if last >= host_cpus:\n        raise Refusal(\n            f"replay slot {slot} needs CPUs {base}-{last}',
     '    if last >= host_cpus and slot != 0:\n        raise Refusal(\n            f"replay slot {slot} needs CPUs {base}-{last}'),
    ("K16", False, "host CPU check off by one",
     '    if last >= host_cpus:\n        raise Refusal(\n            f"replay slot {slot} needs CPUs {base}-{last}',
     '    if last > host_cpus:\n        raise Refusal(\n            f"replay slot {slot} needs CPUs {base}-{last}'),
    ("K17", False, "slots spaced 16 CPUs apart (blocks meet)",
     "    return ReplaySlot(slot).number * (SLOT_JOB_RANGES + 1) * CONTAINER_CPU_LIMIT",
     "    return ReplaySlot(slot).number * SLOT_JOB_RANGES * CONTAINER_CPU_LIMIT"),
    ("K18", False, "run uses a constant 4 ranges, not the derived count",
     "        cpu_ranges = job_cpu_ranges(slot.number, concurrency)",
     "        cpu_ranges = job_cpu_ranges(slot.number, SLOT_JOB_RANGES)"),
    ("K19", False, "concurrency sums every job, not the CONCURRENT_JOB_LIMIT widest",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
     "        most = max(most, sum(widths))"),
    ("K20", False, "a signed max-parallel is accepted",
     're.fullmatch(r"[0-9]{1,6}", raw)', 're.fullmatch(r"-?[0-9]{1,6}", raw)'),
    ("K21", False, "a too-wide derivation is not refused",
     "    if not 1 <= concurrency <= SLOT_JOB_RANGES:", "    if concurrency < 1:"),
    ("K22", False, "staging planted on a job range is not refused",
     "    if shared:\n        raise Refusal(f\"replay slot {slot}'s CPU ranges overlap",
     "    if False:\n        raise Refusal(f\"replay slot {slot}'s CPU ranges overlap"),
    ("K23", False, "a CPU-range problem fails the run's verdict",
     "        report_job_cpu_ranges(workflow, moved)\n        observed_volumes",
     "        report_job_cpu_ranges(workflow, moved)\n        if moved.problems:\n            return RC_FAILED\n        observed_volumes"),
    ("K24", False, "the run prints no CPU-range summary or warnings",
     "        report_job_cpu_ranges(workflow, moved)\n        observed_volumes",
     "        observed_volumes"),
    ("K25", False, "the record moves containers it does not own",
     "        if attributes.get(DOCKER_OWNER_LABEL) != self.boundary.token:",
     "        if False:"),
    ("K26", False, "the event stream is not filtered to the boundary's label",
     '        f"label={DOCKER_OWNER_LABEL}={boundary.token}",\n        *(word',
     '        *(word'),
    ("K27", False, "a start whose create was never read is not placed",
     '            if action in ("create", "start"):', '            if action == "create":'),
    ("K28", False, "execute_workflows never hands the monitor its ranges",
     "            boundary, plan.cpu_ranges, context=context\n        ) as moved:",
     "            boundary, (), context=context\n        ) as moved:"),
    ("K29", False, "stop runs with cleanup signals unblocked",
     "    with blocked_cleanup_signals():\n        try:\n            ended_early",
     "    with contextlib.nullcontext():\n        try:\n            ended_early"),
    ("K30", False, "a late update event is not re-read",
     '            action == "start" or (action == "update" and known == "moving")',
     '            action == "start"'),
    ("K31", False, "a reader crash is not recorded as a problem",
     '        record.problems.append(f"the CPU-range monitor stopped reading events: {exc}")',
     "        pass"),
    ("K32", False, "the event stream replays from an hour in the future (sees nothing)",
     "        str(int(time.time()) - 1),", "        str(int(time.time()) + 3600),"),
    ("K33", False, "inspect equality not required: any answer counts as moved",
     "        elif cpus == target:", "        elif True:"),
    ("K34", False, "the events stream is not in its own session",
     "                    stderr=subprocess.DEVNULL,\n                    start_new_session=True,",
     "                    stderr=subprocess.DEVNULL,\n                    start_new_session=False,"),
    ("K35", False, "a gone container (No such container on update) is not released",
     '                if "No such container" in (result.stderr or ""):\n                    self.release(container_id)\n                    return',
     '                if "No such container" in (result.stderr or ""):\n                    return'),
    ("K36", False, "stop raises the last failure instead of the first",
     "    if failures:\n        raise failures[0]", "    if failures:\n        raise failures[-1]"),
]


def run_one(mutant: tuple[str, bool, str, str, str]) -> str:
    ident, probe, what, old, new = mutant
    tree = PACKET / "scratch" / "mut" / ident
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(PRISTINE, tree, copy_function=lambda s, d: __import__("os").link(s, d))
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        return f"{ident} ANCHOR x{count} - {what}"
    target.unlink()
    target.write_text(text.replace(old, new), encoding="utf-8")
    result = subprocess.run(
        [str(SANDBOX), str(tree), "python3", "-I", "scripts/act_ci.py", "--selftest"],
        capture_output=True, text=True, timeout=900,
    )
    fails = [line.strip() for line in result.stdout.splitlines() if line.startswith("  FAIL")]
    verdict = "KILLED" if result.returncode != 0 else "SURVIVED"
    line = f"{ident} {verdict} rc={result.returncode} fails={len(fails)} - {what}"
    if fails:
        line += f"\n    first: {fails[0][:200]}"
    elif result.returncode != 0:
        line += f"\n    tail: {(result.stdout + result.stderr).strip().splitlines()[-1][:200]}"
    if probe:
        shutil.copy(PROBE, tree / ".probe_r2.py")
        presult = subprocess.run(
            [str(SANDBOX), str(tree), "python3", "-I", ".probe_r2.py", ".", "400"],
            capture_output=True, text=True, timeout=900,
        )
        pfails = [l for l in presult.stdout.splitlines() if l.startswith("FAIL")]
        line += f"\n    probe rc={presult.returncode}: " + ("; ".join(l.split(":")[0] for l in pfails) or "all PASS")
    shutil.rmtree(tree)
    return line


def main() -> int:
    with concurrent.futures.ThreadPoolExecutor(JOBS) as pool:
        results = list(pool.map(run_one, MUTANTS))
    for line in results:
        print(line)
    killed = sum(1 for line in results if " KILLED " in line)
    survived = [line.split()[0] for line in results if " SURVIVED " in line]
    anchors = [line.split()[0] for line in results if " ANCHOR " in line]
    print(f"mutants: {len(results)}, killed {killed}, survived {survived}, bad anchors {anchors}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
