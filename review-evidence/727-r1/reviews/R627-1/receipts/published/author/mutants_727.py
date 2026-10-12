#!/usr/bin/env python3
"""Lane 727 mutation evidence for scripts/suite_shards.py --selftest.

usage: python3 -I mutants_727.py REPO SCRATCH

Builds one structure-only tree per case under SCRATCH (the selector, the
workflow file, and an empty Makefile per suite directory of REPO), applies
the case's change, runs that copy's --selftest and prints its rc and the arm
lines that are not `ok`/`[ok]`. Every code mutant is an exact replacement
that must match the expected number of times, so fixture drift fails loudly.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

SELECTOR = "scripts/suite_shards.py"
WORKFLOW = ".github/workflows/rtl.yml"


def build(repo: Path, dest: Path) -> None:
    """A tree with the real selector, workflow and suite directory names."""
    (dest / "scripts").mkdir(parents=True)
    (dest / ".github/workflows").mkdir(parents=True)
    shutil.copy(repo / SELECTOR, dest / SELECTOR)
    shutil.copy(repo / WORKFLOW, dest / WORKFLOW)
    for suite in sorted((repo / "tb/verilator").iterdir()):
        if suite.is_dir() and (suite / "Makefile").is_file():
            (dest / "tb/verilator" / suite.name).mkdir(parents=True)
            (dest / "tb/verilator" / suite.name / "Makefile").touch()


def edit(path: Path, old: str, new: str, count: int = 1) -> None:
    """Replace `old` exactly `count` times."""
    text = path.read_text()
    assert text.count(old) == count, f"{path}: {old!r} found {text.count(old)}x"
    path.write_text(text.replace(old, new))


def edit_function(path: Path, name: str, old: str, new: str) -> None:
    """Replace every `old` inside one top-level function's source."""
    text = path.read_text()
    start = text.index(f"\ndef {name}(")
    end = text.index("\ndef ", start + 1)
    body = text[start:end]
    assert old in body, f"{name}: {old!r} absent"
    path.write_text(text[:start] + body.replace(old, new) + text[end:])


def m_unmeasured_free(t: Path) -> None:
    """An inventory suite with no duration is not flagged and costs 0 s."""
    edit(t / SELECTOR,
         '    problems = [f"{suite}: inventory suite with no recorded duration in "\n'
         '                "SUITE_SECONDS (refresh it as the module docstring says)"\n'
         '                for suite in suites if suite not in seconds]\n',
         "    problems = []\n")
    edit_function(t / SELECTOR, "balance", "seconds[suite]", "seconds.get(suite, 0)")


def m_stale_ignored(t: Path) -> None:
    """A recorded duration with no inventory suite is not flagged."""
    edit(t / SELECTOR,
         '    problems += [f"{suite}: SUITE_SECONDS names a suite that is not in the "\n'
         '                 "inventory" for suite in sorted(set(seconds) - inventory)]\n',
         "")


def m_timeout_mirrored(t: Path) -> None:
    """The gate uses a mirrored 120 min and 5 workers instead of reading rtl.yml."""
    edit_function(t / SELECTOR, "headroom_problems",
                  "timeout, workers = verilator_job_limits(workflow)",
                  "timeout, workers = 120, 5")


def m_block_unbounded(t: Path) -> None:
    """The Verilator job's block runs on into the jobs after it."""
    edit(t / SELECTOR,
         "        if line.strip() and not line.startswith(\"   \") \\\n"
         "                and not line.lstrip().startswith(\"#\"):\n"
         "            break\n",
         "")


def m_overhead_dropped(t: Path) -> None:
    """The prediction leaves out each worker's measured overhead."""
    edit(t / SELECTOR,
         "    load = list(overhead) if layout else [0] * total\n",
         "    load = [0] * total\n")


def m_mean_only(t: Path) -> None:
    """Only the mean worker is held to the bound."""
    edit(t / SELECTOR,
         "for worker, value in enumerate(load) if value > bound]",
         "for worker, value in enumerate(load) if sum(load) / len(load) > bound]")


def m_at_bound_refused(t: Path) -> None:
    """A worker exactly at the bound is refused (> became >=)."""
    edit(t / SELECTOR,
         "for worker, value in enumerate(load) if value > bound]",
         "for worker, value in enumerate(load) if value >= bound]")


def m_pin_dropped(t: Path) -> None:
    """chmap_capture is no longer pinned to the Yosys/sv2v worker."""
    edit(t / SELECTOR, 'PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}',
         'PINNED_SUITES = {"tsn_fuzz": 1}')


def m_tsn_pin_dropped(t: Path) -> None:
    """tsn_fuzz is no longer pinned to the tsn-gen worker."""
    edit(t / SELECTOR, 'PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}',
         'PINNED_SUITES = {"chmap_capture": 3}')


def m_tsn_pin_moved(t: Path) -> None:
    """tsn_fuzz is pinned to worker 2, where tsn-gen is not built."""
    edit(t / SELECTOR, 'PINNED_SUITES = {"tsn_fuzz": 1, "chmap_capture": 3}',
         'PINNED_SUITES = {"tsn_fuzz": 2, "chmap_capture": 3}')


def m_measure_from_job_start(t: Path) -> None:
    """--measure starts a worker's first suite at the job, setup included."""
    edit(t / SELECTOR, "    windows, previous = {}, start\n",
         "    windows, previous = {}, first\n")


def t_unmeasured_suite(t: Path) -> None:
    """The tree gains a suite directory that the table does not name."""
    (t / "tb/verilator/new_unmeasured").mkdir()
    (t / "tb/verilator/new_unmeasured/Makefile").touch()


def t_suite_removed(t: Path) -> None:
    """A measured suite leaves the inventory (no Makefile) while its duration stays."""
    (t / "tb/verilator/pcmlpf/Makefile").rename(t / "tb/verilator/pcmlpf/Makefile.gone")


def t_heavy_entry(t: Path) -> None:
    """One real table entry grows by 500 s (gptp_plane 784 s to 1284 s)."""
    edit(t / SELECTOR, '    "gptp_plane": 784,\n', '    "gptp_plane": 1284,\n')


def t_timeout_lowered(t: Path) -> None:
    """rtl.yml lowers the Verilator job to 116 minutes (bound 4176 s)."""
    text = (t / WORKFLOW).read_text()
    start = text.index("\n  verilator-shards:\n")
    at = text.index("    timeout-minutes: 120\n", start)
    (t / WORKFLOW).write_text(text[:at] + "    timeout-minutes: 116\n"
                              + text[at + len("    timeout-minutes: 120\n"):])


def t_worker_count(t: Path) -> None:
    """rtl.yml grows to six workers while the overhead table has five."""
    edit(t / WORKFLOW, "        shard: [0, 1, 2, 3, 4]\n        total: [5]\n",
         "        shard: [0, 1, 2, 3, 4, 5]\n        total: [6]\n")


def t_workflow_missing(t: Path) -> None:
    """The tree has no rtl.yml to read."""
    (t / WORKFLOW).rename(t / (WORKFLOW + ".gone"))


def t_renamed_copy(t: Path) -> None:
    """A renamed copy outside scripts/, as test_suite_cancellation.py runs."""
    (t / SELECTOR).rename(t / "real_selector.py")


CASES = [("control", None)] + [(f.__name__, f) for f in (
    m_unmeasured_free, m_stale_ignored, m_timeout_mirrored, m_block_unbounded,
    m_overhead_dropped, m_mean_only, m_at_bound_refused, m_pin_dropped,
    m_tsn_pin_dropped, m_tsn_pin_moved, m_measure_from_job_start, t_unmeasured_suite,
    t_suite_removed, t_heavy_entry, t_timeout_lowered, t_worker_count,
    t_workflow_missing, t_renamed_copy)]


def main(argv: list[str]) -> int:
    """Run every case; 0 when each behaves as recorded in HANDOFF.md."""
    repo, scratch = Path(argv[1]).resolve(), Path(argv[2]).resolve()
    scratch.mkdir(parents=True, exist_ok=False)
    for name, change in CASES:
        tree = scratch / name
        build(repo, tree)
        if change is not None:
            change(tree)
        script = tree / ("real_selector.py" if name == "t_renamed_copy" else SELECTOR)
        run = subprocess.run([sys.executable, "-I", str(script), "--selftest"],
                             capture_output=True, text=True, cwd=scratch)
        lines = run.stdout.splitlines()
        odd = [line.strip() for line in lines
               if not re.match(r"\s+(ok |\[ok\])", line)]
        doc = change.__doc__ if change else "unmodified copy of the head"
        print(f"== {name}: {doc}")
        print(f"   rc={run.returncode}")
        for line in odd:
            print(f"   {line}")
        if run.stderr.strip():
            print("   stderr: " + run.stderr.strip().splitlines()[-1])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
