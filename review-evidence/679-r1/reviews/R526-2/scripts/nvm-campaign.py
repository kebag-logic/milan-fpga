"""Run the unmodified complete store campaign with physical worker-path reuse.

Only work / mutant.name is redirected. All identities, input construction,
compiler flags, content cache keys and failure oracles remain unchanged.
"""
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as subject

original = subject.plant_and_grade
lock = threading.Lock()
slots = {}


class WorkSlot:
    def __init__(self, path, name):
        self.path, self.name = path, name

    def __truediv__(self, name):
        assert name == self.name
        return self.path


def reuse_directory(mutant, shape, held, work, build):
    with lock:
        index = slots.setdefault(threading.get_ident(), len(slots))
        assert index < 4
    return original(mutant, shape, held, WorkSlot(work / f"slot-{index}", mutant.name), build)


subject.plant_and_grade = reuse_directory
sys.argv = [str(subject.__file__), "--require-rv32", "--self-test", "--jobs", "4"]
print("Original full campaign: physical worker-directory reuse only", flush=True)
raise SystemExit(subject.main())
