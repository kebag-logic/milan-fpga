#!/usr/bin/env python3
"""Reviewer probe: map commands from a durable baseline on the shipping glue.

Usage: r329_probe.py <tree> <outdir> [<shadow.sv> <label>]

Derives tb/verilator/pp_shadow/r329_probe_main.cpp in the DISPOSABLE <tree>
from the reviewed sim_main.cpp (no reviewed file is edited) and runs it on
the dynamic-output fixture (`make run-pending CPP=...`). An optional mutant
shadow replaces hdl/milan/KL_pp_shadow.sv in the source list only.

Probes (all on dynamic STREAM_PORT_INPUT 0, preloaded through the firmware
channel-map CSR window so the mapping exists while status reads durable):
  P1 REMOVE of a present mapping: a real change; pending must rise on the
     accepting edge and status must never read durable afterwards.
  P2 ADD refused at record validation (stream_index 7): nothing changes;
     pending must stay clear.
  P3 ADD of the mapping already present (unchanged duplicate): reported as
     an OBSERVATION of the documented conservative behaviour.
"""

import subprocess
import sys
from pathlib import Path

HOOK = '        pending_boot(7);\n        pending_report("K reset", 0, 0, 0);\n'

PROBE = r'''
    std::vector<uint8_t> r329_cmd(uint16_t opcode, const std::vector<uint8_t>& p,
                                  uint16_t seq, unsigned* status) {
        uint8_t frame[160];
        const size_t at = tx_frames.size();
        const size_t bytes = build_aecp(frame, 0, TEST_EID, opcode, seq, p.data(), p.size());
        inject_rx(frame, bytes, 400);
        run_idle(12000);
        const int k = last_aecp(at);
        std::vector<uint8_t> r = k >= 0 ? tx_frames[k].bytes : std::vector<uint8_t>{};
        *status = r.size() >= 38 ? (r[16] >> 3) & 31u : 255u;
        return r;
    }
    void r329_preload_input0() {
        axi_write(A_CHMAP_CTRL, 0x1);
        axi_write(A_CHMAP_SEL, 0);          // side 0, key 0: input port 0 cluster 0
        axi_write(A_CHMAP_WORD, 0x8000);    // {en, stream 0, channel 0}
        axi_write(A_CHMAP_CTRL, 0x0);
        run_idle(200);
    }
    unsigned r329_input0_mappings() {
        std::vector<uint8_t> get(8, 0);
        put16be(get.data(), 0x000e);
        unsigned st = 0;
        const auto r = r329_cmd(0x002b, get, 0x6000, &st);
        return (st == 0 && r.size() >= 48) ? static_cast<unsigned>(get_be(r, 46, 2)) : 0xffffu;
    }
    void r329_probes() {
        printf("[R329] probes from a durable baseline (reviewer-derived)\n");
        std::vector<uint8_t> map(16, 0);
        put16be(map.data(), 0x000e);
        put16be(map.data() + 4, 1);          // one record: stream 0/ch 0/cluster 0
        unsigned st = 0;

        pending_boot(6);
        r329_preload_input0();
        ck("R329 P1 preload visible to GET_AUDIO_MAP", r329_input0_mappings(), 1);
        ck("R329 P1 baseline durable after preload", axi_read(A_PP_STAT) & 0xb40u, 0x40u);
        r329_cmd(0x002d, map, 0x6011, &st);
        ck("R329 P1 REMOVE status SUCCESS", st, 0);
        ck("R329 P1 REMOVE took effect", r329_input0_mappings(), 0);
        pending_report("R329 P1 remove-from-durable", 0, 1, 1);

        pending_boot(6);
        std::vector<uint8_t> bad = map;
        put16be(bad.data() + 8, 7);          // stream_index 7: refused at validation
        r329_cmd(0x002c, bad, 0x6021, &st);
        printf("  [R329-obs] P2 refused ADD status %u\n", st);
        ck("R329 P2 refused ADD is not SUCCESS", st != 0, 1);
        ck("R329 P2 refused ADD leaves map empty", r329_input0_mappings(), 0);
        pending_report("R329 P2 refused-at-validation", 0, 0, 0);

        pending_boot(6);
        r329_preload_input0();
        ck("R329 P3 preload visible to GET_AUDIO_MAP", r329_input0_mappings(), 1);
        r329_cmd(0x002c, map, 0x6031, &st);
        const uint32_t s = axi_read(A_PP_STAT);
        printf("  [R329-obs] P3 duplicate ADD status %u, phase-5 records %u, marks %u, "
               "mappings after %u, PP_STAT[11] pend %u, durable %u\n", st,
               pending.maps, pending.marks, r329_input0_mappings(), (s >> 11) & 1u,
               (s & 0xb40u) == 0x40u ? 1u : 0u);
        pending.armed = false;
    }
'''


def main() -> None:
    tree = Path(sys.argv[1]).resolve()
    outdir = Path(sys.argv[2]).resolve()
    shadow = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
    label = sys.argv[4] if len(sys.argv) > 4 else "shipping"
    tb = tree / "tb/verilator/pp_shadow"
    src = (tb / "sim_main.cpp").read_text()
    assert src.count(HOOK) == 1, "probe hook anchor changed"
    anchor = "    void grade_pending_live_writes() {\n"
    assert src.count(anchor) == 1
    probe = src.replace(HOOK, "        r329_probes();\n" + HOOK)
    probe = probe.replace(anchor, PROBE + anchor)
    (tb / "r329_probe_main.cpp").write_text(probe)
    outdir.mkdir(parents=True, exist_ok=True)
    bdir = outdir / "build" / label
    bdir.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["make", "run-pending", f"PENDING_BUILD_DIR={bdir}", "CPP=r329_probe_main.cpp"]
    if shadow is not None:
        listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"], cwd=tb,
                                 check=True, capture_output=True, text=True)
        ship = (tree / "hdl/milan/KL_pp_shadow.sv").resolve()
        srcs = [(tb / p).resolve() for p in listing.stdout.split()]
        srcs = [shadow if p == ship else p for p in srcs]
        cmd.append("DP_SRCS=" + " ".join(map(str, srcs)))
    log = outdir / f"probe.{label}.log"
    with log.open("w") as fh:
        rc = subprocess.run(cmd, cwd=tb, stdout=fh, stderr=subprocess.STDOUT).returncode
    text = log.read_text(errors="replace")
    for line in text.splitlines():
        if "R329" in line or line.startswith(("pp_shadow:", "RESULT")):
            print(line)
    print(f"rc={rc}")


if __name__ == "__main__":
    main()
