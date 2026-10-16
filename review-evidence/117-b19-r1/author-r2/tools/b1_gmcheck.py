"""Print the per-step rows of one software-GM run and a restore verdict.

exit 0 = the switch is grandmaster again, the DUT is healthy to the end, both
listeners never unlocked, the servo is LOCKED, both CRF directions flow to the
end and the bindings held; 3 = not.
"""
import json, sys
from pathlib import Path
name = sys.argv[1]
a = json.load(open(Path(__file__).resolve().parent.parent / "bench" / name / "analysis.json"))
ce = a["counter_endpoints"]
d = {k: v["delta"] for k, v in ce.items()}
ok = bool(a["gm"] and a["gm"][-1][1] == "3cc0c6fffefe0210" and a["health"][-1][1] == "sync1 asc1 tu0"
          and a["servo"][-1][1]["state"] == 4 and d["dut:counter-5-1"]["1"] == 0 and d["peer:counter-5-8"]["1"] == 0
          and a["bindings"]["all_connected"] and a["reset_epochs"] == [1]
          and a["wire"]["dut"]["last"] > 100 and a["wire"]["peer"]["last"] > 100)
rows = []
for i, p in enumerate(a.get("per_step", [])):
    st = p["step"]
    t_step = st["bracket"][1]
    rows.append(dict(run=name, edge="takeover" if i == 0 else "release", console_bracket=st["bracket"],
                     console_step_s=st["phc_minus_wall_delta_s"],
                     wire_step_s=[j["delta_s"] for j in a.get("dut_phc_wire_jumps", [])][i:i + 1],
                     far_jump_s=[j["delta_s"] for j in a.get("far_time_jumps", [])][i:i + 1],
                     tu_first=p["tu_first_set"], tu_steady_clear=p["tu_steady_clear"],
                     step_to_steady_s=round(p["tu_steady_clear"] - st["bracket"][0], 3) if p["tu_steady_clear"] else None,
                     dut_wire_tu1=p["crf"]["dut"]["tu1"], dut_wire_tu1_span=p["crf"]["dut"]["tu1_span"],
                     dut_mr=p["crf"]["dut"]["mr"], peer_mr=p["crf"]["peer"]["mr"],
                     dut_gap=p["crf"]["dut"]["max_gap_s"], peer_gap=p["crf"]["peer"]["max_gap_s"]))
for r in rows:
    print(json.dumps(r))
print(json.dumps(dict(run=name, announce=a["announce_gm"], gm=a["gm"], wire_mr=[a["wire"]["dut"]["mr"], a["wire"]["peer"]["mr"]],
                      servo_states=sorted({s[1]["state"] for s in a["servo"]}),
                      discards=[a["servo"][0][1]["discards"], a["servo"][-1][1]["discards"]],
                      tucnt=a["clkv_tucnt_first_last"], deltas=d, health=a["health"])))
print("RESTORED" if ok else "NOT_RESTORED")
sys.exit(0 if ok else 3)
