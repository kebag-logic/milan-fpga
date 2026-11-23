#!/usr/bin/env python3
"""Reviewer-owned disposable plants for the #963 running check, run through the AECP campaign's own machinery
(aecp_mutants.campaign: an isolated copy of the tree, the named check required to fail on its words).

Usage (from the root of a disposable copy of the tree under review):
  python3 -B <this> <output-dir>
Each plant names the check that should catch it; the result is the campaign's [ok]/[ESCAPED] line and results.json.
"""
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'sw/firmware/ctrl/test'))
sys.path.insert(0, str(ROOT / 'sw/firmware/gtest'))
import aecp_mutants as m  # noqa: E402

EDIT = 'Core.MapEditsAreTheirDefinitionRowForRow'
STREAMS = 'Core.MapEditWorkObservesEachOutputStreamOnce'
PLANTS = [
    # an input port's edit observes a stream as if it were an output's
    m.Defect('review-input-port-observed', 'aecp/aecp_maps.c', '\tif (input) {\n\t\treturn true;\n\t}\n',
             '\tif (input && r == NULL) {\n\t\treturn true;\n\t}\n',
             ((EDIT, 'the edit reads its port once for each output stream its definition reaches'),)),
    # the table outlives its edit: a stream found idle in one edit is never observed again
    m.Defect('review-table-kept-across-edits', 'aecp/aecp_maps.c', 'uint32_t observed[MAP_IDLE_WORDS] = {0};',
             'static uint32_t observed[MAP_IDLE_WORDS];',
             ((STREAMS, 'an edit observes each stream it maps once, in its order'),)),
    # the running check is taken after the geometry's refusal is ignored: an illegal mapping's stream is observed
    m.Defect('review-observed-before-legal', 'aecp/aecp_maps.c',
             'if ((e.flags[n] & ILLEGAL) != 0u || !idle(a, observed, e.input, &e.rows[n].r) ||',
             'if (!idle(a, observed, e.input, &e.rows[n].r) || (e.flags[n] & ILLEGAL) != 0u ||',
             ((EDIT, 'the edit reads its port once for each output stream its definition reaches'),)),
]


def main() -> int:
    m.DEFECTS = tuple(PLANTS)
    m.controls = lambda: None  # the table-drift control is the campaign's own table's; these rows are extra
    escaped = m.campaign(Path(sys.argv[1]).resolve(), 4, (0, 1))
    print('extra plants:', 'some ESCAPED' if escaped else 'all caught')
    return 1 if escaped else 0


if __name__ == '__main__':
    sys.exit(main())
