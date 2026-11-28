"""Replay a census trace's transmit commits through the shipping transmit queue at the MII rate (the 100 Mb/s egress
ruling on PR #1020, comment 7216971645, items 2(a) and 2(b); without the injected USB frame, as #1004 carries it).

Lane-local evidence tool, not the in-tree grader: that grader, with its planted defects, belongs to PR #1004's next
round. The model, from the RTL and the SoC as they stand:

* KL_mbx_tx serves records one at a time in commit order across the channels (SEQ order), one byte per mailbox
  cycle at 80 MHz, and moves TX_TAIL past a record only once its last byte is taken. A record is 2 header words and
  ceil(LEN / 4) payload words; the rings are the contract's (ADP 128, ACMP 256, AECP 512, MAAP 128, SRP 512 words).
* The control lane spaces its frames by the min-IFG gasket, 512 cycles at 50 MHz after each frame; the gPTP plane
  joins after the gasket; the AAF talkers and the CRF talker are the data lane. Each merge, and the MAC-boundary
  merge of the two lanes, is a round-robin frame arbiter (adp_tx_arbiter).
* MilanMAC's store-and-forward FIFO (512 x 8 B, 8 frame slots) releases a frame only once it is wholly buffered.
* The line: 80 ns an octet; a frame takes its preamble and SFD, max(LEN, 60) octets, the FCS and the 12-octet gap.
* The testbench's own holds (TXREADY 0, the held-egress groups) hold the mailbox's output here too, so this queue is
  never faster than the census's and a FULL there stays FULL here: (a) checks every committed record found room.

(a) Every commit's free-space test keeps its census outcome: at each TXC, the replayed ring holds the records still
    unsent ahead of it and the new ones, within the ring. The test ran in mbx_tx_begin before the commit, so the
    replay counts the ring as it stood MOVE_US before the TXC (the record mover's time is not credited as drain).
(b) The largest commit-to-last-octet wait, over records whose wait spans no testbench hold, plus 5 %, plus the
    fixed path, is at most 1000 us.

usage: egress_replay.py [--phases N] [--json OUT] LOG [LOG ...]
       egress_replay.py --selftest
"""
from __future__ import annotations

import argparse
import heapq
import json
import math
import re
import sys
from pathlib import Path

SYS_HZ = 80_000_000
OCTET_NS = 80                       # 100 Mb/s
GASKET_NS = 512 * 20                # tx_ifg_gasket GAP_CYCLES 512 at 50 MHz
MBX_BYTE_NS = 1e9 / SYS_HZ          # KL_mbx_tx: one byte a mailbox cycle
DATA_BYTE_NS = 1e9 / 50e6 / 8       # the 64-bit datapath lane at 50 MHz
RING_WORDS = (128, 256, 512, 128, 512)   # mbx_contract.h: ADP, ACMP, AECP, MAAP, SRP TX words
HDR_WORDS = 2
SF_FRAMES, SF_BYTES = 8, 512 * 8
MOVE_US = 20.0                      # a record's payload move before its commit, at most (not credited)
#: The fixed path: the pipeline between the mailbox and the line that the queue above does not model (the scan and
#: header of KL_mbx_tx, the mailbox and MAC crossings, the core's crossing to the MII clock and the PHY register
#: stages), bounded analytically: about 40 cycles at 50 MHz and 10 at 25 MHz, under 1.2 us, stated as 2 us. It is
#: not measured on the shipping chain here; the ruling's measured figure is owed to #1004's grader.
FIXED_PATH_US = 2.0
BOUND_US = 1000.0
MARGIN = 1.05


def line_octets(length: int) -> int:
    """Octets of line time a frame of `length` octets (no FCS) takes: preamble+SFD, padded frame, FCS, gap."""
    return 8 + max(length, 60) + 4 + 12


def last_octet_ns(length: int) -> int:
    """From the frame's first preamble octet to its last octet (FCS) on the line."""
    return (8 + max(length, 60) + 4) * OCTET_NS


#: The 4x4 shape's SR and gPTP egress, as (name, frame octets without FCS, period in ns, count each period).
#: AAF: four talkers, 2-channel 48 kHz PCM32: an 18-octet tagged header and the 72-octet AVTPDU (Milan v1.2 Table
#: 4.4's MaxFrameSize less its headroom octet), 8,000 a second each. CRF: 18 + 28 octets, 500 a second (Milan 7.3.2).
#: gPTP (IEEE 802.1AS-2020): Sync and Follow_Up at logSyncInterval -3, Announce, Pdelay_Req, Pdelay_Resp and
#: Pdelay_Resp_Follow_Up once a second.
SR_4X4 = (('aaf', 90, 125_000, 4), ('crf', 46, 2_000_000, 1))
SR_1X1 = (('aaf', 90, 125_000, 1),)
SHAPES = {'4x4': SR_4X4, '1x1': SR_1X1}
GPTP = (('sync', 58, 125_000_000, 1), ('follow_up', 90, 125_000_000, 1), ('announce', 90, 1_000_000_000, 1),
        ('pdelay_req', 68, 1_000_000_000, 1), ('pdelay_resp', 68, 1_000_000_000, 1),
        ('pdelay_resp_fu', 68, 1_000_000_000, 1))


def parse(text: str) -> tuple[list, list, list]:
    """The commits (ns, channel, head words), the frames each channel sent in order, and the testbench's holds."""
    txc, wire, holds = [], {}, []
    held_at = None
    for line in text.splitlines():
        if line.startswith('TXC '):
            _, cyc, ch, head = line.split()
            txc.append((int(cyc) * 1e9 / SYS_HZ, int(ch), int(head)))
        elif line.startswith('WIRE '):
            parts = line.split()
            wire.setdefault(int(parts[3]), []).append((len(parts[4]) // 2, int(parts[1]) * 1e9 / SYS_HZ))
        elif line.startswith('TXREADY '):
            _, cyc, on = line.split()
            t = int(cyc) * 1e9 / SYS_HZ
            if on == '0' and held_at is None:
                held_at = t
            elif on == '1' and held_at is not None:
                holds.append((held_at, t)); held_at = None
    if held_at is not None:
        holds.append((held_at, math.inf))
    return txc, wire, holds


def records(txc: list, wire: dict) -> tuple[list, list[str]]:
    """Each committed record, in commit order: (commit ns, channel, length, words, census free ns: the testbench took its
    last byte then, which is when KL_mbx_tx moved TX_TAIL past it). A TXC may commit several; its head advance is
    matched to the channel's sent frames in order. A mismatch is a finding, never skipped silently."""
    out, problems = [], []
    head = {}
    nxt = {ch: 0 for ch in wire}
    for t, ch, word in txc:
        advance = (word - head.get(ch, 0)) & 0xFFFF
        head[ch] = word
        got = 0
        while got < advance:
            k = nxt.get(ch, 0)
            frames = wire.get(ch, [])
            if k >= len(frames):
                problems.append(f'channel {ch}: a commit at {t / 1e3:.3f} us has no frame sent for it')
                break
            length, sent = frames[k]
            words = HDR_WORDS + (length + 3) // 4
            out.append((t, ch, length, words, sent))
            nxt[ch] = k + 1
            got += words
        if got != advance and got >= advance:
            problems.append(f'channel {ch}: a commit at {t / 1e3:.3f} us advanced {advance} words, frames make {got}')
    return out, problems


def in_hold(holds: list, t: float) -> float | None:
    """The end of the hold that covers t, or None."""
    for a, b in holds:
        if a <= t < b:
            return b
    return None


def periodic(kinds: tuple, end_ns: float, phase_ns: float) -> list:
    """Every frame of the periodic sources up to end_ns, as (ns, length, source)."""
    out = []
    for name, length, period, count in kinds:
        t = phase_ns % period
        while t <= end_ns:
            out += [(t, length, name)] * count
            t += period
    return sorted(out)


def replay(recs: list, holds: list, phase_ns: float, sr: tuple = SR_4X4, gptp: tuple = GPTP) -> dict:
    """The queue's discrete-event replay. Returns each record's free time (ns its last byte left the ring) and the
    time of its last octet on the line."""
    end = (max([r[0] for r in recs]) if recs else 0) + 50e6
    data = periodic(sr, end, phase_ns)
    ptp = periodic(gptp, end, phase_ns)
    n = len(recs)
    freed, last = [0.0] * n, [0.0] * n
    ci = di = pi = 0
    ctl_ready = 0.0          # the gasket: when the control lane next accepts a frame
    line_free = 0.0
    fifo = []                # (eligible ns, length, record index or -1) in line order, not yet started
    rr = 0                   # boundary round-robin: 0 grants control first, 1 data first
    now = 0.0
    lane_rr = 0              # control/gPTP round-robin after the gasket

    guard = 0
    while ci < n or di < len(data) or pi < len(ptp):
        guard += 1
        if guard > 50_000_000:
            raise RuntimeError('replay did not converge')
        # the next control record available to the control lane: committed, past any hold, past the gasket
        c_at = math.inf
        if ci < n:
            c_at = max(recs[ci][0], ctl_ready)
            h = in_hold(holds, c_at)
            while h is not None:
                c_at = h
                h = in_hold(holds, c_at)
        p_at = ptp[pi][0] if pi < len(ptp) else math.inf
        d_at = data[di][0] if di < len(data) else math.inf
        t = min(c_at, p_at, d_at)
        if t == math.inf:
            break
        now = t
        # drain the line up to now: frames whose line start is <= now leave the FIFO's slots
        while fifo and max(line_free, fifo[0][0]) <= now:
            elig, length, k = fifo.pop(0)
            s = max(line_free, elig)
            if k >= 0:
                last[k] = s + last_octet_ns(length)
            line_free = s + line_octets(length) * OCTET_NS
        if len(fifo) >= SF_FRAMES or sum(f[1] for f in fifo) >= SF_BYTES:
            # FIFO full: nothing enters until the line takes the oldest frame
            elig, length, k = fifo.pop(0)
            s = max(line_free, elig)
            if k >= 0:
                last[k] = s + last_octet_ns(length)
            line_free = s + line_octets(length) * OCTET_NS
            now = max(now, s)
            continue
        ready = [lane for lane, at in (('ctl', c_at), ('ptp', p_at), ('data', d_at)) if at <= now]
        ctl_side = [x for x in ready if x in ('ctl', 'ptp')]
        pick_ctl = None
        if ctl_side:
            if len(ctl_side) == 2:
                pick_ctl = ('ctl', 'ptp')[lane_rr]
            else:
                pick_ctl = ctl_side[0]
        if pick_ctl and 'data' in ready:
            lane = pick_ctl if rr == 0 else 'data'
            rr ^= 1
        else:
            lane = pick_ctl or 'data'
        if lane == 'ctl':
            t0, ch, length, words = recs[ci][:4]
            done = now + length * MBX_BYTE_NS
            freed[ci] = done
            fifo.append((done, length, ci))
            ctl_ready = done + GASKET_NS
            ci += 1
            lane_rr = 1
        elif lane == 'ptp':
            length = ptp[pi][1]
            fifo.append((now + length * DATA_BYTE_NS, length, -1))
            pi += 1
            lane_rr = 0
        else:
            length = data[di][1]
            fifo.append((now + length * DATA_BYTE_NS, length, -1))
            di += 1
    while fifo:
        elig, length, k = fifo.pop(0)
        s = max(line_free, elig)
        if k >= 0:
            last[k] = s + last_octet_ns(length)
        line_free = s + line_octets(length) * OCTET_NS
    return dict(freed=freed, last=last)


def census_room(recs: list, earlier: list, words: int, ring: int) -> float:
    """The earliest instant the census's own ring had room for a record of `words`: when the testbench had taken enough
    of the records committed ahead of it on its channel."""
    used = sum(recs[i][3] for i in earlier)
    if used + words <= ring:
        return 0.0
    for i in sorted(earlier, key=lambda i: recs[i][4]):
        used -= recs[i][3]
        if used + words <= ring:
            return recs[i][4]
    return math.inf


def grade(recs: list, holds: list, phases: int = 5, sr: tuple = SR_4X4) -> dict:
    """(a) and (b) over every phase of the periodic sources; the worst of each."""
    worst_wait, worst_at, fails_a, held_skipped = 0.0, None, [], 0
    for p in range(phases):
        phase = p * 125_000 / phases
        r = replay(recs, holds, phase, sr)
        # (a): the census's test ran at some instant between the earliest its own ring had room for the record and
        # the commit, and no earlier than MOVE_US before the commit; the replayed ring must have room at the latest
        # such instant, the one most favourable to the census and least to the replay, or the outcomes may differ.
        by_ch = {}
        for k, rec in enumerate(recs):
            by_ch.setdefault(rec[1], []).append(k)
        for ch, ks in by_ch.items():
            ring = RING_WORDS[ch]
            for j, k in enumerate(ks):
                t, words = recs[k][0], recs[k][3]
                room = census_room(recs, ks[:j], words, ring)
                test_at = max(t - MOVE_US * 1e3, room)
                used = sum(recs[i][3] for i in ks[:j] if r['freed'][i] > test_at)
                if room > t or used + words > ring:
                    # when the replayed ring first had room: the most the free-space read may precede the commit
                    ahead = sorted((r['freed'][i], recs[i][3]) for i in ks[:j] if r['freed'][i] > test_at)
                    held, replay_room = used, test_at
                    for free_at, w in ahead:
                        if held + words <= ring:
                            break
                        held -= w; replay_room = free_at
                    fails_a.append(dict(phase_ns=phase, channel=ch, commit_us=t / 1e3, test_us=test_at / 1e3,
                                        used=used, record=words, ring=ring, census_room_us=room / 1e3,
                                        replay_room_us=replay_room / 1e3, slack_us=(t - replay_room) / 1e3))
        # (b): commit to last octet, skipping a record whose wait spans a testbench hold
        for k, (t, ch, length, words, _) in enumerate(recs):
            spans = any(a < r['last'][k] and b > t for a, b in holds)
            if spans:
                held_skipped += 1
                continue
            w = (r['last'][k] - t) / 1e3
            if w > worst_wait:
                worst_wait, worst_at = w, dict(phase_ns=phase, channel=ch, commit_us=t / 1e3, length=length)
    total = worst_wait * MARGIN + FIXED_PATH_US
    return dict(records=len(recs), phases=phases, a_failures=len(fails_a), a_first=fails_a[:5],
                a_least_slack_us=min([f['slack_us'] for f in fails_a], default=None),
                b_worst_wait_us=worst_wait, b_worst=worst_at, b_total_us=total, b_bound_us=BOUND_US,
                b_pass=total <= BOUND_US, a_pass=not fails_a, held_records_skipped=held_skipped // max(phases, 1))


def selftest() -> int:
    """Planted defects the replay must catch, and the clean cases it must accept."""
    fails = 0
    def check(name, ok):
        nonlocal fails
        print(('PASS ' if ok else 'FAIL ') + name)
        fails += not ok
    def rec(t, ch, length):
        return (t, ch, length, HDR_WORDS + (length + 3) // 4, t + length * MBX_BYTE_NS + 50)
    one = [rec(1e6, 2, 100)]
    g = grade(one, [], 1)
    check('one 100-octet AECP frame alone waits its own line time and the queue ahead', 0 < g['b_worst_wait_us'] < 60)
    check('one 1500-octet frame fits AECP\'s 512-word ring', grade([rec(1e6, 2, 1500)], [], 1)['a_pass'])
    flood = [rec(1e6 + i * 1e3, 2, 600) for i in range(4)]
    g = grade(flood, [], 1)
    check('four 600-octet AECP commits 1 us apart overrun the 512-word ring at the MII rate (a)', not g['a_pass'])
    many = [rec(1e6 + i, i % 5, 60) for i in range(60)]
    g = grade(many, [], 1)
    check('sixty 60-octet frames at once wait their gaskets: over 600 us (b)', g['b_worst_wait_us'] > 600)
    held = [rec(1e6, 2, 100)]
    g = grade(held, [(0.9e6, 61e6)], 1)
    check('a record whose wait spans a testbench hold is skipped, not graded', g['held_records_skipped'] == 1 and
          g['b_worst_wait_us'] == 0)
    quiet = grade(one, [], 1, sr=())
    check('SR frames lengthen the wait (the shape\'s frames are counted)', quiet['b_worst_wait_us'] <=
          grade(one, [], 5)['b_worst_wait_us'])
    # The backlog-owed shape: twelve 70-octet ACMP records held in the 256-word ring until release at 61 ms, the
    # census freeing them at once after it; a thirteenth committed 17 us after release keeps its outcome, since the
    # replay frees the first held record within a microsecond of release; one committed with no census room is refused.
    release = 61e6
    held12 = [(1e6 + i * 1e5, 1, 70, 20, release + 1e3 * (i + 1) / 12) for i in range(12)]
    late = held12 + [(release + 17.35e3, 1, 70, 20, release + 30e3)]
    g = grade(late, [(0.9e6, release)], 1)
    check('a commit 17.35 us after a hold, its read up to 20 us before it, is refused, its slack stated (a)',
          not g['a_pass'] and 16.0 < g['a_least_slack_us'] < 17.35)
    global MOVE_US
    saved, MOVE_US = MOVE_US, 10.0
    check('the same commit keeps its outcome when its read is at most 10 us before it (a)',
          grade(late, [(0.9e6, release)], 1)['a_pass'])
    MOVE_US = saved
    early = held12 + [(release - 5e3, 1, 70, 20, release + 30e3)]
    check('a commit the census ring had no room for is refused (a)', not grade(early, [(0.9e6, release)], 1)['a_pass'])
    dense = [(1e6 + i * 500, 1, 70, 20, 1e6 + i * 500 + 1e3) for i in range(14)]
    check('fourteen ACMP records the census drained at once overrun the ring at the MII rate (a)',
          not grade(dense, [], 1)['a_pass'])
    sparse = [(1e6 + i * 20e3, 1, 70, 20, 1e6 + i * 20e3 + 1e3) for i in range(14)]
    check('the same records 20 us apart fit (a)', grade(sparse, [], 1)['a_pass'])
    txc = [(0.0, 2, 27), (5.0, 2, 54)]
    recs, problems = records(txc, {2: [(100, 1.0), (100, 6.0)]})
    check('records match commits to frames by head advance', len(recs) == 2 and not problems)
    recs, problems = records([(0.0, 2, 30)], {2: [(100, 1.0)]})
    check('a head advance the frames do not make is a finding', bool(problems))
    return fails


def main(argv: list[str]) -> int:
    """Grade each log; print one JSON object a log, and a summary."""
    ap = argparse.ArgumentParser()
    ap.add_argument('logs', nargs='*')
    ap.add_argument('--phases', type=int, default=5)
    ap.add_argument('--shape', choices=sorted(SHAPES), default='4x4')
    ap.add_argument('--json')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return int(selftest() > 0)
    results = []
    for path in a.logs:
        txc, wire, holds = parse(Path(path).read_text(errors='replace'))
        recs, problems = records(txc, wire)
        g = grade(recs, holds, a.phases, SHAPES[a.shape])
        g.update(log=path, shape=a.shape, match_problems=problems[:5], holds=len(holds))
        results.append(g)
        print(json.dumps({k: g[k] for k in ('log', 'records', 'a_pass', 'a_failures', 'b_worst_wait_us',
                                            'b_total_us', 'b_pass', 'held_records_skipped', 'match_problems')}),
              flush=True)
    worst = max(results, key=lambda g: g['b_worst_wait_us']) if results else None
    summary = dict(logs=len(results), a_pass=all(g['a_pass'] for g in results) and
                   not any(g['match_problems'] for g in results),
                   b_pass=all(g['b_pass'] for g in results),
                   worst_wait_us=worst and worst['b_worst_wait_us'], worst_log=worst and worst['log'],
                   worst_total_us=worst and worst['b_total_us'], fixed_path_us=FIXED_PATH_US, margin=MARGIN)
    print('SUMMARY', json.dumps(summary))
    if a.json:
        Path(a.json).write_text(json.dumps(dict(summary=summary, results=results), indent=1) + '\n')
    return 0 if summary['a_pass'] and summary['b_pass'] else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
