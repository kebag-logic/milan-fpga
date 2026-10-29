"""projection.py: the physical gPTP leg's hosted deadline projection by tb/verilator/milan_dp/README.md's own method,
at the round-2 head (#803). Inputs are the README's recorded figures and the current scenario's cycle count (the
round-1 physical receipt, 899637137 cycles; the round-2 delta changes none of the leg's inputs)."""
HOSTED_SIM_S = 3261.56          # slowest hosted physical simulation, previous-previous scenario
CYC_OLD, CYC_PREV, CYC_NOW = 649624822, 849624822, 899637137
REMAINDER_S = 830               # hosted build, image generation and three accounting controls (does not scale)
LOCAL_SLOWDOWN = 1.3476         # the README's measured local slowdown branch
SETUP_S = 30 * 60               # the job's allowance for toolchain setup and evidence upload

prev_a = HOSTED_SIM_S * CYC_PREV / CYC_OLD                # 4265.7 s, the README's figure
prev_b = HOSTED_SIM_S * LOCAL_SLOWDOWN                     # the 5225 s branch less its remainder
ratio = CYC_NOW / CYC_PREV
proj = sorted([prev_a * ratio + REMAINDER_S, prev_b * ratio + REMAINDER_S])
print(f"previous scenario: {prev_a + REMAINDER_S:.1f} s and {prev_b + REMAINDER_S:.1f} s")
print(f"cycle ratio {CYC_NOW}/{CYC_PREV} = {ratio:.6f}")
print(f"current scenario: {proj[0]:.1f} s and {proj[1]:.1f} s (README rounds to {round(proj[0])} and {round(proj[1])})")
for deadline in (5400, 6900):
    print(f"suite deadline {deadline} s: {100 * proj[0] / deadline:.1f} % and {100 * proj[1] / deadline:.1f} %")
need = proj[1] / 0.80
print(f"worst case at most 80 % needs a deadline of at least {need:.0f} s; 6900 s = 115 min is the next whole 5 min")
for minutes in (120, 145):
    job = minutes * 60
    print(f"job {minutes} min = {job} s: margin {(job - proj[1]) / 60:.1f} to {(job - proj[0]) / 60:.1f} min, "
          f"worst case {100 * proj[1] / job:.1f} %; deadline + 30 min setup = {(6900 + SETUP_S) / 60:.0f} min")
