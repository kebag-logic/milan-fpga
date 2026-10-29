"""projection.py <cycles>: the physical gPTP leg's hosted deadline projection by tb/verilator/milan_dp/README.md's own
method, at the round-3 merge head (#803). Inputs are the README's recorded figures and the scenario's cycle count
measured at the merge head (<cycles>, from the physical leg's own transcript)."""
import sys

HOSTED_SIM_S = 3261.56          # slowest hosted physical simulation, previous-previous scenario
CYC_OLD, CYC_PREV = 649624822, 849624822
CYC_README = 899637137          # the scenario the README projects now (FPGA-gPTP #90's fifth lost response)
CYC_NOW = int(sys.argv[1])
REMAINDER_S = 830               # hosted build, image generation and three accounting controls (does not scale)
LOCAL_SLOWDOWN = 1.3476         # the README's measured local slowdown branch
SETUP_S = 30 * 60               # the job's allowance for toolchain setup and evidence upload
DEADLINE_S, JOB_MIN = 6900, 145

prev_a = HOSTED_SIM_S * CYC_PREV / CYC_OLD                # 4265.7 s, the README's figure
prev_b = HOSTED_SIM_S * LOCAL_SLOWDOWN                     # the 5225 s branch less its remainder
ratio = CYC_NOW / CYC_PREV
proj = sorted([prev_a * ratio + REMAINDER_S, prev_b * ratio + REMAINDER_S])
print(f"merge-head scenario: {CYC_NOW} cycles; the README's {CYC_README}: "
      f"{'equal' if CYC_NOW == CYC_README else 'DIFFERENT'}")
print(f"previous scenario: {prev_a + REMAINDER_S:.1f} s and {prev_b + REMAINDER_S:.1f} s")
print(f"cycle ratio {CYC_NOW}/{CYC_PREV} = {ratio:.6f}")
print(f"merge-head projection: {proj[0]:.1f} s and {proj[1]:.1f} s (rounded {round(proj[0])} and {round(proj[1])})")
print(f"suite deadline {DEADLINE_S} s: {100 * proj[0] / DEADLINE_S:.1f} % and {100 * proj[1] / DEADLINE_S:.1f} %; "
      f"worst case within 80 %: {'yes' if proj[1] <= 0.80 * DEADLINE_S else 'NO'}")
job = JOB_MIN * 60
print(f"job {JOB_MIN} min = {job} s: margin {(job - proj[1]) / 60:.1f} to {(job - proj[0]) / 60:.1f} min, "
      f"worst case {100 * proj[1] / job:.1f} %; deadline + 30 min setup = {(DEADLINE_S + SETUP_S) / 60:.0f} min")
