# Variants used by this round's legs

- `drafts-staged.patch`: the D11 legs' parent changes, applied in a scratch clone at `37e200e6`. tsn-c-stack's draft `6532c3b0` and lwSRP's draft `fc06e7c0` by gitlink, `ctrl_arms.LWSRP_REV` moved, and the runtime's `__lshrdi3` hot-list entry removed, as rounds 8 to 10 staged them. The two submodule commits were fetched locally from round 10's scratch clone.
- `experiment-rx-per-pass-1.patch`: the X11 legs' labelled experiment, in a scratch clone at `37e200e6` and not on the branch. `CTRL_LOOP_RX_PER_PASS` is 1 instead of 2, a pass split by the loop's own named constant, to measure the per-pass share against the rows.

No leg used a harness variant: the CPU clock is the committed harness's default (the product's 50 MHz) or its labelled `--cpu-hz 100000000` option.
