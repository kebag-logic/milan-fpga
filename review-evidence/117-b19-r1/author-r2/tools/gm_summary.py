"""Lane B19: grade the ten software-grandmaster edges (#621 item 3, #387 item 4); no bench access.

usage: gm_summary.py gm01 ... gm05   reads bench/<run>/analysis.json, writes summary/gm-steps.json and .md
Each run is split at 27 s after the software-GM start: the takeover edge lies before, the release after.
Per edge, the assignment's grades:
  one `tu` event   one rise of `tu` in the console samples and one `tu=1` episode on the DUT's CRF PDUs
  no asCapable loss  no console sample and no controller poll with asCapable 0
  one GM_CHANGED   the DUT's AVB_INTERFACE GPTP_GM_CHANGED rises by exactly 1
  no `mr` change   the DUT's CRF PDUs keep one `mr` value
  MEDIA_RESET flat the DUT's two talkers and the peer's CRF listener count no MEDIA_RESET
  no listener unlock MEDIA_UNLOCKED does not move on the DUT's listener or either peer listener
"""
from pathlib import Path
import json, sys

P = Path(__file__).resolve().parent.parent
SPLIT = 27.0
rows, runs = [], {}


def at(tr, t):
    """value of a counter-transition series at time t (last change at or before t)."""
    v = None
    for tt, x in tr:
        if tt <= t:
            v = x
    return v


for name in sys.argv[1:]:
    a = json.load(open(P / "bench" / name / "analysis.json"))
    ct = a["counter_transitions"]
    end = max(x[0] for x in a["health"]) + 60
    for i, (lo, hi) in enumerate([(-9.0, SPLIT), (SPLIT, 200.0)]):
        edge = "takeover" if i == 0 else "release"
        win = lambda t: lo <= t < hi
        h = [x for x in a["health"] if win(x[0])]
        hb = at(a["health"], lo)
        seq = ([hb] if hb else []) + [x[1] for x in h]
        tu_rises = sum(1 for p, q in zip(seq, seq[1:]) if p.endswith("tu0") and q.endswith("tu1"))
        asc0 = sum(1 for x in a["health"] if win(x[0]) and "asc0" in x[1])
        tuw = [x for x in a["wire"]["dut"]["tu"] if win(x[0])]
        wb = at(a["wire"]["dut"]["tu"], lo)
        wseq = ([wb] if wb is not None else []) + [x[1] for x in tuw]
        wire_tu_eps = sum(1 for p, q in zip(wseq, wseq[1:]) if p == 0 and q == 1)
        mrw = [x for x in a["wire"]["dut"]["mr"] if win(x[0])]
        mb = at(a["wire"]["dut"]["mr"], lo)
        mr_changes = sum(1 for p, q in zip(([mb] if mb is not None else []) + [x[1] for x in mrw], [x[1] for x in mrw]) if p != q) if mrw else 0

        def d(key, idx):
            tr = ct.get(key)
            if not tr:
                return None
            b, e = at(tr, lo - .001) or tr[0][1], at(tr, hi - .001)
            return (e or {}).get(idx, 0) - (b or {}).get(idx, 0)

        step = [s for s in a["phc_discontinuities"] if win(s["bracket"][1])]
        wj = [j for j in a.get("dut_phc_wire_jumps", []) if win(j["between"][1])]
        fj = [j for j in a.get("far_time_jumps", []) if win(j["between"][1])]
        ps = next((p for p in a.get("per_step", []) if win(p["step"]["bracket"][1])), None)
        ann = [x for x in a["announce_gm"] if win(x[0])]
        r = dict(run=name, edge=edge,
                 announce=[ann[0][0], ann[0][1][0], ann[0][1][1], ann[0][1][2]] if ann else None,
                 dut_phc_step_ms=[round(j["delta_s"] * 1e3, 3) for j in wj], gm_time_step_ms=[round(j["delta_s"] * 1e3, 3) for j in fj],
                 console_step=[s["bracket"] for s in step],
                 tu_rises_console=tu_rises, tu_episodes_wire=wire_tu_eps,
                 tu_set=ps["tu_first_set"] if ps else None, tu_steady_clear=ps["tu_steady_clear"] if ps else None,
                 wire_tu1=ps["crf"]["dut"]["tu1"] if ps else None, wire_tu1_span=ps["crf"]["dut"]["tu1_span"] if ps else None,
                 ascapable0_samples=asc0,
                 gm_changed=d("dut:counter-9-0", "5"), peer_gm_changed=d("peer:counter-9-0", "5"),
                 mr_changes=mr_changes, mr_values=sorted({x[1] for x in a["wire"]["dut"]["mr"]}),
                 media_reset=dict(dut_aaf_talker=d("dut:counter-6-0", "2"), dut_crf_talker=d("dut:counter-6-1", "2"),
                                  peer_crf_listener=d("peer:counter-5-8", "4"), dut_listener=d("dut:counter-5-0", "4"),
                                  peer_aaf_talker=d("peer:counter-6-0", "2")),
                 media_unlocked=dict(dut_listener=d("dut:counter-5-0", "1"), peer_crf_listener=d("peer:counter-5-8", "1"),
                                     peer_aaf_listener=d("peer:counter-5-0", "1")),
                 talker_tu_counters=dict(dut_aaf=d("dut:counter-6-0", "3"), dut_crf=d("dut:counter-6-1", "3")),
                 clock_domain=[d("dut:counter-36-0", "0"), d("dut:counter-36-0", "1")],
                 dut_listener_other=dict(tu=d("dut:counter-5-0", "5"), late=d("dut:counter-5-0", "9"), early=d("dut:counter-5-0", "10")),
                 crf_max_gap_s=ps["crf"]["dut"]["max_gap_s"] if ps else None)
        r["grade"] = dict(one_tu=tu_rises == 1 and wire_tu_eps == 1, no_ascapable_loss=asc0 == 0, one_gm_changed=r["gm_changed"] == 1,
                          no_mr_change=mr_changes == 0 and len(r["mr_values"]) == 1,
                          media_reset_flat=r["media_reset"]["dut_aaf_talker"] == 0 and r["media_reset"]["dut_crf_talker"] == 0
                          and r["media_reset"]["peer_crf_listener"] == 0,
                          no_listener_unlock=all(v == 0 for v in r["media_unlocked"].values()))
        r["pass"] = all(r["grade"].values())
        rows.append(r)
    runs[name] = dict(clkv_tucnt=a["clkv_tucnt_first_last"], gm=a["gm"], health=a["health"], crf_ctrl=a["crf_ctrl"], servo=a["servo"],
                      crf_pdus=a["wire"]["dut"]["pdus"], crf_max_gap_s=a["wire"]["dut"]["max_gap_s"], reset_epochs=a["reset_epochs"],
                      max_console_gap_s=round(a["max_console_gap_s"], 3), host_gm_first_announce=a.get("host_gm_first_announce"),
                      host_gm_last_announce=a.get("host_gm_last_announce"), switch_back=a.get("switch_gm_first_announce_after"),
                      gm_changed=a["link_counters"]["dut:counter-9-0"]["GM_CHANGED"])
(P / "summary").mkdir(exist_ok=True)
(P / "summary" / "gm-steps.json").write_text(json.dumps(dict(edges=rows, runs=runs), indent=1) + "\n")
md = ["| Run | Edge | DUT PHC step | GM time step | `tu` rises (console / CRF) | `tu` set / steady clear | asCapable 0 samples | GM_CHANGED | `mr` changes | MEDIA_RESET DUT AAF / CRF talker, peer CRF listener | MEDIA_UNLOCKED DUT / peer CRF / peer AAF | Grade |",
      "|---|---|---|---|---|---|---:|---:|---:|---|---|---|"]
for r in rows:
    m, u = r["media_reset"], r["media_unlocked"]
    md.append(f"| {r['run'][-1]} | {r['edge']} | {'/'.join(f'{x:+.3f} ms' for x in r['dut_phc_step_ms'])} | {'/'.join(f'{x:+.3f} ms' for x in r['gm_time_step_ms'])} | "
              f"{r['tu_rises_console']} / {r['tu_episodes_wire']} | {r['tu_set']} / {r['tu_steady_clear']} | {r['ascapable0_samples']} | +{r['gm_changed']} | {r['mr_changes']} | "
              f"+{m['dut_aaf_talker']} / +{m['dut_crf_talker']}, +{m['peer_crf_listener']} | +{u['dut_listener']} / +{u['peer_crf_listener']} / +{u['peer_aaf_listener']} | {'PASS' if r['pass'] else 'FAIL'} |")
(P / "summary" / "gm-steps.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
print(f"edges {len(rows)}, PASS {sum(r['pass'] for r in rows)}")
