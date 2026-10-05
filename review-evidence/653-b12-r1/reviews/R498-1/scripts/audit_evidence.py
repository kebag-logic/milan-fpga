#!/usr/bin/env python3
"""Offline review of public receipts; emits no bench identities.

Usage: python3 audit_evidence.py EVIDENCE_ROOT REPOSITORY OUTPUT_DIRECTORY
EVIDENCE_ROOT contains MANIFEST.json and author/. No hardware access occurs.
"""
import collections
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

root, repo, out = map(Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
src = root / "author"


def read(name):
    return json.loads((src / name).read_text())


def many(pattern):
    return [r for f in sorted(src.glob(pattern)) for r in json.loads(f.read_text())]


def save(name, data):
    (out / name).write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


manifest = json.loads((root / "MANIFEST.json").read_text())
assert all(hashlib.sha256((root / m["file"]).read_bytes()).hexdigest() ==
           m["published_sha256"] for m in manifest)
cycles = {r["cycle"]: r for r in many("cycles-*.json")}
wire = {r["cycle"]: r for r in many("wire-receipts-*.json")}
assert len(cycles) == len(wire) == 182 and cycles.keys() == wire.keys()
csv_rows = list(csv.DictReader((src / "cycles.csv").open()))
assert {r["cycle"] for r in csv_rows} == cycles.keys()
polls = [r for name in ("short-polls.csv", "long-polls.csv")
         for r in csv.DictReader((src / name).open())]
early = [r for r in polls if r["phase"].startswith("first-pdus-")]
assert len(polls) == 1510 and len(early) == 546
assert all(r["status"] == "Success." and int(r["SI"]) == int(r["SEQ"]) == 0
           for r in polls)


def pdu(raw):
    # A six-byte controller-host prefix was redacted in the public export.
    # Its neutral replacement permits field parsing, never identity recovery.
    return bytes.fromhex(raw.replace("<controller-host-id>", "000000000000"))


intervals, firsts = [], []
for tag, r in sorted(wire.items()):
    c = cycles[tag]
    a, b, u = (r[k] for k in ("command", "response", "unlock"))
    aa, bb, uu = (pdu(x["raw"]) for x in (a, b, u))
    assert aa[0:2] == bytes([0xfc, 8]) and bb[0:2] == bytes([0xfc, 9])
    assert aa[12:20] == bb[12:20] == uu[12:20]
    assert aa[28:36] == bb[28:36] == uu[4:12]
    assert aa[38:40] == bb[38:40] == uu[26:28]
    assert aa[48:50] == bb[48:50]
    assert uu[0:2] == bytes([0xfb, 1]) and uu[22:26] == bytes.fromhex("80290005")
    assert bb[2] >> 3 == uu[2] >> 3 == 0
    assert b["status"] == u["status"] == c["status"] == 0
    assert int.from_bytes(uu[28:32], "big") & 0xf == 0xf
    decoded = [int.from_bytes(uu[i:i+4], "big") for i in range(32, 48, 4)]
    assert decoded == [1, 1, 0, 0]
    assert a["i"] < b["i"] < u["i"] and a["tns"] < b["tns"] < u["tns"]
    assert r["capture"] == c["selected_capture"]
    assert r["capture"].endswith("plain.pcap" if c["direction"] == "A" else "observer.pcap")
    delta = (u["tns"] - b["tns"]) / 1000
    assert delta == c["response_unlock_us"]
    assert (b["tns"] - a["tns"]) / 1000 == c["command_response_us"]
    assert c["order"] == "RESPONSE_FIRST" and c["library_state"] == "NotConnected"
    assert c["earlier_unlock_notifications"] == c["nonmonotonic"] == 0
    assert r["format_read"]["talker_status"] == r["format_read"]["listener_status"] == "Success."
    assert r["format_read"]["talker_format"] == r["format_read"]["listener_format"]
    intervals.append({"cycle": tag, "clock": "DUT-link capture" if c["direction"] == "A" else "controller capture",
                      "command_ns": a["tns"], "response_ns": b["tns"], "unlock_ns": u["tns"],
                      "response_unlock_us": delta, "status": 0})
    frames = r["first_twelve_pdus"]
    assert len(frames) == 12
    assert all((y["seq"] - x["seq"]) % 256 == 1 and y["tns"] > x["tns"]
               for x, y in zip(frames, frames[1:]))
    assert all(x["tns"] >= r["bind_command_tap_ns"] for x in frames)
    firsts.append({"cycle": tag, "bind_to_first_ms": (frames[0]["tns"] - r["bind_command_tap_ns"]) / 1e6,
                   "sequences": [x["seq"] for x in frames],
                   "spacing_us": [(y["tns"]-x["tns"])/1000 for x,y in zip(frames, frames[1:])],
                   "presentation_timestamps_present": False})

fixed = [c for c in cycles.values() if c["phase"] == "exact" and c["requested_hold_ms"] < 600000]
edges = [c for c in cycles.values() if c["phase"] != "exact"]
longs = [c for c in cycles.values() if c["requested_hold_ms"] == 600000]
assert (len(fixed),len(edges),len(longs)) == (140,40,2)
matrix = collections.Counter((c["direction"],c["kind"],c["requested_hold_ms"]) for c in fixed)
assert len(matrix) == 28 and set(matrix.values()) == {5}
assert set(x[2] for x in matrix) == {300,600,900,1000,1100,1500,3000}
phase_ranges = []
for direction in "AB":
    for kind in ("AAF", "CRF"):
        for phase in ("before", "after"):
            vals = [c["last_push_to_command_ms"] for c in edges
                    if (c["direction"], c["kind"], c["phase"]) == (direction,kind,phase)]
            assert len(vals) == 5
            assert all(950 < v < 1000 if phase == "before" else 0 < v < 50 for v in vals)
            phase_ranges.append({"direction": direction,"kind":kind,"phase":phase,
                                 "count":len(vals),"min_ms":min(vals),"max_ms":max(vals)})
for c in longs:
    ps = [r for r in polls if r["cycle"] == c["cycle"]]
    assert len(ps) == 305 and sum(r["phase"].startswith("hold-") for r in ps) == 300
    assert c["actual_hold_ms"] >= 600000 and c["stream_gaps"] == 0

page = (repo / "docs/findings/653_DISCONNECT_ORDER_BENCH.md").read_text().splitlines()[393:]
table_tags = set()
for line in page:
    if not line.startswith("| "):
        continue
    cells = [x.strip() for x in line.strip("|").split("|")]
    if cells[0] not in cycles or "SUCCESS" not in cells:
        continue
    c = cycles[cells[0]]; table_tags.add(cells[0])
    d = next(x for x in cells if x.startswith("R / "))
    assert abs(float(d[4:]) - c["response_unlock_us"]) < .00051
    if c in fixed: shown = float(cells[1].split(" / ")[1])
    elif c in edges: shown = float(cells[2])
    else: shown = float(cells[1])
    assert abs(shown-c["actual_hold_ms"]) < .00051
assert table_tags == cycles.keys()

startup = []
for event in read("rule-increments.json"):
    tag = event["cycle"]
    selected = [{k:r[k] for k in ("phase","utc","since_bind_command_ms","ML","MU","EARLY","LATE","FRX")}
                for r in polls if r["cycle"] == tag]
    startup.append({"cycle":tag,"application_callback_us":event["t"],"increments":event["increments"],
                    "counter_reads":selected,"first_twelve":next(x for x in firsts if x["cycle"] == tag)})

restore = read("restore-comparison.json")
expected = [4,4,2,2,14,14,2,1]
assert restore["pass_restore"] and [r["observations"] for r in restore["rows"]] == expected
assert all(r["equal"] and r["start_sha256"] == r["end_sha256"] and not r["different_keys"]
           for r in restore["rows"])
required = [f"{name}-{when}.jsonl" for name in ("census","dut-descs","peer-descs") for when in ("start","end")]
missing = [n for n in required if not (src/n).exists()]

sys.path.insert(0, str(repo / "scripts"))
import docs_check
privacy = []
scan_files = [root / m['file'] for m in manifest] + [root/'MANIFEST.json']
for f in scan_files:
    for n,line in enumerate(f.read_text().splitlines(),1):
        for rule in (*docs_check.IDENTITY_RULES,*docs_check.LOCAL_RULES):
            if rule[0].search(line): privacy.append({"file":str(f.relative_to(root)),"line":n,"category":rule[1]})
identity = read("identity.json")
payload = bytes.fromhex(identity["descriptor_payload"])
encoded_identity = [{"offset":m.start(),"length":len(m.group()),"field":label}
                    for m,label in zip(re.finditer(rb"[\x20-\x7e]{6,}",payload),
                                       ("entity name", "firmware version", "device serial"))]
page_identity = []
for field in encoded_identity:
    if field['field'] == 'firmware version':
        continue
    value = payload[field['offset']:field['offset']+field['length']].decode('ascii')
    for number,line in enumerate((repo/'docs/findings/653_DISCONNECT_ORDER_BENCH.md').read_text().splitlines(),1):
        if value in line:
            page_identity.append({'line':number,'field':field['field'],'in_added_section':number>=394})
save("privacy.json",{"text_rule_findings":privacy,"files_scanned":len(scan_files),
                     "encoded_identity_fields":encoded_identity,
                     "existing_page_identity_fields":page_identity,
                     "descriptor_artifact":"author/identity.json:10",
                     "serial_label_redacted":identity["readback"]["serial_number"] == "<device-serial>",
                     "encoded_serial_redacted":False})
save("intervals.json",intervals)
save("first-pdus.json",firsts)
save("timestamp-startup.json",startup)
save("summary.json",{"evidence_manifest_files_verified":len(manifest),"cycles":len(cycles),
                      "wire_intervals_recomputed":len(intervals),"status_zero":len(intervals),
                      "page_numeric_rows_verified":len(table_tags),"fixed_cycles":len(fixed),
                      "boundary_cycles":len(edges),"boundary_phase_ranges":phase_ranges,
                      "all_counter_reads":len(polls),"early_reads":len(early),
                      "early_reads_zero_frames_counter":sum(int(r["FRX"]) == 0 for r in early),
                      "first_pdu_sequence_checks":len(firsts),"reported_long_windows":[
                          {k:c[k] for k in ("cycle","actual_hold_ms","stream_frames","stream_gaps")} for c in longs],
                      "restore_digest_groups_equal":len(restore["rows"]),
                      "restore_readback_inputs_absent_from_public_packet":missing,
                      "limits":["Library states and full-capture totals remain operator receipts.",
                                "Selected event intervals were recomputed within each selected capture clock.",
                                "Boundary phases and bound durations lack original anchor events in the bounded export.",
                                "No hardware or physical calibration was run."]})
print("PASS: 62 manifest files, 182 same-clock intervals and table rows, 182 initial sequence checks")
print("PASS: 140 fixed cycles, 40 boundary receipts, 1510 zero sequence/interruption reads")
print("OPEN: encoded identity, omitted startup timestamp analysis, unavailable restoration readback inputs")
