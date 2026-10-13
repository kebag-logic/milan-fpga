"""R632-5 mutation campaign for PR #731 round 5: each mutant of the signal-mask code must fail the self-test.

Usage: python3 -I mutants_r632_5.py <packet-dir> <pristine-tree> [--jobs N]

For each mutant: hard-link copy <pristine-tree> to <packet>/scratch/mut5/<id>,
replace scripts/act_ci.py with the mutated text (the anchor must occur exactly
once), then run `act_ci.py --selftest` through <packet>/scripts/sandbox.sh (no
network, no Docker socket). Prints one line per mutant, its failing arms, and
a tally.
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

MUTANTS = [
    ("V01", "the monitor's outer hold is never taken",
     "        signal.pthread_sigmask(signal.SIG_BLOCK, held)\n        reader = threading.Thread(",
     "        pass\n        reader = threading.Thread("),
    ("V02", "a held signal is swallowed when no failure is propagating",
     "                if primary is None:\n                    raise\n",
     "                if primary is None:\n                    pass\n"),
    ("V03", "a held signal replaces a body failure already propagating",
     "                if primary is None:\n                    raise\n",
     "                raise\n"),
    ("V04", "the mask is released before the cleanup runs",
     "        failure: BaseException | None = None\n        try:\n            yield\n",
     "        failure: BaseException | None = None\n        signal.pthread_sigmask(signal.SIG_SETMASK, released)\n        try:\n            yield\n"),
    ("V05", "the release restores the held mask (never released)",
     "                signal.pthread_sigmask(signal.SIG_SETMASK, released)\n            except BaseException as delivered:",
     "                signal.pthread_sigmask(signal.SIG_BLOCK, ())\n            except BaseException as delivered:"),
    ("V06", "act's boundary does not reopen the cleanup signals",
     "    try:\n        signal.pthread_sigmask(signal.SIG_UNBLOCK, CLEANUP_SIGNALS)\n        require_live_pull_request(run.pr",
     "    try:\n        require_live_pull_request(run.pr"),
    ("V07", "act's boundary does not restore the hold",
     "        return result.returncode\n    finally:\n        signal.pthread_sigmask(signal.SIG_SETMASK, held)\n",
     "        return result.returncode\n    finally:\n        pass\n"),
    ("V08", "the live interrupt probe does not reopen the cleanup signals",
     "            signal.pthread_sigmask(signal.SIG_UNBLOCK, CLEANUP_SIGNALS)\n            require_act_job_volumes_absent(",
     "            require_act_job_volumes_absent("),
    ("V09", "the live interrupt probe does not restore the hold",
     "            )\n        finally:\n            signal.pthread_sigmask(signal.SIG_SETMASK, held)\n    except (KeyboardInterrupt, TerminationRequest) as exc:",
     "            )\n        finally:\n            pass\n    except (KeyboardInterrupt, TerminationRequest) as exc:"),
    ("V10", "the reader is started unmasked (outer hold dropped for its start)",
     "        start_cleanup_thread_or_refuse(reader, \"CPU-range monitor\")\n        yield record",
     "        _m = signal.pthread_sigmask(signal.SIG_UNBLOCK, CLEANUP_SIGNALS)\n        reader.start()\n        signal.pthread_sigmask(signal.SIG_SETMASK, _m)\n        yield record"),
    ("V11", "the signal diagnostic beside a kept failure is not printed",
     "                    if beside is delivered:\n                        print(",
     "                    if beside is delivered and False:\n                        print("),
    ("V12", "a cleanup failure displaced by a held signal is not printed",
     "                    elif beside is not None:\n                        print(",
     "                    elif beside is not None and False:\n                        print("),
]


def run_one(mutant: tuple[str, str, str, str]) -> str:
    ident, what, old, new = mutant
    tree = PACKET / "scratch" / "mut5" / ident
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
    try:
        result = subprocess.run(
            [str(SANDBOX), str(tree), "timeout", "600", "python3", "-I", "scripts/act_ci.py", "--selftest"],
            capture_output=True, text=True, timeout=660,
        )
        rc, out = result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        rc, out = -1, "driver timeout"
    fails = [line.strip() for line in out.splitlines() if line.startswith("  FAIL")]
    verdict = "KILLED" if rc != 0 else "SURVIVED"
    line = f"{ident} {verdict} rc={rc} fails={len(fails)} - {what}"
    for each in fails:
        line += f"\n    {each[:220]}"
    if not fails and rc != 0:
        line += f"\n    tail: {out.strip().splitlines()[-1][:220] if out.strip() else ''}"
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
