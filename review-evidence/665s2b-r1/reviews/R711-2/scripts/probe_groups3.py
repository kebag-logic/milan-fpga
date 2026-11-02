#!/usr/bin/env python3
"""Reviewer probe, third batch, on top of probe_groups2.py: one whole save with no other load, to give each step's cost.

usage: probe_groups3.py <checkout>"""
import sys, pathlib
root = pathlib.Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
s = (root / 'scenario.py').read_text()
s = s.replace("""*probe_groups2(p)]""", """*probe_groups2(p), probe_save(p)]""")
s += '''

def probe_save(p: Point) -> Group:
    """A SET_NAME, then every step of the save it starts, with no other load."""
    aecp = CH['aecp']
    name = b'probe'.ljust(64, b'\\0')
    frame = f.aem_command(f.Aem(p.entity_id, CTL2, CTL_MAC, p.mac, 0x6f00), 0x0010,
                          f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name)
    g = Group('z-save', sim_ms=5500)
    ready(g, p)
    g.probe(Probe('z.set_name.if0', 'set_name', 'aecp', f'rxc:{aecp}', [f'resp:{aecp}:6f00'], expect='aecp_response'),
            f'frame 0 {frame.hex()}', wait=f'tx {aecp} 1 within {50 * MS}')
    g.add(f'wait cycles {4500 * MS}')
    return g
'''
(root / 'scenario.py').write_text(s)
