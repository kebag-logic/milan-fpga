#!/usr/bin/env python3
"""Independent PDU-level model of the #629 AAF clock meter (design page at
head f4f0ecb4: The pick, The jump bound, E8, Lost PDUs rules 1-4, History,
lock, era and outputs) driving a model of KL_mmcm_drp_servo's state machine
and PI (lines 562-579, 609-618, 643-648, 228-233 at the page's base).

Written from the page's text, not from the author's model. Sections:
  steps     the step row (120 cases), with the no-cross-gap mutant and the
            round-4 reading (no deviation check in a loss-voided group)
  gapbound  the gap bound's two edge cases, swept over the bound
  alias     every loss run of 1..600 PDUs at all 16 start phases, ideal
            timestamps, against "one restart iff two or more groups voided"
  fill      a loss in a snapshot group against the no-loss run
  servoleg  the servo-with-meter row's loss leg, design and mutants
  counter   the counter row's loss leg, design and held-lock mutant
  legtrim   the servo row's trim check at the loss leg's end
Usage: pdu_model.py <section>
"""
import random
import sys

NOM = 125_000          # ns per PDU (6 samples at 48 kHz)
GRP_NS = 2_000_000
WIN_NS = 512_000_000
B1 = 4096              # adjacent spacing and in-group deviation bound
B2 = 5120              # spacing bound across one voided group (k = 2)
L0 = 5448              # MMCM plan offset, ns per 512 ms window


class Meter:
    """The meter's history, pick, loss and lock rules."""

    def __init__(self, b2=B2, cross_check=True, dev_in_lossgroup=True,
                 clear_lock_on_gap=False, restart_on_any_loss=False):
        self.b2 = b2
        self.cross_check = cross_check
        self.dev_in_lossgroup = dev_in_lossgroup
        self.clear_lock_on_gap = clear_lock_on_gap
        self.restart_on_any_loss = restart_on_any_loss
        self.prev_seq = None
        self.locked = False
        self.settle = 0
        self.grp = None        # open group: dict
        self.hist = False
        self.restarts = []     # PDU index of each restart
        self.rate = 0
        self.rate_valid = False
        self.gap_events = 0

    def _restart(self, n):
        self.hist = False
        self.rate_valid = False
        self.restarts.append(n)

    def _seed(self, g, pick):
        self.hist = True
        self.last_g = g
        self.last_pick = pick
        self.count = 0
        self.snaps = {0: pick}

    def _snap(self, c, v):
        self.snaps[c] = v
        if c >= 2048:
            self.rate = (v - self.snaps[c - 2048] - 8 * WIN_NS) >> 3
            self.rate_valid = True
        for old in [x for x in self.snaps if x < c - 2048]:
            del self.snaps[old]

    def _pick(self, n, g, pick):
        if not self.hist:
            self._seed(g, pick)
            return
        k = (g - self.last_g) % 16
        if k == 1:
            if abs(pick - self.last_pick - GRP_NS) > B1:
                self._restart(n)
                self._seed(g, pick)
                return
        elif k == 2:
            if self.cross_check and abs(pick - self.last_pick - 2 * GRP_NS) > self.b2:
                self._restart(n)
                self._seed(g, pick)
                return
            mid_c = self.count + 1
            if mid_c % 256 == 0:
                last = self.last_pick
                self._snap(mid_c, last + ((pick - last) >> 1))
        else:
            self._restart(n)
            self._seed(g, pick)
            return
        self.count += k
        self.last_g = g
        self.last_pick = pick
        if self.count % 256 == 0:
            self._snap(self.count, pick)

    def pdu(self, n, seq, ts):
        """One accepted PDU: index n (for the record), sequence_num, ts.
        Rule 1: a gap voids the open group; PDUs before the gap were
        deviation-checked as they arrived; PDUs after it are neither checked
        nor used; a group entered without its PDU 0 has no reference."""
        gap = self.prev_seq is not None and seq != (self.prev_seq + 1) % 256
        self.prev_seq = seq
        if gap:
            self.gap_events += 1
            self.settle = 0
            if self.clear_lock_on_gap:
                self.locked = False
        else:
            if self.settle < 7:
                self.settle += 1
            elif not self.locked:
                self.locked = True
        if gap and self.restart_on_any_loss and self.hist:
            self._restart(n)
        i = seq % 16
        g = seq >> 4
        if i == 0:
            self.grp = dict(g=g, ts0=ts, sum=0, void=False, devvoid=False)
        elif gap or self.grp is None or self.grp["g"] != g:
            if self.grp is not None and self.grp["g"] == g and not gap:
                pass
            elif self.grp is not None and self.grp["g"] == g:
                self.grp["void"] = True          # gap inside the group
            else:
                self.grp = dict(g=g, ts0=None, sum=0, void=True, devvoid=False)
        grp = self.grp
        if grp["void"] or grp["devvoid"]:
            return
        dev = ts - grp["ts0"] - i * NOM
        if abs(dev) > B1:
            grp["devvoid"] = True
            if self.hist:
                self._restart(n)
            return
        grp["sum"] += dev
        if i == 15:
            self._pick(n, g, grp["ts0"] + (grp["sum"] // 16))


class Meter4(Meter):
    """Round 4's reading: the deviation verdict is taken at a group's last
    PDU, so a loss-voided group is never deviation-checked."""

    def pdu(self, n, seq, ts):
        gap = self.prev_seq is not None and seq != (self.prev_seq + 1) % 256
        _pdu_deferred(self, n, seq, ts, gap)


def _pdu_deferred(self, n, seq, ts, gap):
    self.prev_seq = seq
    if gap:
        self.gap_events += 1
        self.settle = 0
        if self.clear_lock_on_gap:
            self.locked = False
    else:
        if self.settle < 7:
            self.settle += 1
        elif not self.locked:
            self.locked = True
    i = seq % 16
    g = seq >> 4
    if i == 0:
        self.grp = dict(g=g, ts0=ts, sum=0, void=False, maxdev=0)
    elif self.grp is None or self.grp["g"] != g:
        self.grp = dict(g=g, ts0=None, sum=0, void=True, maxdev=0)
        return
    grp = self.grp
    if gap and i != 0:
        grp["void"] = True
    if grp["ts0"] is not None:
        dev = ts - grp["ts0"] - i * NOM
        grp["sum"] += dev
        grp["maxdev"] = max(grp["maxdev"], abs(dev))
    if i == 15:
        if grp["void"]:
            return
        if grp["maxdev"] > B1:
            if self.hist:
                self._restart(n)
            return
        self._pick(n, g, grp["ts0"] + grp["sum"] // 16)



class Servo:
    """KL_mmcm_drp_servo: ACQUIRE/LOCKED/HOLDOVER, the 512 ms window, PI."""

    def __init__(self, phi_ns, talker_ns_per_win, rng):
        self.next_b = phi_ns + WIN_NS
        self.state = "IDLE"
        self.u = 0
        self.integ = 0
        self.lock_cnt = 0
        self.skip = 0
        self.talker = talker_ns_per_win
        self.rng = rng
        self.log = []          # (t, from, to)
        self.drops = 0
        self.first_locked = None

    def _go(self, t, to):
        if to != self.state:
            self.log.append((t, self.state, to))
            if self.state == "LOCKED" and to == "ACQUIRE":
                self.drops += 1
            if to == "LOCKED" and self.first_locked is None:
                self.first_locked = t
            self.state = to

    def lock_input(self, t, locked):
        if self.state == "IDLE" and locked:
            self._go(t, "ACQUIRE")
        elif self.state in ("ACQUIRE", "LOCKED") and not locked:
            self._go(t, "HOLDOVER")
        elif self.state == "HOLDOVER" and locked:
            self._go(t, "ACQUIRE")
            self.skip = 2
            self.lock_cnt = 0

    def boundary(self, t, meter):
        if self.state == "IDLE":
            return
        run = self.skip == 0 and self.state != "HOLDOVER" and meter.rate_valid
        if self.skip:
            self.skip -= 1
        locerr = L0 - self.u + self.rng.randint(-20, 20)
        # the talker's offset enters through the rate; the plant is the
        # local clock against PTP time, so e = locerr - rate
        e = locerr - meter.rate
        if not run:
            return
        self.integ += e >> 1
        self.u = self.integ + (e >> 2)
        if -1024 < e < 1024:
            self.lock_cnt = min(self.lock_cnt + 1, 4)
        else:
            self.lock_cnt = 0
        if self.state == "ACQUIRE" and self.lock_cnt >= 4:
            self._go(t, "LOCKED")
        elif self.state == "LOCKED" and self.lock_cnt == 0:
            self._go(t, "ACQUIRE")


def run_stream(meter, n_pdus, ts_of, lost, servo=None, until_ns=None):
    """Feed PDUs 0..n_pdus-1 (skipping lost ones) and the servo boundaries
    in time order. ts_of(n) gives the PDU's presentation timestamp."""
    for n in range(n_pdus):
        t = n * NOM
        if servo is not None:
            while servo.next_b <= t:
                servo.boundary(servo.next_b, meter)
                servo.next_b += WIN_NS
        if n in lost:
            continue
        meter.pdu(n, n % 256, ts_of(n))
        if servo is not None:
            servo.lock_input(t, meter.locked)


def ts_maker(ppm, err_fn, steps=()):
    def ts(n):
        v = (n * NOM * (1_000_000 + ppm)) // 1_000_000 + err_fn(n)
        for at, size in steps:
            if n >= at:
                v += size
        return v
    return ts


def uniform_err(seed, J):
    r = random.Random(seed)
    cache = {}

    def f(n):
        if n not in cache:
            cache[n] = r.randint(-J, J)
        return cache[n]
    return f


# ---------------------------------------------------------------- sections

def _step_case(args):
    place, pos, size = args
    J, ppm = 1426, 300
    G = 6000                    # group of the step: 12 s, after LOCKED
    n0 = G * 16
    lost = {n0} if place == "a" else {n0 + 15}
    at = n0 + pos
    res = {}
    for name, mk in (("design", lambda: Meter()),
                     ("mutant", lambda: Meter(cross_check=False)),
                     ("r4", lambda: Meter4()),
                     ("r4mut", lambda: Meter4(cross_check=False))):
        m = mk()
        s = Servo(130_000_000, 0, random.Random(5))
        ts = ts_maker(ppm, uniform_err(11 + pos, J), [(at, size)])
        run_stream(m, (G + 10 * 500) * 16, ts, lost, s)
        where = "-"
        if m.restarts:
            r0 = m.restarts[0]
            where = ("step-PDU" if r0 == at else
                     ("next-pick" if r0 > n0 + 15 else f"pdu{r0 - n0}"))
        res[name] = (len(m.restarts), where, s.drops,
                     round(s.first_locked / 1e9, 3) if s.first_locked else None)
    return place, pos, size, res


def sec_steps():
    from multiprocessing import Pool
    cases = [(pl, pos, sz) for pl in ("a", "b")
             for pos in (range(1, 16) if pl == "a" else range(0, 15))
             for sz in (20833, -20833, 10417, -10417)]
    with Pool(8) as pool:
        rows = pool.map(_step_case, cases)
    for place, pos, size, res in rows:
        print(f"{place} pos {pos:2d} step {size:+6d}: " + "; ".join(
            f"{k} restarts {v[0]} at {v[1]} drops {v[2]} first-LOCKED {v[3]}"
            for k, v in res.items()))

    def tally(name, pred):
        return sum(1 for r in rows if pred(r[3][name]))
    print("SUMMARY cases", len(rows))
    print("design: exactly one restart", tally("design", lambda v: v[0] == 1),
          "; at the step PDU", tally("design", lambda v: v[0] == 1 and v[1] == "step-PDU"),
          "; at the next pick", tally("design", lambda v: v[0] == 1 and v[1] == "next-pick"),
          "; LOCKED drops 0", tally("design", lambda v: v[2] == 0))
    hist = {}
    for r in rows:
        v = r[3]["mutant"]
        key = (v[0], v[2])
        hist[key] = hist.get(key, 0) + 1
    print("no-cross-check mutant (restarts, LOCKED drops): cases", dict(sorted(hist.items())))
    sp = [(r[0], r[1]) for r in rows if r[3]["mutant"][0] == 1]
    print("no-cross-check mutant still restarting at:", sorted(set(sp)))
    print("round-4 reading: exactly one restart", tally("r4", lambda v: v[0] == 1),
          "; its no-cross-check mutant: no restart", tally("r4mut", lambda v: v[0] == 0))


def sec_gapbound():
    G = 6000
    n0 = G * 16

    def case_a(b2):
        m = Meter(b2=b2)
        ts = ts_maker(300, lambda n: 0, [(n0, 3900)])
        run_stream(m, (G + 300) * 16, ts, {n0})
        return len(m.restarts)

    def case_b(b2):
        m = Meter(b2=b2)
        ts = ts_maker(-300, lambda n: 1426 if n < n0 else -1426, [(n0, 10417)])
        run_stream(m, (G + 300) * 16, ts, {n0})
        return len(m.restarts)

    for b in (4096, 5099, 5100, 5120, 6364, 6365, 6400, 8192):
        print(f"bound {b}: (a) restarts {case_a(b)}; (b) restarts {case_b(b)}")
    lo = next(b for b in range(4000, 7000) if case_a(b) == 0)
    hi = max(b for b in range(5000, 7000, 1) if case_b(b) == 1) if case_b(5000) == 1 else None
    print(f"(a) passes (no restart) from bound {lo}; (b) passes (one restart) up to bound {hi}")


def _alias_case(args):
    ppm, start, L = args
    base_g = 40
    n0 = base_g * 16 + start
    m = Meter()
    run_stream(m, n0 + L + 64 * 16, ts_maker(ppm, lambda n: 0), set(range(n0, n0 + L)))
    touched = (n0 + L - 1) // 16 - n0 // 16 + 1
    return ppm, start, L, touched, len(m.restarts)


def sec_alias():
    from multiprocessing import Pool
    cases = [(ppm, st, L) for ppm in (0, 300, -300) for st in range(16)
             for L in range(1, 601)]
    with Pool(8) as pool:
        rows = pool.map(_alias_case, cases, chunksize=64)
    bad = [r for r in rows if r[4] != (0 if r[3] == 1 else 1)]
    print(f"alias sweep: {len(rows)} cases (ppm 0, +300, -300; start PDU 0..15; runs of 1..600 PDUs)")
    print(f"cases not matching 'one restart iff two or more groups voided': {len(bad)}")
    for r in bad[:40]:
        print("  ", r)
    page = [(0, st, L) for st in (0, 5) for L in [16 * x for x in range(2, 34)] + [255, 256, 257, 512]
            if not (st == 5 and L % 16 == 0 and L not in (256, 512))]
    pr = [_alias_case(c) for c in page]
    print(f"page cases (whole runs of 2..33 groups from PDU 0; 255/256/257/512 PDUs from PDU 0 and 5): "
          f"{len(pr)} cases, restarts == 1 in {sum(1 for r in pr if r[4] == 1)}")
    print("one whole lost group: restarts", _alias_case((0, 0, 16))[4])
    print("k = 0 (15 whole voided groups, 16 intervals): restarts", _alias_case((0, 0, 240))[4])


def sec_fill():
    # snapshot group at count 3 x 256 after the history start (group 0)
    G = 3 * 256
    lost = {G * 16 + 5}
    a, b = Meter(), Meter()
    ts = ts_maker(100, lambda n: 0)
    ra, rb = [], []
    n_end = 12 * 256 * 16
    for n in range(n_end):
        if n not in lost:
            a.pdu(n, n % 256, ts(n))
        b.pdu(n, n % 256, ts(n))
        if n % (256 * 16) == 16 * 16 and a.rate_valid:
            ra.append(a.rate)
            rb.append(b.rate)
    diff = max(abs(x - y) for x, y in zip(ra, rb))
    print(f"fill: restarts {len(a.restarts)}; rates compared {len(ra)}; largest difference {diff} ns")
    # a rate change inside the 4 ms: midpoint error per ppm of change
    worst = 0
    for cut in range(0, 32):
        def t2(n, cut=cut):
            base = G * 16 - 16 + cut
            v = n * NOM
            if n > base:
                v += ((n - base) * NOM * 50) // 1_000_000
            return v
        p_prev = sum(t2((G - 1) * 16 + i) - i * NOM for i in range(16)) // 16
        p_next = sum(t2((G + 1) * 16 + i) - i * NOM for i in range(16)) // 16
        p_true = sum(t2(G * 16 + i) - i * NOM for i in range(16)) // 16
        mid = p_prev + ((p_next - p_prev) >> 1)
        worst = max(worst, abs(mid - p_true))
    print(f"fill: a 50 ppm rate change at any of 32 PDU positions in the 4 ms moves the midpoint off the true pick by at most {worst} ns ({worst / 50:.2f} ns per ppm)")


def _leg(mutant, step_ppm, lead_s=40, leg_s=60, tail_s=20, J=1426):
    rng = random.Random(3)
    ppm0 = 20
    leg0 = int(lead_s * 8000)
    leg1 = leg0 + int(leg_s * 8000)
    lost = set(range(leg0 + 2400, leg1, 2400))   # one PDU every 0.3 s
    m = {"design": Meter(), "held_lock_cleared": Meter(clear_lock_on_gap=True),
         "restart_any_loss": Meter(restart_on_any_loss=True)}[mutant]
    err = uniform_err(9, J)

    def ts(n):
        v = (n * NOM * (1_000_000 + ppm0)) // 1_000_000
        if n >= leg0 and step_ppm:
            v += ((n - leg0) * NOM * step_ppm) // 1_000_000
        return v + err(n)
    s = Servo(130_000_000, 0, rng)
    # local plant offset: the plan's L0; the talker's offset is in the rate
    run_stream(m, leg1 + int(tail_s * 8000), ts, lost, s)
    return m, s, leg0 * NOM, leg1 * NOM, lost


def sec_servoleg():
    for mut in ("design", "held_lock_cleared", "restart_any_loss"):
        m, s, t0, t1, lost = _leg(mut, 4)
        in_leg = [x for x in s.log if t0 <= x[0] <= t1]
        left = [x for x in in_leg if x[1] == "LOCKED"]
        hold = sum(1 for x in in_leg if x[2] == "HOLDOVER")
        relock = [x[0] for x in s.log if x[2] == "LOCKED" and x[0] > t0]
        # trim against the talker after the step: u tracks L0 - talker
        target = L0 - (24 * 512)
        final_off = (L0 - s.u) - 24 * 512
        print(f"{mut}: first LOCKED {s.first_locked/1e9 if s.first_locked else None:.3f} s; "
              f"restarts in leg {sum(1 for r in m.restarts if t0 <= r*NOM <= t1)}; "
              f"LOCKED left in leg {len(left)} (first at {left[0][0]/1e9 if left else None}); "
              f"HOLDOVER entries in leg {hold}; LOCKED regained after leg start at "
              f"{[round(x/1e9,3) for x in relock][:3]}; first lost PDU at {min(lost)*NOM/1e9:.3f} s; "
              f"leg ends {t1/1e9:.3f} s; trim off the +24 ppm talker at the end: {final_off/512:.2f} ppm")


def sec_counter():
    for mut in ("design", "held_lock_cleared", "restart_any_loss"):
        m, s, t0, t1, lost = _leg(mut, 0)
        unl = [x[0] for x in s.log if x[1] == "LOCKED" and x[0] >= t0]
        lck = [x[0] for x in s.log if x[2] == "LOCKED" and x[0] >= t0]
        unl_leg = [x for x in unl if x <= t1]
        lck_leg = [x for x in lck if x <= t1]
        after = [round((x - t1) / 1e9, 3) for x in lck if x > t1]
        print(f"{mut}: C1 UNLOCKED moves in leg {len(unl_leg)} (at {[round(x/1e9,3) for x in unl_leg][:2]}); "
              f"LOCKED moves in leg {len(lck_leg)}; LOCKED regained {after[:1]} s after the leg ends; "
              f"meter lock held through leg: {not any(True for x in s.log if x[2]=='HOLDOVER' and t0<=x[0]<=t1)}")


if __name__ == "__main__" and sys.argv[1] != "legtrim":
    {"steps": sec_steps, "gapbound": sec_gapbound, "alias": sec_alias,
     "fill": sec_fill, "servoleg": sec_servoleg, "counter": sec_counter}[sys.argv[1]]()


def sec_legtrim():
    """The servo-with-meter row's trim check, taken at the loss leg's end."""
    for mut in ("design", "held_lock_cleared", "restart_any_loss"):
        m, s, t0, t1, lost = _leg(mut, 4, tail_s=0)
        off = ((L0 - s.u) - 24 * 512) / 512
        print(f"{mut}: at the loss leg's end the trim is {off:+.2f} ppm off the +24 ppm talker "
              f"(row: within 0.5 ppm); state {s.state}; LOCKED left in leg "
              f"{sum(1 for x in s.log if x[1] == 'LOCKED' and t0 <= x[0] <= t1)}")


if __name__ == "__main__" and sys.argv[1] == "legtrim":
    sec_legtrim()
