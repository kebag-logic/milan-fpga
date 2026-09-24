#!/usr/bin/env python3
"""Round-2 reviewer-added mutants (the round-1 set in mutate.py is unchanged).
Refuses if the anchor text is not found exactly once."""
import sys

MUTANTS = {
    # U12's IDLE arm: IDLE no longer clears the discard tally
    "M16_idle_no_clear": ("          disc_run_r <= '0; disc_cnt_r <= '0;\n          verified_r",
                          "          disc_run_r <= '0;\n          verified_r"),
    # U10's timing arm, bound side: the step verdict three cycles late
    # (count on the 5th edge, still sooner than the 1024 ppm guard can)
    "M17_detect_3_late": ("  wire step_hit_w  = ptp_jump_r && win_valid_r;",
                          "  logic [2:0] jd_m;\n  always_ff @(posedge clk_i) jd_m <= {jd_m[1:0], ptp_jump_r};\n  wire step_hit_w  = jd_m[2] && win_valid_r;"),
}

def main() -> int:
    name, path = sys.argv[1], sys.argv[2]
    old, new = MUTANTS[name]
    src = open(path, encoding="utf-8").read()
    if src.count(old) != 1:
        print(f"REFUSED {name}: anchor found {src.count(old)} times", file=sys.stderr)
        return 2
    open(path, "w", encoding="utf-8").write(src.replace(old, new))
    print(f"APPLIED {name}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print("\n".join(MUTANTS)); sys.exit(0)
    sys.exit(main())
