[A370] REVIEW READY

Commit: 3baff4411fd70aaccb066662628ff0b0a7d7c05d (local branch `582-baremetal-clock`; no push or PR).

Changed: the builder and SoC import the existing capture recipe clock and refuse divergent bare-metal clocks by name. The 80 MHz ROM variant is now a refusal case; the Scala diagnostic covers every override. Memory-watchdog coverage and the extra sweep derive clock pairs from configurations. Current tap conversions are configuration-checked; the dated 100 MHz silicon conversions remain historical.

Validation: all assigned gates returned rc 0. All commands ran in the physical assigned worktree, in the foreground, without pipelines.

- Full builder bank with `--require-rv32`, and the same full bank with its three RV32 census candidates deliberately hidden.
- `python3 sw/builder/test_declarations.py`.
- `python3 scripts/check_nvm_capture.py`.
- `python3 sw/litex/test_pp_mem_bridge.py`: 113/113 checks plus actual SoC CLI and independent clock-pair controls.
- `python3 sw/builder/test_clock_contract.py --soc`: five configuration positives; 25 named clock refusals; no artifacts on refusal; implicit-system/disabled-domain paths; sweep defaults and overrides; tap conversions.
- Eleven source mutations killed by their intended tests: removed/ceiling builder guard, narrowed Scala message, removed/ceiling SoC guard, bypassed system fallback, copied sweep system/Milan clocks, swapped/copied watchdog clocks, and old tap conversion. Sources restored; focused tests pass.
- Documentation checks and relevant scope/source/idiom/shape checks: 31 commands, all rc 0. The added-line check uses base `9e9954e96bf55181edb9949ae94c9abd4ab6aaf5` and the committed head: 40 added lines in two pages, 339/339 arms.
- `git diff --check` and `git diff --check 9e9954e96bf55181edb9949ae94c9abd4ab6aaf5 HEAD`: rc 0.

The existing gate 11 calibration arm lacks its historical placed-resource report and is recorded NOT RUN. The deliberate compiler-absent mode also records its compiler-dependent stand-downs; the required-RV32 run covers those instruments. No hardware validation is claimed.

Acceptance: all five tracked configurations build. Every generated-artifact set matches the base byte-for-byte; the STOP condition was not triggered. The digest below hashes compact sorted JSON of artifact-role to per-file SHA-256; the complete per-file manifests are in the handoff.

| Configuration | Base and final SHA-256 |
|---|---|
| `endstation_arty_4x4` | `f1a8ba03c1e639a0e6628d664efadc5d71f5ea45e7aa5398d44c93a8cf92b3f0` |
| `endstation_arty_8ch` | `e31a65d95263cc96f308d9b29d83e53c0425a25a110728120741fe41e671f7fc` |
| `endstation_arty_current` | `12f3fcedf8b24a32862d00e4a42e2107b8ad2b115606fcbfcf74c77a59b0427f` |
| `endstation_ax7101_1x1_tdm8` | `deeee0e1261257049a0e4b69349d86c6f6ff52cc63c097f9f77d388b4b1050c4` |
| `endstation_ax7101_8x8` | `6f8ce8711b3d995df08874ede226159efb4cd566cd7d47002896d1eb881e7732` |

Tap-tool audit: tracked trace payloads and the generic reader retain `min_cyc`, `last_cyc`, and `max_cyc`; no tracked tap-cycle-to-time conversion tool was found. No firmware, RTL, submodule, configuration, or capture-receipt changes.

The output contains `HANDOFF.md`, `PR-BODY.md`, gate logs, per-artifact identities, and executable reproduction scripts. Independent review remains for the assigned internal and external reviewers. Open implementation questions: none. Stopping after this comment as assigned.
