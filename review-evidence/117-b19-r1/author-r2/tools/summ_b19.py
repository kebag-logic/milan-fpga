"""Lane B19: the findings-page tables from the analyses; no bench access.

usage: summ_b19.py   reads bench/cycleNN/{analysis,correlation}.json, firstreach/analysis.json,
bench/retention/retention.json; writes summary/cycles.md, summary/correlation.md, summary/firstreach.md
and summary/retention.md. Console times are the DUT-PHC placements of corr_analyze.py (the first
sample that shows the new value); wire times are the tap's, on the same base.
"""
from pathlib import Path
import json

P = Path(__file__).resolve().parent.parent
f = lambda x, n=2: "-" if x is None else f"{x:.{n}f}"
rows, crow, srow = [], [], []
for i in range(1, 7):
    a = json.load(open(P / f"bench/cycle{i:02d}/analysis.json"))
    c = json.load(open(P / f"bench/cycle{i:02d}/correlation.json"))
    E, W = c["edges"], c["wire"]
    first = lambda fld, to: next((e["first_after"] for e in E[fld] if str(e["to"]) == str(to)), None)
    last = lambda fld, to: [e for e in E[fld] if str(e["to"]) == str(to)][-1]["first_after"] if [e for e in E[fld] if str(e["to"]) == str(to)] else None
    sync0, gmself, asc0 = first("sync", 0), first("gm", "020000fffe000001"), first("asCapable", 0)
    asc1, gmsw, sync1, tu0 = last("asCapable", 1), last("gm", "3cc0c6fffefe0210"), last("sync", 1), last("tu", 0)
    allgood = max(x for x in (asc1, gmsw, sync1, tu0) if x is not None)
    ann = W["switch_announces_after_return"][0][0]
    rec = allgood - ann
    bound = i <= 3
    rows.append(f"| {i} | {'yes' if bound else 'no'} | {a['off_hold_s']:.2f} | {f(sync0)} | {f(gmself)} | {f(asc0)} | {f(W['switch_first_frame'])} | "
                f"{f(ann)} | {f(asc1)} | {f(gmsw)} | {f(allgood)} | **{rec:.2f}** | {'PASS' if rec <= 5 else 'FAIL'} |")
    acc = [x for x in W["switch_announces_after_return"] if x[0] <= gmsw]
    pd2 = W["dut_completed_pdelay_after_return"][1] if len(W["dut_completed_pdelay_after_return"]) > 1 else None
    tub = next((e for e in E["tu"] if str(e["to"]) == "1"), None)
    crf1 = next((x for x in c["crf_tu_vs_csr"] if x["wire"]["to"] == 1), None)
    crow.append(dict(cycle=i, sync_after_last_sync=[round(e["last_before"] - W["switch_last_sync"], 2) for e in E["sync"] if str(e["to"]) == "0"][0],
                     sync_after_last_sync_hi=round(sync0 - W["switch_last_sync"], 2),
                     gm_after_last_ann=[round(e["last_before"] - W["switch_last_announce"], 2) for e in E["gm"] if e["to"] == "020000fffe000001"][0],
                     gm_after_last_ann_hi=round(gmself - W["switch_last_announce"], 2),
                     asc0_after_last_resp=[round(asc0 - 0.25 - W["switch_last_pdelay_resp"], 2), round(asc0 - W["switch_last_pdelay_resp"], 2)],
                     asc1_bracket=[e for e in E["asCapable"] if str(e["to"]) == "1"][-1], second_pdelay=pd2,
                     gm_bracket=[e for e in E["gm"] if e["to"] == "3cc0c6fffefe0210"][-1], accepted_announce=acc[-1][0] if acc else None,
                     announce_index=len(acc), tu_clear_after_adoption=[round(tu0 - 0.25 - gmsw, 2), round(tu0 - gmsw, 2)] if tu0 else None,
                     crf_tu1=crf1["wire"]["first_after"] if crf1 else None, crf_inside=crf1["wire_inside"] if crf1 else None,
                     tu_bracket=[tub["last_before"], tub["first_after"]] if tub else None,
                     crf_first_after_return=next((x["wire"]["first_after"] for x in c["crf_tu_vs_csr"] if x["wire"]["to"] == 0), None),
                     gm_changed=c["controller_dut_gm_changed"], ctl=c["controller_dut_avb"], tucnt=c["clkv_tucnt"], tu1_span=c["tu1_span_s"],
                     master=W["dut_master_frames"], adp=W["dut_adp"], placed=c["placed_by_phc"], samples=c["samples"], cal=c["calibration_s"],
                     crf_ctrl=a["crf_ctrl"], stream_start=a["cycle_edges"]["dut_crf_stream_start_stop_delta"], tu1_pdus=W["crf_tu1_pdus"],
                     crf_last=a["cycle_edges"]["crf_last_before_on"], media_locked=a["media_locked_at"], carrier=a["carrier"],
                     last_far=a["last_far_frame_before_on"], far_after5=a["far_frames_during_off_after_5s"], peer_idx=a["peer_available_index"],
                     gap=round(a["max_console_gap_s"], 3), epochs=a["reset_epochs"], link=a["cycle_edges"]["link_delta"],
                     gmch=a["cycle_edges"]["gm_changed_delta"], peer_ctr=a["counter_transitions"].get("peer:counter-5-8")))
(P / "summary").mkdir(exist_ok=True)
head = ["| Cycle | CRF binding | Off for | DUT sync 0, `tu` 1 | DUT GM = itself | DUT asCapable 0 | Switch first frame | Switch first Announce | DUT asCapable 1 | DUT GM = switch | DUT all-good | Recovery | 5 s bound |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
(P / "summary/cycles.md").write_text("\n".join(head + rows) + "\n")
(P / "summary/correlation.json").write_text(json.dumps(crow, indent=1) + "\n")
print("\n".join(head + rows))
for r in crow:
    print(json.dumps({k: r[k] for k in ("cycle", "sync_after_last_sync", "sync_after_last_sync_hi", "gm_after_last_ann", "gm_after_last_ann_hi", "asc0_after_last_resp",
                                         "second_pdelay", "accepted_announce", "announce_index", "tu_clear_after_adoption", "crf_tu1", "crf_inside", "tu_bracket",
                                         "crf_first_after_return", "tucnt", "tu1_span", "placed", "samples", "cal", "stream_start", "tu1_pdus", "crf_last",
                                         "media_locked", "carrier", "last_far", "far_after5", "peer_idx", "gap", "epochs", "link", "gmch")}))
    print("   asc1", r["asc1_bracket"], "gm", r["gm_bracket"], "crf_ctrl", r["crf_ctrl"], "ctl", r["ctl"], "gmc", r["gm_changed"], "master", r["master"], "adp", r["adp"][:3])
