#!/usr/bin/env python3
"""Reviewer probe of the save-landing row "After a header that fails its
read-back: the old slot, still active; compaction erases the standby and
restarts from step 1". Uses the published compaction model's Flash, System
and boot. The header page is programmed intact (its check passes) but the
read-back is reported as failed (a transient read error), so the old slot
stays active. A save then appends to the old slot and is acknowledged.
A power cut lands before the standby's erase has removed the header.
Usage: python3 -I probe_compaction_header_readback.py /path/to/compaction_model.py
"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("cm", sys.argv[1]); cm = importlib.util.module_from_spec(spec); spec.loader.exec_module(cm)
fl = cm.Flash(); s = cm.System(fl)
s.save({1: ('h', 1)})
old, new = s.active, 1 - s.active
p_new = 1
for i in range(0, cm.LIVE_KEYS, cm.PER_PAGE):                  # step 2 copy
    fl.program(new, p_new, ('BASE', tuple(sorted(s.live.items())[i:i + cm.PER_PAGE]))); p_new += 1
q = 0
while q < len(s.log[old]):                                       # step 3 replay
    chunk = tuple(s.log[old][q:q + cm.PER_PAGE]); fl.program(new, p_new, ('LOG', chunk)); p_new += 1; q += len(chunk)
fl.program(new, 0, ('HDR', s.gen + 1))                           # step 4 header, stored intact
# read-back reported as failed: per the table the old slot stays active
s.save({7: ('after-failed-header', 1)})                           # acknowledged, in the old slot
# power cut now, before the standby erase reaches its header
state, used = cm.boot(fl)
print("boot uses slot", used, "(new standby)" if used == new else "(old slot)")
print("acknowledged key 7:", s.ack[7], "| after reboot:", state.get(7))
print("LOST" if state != s.ack else "kept")
