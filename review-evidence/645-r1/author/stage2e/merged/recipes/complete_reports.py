import json, os
from pathlib import Path
out=Path(os.environ["OUT"])
e=out/"stage2e/merged"
s=json.loads((e/"measurement-summary.json").read_text())
assert all(v==0 for v in s["required_rc"].values())
head=s["head"]
own=s["area"]["ownership"]
lut=own["final_own_LUT_upper_bound"];ff=own["own_FF_delta"]
assert lut<=120 and ff<=120
rows=["| Directive | Slow WNS / WHS (ns) | Fast WNS / WHS (ns) | Margin grade |", "|---|---:|---:|---|"]
for name,v in s["timing"].items():
    corners={r["corner"]:r for r in v["rows"] if r["power_temperature_C"]==0}
    cells=[f"{corners[c]['WNS_ns']:+.3f} / {corners[c]['WHS_ns']:+.3f}" for c in ["Slow","Fast"]]
    grade="PASS (0)" if v["passes_margin"] else "FAIL (1); stage-2e disposition"
    rows.append(f"| {name} | {cells[0]} | {cells[1]} | {grade} |")
table="\n".join(rows)
ooc=s["ooc"]
ooc_delta={k:sum(ooc[h]["resources"][k]-ooc[b]["resources"][k] for b,h in [("settle_base","settle_head"),("cmc_base","cmc_head")]) for k in ["Slice LUTs","Slice Registers"]}
area_rows=["| Measured scope | Base LUT / FF | Head LUT / FF | Delta LUT / FF |", "|---|---:|---:|---:|"]
for title,b,h in [("Recentre blocks","settle_base","settle_head"),("Complete capture module","cmc_base","cmc_head")]:
    a=ooc[b]["resources"];z=ooc[h]["resources"]
    vals=[int(a["Slice LUTs"]),int(a["Slice Registers"]),int(z["Slice LUTs"]),int(z["Slice Registers"])]
    area_rows.append(f"| {title} | {vals[0]} / {vals[1]} | {vals[2]} / {vals[3]} | {vals[2]-vals[0]:+d} / {vals[3]-vals[1]:+d} |")
area="\n".join(area_rows)+f"\n\nThe conservative routed own-logic bound is **{lut} LUT / {ff} FF**, within the\n120/120 limit. The bound counts the complete new settle cone and capture-module\ndelta, then excludes only identical functions with recorded proof. The shared\nband proof covers all 65,536 signed-error assignments and catches its planted\ncontrol. Whole-design resource movement includes the processor adoption and\nis not charged to this lane. Fresh OOC, routed cell lists, proof and return\ncodes are retained in `stage2e/merged/area-ooc/` and `area-route/`.\n"
for name in ["HANDOFF.md","PR-BODY.md"]:
    p=out/name;t=p.read_text();assert head in t
    start=t.index("Fresh current-head table:")
    end=t.index("The base's failing path",start)
    t=t[:start]+"Fresh current-head table:\n\n"+table+"\n\nAll three fresh implementation processes and constraint checks return 0, with\nthe full critical-warning census retained. Detailed worst-five extracts and timing grades are\nretained for every directive.\n\n"+t[end:]
    t=t.replace("The physical area measurements remain pending.", "Fresh OOC and routed attribution pass the own-area limit; every measurement\nprocess and source-input verification returns 0.")
    if name=="HANDOFF.md":
        t=t.replace("Status: **IN PROGRESS -- refreshing acceptance after the required dev merge**.","Status: **REVIEW READY under the stage-2e ruling**.")
        a="That satisfies the ruling's timing condition for REVIEW READY. Current-head\nfunctional acceptance, the timing comparison and vendor parser are complete.\nArea measurements remain pending; no readiness verdict is claimed before those\nresults are inspected."
        b="That satisfies the ruling's timing condition for REVIEW READY. Current-head\nfunctional, parser and own-area acceptance is complete, and all fresh timing\nreports have been inspected. Failed margin grades remain failed; no threshold\nwas weakened."
        assert a in t;t=t.replace(a,b)
        a="The current long runner is `merged/run_measurements.py`; its progress is in\n`measurement-driver.log`, per-step logs and `.rc` files. It is presently\nrunning the remaining parser and area sequence under the shared lock;\ncompletion is not inferred from launch."
        b="The completed measurement runner is `merged/run_measurements.py`; its exact\nsequence is recorded in `measurement-driver.log`, per-step logs and `.rc` files.\nThe aggregate measurement and functional return codes are both zero."
        assert a in t;t=t.replace(a,b)
        t=t.replace("Historical OOC +80 LUT / +73 FF; prior routed bound 113 LUT / 73 FF; fresh current measurement pending",f"Fresh OOC {int(ooc_delta['Slice LUTs']):+d} LUT / {int(ooc_delta['Slice Registers']):+d} FF; routed bound {lut} LUT / {ff} FF")
        start=t.index("Fresh three-directive implementation is complete;")
        end=t.index("## Current functional acceptance",start)
        t=t[:start]+area+"\nAll heavy builds completed before vendor implementation. Only existing-binary\nboundary simulations overlapped it after their binaries and the remaining\nrun-only driver path were verified. The completed boundary verdict is zero.\nSee `render-boundary-builds.json`.\n\n"+t[end:]
        t=t.replace("timing disposition, without converting a failed grade into a pass. Finish and\ninspect current-head evidence before the public REVIEW READY or STOP comment.","timing disposition, without converting a failed grade into a pass. The refreshed\ncurrent-head acceptance is complete; hand the committed lane to independent\nreview with the prepared PR body.")
    else:
        t=t.replace("IN PROGRESS -- merged-head acceptance is running; `645-ring-slip` -> `dev`.","REVIEW READY under the stage-2e ruling; `645-ring-slip` -> `dev`.")
        t=t.replace("condition, after the remaining current-head evidence is completed and inspected.","condition. Current-head functional, parser and own-area acceptance is complete,\nand all fresh timing reports have been inspected.")
        t=t.replace("stage-2e ruling, not changed into a timing pass. Current-head functional\nacceptance and timing collection are complete; vendor parser and area\nmeasurements remain pending.","stage-2e ruling, not changed into a timing pass. Current-head functional, parser\nand own-area acceptance is complete.\n\n"+area)
    p.write_text(t)
print("Updated both reports from completed measurements at",head)
