"""Drive the real AX7101 _CRG with edge-case declared parts (run from sw/litex of a probe tree)."""
from unittest.mock import patch
import milan_soc
from platforms.ax7101_timing import TIMING_GRADE
for part in ("xc7a100t-fgg484-2", "xc7a100t-fgg484-1", "xc7a100t-fgg484-3",
             "xc7a100t-fgg484-2L", "xc7a100t-fgg484-1LI", "xc7a100tfgg484"):
    try:
        with patch.dict(TIMING_GRADE, part=part):
            platform = milan_soc.alinx_ax7101.Platform()
            with patch.object(milan_soc, "S7PLL", wraps=milan_soc.S7PLL) as pll:
                milan_soc._CRG(platform, 100e6)
        print(f"{part}: speedgrade={pll.call_args.kwargs['speedgrade']}")
    except Exception as exc:  # report, do not hide, the failure mode
        print(f"{part}: REFUSED {type(exc).__name__}: {str(exc)[:100]}")
