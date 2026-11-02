#!/usr/bin/env python3
"""Reviewer probe: apply the probe groups to a scratch copy of the head (never the head itself).

usage: probe_groups.py <checkout>
Adds to tb/verilator/ctrl_service_budget: two links changing together or a pass apart, quiet and under the
composed load, and the composed load during a save's read-back at several phases of the centisecond tick."""
import re, sys, pathlib
root = pathlib.Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
s = (root / 'scenario.py').read_text()
s = s.replace("""*backlog_groups(p), *control_groups(p)]""", """*backlog_groups(p), *control_groups(p), *probe_groups(p, build)]""")
s += '''

PROBE_OFFSETS = (1, 5000, 10000, 20000, 30000, 50000, 80000, 120000)


def _links_quiet(p: Point) -> Group:
    """Two interfaces' links change together, then a growing distance apart, with no other load."""
    g = Group('x-links-quiet', sim_ms=3200)
    ready(g, p)
    g.add(f'wait cycles {100 * MS}', *OPEN_WINDOW)
    g.probe(Probe('x.links.if0', 'first joint link change', 'adp', 'pad:LINK:0', ['cancel:0'], until='x_end'),
            'link 0 0', wait='cycles 1', settle='')
    first = True
    for d in PROBE_OFFSETS:
        if not first:
            g.add('link 0 0')
        first = False
        g.add(f'wait cycles {d}', 'link 1 0', f'wait cycles {30 * MS}', 'link 0 1', f'wait cycles {d}', 'link 1 1',
              f'wait cycles {120 * MS}', 'wait quiet 3 within 2000000')
    g.add('mark x_end')
    return g


def _composed(name: str, p: Point, apart: int, before: list[str], count: int = 14, links: int = 2) -> Group:
    """backlog's window with both links changing (apart cycles apart), and optional steps before it."""
    acmp = CH['acmp']
    get = lambda seq: acmp_cmd(p, 'GET_RX_STATE', 0, seq)
    g = Group(name, sim_ms=4500)
    ready(g, p)
    g.add(*before)
    announced(g)
    g.add(*OPEN_WINDOW)
    gm_run(g, p, count)
    g.probe(Probe(f'{name}.event.if0', 'an event behind 15 others', 'adp', 'pad:LINK:0', ['cancel:0'],
                  until='composed_end'), 'link 0 0', wait='cycles 1', settle='')
    g.load['LINK'] = 1
    composed_load(g, p, own='acmp')
    if links == 2:
        if apart:
            g.add(f'wait cycles {apart}')
        g.add('link 1 0')
        g.load['LINK'] = 2
    number = admission('acmp', get(0))['at_once']
    for n in range(number - 1):
        g.offer('acmp', f'frame 0 {get(0x7200 + n).hex()}', get(0))
    g.probe(Probe(f'{name}.acmp_command.if0', 'an ACMP command behind a full acmp ring', 'acmp', f'rxc:{acmp}',
                  [f'resp:{acmp}:72ff'], until='composed_end'), f'frame 0 {get(0x72ff).hex()}',
            wait=f'tx {acmp} {number} within {300 * MS}', settle='quiet 3 within 50000000')
    g.load['acmp'] += 1
    g.add('mark composed_end')
    return g


def probe_groups(p: Point, build: dict) -> list[Group]:
    """The reviewer's probe groups."""
    out = [_links_quiet(p), _composed('x-links-same', p, 0, []), _composed('x-links-1ms', p, 100000, []),
           _composed('x-links-2ms', p, 200000, [])]
    name = b'probe'.ljust(64, b'\\0')
    for k in range(6):
        frame = f.aem_command(f.Aem(p.entity_id, CTL2, CTL_MAC, p.mac, 0x6f00), 0x0010,
                              f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + f.be(0, 2) + name)
        before = [f'frame 0 {frame.hex()}', f'wait cycles {k * 166700}']
        out.append(_composed(f'x-save-{k}', p, 0, before, 15, 1))
    return out
'''
(root / 'scenario.py').write_text(s)
g = (root / 'grade.py').read_text()
g = g.replace("""COMPOSED_ROWS = (*BACKLOG_ROWS, 'fixture')""",
 """COMPOSED_ROWS = (*BACKLOG_ROWS, 'fixture', 'x-links-same', 'x-links-1ms', 'x-links-2ms', *(f'x-save-{k}' for k in range(6)))""")
g = g.replace("""    if name == 'backlog':
        load['LINK'] = 1
""", """    if name == 'backlog' or name.startswith('x-save'):
        load['LINK'] = 1
    if name.startswith('x-links'):
        load['LINK'] = 2
        load['GM'] -= 1
""")
(root / 'grade.py').write_text(g)
