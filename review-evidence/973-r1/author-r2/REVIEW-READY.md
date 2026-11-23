[A822] REVIEW READY
Commit: 5759780f2251ef25221c6a395250312dce656ca4
Round 2, PR #978; local branch `pf-973-1`, PR base `dev-soft-core`. Four local commits after `9a71daa9`.

F1: `srp_link_mutants.py` is classified in `ctrl_configs.py`'s `OUTSIDE` list with its non-compiling role stated.
`ctrl_boundary.py --require-rv32 --selftest` now passes locally: 4,455 compiled sources, zero findings,
117 boundary + 185 pin + 4 figure controls, zero misbehaved controls.

F2: SRP recovers after a re-attach that reads DOWN when its record is elided. A poll marks an uncarried register UP;
a later poll takes it only after a pass whose event take emptied the ring. Pending LINK events still arrive before
that fallback, preserving #973's first-UP behavior. The committed re-attach probe fails on `9a71daa9`'s firmware
at both shipping shapes and passes with the fix. Its ordinary later-UP control passes on both. A full-ring ordering
test and four more planted defects cover the fallback.

F3: retained and documented. Skipping the second DOWN reset adds 16 B to the current 8x8/1if image; that prototype
is refused at 58.5 RAMB36 against the unchanged 58-tile ledger. F4: the README states that marked recovery also
recovers an UP dropped by the re-entry guard. F5: the prepared PR body relates to #665, #970, #972, and #872.

Validation at this exact head:
- `test_ctrl_firmware.py --require-rv32 --self-test --shard K/4 --jobs 8`, K=0..3: PASS. 77 suite verdicts;
  control 826/826 caught; AECP 385 `[ok]`; SRP 576 `[ok]`; no escaped plants in the final gate.
- Eleven link plants killed at 1x1/1if, 8x8/1if, and 1x1/2if. The reviewer register-UP and sink-double-reset plants
  also remain killed. The old OR planting site is replaced by the committed OR plant at the new line.
- The reviewer's clear-carried-on-DOWN control escapes: the new fallback restores the same state and single reset,
  potentially one poll later. The escaped result is retained; that development campaign is not claimed all green.
- `fw_coverage.py --selftest` and `--check`: PASS, 40 files.
- `make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants`: PASS, zero findings, plants caught.
- CPU `run.py` at `1x1` and `8x8-1if`, all ten groups: PASS. 88/86 paired probes; zero refusals, budget misses,
  per-pass-share misses, or changed verdicts. Largest absolute base/head difference 0.217 ms against a 20 ms bound.
- `flip_grade.py --check` at both shipping points, `load_grade.py --check`, and `shape_costs.py --check`: PASS,
  byte-identical to base. Loads 0.511/0.744 against 0.70/0.75; 1x1 last notice 127.31 ms, ACMP 29.06 ms,
  txL 47.88 ms. The stored last-notice gate remains 130 ms, tighter than the owner's 140 ms ceiling.
- `plat_ledger.py`: PASS at all four points. ROM 126488/128104/139256/140856 B; SRAM unchanged;
  45/46/58/63 RAMB36 unchanged. The 8x8/1if ROM has 8 B before its next allocation.
- Documentation workflow gate steps: 104/104 PASS. Builder legs 0/1 pass with one declared NOT RUN arm each
  (an ineffective environment-option plant and a missing physical calibration report, respectively).
- Split boot: 1x1 and 8x8 PASS; self-test 6/6 native controls and 6/6 planted defects.

No RTL, mailbox contract, loop, budget bound, or budget harness change. The working tree is clean; no push or PR
edit was performed. Receipts, exact commands, and the indexed mutation logs accompany the Round 2 packet.

Independent re-review, the manager's push and hosted/local workflow reruns, merge-candidate validation,
existing fit/timing obligations, and post-merge bench scenarios remain required. This is author evidence,
not review approval or LAB qualification.
