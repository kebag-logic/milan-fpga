[A370]

Closes #582

Status: round 3 at `aafcae59732c0a12333b73d82d5cdcbcbf90c47f`, ready for independent delta review.

The builder and SoC now refuse bare-metal clocks that differ from the shared capture recipe contract. The former 80 MHz ROM variant is tested as a refusal, and the Scala diagnostic now covers every override.

Memory watchdog tests and the extra sweep read clock pairs from the configurations. The latency-tap page derives current cycle times per shape and preserves the dated silicon measurements at their original clock. The existing capture recipe remains the single clock definition, keeping the hash-bound measurement receipt unchanged.

Reproduce: `python3 sw/builder/test_clock_contract.py --soc` in the SoC environment. The extra sweep supports `--dry-run` for checking configuration-derived clock arguments.

Round 1 recorded passing builder, focused and documentation checks; independent review found the missing CI scope registration and the additional gaps resolved in Round 2. All five configurations retain identical generated artifact hashes. The existing hardware-report calibration arm remains NOT RUN because its report is absent; the deliberate compiler-absent mode records its expected stand-downs.

Independent review remains outstanding.

## Round 2

The latency-tap page is registered with the CI scope classifier, including its mutation control and reader documentation. The full builder bank now compares every configured gPTP ROM against an independent generator invocation at the Milan clock. Refusal tests cover each product command line, the no-Milan path, and `flashboot: none`.

The parameter reference and builder mapping name the fixed clock by its single definition. CLI usage and help state the required clock and generated entity options; defaults are unchanged. Watchdog clock pairs and sweep expectations now use normalized configurations, including omitted system clocks.

Head: `77998f14b16bf7605956332d0f0ac8af0cecab5a`. The required reviewer mutations are killed and controls pass. All five artifact sets match the base. Both complete builder compiler modes, declarations, capture receipt, memory bridge, focused contract checks, all 38 documentation/related commands, reviewer probes and whitespace checks return rc 0 at this committed head. The explicit classifier, scope, shape and documentation self-tests pass. The existing physical-calibration report remains unavailable; compiler-absent stand-downs are expected and recorded.

## Round 3

The CI policy now keeps the tap page outside the documentation-only table and explains its reader exclusion from `DOCS_JOB_PY`. The no-Milan help states the CLI smoke-path limitation. Product refusal cases include each configuration’s generated entity directory. The ROM test reports and skips its system-clock control when both configured clocks are equal.

Head: `aafcae59732c0a12333b73d82d5cdcbcbf90c47f`. The assigned S9 mutant is killed; the equal-clock probe passes with its reported skip. Both ROM miswiring mutants remain killed, and controls pass. All five configuration artifact sets match the base. All 48 validation commands return rc 0 at this committed head: both complete builder compiler modes, the focused SoC clock contract, declarations, capture receipt, memory bridge, reviewer probes, artifact identity, all 38 documentation/policy commands and both whitespace checks. This includes every explicitly assigned policy self-test. The existing physical-calibration report is absent; compiler-absent stand-downs are expected and recorded.
