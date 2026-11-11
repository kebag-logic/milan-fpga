#!/usr/bin/env python3
"""R822-3 extra disposable probes, driven by the unchanged R822-2 harness (r822_probes.py).

Usage: python3 -B r822_r3_probes.py <probe-tree> <out-dir>

Each probe edits one file of a COPY of the reviewed head, runs the host platboot arm at one
interface (and the AECP core arm where named), records rc and failing lines, and restores
the file from git. Results in <out-dir>/results.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r822_probes as p  # noqa: E402  (reads argv[1], argv[2] as the R822-2 harness does)

OTHERS = '\t\t\tif (ch != MBX_CH_ADP && !drained(ch)) {\n'
DEPART = '\t} else if (ctrl_plat.reboot != 0u) {\n\t\tdepart(&ctrl_plat);\n'
p.PROBES.clear()
p.PROBES.update({
    'clean': [],
    # equivalence check of the claim that AECP's ring needs no wait of its own (expected to survive)
    'depart-past-the-aecp-ring': [(p.PLAT, OTHERS,
                                   '\t\t\tif (ch != MBX_CH_ADP && ch != MBX_CH_AECP && !drained(ch)) {\n')],
    # the head's own loop-after-the-DEPARTING defect, to list every check it reaches (which channels' words)
    'loop-after-the-departing': [(p.PLAT, DEPART, DEPART + '\t\tif (ctrl_plat.reboot != 3u) {\n'
                                  '\t\t\tctrl_loop_step(&ctrl_plat.app.loop);\n\t\t}\n')],
    # AECP's own refusal removed: the platform gate alone must still hold AECP (platboot expected to pass);
    # the AECP core test is expected to catch it
    'aecp-ready-ignores-the-reboot': [(p.AECP,
                                       '\treturn aecp_enter(a) && a->open && !a->response_owed && !a->notify && '
                                       'a->reboot == 0u;\n',
                                       '\treturn aecp_enter(a) && a->open && !a->response_owed && !a->notify;\n')],
})
p.AECP_PROBES.clear()
p.AECP_PROBES.add('aecp-ready-ignores-the-reboot')

if __name__ == '__main__':
    sys.exit(p.main())
