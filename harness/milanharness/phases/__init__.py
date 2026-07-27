# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Phase drivers. Each is `run(ctx, clock)` and owns no timeout of its own -
#! the runner gives it a `PhaseClock` and runs each item under its own alarm.

from . import (p0_baseline, p1_smoke, p2_validation, p3_counters, p4_matrix,
               p5_adversarial, p6_quality, p7_soak)

PHASE_FUNCS = {
    "baseline": p0_baseline.run,
    "smoke": p1_smoke.run,
    "validation": p2_validation.run,
    "counters": p3_counters.run,
    "matrix": p4_matrix.run,
    "adversarial": p5_adversarial.run,
    "quality": p6_quality.run,
    "soak": p7_soak.run,
}

__all__ = ["PHASE_FUNCS"]
