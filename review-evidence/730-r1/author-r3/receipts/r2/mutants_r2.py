"""Plant one Round 2 defect per copy of scripts/act_ci.py and report which ones `--selftest` catches.

Usage: python3 -I mutants_r2.py <tree> <scratch dir> <jobs>
<tree> is an extracted tree holding the candidate scripts/act_ci.py; it is never modified.
"""
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

MUTANTS = {
    "N01_die_frees_its_range": (
        '        if action == "destroy":\n            self.release(container_id)',
        '        if action in ("destroy", "die"):\n            self.release(container_id)',
    ),
    "N02_timed_out_move_released": (
        "        except Refusal as exc:\n            failure = str(exc)\n",
        "        except Refusal as exc:\n            self.release(container_id)\n            return\n",
    ),
    "N03_refused_move_released": (
        '                failure = detail[-1] if detail else f"exit status {result.returncode}"\n',
        "                self.release(container_id)\n                return\n",
    ),
    "N04_no_inspect_when_full": (
        "            for holder in list(self.held):\n                self.check(holder)\n",
        "            pass\n",
    ),
    "N05_move_trusted_without_inspect": (
        "        self.check(container_id, moved_now=True, failure=failure)\n",
        '        self.outcome[container_id] = "moved"\n',
    ),
    "N06_start_not_inspected": (
        '            action == "start" or (action == "update" and known == "moving")\n',
        '            action == "update" and known == "moving"\n',
    ),
    "N07_late_update_not_inspected": (
        '            action == "start" or (action == "update" and known == "moving")\n',
        '            action == "start"\n',
    ),
    "N08_reap_failure_skips_join": (
        "        except BaseException as exc:\n            failures.append(exc)\n        if reader is not None",
        "        except BaseException as exc:\n            raise\n        if reader is not None",
    ),
    "N09_join_failure_not_retried": (
        "            failure = failure or exc\n            time.sleep(0.25)\n",
        "            return exc\n",
    ),
    "N10_slot0_fallback_restored": (
        "    if last >= host_cpus:\n        raise Refusal(\n            f\"replay slot {slot} needs CPUs {base}-{last}",
        "    if last >= host_cpus:\n        if ReplaySlot(slot).number == 0:\n            return ()\n"
        "        raise Refusal(\n            f\"replay slot {slot} needs CPUs {base}-{last}",
    ),
    "N11_start_without_create_ignored": (
        '            if action in ("create", "start"):\n',
        '            if action == "create":\n',
    ),
    "N12_cleanup_failure_swallowed": (
        "    if failures:\n        raise failures[0]\n",
        "    if False:\n        raise failures[0]\n",
    ),
    "N13_poll_failure_unguarded": (
        "        try:\n            ended_early = process.poll() is not None\n        except Exception as exc:\n"
        "            ended_early = False\n",
        "        if True:\n            ended_early = process.poll() is not None\n        if False:\n"
        "            ended_early = False\n",
    ),
    "N14_join_before_containment": (
        "        try:\n            seams.terminate_group(\n",
        "        if reader is not None and reader.ident is not None:\n"
        "            join_job_cpu_reader(reader, record, process.pid)\n"
        "        try:\n            seams.terminate_group(\n",
    ),
    "N15_reserved_counts_as_moved": (
        '        return sum(1 for each in self.outcome.values() if each == "moved")\n',
        '        return sum(1 for each in self.outcome.values() if each in ("moved", "moving"))\n',
    ),
    "N16_gone_not_counted": (
        '        if self.outcome.get(container_id) == "moving":\n            self.outcome[container_id] = "gone"\n',
        "        pass\n",
    ),
    "N17_mismatch_not_reported": (
        "        elif moved_now or self.outcome[container_id] == \"moved\":\n",
        "        elif False:\n",
    ),
    "N18_pipe_left_open_after_failure": (
        "        try:\n            if process.stdout is not None:\n                process.stdout.close()\n"
        "        except Exception as exc:\n            failures.append(exc)\n",
        "        if not failures and process.stdout is not None:\n            process.stdout.close()\n",
    ),
    "N19_hosted_cpu_count_unpinned": (
        "    with mock.patch.multiple(sys.modules[__name__], **fakes), mock.patch.object(\n"
        "        os, \"cpu_count\", return_value=128\n",
        "    with mock.patch.multiple(sys.modules[__name__], **fakes), mock.patch.object(\n"
        "        os, \"cpu_count\", return_value=4\n",
    ),
    "N21_held_ranges_ignored": (
        "        return [index for index in range(len(self.ranges)) if index not in taken]\n",
        "        return list(range(len(self.ranges)))\n",
    ),
    "N20_planted_exit_ignored": (
        "        spawn_boundary(command, **kwargs)\n        return planted.act_returncode\n",
        "        return spawn_boundary(command, **kwargs)\n",
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
        shutil.rmtree(target)
        return name, -1, count, "anchor not unique"
    path.write_text(text.replace(old, new), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-I", "scripts/act_ci.py", "--selftest"],
        cwd=target, capture_output=True, text=True, timeout=900,
    )
    out = result.stdout + result.stderr
    (scratch / f"{name}.log").write_text(out, encoding="utf-8")
    failed = [line.strip() for line in out.splitlines() if line.lstrip().startswith("FAIL")]
    shutil.rmtree(target)
    first = failed[0] if failed else out.strip().splitlines()[-1]
    return name, result.returncode, len(failed), first[:170]


def main() -> int:
    tree, scratch, jobs = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), int(sys.argv[3])
    scratch.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda name: run_one(tree, scratch, name), MUTANTS))
    for name, rc, failed, first in results:
        verdict = "INVALID" if rc == -1 else ("KILLED" if rc != 0 else "SURVIVED")
        print(f"{name}\t{verdict}\trc={rc}\tfail_arms={failed}\t{first}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
