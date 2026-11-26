#!/usr/bin/env python3
"""Append reviewer probe plants to a disposable tree's tests/mutations.json.
Usage: add_probe_plants.py <probe-tree>. Each 'old' must occur exactly once."""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
src = (root / 'src/adp.c').read_text()
A27_MOD = "A27 the seed is the sum's least significant 32 bits, modulo 2^32 (6.2.4.2.2)"
A22 = "A22 a seed that mixes to zero starts the generator at 1"
A28 = "A28 a draw outside DOWN takes no sample"
A27_IF = "A27 interfaces 0, 1, 2 and 255 sampled together draw apart"
A32 = "A32 an ENTITY_DISCOVER in WAITING draws its delay and takes no sample"
SUM = "\tuint32_t sum = (uint32_t)e->mac + sample;\n"
DISC = "\ttimer_stop(a);                                                  // Milan v1.2 5.6.3.5.4\n\tenter_delay(a, ADP_DRAW_DELAY);\n"
plants = [
    ("r939-sum-high-word-folded", SUM,
     "\tuint64_t wide = e->mac + sample;\n\tuint32_t sum = (uint32_t)wide ^ (uint32_t)(wide >> 32);\n",
     "AdpCore.A27EverySeedTermIsMixedIn", A27_MOD),
    ("r939-sum-adds-mac-high-bits", SUM,
     "\tuint32_t sum = (uint32_t)e->mac + sample + (uint32_t)(e->mac >> 32);\n",
     "AdpCore.A22GeneratorNeverStuckAtZero", A22),
    ("r939-gm-change-draw-sampled",
     "\t\tenter_delay(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.7\n",
     "\t\tleave_down(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.7\n",
     "AdpCore.A28EachLeaveOfDownTakesAFreshSample", A28),
    ("r939-advertise-draw-sampled",
     "\t\tenter_delay(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.5\n",
     "\t\tleave_down(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.5\n",
     "AdpCore.A28EachLeaveOfDownTakesAFreshSample", A28),
    ("r939-interface-seven-bits", "((uint32_t)a->interface << 24)",
     "((uint32_t)(a->interface & 0x7Fu) << 24)", "AdpCore.A27EverySeedTermIsMixedIn", A27_IF),
    ("r939-discover-zero-target-sampled", DISC,
     "\ttimer_stop(a);                                                  // Milan v1.2 5.6.3.5.4\n\tif (target == 0u) {\n\t\tleave_down(a, ADP_DRAW_DELAY);\n\t\treturn;\n\t}\n\tenter_delay(a, ADP_DRAW_DELAY);\n",
     "AdpCore.A32ADiscoverDrawTakesNoSample", A32),
    ("r939-discover-own-target-sampled", DISC,
     "\ttimer_stop(a);                                                  // Milan v1.2 5.6.3.5.4\n\tif (target != 0u) {\n\t\tleave_down(a, ADP_DRAW_DELAY);\n\t\treturn;\n\t}\n\tenter_delay(a, ADP_DRAW_DELAY);\n",
     "AdpCore.A32ADiscoverDrawTakesNoSample", A32),
]
m = json.loads((root / 'tests/mutations.json').read_text())
for name, old, new, test, needle in plants:
    assert src.count(old) == 1, (name, src.count(old))
    m.append({"name": name, "path": "src/adp.c", "old": old, "new": new,
              "kills": [{"test": test, "needle": needle}], "original_tests": [test]})
(root / 'tests/mutations.json').write_text(json.dumps(m, indent=2) + '\n')
print('added', len(plants))
