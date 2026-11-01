#!/usr/bin/env python3
"""Fault probes on the port census's REBOOT terminal, run from a tree copy's sw/mailbox, on the recipe shape."""
import sys
from dataclasses import replace
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'sw/mailbox'))
import mailbox_model
import publication_census as pc
sys.modules.setdefault('publication_census', pc)
import census_elab, census_ports
from census_elab import Cell
from census_plants import ReadByProbe

src = pc.load(pc.DATAPATH, pc.WRAPPER_SV)
net = census_elab.elaborate(pc.overlay(src), census_elab.RECIPE)

def run(name, n, expect, terminal=None):
    saved = census_ports.REBOOT_TERMINAL
    if terminal is not None:
        census_ports.REBOOT_TERMINAL = terminal
    try:
        s = census_ports.survey_ports(pc.flow(n), pc)
    finally:
        census_ports.REBOOT_TERMINAL = saved
    hits = [f for f in s.findings if 'reboot' in f.lower() or 'u_probe_g' in f]
    print(f'--- {name}\n    expect: {expect}\n    ends: {s.ends}\n    findings: {len(s.findings)}')
    for f in (hits or s.findings)[:6]:
        print('      ' + f[:200])

def rewire(n, port, bits):
    c = n.cells['reboot_ctrl']
    return replace(n, cells={**n.cells, 'reboot_ctrl': replace(c, conns={**c.conns, port: bits})})

req = tuple(b for b in net.names['pp_reboot_req_w'] if isinstance(b, int))
other = tuple(b for b in net.names['pp_maap_int_state_nc_w'] if isinstance(b, int))[:1]
print('reboot_ctrl ports:', sorted(net.cells['reboot_ctrl'].conns))
run('control: the tracked netlist', net, 'no finding; reboot 1')
run('terminal removed', net, 'g-on-wire at reboot_ctrl.reboot_req_i', ('none', 'none', 'none'))
run('the arm: a probe on the request net', ReadByProbe('pp_reboot_req_w')(net), 'g-on-wire at u_probe_g.a_i')
run('the request also on another input of the cell', rewire(net, 'nvm_backed_i', req), 'g-on-wire at reboot_ctrl.nvm_backed_i')
run('a different G output driven into reboot_req_i', rewire(net, 'reboot_req_i', other),
    'author open risk 1: expected accepted, the terminal is not per output')
c = net.cells['reboot_ctrl']
run('the same port on a cell of another module', replace(net, cells={**net.cells, 'reboot_ctrl': replace(c, kind='KL_other')}),
    'g-on-wire: the terminal names the module too')
run('the request no longer reaches the terminal', rewire(net, 'reboot_req_i', ()),
    'the amr exclusion refuses a stale name; expected no refusal here')

# Mutant of the code: the terminal widened from the one port to any input of the cell. The census's own
# arm (a probe on the request's net) must be judged under it, and the planted second input shows what it would miss.
real = census_ports._g_end
def widened(n, e, shim_ok):
    if e[0] != 'out' and e[1] == 'reboot_ctrl' and n.cells[e[1]].kind == 'KL_reboot_ctrl':
        return 'reboot', e[2]
    return real(n, e, shim_ok)
census_ports._g_end = widened
run('MUTANT widened terminal: the census arm', ReadByProbe('pp_reboot_req_w')(net), 'still g-on-wire at the probe, so the arm does not see this mutant')
run('MUTANT widened terminal: the request also on another input', rewire(net, 'nvm_backed_i', req), 'accepted: no self-test arm plants this')
census_ports._g_end = real
