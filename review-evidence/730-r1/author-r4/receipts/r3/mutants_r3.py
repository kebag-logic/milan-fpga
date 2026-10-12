"""Plant one Round 3 defect per copy of scripts/act_ci.py and report which ones `--selftest` catches.

Usage: python3 -I mutants_r3.py <tree> <scratch dir> <jobs>
<tree> is an extracted tree holding the candidate scripts/act_ci.py; it is never modified.
"""
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys

MUTANTS = {
    "N22_primary_not_passed_to_stop": (
        "                process, reader, record, context=context, seams=seams, primary=primary\n",
        "                process, reader, record, context=context, seams=seams, primary=None\n",
    ),
    "N23_primary_ignored_by_stop": (
        "    if primary is not None:\n        return\n",
        "    if False:\n        return\n",
    ),
    "N24_cleanup_failure_not_printed": (
        "        for later in failures if primary is not None else failures[1:]:\n",
        "        for later in ():\n",
    ),
    "N25_raised_failure_printed_too": (
        "        for later in failures if primary is not None else failures[1:]:\n",
        "        for later in failures:\n",
    ),
    "N26_only_a_signal_is_kept": (
        "    except BaseException as exc:\n        primary = exc\n        raise\n",
        "    except TerminationRequest as exc:\n        primary = exc\n        raise\n",
    ),
    "N27_a_signal_is_not_kept": (
        "    except BaseException as exc:\n        primary = exc\n        raise\n",
        "    except Exception as exc:\n        primary = exc\n        raise\n",
    ),
    "N28_hold_not_printed": (
        "                    file=sys.stderr,\n                    flush=True,\n                )\n            except Exception:\n"
        "                # Diagnostics have no authority to release containment.\n",
        "                    file=io.StringIO(),\n                    flush=True,\n                )\n            except Exception:\n"
        "                # Diagnostics have no authority to release containment.\n",
    ),
    "N29_hold_not_recorded": (
        '            record.problems.append("the CPU-range monitor survived its bounded shutdown")\n',
        "            pass\n",
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
