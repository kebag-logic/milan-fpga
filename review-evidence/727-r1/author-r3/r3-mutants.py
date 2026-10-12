#!/usr/bin/env python3
"""Lane 727 round-3 mutation evidence for scripts/suite_shards.py --selftest.

usage: python3 -I r3-mutants.py REPO SCRATCH

Builds one structure-only tree per case under SCRATCH (the selector, the
workflow file, the sweep driver, and an empty Makefile per suite directory
of REPO), applies
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
DRIVER = "scripts/run_all_suites.sh"


def build(repo: Path, dest: Path) -> None:
    """A tree with the real selector, workflow, driver and suite names."""
    (dest / "scripts").mkdir(parents=True)
    (dest / ".github/workflows").mkdir(parents=True)
    shutil.copy(repo / SELECTOR, dest / SELECTOR)
    shutil.copy(repo / WORKFLOW, dest / WORKFLOW)
    shutil.copy(repo / DRIVER, dest / DRIVER)
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
    edit(t / SELECTOR, "                for suite in suites if suite not in seconds]\n",
         "                for suite in suites if False]\n")
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


def m_reader_mirrored(t: Path) -> None:
    """The driver reader returns a mirrored 1800 s default instead of the `*` arm."""
    edit(t / SELECTOR, "    return dict(arms[:-1]), arms[-1][1]\n",
         "    return dict(arms[:-1]), 1800\n")


def m_named_arms_ignored(t: Path) -> None:
    """The driver reader drops every named arm, so every suite gets the default."""
    edit(t / SELECTOR, "    return dict(arms[:-1]), arms[-1][1]\n",
         "    return {}, arms[-1][1]\n")


def m_provisional_unchecked(t: Path) -> None:
    """A provisional figure is never compared with the driver's."""
    edit(t / SELECTOR, "        elif seconds[suite] != expected:\n", "        elif False:\n")


def m_provisional_missing_ignored(t: Path) -> None:
    """A provisional name with no SUITE_SECONDS figure is let through."""
    edit(t / SELECTOR,
         '            problems.append(f"{suite}: PROVISIONAL_SUITES names a suite with no "\n'
         '                            "figure in SUITE_SECONDS")\n',
         "            pass\n")


def m_head_provisional_skipped(t: Path) -> None:
    """The head arm never checks this tree's own provisional figures; plants aaf as
    provisional at its measured 73 s, which the driver's 1800 s default refuses."""
    edit(t / SELECTOR, "        provisional = provisional_problems(driver)\n",
         "        provisional = []\n")
    t_provisional_mismatch(t)


def m_in_checkout_false(t: Path) -> None:
    """in_checkout() always says no, so a checkout would skip every head arm."""
    edit(t / SELECTOR,
         '    return HERE.name == "suite_shards.py" and HERE.parent.name == "scripts"\n',
         "    return False\n")


def m_tie_by_hash(t: Path) -> None:
    """Equal durations are ordered by the process's string hash, not by name."""
    edit(t / SELECTOR, "key=lambda suite: (-seconds[suite], suite)):",
         "key=lambda suite: (-seconds[suite], hash(suite))):")


def t_provisional_mismatch(t: Path) -> None:
    """aaf is marked provisional at its measured 73 s; suite_timeout gives it 1800 s."""
    edit(t / SELECTOR, "PROVISIONAL_SUITES: frozenset[str] = frozenset()\n",
         'PROVISIONAL_SUITES: frozenset[str] = frozenset({"aaf"})\n')


def t_provisional_named_arm(t: Path) -> None:
    """milan_dp_mclk is marked provisional at its 3600 s suite_timeout arm (passes)
    after its figure is set to that arm (the balance then puts a worker over)."""
    edit(t / SELECTOR, '    "milan_dp_mclk": 2038,\n', '    "milan_dp_mclk": 3600,\n')
    edit(t / SELECTOR, "PROVISIONAL_SUITES: frozenset[str] = frozenset()\n",
         'PROVISIONAL_SUITES: frozenset[str] = frozenset({"milan_dp_mclk"})\n')


def t_new_suite(t: Path) -> None:
    """A new suite directory with no figure: the refusal must name the new-suite steps."""
    (t / "tb/verilator/zz_new_suite").mkdir()
    (t / "tb/verilator/zz_new_suite/Makefile").touch()


def t_driver_missing(t: Path) -> None:
    """The tree has no run_all_suites.sh to read."""
    (t / DRIVER).rename(t / (DRIVER + ".gone"))


def t_driver_arm_alternation(t: Path) -> None:
    """A suite_timeout arm names two suites, which the reader does not model."""
    edit(t / DRIVER, "    milan_dp_mclk)     printf", "    milan_dp_mclk|zz) printf")


def t_driver_star_not_last(t: Path) -> None:
    """A named arm follows the `*` arm, where bash can never reach it."""
    text = (t / DRIVER).read_text()
    star = "    *)                 printf '%s\\n' \"${SUITE_TIMEOUT:-1800}\" ;;\n"
    assert text.count(star) == 1, "star arm"
    (t / DRIVER).write_text(text.replace(
        star, star + "    zz_late)           printf '%s\\n' \"${SUITE_TIMEOUT:-60}\" ;;\n"))


CASES = [("control", None)] + [(f.__name__, f) for f in (
    m_unmeasured_free, m_stale_ignored, m_timeout_mirrored, m_block_unbounded,
    m_overhead_dropped, m_mean_only, m_at_bound_refused, m_pin_dropped,
    m_tsn_pin_dropped, m_tsn_pin_moved, m_measure_from_job_start, t_unmeasured_suite,
    t_suite_removed, t_heavy_entry, t_timeout_lowered, t_worker_count,
    t_workflow_missing, t_renamed_copy,
    m_reader_mirrored, m_named_arms_ignored, m_provisional_unchecked,
    m_provisional_missing_ignored, m_head_provisional_skipped, m_in_checkout_false,
    m_tie_by_hash, t_provisional_mismatch, t_provisional_named_arm, t_new_suite,
    t_driver_missing, t_driver_arm_alternation, t_driver_star_not_last)]


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
