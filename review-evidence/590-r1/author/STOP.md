[A385] STOP

Head: `8bc97021f28fb7f729418d3a00851c84ea0b50fd` (unchanged; the implementation is an uncommitted working draft).

The firmware census is blocked by a scope conflict. In both compiler modes, `sw/builder/test_builder.py:13304` asserts exactly two selections for its planted conditional. The optional MDIO implementation introduces a second conditional group, so the fixture now correctly enumerates four selections and fails that fixed-count assertion. The assignment excludes builder edits, so that file remains unchanged. A correction to this test fixture needs an explicit scope decision before this gate can be cleared; no assertion has been removed or weakened.

Reproduction entry points from the candidate workspace with its existing Python dependencies and compiler selector (both runs exited 1 at that assertion):

```sh
rtk proxy timeout 1800 python3 -B -c 'import sys; sys.path.insert(0,"sw/builder"); import test_builder; test_builder.test_baremetal_profile_contract()'
rtk proxy timeout 1800 python3 -B sw/builder/test_firmware_compiler.py --absent --audit /tmp/a385-census-absent.jsonl
```

The compiler-present run selected RV32 GCC 14.3.0. It passed the baseline contract check before reaching the fixture assertion. The absent run explicitly skipped the compiler-dependent instruments and failed the same fixture assertion; it is not compiled-census evidence.

Preliminary checks: the existing firmware host self-test passes all five shapes including Arty and kills all four existing mutants. The new PHY host test passes and kills a missing-publication mutant. Service-harness self-tests and the CI-scope self-test pass. The foreground 8x8 / 50 MHz / traffic-on capture arm completed with rc 0: 16/16 captures, minimum 13.21794 ms, maximum 13.23262 ms against the 24.5 ms bar, zero mismatches and zero open-record copies. All captures had concurrent requests, responses and reads. Processor pin: `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`. This is preliminary draft evidence, not the required complete re-measure or final-head gate set.

The required final-head service measurements, MDIO target timing and fabric-link simulation, remaining capture arms and receipt replacement, timing/dispatch controls, documentation updates and full builder banks are incomplete. No commit or REVIEW READY claim is offered. No push, PR operation, merge, hardware, RTL, processor, configuration or builder change was made.

The working draft, proposed unapplied fixture adjustment, command logs, artifact hashes, HANDOFF.md and draft PR-BODY.md are retained in the assigned output directory. Firmware SHA-256: `c4ae162d591beb89c44cb1092a6b93134df99fc1d6997271cbe877ee181b574c`.
