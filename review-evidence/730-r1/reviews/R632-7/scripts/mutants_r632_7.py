#!/usr/bin/env python3
"""Reviewer mutation set R632-7 for PR #731 at b341e875: gaps the earlier campaigns did not target.

Usage: python3 -I mutants_r632_7.py <packet> <pristine-tree> [--jobs N] [--only ID,ID]

Each mutant applies one or more exact-once anchor replacements to
scripts/act_ci.py of a copy under <packet>/scratch/mut7/<id>, then runs
`act_ci.py --selftest` through <packet>/scripts/sandbox.sh (no network, no
Docker socket, read-only system). A mutant marked with probes also runs the
reviewer probes (probe_r632_7_lifecycle.py with 60 seeds per mode,
probe_r632_7_derivation.py) on the mutated tree. KILLED means the self-test
exited non-zero; the probe columns say whether a probe failed it.
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
PROBES = ("probe_r632_7_lifecycle.py", "probe_r632_7_derivation.py")

DERIVE = (
    "        concurrency = replay_container_concurrency(layout.checkout, workflows)\n"
    "        cpu_ranges = job_cpu_ranges(slot.number, concurrency)\n"
)
SLOT_ENTRY = "        with replay_slot(slot, context=context, scratch=layout.temporary):\n            prefix = (\n"

MUTANTS: tuple[tuple[str, str, tuple[tuple[str, str], ...], bool], ...] = (
    ("T01", "the derivation and the host check run after the slot is entered",
     ((DERIVE, ""), (SLOT_ENTRY, SLOT_ENTRY.split("\n")[0] + "\n" + DERIVE.replace("        ", "            ") + "            prefix = (\n")), True),
    ("T02", "the live interrupt probe no longer requires the container's move",
     (("        if cpu_ranges and (moved.moved < 1 or moved.problems):\n", "        if False:\n"),), False),
    ("T03", "the monitor prints the 'cleanup was interrupted' line for a signal with no earlier failure",
     (("                beside = delivered if primary is not None else failure\n",
       "                beside = delivered\n"),), False),
    ("T04", "a signal held through the monitor's cleanup is swallowed when nothing else propagates",
     (("                if primary is None:\n                    raise\n\n\n@dataclass\nclass _CleanupSignalLatch",
       "                pass\n\n\n@dataclass\nclass _CleanupSignalLatch"),), False),
    ("T05", "the monitor does not hold the cleanup signals across its body",
     (("        signal.pthread_sigmask(signal.SIG_BLOCK, held)\n        reader = threading.Thread(",
       "        reader = threading.Thread("),), False),
    ("T06", "the run's CPU-range report is read inside the monitor, before its reader is joined",
     (("            )\n        report_job_cpu_ranges(workflow, moved)\n        observed_volumes",
       "            )\n            report_job_cpu_ranges(workflow, moved)\n        observed_volumes"),), False),
    ("T07", "the monitor stops reading destroy events",
     (('JOB_CPU_RANGE_EVENTS = ("create", "update", "start", "die", "destroy")',
       'JOB_CPU_RANGE_EVENTS = ("create", "update", "start", "die")'),), True),
    ("T08", "the monitor's cleanup never restores the incoming mask (held signals never delivered)",
     (("            try:\n                signal.pthread_sigmask(signal.SIG_SETMASK, released)\n",
       "            try:\n                signal.pthread_sigmask(signal.SIG_BLOCK, ())\n"),), False),
    ("T09", "the derivation reads the trusted runner's workflows, not the PR checkout",
     (("        concurrency = replay_container_concurrency(layout.checkout, workflows)\n",
       "        concurrency = replay_container_concurrency(ROOT, workflows)\n"),), True),
    ("L1", "probe validity: a die frees the range",
     (('        if action == "destroy":\n            self.release(container_id)\n',
       '        if action in ("destroy", "die"):\n            self.release(container_id)\n'),), True),
    ("L2", "probe validity: an inspect that times out frees the range",
     (("            self.problems.append(\n                f\"cannot read job container {short}'s CPUs{after}: {exc}; \"\n",
       "            self.release(container_id)\n            self.problems.append(\n                f\"cannot read job container {short}'s CPUs{after}: {exc}; \"\n"),), True),
    ("L3", "probe validity: an off-target move releases its range",
     (("        elif moved_now or self.outcome[container_id] == \"moved\":\n",
       "        elif moved_now or self.outcome[container_id] == \"moved\":\n            self.held.pop(container_id, None)\n"),), True),
    ("L4", "probe validity: a timed-out move releases its range at once",
     (("        except Refusal as exc:\n            failure = str(exc)\n",
       "        except Refusal as exc:\n            self.held.pop(container_id, None)\n            self.outcome[container_id] = \"staging\"\n            return\n"),), True),
    ("L5", "probe validity: the derivation ignores max-parallel",
     (("    return max(1, int(raw))\n", "    return ACT_DEFAULT_MAX_PARALLEL\n"),), True),
)


def sandboxed(tree: pathlib.Path, *command: str) -> tuple[int | str, str, str]:
    try:
        result = subprocess.run(
            [str(SANDBOX), str(tree), *command], capture_output=True, text=True, timeout=900,
            env={"PATH": "/usr/bin", "SANDBOX_RO": str(PACKET / "scripts")},
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "timeout", "", ""


def run(mutant: tuple[str, str, tuple[tuple[str, str], ...], bool]) -> str:
    ident, title, edits, probes = mutant
    tree = PACKET / "scratch" / "mut7" / ident
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(PRISTINE, tree, copy_function=shutil.copy)
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text()
    for old, new in edits:
        if text.count(old) != 1:
            shutil.rmtree(tree, ignore_errors=True)
            return f"{ident} BAD-ANCHOR ({text.count(old)}) {title}"
        text = text.replace(old, new)
    target.write_text(text)
    rc, out, err = sandboxed(tree, "/usr/bin/python3", "-I", "scripts/act_ci.py", "--selftest")
    fails = [line.strip() for line in out.splitlines() if line.startswith("  FAIL")]
    verdict = "KILLED" if rc != 0 else "SURVIVED"
    first = fails[0][:220] if fails else ((err.strip().splitlines() or [""])[-1][:220])
    report = f"{ident} {verdict} rc={rc} fails={len(fails)} - {title}\n    first: {first}"
    if probes:
        for probe in PROBES:
            args = [str(tree)] + (["60"] if "lifecycle" in probe else [])
            prc, pout, perr = sandboxed(tree, "/usr/bin/python3", "-I", str(PACKET / "scripts" / probe), *args)
            bad = [line.strip() for line in pout.splitlines() if line.lstrip().startswith("FAIL")]
            last = (bad[0] if bad else (pout.strip().splitlines() or perr.strip().splitlines() or [""])[-1])[:200]
            report += f"\n    {probe}: rc={prc} {'FAILED' if prc != 0 else 'passed'}: {last}"
    shutil.rmtree(tree, ignore_errors=True)
    return report


ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
if ONLY:
    MUTANTS = tuple(each for each in MUTANTS if each[0] in ONLY)
with concurrent.futures.ThreadPoolExecutor(max_workers=JOBS) as pool:
    lines = list(pool.map(run, MUTANTS))
for line in lines:
    print(line)
survived = [line.split()[0] for line in lines if " SURVIVED " in line]
bad = [line.split()[0] for line in lines if " BAD-ANCHOR " in line]
print(f"mutants: {len(lines)}, killed {len(lines) - len(survived) - len(bad)}, survived {survived}, bad anchors {bad}")
sys.exit(0)
