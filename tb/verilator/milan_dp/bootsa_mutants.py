#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the #839 boot leg in milan_dp: prove its checks can fail.

sim_boot_sa.cpp (the obj_bootsa leg) boots the shipping 1x1 datapath through
milan_init()'s own order and grades the source address of every frame at the
MAC boundary. The fix it proves is in milan_datapath: the station-MAC pair's
sequencing (mac_addr_seq) records when both halves have been written, the
four CSR-addressed transmitters are held until then, and octets 6 to 11 of
every control-lane frame are stamped from the CSR. Each mutant below takes a
piece away, or breaks the stamp's position, in a copy of the RTL, and the
SAME leg is rebuilt through the Makefile's own recipe (`make bootsa-build`
with BOOTSA_MDIR and DP_SRC overridden) and run. A mutant is caught only when the leg
FAILS by its own verdict (a `[FAIL]` line or a tally with failures, read by
scripts/suite_tally.py) AND every check the mutant names is among the
failures; a crash, an abort or a build failure is not a catch. The positive
control is the clean leg, run first.

The first mutant is the defect as shipped: no hold and no stamp. It must fail
the leg by the names the issue's acceptance reads, the all-zero source
address and the MSRP frame's source address.

What bounds a run: the leg is cycle-bounded (its own fixed phases and the
AXI4-Lite BFM's 2048-cycle handshake bound), so a mutant ends no later than
the clean leg's bound. This driver sets no host-time deadline.

Usage: make -C tb/verilator/milan_dp bootsa-mutants
       (or python3 bootsa_mutants.py from tb/verilator/milan_dp)
Exit 0 = every mutant was caught and the clean leg passes.
"""

import re
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = {"DP_SRC": HERE / "../../../hdl/milan/milan_datapath.sv"}
EXE = "Vmilan_dp_bootsa"
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

#: the transmit gate: both halves of the pair
PAIR = "  assign tx_sa_ok_w = mac_alo_wr_r & mac_ahi_wr_r;"
#: the control lane's stamp
STAMP = ("        if (ctl_sa_idx_r == TX_SA_IW_C'(b) && (b * int'(TX_SA_BPB_C) + ln) >= 6\n"
         "            && (b * int'(TX_SA_BPB_C) + ln) < 12)\n"
         "          ctlg2_tdata[8*ln +: 8] = cfg_mac_addr[8*(b * int'(TX_SA_BPB_C) + ln - 6) +: 8];")
NO_STAMP = ("        if (1'b0)\n"
            "          ctlg2_tdata[8*ln +: 8] = cfg_mac_addr[8*(b * int'(TX_SA_BPB_C) + ln - 6) +: 8];")
ZERO = "[BOOTSA] no frame carries the all-zero source address"
EARLY = "[BOOTSA] no CSR-addressed transmitter starts a frame before the station MAC is written"
MSRP_SA = "[BOOTSA] every MSRP frame's source address is the station MAC"
MSRP_DA = "[BOOTSA] every MSRP frame's destination address is its protocol's"
ADP_DA = "[BOOTSA] every ADP frame's destination address is its protocol's"
LO_ALONE = "[BOOTSA] pair: MAC_ADDR_LO alone opens no CSR-addressed transmitter"
HI_ALONE = "[BOOTSA] pair: MAC_ADDR_HI alone opens no CSR-addressed transmitter"

#: (name, {file variable: [(fragment, replacement)]}, the checks it must fail)
MUTATIONS = [
    ("the defect as shipped: no hold and no stamp",
     {"DP_SRC": [(PAIR, "  assign tx_sa_ok_w = 1'b1;"), (STAMP, NO_STAMP)]},
     [ZERO, EARLY, MSRP_SA]),
    ("no hold: the stamp alone",
     {"DP_SRC": [(PAIR, "  assign tx_sa_ok_w = 1'b1;")]},
     [ZERO, EARLY, MSRP_SA]),
    ("no stamp: the hold alone releases the MSRP PDU built from the reset address",
     {"DP_SRC": [(STAMP, NO_STAMP)]},
     [ZERO, MSRP_SA]),
    ("MAC_ADDR_LO alone completes the pair",
     {"DP_SRC": [(PAIR, "  assign tx_sa_ok_w = mac_alo_wr_r;")]},
     [LO_ALONE]),
    ("MAC_ADDR_HI alone completes the pair",
     {"DP_SRC": [(PAIR, "  assign tx_sa_ok_w = mac_ahi_wr_r;")]},
     [HI_ALONE]),
    ("the stamp lands on the destination, octets 0 to 5",
     {"DP_SRC": [(STAMP, STAMP.replace(">= 6", ">= 0").replace("< 12", "< 6")
                  .replace("ln - 6)", "ln)"))]},
     [MSRP_DA, MSRP_SA]),
    ("the stamp's beat position survives a frame's last beat",
     {"DP_SRC": [("      if (ctlg2_tlast)                                     ctl_sa_idx_r <= '0;",
                  "      if (ctlg2_tlast)                                     ctl_sa_idx_r <= 1'b1;")]},
     [ADP_DA]),
]


def build(sources: dict[str, Path], mdir: Path) -> Path | None:
    """Build the leg against `sources` through the suite's own recipe; the
    executable, or None when the recipe failed or left none."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "bootsa-build", f"BOOTSA_MDIR={mdir}",
         *(f"{var}={path}" for var, path in sources.items())],
        capture_output=True, text=True, check=False)
    exe = mdir / EXE
    if out.returncode != 0 or not exe.is_file():
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exe


def run_leg(exe: Path) -> tuple[int, str]:
    """(rc, output) of one run of the leg; it is cycle-bounded (docstring)."""
    out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True,
                         text=True, check=False)
    return out.returncode, out.stdout + out.stderr


def verdict(rc: int, out: str, must_fail: list[str]) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        fails = [line.strip() for line in out.splitlines() if line.strip().startswith("[FAIL]")]
        missing = [name for name in must_fail if not any(name in line for line in fails)]
        if missing:
            return f"failed, but not by every named check (missing {missing!r})"
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def run_mutant(mutation: tuple[str, dict[str, list[tuple[str, str]]], list[str]],
               work: Path) -> bool:
    """Plant one mutation, build and run the leg; True when it was caught."""
    name, plants, breaks = mutation
    tag = re.sub(r"[^A-Za-z0-9]+", "_", name)[:48]
    sources = {}
    for var, edits in plants.items():
        text = RTL[var].read_text()
        for pattern, replacement in edits:
            if text.count(pattern) != 1:
                print(f"[FAIL] mutation {name!r}: its pattern appears {text.count(pattern)} "
                      f"time(s) in {RTL[var].name}, expected exactly 1. The RTL moved and "
                      f"this mutant is no longer mutating anything - fix the pattern, do "
                      f"not delete the arm.")
                return False
            text = text.replace(pattern, replacement)
        path = work / f"{tag}_{RTL[var].name}"
        path.write_text(text)
        sources[var] = path
    exe = build(sources, work / f"obj_{tag}")
    if exe is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the leg")
        return False
    rc, out = run_leg(exe)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        print(f"[PASS] mutant caught: {name} - fails " + "; ".join(f'"{b}"' for b in breaks))
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The leg does not prove {breaks!r}.")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="bootsa-mutants-") as td:
        work = Path(td)
        clean = HERE / "obj_bootsa" / EXE
        exe = clean if clean.is_file() else build({}, work / "obj_clean")
        answer = verdict(*run_leg(exe), []) if exe else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated gateware passes the obj_bootsa leg")
        else:
            fails += 1
            print(f"[FAIL] the unmutated gateware does NOT pass obj_bootsa ({answer}) - "
                  f"every mutant result on it is meaningless")
        for mutation in MUTATIONS:
            if run_mutant(mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
