#!/usr/bin/env python3
"""Plant one defect per copy of scripts/act_ci.py and report which ones `--selftest` catches.

Usage: mutants.py <exact-head tree> <scratch dir> <jobs>
The exact-head tree is an extracted `git archive` of the reviewed head; it is
never modified. Each mutant is a fresh copy under <scratch dir>/<name>.
"""

import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

MUTANTS = {
    "M01_slot_spacing_no_staging": (
        "return ReplaySlot(slot).number * (SLOT_JOB_RANGES + 1) * CONTAINER_CPU_LIMIT",
        "return ReplaySlot(slot).number * SLOT_JOB_RANGES * CONTAINER_CPU_LIMIT",
    ),
    "M02_job_ranges_start_on_staging": (
        "base + CONTAINER_CPU_LIMIT, last + 1, CONTAINER_CPU_LIMIT",
        "base, last + 1 - CONTAINER_CPU_LIMIT, CONTAINER_CPU_LIMIT",
    ),
    "M03_overlap_guard_removed": (
        "    if shared:\n        raise Refusal(f\"replay slot {slot}'s CPU ranges overlap",
        "    if False:\n        raise Refusal(f\"replay slot {slot}'s CPU ranges overlap",
    ),
    "M04_sum_replaced_by_max": (
        "most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
        "most = max(most, max(widths))",
    ),
    "M05_max_parallel_ignored": (
        "    return max(1, int(raw))",
        "    return ACT_DEFAULT_MAX_PARALLEL",
    ),
    "M06_expression_max_parallel_defaulted": (
        '    if not isinstance(raw, str) or re.fullmatch(r"[0-9]{1,6}", raw) is None:\n',
        '    if not isinstance(raw, str) or re.fullmatch(r"[0-9]{1,6}", raw) is None:\n'
        "        return ACT_DEFAULT_MAX_PARALLEL\n    if False:\n",
    ),
    "M07_too_wide_not_refused": (
        "    if not 1 <= concurrency <= SLOT_JOB_RANGES:",
        "    if not 1 <= concurrency:",
    ),
    "M08_no_free_on_die": (
        "            self.held.pop(container_id, None)\n",
        "            pass\n",
    ),
    "M09_held_ranges_ignored": (
        "free = [index for index in range(len(self.ranges)) if index not in taken]",
        "free = list(range(len(self.ranges)))",
    ),
    "M10_no_label_filter": (
        '        f"label={DOCKER_OWNER_LABEL}={boundary.token}",\n',
        "",
    ),
    "M11_owner_check_removed": (
        "        if attributes.get(DOCKER_OWNER_LABEL) != self.boundary.token:",
        "        if False:",
    ),
    "M12_monitor_not_stopped_on_raise": (
        "        yield record\n    finally:\n        if process is not None:\n"
        "            stop_job_cpu_range_monitor(process, reader, record, context=context, seams=seams)",
        "        yield record\n"
        "        stop_job_cpu_range_monitor(process, reader, record, context=context, seams=seams)\n"
        "    finally:\n        pass",
    ),
    "M13_reader_not_joined": (
        "        if reader is not None and reader.ident is not None:",
        "        if False:",
    ),
    "M14_act_outside_monitor": (
        "        ) as moved:\n            result = execute_act_boundary(\n",
        "        ) as moved:\n            pass\n        if True:\n            result = execute_act_boundary(\n",
    ),
    "M15_plan_without_ranges": (
        "                cpu_ranges=cpu_ranges,\n",
        "                cpu_ranges=(),\n",
    ),
    "M16_problems_fail_the_workflow": (
        "        report_job_cpu_ranges(workflow, moved)\n        observed_volumes",
        "        report_job_cpu_ranges(workflow, moved)\n        if moved.problems:\n"
        "            return RC_FAILED\n        observed_volumes",
    ),
    "M17_problems_never_printed": (
        "    for problem in record.problems:",
        "    for problem in ():",
    ),
    "M18_interrupt_move_not_required": (
        "        if cpu_ranges and (moved.moved < 1 or moved.problems):",
        "        if False:",
    ),
    "M19_ended_early_not_reported": (
        "        if ended_early:",
        "        if False:",
    ),
    "M20_slot0_small_host_refused": (
        "        if ReplaySlot(slot).number == 0:\n            return ()",
        "        if False:\n            return ()",
    ),
    "M21_range_three_wide": (
        'f"{first}-{first + CONTAINER_CPU_LIMIT - 1}"\n        for first in range(',
        'f"{first}-{first + CONTAINER_CPU_LIMIT - 2}"\n        for first in range(',
    ),
    "M22_ranges_checked_after_slot_entry": (
        "        concurrency = replay_container_concurrency(layout.checkout, workflows)\n"
        "        cpu_ranges = job_cpu_ranges(slot.number, concurrency)\n",
        "        concurrency = replay_container_concurrency(layout.checkout, workflows)\n"
        "        cpu_ranges = ()\n",
    ),
    "M23_report_skipped": (
        "        report_job_cpu_ranges(workflow, moved)\n        observed_volumes",
        "        observed_volumes",
    ),
    "C24_free_on_destroy_only_control": (
        "        else:\n            self.held.pop(container_id, None)\n",
        "        elif action == \"destroy\":\n            self.held.pop(container_id, None)\n",
    ),
}


def run_one(tree: pathlib.Path, scratch: pathlib.Path, name: str) -> tuple[str, int, int, str]:
    old, new = MUTANTS[name]
    target = scratch / name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(tree, target, symlinks=True)
    path = target / "scripts" / "act_ci.py"
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        return name, -1, count, "anchor not unique"
    path.write_text(text.replace(old, new), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-I", "scripts/act_ci.py", "--selftest"],
        cwd=target,
        capture_output=True,
        text=True,
        timeout=900,
    )
    out = result.stdout + result.stderr
    (scratch / f"{name}.log").write_text(out, encoding="utf-8")
    failed = [line.strip() for line in out.splitlines() if line.lstrip().startswith("FAIL")]
    shutil.rmtree(target)
    return name, result.returncode, len(failed), (failed[0][:160] if failed else out.strip().splitlines()[-1][:160])


def main() -> int:
    tree, scratch, jobs = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), int(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda name: run_one(tree, scratch, name), MUTANTS))
    for name, rc, failed, first in results:
        verdict = "KILLED" if rc != 0 else "SURVIVED"
        if rc == -1:
            verdict = "INVALID"
        print(f"{name}\t{verdict}\trc={rc}\tfail_arms={failed}\t{first}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
