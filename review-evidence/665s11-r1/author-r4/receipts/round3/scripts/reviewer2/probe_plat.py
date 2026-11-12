#!/usr/bin/env python3
"""Reviewer probes: plant one edit into a scratch copy of sw/firmware/ctrl (the campaign's own plant()), run the
named host arms, and print each test's [FAIL] lines. No edit touches the checkout.
Usage: probe_plat.py <repo-root> <scratch-dir> <probe-name|all>"""
import sys
from pathlib import Path
root, scratch, which = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import ctrl_mutants, plat_arms, ctrl_arms, fw_gtest           # noqa: E402
from ctrl_build import Tree, Refusal, Outcome                 # noqa: E402
from ctrl_mutant import Mutant                                # noqa: E402
PLAT, AECP = 'plat/ctrl_plat.c', 'aecp/aecp.c'
PROBES = {
    # control: the head unchanged
    'head': (PLAT, '\treturn !aecp_reboot_accepted(', '\treturn !aecp_reboot_accepted(', ('platboot1',)),
    # the receive gate left off the MAAP and SRP channels: B19 sends no MAAP or SRP frame
    'gate-skips-maap-and-srp': (PLAT, '\t\tif (p->rx[ch].fn != NULL) {\n',
                                '\t\tif (p->rx[ch].fn != NULL && ch < MBX_CH_MAAP) {\n', ('platboot1',)),
    # the gate closed only once the REBOOT's frames are handed over, not at its SUCCESS
    'gate-from-the-handover': (AECP, '\treturn a->reboot != 0u;\n', '\treturn a->reboot >= 2u;\n',
                               ('platboot1', 'unit')),
}
names = list(PROBES) if which == 'all' else [which]
build = fw_gtest.Build(jobs=4)
arms = {'platboot1': lambda t: plat_arms.arm_platboot(t, 1), 'unit': ctrl_arms.arm_unit}
for name in names:
    path, old, new, use = PROBES[name]
    m = Mutant(name, path, old, new, use[0], '', '')
    work = scratch / name
    ctrl, stack = ctrl_mutants.plant(m, work)
    tree = Tree(ctrl, work / 'work' / 'build', scratch / 'reuse', build, stack)
    for arm in use:
        try:
            o = arms[arm](tree)
        except Refusal as exc:
            o = Outcome(arm, 2, f'refused: {exc}')
        fails = [ln.strip() for ln in o.log.splitlines() if '[FAIL]' in ln]
        reboot = [ln for ln in fails if 'Reboot' in ln or 'Boot.B1' in ln or 'Boot.B2' in ln]
        print(f'PROBE {name} arm {arm}: rc {o.rc}; {len(fails)} failed check(s); REBOOT-related {len(reboot)}')
        for ln in fails[:12]:
            print('    ' + ln[:300])
        passed = [ln.strip() for ln in o.log.splitlines() if ('B19' in ln or 'B20' in ln or 'B21' in ln or 'Reboot' in ln) and ('OK' in ln or 'PASS' in ln)]
        for ln in passed[:8]:
            print('    passed: ' + ln[:200])
