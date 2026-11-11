#!/usr/bin/env python3
"""guard_probe2.py <clone> [--snapshot-fix]: milan_soc.exact_cpu_decode (round-2 guard) against stand-in VexiiRiscv finalize
orders a re-pinned LiteX could have. For each: whether the guard refuses, the refusal's reason, and the region
list the generator would be handed (what generate_netlist reads: the instance attribute if one shadows the
class, else the class list). Nothing is generated; LiteX's naming step is replaced by a recorder of the list it
hashed. Shapes 1-4 are round 1's guard_probe.py shapes; 5-7 mutate the class list IN PLACE after naming."""
import sys
from pathlib import Path
from unittest.mock import patch

clone = Path(sys.argv[1])
sys.path.insert(0, str(clone / 'sw/litex'))
if '--snapshot-fix' in sys.argv:
    # Disposable in-memory variant: the naming step records a COPY of the list it hashed. No file is written.
    import importlib.util
    src = clone / 'sw/litex/milan_soc.py'
    text = src.read_text()
    line = "        named.append(VexiiRiscv.memory_regions)\n"
    assert text.count(line) == 1
    spec = importlib.util.spec_from_loader('milan_soc', loader=None, origin=str(src))
    milan_soc = importlib.util.module_from_spec(spec)
    milan_soc.__file__ = str(src)
    sys.modules['milan_soc'] = milan_soc
    exec(compile(text.replace(line, "        named.append(list(VexiiRiscv.memory_regions))\n"), str(src), 'exec'),
         milan_soc.__dict__)
    print('IN-MEMORY SNAPSHOT FIX APPLIED: named.append(list(VexiiRiscv.memory_regions))')
else:
    import milan_soc  # noqa: E402
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv  # noqa: E402

WHOLE = [(0x0, 0x38000, 'rxc', 'p'), (0x1000_0000, 0x38000, 'rwxc', 'p'), (0x0100_0000, 0x100_0000, 'rxc', 'p')]
EXTRA = (0x2000_0000, 0x1000, 'rw', 'p')


def pieces(rows):
    return all(s & (s - 1) == 0 and o % s == 0 for o, s, *_ in rows)


def shape(name, finalize):
    class StandIn(VexiiRiscv):
        def __init__(self):
            pass
        do_finalize = finalize
    cpu = StandIn()
    hashed = []
    with patch.object(VexiiRiscv, 'generate_netlist_name',
                      staticmethod(lambda: hashed.append(list(VexiiRiscv.memory_regions)))), \
            patch.object(VexiiRiscv, 'memory_regions', [], create=True):
        milan_soc.exact_cpu_decode(cpu)
        try:
            cpu.do_finalize()
            refusal = None
        except RuntimeError as exc:
            refusal = str(exc)
        handed = list(getattr(cpu, 'memory_regions', VexiiRiscv.memory_regions))
    same = bool(hashed) and handed == hashed[-1]
    if refusal:
        verdict = 'refused'
        reason = ('names-cache' if 'remove it from the generator' in refusal else
                  'not-aligned' if 'not aligned powers of two' in refusal else
                  'never-named' if 'no longer names it' in refusal else 'other')
    else:
        verdict = 'built exact' if pieces(handed) and same else (
            'BUILT SINGLE-MASK SILENTLY' if not pieces(handed) else 'BUILT, GENERATOR LIST != HASHED LIST, SILENTLY')
        reason = '-'
    print(f'{name}: {verdict}; reason {reason}; generator handed == list the name hashed: {same}; '
          f'generator handed {[(hex(o), hex(s)) for o, s, *_ in handed]}')


def today(self):
    """LiteX at the pin: collect into a fresh class list, then self.generate_netlist_name()."""
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()


def class_call(self):
    VexiiRiscv.memory_regions = list(WHOLE)
    VexiiRiscv.generate_netlist_name()


def recollect_after_name(self):
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()
    VexiiRiscv.memory_regions = list(WHOLE)


def instance_list(self):
    self.generator_regions = list(WHOLE)
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()


def recollect_in_place(self):
    """A re-pin that re-collects after naming into the same list object (clear, then append each row)."""
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()
    VexiiRiscv.memory_regions.clear()
    VexiiRiscv.memory_regions.extend(WHOLE)


def slice_assign(self):
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()
    VexiiRiscv.memory_regions[:] = WHOLE


def append_after_name(self):
    """A re-pin that adds one aligned row (e.g. a device window) to the class list after naming."""
    VexiiRiscv.memory_regions = list(WHOLE)
    self.generate_netlist_name()
    VexiiRiscv.memory_regions.append(EXTRA)


for n, f in (('1 pinned order', today), ('2 class-level naming call', class_call),
             ('3 list re-collected after naming (rebound)', recollect_after_name),
             ('4 list kept on the instance (generator_regions)', instance_list),
             ('5 list re-collected after naming IN PLACE (clear+extend)', recollect_in_place),
             ('6 list replaced after naming IN PLACE ([:] =)', slice_assign),
             ('7 aligned row appended after naming IN PLACE', append_after_name)):
    shape(n, f)
