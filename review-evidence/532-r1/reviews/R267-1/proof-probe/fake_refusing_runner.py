#!/usr/bin/env python3
"""[R267] A stand-in runner for probing scripts/act_slot_proof.sh's grading only.

It never runs a workflow and never touches Docker, sudo or the network. Every PR
run refuses (exit 2) at the same point, after an isolated slot would have been
acquired. An isolated slot is emulated by an flock on a scratch file, so a
second concurrent run in one slot is refused with the real runner's wording.
The live interrupt self-test prints the slot-0 PASS line only (no slot line)
and exits 0, as a runner that silently ignored --slot would.
"""

import fcntl
import pathlib
import sys
import time


def value(flag: str, default: str = "") -> str:
    """The word after `flag` in argv, or `default`."""
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main() -> int:
    if "--interrupt-selftest" in sys.argv:
        print("interrupt-selftest: PASS (slot 0 only; the requested slot was ignored)")
        return 0
    slot = int(value("--slot", "0"))
    lock_dir = pathlib.Path(__file__).resolve().parent.parent / "scratch" / "fake-locks"
    lock_dir.mkdir(parents=True, exist_ok=True)
    handle = open(lock_dir / f"slot-{slot}.lock", "w")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        if slot:
            print(f"act-ci: REFUSED: replay slot {slot} is in use by another runner invocation",
                  file=sys.stderr)
        else:
            print("act-ci: REFUSED: shared Docker volume 'act-toolcache' already exists",
                  file=sys.stderr)
        return 2
    if slot:
        print(f"act-ci: slot {slot}: own daemon unix:///run/milan-act-slot-{slot}/docker.sock",
              flush=True)
    else:
        print("act-ci: running docs (.github/workflows/docs.yml)", flush=True)
    time.sleep(12)
    print("act-ci: REFUSED: act version check failed: the same refusal in every run",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
