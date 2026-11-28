# Arty split 4x4/1if, round 4: the rulings, #1004 round 11, and the PR

Round 3's qualification stands: route, census, row, egress and identity (round3/REPORT.md sections 1 to 5). This round applies the manager's five decisions, merges #1004 round 11 and re-runs the gates the merge and the new commits touch. It also prepares the PR.

## 1. Commits this round

| Commit | Change |
|---|---|
| `5e298db8e` | Merge of #1004 round 11 (`c0b625d1792e61b8e99944daea65b842e6b9dcde`, the local `arty-int-1127` tip, the head pushed to `pf-arty-split-1`) |
| `9e8ca43bd` | The `arty-4x4` held-egress ledger: `egress_ledger.py`, section 15's table, the harness README, BUILDING, ENDSTATION_BUILDER, FR_NFR 3.4.1 |
| `12ab4b189` | FR-CLK-05: the 4x4 image's timestamp correction pair at 100 MHz, owed to a measurement on the board |

**The merge.** #1004 round 11 changes 11 files. Nine merged clean. Two conflicted on wording against this lane's per-point code:
- `tb/verilator/ctrl_service_budget/README.md`: the lane's `arty-1x1` and `arty-4x4` paragraphs kept, with round 11's "#983's host point" wording;
- `tb/verilator/ctrl_service_budget/arty_grade.py`: the lane's per-point `CLOCKS[point]` check kept, with round 11's "CPU (sys domain) clock" message.

The clean-merged files are:
- `ctrl_loop.h`: a comment in the AX7101 defaults' header block;
- `egress_ledger.py`, `SPLIT_CONTROL_MEMORY.md`: wording;
- `gtest/README.md`, `coverage.ratchet`: the console's coverage exclusion;
- `REGISTER_MAP.md`, `register_descriptions.json`, `rtl_fingerprint.txt`: the regenerated register reference;
- `measure_test_evidence_readers.py`: a reader note.

No HDL, LiteX or firmware code line changed. `check_baremetal_only.py --check` passes on the merged tree, so no retired-stack term remains.

## 2. Decisions applied

1. **Held-egress ledger.** `arty-4x4` is its own ledger point by #878's rule, as #1020's ruling (comment 7234489667, item 3) makes the USB-network Arty's.
   - `ARTY_4X4` holds the seven rows the link-rate census measured on the qualified image, at exactly 100 MHz (round 3's `qualification.json`, `held_egress.rows`).
   - Each figure is derived by `figure()`. Section 15's new table states the measured and ledger values side by side.
   - The largest figure is 63.50 ms, over the 63.32736 ms measured.

   | Row | Measured, ms | Ledger, ms | Headroom, ms |
   |---|---:|---:|---:|
   | `backlog.owed.if0` | 62.64658 | 62.78 | 0.13342 |
   | `backlog.owed_behind0.if0` | 62.82023 | 62.97 | 0.14977 |
   | `backlog.owed_behind1.if0` | 62.98813 | 63.14 | 0.15187 |
   | `backlog.owed_behind2.if0` | 63.15874 | 63.32 | 0.16126 |
   | `backlog.owed_behind3.if0` | 63.32736 | 63.50 | 0.17264 |
   | `backlog-owed.service.acmp.last.if0` | 61.81513 | 61.91 | 0.09487 |
   | `backlog-owed.service.aecp.last.if0` | 61.56471 | 61.65 | 0.08529 |

   **Which measurement.** The basis is the link-rate census, because it ran on the image the row qualifies. Censuses 2 and 3 ran with instant egress on earlier rows' firmware, which never ships; their held-egress rows were not regraded.

   **Grade.** `egress_ledger.py --point arty-4x4` over census 4's eight results directories reads 1655 instances, all measured. The result is PASS: no row over its figure, every row measured, no new miss.

   **Self-test.** The controls now run at all three points. At `arty-4x4` they plant each row one 10 ns cycle over its figure, and 36.76 ms over. Three new mutants are caught:
   - the 1x1 ledger used at the 4x4;
   - a 4x4 measurement changed without rederiving its figure;
   - a 4x4 figure a hundredth under the rule.

   The result is 24 mutants caught, 0 failures. The README's mutant count was stale at the base (it said eighteen for 21) and now states twenty-four. The 1x1's and 8x8/1if's figures are unchanged.
2. **Bind bounds.** Confirmed: 550 ms in flight and 4 burst saves, PR #1004's rule at this point (`bind_save.py`, `d0f402ee5`). No change this round.
3. **Dependency.** #1004 round 11 is merged (section 1). The images are byte-identical (section 4).
4. **Latency pair at 100 MHz.** Recorded as owed in FR_NFR, as a note under FR-CLK-05 ("measured physical correction"), and in the PR body. There was no bench and no flash.
5. **Thin margins.** Recorded as measured, with the owner bounds unchanged:

   | Quantity | Measured | Bound | Margin |
   |---|---:|---:|---:|
   | txL | 48.72 ms | 49 ms | 0.28 ms |
   | THE SHARE (longest whole pass, 173322 cycles) | 1.733 ms | 2 ms | 0.267 ms |
   | Setup, Slow WNS, ExtraPostPlacementOpt | +0.049 ns | +0.030 ns | 0.019 ns |
   | Setup, ExtraTimingOpt and AltSpreadLogic_high | +0.002 ns | +0.030 ns | misses the floor (not the shipped route) |
   | Hold, Fast WHS, ExtraPostPlacementOpt | +0.012 ns | 0 ns | 0.012 ns |

## 3. Gates at `12ab4b189`

Every gate below ran at `12ab4b189f54439cd126f677b906a19835d7f32a`, at nice 19, with logs in `receipts/`.

| Gate | Result |
|---|---|
| Firmware, four shards, `--require-rv32` | PASS, each shard `test_ctrl_firmware: PASS` |
| Split boot simulation at the 4x4 (100 MHz) | PASS, 0 findings |
| Native controls at the 4x4 | 6 of 6 as required |
| Region decode self-test at the 4x4 | PASS |
| Split boot simulation at `endstation_arty_split` | PASS, 0 findings |
| `test_ctrl_memory` | PASS, 0 failures |
| MII and `lat` host arms | PASS, 15 of 15 plants caught |
| Firmware coverage ratchet (`fw_coverage.py --selftest`, `--check --jobs 4`) | PASS (40 files) |
| `egress_ledger.py --selftest` | PASS, 24 mutants, 0 failures |
| `egress_ledger.py --point arty-4x4` over census 4 | PASS, 1655 instances measured |
| `arty_grade.py --point arty-1x1`, `--point arty-4x4`, `--selftest` | PASS |
| Service self-test, 8 partitions | 323 of 323 mutants caught, 0 failures |
| `sw/builder/test_builder.py` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11, section 5) |
| Docs workflow, 96 runner-free commands (`tools/docs-cmds.txt`) | PASS, see below |
| `gen_hdl_reference.py --selftest` and the HTML build | PASS, 44/44 arms |
| `check_em_dash.py --base aa30d77f` (merge-base with `dev-soft-core`) | PASS, 0 findings over 2799 added lines in 64 pages |
| `check_baremetal_only.py --check` | PASS, 0 findings over 1987 files |

**Docs.** On system Python, 86 of the 96 commands pass. The other 10 failed for missing packages that CI installs:
- `wavedrom` and the pinned Markdown renderer;
- for `check_em_dash`, an unset `$base`.

Each of the 10 was re-run with its package present, and each passes:
- `gen_wavedrom.py` ×4 and `gen_register_reference.py --check` / `--selftest` in the LiteX venv;
- `gen_toc.py --selftest` / `--verify-anchors` / `--check` and `check_em_dash.py` in an existing Markdown venv, with the base given.

The receipts are `docs/venv-docs.rc.txt`, `docs/venv2-docs.rc.txt` and `docs/em-dash.log`.

The builder log's `disabled-writer endstation_arty_4x4 … FAIL` lines are a planted-mutant arm ("caught in both states"). They print identically at round 3's head.

## 4. Byte identity

At `12ab4b189` (after the merge), the existing images were rebuilt with `tools/identity.py head` and compared with round 3's base digests (`aa53840d9`):
- All 66 builder outputs of the six existing configurations are byte-identical.
- The product ELFs are byte-identical: `endstation_arty_split` `f17d1a9d…`, `endstation_ax7101_1x1_tdm8` `6e0a5412…`, `endstation_ax7101_8x8` `0f1450ac…`.
- As in round 3, only the three `size.json` files differ, through the `ar` member digests of `libc.a` and `libcompiler_rt.a` and the absolute paths in `ctrl_app.map`. The members are the same and the maps are equal after path normalisation.
- The 4x4 product ELF is `1b8066e4cd65f446366f6f2574a8e6b099310f7d34f6d8923d861f20a887b09c`, the routed round-3 image's ELF.

So the merge's `ctrl_loop.h` comment changes no firmware byte. The round-3 census traces and route therefore stand for the head.

## 5. Gate 11

NOT RUN. It compares `arty_current`'s resource estimate with the place report `~/litex-milan/work/build_arty_eto_milanfinal48/gateware/digilent_arty_utilization_place.rpt`, the build the estimator was calibrated against. That directory is not on this host (the work tree has 418 entries, none `*milanfinal48*`). Nothing in the tree records the commit it was built from: `endstation_builder.py`'s calibration notes name only the directory. The build is an earlier-architecture Arty image (VexiiRiscv with a 64 KB L2, the retained-fabric AECP listener), so it cannot be rebuilt from this branch.

A current `arty_current` place report at that path would replace the gate's oracle rather than run it. The estimate it would compare is `arty_current`'s, whose builder outputs are byte-identical to the base (section 4), so this branch does not move it.

## 6. Open

- Owed: the timestamp correction pair at 100 MHz, to be measured on the board.
- The thin margins in section 2, item 5, as measured.
- Review: independent review of the PR at its head; nothing is pushed or posted.
