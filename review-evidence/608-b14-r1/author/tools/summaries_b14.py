#!/usr/bin/env python3
"""Lane B14: bounded summaries of items 3, 5, 6 and 7 for the packet (read-only; nothing here touches the bench).

usage: summaries_b14.py <packet_dir>
Writes:
  item3/summary.json, item3/cycles.tsv   from item3/cycles/*/analysis.json and result.json (an608_b14.py);
  soak/summary.json                      from soak/run-events.jsonl, soak/console-*.txt, soak/capture-receipts.jsonl
                                         and the raw counter and timing reads under $VALIDATION_STORAGE/608-b14-raw/soak;
  maap/summary.json                      from /tmp/608-b14/raw/maap-soak.json (maap_b14.py) and the console's MAAP words.
The soak wire aggregate, coverage and overlap recovery are read from the receipts the lane's
analysis commands wrote under /tmp/608-b14/raw (soak-wire-aggregate.txt, soak-coverage.txt,
soak-overlap-recovery.txt) and copied verbatim into soak/.
"""
import collections
import glob
import json
import re
import shutil
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import b7_decode as X  # noqa: E402

pk = Path(sys.argv[1])
RAWS = Path("$VALIDATION_STORAGE/608-b14-raw/soak")

# ---- item 3 --------------------------------------------------------------------------------------
rows = []
for f in sorted(pk.glob("item3/cycles/cycle-*/analysis.json")):
    a = json.loads(f.read_text())
    r = json.loads((f.parent / "result.json").read_text())
    log = (f.parent / "action.log").read_text() if (f.parent / "action.log").exists() else ""
    lk = re.findall(r"^(LOCK|UNLOCK) (\S+)", log, re.M)
    ev = [l.split("\t") for l in (f.parent / "msrp.tsv").read_text().splitlines()[1:]]
    D, R = a["disconnect_response_s"], a["response_s"]
    hold = sorted({(e[1], e[2], e[3]) for e in ev if D - 0.001 <= float(e[0]) < R and e[4] in ("0200000000010001", "None")})
    rows.append(dict(cycle=a["name"], graded=a["name"] != "cycle-001", capture_rc=r.get("capture_rc"),
                     lock=[t for _, t in lk], stop_608=a["stop_608"], registrar_at_lv=a["registrar_at_lv"],
                     lv_after_disconnect_s=a["bridge_lv_after_disconnect_s"], last_pdu_after_lv_s=a["last_pdu_after_lv_s"],
                     last_pdu_after_disconnect_s=a["last_pdu_after_disconnect_s"],
                     pdus_after_lv_plus_period=a["pdus_after_lv_plus_period"], hold_pdus=a["hold_pdus"],
                     settled_pdus=a["settled_pdus"], start_stop_delta=a["dut_out1_start_stop_delta"],
                     restart_75=a["restart_75"], restart_s=a["restart_s"],
                     bridge_ready_after_response_s=a["bridge_ready_after_response_s"],
                     dut_ta_lv_in_hold=a["dut_ta_lv_in_hold"], msrp_hold_profile=hold,
                     leaveall_pdus_by_sender=a["leaveall_pdus_by_sender"], msrp_pdus_by_sender=a["msrp_pdus_by_sender"],
                     span_s=a["capture_span_s"], malformed=len(a["msrp_malformed"])))
g = [r for r in rows if r["graded"]]


def rng(k, rs=g):
    v = [r[k] for r in rs if r[k] is not None]
    return dict(n=len(v), min=min(v), median=statistics.median(v), max=max(v)) if v else None


prof = collections.Counter(json.dumps(r["msrp_hold_profile"]) for r in g)
s3 = dict(cycles=len(rows), graded=len(g), graded_range=[g[0]["cycle"], g[-1]["cycle"]],
          stop_608=dict(collections.Counter(r["stop_608"] for r in g)),
          restart_75=dict(collections.Counter(r["restart_75"] for r in g)),
          registrar_at_lv=dict(collections.Counter(r["registrar_at_lv"] for r in g)),
          start_stop_delta=dict(collections.Counter(json.dumps(r["start_stop_delta"]) for r in g)),
          pdus_after_lv_plus_period=dict(collections.Counter(r["pdus_after_lv_plus_period"] for r in g)),
          settled_pdus=dict(collections.Counter(r["settled_pdus"] for r in g)),
          lv_after_disconnect_s=rng("lv_after_disconnect_s"), last_pdu_after_lv_s=rng("last_pdu_after_lv_s"),
          last_pdu_after_disconnect_s=rng("last_pdu_after_disconnect_s"), restart_s=rng("restart_s"),
          bridge_ready_after_response_s=rng("bridge_ready_after_response_s"), hold_pdus=rng("hold_pdus"),
          leaveall_pdus_by_sender=dict(sum((collections.Counter(r["leaveall_pdus_by_sender"]) for r in g), collections.Counter())),
          msrp_pdus_by_sender=dict(sum((collections.Counter(r["msrp_pdus_by_sender"]) for r in g), collections.Counter())),
          capture_s_total=round(sum(r["span_s"] for r in g), 3), malformed_msrp=sum(r["malformed"] for r in rows),
          hold_profiles=[dict(cycles=v, events=json.loads(k)) for k, v in prof.most_common()],
          pilot=[r for r in rows if not r["graded"]])
(pk / "item3" / "summary.json").write_text(json.dumps(s3, indent=1) + "\n")
with open(pk / "item3" / "cycles.tsv", "w") as f:
    cols = ["cycle", "graded", "stop_608", "registrar_at_lv", "lv_after_disconnect_s", "last_pdu_after_lv_s",
            "pdus_after_lv_plus_period", "hold_pdus", "start_stop_delta", "restart_s", "bridge_ready_after_response_s",
            "dut_ta_lv_in_hold", "capture_rc", "lock"]
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join(str(r[c]) for c in cols) + "\n")

# ---- soak (items 5 and 6) -------------------------------------------------------------------------
ev = [json.loads(l) for l in open(pk / "soak" / "run-events.jsonl")]
polls = [e for e in ev if e.get("event") == "soak_poll"]
chunks = [e for e in ev if e.get("event") in ("chunk_start", "chunk_end")]


def load(f):
    return {f"{r['role']}|{r['descriptor_type']}|{r['descriptor_index']}": r for r in (json.loads(l) for l in open(f))}


first, last = load(RAWS / "counters-soak-000.jsonl"), load(RAWS / "counters-soak-120.jsonl")
names = {5: X.CTR_NAMES[5], 6: X.CTR_NAMES[6], 36: X.CTR_NAMES[0x24], 9: X.CTR_NAMES[9]}
deltas = {}
for k, a in first.items():
    b = last[k]
    if a["status"] != "SUCCESS":
        deltas[k] = dict(status=[a["status"], b["status"]])
        continue
    nm = names.get(a["descriptor_type"], {})
    deltas[k] = dict(valid_mask=hex(a["valid_mask"]),
                     counters={nm.get(int(i), i): dict(at_first_poll=a["counters"][i], delta=b["counters"][i] - a["counters"][i])
                               for i in a["counters"]})
t0 = [json.loads(l) for l in open(RAWS / "timing-postbind.jsonl")]
tchg = 0
treads = 0
for f in sorted(glob.glob(str(RAWS / "timing-soak-*.jsonl"))):
    treads += 1
    for r, b in zip((json.loads(l) for l in open(f)), t0):
        tchg += sum(r.get(k) != b.get(k) for k in ("gm_fingerprint", "as_capable", "path_fingerprint", "path_count", "domain"))


def word(t, addr, n):
    i = t.find(f"cmd='mem_read {addr} {n}'")
    if i < 0:
        return None
    seg = t[i:].split("litex", 1)[0]
    by = []
    for m in re.finditer(r"^0x9[0-9a-f]{7}\s+((?:[0-9a-f]{2} )+)", seg, re.M):
        by += m.group(1).split()
    b = bytes(int(x, 16) for x in by[:n])
    return [f"{int.from_bytes(b[k:k + 4], 'little'):08x}" for k in range(0, len(b), 4)]


cons = []
for f in sorted((pk / "soak").glob("console-*.txt")):
    t = f.read_text()
    m = re.search(r"### (\S+) cmd='milan_status'", t)
    sy = re.search(r"SYNC=(\d) ASCAPABLE=(\d) TU=(\d)", t)
    cons.append(dict(read=f.stem[8:], utc=m.group(1) if m else None, sync_ascapable_tu="".join(sy.groups()) if sy else None,
                     gm_equals_parent=(re.search(r"GPTP_GM=(\w+)", t).group(1) == re.search(r"GPTP_PARENT=(\w+)", t).group(1)),
                     mac_status=word(t, "0x90000110", 4), rmon_0x200_0x230=word(t, "0x90000200", 52),
                     maap_0x6cc_0x6d4=word(t, "0x900006cc", 12), slip_render_0x8d4_0x8dc=word(t, "0x900008d4", 12),
                     servo_0x8f8=word(t, "0x900008f8", 4)))
rec = [json.loads(l) for l in open(pk / "soak" / "capture-receipts.jsonl")]
drops = collections.Counter()
for r in rec:
    m = re.search(r"(\d+) packets dropped by kernel", " ".join(r["summary"]))
    drops["with_statistic" if m else "without_statistic"] += 1
    drops["kernel_drops"] += int(m.group(1)) if m else 0
art = [json.loads(l) for l in open(pk / "soak" / "capture-artifacts.jsonl")]
for name in ("soak-wire-aggregate.txt", "soak-coverage.txt", "soak-overlap-recovery.txt"):
    shutil.copy(f"/tmp/608-b14/raw/{name}", pk / "soak" / name)
s5 = dict(t0_utc=__import__("time").strftime("%Y-%m-%dT%H:%M:%S", __import__("time").gmtime(json.load(open(RAWS / "state.json"))["t0"])),
          polls=len(polls), last_elapsed_s=polls[-1]["elapsed_s"], chunks=sum(e["event"] == "chunk_start" for e in chunks),
          polls_with_errors=sum(bool(p["errors"]) for p in polls), timing_polls=sum(p["timing"] for p in polls),
          console_polls=sum(p["console_rc"] is not None for p in polls), console_rc_nonzero=sum(bool(p["console_rc"]) for p in polls),
          hive_rule_increments=sum(p["hive_increments"] for p in polls),
          timing_reads=treads, timing_changes=tchg, counter_deltas_first_to_last_poll=deltas,
          console=cons, captures=len(rec), capture_statistics=dict(drops),
          capture_bytes=sum(a["bytes"] for a in art), capture_files=len(art),
          capture_remote_hash_matches=all(a["remote_hash_matches"] for a in art))
(pk / "soak" / "summary.json").write_text(json.dumps(s5, indent=1) + "\n")

# ---- item 7 --------------------------------------------------------------------------------------
m = json.load(open("/tmp/608-b14/raw/maap-soak.json"))
mw = sorted({tuple(c["maap_0x6cc_0x6d4"]) for c in cons if c["maap_0x6cc_0x6d4"]})
s7 = dict(captures=m["captures"], pdus=m["pdus"], duplicates_dropped=m["duplicates_dropped"], covered_s=m["covered_s"],
          span_s=m["span_s"], by_sender=m["by_sender"], overlaps=m["overlaps"], non_announce=m["non_announce"],
          console_maap_words_distinct=mw)
(pk / "maap").mkdir(exist_ok=True)
(pk / "maap" / "summary.json").write_text(json.dumps(s7, indent=1) + "\n")
print(json.dumps(dict(item3=dict(cycles=s3["cycles"], graded=s3["graded"], stop=s3["stop_608"]), soak=dict(polls=s5["polls"], errors=s5["polls_with_errors"]),
                      maap=dict(pdus=s7["pdus"], overlaps=len(s7["overlaps"])))))
