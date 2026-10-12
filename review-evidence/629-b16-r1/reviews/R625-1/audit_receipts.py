#!/usr/bin/env python3
"""Reconcile public receipts with the exact-head findings; no capture re-grade.

Usage: audit_receipts.py <candidate> <evidence-root-containing-MANIFEST.json>
"""
import hashlib
import json
from pathlib import Path
import re
import statistics
import sys

root, evidence = map(Path, sys.argv[1:])
p = evidence / "author-r1"
doc = (root / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md").read_text()
doc = doc[doc.index("\n## Dev 5603c353, 2026-10-12: lane B16"):]
result = {}
errors = []


def get(path):
    return json.loads((p / path).read_text())


def events(run):
    return [json.loads(line) for line in (p / "runs" / run / "events.jsonl").read_text().splitlines()]


def ensure(ok, label):
    if not ok:
        errors.append(label)


manifest = json.loads((evidence / "MANIFEST.json").read_text())
for row in manifest:
    ensure(hashlib.sha256((evidence / row["file"]).read_bytes()).hexdigest() == row["published_sha256"],
           "publication hash: " + row["file"])
result["publication_manifest_files"] = len(manifest)
hashes = {r["published_sha256"]: (evidence / r["file"]).stat().st_size for r in manifest}
raw = get("RAW-ARTIFACTS.json")["files"]
raw_hashes = {r["sha256"]: r["bytes"] for r in raw}
table_hashes = []
for line in doc.splitlines():
    m = re.search(r"\| ([\d,]+|Withheld) \| `([0-9a-f]{64})` \|$", line)
    if not m:
        continue
    size, digest = m.groups()
    actual = hashes.get(digest, raw_hashes.get(digest))
    ensure(actual is not None, "unmatched documented hash: " + digest)
    if size != "Withheld":
        ensure(actual == int(size.replace(",", "")), "documented size: " + digest)
    table_hashes.append(digest)
result["documented_hash_size_rows_checked"] = len(table_hashes)
result["raw_capture_limit"] = "Raw captures and poll histories are hash inventories, not published samples."

points = {}
for run in ("pts1", "pts2", "pts3", "b0-2", "bcrf", "baaf"):
    for point, name in (("a", "a-peer-tap.json"), ("b", "b-dut-tap.json"), ("c", "c-mcasp.json")):
        d = get(f"summary/{run}/{name}")
        ensure(d["tone_channels"] == {"997": [0], "9973": [1]}, f"{run}/{point} tone channels")
        if point != "c":
            ensure(d["info"]["seq_gaps"] == 0 and d["info"]["bad_length"] == 0, f"{run}/{point} gaps/length")
        points[run, point] = d
        for index, tone in ((0, "tone_997"), (1, "tone_9973")):
            t = d["channels"][index][tone]
            ensure(t["blocks"] == len(t["per_block"]), f"{run}/{point} block inventory")
            # Stored medians are rounded separately; compare at published precision.
            for key, value in t["median"].items():
                median = statistics.median(b[key] for b in t["per_block"])
                ensure(abs(median - value) < 0.0011, f"{run}/{point}/{tone}/{key} median")

point_rows = 0
for line in doc.splitlines():
    cells = [c.strip() for c in line.split("|")[1:-1]]
    if len(cells) != 10 or cells[1] not in ("(a)", "(b)", "(c)"):
        continue
    match = re.match(r"`([^`]+)`", cells[0])
    if not match or (match[1], cells[1][1]) not in points:
        continue
    run, point = match[1], cells[1][1]
    d = points[run, point]
    expected_frames = f"{d['frames']:,}"
    if point != "c":
        expected_frames += f"; {d['info']['pdus']:,} PDUs, {d['info']['seq_gaps']} gaps"
    ensure(cells[2] == expected_frames, f"{run}/{point} displayed frames")
    ensure(cells[3] == f"{d['channels'][0]['tone_997']['median']['level_dbfs']:.4f}", f"{run}/{point} displayed level")
    for index, tone, offset in ((0, "tone_997", 4), (1, "tone_9973", 7)):
        t = d["channels"][index][tone]
        m = t["median"]
        ensure(cells[offset+1] == f"{m['thdn_db']:.2f} ({t['worst_thdn_db']:.2f})", f"{run}/{point}/{tone} displayed THD+N")
        # A four-decimal receipt can straddle a two-decimal rounding tie.
        ensure(abs(float(cells[offset+2]) - m['snr_db']) <= 0.005051,
               f"{run}/{point}/{tone} displayed SNR")
        frequency, ppm = re.match(r"([\d,.]+) Hz, ([-+\d.]+) ppm", cells[offset]).groups()
        ensure(abs(float(frequency.replace(',', '')) - m['f_hz']) <= 0.000051, f"{run}/{point}/{tone} displayed frequency")
        ensure(abs(float(ppm) - m['ppm']) <= 0.0051, f"{run}/{point}/{tone} displayed offset")
    point_rows += 1
result["point_table_rows_checked"] = point_rows

grades = {}
for run in ("pts1", "pts2", "pts3", "b0-2", "bcrf", "baaf"):
    d = get(f"summary/{run}/c-b9-grade.json")
    blocks = d["blocks"]
    summary = d["summary"]
    free = [b for b in blocks if b['events'] == 0]
    med = {ch: statistics.median(b[ch]["thdn_db"] for b in free) for ch in ('ch0', 'ch1')}
    floor = [b for b in free if all(b[ch]['thdn_db'] <= med[ch] + 3 for ch in med)]
    ensure(summary['blocks_at_floor'] == len(floor), run + " floor count")
    ensure(summary['blocks'] == len(blocks), run + " total blocks")
    ensure(summary['events'] == len(d['events']) == 0, run + " no events")
    for ch in ('ch0', 'ch1'):
        for label, group in [('all', blocks), ('floor', floor)]:
            s = summary[f'{ch}_{label}']
            ensure(s['thdn_db_median'] == round(statistics.median(b[ch]['thdn_db'] for b in group), 2), run + ch + label + " THD+N")
            ensure(s['thdn_db_worst'] == round(max(b[ch]['thdn_db'] for b in group), 2), run + ch + label + " worst")
            ensure(s['snr_db_median'] == round(statistics.median(b[ch]['snr_db'] for b in group), 2), run + ch + label + " SNR")
    grades[run] = {"blocks": len(blocks), "at_floor": len(floor), "degraded": len(free)-len(floor),
                   "phase_net_frames": d['phase_net_frames'], "summary": summary}
result['grades'] = grades

alignment = {}
for run in ('pts1', 'pts2', 'pts3', 'b0-2', 'bcrf', 'baaf'):
    for point in ('a', 'b'):
        d = get(f'summary/{run}/align-{point}-c.json')
        ensure(d['verdict'] == 'SAMPLE-EXACT' and d['frames_differing'] == 0 and not d['slips'], run + point + ' alignment')
        ensure(d['compared_equal'] == d['covered_recording_frames'][1]-d['covered_recording_frames'][0], run + point + ' coverage')
        alignment[run+'-'+point] = d
result['alignment'] = alignment
result['b0_attribution_boundary'] = {
    "peer_link_frames": points['b0-2', 'a']['frames'],
    "peer_link_whole_blocks": points['b0-2', 'a']['channels'][0]['tone_997']['blocks'],
    "output_frames": points['b0-2', 'c']['frames'],
    "output_whole_blocks": grades['b0-2']['blocks'],
    "output_degraded_blocks": grades['b0-2']['degraded'],
    "directly_compared_frames": alignment['b0-2-a']['compared_equal'],
    "claimed_131_peer_link_blocks_supported": False,
}

for run in ('loop1', 'loop2'):
    for point, name in [('a', 'a-peer-tap.json'), ('b', 'b-dut-tap.json')]:
        ensure(get(f'summary/{run}/{name}')['frames'] == 0, run + point + ' no stream')
acmp = get('summary/loop2/acmp-peer-tap.json')['acmp']
probes = [a for a in acmp if a['msg'] == 'CONNECT_TX_COMMAND']
ensure(len(probes) == 2, 'loopback probe count')
ensure(not any(a['msg'] == 'CONNECT_TX_RESPONSE' for a in acmp), 'loopback no probe response')
result['loopback'] = {'probes': len(probes), 'probe_interval_ms': (probes[1]['t']-probes[0]['t'])*1000,
                      'probe_responses': 0}

state = {}
for run in ('loop1','loop2','pts1','pts2','b0','b0-2','pts3','bcrf','baaf'):
    ev = events(run)
    fin = next(e for e in ev if e['kind'] == 'final')
    ensure(fin['equal_to_found'] and not fin['differ'], run+' full readback')
    sets = [e for e in ev if e['kind'] == 'set-clock']
    for e in sets:
        ensure(e['status'] == 'SUCCESS' and e['readback'] == e['src'], run+' clock set/read')
    formats = [e for e in ev if e['kind'] == 'format-check']
    ensure(all(e['ok'] for e in formats), run+' formats')
    if run in ('bcrf','baaf'):
        expected = [('peer',0),('dut',1 if run=='bcrf' else 2),('dut',0),('peer',1)]
        ensure([(e['who'],e['src']) for e in sets] == expected, run+' clock order')
        summary = next(e for e in ev if e['kind']=='poll-summary')
        window = summary['spans']['window-start..window-end']
        ensure(window['polls']==596 and window['servo']=={'LOCKED':596} and window['failed']==0, run+' lock window')
        ensure(window['first']['0x8d8']==window['last']['0x8d8']=='00000000' and window['distinct']['0x8d8']==1, run+' static TDM')
        ensure(window['distinct']['0x8d4']==1, run+' static loopback')
        tone = next(e for e in ev if e['kind']=='tone-summary')
        ensure(tone['states']=={'RUNNING':tone['reads']} and tone['hw_ptr_monotonic'], run+' tone running')
        state[run] = {'sets':sets, 'window':window, 'lock':next(e for e in ev if e['kind']=='servo-state'),
                      'tone':tone, 'final_equal':True}
    else:
        ensure(not sets, run+' no clock changes')
        state[run] = {'clock_sets':0, 'format_checks':len(formats), 'final_equal':True}
result['state_records'] = state
gate = get('gates/b16c/results.json')
ensure(gate['head']=='e20fd2820a9c6b9effabc529a742e732263fafa8' and all(g['rc']==0 for g in gate['gates']), 'author exact-head gates')
result['author_gates'] = {'head':gate['head'], 'entries':len(gate['gates']), 'all_rc0':gate['all_rc0'],
                         'execution_scope':'author documentation gates; no manager source bank'}
result['reconciliation_errors'] = errors
print(json.dumps(result, indent=2))
sys.exit(int(bool(errors)))
