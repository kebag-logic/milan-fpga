"""Probe the ledger arms of sw/litex/test_ctrl_memory.py without migen/litex (stubbed; the ledger code uses neither):
at the tree as given, and with the size fixture's 8x8/2if entry planted back to 59.0 and forward to 60.0."""
import dataclasses, sys, tempfile, types
from pathlib import Path
root = Path(sys.argv[1]).resolve()
import importlib.abc, importlib.machinery
class _Any(type):
    def __getattr__(cls, name): return _Any(name, (), {})
    def __call__(cls, *a, **k): return cls
class _Stub(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path, target=None):
        if name.split(".")[0] in ("migen", "litex", "litespi", "liteeth", "litedram", "litex_boards"):
            return importlib.machinery.ModuleSpec(name, self, is_package=True)
    def create_module(self, spec):
        m = types.ModuleType(spec.name); m.__path__ = []; m.__getattr__ = lambda n: _Any(n, (), {}); return m
    def exec_module(self, module): pass
sys.meta_path.insert(0, _Stub())
sys.path.insert(0, str(root / "sw/litex"))
import test_ctrl_memory as t
import ctrl_memory
def arms(label):
    problems = []
    with tempfile.TemporaryDirectory() as d:
        t.ledger_arms(problems, Path(d))
    print(f"{label}: {len(problems)} problem(s)")
    for p in problems[:4]: print("   ", p[:200])
    return problems
base = dict(ctrl_memory.LEDGERED)
ok = not arms("as committed")
for tiles in (59.0, 60.0):
    ctrl_memory.LEDGERED = dict(base, **{"8x8-two-interfaces": dataclasses.replace(base["8x8-two-interfaces"], tiles=tiles)}) \
        if dataclasses.is_dataclass(base["8x8-two-interfaces"]) else dict(base, **{"8x8-two-interfaces": base["8x8-two-interfaces"]._replace(tiles=tiles)})
    ok &= bool(arms(f"fixture entry planted at {tiles}"))
ctrl_memory.LEDGERED = base
print("PROBE", "PASS" if ok else "FAIL")
