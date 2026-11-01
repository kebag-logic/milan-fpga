#!/usr/bin/env python3
"""Probes on the published round-4 flash model: saves between the standby's
erase steps after a failed header, a second failed header on the restart, and
a header format whose all-zero page passes its check.
Usage: python3 -I probe_compaction_r4.py <dir holding compaction_model.py>"""
import sys

sys.path.insert(0, sys.argv[1])
import compaction_model as c  # noqa: E402


def failed_header(self, s_old, s_new, saves_at, boundary, during_header, rb):
    fl = self.fl
    fl.program_zero(s_new, 0, sticks=(rb != 'intact_zero_fails'))
    if rb == 'intact_zero_fails':
        fl.erase_half(s_new, 0)
    if during_header:
        self.save(during_header)
    for b in sorted(k for k in saves_at if k >= boundary):
        self.save(saves_at[b])
    n = getattr(self, 'seq_probe', 0)
    self.seq_probe = n + 1
    self.save({10: ('between0', n)})
    fl.erase_half(s_new, 0)
    self.save({11: ('between1', n)})
    fl.erase_half(s_new, 1)
    self.save({13: ('between2', n)})
    self.end[s_new] = 1
    self.log[s_new] = []
    again = 'intact' if self.__dict__.get('fail_twice') and n == 0 else None
    self.compaction({}, None, again)


def scenario(rb, save_b, header_save, cut, twice):
    fl = c.Flash()
    fl.cut_at = cut
    s = c.System(fl)
    s.fail_twice = twice
    try:
        s.save({1: ('h', 1)})
        s.save({2: ('h', 2), 3: ('h', 3)})
        saves = {save_b: {1: ('c', save_b), 9: ('c', save_b)}} if save_b is not None else {}
        s.compaction(saves, {3: ('e', 0), 12: ('e', 0)} if header_save else None, rb)
        s.save({4: ('after', 0)})
        hit = False
    except c.Cut:
        hit = True
    state, _ = c.boot(fl)
    return c.acceptable(state, s, hit), fl.ops


def sweep():
    runs = fails = 0
    first = None
    for rb in ('intact', 'torn', 'intact_zero_fails'):
        for twice in (False, True):
            for save_b in [None] + list(range(0, 10)):
                for hs in (False, True):
                    ok, ops = scenario(rb, save_b, hs, None, twice)
                    runs += 1
                    if not ok:
                        fails += 1
                        first = first or (rb, twice, save_b, hs, 'no cut')
                    for op in range(ops):
                        for mode in ('before', 'torn', 'after'):
                            ok, _ = scenario(rb, save_b, hs, (op, mode), twice)
                            runs += 1
                            if not ok:
                                fails += 1
                                first = first or (rb, twice, save_b, hs, op, mode)
    return runs, fails, first


orig_fh, orig_boot = c.System._failed_header, c.boot
c.System._failed_header = failed_header
print("saves between the standby's erase steps, one or two failed headers:", sweep())
c.System._failed_header = orig_fh


def boot_zero_passes(fl):
    # the header format #823 must exclude: an all-zero page passes its check
    best = None
    for s in (0, 1):
        h = fl.slot[s][0]
        if h == 'ZERO':
            h = ('HDR', 10 ** 6)
        if isinstance(h, tuple) and h[0] == 'HDR':
            if best is None or h[1] > best[1]:
                best = (s, h[1])
    if best is None:
        return {}, None
    saved = fl.slot[best[0]][0]
    fl.slot[best[0]][0] = ('HDR', best[1])
    fl.slot[1 - best[0]][0] = None
    r = orig_boot(fl)
    fl.slot[best[0]][0] = saved
    return r


c.boot = boot_zero_passes
r, f, ff = c.sweep((), ('intact',))
print(f"mutation an all-zero header passes its check: {r} runs, {f} lose a change; first {ff}")
c.boot = orig_boot

t = 5.35
print(f"t_page {(260 * 8 / 12.5e6 * 1e3) * 2 + 0.011 + 5.0:.3f} ms; T_worst {10 + t + 2 + 32 * t + 32 * t:.2f} ms; "
      f"with one zeroing page {10 + t + 2 + 32 * t + 32 * t + t:.2f} ms")
p = 5.35e-3
t_all = 382.5 * p
erase = (12 + 0.17 + 0.32) / 0.9
tot = t_all + erase + t_all
print(f"failed header then restart, S1 and S2: {t_all:.3f} s + erase {erase:.2f} s + {t_all:.3f} s = {tot:.2f} s; "
      f"appended <= {32 + 0.1 * tot / p:.1f} pages against 392 free at the trigger")
tot2 = tot + 3.0 / 0.9
print(f"double fault adds a held 3 s erase: {tot2:.2f} s; appended <= {32 + 0.1 * tot2 / p:.1f} pages")
ex = 2 + 200e-6 * 2917 + 0.16
print(f"E_x {ex:.4f} us; A4 {0.125 + 2.667:.3f} ms; drift over 22 packets {22 * 125 * 200e-6:.3f} us; "
      f"partner margin {62.5 - 2.744 - 0.55:.2f} us; neighbour distance {125 - 2.744 - 0.55:.2f} us")
