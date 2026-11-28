[A863] REVIEW READY
Commit: 12ab4b189f54439cd126f677b906a19835d7f32a
Branch: `arty-4x4-1127`, PR base `dev-soft-core`, stacked on #1004 (carries #1004 round 11 `c0b625d1792e61b8e99944daea65b842e6b9dcde`; merges after it).

Changed:
- Arty split 4x4/1if: `configs/endstation_arty_split_4x4.yaml` (4 AAF talkers and 4 AAF listeners, CRF in and out, one 100 Mb/s interface, AUDIO_UNIT 48 kHz only, sys/CPU 100 MHz = 800 MHz VCO / 8) and its generated shape include.
- `ctrl_loop.h` THE SHAPES (1,5,5) row, the rule's: slice 1250 us, pace 5 ms, queued 125 ms, TX 29 ms.
- Service-budget harness: the `arty-4x4` point in every per-point table at its own 100 MHz clock, `arty_grade.py --point`, bind bounds 550 ms / 4 saves, its own held-egress ledger (`egress_ledger.py` `ARTY_4X4`); `egress_mii.py` counts the CRF output's frame; the fixed-path bench takes another sys clock.
- Builder suite and harness self-test name the new configuration and point.
- Docs: ENDSTATION_BUILDER, BUILDING, harness README, FR_NFR 3.4.1 (100 Mb/s row, held egress) and FR-CLK-05 (owed correction pair), SPLIT_CONTROL_MEMORY section 15 (qualification, held-egress ledger, memory).
- Merge of #1004 round 11 (`5e298db8e`); two wording conflicts resolved keeping the per-point code.

Validation (exact head unless named):
- Route at sys 100 MHz, ExtraPostPlacementOpt, every corner: Slow WNS +0.049 / WHS +0.156 ns, Fast WNS +1.606 / WHS +0.012 ns, 0 failing endpoints (#818 floor +0.030 ns, WHS >= 0). ELF `1b8066e4cd65f446366f6f2574a8e6b099310f7d34f6d8923d861f20a887b09c`, rebuilt byte-identical at this head.
- Census: three complete 159-case censuses at 100 MHz, the last at link rate; qualification PASS over 159 cases and 8 variants: load 0.4689/0.70, ACMP 28.52/30 ms, txL 48.72/49 ms, last notice 117.68/140 ms, THE SHARE 1.733/2 ms.
- 100 Mb/s egress (`egress_mii.py`, 159 cases): (a) PASS at link rate; (b) 446.76 us wait, with one gPTP burst and 5 %, plus the 300.0 ns fixed path measured at 100 MHz, is 527.04 us <= 1000 us.
- `egress_ledger.py --point arty-4x4` over census 4: 1655 instances, all measured, PASS. `--selftest`: 24 mutants caught, 0 failures.
- `arty_grade.py --point arty-1x1`, `--point arty-4x4`, `--selftest`: PASS.
- Service self-test, 8 partitions: 323/323 mutants caught, 0 failures.
- `sw/builder/test_builder.py`: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: its calibration report, a v1-era `build_arty_eto_milanfinal48` place report, is not on disk and its build is not reproducible from the tree).
- `fw_coverage.py --selftest` and `--check`: PASS.
- Firmware, four shards with `--require-rv32`: PASS.
- Split boot simulation at the 4x4 and at the 1x1: PASS, 0 findings each.
- Native controls 6/6 and the 4x4 region self-test: PASS.
- `test_ctrl_memory`: 0 failures. MII and `lat` host arms: 15/15 plants caught.
- Docs workflow: all 96 runner-free checks plus `gen_hdl_reference` pass. Ten of them were re-run with the packages CI installs (wavedrom, the pinned Markdown renderer), as REPORT.md section 3 lists. `check_em_dash --base aa30d77f`: 0 findings over 2799 added lines. `git diff --check c0b625d1..HEAD`: clean.
- Identity at this head against `aa53840d9`: all 66 builder outputs of the six existing configs and the product ELFs of `endstation_arty_split` (`f17d1a9d…`), `endstation_ax7101_1x1_tdm8` (`6e0a5412…`) and `endstation_ax7101_8x8` (`0f1450ac…`) are byte-identical; `size.json` differs only by `ar` mtimes and map paths.

Acceptance criteria:
- 4x4/1if configuration builds and fits: met (49.5 of 56 RAMB36; 41,858 LUT, 86 BRAM tiles).
- Row by the unchanged rule (#969 disposition, #1022 owner), fixed point, owner bounds: met at 100 MHz (table above); at 80 MHz no row exists (round 1).
- 100 Mb/s egress replay (a) and (b): met.
- Routes at every corner against the #818 floor: met by ExtraPostPlacementOpt; the other two directives miss the floor at +0.002 ns.
- All gates: met, gate 11 NOT RUN with its reason.
- 1x1 and ALINX images byte-identical: met.
- Held-egress ledger at `arty-4x4` (manager decision 1): met, 61.65 to 63.50 ms, measured 61.56471 to 63.32736 ms.

Open risks/questions:
- Owed: the timestamp correction pair at 100 MHz (image keeps 1409/100 ns measured at 80 MHz); needs a measurement on the board.
- Thin margins, as measured: txL 0.28 ms, THE SHARE 0.267 ms, setup 0.019 ns over the floor on the one closing directive, hold +0.012 ns.
- Depends on #1004 landing first.
