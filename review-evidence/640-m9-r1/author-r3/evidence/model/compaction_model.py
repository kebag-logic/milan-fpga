#!/usr/bin/env python3
"""Host flash model of the Mark II save path and compaction (lane evidence,
round 3; not a gate).

The ordering under test (stream-engine page, round 3):
  C1 note the active log end E0; the replay cursor Q starts there
  C2 copy the live tables into the standby slot, page by page; each page is
     assembled at a page boundary where no save is pending, so it holds
     durable values only (saves have strict priority at every boundary)
  C3 replay every active record at Q or later into the standby, in order,
     page by page; saves keep appending to the active slot meanwhile
  C4 at a page boundary where Q equals the log end and no save is pending,
     start the header page at once: the check and the header are one step
     that no save can split; a save that arrives during the header page
     waits for it and then appends to the new slot
  C5 saves append to the new slot; C6 the old slot is erased later
Boot: the valid header with the highest generation wins; base copy, then
records in sequence order; a transaction counts only with its commit.

Exercised: one save placed at every page boundary of a compaction (and one
arriving during the header page), with and without a second save, and a
power cut before, inside (torn) and after every page operation of the run.
Check: after reboot every key holds its last acknowledged value, or the
value of a save that was in flight at the cut (all of that transaction or
none of it).
Mutations, each must lose a change: 'split' (a save may run between the
check and the header), 'no_replay' (skip C3).
Usage: python3 -I compaction_model.py
"""
import itertools
import sys

PER_PAGE = 4          # records per page
LIVE_KEYS = 16        # live image: 4 base pages
SLOT_PAGES = 64


class Cut(Exception):
    pass


class Flash:
    """Two slots of pages. A page is None (erased) or a tuple payload; a
    torn page is 'TORN' (fails its check)."""

    def __init__(self):
        self.slot = [[None] * SLOT_PAGES, [None] * SLOT_PAGES]
        self.ops = 0
        self.cut_at = None          # (op index, mode) mode in before/torn/after

    def _op(self):
        n = self.ops
        self.ops += 1
        if self.cut_at and self.cut_at[0] == n:
            return self.cut_at[1]
        return None

    def program(self, s, p, payload):
        mode = self._op()
        if mode == 'before':
            raise Cut()
        assert self.slot[s][p] is None, (s, p)
        if mode == 'torn':
            self.slot[s][p] = 'TORN'
            raise Cut()
        self.slot[s][p] = payload
        if mode == 'after':
            raise Cut()

    def erase(self, s):
        # a sector erase in several steps; a cut leaves a partial erase
        for half in (0, 1):
            mode = self._op()
            if mode == 'before':
                raise Cut()
            lo, hi = (0, SLOT_PAGES // 2) if half == 0 else (SLOT_PAGES // 2, SLOT_PAGES)
            if mode == 'torn':
                for p in range(lo, (lo + hi) // 2):
                    self.slot[s][p] = None
                raise Cut()
            for p in range(lo, hi):
                self.slot[s][p] = None
            if mode == 'after':
                raise Cut()


def boot(fl):
    best = None
    for s in (0, 1):
        h = fl.slot[s][0]
        if isinstance(h, tuple) and h[0] == 'HDR':
            if best is None or h[1] > best[1]:
                best = (s, h[1])
    if best is None:
        return {}, None
    s = best[0]
    state = {}
    recs = []
    for p in range(1, SLOT_PAGES):
        pg = fl.slot[s][p]
        if not isinstance(pg, tuple):
            continue
        if pg[0] == 'BASE':
            for k, v in pg[1]:
                state[k] = v
        elif pg[0] == 'LOG':
            recs.extend(pg[1])
    recs.sort(key=lambda r: r[0])
    committed = {r[1] for r in recs if r[4]}
    for seq, txn, k, v, commit in recs:
        if txn in committed:
            state[k] = v
    return state, s


class System:
    def __init__(self, fl, mut=()):
        self.fl, self.mut = fl, set(mut)
        self.live = {k: ('v0', k) for k in range(LIVE_KEYS)}
        self.ack = dict(self.live)          # last acknowledged durable values
        self.inflight = None                # (txn, {k: v}) being saved
        self.active, self.gen = 0, 1
        self.end = [1, 1]                   # next free page per slot
        self.seq = 0
        self.txn = 0
        self.log = {0: [], 1: []}           # records per slot, in order
        # initial image: header, base pages, written before the run
        fl.slot[0][0] = ('HDR', 1)
        items = sorted(self.live.items())
        for i in range(0, LIVE_KEYS, PER_PAGE):
            fl.slot[0][self.end[0]] = ('BASE', tuple(items[i:i + PER_PAGE]))
            self.end[0] += 1

    def save(self, changes):
        """Strict-priority save: apply, then append one transaction."""
        self.txn += 1
        txn = self.txn
        for k, v in changes.items():
            self.live[k] = v
        self.inflight = (txn, dict(changes))
        recs = []
        items = list(changes.items())
        for i, (k, v) in enumerate(items):
            self.seq += 1
            recs.append((self.seq, txn, k, v, i == len(items) - 1))
        s = self.active
        for i in range(0, len(recs), PER_PAGE):
            chunk = tuple(recs[i:i + PER_PAGE])
            self.fl.program(s, self.end[s], ('LOG', chunk))
            self.end[s] += 1
            self.log[s].extend(chunk)
        self.ack.update(changes)
        self.inflight = None

    def compaction(self, saves_at, during_header=None):
        """saves_at: {boundary index: changes}; a save runs at that page
        boundary. during_header: changes that arrive while the header page
        is being programmed."""
        fl, s_old = self.fl, self.active
        s_new = 1 - s_old
        q = len(self.log[s_old])                       # C1
        boundary = 0

        def at_boundary():
            nonlocal boundary
            ch = saves_at.get(boundary)
            boundary += 1
            if ch:
                self.save(ch)

        # C2: copy live tables; a page is assembled with no save pending
        p_new = 1
        for i in range(0, LIVE_KEYS, PER_PAGE):
            at_boundary()
            items = sorted(self.live.items())
            fl.program(s_new, p_new, ('BASE', tuple(items[i:i + PER_PAGE])))
            p_new += 1
        # C3: replay at page granularity until the cursor meets the log end
        while True:
            at_boundary()
            if 'no_replay' in self.mut:
                break
            if q >= len(self.log[s_old]):
                if 'split' in self.mut:
                    at_boundary()            # the window the ordering closes
                break
            chunk = tuple(self.log[s_old][q:q + PER_PAGE])
            fl.program(s_new, p_new, ('LOG', chunk))
            p_new += 1
            q += len(chunk)
        # C4: the check passed; the header starts at once
        self.gen += 1
        fl.program(s_new, 0, ('HDR', self.gen))
        self.log[s_new] = []
        self.active, self.end[s_new] = s_new, p_new
        if during_header:
            self.save(during_header)         # waited for the header page
        # C5: saves now append to the new slot; C6: erase the old one
        for b in sorted(k for k in saves_at if k >= boundary):
            self.save(saves_at[b])
        fl.erase(s_old)
        self.end[s_old] = 1
        self.log[s_old] = []


def acceptable(state, sysm, cut):
    """Every key holds its last acknowledged value, or (only after a cut) the
    in-flight transaction applied whole."""
    if not cut or sysm.inflight is None:
        return state == sysm.ack
    txn, ch = sysm.inflight
    with_txn = dict(sysm.ack)
    with_txn.update(ch)
    return state == sysm.ack or state == with_txn


def scenario(save_b, second_b, header_save, cut, mut=()):
    fl = Flash()
    fl.cut_at = cut
    sysm = System(fl, mut)
    # some history in the active log before compaction starts
    try:
        sysm.save({1: ('h', 1)})
        sysm.save({2: ('h', 2), 3: ('h', 3)})
        saves = {}
        if save_b is not None:
            saves[save_b] = {1: ('c', save_b), 9: ('c', save_b)}
        if second_b is not None:
            saves.setdefault(second_b, {}).update({2: ('d', second_b), 14: ('d', second_b),
                                                    5: ('d', second_b), 6: ('d', second_b),
                                                    7: ('d', second_b)})
        hs = {3: ('e', 0), 12: ('e', 0)} if header_save else None
        sysm.compaction(saves, hs)
        sysm.save({4: ('after', 0)})
        hit = False
    except Cut:
        hit = True
    state, _ = boot(fl)
    return acceptable(state, sysm, hit), hit, fl.ops


def sweep(mut=()):
    """Every save boundary, with and without a second save and a save during
    the header page; every power cut point and mode, plus no cut."""
    # boundaries: 4 copy pages + replay pages; at most about 12 boundaries
    bounds = list(range(0, 12))
    runs = fails = 0
    first_fail = None
    for save_b in [None] + bounds:
        for second_b in [None] + bounds:
            for header_save in (False, True):
                ok, _, ops = scenario(save_b, second_b, header_save, None, mut)
                runs += 1
                if not ok:
                    fails += 1
                    first_fail = first_fail or (save_b, second_b, header_save, 'no cut')
                for op in range(ops):
                    for mode in ('before', 'torn', 'after'):
                        ok, hit, _ = scenario(save_b, second_b, header_save, (op, mode), mut)
                        runs += 1
                        if not ok:
                            fails += 1
                            first_fail = first_fail or (save_b, second_b, header_save, (op, mode))
    return runs, fails, first_fail


def main():
    runs, fails, ff = sweep()
    print(f"ordering as specified: {runs} runs, {fails} lose a change")
    ok = fails == 0
    for mut in ('split', 'no_replay'):
        r, f, ff = sweep((mut,))
        print(f"mutation {mut}: {r} runs, {f} lose a change; first {ff}")
        ok &= f > 0
    print("ALL PASS" if ok else "SOME FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
