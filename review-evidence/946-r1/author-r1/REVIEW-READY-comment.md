[A797] REVIEW READY
Commit: `66c6edf3` on `946-ctx-fmt` (dev-soft-core `cb96336d` + 6 commits). It composes onto the flip train (PR #945, `b1f1161b`) as step 12 with no conflict (a scratch composition, `d6d71354`).

Changed: firmware only, in the split platform. No RTL, no mailbox-contract change, and the AECP face is untouched.
- Cause: `KL_avtp_rx_monitor_ctx` judges a PDU of a stream above 0 against its LCTX context's FMT_LO/FMT_HI words. The engine writes those words for stream 0 only, and nothing else wrote them, so inputs 1-7 compared every PDU against a zero format.
- Fix: `sw/firmware/ctrl/plat/ctrl_plat.c`, `ctrl_plat_csr.c`/`.h`. Every AAF STREAM_INPUT above 0 takes its current format into its context through the existing CSR 0x800 window: after the face's open (before ADP starts), at a SET_STREAM_FORMAT once its commit is acknowledged, and at the platform's poll for a change the face defers or a change of another kind, once a later commit is acknowledged.
- Tests: `test_plat_sinks.cpp` S1-S5 at 8x8/1if and 1x1/1if, `test_plat.cpp` C5/C6, and 19 planted defects (`sink_mutants.py`). An RTL contract test at the 8x8 shape's eight contexts (`tb/verilator/avtp_rxmon/sim_ctxfmt.cpp`, 96 checks) with 4 planted engine defects (`ctxfmt_mutants.py`).
- Docs: `sw/firmware/ctrl/plat/README.md`.

Validation (lane / composition):
- Firmware gate, `test_ctrl_firmware.py --require-rv32 --self-test`: PASS / PASS. The suites passed (75 / 74 verdicts, none failed), and every planted-defect campaign reddened all its defects: 1,546 / 1,778, the control campaign 736 of 736 / 816 of 816, the 19 new ones among them, none escaped.
- `fw_coverage.py --check`: PASS / PASS. Both changed files are at 100 % lines and branches after the documented exclusions.
- `make -C tb/verilator/avtp_rxmon` (the pinned toolchain): PASS, with CTXFMT N=8 96/96 and its mutants 5/5. The composition's sweep: 65 of 65 suites, 2,713,122 checks, 0 in-suite failures. The only declared skips are tsn_fuzz's external-generator campaigns.
- Twin and plants: on the composition, 0 findings and every plant refused. On the lane, the one finding is dev-soft-core's own (owed row `split-talker-failed`, which the train restates); the lane's captures are byte-identical to the base's.
- Docs workflow steps: lane, every applicable step passes; composition, 97/97.
- Split boot simulation at 8x8 on the composition: PASS. Before ready, the product image writes SEL k, FMT_LO `02006000`, FMT_HI `02050220` and SEL back for k = 1..7. That is 28 writes more than the train head, and 0.107 ms more to ready (67.241 against 67.134 ms).
- CPU budget rows: they carry. The budget images are hash-equal to the train's recorded images (1x1 `55484254e638ed7f`, 8x8/1if `175418f4b5b1a9d4`), and no input of those images changed.

Acceptance criteria:
- Inputs 1-7 receive, alone and all at once: met in simulation. The RTL test feeds each of the eight contexts, holding the words the platform writes, an in-format PDU: each first one is accepted and counted in FRAMES_RX, with UNSUPPORTED_FORMAT at 0. The product image writes those words for inputs 1-7 before ready. On hardware this is the bench's stream item, to rerun.
- A monitor-context test binds streams above 0 and fails on the current code: [CF1] reproduces the bench symptom on the RTL (inputs 1-7 discard, input 0 receives). The defect is in firmware, so the test that fails on the shipped behaviour is S1: it fails for each of inputs 1-7 by name, and passes with the fix.
- The bench's stream, power-cycle and soak items at 8x8/1if: not run here (no hardware in this lane).

Open risks/questions:
- ROM: about 1 KB of RV32 text costs half a RAMB36 at one ledger point on each base. dev-soft-core's 8x8/1if goes from 56 to 56.5; the train already carries an 8x8/1if entry at 58.0. The train's 8x8/2if goes from 62.5 to 63.0, so its `platform-8x8-two-interfaces` entry needs raising on composition. Under the owner's loose-BRAM rule this is S14 debt. The lane leaves the ledger alone, so it merges cleanly.
- F-G2 (one stream bound to two inputs) has another cause. The parser classifies a PDU to one context (`avtp_stream_parser.sv:193-196`); fixing it needs RTL and a ruling. Its own ticket.
- F-G3 is #943's.
- The all-fabric image shares F-G1 and is byte-identical here. Its fix is RTL. Its own ticket.
