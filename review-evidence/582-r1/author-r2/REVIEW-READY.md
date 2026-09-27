[A374] REVIEW READY

Commit: `77998f14b16bf7605956332d0f0ac8af0cecab5a` on `582-baremetal-clock` (local only).

Required items 1-6 are implemented: tap-page CI classification and mutation control; configured-clock ROM evidence; product/no-Milan/flashboot-none refusals; fixed-clock parameter references; accurate CLI requirements with unchanged defaults; normalized watchdog and sweep clocks.

Reviewer evidence: R354 M21 and R355 probe 36 are KILLED by the new full-bank ROM test. R355 S1-S4 and B3 are KILLED, with C0-C3 passing. Pair mutations M16-M18 are KILLED. The 75-case SoC probe and omitted-system-clock probe pass. All five generated artifact sets match the base, and configuration files, recipe and capture receipt are unchanged. The STOP condition was not triggered.

Validation: all 51 recorded commands return rc 0 at this committed head, run in the foreground without pipelines from the physical assigned lane. This includes both complete builder compiler modes, `test_clock_contract.py --soc`, declarations, capture receipt, memory bridge, 38 documentation/related commands, all explicitly assigned self-tests, reviewer probes, artifact identity and both whitespace checks. The bare-metal scope gate ran with its required `--check` and `--selftest` modes; invoking it without a mode returns a usage error. The existing physical-calibration arm is NOT RUN because its report is absent; the compiler-absent mode records its expected stand-downs.

The handoff records each item with file:line and mutation/probe evidence, the five-configuration SHA-256 table against the base, and every gate command/result. The local PR body retains its original label and `Closes #582` and includes Round 2.

No push, PR edit, merge, hardware, firmware, RTL, configuration or capture-receipt change. Independent re-review remains for [R354] and [R355].
