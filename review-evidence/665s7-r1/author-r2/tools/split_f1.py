"""split_f1.py LANE FINAL_DIR: write the F-1-only versions (the 20 ms allowance and its 221/219 ms pair) of the
round 2 files into LANE from the final versions in FINAL_DIR, each edit anchored once."""
import sys
from pathlib import Path

lane, final = Path(sys.argv[1]), Path(sys.argv[2])
dp = lane / "tb/verilator/milan_dp"


def edit(text, pairs, name="edit"):
    for old, new in pairs:
        assert text.count(old) == 1, (name, old[:80])
        text = text.replace(old, new)
    return text


# ---- srptx_grade.py
t = (final / "srptx_grade.py").read_text()
t = edit(t, [
("""  [TIME]  each participant's transmit opportunities at egress (IEEE 802.1Q-2018 10.7.4, 10.7.11, Table 10-7,
          Milan v1.2 Table 4.3's values), each bound widened by the approved service allowance T_svc = 20 ms
          (#867 item 3; #665, the owner's ruling of 2026-11-06): no four in 1.5 x JoinTime; each a Join
          timer sends within JoinTime's range (180 to 240 ms) of the one before, on each side (10.7.4.1);
          after a New, or a declaration's first message, the attribute's next message within JoinTime; each
          LeaveAll within LeaveAllTime to 1.5 x LeaveAllTime (10.7.4.3) of the last, or of a received one
          (rLA!, Table 10-5), the transmit opportunity's wait (JoinTime) added, and none missing at the
          run's end.""",
"""  [TIME]  each participant's transmit opportunities at egress (IEEE 802.1Q-2018 10.7.4, Table 10-7, Milan
          v1.2 Table 4.3's values), each bound widened by the approved service allowance T_svc = 20 ms
          (#867 item 3; #665, the owner's ruling of 2026-11-06): no four in 1.5 x JoinTime; after a New, or
          a declaration's first message, the attribute's next message within JoinTime; each LeaveAll within
          LeaveAllTime to 1.5 x LeaveAllTime (10.7.4.3) of the last, or of a received one (rLA!, Table
          10-5), the transmit opportunity's wait (JoinTime) added, and none missing at the run's end."""),
("""#: the JoinTime Milan v1.2 Table 4.3 allows, 180 to 240 ms (docs/reference/FR_NFR.md 3.4.1)
JOIN_RANGE_MS = (180, 240)
""", ""),
("""#: a Join timer's transmit opportunity after the one before it (IEEE 802.1Q-2018 10.7.4.1, 10.7.11): JoinTime's
#: range widened by T_svc on each side, as LeaveAll's is
JOIN_BOUNDS_MS = (JOIN_RANGE_MS[0] - SVC_MS, JOIN_RANGE_MS[1] + SVC_MS)
""", ""),
("""    join_low, join_high = JOIN_BOUNDS_MS
""", ""),
("""        # each a Join timer sent, after the one before it (10.7.4.1: jointimer spaces transmit opportunities)
        for f, gap in join_intervals(cap, frames, causes(cap, proto, frames)):
            if not join_low <= gap / 1000 <= join_high:
                found.append(f"[TIME] {proto}: a Join timer's transmit opportunity at ms {f.ms}, {gap / 1000:.3f} ms "
                             f"after the one before, outside JoinTime's range widened by T_svc ({join_low} to "
                             f"{join_high} ms; IEEE 802.1Q-2018 10.7.4.1, 10.7.11, Table 10-7; Milan v1.2 Table 4.3)")
""", ""),
])
head, rest = t.split("def causes(", 1)
_, rest = rest.split("def measure_time(", 1)
body_old = '''        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        armed = {(t["id"], round(t["us"], 3)): t["cs"] for t in timers if t["event"] == "arm"}
        cause = causes(cap, proto, frames)
        after: dict[str, list[float]] = {"join": [], "periodic": [], "leaveall": []}
        interval: dict[str, list[float]] = {"join": [], "periodic": [], "leaveall": []}
        for f, c in zip(frames, cause):
            if c and not cap.held(c[1]["ms"], f.ms):
                after[c[0]].append(f.us - c[1]["ms"] * 1000.0)
        interval["join"] = [gap - JOIN_MS * 1000 for _, gap in join_intervals(cap, frames, cause)]
        for k in range(1, len(frames)):
            c, p = cause[k], cause[k - 1]
            if c is None or cap.held(frames[k - 1].ms, frames[k].ms):
                continue
            if c[0] == "periodic" and p and p[0] == "periodic":
                interval["periodic"].append(frames[k].us - frames[k - 1].us - PERIODIC_MS * 1000)'''
body_new = '''        frames = [f for f in cap.mrpdus if f.proto == proto and not f.error and not cap.queued(f)]
        expiries = [t for t in timers if t["proto"] == proto and t["event"] == "expire"
                    and t["kind"] in ("join", "periodic", "leaveall")]
        armed = {(t["id"], round(t["us"], 3)): t["cs"] for t in timers if t["event"] == "arm"}
        cause: list[tuple[str, dict] | None] = []
        for f in frames:
            kinds = ("leaveall",) if f.leave_all_types() else ("join", "periodic")
            before = [t for t in expiries if t["kind"] in kinds and t["us"] <= f.us
                      and f.us - t["us"] < ATTRIBUTE_MS * 1000]
            cause.append(("leaveall" if f.leave_all_types() else max(before, key=lambda t: t["us"])["kind"],
                          max(before, key=lambda t: t["us"])) if before else None)
        after: dict[str, list[float]] = {"join": [], "periodic": [], "leaveall": []}
        interval: dict[str, list[float]] = {"join": [], "periodic": [], "leaveall": []}
        for f, c in zip(frames, cause):
            if c and not cap.held(c[1]["ms"], f.ms):
                after[c[0]].append(f.us - c[1]["ms"] * 1000.0)
        for k in range(1, len(frames)):
            c, p = cause[k], cause[k - 1]
            if c is None or cap.held(frames[k - 1].ms, frames[k].ms):
                continue
            gap = frames[k].us - frames[k - 1].us
            if c[0] == "join":
                interval["join"].append(gap - JOIN_MS * 1000)
            elif c[0] == "periodic" and p and p[0] == "periodic":
                interval["periodic"].append(gap - PERIODIC_MS * 1000)'''
rest = edit(rest, [(body_old, body_new)], "measure_time")
(dp / "srptx_grade.py").write_text(head + "def measure_time(" + rest)

# ---- srptx_plants.py
t = (final / "srptx_plants.py").read_text()
start = t.index('    "join-early-past-t-svc": (')
end = t.index('    "rate": (')
t = t[:start] + t[end:]
t = edit(t, [
("""JOIN_BOUNDS_MS = (g.JOIN_RANGE_MS[0] - ITEM3_SVC_MS, g.JOIN_RANGE_MS[1] + ITEM3_SVC_MS)
""", ""),
("""JOIN_WORDS = f"ms after the one before, outside JoinTime's range widened by T_svc ({JOIN_BOUNDS_MS[0]} to " \\
             f"{JOIN_BOUNDS_MS[1]} ms"
""", ""),
("""    "join-early-within-t-svc": ("wire", f"join-early-past-t-svc's move, the second frame {JOIN_BOUNDS_MS[0] + 1} ms "
                                "after the first"),
    "join-interval-late-within": ("wire", f"join-interval-late's move, the second frame {JOIN_BOUNDS_MS[1] - 1} ms "
                                  "after the one before"),
""", ""),
("""    "join-early-past-t-svc": ("first", 2, JOIN_BOUNDS_MS[0] - 1, True),
    "join-early-within-t-svc": ("first", 2, JOIN_BOUNDS_MS[0] + 1, True),
    "join-interval-late": ("leave-all", 2, JOIN_BOUNDS_MS[1] + 1, True),
    "join-interval-late-within": ("leave-all", 2, JOIN_BOUNDS_MS[1] - 1, True),
""", ""),
])
(dp / "srptx_plants.py").write_text(t)

# ---- srptx_mutants.py
t = (final / "srptx_mutants.py").read_text()
t = edit(t, [
("""JOIN_ARM = "    shlan_timer_arm(&ps->join_timer, ps->join_cs);"
#: the grade's words for a Join timer's transmit opportunity outside JoinTime's range widened by T_svc
JOIN_SPACING = f"ms after the one before, outside JoinTime's range widened by T_svc ({g.JOIN_BOUNDS_MS[0]} to " \\
               f"{g.JOIN_BOUNDS_MS[1]} ms"
""", ""),
("""     JOIN_ARM, "    shlan_timer_arm(&ps->join_timer, ps->join_cs + 3u);",""",
 """     "    shlan_timer_arm(&ps->join_timer, ps->join_cs);", "    shlan_timer_arm(&ps->join_timer, ps->join_cs + 3u);","""),
("""    ("a Join timer of 10 centiseconds", MRP,
     JOIN_ARM, "    shlan_timer_arm(&ps->join_timer, ps->join_cs - 10u);",
     "wire", 3000, JOIN_SPACING),
    ("a Join timer of 15 centiseconds", MRP,
     JOIN_ARM, "    shlan_timer_arm(&ps->join_timer, ps->join_cs - 5u);",
     "wire", 3000, JOIN_SPACING),
""", ""),
])
(dp / "srptx_mutants.py").write_text(t)

# ---- tb/verilator/milan_dp/README.md
t = (final / "README.md").read_text()
t = edit(t, [
("""No four transmit opportunities in 1.5 x JoinTime (280 ms); each transmit opportunity a Join timer sent within JoinTime's range, 180 to 240 ms, of the one before, on each side (160 to 260 ms); after a New""",
 """No four transmit opportunities in 1.5 x JoinTime (280 ms); after a New"""),
("""| IEEE 802.1Q-2018 10.7.4.1, 10.7.4.3, 10.7.11, Tables 10-3, 10-5 and 10-7; Milan v1.2 Table 4.3; #867 item 3;""",
 """| IEEE 802.1Q-2018 10.7.4.1, 10.7.4.3, Tables 10-3, 10-5 and 10-7; Milan v1.2 Table 4.3; #867 item 3;"""),
("""20 ms T_svc. In every scenario, each transmit opportunity a Join timer sent
left 198.989 to 200.015 ms after the one before, inside 160 to 260 ms.

The Join bound is JoinTime's range, not the 200 ms the adapter configures,
widened on each side. A frame delayed within T_svc shortens the interval after
it: one 219 ms after the frame before leaves the next 179.99 ms later. A bound
of 200 ms less T_svc, 180 ms, would refuse that frame, which item 3 allows.""",
 """20 ms T_svc."""),
("""| `join-early-past-t-svc` (a short Join timer: the second and third MSRP frames, their records and timers earlier, the second 159 ms after the first) | wire | `a Join timer's transmit opportunity at ms 160, 159.000 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` |
| `join-interval-late` (a long Join timer after the first MSRP LeaveAll, the second Join frame 261 ms after the one before, where no New is followed) | wire | `a Join timer's transmit opportunity at ms 15021, 261.000 ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` |
""", ""),
("""| `join-early-within-t-svc` | wire | `join-early-past-t-svc`'s frames, the second 161 ms after the first |
| `join-interval-late-within` | wire | `join-interval-late`'s frames, the second 259 ms after the one before |
""", ""),
("""| a Join timer of 10 centiseconds | lwSRP `mrp_transmit` | wire, 3 s | `ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` |
| a Join timer of 15 centiseconds | lwSRP `mrp_transmit` | wire, 3 s | `ms after the one before, outside JoinTime's range widened by T_svc (160 to 260 ms` |
""", ""),
("""twenty-five plants, three controls and twelve code mutants""", """twenty-three plants, a control and ten code mutants"""),
])
(dp / "README.md").write_text(t)

# ---- sw/firmware/ctrl/srp/README.md
t = (final / "srp-README.md").read_text()
t = edit(t, [("within T_svc (20 ms) on each side, and a full ring", "within T_svc (20 ms), and a full ring")], "srp")
(lane / "sw/firmware/ctrl/srp/README.md").write_text(t)
print("F-1 versions written")
