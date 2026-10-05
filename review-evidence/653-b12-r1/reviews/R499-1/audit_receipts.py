#!/usr/bin/env python3
"""Read-only audit of the published, bounded bench receipts.

Usage: python3 audit_receipts.py EVIDENCE_ROOT CHECKOUT
EVIDENCE_ROOT contains MANIFEST.json and author/ at evidence commit
9649a107657bdc77d1c47d7ce735e6a282394235, review-evidence/653-b12-r1.
No raw identifying field values are printed.
"""
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import sys


def main():
    root, repo = map(Path, sys.argv[1:])
    author = root / "author"
    manifest = json.loads((root / "MANIFEST.json").read_text())
    for entry in manifest:
        assert hashlib.sha256((root / entry["file"]).read_bytes()).hexdigest() == entry["published_sha256"]
    print(json.dumps({"published_manifest_files_verified": len(manifest)}))
    cycles = {r["cycle"]: r for f in sorted(author.glob("cycles-*.json")) for r in json.loads(f.read_text())}
    wires = {r["cycle"]: r for f in sorted(author.glob("wire-receipts-*.json")) for r in json.loads(f.read_text())}
    assert len(cycles) == len(wires) == 182 and cycles.keys() == wires.keys()
    page = (repo / "docs/findings/653_DISCONNECT_ORDER_BENCH.md").read_text()
    # The publisher replaced six identifier octets, leaving the two suffix octets.
    # Use a fixed anonymous value solely to recover byte offsets for decoding.
    def raw(r):
        return bytes.fromhex(r["raw"].replace("<controller-host-id>", "000000000000"))

    intervals, first = [], []
    counts = collections.Counter()
    for cid, c in cycles.items():
        w = wires[cid]
        assert w["capture"] == c["selected_capture"]
        expected = "observer.pcap" if c["direction"] == "B" else "plain.pcap"
        assert w["capture"].endswith(expected)
        cmd, rsp, unl = (w[k] for k in ("command", "response", "unlock"))
        a, b, u = map(raw, (cmd, rsp, unl))
        assert a[0] == b[0] == 0xfc and a[1] & 15 == 8 and b[1] & 15 == 9
        # Correlate controller, listener, listener input and transaction sequence.
        # A successful unbind response can clear the former talker fields.
        assert a[12:20] == b[12:20] and a[28:36] == b[28:36]
        assert a[38:40] == b[38:40] and a[48:50] == b[48:50]
        assert b[2] >> 3 == 0 == rsp["status"] == c["status"]
        assert u[0] == 0xfb and u[1] & 15 == 1 and u[2] >> 3 == 0
        assert int.from_bytes(u[22:24], "big") == 0x8029
        assert u[4:12] == a[28:36] and u[12:20] == a[12:20]
        assert u[24:26] == b"\x00\x05" and u[26:28] == a[38:40]
        valid = int.from_bytes(u[28:32], "big")
        assert valid & 15 == 15
        ctr = [int.from_bytes(u[i:i+4], "big") for i in range(32, 48, 4)]
        assert ctr == [1, 1, 0, 0]
        assert cmd["i"] < rsp["i"] < unl["i"]
        assert cmd["tns"] < rsp["tns"] < unl["tns"]
        response_us = (unl["tns"] - rsp["tns"]) / 1000
        command_us = (rsp["tns"] - cmd["tns"]) / 1000
        assert response_us == c["response_unlock_us"]
        assert command_us == c["command_response_us"]
        row = next(line for line in page.splitlines() if line.startswith("| " + cid + " |"))
        assert f"R / {response_us:.3f}" in row and "SUCCESS" in row
        assert f"{c['actual_hold_ms']:.3f}" in row
        assert c["library_state"] == "NotConnected" and c["order"] == "RESPONSE_FIRST"
        pdus = w["first_twelve_pdus"]
        assert len(pdus) == 12
        assert all(y["seq"] == (x["seq"] + 1) % 256 for x, y in zip(pdus, pdus[1:]))
        assert all(x["tns"] >= w["bind_command_tap_ns"] for x in pdus)
        assert len({(x["sub"], x["port"]) for x in pdus}) == 1
        first.append({"cycle": cid, "kind": c["kind"], "direction": c["direction"],
                      "first_after_bind_ms": (pdus[0]["tns"] - w["bind_command_tap_ns"]) / 1e6,
                      "spacing_us": [(y["tns"] - x["tns"]) / 1000 for x, y in zip(pdus, pdus[1:])]})
        intervals.append(response_us)
        counts[(c["direction"], c["kind"], c["phase"])] += 1
    print(json.dumps({"cycle_rows": len(cycles), "wire_pair_checks": 182,
                      "interval_range_us": [min(intervals), max(intervals)],
                      "first_pdus_checked": 182 * 12, "adjacent_sequence_checks": 182 * 11,
                      "sequence_discontinuities": 0}))
    for direction in ("A", "B"):
        for kind in ("AAF", "CRF"):
            selected = [c for c in cycles.values() if c["direction"] == direction and c["kind"] == kind]
            fixed = [c for c in selected if c["phase"] == "exact" and c["requested_hold_ms"] < 600000]
            assert collections.Counter(c["requested_hold_ms"] for c in fixed) == {x: 5 for x in (300, 600, 900, 1000, 1100, 1500, 3000)}
            for phase in ("before", "after"):
                edge = [c for c in selected if c["phase"] == phase]
                assert len(edge) == 5
                times = [c["last_push_to_command_ms"] for c in edge]
                lo, hi = (975, 985) if phase == "before" else (25, 31)
                assert all(lo <= t <= hi for t in times)
                print(json.dumps({"direction": direction, "kind": kind, "phase": phase,
                                  "cycles": len(edge), "reported_since_prior_push_ms": [min(times), max(times)],
                                  "raw_push_anchor_published": False}))
            f = [x for x in first if x["direction"] == direction and x["kind"] == kind]
            arrivals = [x["first_after_bind_ms"] for x in f]
            spaces = [v for x in f for v in x["spacing_us"]]
            print(json.dumps({"direction": direction, "kind": kind,
                              "first_after_bind_ms": [min(arrivals), max(arrivals)],
                              "first_twelve_spacing_us": [min(spaces), max(spaces)]}))

    polls = [r for name in ("short-polls.csv", "long-polls.csv") for r in csv.DictReader((author / name).open())]
    assert len(polls) == 1510
    assert all(r["status"] == "Success." and int(r["SEQ"]) == int(r["SI"]) == 0 for r in polls)
    early = [r for r in polls if r["phase"].startswith("first-pdus-")]
    assert len(early) == 546
    empty = collections.Counter(r["phase"] for r in early if int(r["FRX"]) == 0)
    print(json.dumps({"counter_reads": len(polls), "early_reads": len(early), "sequence_and_interruption_nonzero_reads": 0,
                      "early_reads_with_zero_FRX": dict(empty),
                      "cycles_with_zero_FRX_at_all_early_reads": sum(all(int(r['FRX']) == 0 for r in early if r['cycle'] == cid) for cid in cycles)}))
    for cid in ("A-600s", "B-600s"):
        selected = [r for r in polls if r["cycle"] == cid and r["phase"].startswith("hold-")]
        assert len(selected) == 300
        assert cycles[cid]["actual_hold_ms"] >= 600000
        response_gaps = [(int(y['response_us']) - int(x['response_us'])) / 1e6 for x, y in zip(selected, selected[1:])]
        print(json.dumps({"cycle": cid, "scheduled_reads": len(selected),
                          "actual_hold_ms": cycles[cid]["actual_hold_ms"],
                          "poll_response_gap_s": [min(response_gaps), max(response_gaps)],
                          "reported_frames": cycles[cid]["stream_frames"], "reported_gaps": cycles[cid]["stream_gaps"]}))
    errors = json.loads((author / "rule-increments.json").read_text())
    assert sum((collections.Counter(r["increments"]) for r in errors), collections.Counter()) == {"EARLY": 1, "LATE": 1}
    for cid, name in (("BAAF0300-2", "EARLY"), ("BAAF0900-5", "LATE")):
        p = next(r for r in early if r["cycle"] == cid and r["phase"] == "first-pdus-20")
        previous = next(r for r in polls if r["cycle"] == cid and r["phase"] == "pre-bind")
        error = next(r for r in errors if r["cycle"] == cid)
        assert int(previous[name]) == 0 and int(p[name]) == 1
        assert int(p["response_us"]) < cycles[cid]["command_time_us"]
        print(json.dumps({"cycle": cid, "counter": name, "first_read_utc": p["utc"],
                          "first_read_since_bind_ms": float(p["since_bind_command_ms"]),
                          "received_frames_by_first_read": int(p["FRX"]),
                          "callback_lag_after_first_read_ms": (error["t"] - int(p["response_us"])) / 1000,
                          "error_predates_unbind": True,
                          "first_pdu_after_bind_ms": next(x["first_after_bind_ms"] for x in first if x["cycle"] == cid),
                          "presentation_timestamp_retained_in_first_pdu_receipt": False}))

    restore = json.loads((author / "restore-comparison.json").read_text())
    assert restore["pass_restore"] and len(restore["rows"]) == 8
    assert all(r["equal"] and r["start_sha256"] == r["end_sha256"] for r in restore["rows"])
    expected_raw = [f"{stem}-{phase}.jsonl" for stem in ("census", "dut-descs", "peer-descs") for phase in ("start", "end")]
    print(json.dumps({"restore_equal_summary_rows": 8, "restore_observations": sum(r["observations"] for r in restore["rows"]),
                      "restore_source_readbacks_in_public_packet": sum((author / f).exists() for f in expected_raw),
                      "restore_source_readbacks_needed": 6}))
    identity = json.loads((author / "identity.json").read_text())
    payload = bytes.fromhex(identity["descriptor_payload"])
    serial = payload[248:312].split(b"\0", 1)[0]
    assert serial and identity["readback"]["serial_number"] == "<device-serial>"
    serial_text = serial.decode("ascii")
    lines = [i for i, line in enumerate(page.splitlines(), 1) if serial_text in line]
    print(json.dumps({"privacy": {"redacted_display_serial_has_unredacted_encoded_copy": True,
                                   "encoded_serial_offset": 248, "encoded_serial_length": len(serial),
                                   "same_serial_plaintext_page_lines": lines},
                      "check_result": "completed; deficiencies reported separately"}))


if __name__ == "__main__":
    main()
