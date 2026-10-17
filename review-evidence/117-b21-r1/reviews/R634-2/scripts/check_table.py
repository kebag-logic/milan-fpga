"""Compare the findings page's per-cycle restart table with the bound tool's JSON.
usage: check_table.py <findings_md> <rA-bound.json>"""
import json, re, sys
md, js = sys.argv[1:3]
g = json.load(open(js))
txt = open(md).read()
sec = txt.split("### B21 round 3: corrections after review", 1)[1]
rows = re.findall(r"^\| (\d+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| (yes|no) \|$", sec, re.M)
bad = 0
print("cycle lower_md lower_js upper_md upper_js width_md width_calc")
for (c, lo, up, wd, y), r in zip(rows, g["cycles"]):
    lj, uj = r["lower_s"] * 1e3, r["upper_s"] * 1e3
    wc = uj - lj
    ok = int(c) == r["cycle"] and f"{lj:.1f}" == lo and f"{uj:.1f}" == up and abs(float(wd) - wc) < 0.051 and (y == "yes") == (uj < 1000)
    bad += not ok
    print(c, lo, f"{lj:.3f}", up, f"{uj:.3f}", wd, f"{wc:.1f}", r["pass_"], r.get("first_output_frame_packet_after_first_aaf"), r.get("wire_frames_after_last_output_frame"), r["silence_frames"], "" if ok else "MISMATCH")
print("rows", len(rows), "mismatches", bad, "verdict", g["verdict"], "time_base", g["time_base"]["realtime_minus_monotonic_range_s"])
print("upper", g["upper_s"]); print("lower", g["lower_s"])
