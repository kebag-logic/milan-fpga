[A370]

Closes #582

Status: round 1 at `3baff4411fd70aaccb066662628ff0b0a7d7c05d`, under independent review.

The builder and SoC now refuse bare-metal clocks that differ from the shared capture recipe contract. The former 80 MHz ROM variant is tested as a refusal, and the Scala diagnostic now covers every override.

Memory watchdog tests and the extra sweep read clock pairs from the configurations. The latency-tap page derives current cycle times per shape and preserves the dated silicon measurements at their original clock. The existing capture recipe remains the single clock definition, keeping the hash-bound measurement receipt unchanged.

Reproduce: `python3 sw/builder/test_clock_contract.py --soc` in the SoC environment. The extra sweep supports `--dry-run` for checking configuration-derived clock arguments.

Validation: both full builder modes, declarations, capture receipt, memory bridge, 11 mutation controls, 31 documentation/related checks and whitespace checks return zero. All five configurations retain identical generated artifact hashes. The existing hardware-report calibration arm remains NOT RUN because its report is absent; the deliberate compiler-absent mode records its expected stand-downs.

Independent review remains outstanding.
