"""Reviewer mutation campaign for PR #731 round 3: each mutant must fail the runner's self-test.

Usage: python3 -I mutants_r3.py <packet-dir> <pristine-tree> [--jobs N]

For each mutant: hard-link copy <pristine-tree> to <packet>/scratch/mut3/<id>,
replace scripts/act_ci.py with the mutated text (the anchor must occur exactly
once), then run `act_ci.py --selftest` through <packet>/scripts/sandbox.sh (no
network, no Docker socket). Prints one line per mutant with every failing arm,
and a tally. A SURVIVED mutant names behaviour no self-test arm pins.
"""

from __future__ import annotations

import concurrent.futures
import os
import pathlib
import shutil
import subprocess
import sys

PACKET = pathlib.Path(sys.argv[1]).resolve()
PRISTINE = pathlib.Path(sys.argv[2]).resolve()
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 8
SANDBOX = PACKET / "scripts" / "sandbox.sh"

MUTANTS: list[tuple[str, str, str, str]] = [
    # --- round-3 delta: first failure wins ---
    ("Q01", "primary never recorded: a cleanup failure replaces an interrupt or body failure",
     "    except BaseException as exc:\n        primary = exc\n        raise",
     "    except BaseException as exc:\n        raise"),
    ("Q02", "with a primary, the first cleanup failure is not printed beside it",
     "        for later in failures if primary is not None else failures[1:]:",
     "        for later in failures[1:]:"),
    ("Q03", "with a primary, the first cleanup failure is raised in its place",
     "    if primary is not None:\n        return\n    if failures:\n        raise failures[0]",
     "    if failures:\n        raise failures[0]"),
    ("Q04", "with no primary, the raised cleanup failure is also printed",
     "        for later in failures if primary is not None else failures[1:]:",
     "        for later in failures:"),
    ("Q05", "cleanup failures printed on stdout, not stderr",
     "                    f\"act-ci: CPU-range monitor cleanup also failed: {type(later).__name__}: {later}\",\n                    file=sys.stderr,",
     "                    f\"act-ci: CPU-range monitor cleanup also failed: {type(later).__name__}: {later}\",\n                    file=sys.stdout,"),
    ("Q06", "a failure closing the event pipe is swallowed",
     "                process.stdout.close()\n        except Exception as exc:\n            failures.append(exc)",
     "                process.stdout.close()\n        except Exception as exc:\n            pass"),
    ("Q07", "a poll failure is not recorded as a problem",
     "            record.problems.append(f\"cannot tell whether the Docker event stream ended early: {exc}\")",
     "            pass"),
    ("Q08", "an early-ended stream is not reported",
     "        if ended_early:\n            record.problems.append(",
     "        if False:\n            record.problems.append("),
    # --- record / allocation ---
    ("Q09", "a removed container that had moved is counted as removed before its move",
     "        if self.outcome.get(container_id) == \"moving\":\n            self.outcome[container_id] = \"gone\"",
     "        if self.outcome.get(container_id) in (\"moving\", \"moved\"):\n            self.outcome[container_id] = \"gone\""),
    ("Q10", "the peak number of held ranges is never raised",
     "        self.most_at_once = max(self.most_at_once, len(self.held))",
     "        self.most_at_once = self.most_at_once"),
    ("Q11", "a container left without a range is not marked staging",
     "            self.outcome[container_id] = \"staging\"",
     "            self.outcome[container_id] = \"moving\""),
    ("Q12", "an inspect saying No such container is a Refusal (a gone holder never frees its range)",
     "        if \"No such container\" in (result.stderr or \"\"):\n            return None\n        detail = (result.stderr or \"\").strip().splitlines()\n        raise Refusal(\"docker container inspect failed\"",
     "        detail = (result.stderr or \"\").strip().splitlines()\n        raise Refusal(\"docker container inspect failed\""),
    ("Q13", "an off-target read of a moved container is not warned",
     "        elif moved_now or self.outcome[container_id] == \"moved\":",
     "        elif moved_now:"),
    ("Q14", "a move reported failed but seen on target is not warned",
     "            if failure:\n                self.problems.append(\n                    f\"the move of job container {short} to {target} reported {failure}, \"",
     "            if False:\n                self.problems.append(\n                    f\"the move of job container {short} to {target} reported {failure}, \""),
    ("Q15", "a destroy of an unknown container is placed",
     "        if action == \"destroy\":\n            self.release(container_id)",
     "        if action == \"destroy\" and known is not None:\n            self.release(container_id)"),
    ("Q16", "a container's ID shape is not checked",
     "            or not DOCKER_ID_RE.fullmatch(container_id)\n",
     ""),
    ("Q17", "the free list picks the highest free range",
     "        return [index for index in range(len(self.ranges)) if index not in taken]",
     "        return [index for index in reversed(range(len(self.ranges))) if index not in taken]"),
    # --- derivation ---
    ("Q18", "a strategy without a matrix counts as act's default width",
     "    if \"matrix\" not in strategy:\n        return 1",
     "    if \"matrix\" not in strategy:\n        return ACT_DEFAULT_MAX_PARALLEL"),
    ("Q19", "max-parallel 0 is not raised to act's floor of one",
     "    return max(1, int(raw))",
     "    return int(raw)"),
    ("Q20", "an unbounded digit string is accepted",
     "re.fullmatch(r\"[0-9]{1,6}\", raw)",
     "re.fullmatch(r\"[0-9]+\", raw)"),
    ("Q21", "a non-mapping strategy is read as no strategy",
     "    if not isinstance(strategy, dict):\n        raise Refusal(",
     "    if not isinstance(strategy, dict):\n        return 1\n        raise Refusal("),
    ("Q22", "a job without a strategy runs act's default width",
     "    strategy = job.get(\"strategy\")\n    if strategy is None:\n        return 1",
     "    strategy = job.get(\"strategy\")\n    if strategy is None:\n        return ACT_DEFAULT_MAX_PARALLEL"),
    ("Q23", "a workflow's concurrency is its widest job only, ignoring CONCURRENT_JOB_LIMIT",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
     "        most = max(most, widths[0])"),
    ("Q24", "a replay's concurrency is the last workflow's, not the most",
     "        most = max(most, sum(widths[:CONCURRENT_JOB_LIMIT]))",
     "        most = sum(widths[:CONCURRENT_JOB_LIMIT])"),
    # --- layout / plan ---
    ("Q25", "the plan line names slot 0's staging range on every slot",
     "        f\"CONCURRENT_JOB_LIMIT {CONCURRENT_JOB_LIMIT}); each created on \"\n        f\"--cpuset-cpus={container_cpuset(slot)}, then",
     "        f\"CONCURRENT_JOB_LIMIT {CONCURRENT_JOB_LIMIT}); each created on \"\n        f\"--cpuset-cpus={container_cpuset(0)}, then"),
    ("Q26", "the overlap check never reports a shared CPU",
     "                shared.append(f\"{holders[cpu]} and {owner} share CPU {cpu}\")",
     "                pass"),
    ("Q27", "the monitor starts its stream even with no ranges",
     "    if not ranges:\n        yield record\n        return\n    command = [",
     "    command = ["),
    ("Q28", "the events stream's stderr is a pipe nobody reads",
     "                    stderr=subprocess.DEVNULL,\n                    start_new_session=True,\n                )\n        except OSError as exc:\n            raise Refusal(f\"cannot start the CPU-range monitor",
     "                    stderr=subprocess.PIPE,\n                    start_new_session=True,\n                )\n        except OSError as exc:\n            raise Refusal(f\"cannot start the CPU-range monitor"),
    ("Q29", "the derivation reads the trusted runner's workflows, not the materialized checkout",
     "        concurrency = replay_container_concurrency(layout.checkout, workflows)",
     "        concurrency = replay_container_concurrency(ROOT, workflows)"),
    ("Q30", "a reader's own failure stops the run instead of being recorded",
     "    except Exception as exc:\n        record.problems.append(f\"the CPU-range monitor stopped reading events: {exc}\")",
     "    except Exception as exc:\n        raise"),
]


def run_one(mutant: tuple[str, str, str, str]) -> str:
    ident, what, old, new = mutant
    tree = PACKET / "scratch" / "mut3" / ident
    if tree.exists():
        shutil.rmtree(tree)
    shutil.copytree(PRISTINE, tree, copy_function=os.link)
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        shutil.rmtree(tree)
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
    for each in fails:
        line += f"\n    {each[:220]}"
    if not fails and result.returncode != 0:
        line += f"\n    tail: {(result.stdout + result.stderr).strip().splitlines()[-1][:220]}"
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
    raise SystemExit(main())
