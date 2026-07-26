#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
test_trace_roundtrip.py - host-runnable gate for the CTF fault log.

Gates (Phase 10, docs/design/TRACE_LOGGING.md):
   1. flash map: FLASHBOOT_LAYOUT + FLASHBOOT_RESERVED are erase-block aligned,
      non-overlapping and inside the device, and sw/dts/mtd-partitions.dtsi is
      byte-identical to what they generate (+ dtc structural check);
   2. the checked-in generated/ producer is what milan_trace.yaml produces -
      re-generated and diffed WHEN barectf is importable, LOUDLY SKIPPED when it
      is not, so an outsider without barectf still runs every other gate;
   3. the event-record id -> name map is pinned.  barectf assigns ids by SORTED
      EVENT NAME, so adding an event renumbers its alphabetical successors; this
      gate turns that into a visible diff instead of silently mis-decoding every
      archived trace;
   4. the producer COMPILES and RUNS with a host C compiler (the same barectf.c
      + milan_trace.c the board daemon links), producing real CTF segments;
   5. those segments decode: packet count matches the ring's own statistics,
      zero structural notes, and every one of the 23 event types is exercised;
   6. the pinned xz chain compresses them, and the measured ratio is reported
      and bounded;
   7. TORN RAW segment - truncated mid-packet, the reader recovers exactly the
      whole packets and says so;
   8. TORN XZ segment - truncated at 10/25/50/75/90 %, the reader recovers a
      monotonically growing PREFIX of the full event list.  Prefix, not
      "some events": every recovered record is byte-identical to the record at
      the same position in the intact decode;
   9. negative controls - a clobbered packet magic and an impossible
      content_size are REFUSED at that packet, not decoded into plausible
      nonsense, and the packets before the damage survive;
  10. the 32-bit event timestamp cannot wrap ambiguously: the largest gap
      between consecutive records in the produced trace is far below 2^32 us,
      and the C header's heartbeat ceiling agrees with the yaml contract;
  11. the FLASH-WEAR TOKEN BUCKET: driven with the shipping defaults, a
      continuously-faulting board is held by the BUDGET (not by the rate
      limiter), the count matches the closed-form arithmetic, and the bucket
      refills over an idle hour.  This is what the >11-year flash lifetime in
      TRACE_LOGGING.md section 5 actually rests on;
  12. rotation: oldest-first eviction holds the /user/log budget, and the
      pinned first-fault segment survives an eviction that would otherwise
      take it;
  13. the /user/log budget is arithmetically inside the `user` flash slot;
  14. babeltrace2 cross-check when it is installed (loud skip otherwise) - our
      pure-python reader must agree with the canonical one on the event count.

Everything here runs on a plain host: python3 stdlib, a C compiler, and
optionally barectf / dtc / babeltrace2, each of which is a LOUD SKIP when
absent rather than a silent pass.  Nothing here touches a board.

    python3 sw/trace/test_trace_roundtrip.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
GEN = os.path.join(HERE, "generated")

sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sw", "dts"))
import ctf_read          # noqa: E402
import trace_segment     # noqa: E402
import gen_mtd_partitions as gmp   # noqa: E402

SKIPS = []


def _skip(what, why):
    SKIPS.append(f"{what}: {why}")
    print(f"  [SKIP] {what} - {why}")


# The ABI, pinned.  See gate 3.
EVENT_IDS = {
    0: "acmp_listener", 1: "avtp_rx", 2: "boot", 3: "csr_access", 4: "daemon",
    5: "heartbeat", 6: "journal", 7: "link", 8: "ltap", 9: "maap",
    10: "mac_reset", 11: "mediaclk", 12: "note", 13: "parser_probe", 14: "ptp",
    15: "ring", 16: "srp", 17: "srp_refusal", 18: "stream_ctx",
    19: "stream_ctx_write", 20: "trace_drop", 21: "trace_evict",
    22: "trace_flush",
}

# Every event type must appear in the scripted run.  An event nobody has ever
# emitted is an untested wire layout, which is how a decorative ABI starts
# (docs/limitations/RECURRING_DEFECT_PATTERNS.md pattern 1).
MUST_EXERCISE = set(EVENT_IDS.values())


def test_flash_map_and_mtd_node():
    rows, flash_size, erase = gmp.load_map()
    problems = gmp.check_map(rows, flash_size, erase)
    assert not problems, "flash map: " + "; ".join(problems)

    names = [r[0] for r in rows]
    assert "journal" in names and "user" in names, \
        "the writable slots are missing from the flash map"
    user = [r for r in rows if r[0] == "user"][0]
    jnl = [r for r in rows if r[0] == "journal"][0]
    assert jnl[2] == 2 * erase, \
        f"journal must be exactly 2 erase blocks (A/B), got 0x{jnl[2]:X}"
    assert user[2] == 2 * 1024 * 1024, \
        f"user slot must be 2 MiB, got 0x{user[2]:X}"

    rc = gmp.main(["--check"])
    assert rc == 0, "mtd-partitions.dtsi is stale vs the SoC flash map"

    errs = gmp.dtc_check(gmp.emit(rows, flash_size, erase))
    if errs == ["dtc not installed"]:
        _skip("gate 1 dtc", "dtc not installed")
    else:
        assert not errs, "dtc: " + "; ".join(errs)
    print(f"  [gate 1] {len(rows)} slots, erase-block aligned, no overlap, "
          f"0x{sum(r[2] for r in rows):X} of 0x{flash_size:X} allocated; "
          "mtd-partitions.dtsi in step")


def test_generated_is_fresh():
    """Re-run barectf and diff, when barectf is importable."""
    try:
        import barectf  # noqa: F401
    except Exception as e:
        _skip("gate 2 regeneration",
              f"barectf not importable ({type(e).__name__}); the checked-in "
              "generated/ is used as-is")
        return
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run(
            [sys.executable, "-m", "barectf.cli" if False else "barectf",
             "generate", "--code-dir", td, "--headers-dir", td,
             "--metadata-dir", td, os.path.join(HERE, "milan_trace.yaml")],
            capture_output=True, text=True)
        if r.returncode != 0:
            # barectf is importable but its CLI entry point is not on PATH;
            # drive the library directly rather than skipping.
            import barectf.cli as bcli
            argv = sys.argv
            sys.argv = ["barectf", "generate", "--code-dir", td,
                        "--headers-dir", td, "--metadata-dir", td,
                        os.path.join(HERE, "milan_trace.yaml")]
            try:
                bcli._run()
            except SystemExit:
                pass
            finally:
                sys.argv = argv
        stale = []
        for name in ("metadata", "barectf.c", "barectf.h",
                     "barectf-bitfield.h"):
            fresh = os.path.join(td, name)
            if not os.path.isfile(fresh):
                stale.append(f"{name} (barectf produced nothing)")
                continue
            if _strip_gen_stamp(open(fresh, encoding="utf-8").read()) != \
               _strip_gen_stamp(open(os.path.join(GEN, name),
                                     encoding="utf-8").read()):
                stale.append(name)
        assert not stale, \
            ("generated/ is stale vs milan_trace.yaml: " + ", ".join(stale) +
             " - re-run barectf (sw/trace/README.md) and commit the result")
    print("  [gate 2] generated/ re-generates byte-identically from "
          "milan_trace.yaml (barectf present)")


_STAMP = re.compile(r"^.*(on \d{4}-\d{2}-\d{2}T[\d:.]+|barectf_gen_date = .*)$",
                    re.MULTILINE)


def _strip_gen_stamp(text):
    """Drop barectf's generation timestamp - it changes on every run and is not
    part of the ABI."""
    return _STAMP.sub("", text)


def test_event_ids_pinned():
    meta = _meta()
    got = meta.event_ids()
    assert got == EVENT_IDS, (
        "event-record id map changed.\n"
        f"  pinned: {EVENT_IDS}\n  now:    {got}\n"
        "barectf numbers events by SORTED NAME, so adding or renaming one "
        "renumbers its alphabetical successors and every ARCHIVED trace "
        "decoded against the NEW metadata is wrong. If this change is "
        "intended, bump environment.milan_trace_abi in milan_trace.yaml and "
        "update EVENT_IDS here in the same commit.")
    ctx = [n for n, _ in meta.event_context]
    assert ctx == ["sev", "src"], f"common context changed: {ctx}"
    hdr = dict(meta.event_header)
    assert hdr["timestamp"].size == 32, "event timestamp width changed"
    assert hdr["id"].size == 8, "event id width changed"
    print(f"  [gate 3] {len(got)} event types, id map pinned; common context "
          f"{ctx}; 8-bit id + 32-bit timestamp")


_META = None


def _meta():
    global _META
    if _META is None:
        _META = ctf_read.Metadata(
            open(os.path.join(GEN, "metadata"), encoding="utf-8").read())
    return _META


def _cc():
    for cand in (os.environ.get("CC"), "cc", "gcc", "clang"):
        if cand and shutil.which(cand):
            return cand
    return None


_RUN = {}


def test_producer_builds_and_runs():
    cc = _cc()
    if cc is None:
        _skip("gates 4-13", "no C compiler (set CC=) - nothing to produce")
        return
    td = tempfile.mkdtemp(prefix="milan-trace-")
    _RUN["dir"] = td
    exe = os.path.join(td, "trace_selftest")
    r = subprocess.run(
        [cc, "-std=c99", "-O2", "-Wall", "-Wextra", "-Werror",
         "-I", HERE, "-o", exe,
         os.path.join(HERE, "trace_selftest.c"),
         os.path.join(HERE, "milan_trace.c"),
         os.path.join(GEN, "barectf.c")],
        capture_output=True, text=True)
    assert r.returncode == 0, f"producer does not compile:\n{r.stderr}"
    raw = os.path.join(td, "raw")
    os.makedirs(raw)
    r = subprocess.run([exe, raw], capture_output=True, text=True)
    assert r.returncode == 0, f"producer failed:\n{r.stderr}"
    _RUN["raw"] = raw
    stats = dict(ln.split("=", 1) for ln in
                 open(os.path.join(raw, "stats.txt")).read().split())
    _RUN["stats"] = stats
    print(f"  [gate 4] {cc} -Werror built the shipping producer; run wrote "
          f"{stats['segments']} segments / {stats['packets_written']} packets "
          f"over {int(stats['sim_us']) // 1000000} s of simulated board time")


def test_segments_decode():
    if "raw" not in _RUN:
        return
    meta = _meta()
    total_pkts, names, events = 0, set(), []
    for f in sorted(os.listdir(_RUN["raw"])):
        if not f.startswith("seg-"):
            continue
        blob = open(os.path.join(_RUN["raw"], f), "rb").read()
        packets, evs, note = ctf_read.decode(blob, meta)
        assert note is None, f"{f}: decode note on an intact segment: {note}"
        total_pkts += len(packets)
        events.extend(evs)
        names.update(e["name"] for e in evs)
    # Every packet the ring closed is either in a segment, or was dropped by
    # the lapping ring, or is still resident.  Nothing else is admissible - a
    # packet that is none of the three vanished silently, which is the one
    # behaviour a fault log may never have.
    st = _RUN["stats"]
    expect = (int(st["packets_written"]) - int(st["packets_dropped"])
              - int(st["packets_resident"]))
    assert total_pkts == expect, (
        f"decoded {total_pkts} packets; the ring accounts for {expect} "
        f"(written {st['packets_written']} - dropped {st['packets_dropped']} "
        f"- resident {st['packets_resident']})")
    missing = MUST_EXERCISE - names
    assert not missing, f"event types never exercised: {sorted(missing)}"
    _RUN["events"] = events
    print(f"  [gate 5] {total_pkts} packets / {len(events)} records decode "
          f"clean; ring accounting closes (written {st['packets_written']}, "
          f"dropped {st['packets_dropped']}); all {len(names)} event types "
          "exercised")


def test_compression_ratio():
    if "raw" not in _RUN:
        return
    packed = os.path.join(_RUN["dir"], "log")
    raws = sorted(os.path.join(_RUN["raw"], f)
                  for f in os.listdir(_RUN["raw"]) if f.startswith("seg-"))
    rc = trace_segment.main(["pack"] + raws + ["-o", packed])
    assert rc == 0
    _RUN["log"] = packed
    tin = sum(os.path.getsize(p) for p in raws)
    tout = sum(os.path.getsize(os.path.join(packed, f))
               for f in os.listdir(packed) if f.endswith(".xz"))
    ratio = tout / tin
    assert ratio < 0.40, (
        f"compressed ratio {ratio:.3f} is worse than the 0.40 guard - the "
        "flash budget in TRACE_LOGGING.md section 5 assumes ~0.25")
    bpr = tout / max(1, len(_RUN["events"]))
    _RUN["ratio"], _RUN["bpr"] = ratio, bpr
    print(f"  [gate 6] {tin} -> {tout} B, ratio {ratio:.4f} ({tin / tout:.2f}x), "
          f"{bpr:.2f} compressed bytes per trace record")


def _biggest_raw():
    raws = sorted((os.path.getsize(os.path.join(_RUN["raw"], f)),
                   os.path.join(_RUN["raw"], f))
                  for f in os.listdir(_RUN["raw"]) if f.startswith("seg-"))
    return raws[-1][1]


def test_torn_raw_segment():
    if "raw" not in _RUN:
        return
    meta = _meta()
    path = _biggest_raw()
    full = open(path, "rb").read()
    psize = 4096
    whole, _e, note = ctf_read.decode(full, meta)
    assert note is None
    # cut 1234 bytes into the middle of a packet
    cut = (len(full) // 2) + 1234
    packets, events, note = ctf_read.decode(full[:cut], meta)
    assert note is not None, "a mid-packet truncation must be REPORTED"
    assert len(packets) == cut // psize, (
        f"recovered {len(packets)} whole packets, expected {cut // psize}")
    ref = [e for e in _decode_events(full, meta)]
    assert events == ref[:len(events)], \
        "the torn decode is not a prefix of the intact decode"
    print(f"  [gate 7] raw segment cut mid-packet at byte {cut}: "
          f"{len(packets)}/{len(whole)} whole packets recovered, "
          f"{len(events)} records, reported as `{note}`")


def _decode_events(blob, meta):
    _p, e, _n = ctf_read.decode(blob, meta)
    return e


def test_torn_xz_segment():
    if "log" not in _RUN:
        return
    meta = _meta()
    src = _biggest_raw()
    plain = open(src, "rb").read()
    blob = trace_segment.compress(plain)
    ref = _decode_events(plain, meta)
    last, rows = -1, []
    for frac in (0.10, 0.25, 0.50, 0.75, 0.90, 1.00):
        n = int(len(blob) * frac)
        data, trunc = trace_segment.decompress_tolerant(blob[:n])
        packets, events, _note = ctf_read.decode(data, meta)
        assert trunc == (frac < 1.0), \
            f"truncation at {frac:.0%} not reported by the xz layer"
        assert events == ref[:len(events)], (
            f"at {frac:.0%} the recovered records are not a PREFIX of the "
            "intact decode - a truncated segment produced different data, "
            "not less data")
        assert len(events) >= last, "recovery is not monotone in kept bytes"
        last = len(events)
        rows.append((frac, n, len(data), len(packets), len(events)))
    assert rows[-1][4] == len(ref)
    assert rows[0][4] > 0, \
        "10 % of a segment recovered nothing - the xz stream is not " \
        "incrementally decodable, revisit the chain in trace_segment.py"
    detail = "  ".join(f"{f:.0%}->{p}pkt" for f, _n, _d, p, _e in rows)
    print(f"  [gate 8] truncated xz decodes as a growing PREFIX: {detail}")


def test_negative_controls():
    if "raw" not in _RUN:
        return
    meta = _meta()
    full = bytearray(open(_biggest_raw(), "rb").read())
    psize = 4096
    good, _e, _n = ctf_read.decode(bytes(full), meta)
    assert len(good) > 4

    bad = bytearray(full)
    bad[3 * psize] ^= 0xFF                       # clobber packet 3's magic
    packets, _events, note = ctf_read.decode(bytes(bad), meta)
    assert len(packets) == 3 and note and "magic" in note, \
        f"clobbered magic not caught: {len(packets)} packets, note={note}"

    bad = bytearray(full)
    # content_size sits after magic(4) + stream_id(1) + packet_size(4)
    off = 3 * psize + 4 + 1 + 4
    bad[off:off + 4] = (0xFFFFFFF8).to_bytes(4, "little")
    packets, _events, note = ctf_read.decode(bytes(bad), meta)
    assert len(packets) == 3 and note, \
        f"impossible content_size not caught: {len(packets)} packets"

    bad = bytearray(full[:5 * psize])
    bad[4 * psize:] = b"\xff" * psize            # erased flash tail
    packets, _events, note = ctf_read.decode(bytes(bad), meta)
    assert len(packets) == 4 and note is None, \
        "an erased tail must end the decode quietly, not raise a note"
    print("  [gate 9] clobbered magic and impossible content_size are refused "
          "AT that packet (3 earlier packets survive); an erased tail ends the "
          "decode quietly")


def test_timestamp_wrap_margin():
    if "events" not in _RUN:
        return
    ts = [e["ts"] for e in _RUN["events"]]
    gaps = [b - a for a, b in zip(ts, ts[1:])]
    worst = max(gaps) if gaps else 0
    wrap = 1 << 32
    assert worst < wrap // 4, (
        f"largest inter-record gap {worst} us is within 4x of the 32-bit "
        f"timestamp wrap ({wrap} us) - the heartbeat is not doing its job")
    hdr = open(os.path.join(HERE, "milan_trace.h")).read()
    m = re.search(r"#define MILAN_TRACE_HEARTBEAT_MAX_US\s+(\d+)u", hdr)
    assert m, "MILAN_TRACE_HEARTBEAT_MAX_US missing from milan_trace.h"
    hb = int(m.group(1))
    assert hb * 4 < wrap, "the heartbeat ceiling does not bound the wrap"
    yml = open(os.path.join(HERE, "milan_trace.yaml")).read()
    assert "MILAN_TRACE_HEARTBEAT_MAX_US" in yml, \
        "the yaml contract no longer names the heartbeat requirement"
    print(f"  [gate 10] worst inter-record gap {worst} us; heartbeat ceiling "
          f"{hb} us; 32-bit timestamp wraps at {wrap} us "
          f"({wrap / hb:.0f}x margin)")


def test_flash_wear_budget():
    """The token bucket in milan_trace.c, driven by the shipping defaults.

    The >11-year flash-lifetime claim rests on this bucket, not on "flushes are
    rare"; a rate limiter alone permits ~98 MiB/day.  The drill runs a
    continuously-faulting board and counts the 100 KiB flushes it gets before
    the budget - not the rate limiter - refuses one.
    """
    if "stats" not in _RUN:
        return
    st = _RUN["stats"]
    hdr = open(os.path.join(HERE, "milan_trace.h")).read()
    per_hour = eval(re.search(
        r"#define MILAN_TRACE_BUDGET_BYTES_PER_HOUR\s+\(([^)]+)\)",
        hdr).group(1).replace("u", ""))
    minflush = eval(re.search(
        r"#define MILAN_TRACE_MIN_FLUSH_BYTES\s+\(([^)]+)\)",
        hdr).group(1).replace("u", ""))
    n = int(st["budget_flushes"])
    assert int(st["budget_hold"]) == 6, (
        f"the drill stopped for hold code {st['budget_hold']}, not BUDGET (6) - "
        "the budget is not the binding limit, so the lifetime claim is unproven")
    # Closed form: start full, each round refills 60 s worth then spends 100 KiB,
    # and the run stops when the bucket cannot afford MIN_FLUSH_BYTES.
    left, expect = per_hour, 0
    while True:
        left = min(per_hour, left + per_hour * 60 // 3600)
        if left < minflush:
            break
        left -= 100 * 1024
        expect += 1
    assert n == expect, f"budget drill gave {n} flushes, arithmetic says {expect}"
    assert int(st["budget_after_1h"]) == per_hour, \
        "the bucket did not refill to full after an idle hour"
    day = per_hour * 24
    print(f"  [gate 11] budget {per_hour} B/h ({day / 1048576:.0f} MiB/day "
          f"ceiling): a continuously-faulting board gets {n} x 100 KiB flushes "
          f"then holds on BUDGET; the bucket refills to full over an idle hour")


def test_rotation_policy():
    td = tempfile.mkdtemp(prefix="milan-rot-")
    try:
        sizes = [70000] * 30            # 2.1 MB of segments over a 1.5 MiB budget
        for i, s in enumerate(sizes):
            open(os.path.join(td, f"seg-{i:06d}.ctf.xz"), "wb").write(b"\0" * s)
        budget = trace_segment.DEFAULT_LOG_BUDGET
        rc = trace_segment.main(["rotate", td, "--budget", str(budget)])
        assert rc == 0
        left = [n for n, _p in trace_segment.segments(td)]
        total = sum(os.path.getsize(p) for _n, p in trace_segment.segments(td))
        assert total <= budget, f"rotation left {total} B over a {budget} B budget"
        assert trace_segment.PINNED_SEGMENT in left, \
            "the pinned first-fault segment was evicted"
        assert left[1] > 1, "eviction did not take the OLDEST rotating segments"
        assert max(left) == len(sizes) - 1, "the newest segment was evicted"
        print(f"  [gate 12] 30 segments / {sum(sizes)} B -> {len(left)} kept / "
              f"{total} B within the {budget} B budget; segment "
              f"{trace_segment.PINNED_SEGMENT} pinned, oldest rotating evicted "
              f"first (kept {left[:4]}...{left[-1]})")
    finally:
        shutil.rmtree(td, ignore_errors=True)


def test_log_budget_fits_user_slot():
    rows, _fs, erase = gmp.load_map()
    user = [r for r in rows if r[0] == "user"][0]
    budget = trace_segment.DEFAULT_LOG_BUDGET
    assert budget < user[2], \
        f"log budget {budget} B does not fit the {user[2]} B user slot"
    left = user[2] - budget
    assert left >= 8 * erase, (
        f"only {left} B left in /user for the state the partition exists for "
        "(entity names, channel maps, mixer state)")
    assert trace_segment.SEGMENT_BYTES % 4096 == 0
    print(f"  [gate 13] /user 0x{user[2]:X}: log budget {budget} B "
          f"({budget / user[2]:.0%}), {left} B left for /user state; "
          f"segment ceiling {trace_segment.SEGMENT_BYTES} B")


def test_babeltrace2_agrees():
    if "log" not in _RUN:
        return
    if shutil.which("babeltrace2") is None:
        _skip("gate 14 babeltrace2",
              "babeltrace2 not installed - the pure-python reader is "
              "un-cross-checked on this host")
        return
    out = os.path.join(_RUN["dir"], "bt")
    assert trace_segment.main(["unpack", _RUN["log"], "-o", out]) == 0
    r = subprocess.run(["babeltrace2", out], capture_output=True, text=True)
    assert r.returncode == 0, f"babeltrace2 refused the trace:\n{r.stderr}"
    n = len([ln for ln in r.stdout.splitlines() if ln.strip()])
    meta, items = ctf_read.load(out)
    ours = sum(len(ctf_read.decode(b, meta)[1]) for _n, b, _t in items)
    assert n == ours, f"babeltrace2 saw {n} records, ctf_read saw {ours}"
    print(f"  [gate 14] babeltrace2 and ctf_read.py agree on {ours} records")


def test_event_catalogue_fresh():
    """Gate 15: docs/reference/TRACE_EVENTS.md is generated from the YAML, so
    "what is being logged" cannot drift from the ABI that emits it. Same
    staleness contract as the traceability matrix."""
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(HERE, "gen_trace_events.py"), "--check"],
                       capture_output=True, text=True)
    if "pyyaml not installed" in (r.stderr or ""):
        _skip("gate 15 event catalogue", "pyyaml not installed")
        return
    assert r.returncode == 0, \
        f"event catalogue is STALE - run sw/trace/gen_trace_events.py\n{r.stdout}{r.stderr}"
    print(f"  [gate 15] {r.stdout.strip()}")


if __name__ == "__main__":
    for fn in (test_flash_map_and_mtd_node, test_generated_is_fresh,
               test_event_ids_pinned, test_producer_builds_and_runs,
               test_segments_decode, test_compression_ratio,
               test_torn_raw_segment, test_torn_xz_segment,
               test_negative_controls, test_timestamp_wrap_margin,
               test_flash_wear_budget,
               test_rotation_policy, test_log_budget_fits_user_slot,
               test_babeltrace2_agrees, test_event_catalogue_fresh):
        print(f"{fn.__name__}:")
        fn()
    if "dir" in _RUN:
        shutil.rmtree(_RUN["dir"], ignore_errors=True)
    if SKIPS:
        print(f"SKIPPED ({len(SKIPS)}): " + " | ".join(SKIPS))
    print("ALL GATES PASS")
