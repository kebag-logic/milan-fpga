#!/usr/bin/env python3
"""Reviewer probes for round 3: plant one or more edits into a scratch copy of sw/firmware/ctrl (the campaign's own
plant() for the first, the same exact-once replace for the rest), run the platboot1 arm, and print every [FAIL]
line and the REBOOT tests that passed. No edit touches the checkout.
Usage: probe_r3.py <repo-root> <scratch-dir> <probe-name|all>"""
import sys
from pathlib import Path
root, scratch, which = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), sys.argv[3]
sys.path.insert(0, str(root / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(root / 'sw/firmware/gtest'))
import ctrl_mutants, plat_arms, fw_gtest                      # noqa: E402
from ctrl_build import Tree, Refusal, Outcome                 # noqa: E402
from ctrl_mutant import Mutant                                # noqa: E402
PLAT, AECP = 'plat/ctrl_plat.c', 'aecp/aecp.c'
TAKE = '\treturn !aecp_reboot_accepted(&ctrl_plat.aecp.core) && (own->ready == NULL || own->ready(own->ctx));\n'
DEPART = '\t} else if (ctrl_plat.reboot != 0u) {\n\t\tdepart(&ctrl_plat);\n'
STEP_END = '\t} else {\n\t\tctrl_loop_step(&ctrl_plat.app.loop);\n\t}\n}\n'
SILENT = '\t\treturn false;\n\t}\n\tbool pending = asynchronous(a);\n'
PROBES = {
    # control: the head unchanged
    'head': ((PLAT, TAKE, TAKE),),
    # the gate one pass late: it reads acceptance latched at the end of the previous step, so frames serviced
    # after AECP in the pass that takes the REBOOT are taken. Only a check in that same pass can see it.
    'gate-one-pass-late': (
        (PLAT, 'static bool taking(void *ctx)\n', 'static bool late_accepted;\nstatic bool taking(void *ctx)\n'),
        (PLAT, TAKE, '\treturn !late_accepted && (own->ready == NULL || own->ready(own->ctx));\n'),
        (PLAT, STEP_END, '\t} else {\n\t\tctrl_loop_step(&ctrl_plat.app.loop);\n\t}\n'
                         '\tlate_accepted = aecp_reboot_accepted(&ctrl_plat.aecp.core);\n}\n'),
    ),
    # AECP able to transmit after the DEPARTING: the loop serviced after it (the shipped loop-on defect's edit)
    # and the AECP core's REBOOT silence lifted once its frames are out. Asks whether B20's AECP words can fail.
    'aecp-transmits-after-the-departing': (
        (PLAT, DEPART, DEPART + '\t\tif (ctrl_plat.reboot != 3u) {\n\t\t\tctrl_loop_step(&ctrl_plat.app.loop);\n'
                                '\t\t}\n'),
        (AECP, SILENT, '\t\tif (a->reboot != 2u) {\n\t\t\treturn false;\n\t\t}\n\t}\n'
                       '\tbool pending = asynchronous(a);\n'),
    ),
}
names = list(PROBES) if which == 'all' else [which]
build = fw_gtest.Build(jobs=4)
for name in names:
    edits = PROBES[name]
    path, old, new = edits[0]
    work = scratch / name
    try:
        ctrl, stack = ctrl_mutants.plant(Mutant(name, path, old, new, 'platboot1', '', ''), work)
        for p, o, n in edits[1:]:
            t = ctrl / p
            text = t.read_text(encoding='utf-8')
            if text.count(o) != 1:
                raise Refusal(f'{name}: fixture occurs {text.count(o)} times in {p}')
            t.write_text(text.replace(o, n), encoding='utf-8')
        tree = Tree(ctrl, work / 'work' / 'build', scratch / 'reuse', build, stack)
        o = plat_arms.arm_platboot(tree, 1)
    except Refusal as exc:
        o = Outcome('platboot1', 2, f'refused: {exc}')
    fails = [ln.strip() for ln in o.log.splitlines() if '[FAIL]' in ln]
    print(f'PROBE {name} arm platboot1: rc {o.rc}; {len(fails)} failed check(s)')
    for ln in fails[:40]:
        print('    ' + ln[:300])
    for ln in o.log.splitlines():
        s = ln.strip()
        if s.startswith('[       OK ] Boot.B') or s.startswith('[  FAILED  ] Boot.B'):
            print('    ' + s[:200])
    if o.rc == 2:
        print('    ' + o.log[-2000:])
