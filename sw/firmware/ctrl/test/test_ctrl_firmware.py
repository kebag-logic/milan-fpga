#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Gate: the control-plane firmware of #665 lane F0, built and run on the host.

WHAT IT RUNS. The firmware under sw/firmware/ctrl is portable C11; here it is
compiled for the host exactly as the target compiles it, against the mailbox
model (host/mbx_model.c) behind mbx_hal.h, and graded by these arms:

  model    the mailbox suite (tb/verilator/mbx/suite.hpp, the checks the RTL
           passes through both bus adapters) run on the model, so the model
           the other arms rely on answers to the RTL's expectations;
  port     the lwSRP port layer (static pool, debug sink), the mailbox
           driver and the event loop (test_port_loop.c);
  adp      the ADP core over fake ports, the adapter's tag race and every
           response path's service-latency bound (test_adp.c);
  walk     the PROCESSOR's own ADP stimulus and expectations, cut out of the
           pinned submodule's tb/adp_engine/sim_main.cpp at build time (its
           entity constants, its model_frame builder and its Table 5.51
           transcription ADV), driving the firmware through the model
           (adp_walk.cpp). The pin and the file's blob are proved first;
  entity   for every shipped config, the ENTITY_AVAILABLE the firmware builds
           from adp_entity.py's header, field by field against what the fabric
           is programmed with (boot_policy.fabric_constants), compiled with
           (the builder's ADP shape include) and the processor's
           ADP_ENTITY_CAPS_C;
  rv32     the portable set and the MMIO platform cross-compiled freestanding
           for RV32I with the pinned SDK, every undefined symbol a C-library
           string or format function or a libgcc helper (no heap, no OS);
  lwsrp    with --lwsrp DIR only: lwSRP's own MRP core on the port layer and
           the mailbox (lwsrp_port.c). lwSRP is referenced, never vendored.

--self-test then plants each defect of ctrl_mutants.py into a COPY of the
firmware tree and requires the named check of the named arm to fail.

Usage:
    python3 sw/firmware/ctrl/test/test_ctrl_firmware.py
    python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
    python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --lwsrp <lwSRP checkout>

Exit 0 = every arm passed and every planted defect reddened; 1 = a finding;
2 = refused (the processor pin, a missing compiler, an extraction marker).
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    """Run the arms, then the planted defects when asked."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--require-rv32", action="store_true", help="fail, not skip, when no RV32 compiler is found")
    ap.add_argument("--lwsrp", type=Path, help="a lwSRP checkout: also run the lwSRP port arm")
    ap.add_argument("--self-test", action="store_true", help="also plant every defect and require it caught")
    ap.add_argument("--build-dir", type=Path, help="keep builds here (default: a temporary directory)")
    args = ap.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="ctrl-fw-") as tmp:
        out = args.build_dir.resolve() if args.build_dir else Path(tmp)
        try:
            tree = Tree(CTRL, out / "checkout", out / "reuse")
            cut_reuse(tree.reuse)
            outcomes = [ctrl_arms.arm_model(tree), ctrl_arms.arm_port(tree), ctrl_arms.arm_adp(tree),
                        ctrl_arms.arm_walk(tree),
                        ctrl_arms.arm_entity(tree), ctrl_arms.arm_rv32(tree, args.require_rv32)]
            if args.lwsrp is not None:
                outcomes.append(ctrl_arms.arm_lwsrp(tree, args.lwsrp.resolve()))
        except Refusal as exc:
            print(f"REFUSED: {exc}")
            return 2
        failed = ctrl_arms.report(outcomes)
        if args.self_test and not failed:
            failed = ctrl_mutants.campaign(out / "mutants", tree.reuse)
    print(f"test_ctrl_firmware: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
