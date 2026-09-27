"""Reviewer probe: how the AX7101 PLL speed grade derivation (milan_soc.py:215)
treats declared parts with other suffixes. Run from sw/litex with the LiteX
interpreter; writes nothing."""
from unittest.mock import patch
import milan_soc
from platforms.ax7101_timing import TIMING_GRADE

for part in ("xc7a100t-fgg484-2", "xc7a100t-fgg484-1", "xc7a100t-fgg484-3",
             "xc7a100tfgg484-2", "xc7a100t-fgg484-2L", "xc7a100t-fgg484-1L"):
    with patch.dict(TIMING_GRADE, part=part):
        platform = milan_soc.alinx_ax7101.Platform()
        try:
            with patch.object(milan_soc, "S7PLL", wraps=milan_soc.S7PLL) as pll:
                milan_soc._CRG(platform, 100e6)
            print(f"PLL {part:22s} speedgrade={pll.call_args.kwargs['speedgrade']}")
        except Exception as exc:
            print(f"PLL {part:22s} REFUSED {type(exc).__name__}: {exc}")
