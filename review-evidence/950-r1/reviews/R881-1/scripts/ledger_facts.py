"""ledger_facts.py <tree-root>: the memory ledger's own facts and refusals (ctrl_memory_ledger.facts, .refusals,
.HELD), run where no LiteX is installed. migen, litex and milan_soc are stood in by inert modules ONLY so that
test_ctrl_memory.py imports for its ELF writer (ledger_elf); nothing graded here calls them. The product SoC build's
facts (product_facts, milan_soc.add_ctrl_memory) need the real LiteX and are NOT run: a stated limit."""
import sys
import tempfile
import types
from functools import partial
from pathlib import Path

root = Path(sys.argv[1]).resolve()


class _Inert(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return type(name, (), {"__init__": lambda self, *a, **k: None})


for name in ("migen", "litex", "litex.soc", "litex.soc.integration", "litex.soc.integration.builder",
             "litex.soc.interconnect", "milan_soc"):
    sys.modules[name] = _Inert(name)
sys.path.insert(0, str(root / "sw/litex"))
import test_ctrl_memory as t  # noqa: E402
import ctrl_memory  # noqa: E402
import ctrl_memory_ledger as ledgers  # noqa: E402

failures = 0
held = {name: (p.symbols, p.tiles) for name, p in ctrl_memory.LEDGERED.items()}
ok = held == ledgers.HELD
failures += not ok
print(f"[{'ok' if ok else 'FAIL'}] the ledger holds the ruled points: {held}")
with tempfile.TemporaryDirectory() as tmp:
    write = partial(t.ledger_elf, Path(tmp))
    for holds, what in ledgers.facts(write):
        failures += not holds
        print(f"[{'ok' if holds else 'FAIL'}] {what}")
    for rule, what, attempt in ledgers.refusals(write):
        try:
            attempt()
            got = None
        except ctrl_memory.Refusal as exc:
            got = exc.rule
        holds = got == rule
        failures += not holds
        print(f"[{'ok' if holds else 'FAIL'}] refused by {rule}: {what} (got {got})")
print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'} ({failures} failure(s))")
raise SystemExit(1 if failures else 0)
