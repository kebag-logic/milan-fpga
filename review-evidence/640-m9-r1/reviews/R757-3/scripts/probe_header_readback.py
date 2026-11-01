#!/usr/bin/env python3
"""Probe: compaction when the header page fails its read-back.

Usage: python3 -I probe_header_readback.py <dir-of-compaction_model.py>

Uses the author's host flash model (compaction_model.py, unchanged) for the
flash, boot and system classes. It drives the stream-engine page's row
"After a header that fails its read-back | The old slot, still active |
Compaction erases the standby and restarts from step 1".

A read-back can fail while the programmed header is in fact intact (a
transient error on the read path). Then:
  1. the header is valid in flash with a higher generation;
  2. saves append to the old slot, as the row says;
  3. a power cut lands before the standby erase reaches the header page.
Boot picks the valid header with the higher generation, so it reads the new
slot, which never received those saves.

Arms:
  as_written  the row as written: no step makes the header invalid
  invalidate  control: the header page is overwritten with zeros (a NOR
              program can only clear bits, so its check then fails) before
              any save appends to the old slot
Expect: as_written loses the save; invalidate loses nothing.
"""
import sys

sys.path.insert(0, sys.argv[1])
import compaction_model as cm  # noqa: E402


def run(arm):
    fl = cm.Flash()
    sysm = cm.System(fl)
    sysm.save({1: ('h', 1)})
    s_old = sysm.active
    s_new = 1 - s_old
    # C1 to C3 with no save in the window: copy, then replay the log
    p_new = 1
    for i in range(0, cm.LIVE_KEYS, cm.PER_PAGE):
        items = sorted(sysm.live.items())
        fl.program(s_new, p_new, ('BASE', tuple(items[i:i + cm.PER_PAGE])))
        p_new += 1
    log = sysm.log[s_old]
    for q in range(0, len(log), cm.PER_PAGE):
        fl.program(s_new, p_new, ('LOG', tuple(log[q:q + cm.PER_PAGE])))
        p_new += 1
    # C4: the header programs correctly; its read-back reports a failure
    fl.program(s_new, 0, ('HDR', sysm.gen + 1))
    readback_failed = True
    if readback_failed and arm == 'invalidate':
        fl.slot[s_new][0] = 'TORN'          # zeros over the page: check fails
    # the old slot stays active; a save lands and becomes durable there
    sysm.save({9: ('after-readback-fail', 0)})
    assert sysm.active == s_old
    # power cut before the standby erase reaches the header page
    state, used = cm.boot(fl)
    lost = {k: v for k, v in sysm.ack.items() if state.get(k) != v}
    return used, lost


def main():
    rc = 0
    for arm in ('as_written', 'invalidate'):
        used, lost = run(arm)
        print(f"{arm}: boot uses slot {used}; acknowledged values lost: {lost or 'none'}")
        if arm == 'as_written' and not lost:
            rc = 1
        if arm == 'invalidate' and lost:
            rc = 1
    print("PROBE AS EXPECTED" if rc == 0 else "PROBE NOT AS EXPECTED")
    return rc


if __name__ == "__main__":
    sys.exit(main())
