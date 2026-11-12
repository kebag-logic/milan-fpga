# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""SRP's Talker declarations as each source's validity moves them (#895; Milan v1.2 4.3.3.1, 5.3.7.4): the passes that
declare a Talker when a probe opens its source's DA gate, and that withdraw it when the probe window ends.

build.py's valid-destinations variant (a scratch copy of the size fixture, never the formal image) makes the fixture's
ACMP source port report each source's destination as the target platform's does, valid once MAAP holds its interface's
range, at base + n (Milan v1.2 5.5.4.1). So a PROBE_TX for a source is answered SUCCESS, its DA gate opens, and the
composition hands the gate to SRP, which declares the source's Talker Advertise at once, in a pass given whole to THE
TRANSMIT. Each probe's row runs from the command's commit to SRP's next frame, the declaration. With no Listener, the
15 s probe window then closes every gate and SRP withdraws every Talker in its own passes. whole_grade.py holds each
such pass to THE TRANSMIT's stated build cost and share.py to the per-pass share, as for every group.
"""
from __future__ import annotations

import answers
import scenario

#: The fixture's edits, each (unique anchor, replacement): the source port valid once MAAP holds the range.
FIXTURE_EDITS = (
    ('static void source(void *ctx, unsigned n, struct acmp_source_state *out)\n'
     '{ (void)ctx; (void)n; out->dest_mac_valid=false; }\n',
     'static void source(void *ctx, unsigned n, struct acmp_source_state *out);\n'),
    ('    (void)ctx; (void)count;\n    image_allocation[interface] = valid ? base : 0;\n}\n',
     '    (void)ctx;\n    image_allocation[interface] = valid ? base : 0;\n'
     '    image_count[interface] = valid ? count : 0u;\n}\n'
     'static void source(void *ctx, unsigned n, struct acmp_source_state *out)\n'
     '{\n    (void)ctx;\n    const unsigned i = n % MBX_N_IF;\n'
     '    out->dest_mac_valid = image_allocation[i] != 0u && n < image_count[i];\n'
     '    out->stream = (struct acmp_stream){image_entity.mac << 16 | n, image_allocation[i] + n, 2u};\n'
     '    out->asking_failed = false;\n}\n'),
    ('static volatile uint64_t image_allocation[MBX_N_IF];\n',
     'static volatile uint64_t image_allocation[MBX_N_IF];\nstatic volatile uint16_t image_count[MBX_N_IF];\n'),
)
#: The simulated time the group needs: MAAP's range, a probe a source, and the probe window's end.
SIM_MS = 21000
#: The probe window, Milan v1.2 4.3.3.1 (acmp.c's da_fresh_ms), and the wait past it.
WINDOW_MS = 16000


def groups(p: scenario.Point) -> list[scenario.Group]:
    """The arm's one group: a PROBE_TX for every source once MAAP holds the ranges, then the probe window's end."""
    srp, acmp, ms = scenario.CH['srp'], scenario.CH['acmp'], scenario.MS
    g = scenario.Group('srp-talker', sim_ms=SIM_MS)
    scenario.ready(g, p)
    g.add(f'wait cycles {2600 * ms}', 'wait quiet 3 within 2000000')
    seq = 0x5300
    for n in range(p.sources):
        i = n % p.interfaces
        g.probe(scenario.Probe(f'srp.talker_declare.s{n}', 'PROBE_TX -> Talker Advertise (DA gate opens)', 'srp',
                               f'rxc:{acmp}', [f'resp:{acmp}:{seq:x}', f'tx:{srp}'],
                               expect=answers.acmp('PROBE_TX_RESPONSE', 'SUCCESS')),
                f'frame {i} {scenario.talker_cmd(p, "PROBE_TX", n, seq).hex()}', wait=f'tx {srp} 1 within {300 * ms}')
        seq += 1
    g.add(f'wait cycles {WINDOW_MS * ms}', 'wait quiet 3 within 2000000')
    return [g]
