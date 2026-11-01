#!/usr/bin/env python3
"""Reviewer probe of the failed-header path, driving the author's flash model.
Usage: python3 -I probe_flash_r4.py <dir holding compaction_model.py>

Arm 1: the restarted compaction's header fails its read-back once more.
Arm 2: saves resume before the zeroing (the order the page forbids).
Arm 3: the zeroed page is taken as still valid (the #823 format requirement
       not met); boot must then lose the save, so the requirement is load-bearing.
"""
import importlib.util
import os
import sys

spec = importlib.util.spec_from_file_location("compaction_model", os.path.join(sys.argv[1], "compaction_model.py"))
m = importlib.util.module_from_spec(spec)
sys.modules["compaction_model"] = m
spec.loader.exec_module(m)
orig = m.System._failed_header


def twice(self, s_old, s_new, saves_at, boundary, during_header, rb):
    fl = self.fl
    fl.program_zero(s_new, 0, sticks=(rb != 'intact_zero_fails'))
    if rb == 'intact_zero_fails':
        fl.erase_half(s_new, 0)
    if during_header:
        self.save(during_header)
    for b in sorted(k for k in saves_at if k >= boundary):
        self.save(saves_at[b])
    fl.erase(s_new)
    self.end[s_new] = 1
    self.log[s_new] = []
    self.count = getattr(self, 'count', 0) + 1
    self.compaction({}, None, rb if self.count == 1 else None)


m.System._failed_header = twice
for rb in ('intact', 'torn', 'intact_zero_fails'):
    r, f, ff = m.sweep((), (rb,))
    print(f"arm 1, header fails twice running, {rb}: {r} runs, {f} lose a change; first {ff}")
m.System._failed_header = orig


def late_zero(self, s_old, s_new, saves_at, boundary, during_header, rb):
    if during_header:
        self.save(during_header)             # before the header is invalid
    self.fl.program_zero(s_new, 0, sticks=True)
    for b in sorted(k for k in saves_at if k >= boundary):
        self.save(saves_at[b])
    self.fl.erase(s_new)
    self.end[s_new] = 1
    self.log[s_new] = []
    self.compaction({}, None, None)


m.System._failed_header = late_zero
r, f, ff = m.sweep((), ('intact',))
print(f"arm 2, the waiting save runs before the zeroing: {r} runs, {f} lose a change; first {ff}")
m.System._failed_header = orig

orig_boot = m.boot


def boot_zero_valid(fl):
    saved = [fl.slot[s][0] for s in (0, 1)]
    for s in (0, 1):
        if fl.slot[s][0] == 'ZERO':
            fl.slot[s][0] = ('HDR', 10 ** 6)     # an all-zero header passes its check
    try:
        return orig_boot(fl)
    finally:
        for s in (0, 1):
            fl.slot[s][0] = saved[s]


m.boot = boot_zero_valid
r, f, ff = m.sweep((), ('intact',))
print(f"arm 3, an all-zero header passes its check: {r} runs, {f} lose a change; first {ff}")
m.boot = orig_boot
