[A761c] REVIEW READY
Commit: d08d30c6ecbac2e45867c3a509ef309ed081ab15 (branch `665-s11-aecp-reboot`, five commits on round 1's `b29f94d7aa`; not pushed)

Changed (round 2, under the ruling issuecomment-6789331293):
- Parity with the processor (REQ-FWX-001; the processor's `06_aecp_engine.md` 6.11). From the REBOOT's SUCCESS no received frame of any channel is taken: every channel's take sits behind a platform gate on the new `aecp_reboot_accepted`, installed through the loop's own bind API with each module's binding behind it. `sw/firmware/ctrl/loop/` is untouched. Once the REBOOT's frames are out (`aecp_reboot_due`) the loop is no longer serviced, so no channel starts another transmission. ENTITY_DEPARTING is committed only after every other ring has drained, so nothing follows it. The port fires once ADP's ring has drained too. No mailbox contract change.
- Tests: host B19 (no frame of any channel taken after the SUCCESS), B20 (no other channel's transmission while the DEPARTING is held 5 s with producers running), B21 (the DEPARTING waits for every other ring), B17 widened (nothing sent after the port). Each has a planted defect caught on its own words. AECP: index judged before the lock (R821 S1) and the acceptance reported, two more defects.
- CPU simulation: the `reset-before-the-response` plant now fires the port before the SUCCESS leaves and is caught by "the REBOOT's SUCCESS left the mailbox after the reset port fired". An AEM command and a BIND_RX are sent in the window, and frames after the DEPARTING and after the port are graded. A new plant opens the receive gate. Every plant and control must give its own finding's words. New controls `frame-after-the-departing` and `replay-mixed`. `PYTHONHASHSEED` is pinned for every export.
- Docs: `REBOOT_RESET.md` section 8 (the window as the processor keeps it; 424,271 bus cycles as one scenario's measurement; no firmware-stage bound while a ring is held). `MAILBOX_SPLIT.md` with R822-1 R1's exact text. The CDC census row names the REBOOT request level, via its generator. Both READMEs and the simulation README updated.
- Memory ledger re-measured: `ctrl_plat` 18,528 / 20,016 / 19,184 / 21,328 B. One coverage exclusion row: the gate's unbound-channel test, unreachable because every channel has its handler at ready.

Validation (each on a fresh clean clone of `d08d30c6ec`):
- `rtl-fast`, `elaborate`, `rtl`: 88 `run:` steps rc 0, 167 not run each with its reason, 0 bad. elaborate-gates-1's LiteX aggregate first ended UNKNOWN (exit 92, `test_soc_timing_cuts` at the 900 s wall clock under host load); rerun alone on the same clone 8 of 8 PASS.
- `docs.yml`: 64 rc 0, 31 not run with reasons, 0 bad.
- Full sweep, four native shards (the capture_coherence shard on 4 CPUs): 65 of 65 suites, 2,192,899 checks, 0 failures, 0 timed out; preflight PASS on each.
- `test_ctrl_firmware.py --require-rv32 --self-test`: PASS, control campaign 583 of 583. `fw_coverage.py --check`: PASS (35 files).
- Mutant drivers: AECP 152 of 152, SRP 280, saved-state 109 of 109 planted defects reddened.
- Publication census `--check --selftest`: 6 shapes, 246 checks, 0 failures; 0 of 164 arms failed; the REBOOT plants refused.
- S2 harness: self-test 0 failures; 1x1/1if 13 of 81 paths and 8x8/2if 29 of 129 over T_svc, recorded; every path equal to round 1's head. The base side is now published.
- `test_builder.py --require-rv32`: all gates pass except gate 11's calibration arm (no Vivado place report on this host); gate 1b's MAKEFLAGS mutation was run with GNU Make 4.4.1. `behave`: 14 features, 508 scenarios. `git diff --check` against the merge base: clean.
- `ctrl_reboot/run.py --self-test` and plain, both with no seed in the environment: PASS, 12 of 12 plants and controls on their own words.
- All-fabric exports (1x1, 8x8): all 22 generated files equal to the base's, LiteX's timestamps and hierarchy-comment order aside (they also differ between two exports of one commit).
- Reviewer probes at `d08d30c6ec`, scripts unchanged: R821 `behaviour-acmp-after-success` passes (`acmp_frames_after_success=0 sink_bound=0 frames_after_departing=0`); R821 `lock-before-the-index` now caught; R822 `run_probe_window.sh` reports `sink.bound` 0 and no ACMP frame.

Acceptance criteria: items 2 to 5 met; item 1 met for six of the eight items and the binding (configuration and sampling rate cannot leave their defaults at the shipping shape), so the PR says Relates to #871, as the ruling's item 7 keeps it.

Open risks/questions:
- R821 S4 not taken: a 0 tie on `i_reboot_req` in the all-fabric Instance adds exactly one line (`.i_reboot_req (1'd0),`) to the generated all-fabric top `.v` at both shipping configs, so it cannot keep the exports byte-identical as the ruling requires. The port is unread at `CTRL_SPLIT_P = 0`. Needs a decision if that line is wanted.
- The split boot simulation (`tb/verilator/ctrl_split_boot/run.py`, not this lane's) pins no hash seed and refused twice with none at an intermediate head, R822-F3's class; it passes with `PYTHONHASHSEED=0`. Suggest a new issue for its owner.
- The firmware stage has no bound while a mailbox ring is held (now documented, as the processor documents for its MAC).
