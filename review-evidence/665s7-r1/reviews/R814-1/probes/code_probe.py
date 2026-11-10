#!/usr/bin/env python3
"""code_probe.py - reviewer code mutants for the split build's SRP transmit check (#867), with section ablation.

  python3 -I code_probe.py TREE WORK JOBS ARM [ARM ...]      (ARM: a key of PROBES, or "author:<n>")

TREE is a checkout of the reviewed head whose milan_dp dependencies are already built (`make srptx` ran there).
WORK is a scratch directory; each arm builds there through srptx_mutants.build() (the author's own recipe:
twin_fw.py --replace for a firmware unit, DP_SRC for the datapath) and runs its scenario with
srptx_mutants.run(), which keeps the capture. The capture is then graded section by section (the grader's own
functions), so for each arm the probe prints which sections refuse it. "author:<n>" is the n-th arm of
srptx_mutants.ARMS (0-based), re-run here to see whether any section other than the one owning its words also
refuses it; the other keys are the reviewer's own arms, each with the reviewer's prediction.

No control here: the control is `make srptx` and `make srptx-mutants` on the same tree recipe.
"""
import concurrent.futures
import sys
from pathlib import Path

TREE, WORK, JOBS = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), int(sys.argv[3])
sys.path.insert(0, str(TREE / "tb/verilator/milan_dp"))
import srptx_grade as g  # noqa: E402
import srptx_mutants as sm  # noqa: E402

MRP, ADAPTER = sm.MRP, sm.ADAPTER
CONF = ("    (void)mrp_port_configure(i->msrp,0,20,500,1000,(uint32_t)i->mac,true);\n"
        "    (void)mrp_port_configure(i->mvrp,0,20,500,1000,(uint32_t)i->mac ^ 0x91u,true);")
PROBES = {
    # item 3, the Join spacing's lower side: JoinTime configured short of Milan v1.2 Table 4.3's 180 ms
    "join-10cs": (ADAPTER, CONF, CONF.replace(",20,500", ",10,500"), "wire", 40000,
                  "JoinTime 100 ms, outside Table 10-7 / Milan Table 4.3 (180-240 ms): a spacing check must refuse"),
    "join-15cs": (ADAPTER, CONF, CONF.replace(",20,500", ",15,500"), "wire", 40000,
                  "JoinTime 150 ms, outside Milan Table 4.3 (180-240 ms): a spacing check must refuse"),
    "join-17cs": (ADAPTER, CONF, CONF.replace(",20,500", ",17,500"), "wire", 40000,
                  "JoinTime 170 ms, outside Milan Table 4.3 (180-240 ms): a spacing check must refuse"),
    "join-30cs": (ADAPTER, CONF, CONF.replace(",20,500", ",30,500"), "wire", 40000,
                  "JoinTime 300 ms: expect [TIME] past JoinTime + the MRP service bound"),
    # item 3, LeaveAll's lower side
    "leaveall-5s": (MRP, "    return ps->leaveall_cs + 1u + ps->random % (ps->leaveall_cs / 2u - 1u);",
                    "    return ps->leaveall_cs / 2u;", "wire", 40000,
                    "LeaveAll drawn at 5 s: expect [TIME] outside 9782 to 15218 ms"),
    # item 3, the rate rule: Join timer ignored, a transmit at every poll
    "no-join-wait": (MRP, "    if (!ps->prepared_pdu && (!ps->tx_pending || ps->join_wait)) {",
                     "    if (!ps->prepared_pdu && (!ps->tx_pending)) {", "wire", 20000,
                     "transmit opportunities not paced by the Join timer: expect [TIME] four in"),
    # item 1, the PDU EndMark omitted
    "no-pdu-endmark": (MRP, "    pdu[off++] = 0; pdu[off++] = 0; /* MRPDU EndMark */",
                       "    /* MRPDU EndMark omitted */", "wire", 3000,
                       "no MRPDU EndMark: expect [WIRE] missing PDU EndMark"),
    # item 1, MVRP sent to the other application's group address
    "msrp-group-on-all": (ADAPTER, "        memcpy(m->owed_frame,s->app->ops->group_addr,6);",
                          "        memcpy(m->owed_frame,\"\\x01\\x80\\xc2\\x00\\x00\\x0e\",6);", "wire", 3000,
                          "MVRP sent to the MSRP group: expect [WIRE] not the MVRP group address"),
    # item 5, a withdrawal in LV that ends the registration at once
    "lv-fast-leave": (MRP, "        _RX,                                /* LV: -x-                  */",
                      "        _RE(REG_IND_LV, REG_TIMER_NONE, MRP_REG_STATE_MT),", "licence", 0,
                      "rLv! in LV goes straight to MT: expect [608] the talker stopped at ms ~18000"),
}


def sections(cap):
    """Findings per grader section, from the grader's own functions."""
    out = {"BENCH": [], "WIRE": g.grade_wire(cap), "SA": g.grade_source(cap)[0], "TX": g.grade_tx(cap)[0],
           "TIME": g.grade_time(cap), "608/LIC": g.grade_licence(cap)[0]}
    if cap.doc["layout_error"]:
        out["BENCH"].append(f"[BENCH] {cap.doc['layout_error']}")
    if cap.doc["intra_ms_max_us"] >= g.MS_US:
        out["BENCH"].append("[BENCH] intra-ms overrun")
    return out


def arm_spec(key):
    if key.startswith("author:"):
        name, src, old, new, scen, ms, words = sm.ARMS[int(key.split(":")[1])]
        return name, src, old, new, scen, ms, f"author arm, refused by {words!r}", words
    src, old, new, scen, ms, expect = PROBES[key]
    return key, src, old, new, scen, ms, expect, None


def one(key):
    name, src, old, new, scen, ms, expect, words = arm_spec(key)
    lines = [f"PROBE {name} [{key}] ({scen}{f' {ms} ms' if ms else ''}); expectation: {expect}"]
    text = src.read_text()
    if text.count(old) != 1:
        return lines + [f"  RESULT {name}: anchor not found once in {src.name}"]
    arm = WORK / key.replace(":", "_")
    arm.mkdir(parents=True, exist_ok=True)
    copy = arm / src.name
    copy.write_text(text.replace(old, new))
    ok, out = sm.build(arm, src, copy)
    if not ok:
        return lines + [f"  RESULT {name}: BUILD FAILED\n{out}"]
    run_rc, found, out = sm.run(arm, scen, ms)
    tail = [line for line in out.splitlines() if line.startswith("srptx ")]
    lines.append(f"  binary rc {run_rc}; {tail[0] if tail else 'no summary'}; findings: {len(found)}")
    capture = arm / f"{scen}-{ms}.json"
    if capture.exists():
        sec = sections(g.load(capture))
        hit = {k: len(v) for k, v in sec.items() if v}
        lines.append(f"  sections refusing: {hit or 'NONE'}")
        for k, v in sec.items():
            for f in v[:2]:
                lines.append(f"    {k}: {f[:300]}")
        if words is not None:
            owner = [k for k, v in sec.items() if any(words in f for f in v)]
            others = {k: n for k, n in hit.items() if k not in owner}
            lines.append(f"  owner section(s) {owner}; other sections refusing {others or '{}'}; "
                         f"escapes without its owner: {'yes' if not others else 'NO'}")
    lines.append(f"  RESULT {name}: {'REFUSED' if found else 'ESCAPED (no finding)'}")
    return lines


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    keys = sys.argv[4:]
    with concurrent.futures.ThreadPoolExecutor(max_workers=JOBS) as pool:
        for lines in pool.map(one, keys):
            print("\n".join(lines), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
