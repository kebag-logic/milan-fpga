#!/usr/bin/env python3
"""Reviewer probe, second batch, on top of probe_groups.py in the same scratch copy: a save's read-back and a joint
link change in the bound-talker window, the heaviest composed window of the author's run.

usage: probe_groups2.py <checkout>"""
import sys, pathlib
root = pathlib.Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
s = (root / 'scenario.py').read_text()
s = s.replace("""*control_groups(p), *probe_groups(p, build)]""", """*control_groups(p), *probe_groups(p, build), *probe_groups2(p)]""")
s += '''

def _adp_window(p: Point, name: str, before: list[str], links: bool) -> Group:
    """backlog-adp's window (bound_talker_groups), with steps before it, and optionally both links changing."""
    acmp, adp = CH['acmp'], CH['adp']
    disc = f.adp(f.ADP_DISCOVER, 0, CTL_MAC, f.Adp(valid_time=0))
    gone = f.adp(f.ADP_DEPARTING, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=0, talker_sources=1, talker_caps=0x4001))
    avail = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC, f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001))
    count = 13 if links else 15
    last_gm = max(n for n in range(count) if n % p.interfaces == 0)
    current = f.adp(f.ADP_AVAILABLE, TALKER_A, TALKER_A_MAC,
                    f.Adp(valid_time=10, talker_sources=1, talker_caps=0x4001, gm_id=0x0A0B0C0DFFFE0000 + last_gm))
    at_once = admission('adp', disc)['at_once']
    g = Group(name, sim_ms=4500)
    ready(g, p)
    g.add(*before)
    announced(g)
    g.add(f'frame 0 {acmp_cmd(p, "BIND_RX", 0, 0x7000).hex()}', f'wait tx {acmp} 2 within {20 * MS}',
          'wait quiet 3 within 2000000', f'frame 0 {avail.hex()}', 'wait quiet 3 within 2000000',
          f'frame 0 {gone.hex()}', f'wait cycles {50 * MS}', 'wait quiet 3 within 2000000', *OPEN_WINDOW)
    gm_run(g, p, count)
    if links:
        g.add('link 0 0', 'link 1 0')
        g.load['LINK'] = 2
    composed_load(g, p, own='adp')
    for n in range(at_once - 1):
        g.offer('adp', f'frame {n % p.interfaces} {disc.hex()}', disc)
    g.probe(Probe(f'{name}.adp_available.if0', 'an ENTITY_AVAILABLE behind a full adp ring', 'disc',
                  f'rxc:{adp}', [f'arm:{p.interfaces}'], until='composed_end'), f'frame 0 {current.hex()}',
            wait=f'tmr {p.interfaces} 1 within {400 * MS}', settle='quiet 3 within 50000000')
    g.load['adp'] += 1
    g.add('mark composed_end')
    return g


def probe_groups2(p: Point) -> list[Group]:
    """The second batch."""
    name = b'probe'.ljust(64, b'\\0')
    frame = f.aem_command(f.Aem(p.entity_id, CTL2, CTL_MAC, p.mac, 0x6f00), 0x0010,
                          f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name)
    out = [_adp_window(p, 'y-links', [], True)]
    for k in range(8):
        out.append(_adp_window(p, f'y-save-{k}', [f'frame 0 {frame.hex()}', f'wait cycles {k * 125000}'], False))
    return out
'''
(root / 'scenario.py').write_text(s)
g = (root / 'grade.py').read_text()
g = g.replace("""*(f'x-save-{k}' for k in range(6)))""", """*(f'x-save-{k}' for k in range(6)), 'y-links', *(f'y-save-{k}' for k in range(8)))""")
g = g.replace("""    if name == 'backlog-adp-refill':
        load['adp'] = room('adp')
""", """    if name == 'backlog-adp-refill':
        load['adp'] = room('adp')
    if name == 'y-links':
        load['LINK'] = 2
        load['GM'] -= 2
""")
(root / 'grade.py').write_text(g)
