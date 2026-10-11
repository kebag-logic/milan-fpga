#!/usr/bin/env python3
"""usage: stack_plants_probe.py <checkout> [gate arguments...]
Reviewer-owned stack-side plants, judged by the boundary gate's own control machinery in place of the gate's
plant table: each plant is written into a copy of the firmware's tree and the stack (ctrl_boundary.mirror),
compiled by a real builder function (the arms' C compile, the image builder's RV32 compile, the arms' C++ test
compile), captured, and judged. Nothing in the checkout is written. The gate then runs as usual over the real
builders' capture (with --selftest, the pin controls too)."""
import sys
from pathlib import Path
root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_boundary  # noqa: E402
from ctrl_plants import Plant, arms, image, tests  # noqa: E402

MINE = (
    Plant("R584-7 K1: a stack source includes the mailbox register-map contract (host arms' C compile)",
          "stack", "src/maap.c", '#include "maap.h"\n', '#include "maap.h"\n#include "mbx_contract.h"\n',
          "stack: tsn-c-stack/src/maap.c reads sw/firmware/ctrl/mbx/mbx_contract.h",
          run=arms("tsn-c-stack/src/maap.c")),
    Plant("R584-7 K2: a stack public header includes the platform loop under NDEBUG (a firmware adapter's compile)",
          "stack", "include/adp.h", "#include <stdint.h>\n",
          '#include <stdint.h>\n#ifdef NDEBUG\n#include "ctrl_loop.h"\n#endif\n',
          "stack: tsn-c-stack/include/adp.h includes sw/firmware/ctrl/loop/ctrl_loop.h",
          run=arms("adp/adp_mbx.c")),
    Plant("R584-7 K3: a stack source includes the mailbox HAL (the image builder's RV32 compile)",
          "stack", "src/acmp.c", '#include "wire.h"\n', '#include "wire.h"\n#include "mbx_hal.h"\n',
          "stack: tsn-c-stack/src/acmp.c reads sw/firmware/ctrl/mbx/mbx_hal.h", run=image()),
    Plant("R584-7 K4: a stack test includes the app (the arms' C++ test compile)",
          "stack", "tests/test_adp.cpp", '#include "wire.h"\n', '#include "wire.h"\n#include "ctrl_app.h"\n',
          "stack: tsn-c-stack/tests/test_adp.cpp includes sw/firmware/ctrl/app/ctrl_app.h",
          run=tests('STACK + "/tests/test_adp.cpp"')),
    Plant("R584-7 K5: a stack public header includes the saved-state port (an adapter's compile)",
          "stack", "include/acmp.h", "#include <stdint.h>\n", '#include <stdint.h>\n#include "nvm_state.h"\n',
          "stack: tsn-c-stack/include/acmp.h includes sw/firmware/ctrl_nvm/nvm_state.h",
          run=arms("acmp/acmp_mbx.c")),
    Plant("R584-7 K6: a stack source includes a mailbox header by a relative path (the image builder's RV32 compile)",
          "stack", "src/maap.c", '#include "wire.h"\n',
          '#include "wire.h"\n#if 0\n#endif\n#include "../../../sw/firmware/ctrl/mbx/mbx_wire.h"\n',
          "stack: tsn-c-stack/src/maap.c reads sw/firmware/ctrl/mbx/mbx_wire.h", run=image()),
    Plant("R584-7 K7 pass: a firmware adapter includes the stack's public wire.h by a relative path",
          "ctrl", "adp/adp_mbx.c", '#include "adp_mbx.h"\n',
          '#include "adp_mbx.h"\n#include "../../../../third_party/tsn-c-stack/include/wire.h"\n', "",
          run=arms("adp/adp_mbx.c")),
)
ctrl_boundary.PLANTS = MINE
sys.exit(ctrl_boundary.main(sys.argv[2:]))
