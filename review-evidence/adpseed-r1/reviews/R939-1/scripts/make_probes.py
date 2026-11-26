#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the reviewer's disposable probe plants for the ADP seeding rule.

Usage: make_probes.py <repo> <out.json>
Each probe is applied by the repository's own mutation driver in --discover mode
(no named kill), so its results.json lists every test that fails on the probe.
"""
import json
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]), Path(sys.argv[2])
src = (repo / 'src/adp.c').read_text()


def probe(name, old, new):
    if src.count(old) != 1:
        raise SystemExit(name + ': old text must match once, matched ' + str(src.count(old)))
    return {'name': 'probe-' + name, 'path': 'src/adp.c', 'old': old, 'new': new, 'kills': [], 'original_tests': []}


rx = 'timer_stop(a);                                                  // Milan v1.2 5.6.3.5.4\n\tenter_delay(a, ADP_DRAW_DELAY);'
gm = 'enter_delay(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.7'
adv = 'enter_delay(a, ADP_DRAW_DELAY);                         // Milan v1.2 5.6.3.5.5'
probes = [
    # Scope: no sample at any other draw. Each of the three other draws sampled alone.
    probe('discover-draw-sampled', rx, rx.replace('enter_delay', 'leave_down')),
    probe('gm-change-draw-sampled', gm, gm.replace('enter_delay', 'leave_down')),
    probe('advertise-draw-sampled', adv, adv.replace('enter_delay', 'leave_down')),
    # Scope: one sample for the other interface's rise.
    probe('other-interface-rise-unsampled', 'leave_down(a, ADP_DRAW_DELAY);',
          '(a->interface == 0u ? leave_down : enter_delay)(a, ADP_DRAW_DELAY);'),
    # Scope: an enable with the link down takes no sample.
    probe('enable-link-down-sampled', '\t\ta->state = ADP_STATE_DOWN;                              // Milan v1.2 5.6.3.5.1\n',
          '\t\t(void)a->ports->seed(a->ports->ctx);\n\t\ta->state = ADP_STATE_DOWN;                              // Milan v1.2 5.6.3.5.1\n'),
    # Scope: a disable takes no sample.
    probe('disable-sampled', '\tif (!enable) {\n\t\tshutdown(a);\n',
          '\tif (!enable) {\n\t\t(void)a->ports->seed(a->ports->ctx);\n\t\tshutdown(a);\n'),
    # Scope: the interface is mixed in; only its lowest bit kept.
    probe('interface-low-bit-only', '((uint32_t)a->interface << 24)', '((uint32_t)(a->interface & 1u) << 24)'),
    # Scope: the startup sample alone ignored.
    probe('startup-sample-ignored', 'uint32_t sample = a->ports->seed(a->ports->ctx);',
          'uint32_t sample = a->ports->seed(a->ports->ctx) & (kind == ADP_DRAW_STARTUP ? 0u : 0xFFFFFFFFu);'),
    # The draw taken before the new seed is installed.
    probe('draw-before-seed', '\ta->rng = x != 0u ? x : 1u;\n\tenter_delay(a, kind);\n',
          '\tenter_delay(a, kind);\n\ta->rng = x != 0u ? x : 1u;\n'),
    # Only the low half of the sample used.
    probe('sample-low-half-only', 'uint32_t sum = (uint32_t)e->mac + sample;', 'uint32_t sum = (uint32_t)e->mac + (sample & 0xFFFFu);'),
    # The literal reading of 6.2.4.2.2: the least significant octets of the sum, no end-around carry.
    probe('plain-modular-sum', '\tsum += sum < sample;\n', ''),
    # The first rise's sample quantized to 16 clock steps (fewer distinct first delays).
    probe('first-rise-sample-quantized', 'uint32_t sample = a->ports->seed(a->ports->ctx);',
          'uint32_t sample = a->ports->seed(a->ports->ctx) & (a->draws == 0u ? 0xFFFFFFF0u : 0xFFFFFFFFu);'),
    # The later rises' sample quantized to 16 clock steps.
    probe('later-rise-sample-quantized', 'uint32_t sample = a->ports->seed(a->ports->ctx);',
          'uint32_t sample = a->ports->seed(a->ports->ctx) & (a->draws == 0u ? 0xFFFFFFFFu : 0xFFFFFFF0u);'),
]
if len(sys.argv) > 3:
    # Optional: the main core (a795471c) under the head's tests, as one whole-file plant.
    probes.append({'name': 'probe-base-core-under-head-tests', 'path': 'src/adp.c', 'old': src,
                   'new': Path(sys.argv[3]).read_text(), 'kills': [], 'original_tests': []})
out.write_text(json.dumps(probes, indent=2) + '\n')
print(len(probes), 'probes written')
