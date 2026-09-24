#!/usr/bin/env python3
"""Round-2 reviewer-owned mutants, on top of the unchanged round-1 set.

Imports mutate.py (round 1, byte-identical) and adds mutants for the optional
U12 IDLE-clear arm and the U11 re-base position. Same exact-once rule: an edit
that does not match exactly once refuses (exit 3), so a mutant that silently
fails to apply can never read as "survived".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutate  # noqa: E402

RTL = mutate.RTL
EXTRA = {
    # IDLE no longer clears the MCSRV_STAT[15:10] tally (U12 IDLE arm)
    "idle_no_clear": [(RTL, "disc_run_r <= '0; disc_cnt_r <= '0;\n          verified_r",
                       "disc_run_r <= '0;\n          verified_r")],
    # the re-base after the 3rd consecutive guard discard, not the 4th (U11 position)
    "disc_max3": [(RTL, "DISC_MAX_C  = 4;", "DISC_MAX_C  = 3;")],
    # the tally counts only the guard's discards again (the pre-#539 count)
    "tally_guard_only": [(RTL, "7'(guard_hit_w) + 7'(step_hit_w)", "7'(guard_hit_w)")],
}
mutate.MUTANTS.update(EXTRA)

if __name__ == "__main__":
    sys.exit(mutate.main())
