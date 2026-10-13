#!/usr/bin/env python3
"""Reviewer mutation set R632-6 for PR #731 round 6: the act boundary's closing signal window.

Usage: python3 -I mutants_r632_6.py <packet> <pristine-tree> [--jobs N]
Each mutant replaces one anchor (exactly one occurrence) in scripts/act_ci.py
of a copy under <packet>/scratch/mut6/<id>, then runs `act_ci.py --selftest`
through <packet>/scripts/sandbox.sh. KILLED means the self-test exited
non-zero; the first FAIL arm is printed. R6 mutants revert or weaken the
round-6 fix; the run also reports, for each, whether one of the 18 new
closing-restore arms failed.
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

FIX = """    held = signal.pthread_sigmask(signal.SIG_BLOCK, ())
    primary: BaseException | None = None
    try:
        try:
            signal.pthread_sigmask(signal.SIG_UNBLOCK, CLEANUP_SIGNALS)
            require_live_pull_request(run.pr, run.repository, seams.query)
            integrity_check()
            if seams.pre_spawn is not None:
                seams.pre_spawn()
            try:
                result = seams.run_process(
                    command,
                    context=replace(context, env=dict(context.env)),
                    check=False,
                )
            except OSError as exc:
                raise Refusal(f"cannot start act: {exc}") from exc
            require_live_pull_request(run.pr, run.repository, seams.query)
            integrity_check()
            return result.returncode
        except BaseException as exc:
            primary = exc
            raise
        finally:
            signal.pthread_sigmask(signal.SIG_SETMASK, held)
    except TerminationRequest as delivered:
        # The first restore can itself be interrupted before it blocks.
        # The latch defers repeats; restore the hold before any diagnostic.
        signal.pthread_sigmask(signal.SIG_SETMASK, held)
        if primary is None or primary is delivered:
            raise
        try:
            print(
                f"act-ci: act boundary closing was interrupted ({type(delivered).__name__}: "
                f"{delivered}); the failure already propagating is kept",
                file=sys.stderr,
                flush=True,
            )
        except Exception:
            # Diagnostics have no authority to replace what propagates.
            pass
        raise primary
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, held)
"""
# The round-5 body (ede700b0), restored as the full-revert mutant.
ROUND5 = """    held = signal.pthread_sigmask(signal.SIG_BLOCK, ())
    try:
        signal.pthread_sigmask(signal.SIG_UNBLOCK, CLEANUP_SIGNALS)
        require_live_pull_request(run.pr, run.repository, seams.query)
        integrity_check()
        if seams.pre_spawn is not None:
            seams.pre_spawn()
        try:
            result = seams.run_process(
                command,
                context=replace(context, env=dict(context.env)),
                check=False,
            )
        except OSError as exc:
            raise Refusal(f"cannot start act: {exc}") from exc
        require_live_pull_request(run.pr, run.repository, seams.query)
        integrity_check()
        return result.returncode
    finally:
        signal.pthread_sigmask(signal.SIG_SETMASK, held)
"""
MUTANTS = (
    ("S1", "the round-6 fix reverted to the round-5 boundary", FIX, ROUND5),
    ("S2", "the closing signal replaces the active failure",
     "            pass\n        raise primary\n", "            pass\n        raise\n"),
    ("S3", "the active failure is never recorded",
     "        except BaseException as exc:\n            primary = exc\n            raise\n        finally:\n            signal.pthread_sigmask(signal.SIG_SETMASK, held)\n    except TerminationRequest",
     "        except BaseException as exc:\n            raise\n        finally:\n            signal.pthread_sigmask(signal.SIG_SETMASK, held)\n    except TerminationRequest"),
    ("S4", "act runs with the cleanup signals still blocked (not interruptible)",
     "        try:\n            signal.pthread_sigmask(signal.SIG_UNBLOCK, CLEANUP_SIGNALS)\n            require_live_pull_request(run.pr, run.repository, seams.query)",
     "        try:\n            require_live_pull_request(run.pr, run.repository, seams.query)"),
    ("S5", "the handler does not restore the hold before its diagnostic",
     "        # The latch defers repeats; restore the hold before any diagnostic.\n        signal.pthread_sigmask(signal.SIG_SETMASK, held)\n",
     "        # The latch defers repeats; restore the hold before any diagnostic.\n"),
    ("S6", "no restore at all after the handler (outer finally removed)",
     "        raise primary\n    finally:\n        signal.pthread_sigmask(signal.SIG_SETMASK, held)\n\n\n@dataclass\nclass JobCpuRanges:",
     "        raise primary\n    finally:\n        pass\n\n\n@dataclass\nclass JobCpuRanges:"),
    ("S7", "the closing diagnostic is not printed",
     '                f"act-ci: act boundary closing was interrupted ({type(delivered).__name__}: "\n                f"{delivered}); the failure already propagating is kept",',
     '                "",'),
    ("S8", "a signal that is itself the failure also prints the closing diagnostic",
     "        if primary is None or primary is delivered:\n            raise\n",
     "        if primary is None:\n            raise\n"),
    ("S9", "both closing restores removed (the hold is never restored by the boundary)",
     FIX, FIX.replace("        finally:\n            signal.pthread_sigmask(signal.SIG_SETMASK, held)\n", "        finally:\n            pass\n")
        .replace("        # The latch defers repeats; restore the hold before any diagnostic.\n        signal.pthread_sigmask(signal.SIG_SETMASK, held)\n", "")
        .replace("        raise primary\n    finally:\n        signal.pthread_sigmask(signal.SIG_SETMASK, held)\n", "        raise primary\n    finally:\n        pass\n")),
    ("S10", "a Refusal-only filter: a RuntimeError active failure is replaced by the signal",
     "        if primary is None or primary is delivered:\n            raise\n",
     "        if primary is None or primary is delivered or not isinstance(primary, Refusal):\n            raise\n"),
)


def run(mutant: tuple[str, str, str, str]) -> str:
    ident, title, old, new = mutant
    tree = PACKET / "scratch" / "mut6" / ident
    shutil.rmtree(tree, ignore_errors=True)
    shutil.copytree(PRISTINE, tree, copy_function=shutil.copy)
    target = tree / "scripts" / "act_ci.py"
    text = target.read_text()
    if text.count(old) != 1:
        return f"{ident} BAD-ANCHOR ({text.count(old)}) {title}"
    target.write_text(text.replace(old, new))
    try:
        result = subprocess.run(
            [str(PACKET / "scripts" / "sandbox.sh"), str(tree), "/usr/bin/python3", "-I", "scripts/act_ci.py", "--selftest"],
            capture_output=True, text=True, timeout=600,
        )
        rc, out, err = result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired as exc:
        rc, out, err = "timeout", (exc.stdout or b"").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""), ""
    fails = [line.strip() for line in out.splitlines() if line.startswith("  FAIL")]
    closing = sum("act closing restore line" in line for line in fails)
    verdict = "KILLED" if rc != 0 else "SURVIVED"
    first = fails[0][:200] if fails else ((err.strip().splitlines() or [""])[-1][:200])
    shutil.rmtree(tree, ignore_errors=True)
    return f"{ident} {verdict} rc={rc} fails={len(fails)} closing-arm-fails={closing} - {title}\n    first: {first}"


with concurrent.futures.ThreadPoolExecutor(max_workers=JOBS) as pool:
    lines = list(pool.map(run, MUTANTS))
for line in lines:
    print(line)
survived = [line.split()[0] for line in lines if " SURVIVED " in line]
bad = [line.split()[0] for line in lines if " BAD-ANCHOR " in line]
print(f"mutants: {len(lines)}, killed {len(lines) - len(survived) - len(bad)}, survived {survived}, bad anchors {bad}")
sys.exit(0)
