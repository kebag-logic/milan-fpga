#!/usr/bin/env python3
"""R822-3 probe: ADP restarted straight after its SHUTDOWN, so an ENTITY_AVAILABLE can follow the
ENTITY_DEPARTING before the reset port. Asks whether any host test asserts that nothing but the
DEPARTING leaves ADP after it. Driven by the unchanged R822-2 harness.

Usage: python3 -B r822_r3_adp_probe.py <probe-tree> <out-dir>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r822_probes as p  # noqa: E402

SHUTDOWN = '\t\tadp_mbx_set_enable(&p->app.adp, false);\n'
p.PROBES.clear()
p.PROBES['adp-restarted-after-the-departing'] = [(p.PLAT, SHUTDOWN,
                                                  SHUTDOWN + '\t\tadp_mbx_set_enable(&p->app.adp, true);\n')]
p.AECP_PROBES.clear()

if __name__ == '__main__':
    sys.exit(p.main())
