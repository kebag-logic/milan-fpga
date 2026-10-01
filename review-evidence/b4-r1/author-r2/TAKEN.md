[A469] TAKEN
Branch: `b4-bench-1001` at `35a60c8d6ee742216f98232c85926b435ab01b91` (PR #627), local only.
Authoritative references: the round-2 assignment 5925185587; the round-1 reviews on PR #627, R422-1 (5925175550) and R423-1 (5925182051); the B4 assignment 5924192573 and the manager ruling 5924950994; #626.
Interpreted scope: wording only, in `docs/findings/451_TDM8_TIMING_SOC_BOARD.md`, with no figure or verdict change and every measurement table byte-identical.
- R422-1 F1: the full-length recording size matches the 630 s capture (967.7 MB).
- R422-1 F2 and R423-1 S1: the verdict cell and the fs bullet claim only that fs is -42.8 ppm from 48 kHz on an uncalibrated clock, -10.64 ppm of it the plan, and the remaining -32.1 ppm the DUT oscillator's error relative to the SoC board's clock, unsplit and unquantified; the Frequencies paragraph states that signed relative error in place of "the sum of both boards' clock errors".
- R423-F1: the one-bit-offset sentence names which checks each direction trips, as the Framing paragraph details.
- Suggestions R422-1 S1 and S2, and R423-1 S2 and S3: "every identity value"; the talker's end 58.7 s before the unbind; the one-bit delay as the driver's mapping of the device tree's `dsp_a`, not a register readback; the `id` shell check, and no credential typed or stored.
Validation plan: `scripts/docs_check.py`, `scripts/check_doc_style.py`, `scripts/gen_toc.py --check`, `scripts/check_em_dash.py --base e4b771f9` and `scripts/check_doc_paths.py` in the pinned Markdown environment; `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check`, `scripts/check_feature_status.py --self-test` and `git diff --check`. All rc 0, unpiped, from the physical lane path. A diff proving every measurement table byte-identical. Local commit only, no push.
Blockers: none. No bench access in this round.
