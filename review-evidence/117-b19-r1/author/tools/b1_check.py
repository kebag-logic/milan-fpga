"""Print one per-cycle row from bench/<name>/analysis.json and a recovery verdict.

exit 0 = recovered (DUT gPTP healthy to the end, servo LOCKED, both listeners
MEDIA_LOCKED, both CRF directions flowing to the end, bindings held); 3 = not.
"""
import json, sys
from pathlib import Path
name = sys.argv[1]
a = json.load(open(Path(__file__).resolve().parent.parent / "bench" / name / "analysis.json"))
ce = a["counter_endpoints"]
lk = a["link_counters"]["dut:counter-9-0"]
d51, p58 = ce["dut:counter-5-1"]["last"], ce["peer:counter-5-8"]["last"]
servo_end = a["servo"][-1][1]["state"] if a["servo"] else None
end_rel = max(x[0] for x in a["mac_status"]) if a["mac_status"] else 0
w = a["wire"]
ok = bool(a.get("gptp_steady_from") is not None and servo_end == 4 and d51["0"] == d51["1"] + 1
          and p58["0"] == p58["1"] + 1 and w["dut"].get("post_pdus", 0) > 100 and w["peer"].get("post_pdus", 0) > 100
          and a["bindings"]["all_connected"] and a["reset_epochs"] == [1])
row = dict(cycle=name, off_s=round(a.get("off_hold_s", 0), 2),
           link_down_up=f"+{lk['end_LINK_DOWN'] - lk['LINK_DOWN']} / +{lk['end_LINK_UP'] - lk['LINK_UP']}",
           link_counters=f"{lk['LINK_UP']}/{lk['LINK_DOWN']} -> {lk['end_LINK_UP']}/{lk['end_LINK_DOWN']}",
           mac_down=a.get("mac_link_down"), mac_up=a.get("mac_link_up"), mac_values=a["mac_status_values"],
           carrier=a["carrier"], last_far=a.get("last_far_frame_before_on"), wire_return=a.get("first_wire_return"),
           first_gm=a.get("first_gm"), recovery_s=a.get("gptp_recovery_s"), steady_from=a.get("gptp_steady_from"),
           first_pdu=[w["dut"].get("first_valid_after_on"), w["peer"].get("first_valid_after_on")],
           media_locked_at=a.get("media_locked_at"), servo_locked_at=a.get("servo_locked_at"),
           steps=[s["phc_minus_wall_delta_s"] for s in a["phc_discontinuities"]],
           mr=[w["dut"]["mr"], w["peer"]["mr"]], deltas={k: v["delta"] for k, v in ce.items()},
           console_gap=round(a["max_console_gap_s"], 3), epochs=a["reset_epochs"], bindings=a["bindings"])
print(json.dumps(row))
print("RECOVERED" if ok else "NOT_RECOVERED")
sys.exit(0 if ok else 3)
