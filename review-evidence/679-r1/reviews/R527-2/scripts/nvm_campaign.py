#!/usr/bin/env python3
"""Original full driver, bounded physical directories per worker.

Equivalent to the public nvm_foreground.py evidence for issue 679.
Only work / mutant.name is redirected. Mutation identities, inventories,
source seams, flags, cache computation, tests and oracles remain unchanged.
"""
import sys
import threading
from pathlib import Path

root = Path(sys.argv.pop(1)).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as subject

original = subject.plant_and_grade
lock = threading.Lock()
slots = {}
jobs = int(sys.argv[sys.argv.index("--jobs") + 1])

class WorkSlot:
    def __init__(self, path, name):
        self.path, self.name = path, name

    def __truediv__(self, name):
        assert name == self.name, (name, self.name)
        return self.path

def reuse_directory(mutant, shape, held, work, build):
    with lock:
        index = slots.setdefault(threading.get_ident(), len(slots))
        assert index < jobs
    return original(mutant, shape, held,
                    WorkSlot(work / f"slot-{index}", mutant.name), build)

subject.plant_and_grade = reuse_directory
print("Original full campaign; bounded physical per-worker directories only", flush=True)
raise SystemExit(subject.main())
