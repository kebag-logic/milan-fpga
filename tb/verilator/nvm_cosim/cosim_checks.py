#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Every NAMED check of the saved-state co-simulation, and its case metadata.

`cosim_cases.cpp` is stimulus only: it drives the control face, the producer
and the injected failures, and dumps the journal slots and a status
observation at named points. Every verdict is taken here, against the oracle
in `cosim_oracle.py`.

A check is a ``(name, function)`` pair. The NAME is what
``docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md`` cites and what
``run_cases.py`` requires each mutant to be killed by, so renaming one
silently re-aims a mutant: the page and this module are read together.
"""
from __future__ import annotations

import struct

from cosim_oracle import (      # noqa: F401  (B and F are the case file's own
    B, CLK_HZ, Ctx, F, Run,     #  bindings, framed here for the checks below)
    ShapeInfo, TAG_C3, T_HOLD_MS, VD_OK, _bind_frame, _crc16, _erased,
    _frame, klj2_decode)

def _ck(name, fn):
    return (name, fn)


def _c_rec(tag, rid, key, label):
    def _f(c):
        got = c.rec(tag, rid)
        if got is None:
            return False, f"no accepted slot at {tag}"
        ok = got == F[key]
        what = ("expected " + key if ok
                else "ERASED" if _erased(got) else got.hex())
        return ok, f"record 0x{rid:02x} at {tag}: {what}"
    return _ck(f"{label}@{tag}:0x{rid:02x}", _f)


def _c_rec_in(tag, rid, keys, label):
    def _f(c):
        got = c.rec(tag, rid)
        if got is None:
            return False, f"no accepted slot at {tag}"
        hit = [k for k in keys if F[k] == got]
        return bool(hit), f"record 0x{rid:02x} at {tag}: {hit[0] if hit else ('ERASED' if _erased(got) else got.hex())}"
    return _ck(f"{label}@{tag}:0x{rid:02x}", _f)


def _c_converged(tag, want):
    """Convergence is the records AND the published status: once changes
    stop, the slot holds them, nothing is committable, and the status claims
    durability again. A bit held at 1 to make a safety check pass (nvm_dirty
    or the pending bit) fails here."""
    def _f(c):
        bad = [f"0x{r:02x}" for r, k in want.items() if c.rec(tag, r) != F[k]]
        di = c.dirty_img(tag)
        claim = c.durable_claim(tag)
        return (not bad and di == 0 and claim), \
            f"mismatched {bad or 'none'}, committable work {di}, status claims durable {claim}"
    return _ck(f"converged@{tag}", _f)


def _c_arm_in_gap(rid):
    """The case really placed the arm between the port's ERASE completion and
    the grant of the WRITE that completes the same logical record."""
    def _f(c):
        if "erase_done_before_arm" not in c.r.notes:
            return None, "hook not reached on this build"
        t = c.r.notes["erase_done_before_arm"]["value"]
        arm = min([a for a in _strobes(c, 0x8) if a >= t], default=None)
        er = [o for o in _op_evts(c, "port", rid, 2) if o["end"] and o["end"] <= t]
        wr = [o for o in _op_evts(c, "port", rid, 1) if er and o["req"] >= er[-1]["end"]]
        if arm is None or not er or not wr:
            return False, "no ERASE, WRITE and arm to order"
        ok = er[-1]["end"] <= arm <= wr[0]["gnt"]
        return ok, (f"ERASE done at {er[-1]['end']}, arm at {arm}, WRITE requested at "
                    f"{wr[0]['req']} and granted at {wr[0]['gnt']}")
    return _ck(f"arm_inside_erase_write_gap:0x{rid:02x}", _f)


def _c_inflight_at_arm(rid):
    """Revision b premise of A11: the BFM WRITE was GRANTED before the arm
    edge and was still in flight at it (not requested on the arm's own
    edge, which is deferred now)."""
    def _f(c):
        wr = [o for o in _op_evts(c, "bfm", rid, 1)]
        arms = _strobes(c, 0x8)
        if not wr or not arms:
            return None, "no WRITE or no arm on this build"
        w = wr[-1]
        arm = min([a for a in arms if a >= w["gnt"]], default=None)
        ok = arm is not None and w["gnt"] < arm < w["end"]
        gnt = w["gnt"] - arm if arm else None
        end = w["end"] - arm if arm else None
        return ok, (f"WRITE granted {gnt} relative to the arm, "
                    f"ends {end}")
    return _ck(f"write_in_flight_at_arm:0x{rid:02x}", _f)


def _c_copy_in_gap(rid):
    """The ERASE was granted before the arm, completed with done before the
    firmware read the ownership vector, and the WRITE of the same logical
    record was requested before that read and granted only at or after the
    attestation: the capture looked at the record inside the gap."""
    def _f(c):
        if "gap_observed" not in c.r.notes:
            return None, "hook not reached on this build"
        t = c.r.notes["gap_observed"]["value"]
        arm = max([a for a in _strobes(c, 0x8) if a <= t], default=None)
        cert = min([x for x in _strobes(c, 0x10) if x >= t], default=None)
        er = [o for o in _op_evts(c, "port", rid, 2)
              if arm is not None and o["gnt"] <= arm and o["end"] and o["end"] <= t]
        wr = [o for o in _op_evts(c, "port", rid, 1) if er and o["req"] >= er[-1]["end"]]
        if arm is None or cert is None or not er or not wr:
            return False, "no ERASE, arm, gap and WRITE to order"
        e, w = er[-1], wr[0]
        ok = e["gnt"] <= arm and e["end"] <= t < cert <= w["gnt"] and w["req"] < t
        return ok, (f"relative to the arm: ERASE granted {e['gnt'] - arm}, done {e['end'] - arm}; "
                    f"ownership read after {t - arm}; WRITE requested {w['req'] - arm}, granted "
                    f"{w['gnt'] - arm}; attestation {cert - arm}")
    return _ck(f"capture_inside_erase_write_gap:0x{rid:02x}", _f)


def _c_ack_only_slot(tag, rid, key):
    def _f(c):
        in_slot = c.rec(tag, rid) == F[key]
        di = c.dirty_img(tag)
        return (in_slot or di == 1), f"newer record in slot {in_slot}, still owned (dirty) {di}"
    return _ck(f"ack_retires_only_slot@{tag}:0x{rid:02x}", _f)


def _c_no_durable_claim(tag, accepted):
    def _f(c):
        missing = [f"0x{r:02x}" for r, k in accepted.items() if c.rec(tag, r) != F[k]]
        claim = c.durable_claim(tag)
        return not (missing and claim), (
            f"accepted but not in the slot {missing or 'none'}; "
            f"status claims durable {claim}")
    return _ck(f"no_durable_claim@{tag}", _f)


def _c_alarm_revokes(tag):
    def _f(c):
        o = c.o(tag)
        return not (o["alarm"] and o["backed"]), f"alarm {o['alarm']} backed {o['backed']}"
    return _ck(f"alarm_revokes@{tag}", _f)


def _c_no_101():
    def _f(c):
        last = max(c.r.obs.values(), key=lambda o: o["cycle"])
        return last["bad101"] == 0, f"cycles holding (backed 1, dirty 0, stale 1): {last['bad101']}"
    return _ck("unreachable_row_never_held", _f)


def _c_stuck_reported(tag):
    def _f(c):
        o = c.o(tag)
        return o["dev_busy"] == 1 and not c.durable_claim(tag), (
            f"dev_busy {o['dev_busy']} durable claim "
            f"{c.durable_claim(tag)}")
    return _ck(f"stuck_record_reported@{tag}", _f)


def _c_unres_bits(tag, rids):
    def _f(c):
        if not c.contract(tag):
            return None, "no ownership vector on this build"
        own = c.o(tag)["own"]
        got = sorted(w * 32 + b for w in range(8) for b in range(32) if (own[w] >> b) & 1)
        return got == sorted(rids), f"open records {[hex(x) for x in got]}"
    return _ck(f"open_records_named@{tag}", _f)


def _c_first_boot_blank(tag):
    def _f(c):
        n = c.newest(tag)
        if n is None:
            return False, "no accepted slot"
        bad = [hex(r) for r in c.s.recs if not _erased(c.rec(tag, r))]
        return not bad, f"framed records {bad or 'none'} (all must be _erased)"
    return _ck(f"first_boot_erased_image_accepted@{tag}", _f)


def _op_evts(c, src=None, rid=None, op=None):
    return [e for e in c.r.evts if e["k"] == "op" and (src is None or e["src"] == src)
            and (rid is None or e["rid"] == rid) and (op is None or e["op"] == op)]


def _strobes(c, bit):
    return [e["cyc"] for e in c.r.evts if e["k"] == "strobe" and e["v"] & bit and not e["stray"]]


def _held_op(c, src, rid):
    """The first ERASE of this source on this record REQUESTED while a
    capture was open and not yet attested or released, with that capture's
    arm: the request the hold must defer. An earlier operation on the same
    record (the base bindings the real manager flushes before any capture)
    is not it, which is why this is not simply the first operation."""
    arms = _strobes(c, 0x8)
    ends = sorted(_strobes(c, 0x10) + _strobes(c, 0x20))
    for op in _op_evts(c, src, rid, 2):
        arm = max([a for a in arms if a <= op["req"]], default=None)
        if arm is None:
            continue
        end = min([x for x in ends if x >= arm], default=None)
        if end is None or op["req"] <= end:
            return op, arm
    return None, None


def _c_deferred(rid, src="bfm"):
    def _f(c):
        if not _op_evts(c, src, rid, 2) or not _strobes(c, 0x8):
            return None, "no request or no capture on this build"
        op, arm = _held_op(c, src, rid)
        if op is None:
            return False, "no request landed inside a capture"
        cert = min([x for x in _strobes(c, 0x10) if x >= arm], default=None)
        if cert is None:
            return False, f"request at {op['req']}: its capture was never attested"
        ok = op["gnt"] >= cert and op["gnt"] - arm <= T_HOLD_MS * 1000 + 1000
        return ok, (f"requested {op['req'] - arm} cycles after the arm, "
                    f"granted {op['gnt'] - arm} after it, attestation at "
                    f"{cert - arm}")
    return _ck(f"deferred_until_attestation:0x{rid:02x}" + ("" if src == "bfm" else f":{src}"), _f)


def _c_hold_bounded(rid, src="bfm"):
    def _f(c):
        if not _op_evts(c, src, rid, 2) or not _strobes(c, 0x8):
            return None, "no request or no capture on this build"
        op, arm = _held_op(c, src, rid)
        if op is None:
            return False, "no request landed inside a capture"
        d = op["gnt"] - arm
        lo, hi = (T_HOLD_MS - 1) * 1000, (T_HOLD_MS + 1) * 1000
        return lo <= d <= hi, f"held {d} cycles (bound {T_HOLD_MS} ms = {T_HOLD_MS * 1000})"
    return _ck(f"hold_bounded:0x{rid:02x}" + ("" if src == "bfm" else f":{src}"), _f)


def _c_no_uncert_flash():
    def _f(c):
        if not _strobes(c, 0x8):
            return None, "no capture on this build"
        refused = [ln for ln in c.r.fw if "not attested" in ln]
        return bool(refused), f"refused captures reported: {len(refused)}"
    return _ck("unattested_capture_never_flashed", _f)


def _c_slow_copy():
    def _f(c):
        if not _strobes(c, 0x8):
            return None, "no capture on this build"
        refused = [ln for ln in c.r.fw if "not attested" in ln]
        return not refused, f"refused captures {len(refused)}"
    return _ck("slow_copy_attests", _f)


def _c_arm_refused(tag):
    def _f(c):
        if "capid_before_stray" not in c.r.notes:
            return None, "hook not reached on this build"
        o = c.o(tag)
        st = o["stat"]
        before = c.r.notes["capid_before_stray"]["value"]
        ok = (st >> 21) & 1 and (st >> 16) & 1 and o["capid"] == before
        return bool(ok), f"arm_refused {(st >> 21) & 1} open {(st >> 16) & 1} id {before}->{o['capid']}"
    return _ck(f"concurrent_arm_refused@{tag}", _f)


def _c_own_ack_ok():
    def _f(c):
        refused = [ln for ln in c.r.fw if "REFUSED" in ln]
        return not refused, f"refused acknowledgements {len(refused)}"
    return _ck("own_acknowledgements_accepted", _f)


def _c_stale_id_refused(tag):
    def _f(c):
        if "open_capture_id" not in c.r.notes:
            return None, "hook not reached on this build"
        st = c.o(tag)["stat"]
        ok = (st >> 20) & 1 and (st >> 16) & 1 and (st >> 8) & 1
        return bool(ok), f"ack_refused {(st >> 20) & 1} capture open {(st >> 16) & 1} work owned {(st >> 8) & 1}"
    return _ck(f"stale_identity_refused@{tag}", _f)


def _c_late_ack(tag):
    def _f(c):
        o = c.o(tag)
        return c.dirty_img(tag) == 0 and o["backed"] == 0, f"committable work {c.dirty_img(tag)} backed {o['backed']}"
    return _ck(f"late_ack_accepted_not_resurrecting@{tag}", _f)


def _c_refused_ack(tag):
    def _f(c):
        if not _strobes(c, 0x8):
            return None, "no capture on this build"
        refused = [ln for ln in c.r.fw if "REFUSED" in ln]
        return bool(refused) and c.dirty_img(tag) == 1, (
            f"refusal reported {bool(refused)}, work still owned "
            f"{c.dirty_img(tag)}")
    return _ck(f"refused_ack_retires_nothing@{tag}", _f)


def _c_bits(tag, backed, dirty, stale):
    def _f(c):
        o = c.o(tag)
        got = (o["backed"], o["dirty_pub"], o["stale"])
        return got == (backed, dirty, stale), f"(backed, dirty, stale) {got}"
    return _ck(f"status@{tag}=({backed},{dirty},{stale})", _f)


def _c_unmaterialized(tag):
    def _f(c):
        o = c.o(tag)
        live = o["dyn_fmt0_v"] == 1
        slot = c.rec(tag, 0x30)
        missing = live and (slot is None or _erased(slot))
        claim = c.durable_claim(tag)
        where = "erased" if _erased(slot) else slot
        return not (missing and claim), (
            f"live format set {live}, record 0x30 in slot {where}, "
            f"durable claim {claim}")
    return _ck(f"no_durable_claim_unmaterialized@{tag}", _f)


def _c_no_churn_pend(tag):
    def _f(c):
        if not c.contract(tag):
            return None, "no pending state on this build"
        return c.o(tag)["erases"] == 0, f"erases {c.o(tag)['erases']}"
    return _ck(f"pending_drives_no_commit@{tag}", _f)


def _c_failure_revokes(at_report):
    def _f(c):
        hooks = [e for e in c.r.evts if e["k"] == "hook" and e["name"] == "w_stat"
                 and 11 <= (e["v"] & 0xF) <= 13]
        if not hooks:
            return False, "no failure was reported"
        rep = hooks[0]["cyc"]
        losses = [e["cyc"] for e in c.r.evts if e["k"] == "loss" and e["cyc"] >= rep]
        if at_report:
            if not c.contract():
                return None, "the tracked module revokes by the commit deadline"
            ok = bool(losses) and losses[0] - rep <= 5
        else:
            ok = bool(losses) and losses[0] - rep <= 10_000_000
        return ok, f"reported at {rep}, first loss {losses[0] - rep if losses else None} cycles later"
    return _ck("failure_revokes_at_report" if at_report else "failure_revokes", _f)


def _c_producer_never_blocked():
    def _f(c):
        ops = _op_evts(c, "port")
        if not ops:
            return False, "no producer operation"
        worst = max(o["gnt"] - o["req"] for o in ops)
        return worst <= T_HOLD_MS * 1000 + 1000, (
            f"longest request-to-grant wait {worst} cycles over "
            f"{len(ops)} operations")
    return _ck("producer_wait_bounded_by_hold", _f)


def _c_no_loss():
    def _f(c):
        n = len([e for e in c.r.evts if e["k"] == "loss"])
        return n == 0, f"backed fell {n} time(s)"
    return _ck("no_revocation_from_concurrent_update", _f)


def _c_hb_gap(limit_ms):
    def _f(c):
        last = max(c.r.obs.values(), key=lambda o: o["cycle"])
        return last["hb_max_gap_ms"] <= limit_ms, f"largest heartbeat gap {last['hb_max_gap_ms']} ms"
    return _ck(f"heartbeat_gap<={limit_ms}ms", _f)


def _c_stable(t0, t1):
    def _f(c):
        e0, e1 = c.o(t0)["erases"], c.o(t1)["erases"]
        return e1 == e0 and c.dirty_img(t1) == 0, f"erases {e0}->{e1}"
    return _ck("stable_no_churn", _f)


def _c_dirty_img(tag, want, label):
    def _f(c):
        return c.dirty_img(tag) == want, f"committable work {c.dirty_img(tag)}"
    return _ck(f"{label}@{tag}", _f)


def _c_attest_voided(tag):
    def _f(c):
        if not c.contract(tag):
            return None, "no attestation on this build"
        st = c.o(tag)["stat"]
        held = c.r.notes.get("deferred_while_hold", {}).get("value", 1) == 0
        return (not (st >> 19) & 1) and held, f"attested {(st >> 19) & 1}, deferred during the hold {held}"
    return _ck(f"grant_on_attest_edge_voids@{tag}", _f)


def _c_restore(tag, want):
    def _f(c):
        pre = {p["sink"]: p for p in c.o(tag)["preloads"]}
        bad = []
        for sink, key in want.items():
            if key is None:
                continue
            _sink, (_bound, started, _sw), (uid, teid, ceid) = B[key]
            p = pre.get(sink)
            if p is None or int(p["teid"], 16) != teid or p["uid"] != uid or \
                    int(p["ceid"], 16) != ceid or p["started"] != started:
                bad.append(f"sink {sink}: {p}")
        return not bad, f"restored {sorted(pre)}; mismatches {bad or 'none'}"
    return _ck(f"restores_last_verified@{tag}", _f)


def _c_pend_bit():
    """PP_NVM_STAT[22] IS the pending bit the port publishes, at every
    observation of a build that carries the contract (revision b: one wire)."""
    def _f(c):
        bad = [t for t, o in c.r.obs.items()
               if (o["stat"] >> 24) == TAG_C3 and ((o["stat"] >> 22) & 1) != o["pend"]]
        return not bad, f"observations where PP_NVM_STAT[22] differs from nvm_pend: {bad or 'none'}"
    return _ck("pending_bit_is_status_bit_22", _f)


# ---------------------------------------------------- revision b: the load
def _all_strobes(c, bit):
    """Every strobe carrying `bit`, stray or not: the unit cases write theirs
    by hand, so they are all stray."""
    return [e["cyc"] for e in c.r.evts if e["k"] == "strobe" and e["v"] & bit]


def _live_rec(c, tag, rid):
    """The record's bytes in the LIVE window at the observation."""
    raw = (c.r.outdir / f"{tag}-live.bin").read_bytes()
    off, ln = c.s.recs[rid]
    return raw[40 + off:40 + off + ln]


def _own_bit(c, tag, rid):
    return (c.o(tag)["own"][rid >> 5] >> (rid & 31)) & 1


def _show(b, key):
    return "expected " + key if b == F[key] else ("ERASED" if _erased(b) else b.hex())


def _c_every_slot(tag, rid, key):
    """EVERY slot that validates holds the record, not just the newest: what a
    power cycle at any later point could restore."""
    def _f(c):
        got = []
        for letter in "AB":
            raw = (c.r.outdir / f"{tag}-slot{letter}.bin").read_bytes()
            n = struct.unpack_from("<I", raw, 16)[0] if raw[:4] != b"\xff" * 4 else 0
            blob = raw[:n] if 44 <= n <= 65536 else raw[:44]
            vd, _ = klj2_decode(blob, c.s.donor, c.s.ident, c.s.expect)
            if vd == VD_OK:
                off, ln = c.s.recs[rid]
                got.append(f"{letter}: {_show(blob[40 + off:40 + off + ln], key)}")
        ok = bool(got) and all(g.endswith("expected " + key) for g in got)
        return ok, f"verified slots {got or 'none'}"
    return _ck(f"every_verified_slot_keeps@{tag}:0x{rid:02x}", _f)


def _c_no_claim_over_erased_live(tag, rid):
    def _f(c):
        live, claim = _live_rec(c, tag, rid), c.durable_claim(tag)
        return not (_erased(live) and claim), \
            f"live record 0x{rid:02x} erased {_erased(live)}, status claims durable {claim}"
    return _ck(f"no_durable_reading_over_erased_live@{tag}:0x{rid:02x}", _f)


def _c_reload_retried(tag):
    def _f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        st = c.o(tag)["stat"]
        said = any("refused 1 window load(s); accepted at attempt 2" in ln for ln in c.r.fw)
        return said and not (st >> 3) & 1, \
            f"one refusal then acceptance reported {said}, load pending {(st >> 3) & 1}"
    return _ck(f"reload_refused_then_reloaded@{tag}", _f)


def _c_arm_edge_deferred(rid):
    """The ERASE was requested in the ARM's own cycle and granted only after
    the attestation: the hold covers the arm edge itself."""
    def _f(c):
        if not c.contract("arm"):
            return None, "no arm on this build"
        arms, att = _all_strobes(c, 0x8), _all_strobes(c, 0x10)
        ops = [o for o in _op_evts(c, "bfm", rid, 2) if arms and o["req"] == arms[-1]]
        if not arms or not att or not ops:
            return False, "no ERASE requested in the arm's own cycle"
        op, arm = ops[0], arms[-1]
        a = min([x for x in att if x > arm], default=None)
        ok = a is not None and op["gnt"] > a
        return ok, (f"ERASE requested in the arm's cycle, granted {op['gnt'] - arm} cycles after "
                    f"it, attestation at {a - arm if a is not None else None}")
    return _ck(f"arm_edge_request_deferred:0x{rid:02x}", _f)


def _c_own_exact_after_arm(tag, rid):
    def _f(c):
        if not c.contract(tag):
            return None, "no ownership vector on this build"
        busy, bit = c.o(tag)["dev_busy"], _own_bit(c, tag, rid)
        return not (busy and not bit), \
            f"first cycle after the arm edge: dev_busy {busy}, record 0x{rid:02x} open {bit}"
    return _ck(f"ownership_exact_after_arm@{tag}:0x{rid:02x}", _f)


def _c_attest_intact(tag, rid, key):
    def _f(c):
        if not c.contract(tag):
            return None, "no attestation on this build"
        att, live = (c.o(tag)["stat"] >> 19) & 1, _live_rec(c, tag, rid)
        return att == 1 and live == F[key], f"attested {att}, live record 0x{rid:02x} {_show(live, key)}"
    return _ck(f"attested_over_intact_record@{tag}:0x{rid:02x}", _f)


def _c_refused_open(tag, rid, label):
    """The RELOAD was refused and the record still reads open."""
    def _f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        ref, bit = (c.o(tag)["stat"] >> 11) & 1, _own_bit(c, tag, rid)
        return ref == 1 and bit == 1, f"reload refused {ref}, record 0x{rid:02x} open {bit}"
    return _ck(f"{label}@{tag}:0x{rid:02x}", _f)


def _c_closed_equals_load(tag, rid, key):
    """A record that reads closed holds exactly what the load wrote."""
    def _f(c):
        if not c.contract(tag):
            return None, "no ownership vector on this build"
        bit, live = _own_bit(c, tag, rid), _live_rec(c, tag, rid)
        return bit == 1 or live == F[key], f"record 0x{rid:02x} open {bit}, live {_show(live, key)}"
    return _ck(f"closed_record_equals_load@{tag}:0x{rid:02x}", _f)


def _c_held_work(tag):
    def _f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        o = c.o(tag)
        ref = (o["stat"] >> 11) & 1
        ok = c.dirty_img(tag) == 1 and o["pend"] == 1 and ref == 1
        return ok, f"committable work {c.dirty_img(tag)}, pending {o['pend']}, reload refused {ref}"
    return _ck(f"held_work_survives_post_boot_reload@{tag}", _f)


RESET_ROW = {"open": (16, 0), "hold": (17, 0), "valid": (18, 0), "attested": (19, 0),
             "ack_refused": (20, 0), "arm_refused": (21, 0), "pend_bit": (22, 1),
             "committable": (8, 0), "img_cfg": (5, 0), "img_valid": (7, 0),
             "load_pending": (3, 1), "load_accepted": (2, 0), "reload_refused": (11, 0)}


def _c_reset_row(tag):
    """The reset row of the capture machine: the page's table, bit by bit."""
    def _f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        bad = {k: (st >> b) & 1 for k, (b, v) in RESET_ROW.items() if (st >> b) & 1 != v}
        for k, v in (("capid", 0), ("pend", 1), ("backed", 0), ("stale", 0)):
            if o[k] != v:
                bad[k] = o[k]
        own = sorted(w * 32 + b for w in range(8) for b in range(32) if (o["own"][w] >> b) & 1)
        every = own == sorted(c.s.recs)
        #! [2] load accepted is 0 in the row, and it is what refuses an ARM
        #! after reset: the image is not configured either, but the
        #! accepted-load term of section 5.3 rule 9 refuses one even after a
        #! writer configures and validates the window (issue #484)
        return not bad and every, (f"mismatches {bad or 'none'}; every allocated record open "
                                   f"{every} ({len(own)} of {len(c.s.recs)}); an ARM here is "
                                   f"refused by the accepted-load term, [2] = {(st >> 2) & 1}")
    return _ck(f"reset_row@{tag}", _f)


def _c_early_ack(tag):
    def _f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        ok = (st >> 20) & 1 and not (st >> 16) & 1 and o["capid"] == 0
        return bool(ok), f"ack refused {(st >> 20) & 1}, capture open {(st >> 16) & 1}, id {o['capid']}"
    return _ck(f"pre_reset_ack_refused@{tag}", _f)


def _c_reattached(tag):
    def _f(c):
        if not c.contract(tag):
            return None, "no restart model on this build"
        ref = (c.o(tag)["stat"] >> 11) & 1
        said = any("re-attached" in ln for ln in c.r.fw)
        ok = said and not ref and c.dirty_img(tag) == 1
        return ok, (f"re-attach reported {said}, reload refused {ref}, "
                    f"committable work kept {c.dirty_img(tag)}")
    return _ck(f"restart_reattaches@{tag}", _f)


def _c_grant_wins_rebase(tag, rid):
    """Revision c: the mutating grant landed on the LAST re-base write's own
    edge, and the load flag stayed clear -- the RELOAD is refused and the
    record the ERASE blanked still reads open. Nothing was in flight at that
    edge, so only the priority between the two arms can refuse it."""
    def _f(c):
        if not c.contract(tag):
            return None, "no RELOAD on this build"
        ops = _op_evts(c, "bfm", rid, 2)
        rb = c.r.notes.get("rebase_cycle", {}).get("value")
        if not ops or rb is None:
            return False, "no ERASE and no recorded re-base cycle"
        # dev_gnt_o is REGISTERED: a grant decided on the edge that ends
        # cycle N (the edge the re-base write is applied on) is seen at N+1
        same = ops[0]["gnt"] == rb + 1
        ref, bit = (c.o(tag)["stat"] >> 11) & 1, _own_bit(c, tag, rid)
        return same and ref == 1 and bit == 1, \
            (f"grant registered at {ops[0]['gnt']}, decided on the re-base write's own edge "
             f"{rb} ({same}), reload refused {ref}, record 0x{rid:02x} open {bit}")
    return _ck(f"grant_wins_over_rebase_edge@{tag}:0x{rid:02x}", _f)


def _c_hold_bounded_chained(rid):
    """Revision c: a request deferred by one capture is granted at most
    T_HOLD_MS_P after it was raised, THOUGH a second arm followed the first
    capture's end in the adjacent cycle."""
    def _f(c):
        ops, arms = _op_evts(c, "bfm", rid, 2), _all_strobes(c, 0x8)
        if not ops or len(arms) < 2:
            return None, "no chained captures on this build"
        op = ops[0]
        d = op["gnt"] - op["req"]
        return d <= (T_HOLD_MS + 1) * 1000, \
            (f"{len(arms)} arms, the second {arms[1] - arms[0]} cycles after the first; "
             f"request granted {d} cycles after it was raised (bound {(T_HOLD_MS + 1) * 1000})")
    return _ck(f"hold_bounded_across_captures:0x{rid:02x}", _f)


def _c_arm_refused_while_deferred(tag):
    def _f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        st = c.o(tag)["stat"]
        ref, open_b = (st >> 21) & 1, (st >> 16) & 1
        return ref == 1 and open_b == 0, f"arm refused {ref}, capture open {open_b}"
    return _ck(f"arm_refused_while_request_deferred@{tag}", _f)


#: the terminal row of section 5.3, bit by bit: the bits the STATE fixes,
#: whatever the ordering that reached it (revision d adds [2] load accepted,
#: which is 0 in every one of them). nvm_backed, nvm_stale and the
#: committable bit are NOT here: they depend on whether the writer ever
#: heartbeated before it retired, and each row grades them itself.
#: The bits the STATE fixes (issue #484, the acceptance reviews' first two
#: corrections). [23] unres and [22] nvm_pend are NOT here: they read 1, 1 at
#: the boot and FALL once no record is open, which W4 reaches by rewriting
#: every record whole. [11] reload refused, [21] arm refused and [20] ack
#: refused are not here either: each is decided by whether the writer strobed
#: the thing it reports, not by the state, and a writer that retires before it
#: ever arms leaves [21] at 0. All five are graded where the ordering fixes
#: them, by the arguments of c_terminal_row.
TERMINAL_ROW = {"open": (16, 0), "hold": (17, 0), "attested": (19, 0),
                "cap_valid": (18, 0),
                "commit_busy": (10, 0), "img_cfg": (5, 1),
                "img_valid": (7, 0), "load_pending": (3, 0), "load_accepted": (2, 0)}


def _c_terminal_row(tag, bits, said_text, label,
                   ordering=(("unres", 23, 1), ("pend_bit", 22, 1),
                             ("reload_refused", 11, 1), ("arm_refused", 21, 0),
                             ("ack_refused", 20, 0))):
    """What a controller reads in the terminal state: the bits the state
    fixes, and the three the ordering decides. The saved state is NOT
    restored in that boot although a verified slot exists: img_valid 0 and
    the walk's fail and blank say so, the pending bit is 1, no window load
    was accepted ([2] 0) so nothing in this boot may be captured, and the
    boot load is over ([3] 0) so no later RELOAD can close a record over the
    live window."""
    def _f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        o = c.o(tag)
        st = o["stat"]
        bad = {k: (st >> b) & 1 for k, (b, v) in TERMINAL_ROW.items() if (st >> b) & 1 != v}
        #! the bits the ORDERING decides, each with the value THIS ordering
        #! reaches: a lane that built its test from the fixed half alone would
        #! refuse a conforming implementation (issue #484)
        bad.update({k: (st >> b) & 1 for k, b, v in ordering if (st >> b) & 1 != v})
        backed, dirty, stale = bits
        for k, v in (("restore_done", 1), ("restore_fail", 1), ("blank", 1),
                     ("erases", 0), ("backed", backed), ("stale", stale)):
            if o[k] != v:
                bad[k] = o[k]
        if c.dirty_img(tag) != dirty:
            bad["committable"] = c.dirty_img(tag)
        said = any(said_text in ln for ln in c.r.fw)
        return not bad and said, (f"mismatches {bad or 'none'}, status 0x{st:08x}, "
                                  f"the writer reported it {said}")
    return _ck(f"{label}@{tag}", _f)


def _c_arm_refused_no_load(tag):
    """REVISION D, the new term: no capture is armed until a RELOAD has been
    accepted since reset. The image is configured and the writer's own
    validity bit is set, so nothing but the backend's own flag can refuse
    this ARM; the identity does not advance, so no acknowledgement can ever
    quote the capture that was not opened."""
    def _f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        acc, valid = (st >> 2) & 1, (st >> 7) & 1
        ref, open_b = (st >> 21) & 1, (st >> 16) & 1
        ok = acc == 0 and valid == 1 and ref == 1 and open_b == 0 and o["capid"] == 0
        return ok, (f"load accepted {acc}, img valid {valid}, arm refused {ref}, "
                    f"capture open {open_b}, capture identity {o['capid']}")
    return _ck(f"arm_refused_without_accepted_load@{tag}", _f)


def _c_no_capture_no_load(tag):
    """And nothing the control face does afterwards retires anything: with
    no capture open an ATTEST and an ACK are refused, so the work a closed
    record holds is still reported and no reading is durable."""
    def _f(c):
        if not c.contract(tag):
            return None, "no capture state on this build"
        o = c.o(tag)
        st = o["stat"]
        ok = (o["capid"] == 0 and (st >> 19) & 1 == 0 and (st >> 16) & 1 == 0
              and c.dirty_img(tag) == 1 and not c.durable_claim(tag))
        return ok, (f"capture identity {o['capid']}, attested {(st >> 19) & 1}, "
                    f"committable work {c.dirty_img(tag)}, status claims durable "
                    f"{c.durable_claim(tag)}")
    return _ck(f"no_capture_without_accepted_load@{tag}", _f)


def _c_repeat_stops_when_live(tag, want):
    """REVISION D, the writer half: once the window has GONE LIVE (load
    pending 0 with no accepted load) no later RELOAD can be accepted, so the
    writer stops repeating instead of re-basing and refilling a window the
    producer owns."""
    def _f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        st = c.o(tag)["stat"]
        strobed = len(_all_strobes(c, 0x40))
        live = any("window then went live" in ln for ln in c.r.fw)
        ok = live and strobed == want and (st >> 3) & 1 == 0 and (st >> 2) & 1 == 0
        return ok, (f"window went live {live}, RELOAD strobes {strobed} (want {want}), "
                    f"load pending {(st >> 3) & 1}, load accepted {(st >> 2) & 1}")
    return _ck(f"window_live_stops_the_repeat@{tag}", _f)


def _c_restart_stays_retired(tag):
    """REVISION D: a writer restarted in a boot whose window load was never
    accepted does NOT re-attach. It reads [2] and stays retired, so it
    publishes no validity bit over a window no load vouches for; and the
    backend's term refuses every ARM, so a writer that ignored the rule
    could capture nothing either."""
    def _f(c):
        if not c.contract(tag):
            return None, "no restart model on this build"
        o = c.o(tag)
        st = o["stat"]
        said = any("stays retired" in ln for ln in c.r.fw)
        re_att = any("re-attached" in ln for ln in c.r.fw)
        ok = (said and not re_att and (st >> 2) & 1 == 0 and o["capid"] == 0
              and (st >> 16) & 1 == 0 and not c.durable_claim(tag))
        return ok, (f"stayed retired {said}, re-attached {re_att}, load accepted "
                    f"{(st >> 2) & 1}, capture identity {o['capid']}, capture open "
                    f"{(st >> 16) & 1}, status claims durable {c.durable_claim(tag)}")
    return _ck(f"restart_stays_retired_without_load@{tag}", _f)


def _c_write_spans_fill(tag, rid):
    """The PREMISE of the re-review's probe H1, graded: a whole-record WRITE
    was granted before the last RELOAD strobe and ended with done after it,
    so the writer's own FILL wrote the record's bytes while that WRITE was
    streaming and the record now reads CLOSED over bytes the producer did
    not write. If the case fails to place that overlap it fails here rather
    than passing the checks below for the wrong reason."""
    def _f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        ops = _op_evts(c, "bfm", rid, 1)
        rl = _all_strobes(c, 0x40)
        if not ops or not rl:
            return False, "no BFM WRITE, or no RELOAD strobe"
        op, last = ops[-1], rl[-1]
        bit = _own_bit(c, tag, rid)
        ok = (op["gnt"] < last and op["end"] > last and "done" in op["res"] and bit == 0)
        return ok, (f"WRITE granted {op['gnt']}, last RELOAD strobe {last}, ended {op['end']} "
                    f"({op['res']}), record 0x{rid:02x} open {bit}")
    return _ck(f"write_spans_refused_fill@{tag}:0x{rid:02x}", _f)


def _c_nothing_durable_when_closed(tag):
    """The re-review's probe H2: every record rewritten whole, so nothing is
    left open by accident and the pending bit falls. The reading is still
    not durable and no slot was touched, because a boot with no accepted
    load captured nothing.

    ITS OWN PREMISE IS GRADED (issue #484). The check says something about a
    state in which NOTHING IS OPEN; a run that left a record open would reach
    the same verdict for a reason the check is not about, and would pass
    vacuously. So "records open 0 and pending 0" is required, not reported."""
    def _f(c):
        o = c.o(tag)
        nothing_open = (o["stat"] >> 23) & 1 == 0 and o["pend"] == 0
        ok = nothing_open and not c.durable_claim(tag) and o["erases"] == 0
        return ok, (f"records open {(o['stat'] >> 23) & 1}, pending {o['pend']}, backed "
                    f"{o['backed']}, committable {c.dirty_img(tag)}, status claims durable "
                    f"{c.durable_claim(tag)}, flash erases {o['erases']}, "
                    f"premise (nothing left open) {nothing_open}")
    return _ck(f"no_durable_reading_when_nothing_open@{tag}", _f)


def _c_boot_load_closed(tag):
    """Revision c, the construction itself: once the window has gone live --
    the restore walk's first read, or an enabled producer -- the boot load is
    over, whether or not one was ever accepted."""
    def _f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        st = c.o(tag)["stat"]
        return (st >> 3) & 1 == 0, f"load pending {(st >> 3) & 1}, reload refused {(st >> 11) & 1}"
    return _ck(f"boot_load_closed_when_live@{tag}", _f)


def _c_writer_retired(tag):
    """A writer that has disabled itself for this reset answers the liveness
    deadline no more, so the state reads as a port with NO writer and never
    as a commit in flight."""
    def _f(c):
        if not c.contract(tag):
            return None, "no window load on this build"
        o = c.o(tag)
        return o["backed"] == 0 and o["erases"] == 0, \
            f"backed {o['backed']}, pending {o['pend']}, flash erases {o['erases']}"
    return _ck(f"writer_absent_when_retired@{tag}", _f)


def _c_landed_or_reported(tag, rid, key):
    """The change the producer accepted ends in a verified slot, or is still
    reported as owned; never a durable reading over work no slot holds."""
    def _f(c):
        got = c.rec(tag, rid)
        in_slot = got == F[key]
        o = c.o(tag)
        reported = c.dirty_img(tag) == 1 or o["pend"] == 1
        claim = c.durable_claim(tag)
        return (in_slot or reported) and not claim, \
            (f"record 0x{rid:02x} in the newest verified slot {in_slot}, still reported "
             f"{reported}, status claims durable {claim}")
    return _ck(f"change_landed_or_reported@{tag}:0x{rid:02x}", _f)


def _c_restart_takes_no_cold_boot(tag):
    """Revision c: a writer restarted over a live window never reloads it.
    No RELOAD is accepted after the restart (the boot load is over), the
    change stays in the window and stays owned."""
    def _f(c):
        if not c.contract(tag):
            return None, "no restart model on this build"
        o = c.o(tag)
        st = o["stat"]
        cold = sum("refused 4 window loads" in ln for ln in c.r.fw) > 1
        said = any("re-attached" in ln or "stays disabled" in ln or "stays retired" in ln
                   for ln in c.r.fw)
        ok = said and not cold and (st >> 3) & 1 == 0 and c.dirty_img(tag) == 1
        return ok, (f"restart reported {said}, cold-boot path taken {cold}, load pending "
                    f"{(st >> 3) & 1}, committable work kept {c.dirty_img(tag)}")
    return _ck(f"restart_never_reloads_live_window@{tag}", _f)
