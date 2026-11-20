#!/usr/bin/env python3
"""apply_hot5.py TREE ORDER BACKLOG ADP RECORD DROPPED: the relearned order into TREE's hot list, both copies, with the header
that records the procedure and its three windows (#665's ruling of 2026-11-17, issuecomment-6959600243, item 1) and the
traces' sha256. ctrl_split.ld's block between _ctrl_hot_start and _ctrl_hot_end is one `*-<stem>.o(.text.<f>)` a line
(ctrl_hot.entry). Prints how the order differs from the one it replaces."""
import hashlib
import sys
from pathlib import Path

tree, order = Path(sys.argv[1]), Path(sys.argv[2])
traces = [Path(t) for t in sys.argv[3:6]]
dropped = [l.split(None, 3) for l in Path(sys.argv[6]).read_text().splitlines() if l.strip()]
plat = tree / 'sw/firmware/ctrl/plat'
sys.path.insert(0, str(tree / 'sw/firmware/ctrl/test'))
import ctrl_hot  # noqa: E402

new = [tuple(line.split()) for line in order.read_text().splitlines() if line.strip()]
hot = plat / 'ctrl_split_hot.txt'
old = ctrl_hot.recorded(hot.read_text())
sha = [hashlib.sha256(t.read_bytes()).hexdigest() for t in traces]
dropped_lines = "\n".join(f"# Dropped: {d[0]} {d[1]}, which {d[3]} lack" for d in dropped) or "# Dropped: none"
header = f"""# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# ctrl_split_hot.txt - the order plat/ctrl_split.ld's hot list places (#665, NFR-SCOUT-01).
#
# Each function a service pass ran, in the order the passes first ran it, from
# committed-PC traces of the CPU budget harness (tb/verilator/ctrl_service_budget)
# on the 1x1/1if split image, arm A, built and run as run.py does by default, in
# three windows, each traced from 300,000 bus cycles before its first record's
# commit for 900,000 committed PCs (BUDGET_TRACE_AFTER, BUDGET_TRACE_PCS): the
# groups backlog and backlog-adp, each from its first record's commit, then the
# largest legal AECP command's group, aecp-largest-notice, from its first record's
# commit after its load's mark (aecp_long.*), its functions appended after the
# other two windows' in the order it first ran them (#665's ruling of 2026-11-17,
# issuecomment-6959600243, item 1). Every function the windows ran stands where
# they first ran it, and none is placed by hand. Each list is learned so at the
# head it ships with; a fourth window, or a window chosen for one head, needs a
# ruling of its own.
# The list keeps a traced entry only if its section links in every image the
# list serves (#665's ruling of 2026-11-18, issuecomment-6967930396, item 1);
# nothing else is dropped, added or reordered. The images it serves are the
# split images ctrl_srp_image.py links and holds to this list: the size fixture
# at 1x1/1if, 8x8/1if and 8x8/2if in each of the CPU budget harness's six arms,
# each as itself and as the SoC plan's stand-in and mapped images. The target
# platform's image (ctrl_plat_image.py) links the same script without that
# check, and an entry it lacks places nothing there.
{dropped_lines}
# The traces' sha256:
#   backlog              {sha[0]}
#   backlog-adp          {sha[1]}
#   aecp-largest-notice  {sha[2]}
#
# sw/firmware/ctrl/test/ctrl_hot.py requires the script's list to be this one,
# entry for entry, and every entry to name a section of the linked image.
# One entry a line: the object, then the function's section name. A firmware
# object is its source's stem; a runtime archive's member is <archive>:<member>.
"""
hot.write_text(header + ''.join(f'{s} {f}\n' for s, f in new))
ld = plat / 'ctrl_split.ld'
script = ld.read_text()
was = """		/* The service loop's hot code (#665, NFR-SCOUT-01): each function a
		 * service pass runs in the composed backlog windows, in the order a
		 * pass first runs it, ahead of the rest."""
now = """		/* The service loop's hot code (#665, NFR-SCOUT-01): each function a
		 * service pass runs in the windows ctrl_split_hot.txt records, the
		 * composed backlog's and the largest legal AECP command's, in the
		 * order a pass first runs it, ahead of the rest."""
if was in script:
    script = script.replace(was, now)
a = script.index(ctrl_hot.START) + len(ctrl_hot.START)
b = script.index(ctrl_hot.END)
script = script[:a] + '\n' + ''.join(f'\t\t{ctrl_hot.entry(e)}\n' for e in new) + '\t\t' + script[b:]
ld.write_text(script)
gone = [e for e in old if e not in new]
added = [e for e in new if e not in old]
print(f'old {len(old)} entries, new {len(new)}: {len(added)} added, {len(gone)} gone')
print('added:', ' '.join(f'{s}:{f}' for s, f in added))
print('gone:', ' '.join(f'{s}:{f}' for s, f in gone))
