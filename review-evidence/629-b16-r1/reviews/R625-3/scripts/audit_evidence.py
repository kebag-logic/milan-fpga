#!/usr/bin/env python3
"""Independent reduction of public B16 receipts; no private inputs.

Usage: python3 audit_evidence.py EVIDENCE_PACKET REVIEW_PACKET
"""
import collections
import csv
import hashlib
import json
from pathlib import Path
import statistics
import sys

p, output = map(Path, sys.argv[1:3])
out = {}


def read(rel):
    return json.loads((p / rel).read_text())


def events(run):
    return [json.loads(x) for x in (p / f"runs/{run}/events.jsonl").read_text().splitlines()]


def digest(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()


manifest = []
published = {x['file']: x for x in json.loads((p.parent / 'MANIFEST.json').read_text())}
redactions = []
for line in (p / "MANIFEST.sha256").read_text().splitlines():
    sha, rel = line.split(None, 1)
    file = p / rel
    measured = digest(file)
    publication = published['author-r3/' + rel.removeprefix('./')]
    assert measured == publication['published_sha256'], rel
    assert sha == publication['original_sha256'], rel
    if measured != sha:
        assert publication['path_redacted'], rel
        redactions.append(rel)
    manifest.append(rel)
out["provenance"] = {"evidence_commit": "b84584e4ccb069248909f0fdeb7f8b72a1c41ae4",
                     "files_verified": len(manifest), "manifest_sha256": digest(p / "MANIFEST.sha256"),
                     "publication_redactions": redactions}
for name in ("figures-rows.tsv", "figures-coverage.tsv"):
    assert (output / "receipts" / name).read_bytes() == (p / "r3" / name).read_bytes()
out["figures_outputs_byte_equal"] = True
assert (output / "receipts/b0-recomputed.json").read_bytes() == (p / "r2/b0-2-receipt.json").read_bytes()
out["b0_reduction_byte_equal"] = True

# Derive grades from per-block readings rather than trust the stored summary.
grades = {}
for run in ("pts1", "pts2", "pts3", "b0-2", "bcrf", "baaf"):
    g = read(f"summary/{run}/c-b9-grade.json")
    bs = g["blocks"]
    free = [b for b in bs if b["events"] == 0]
    med = [statistics.median(b[f"ch{i}"]["thdn_db"] for b in free) for i in (0, 1)]
    floor = [b for b in free if all(b[f"ch{i}"]["thdn_db"] <= med[i] + 3 for i in (0, 1))]
    degraded = [b["block"] for b in free if b not in floor]
    s = g["summary"]
    assert len(bs) == s["blocks"] and len(floor) == s["blocks_at_floor"]
    assert degraded == s["degraded_event_free_blocks"]
    rec = {"blocks": len(bs), "floor_blocks": len(floor), "degraded_blocks": degraded,
           "events": len(g["events"]), "phase_net_frames": g["phase_net_frames"]}
    for i in (0, 1):
        for label, group in (("floor", floor), ("all", bs)):
            vals = [b[f"ch{i}"]["thdn_db"] for b in group]
            actual = [round(statistics.median(vals), 2), round(max(vals), 2)]
            expected = s[f"ch{i}_{label}"]
            assert actual == [expected["thdn_db_median"], expected["thdn_db_worst"]]
            rec[f"tone{i}_{label}_median_worst"] = actual
    grades[run] = rec
out["grades"] = grades

alignments = {}
for run in grades:
    rec = {}
    for side in ("a", "b"):
        al = read(f"summary/{run}/align-{side}-c.json")
        assert al["comparison"] == "full 24-bit values" and al["frames_differing"] == 0
        assert al["slips"] == [] and al["verdict"] == "SAMPLE-EXACT"
        lo, hi = al["covered_recording_frames"]
        assert lo == 0 and hi == al["compared_equal"]
        rec[side] = {"compared_frames": hi, "seconds": hi / 48000}
    alignments[run] = rec
cov = min(x["compared_frames"] for x in alignments["b0-2"].values())
whole = cov // 48000
inside = [i for i in grades["b0-2"]["degraded_blocks"] if i < whole]
beyond = [i for i in grades["b0-2"]["degraded_blocks"] if i * 48000 >= cov]
assert (len(inside), len(beyond), whole) == (23, 108, 34)
out["alignments"] = alignments
out["b0_attribution"] = {"whole_blocks": whole, "degraded_inside": inside, "degraded_beyond": beyond,
                         "raw_sample_comparisons_not_rerun": True}

control = {}
for run in ("pts2", "b0-2", "bcrf", "baaf"):
    d = read(f"summary/{run}/d-extcap-pair.json")
    per = []
    for ch, tone in ((0, 997), (1, 9973)):
        t = d["rows"][ch][f"tone_{tone}"]
        blocks = t["per_block"]
        loud = [i for i, b in enumerate(blocks) if b["level_dbfs"] > -200]
        # Drop transition blocks; a final non-silent block is retained only
        # when the published acquisition ends before playback does.
        stop = loud[-1] if loud[-1] < len(blocks) - 1 else len(blocks)
        active = list(range(loud[0] + 1, stop))
        floor = statistics.median(blocks[i]["thdn_db"] for i in active)
        clean = [i for i in active if blocks[i]["thdn_db"] <= floor + 3]
        silent = [i for i, b in enumerate(blocks) if b["level_dbfs"] <= -200]
        assert silent == [0, 1]
        assert (len(active), len(clean)) == ((13, 11) if run == "pts2" else (303, 303))
        per.append({"tone": tone, "silent": silent, "first_transition": loud[0], "active_count": len(active),
                    "floor_count": len(clean), "degraded_active": sorted(set(active) - set(clean))})
    control[run] = per
for side in ("dut", "peer"):
    d = read(f"summary/pts2/ctl-dut-talker-{side}-tap.json")
    for ch, tone in ((0, 997), (1, 9973)):
        bs = d["channels"][ch][f"tone_{tone}"]["per_block"]
        active = [i for i, b in enumerate(bs) if b["level_dbfs"] > -200]
        core = list(range(active[0] + 1, active[-1]))
        med = statistics.median(bs[i]["thdn_db"] for i in core)
        assert len(core) == 15 and all(bs[i]["thdn_db"] <= med + 3 for i in core)
out["positive_control"] = control
out["positive_control_taps"] = {"wholly_playing_blocks_per_tone_per_tap": 15}

def signed(v, bits):
    return v - (1 << bits) if v & (1 << (bits - 1)) else v


polls = {}
for run in ("bcrf", "baaf"):
    rows = list(csv.DictReader((p / f"r2/{run}-poll-trace.tsv").read_text().splitlines(), delimiter="\t"))
    r = read(f"r2/{run}-poll-receipt.json")
    es = events(run)
    raw = next(x for x in es if x["kind"] == "raw" and x["file"] == "poll-run.jsonl")
    assert raw["sha256"] == r["raw"]["sha256"] and raw["bytes"] == r["raw"]["bytes"]
    assert r["events"]["sha256"] == digest(p / f"runs/{run}/events.jsonl")
    decoded = []
    for x in rows:
        w = {k: int(v, 16) for k, v in x.items() if k.startswith("0x")}
        decoded.append(dict(n=int(x["n"]), start=float(x["start_after_set_s"]), length=float(x["length_ms"]) / 1000,
                            state=w["0x8f8"] & 7, trim=signed(w["0x8f8"] >> 16, 16) / 16,
                            crf=signed(w["0x748"], 32) / 512, aaf=signed(w["0x8e4"], 32) / 512,
                            aaf_stat=w["0x8e0"], lb=w["0x8d4"], tdm=w["0x8d8"], servo=w["0x8f8"] & 65535))
    window = r["spans"]["window-start..window-end"]
    ws, we = window["from_s"], window["to_s"]
    selected = [x for x in decoded if ws <= x["start"] and x["start"] + x["length"] <= we]
    assert len(selected) == 596 and all(x["state"] == 4 and x["tdm"] == 0 for x in selected)
    extrema = {key: [min(x[key] for x in selected), max(x[key] for x in selected)] for key in ("trim", "crf", "aaf", "lb", "tdm")}
    assert extrema["trim"] == window["trim_ppm"] and extrema["crf"] == window["crf_rate_ppm"]
    if run == "baaf":
        assert extrema["aaf"] == window["aafm_rate_ppm_valid"]
        assert {x["aaf_stat"] for x in selected} == {0x001e0007}
    else:
        assert {x["aaf_stat"] for x in selected} == {0}
    k = next(i for i, x in enumerate(decoded) if x["start"] >= 0 and x["state"] == 4)
    assert decoded[k - 1]["state"] == 3 and k == r["locked"]["first_locked_poll"]
    lock = [decoded[k - 1]["start"], r["locked"]["recomputed_s"][1]]
    assert lock == ([2.585, 3.161] if run == "bcrf" else [6.602, 7.18])
    assert abs(decoded[k]["start"] + decoded[k]["length"] - lock[1]) < .001
    steps = []
    for a, b in zip(decoded, decoded[1:]):
        if a["lb"] != b["lb"]:
            steps.append({"polls": [a["n"], b["n"]], "states": [a["state"], b["state"]],
                          "dups": [a["lb"] & 65535, b["lb"] & 65535]})
    assert len(steps) == (6 if run == "bcrf" else 7)
    assert all(s["states"] == ([0, 0] if i < 5 else [3, 3]) for i, s in enumerate(steps))
    for got, receipt in zip(steps, r["slip_lb_steps"]):
        assert got["polls"] == receipt["polls"] and got["dups"] == receipt["dups"]
    polls[run] = {"raw_sha256": raw["sha256"], "total_polls": len(rows), "window_polls": len(selected),
                  "extrema": extrema, "lock_bracket_s": lock, "slip_steps": steps,
                  "window_servo_counts": dict(collections.Counter(x["servo"] for x in selected))}
out["poll_audit"] = polls

# Restore each run from the actual event payloads, not equal_to_found alone.
restore = {}
for run in ("loop1", "loop2", "pts1", "pts2", "b0", "b0-2", "pts3", "bcrf", "baaf"):
    es = events(run)
    start = next(x for x in es if x["kind"] == "as-found")
    end = next(x for x in es if x["kind"] == "final")
    keys = [k for k in start if k not in ("kind", "t")]
    assert all(end[k] == start[k] for k in keys), run
    for f in (x for x in es if x["kind"] == "format-check"):
        assert f["ok"]
        if f["set"] is None:
            assert f["listener_fmt"] == f["talker_fmt"]
        else:
            assert f["listener_after"] == f["talker_fmt"]
    sets = [x for x in es if x["kind"] == "set-clock"]
    assert all(x["ok"] and x["status"] == "SUCCESS" and x["readback"] == x["src"] for x in sets)
    if run in ("bcrf", "baaf"):
        seq = [(x["who"], x["src"]) for x in sets]
        assert seq == [("peer", 0), ("dut", 1 if run == "bcrf" else 2), ("dut", 0), ("peer", 1)]
        assert sets[-1]["t"] > max(x["t"] for x in es if x["kind"] == "unbind")
        checks = [x for x in es if x["kind"] == "mcasp-playback-check"]
        assert len(checks) == 4 and all(x["rc"] == 0 and x["out"].strip() == "closed" for x in checks)
    else:
        assert not sets
    restore[run] = {"restored_fields": len(keys), "clock_sequence": [(x["who"], x["src"]) for x in sets],
                    "format_checks": sum(x["kind"] == "format-check" for x in es)}
out["restore"] = restore

def jsonl(rel):
    return [json.loads(x) for x in (p / rel).read_text().splitlines()]


wire_clocks = {}
for run in ("bcrf", "baaf"):
    ctl = [x["line"] for x in jsonl(f"runs/{run}/ctl.jsonl") if "line" in x]
    verified = []
    for i, response in enumerate(ctl):
        if response.get("cmd") != "SET_CLOCK_SOURCE":
            continue
        assert response["status"] == "SUCCESS"
        source = int(response["payload"][8:12], 16)
        following = next(x for x in ctl[i + 1:] if x.get("cmd") == "GET_CLOCK_SOURCE" and x["role"] == response["role"])
        assert following["status"] == "SUCCESS" and int(following["payload"][8:12], 16) == source
        verified.append([response["role"], source])
    assert verified == [[a,b] for a,b in restore[run]["clock_sequence"]]
    wire_clocks[run] = verified
out["controller_clock_responses"] = wire_clocks

volatile = {"t", "seq", "rtt_ms", "sequence_id", "t_tx", "t_rx"}
def stable(x):
    if isinstance(x, dict):
        return {k: stable(v) for k,v in x.items() if k not in volatile}
    if isinstance(x, list):
        return [stable(v) for v in x]
    return x


census = []
for a,b in (("start", "end"), ("startb", "endb"), ("startc", "endc"), ("start", "endc")):
    before = stable(jsonl(f"restore/census-{a}.jsonl"))
    after = stable(jsonl(f"restore/census-{b}.jsonl"))
    assert len(before) == len(after) == 46
    different = [i for i,(x,y) in enumerate(zip(before,after)) if x != y]
    assert len(different) == 1
    x,y = before[different[0]], after[different[0]]
    assert x["what"] == y["what"] == "avb" and x["role"] == y["role"] == "dut"
    assert x["payload"][:15] == y["payload"][:15] and x["payload"][23:] == y["payload"][23:]
    census.append({"before": a, "after": b, "equal_entries": 45, "entries": 46,
                   "different": "DUT live propagation delay", "includes_header": True})
out["census"] = census

counter_sets = {}
for mark in ("startc", "endc"):
    counter_sets[mark] = {}
    for row in jsonl(f"restore/counters-{mark}.jsonl"):
        if row.get("cmd") != "GET_COUNTERS":
            continue
        assert row["status"] == "SUCCESS"
        payload = bytes.fromhex(row["payload"])
        key = (row["role"], int.from_bytes(payload[:2], "big"), int.from_bytes(payload[2:4], "big"))
        counter_sets[mark][key] = [int.from_bytes(payload[i:i+4], "big") for i in range(8,len(payload),4)]
out["counters"] = {}
for role, expected in (("dut", [[22,21],[24,23]]), ("peer", [[6,5],[8,7]])):
    got = [counter_sets[mark][role,36,0][:2] for mark in ("startc", "endc")]
    assert got == expected
    out["counters"][role + "_locked_unlocked"] = got
for idx in (0,1):
    got = [counter_sets[mark]["dut",6,idx][2] for mark in ("startc", "endc")]
    assert got == [0,4]
out["counters"]["dut_talker_media_reset_each"] = [0,4]
for run, frames in (("loop1",1056000), ("loop2",768000)):
    d = read(f"summary/{run}/d-extcap-pair.json")
    assert d["frames"] == frames and all(x["min"] == x["max"] == x["nonzero"] == 0 for x in d["rows"])

source = read("r2/source-receipt.json")
raws = {x["path"]: x for x in read("RAW-ARTIFACTS.json")["files"]}
for label, rec in source["reads"].items():
    assert raws[f"source/{label}.json"]["sha256"] == rec["sha256"]
out["source_reads"] = {"raw_hash_bindings": len(source["reads"]), "class_map_sha256": source["class_map_sha256"],
                       "comparisons": source["compare"], "limit": "Raw reads and class map withheld; reductions reviewed, raw extraction not rerun."}
acmp = read("summary/loop2/acmp-peer-tap.json")["acmp"]
probes = [x for x in acmp if x["msg"] == "CONNECT_TX_COMMAND"]
responses = [x for x in acmp if x["msg"] == "CONNECT_TX_RESPONSE"]
assert len(probes) == 2 and not responses
out["loopback"] = {"probes": len(probes), "responses": len(responses), "probe_gap_ms": round((probes[1]["t"] - probes[0]["t"]) * 1000, 1)}
out["pass"] = True
(output / "receipts/independent-audit.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps({"pass": True, "manifest_files": len(manifest), "graded_runs": len(grades), "restored_runs": len(restore)}))
