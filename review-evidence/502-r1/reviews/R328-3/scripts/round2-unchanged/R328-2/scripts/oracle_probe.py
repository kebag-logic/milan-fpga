#!/usr/bin/env python3
"""Reviewer probe for #502: an oracle independent of the trigger signals.

Usage: oracle_probe.py <repo-root> <scratch-dir> [shipping|<mutant-name> ...]

Generates probe_main.cpp from the head's tb/verilator/pp_shadow/sim_main.cpp by
exact-anchor text patches (refusing if an anchor moved) and builds it in both
harness legs. The probe adds:
  * ORACLE: after every clock edge, snapshot the live state itself -- the
    processor name RAM (u_pp.u_aecp.u_store.name_r) and the datapath map
    stores (amap_in_store_r, amap_out_owner_v_r, amap_out_owner_r,
    amap_out_cluster_r, cmap_flat_w). An edge that changes any of them must
    already show pending (pp_nvm_pend_w) after the same edge.
  * REFUSED RECORD: an ADD_AUDIO_MAPPINGS whose record the integrator refuses
    during validation (stream_index 0x7fff) must answer BAD_ARGUMENTS (7) and
    leave pending clear.
Mutant names are those of reviewer_mutants.py (the copy it wrote under
<scratch>/mut/<name>/hdl/milan/KL_pp_shadow.sv is reused).
"""
import subprocess
import sys
from pathlib import Path

VLT = """`verilator_config
public_flat_rd -module "KL_aecp_desc_store" -var "name_r"
public_flat_rd -module "milan_datapath" -var "amap_in_store_r"
public_flat_rd -module "milan_datapath" -var "amap_out_owner_v_r"
public_flat_rd -module "milan_datapath" -var "amap_out_owner_r"
public_flat_rd -module "milan_datapath" -var "amap_out_cluster_r"
public_flat_rd -module "milan_datapath" -var "cmap_flat_w"
"""

PATCHES = [
    ("        unsigned mark_group = 0;\n    };",
     "        unsigned mark_group = 0;\n"
     "        bool have_snap = false;\n"
     "        std::vector<uint8_t> snap;\n"
     "        unsigned oracle_changes = 0;\n"
     "        unsigned oracle_missing = 0;\n"
     "        long oracle_first = -1;\n"
     "    };\n"
     "    template <class T> static void app(std::vector<uint8_t>& v, const T& x) {\n"
     "        const auto* p = reinterpret_cast<const uint8_t*>(&x);\n"
     "        v.insert(v.end(), p, p + sizeof(T));\n"
     "    }\n"
     "    void oracle_edge() {\n"
     "        const auto* rp = dut->rootp;\n"
     "        std::vector<uint8_t> now;\n"
     "        app(now, rp->milan_datapath__DOT__pp_shadow__DOT__u_pp__DOT__u_aecp__DOT__u_store__DOT__name_r);\n"
     "        app(now, rp->milan_datapath__DOT__amap_in_store_r);\n"
     "        app(now, rp->milan_datapath__DOT__amap_out_owner_v_r);\n"
     "        app(now, rp->milan_datapath__DOT__amap_out_owner_r);\n"
     "        app(now, rp->milan_datapath__DOT__amap_out_cluster_r);\n"
     "        app(now, rp->milan_datapath__DOT__cmap_flat_w);\n"
     "        if (pending.have_snap && now != pending.snap) {\n"
     "            ++pending.oracle_changes;\n"
     "            if (pending.oracle_first < 0) pending.oracle_first = pending.cycle;\n"
     "            pending.oracle_missing += !rp->milan_datapath__DOT__pp_nvm_pend_w;\n"
     "        }\n"
     "        pending.snap = std::move(now);\n"
     "        pending.have_snap = true;\n"
     "    }"),
    ("    void pending_post_edge() {\n"
     "        if (!pending.armed || !pending.unsaved || !dut->axis_resetn) return;",
     "    void pending_post_edge() {\n"
     "        if (pending.armed && dut->axis_resetn) oracle_edge();\n"
     "        if (!pending.armed || !pending.unsaved || !dut->axis_resetn) return;"),
    ("        ck(\"K mark group\", pending.wrong_group, 0);\n",
     "        ck(\"K mark group\", pending.wrong_group, 0);\n"
     "        snprintf(label, sizeof label, \"ORACLE %s live change without pending\", tag);\n"
     "        ck(label, pending.oracle_missing, 0);\n"
     "        printf(\"  [o] %s oracle changes %u, first change %ld, first trigger %ld\\n\",\n"
     "               tag, pending.oracle_changes, pending.oracle_first, pending.first_write);\n"),
    ("            pending_report(\"K12 zero records\", 0, 0, 0);\n",
     "            pending_report(\"K12 zero records\", 0, 0, 0);\n"
     "            {\n"
     "                std::vector<uint8_t> bad(16, 0);\n"
     "                put16be(bad.data(), type);\n"
     "                put16be(bad.data() + 4, 1);\n"
     "                put16be(bad.data() + 8, 0x7fff); // stream_index out of range\n"
     "                pending_command(0x002c, bad, static_cast<uint16_t>(0x5038 + type), 7);\n"
     "                pending_report(\"PROBE refused record\", 0, 0, 0);\n"
     "            }\n"),
]


def main():
    root = Path(sys.argv[1]).resolve()
    scratch = Path(sys.argv[2]).resolve()
    targets = sys.argv[3:] or ["shipping"]
    here = root / "tb/verilator/pp_shadow"
    pdir = scratch / "oracle"
    pdir.mkdir(parents=True, exist_ok=True)
    text = (here / "sim_main.cpp").read_text()
    for old, new in PATCHES:
        if text.count(old) != 1:
            sys.exit(f"REFUSED: anchor count {text.count(old)} for {old[:50]!r}")
        text = text.replace(old, new)
    text = text.replace('#include "../../common/verilator_harness.hpp"',
                        f'#include "{root}/tb/common/verilator_harness.hpp"')
    (pdir / "probe_main.cpp").write_text(text)
    (pdir / "probe.vlt").write_text(VLT)
    cpp = f"{pdir}/probe_main.cpp {pdir}/probe.vlt"
    source = (root / "hdl/milan/KL_pp_shadow.sv").resolve()
    listing = subprocess.run(["make", "-s", "-C", "../milan_dp", "print-srcs"], cwd=here,
                             check=True, capture_output=True, text=True).stdout.split()
    sources = [(here / p).resolve() for p in listing]
    for target in targets:
        extra = []
        if target != "shipping":
            mutant = scratch / "mut" / target / "hdl/milan/KL_pp_shadow.sv"
            assert mutant.exists(), mutant
            extra = ["DP_SRCS=" + " ".join(str(mutant if p == source else p) for p in sources)]
        for leg, cmd in (
            ("static", ["make", "run-base", f"BUILD_DIR={pdir}/{target}_static",
                        "SIM_ARGS=--pending-only", f"CPP={cpp}"]),
            ("dynamic", ["make", "run-pending", f"PENDING_BUILD_DIR={pdir}/{target}_dyn",
                         f"CPP={cpp}"]),
        ):
            log = pdir / f"{target}.{leg}.log"
            with log.open("w") as fh:
                rc = subprocess.run(cmd + extra, cwd=here, stdout=fh,
                                    stderr=subprocess.STDOUT).returncode
            out = log.read_text(errors="replace")
            res = "PASS" if (rc == 0 and "RESULT: PASS" in out) else (
                "FAIL" if "RESULT: FAIL" in out else "BUILD-FAIL")
            print(f"== {target} {leg}: rc={rc} {res}")
            for line in out.splitlines():
                if "[FAIL]" in line or "[o]" in line or "checks," in line or "PROBE" in line:
                    print("   " + line.strip())


if __name__ == "__main__":
    main()
