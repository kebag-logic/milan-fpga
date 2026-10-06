"""Run the original full campaign with four reusable physical mutant directories.

Only the work / mutant.name directory operation changes. Mutant identity,
source seams, generated inputs, compiler flags, cache keys, tests, failure
oracles and the driver's inventory/coverage checks remain original.
"""
import sys
import threading
from pathlib import Path
sys.path.insert(0, str(Path("sw/firmware/ctrl_nvm/test").resolve()))
import test_ctrl_nvm as subject
original = subject.plant_and_grade
lock = threading.Lock()
slots = {}

class WorkSlot:
    def __init__(self, path, name):
        self.path, self.name = path, name
    def __truediv__(self, name):
        assert name == self.name, (name, self.name)
        return self.path

def reuse_directory(mutant, shape, held, work, build):
    with lock:
        index = slots.setdefault(threading.get_ident(), len(slots))
        assert index < 4
    slot = WorkSlot(work / f"slot-{index}", mutant.name)
    return original(mutant, shape, held, slot, build)

subject.plant_and_grade = reuse_directory
sys.argv = ["sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py", "--require-rv32", "--self-test", "--jobs", "4"]
print("Full original campaign; only physical per-worker mutant directory reuse enabled", flush=True)
raise SystemExit(subject.main())
