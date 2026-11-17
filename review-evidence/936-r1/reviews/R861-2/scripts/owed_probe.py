#!/usr/bin/env python3
"""Reviewer falsification probe: plant reviewer-chosen variants of the owed-record defect through the AECP
campaign's own plant/build/run/caught machinery, on a disposable checkout. Usage:
  owed_probe.py <checkout> <output-dir>"""
import sys
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
import aecp_mutants as m  # noqa: E402
TAKE = ("        noticed = noticed || app->srp->ifs[interface].noticed != 0u;\n"
        "        app->srp_noticed |= app->srp->ifs[interface].noticed;\n"
        "        app->srp->ifs[interface].noticed = 0u;\n")
CHECK = ('App.NoPassIsIdleWhileAStreamOutputsNoticeIsOwed', "no pass is idle while a STREAM_OUTPUT's notice is owed")
m.DEFECTS = (
    # the record is read after it is cleared, so no pass reports it owed
    m.defect('rv-owed-read-after-clear', 'app/ctrl_app_srp.c', TAKE,
             "        app->srp_noticed |= app->srp->ifs[interface].noticed;\n"
             "        app->srp->ifs[interface].noticed = 0u;\n"
             "        noticed = noticed || app->srp->ifs[interface].noticed != 0u;\n", CHECK),
    # only the first interface's record is reported owed
    m.defect('rv-owed-first-interface-only', 'app/ctrl_app_srp.c', TAKE,
             "        noticed = noticed || (interface == 0u && app->srp->ifs[interface].noticed != 0u);\n"
             "        app->srp_noticed |= app->srp->ifs[interface].noticed;\n"
             "        app->srp->ifs[interface].noticed = 0u;\n", CHECK),
    # control: an unrelated no-op edit at the same site must NOT be reported caught
    m.defect('rv-control-noop', 'app/ctrl_app_srp.c', "    bool pending = noticed;\n",
             "    bool pending = noticed; /* no-op */\n", CHECK),
)
m.controls = lambda: None
print(f"tsn-c-stack at {m.stack_pin(m.STACK.resolve())}", flush=True)
sys.exit(int(m.campaign(out, stack=m.STACK.resolve())))
