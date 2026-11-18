[A797] REVIEW READY (round 2)
Commit: `9f4f3de0` on `946-ctx-fmt` (dev-soft-core `cb96336d` + 11 commits; round 2 is `62296be7`, `85363367`, `0f6c12ba`, `548324b5`, `9f4f3de0` on `66c6edf3`). It composes onto the flip train (PR #945, `b1f1161b`) as step 12 with one composition step, below (scratch composition `d98dd322`; composed again at `9f4f3de0`, the same tree).

Changed (answering R868-1 and R867-1):
- R868-1-F1, a deferred SET_STREAM_FORMAT done again onto an input bound meanwhile: fixed by another ordering, in the split platform only (`plat/ctrl_plat.c`).
  - The platform wraps the face's `applied` port. While the core waits on a change that moves the context of an input bound now (its SET_STREAM_FORMAT, or any input's SET_CONFIGURATION), the change is not applied. The core keeps the values in force and answers ENTITY_MISBEHAVING at `AECP_WAIT_MS`: its documented timeout rollback, bounded, with no contract change.
  - The change port writes each kept change's contexts in the change itself, before the core answers it, with no mailbox access between. The poll is removed.
  - A context's format now moves only while its input is unbound. The race argument is corrected in `ctrl_plat.c`, `plat/README.md` and the PR body.
  - No AECP-face, core, ACMP or RTL source changes.
- Tests (`test_plat_sinks.cpp`). Every case watches each mailbox access: whenever an input's binding has a stream published, its context holds the input's current format, from the access that publishes it; and no SET_STREAM_FORMAT's SUCCESS leaves before its context holds it.
  - S6: the reviewer's order (settled, then acknowledged), then unbind and rebind. S7: acknowledged with the probe unanswered. S8: the timeout. S9: unbound again before the acknowledgement, then rebind. S10: SET_CONFIGURATION.
  - On round 1's platform, S6 reproduces the reviewer's observation (`input 7: current 0205022000806000, context 0205022002006000`), and S4, S5, S7 and S10 fail too.
  - At the RTL, [CF4] covers the PDU side of the boundary: the first PDU after a bind whose format was written the cycle before is accepted.
  - `sink_mutants.py` has 26 planted defects, 7 of them new; each is caught on its named test.
- R867-1 F-2: the poll is gone, so no platform code runs per pass. S5 checks that a change of another kind, and 100 passes with no change, write no context. S2 and S4 check that a change writes its own context alone. Planted: a pass rewriting every context, a change of another kind writing any, a format change writing all.
- R867-1 F-1: the ROM entries are raised on the branch by the owner's rule of 2026-11-15. `platform-8x8-two-interfaces` goes from 60.5 to 61.0 (133,224 B of rom, 104 B past 60.5), and a new `platform-8x8-one-interface` entry sits at 56.5 (131,656 B, 584 B past 56.0). They come with their memory-test cases, the ledger's point and a control, the boot SoC's ledgered points, and SPLIT_CONTROL_MEMORY sections 3 and 5.
- R867-1 F-3: the PR body names F-G2 as #948 and the release image's F-G1 as #949; "Closes #946" stays.
- R868-1-R1 and R867-1 R-1: the work-lane and flash-lane names are gone from the new comments.

Composition step: the ROM ledger's 7 files conflict with the train's. Each takes the train's side; in the platform README only its two ROM hunks do. The train's `platform-8x8-two-interfaces` entry is then raised from 62.5 to 63.0: the composed image plans 140,200 B of rom, 936 B past what 62.5 holds. The composed 8x8/1if image fits the train's 58.0 entry. The patch is in the receipts.

Validation (lane / composition):
- Firmware gate, `test_ctrl_firmware.py --require-rv32 --self-test`: PASS / PASS. Verdicts: 75 / 74, none failed. Control campaign: 743 of 743 / 823 of 823. AECP and SRP campaigns: 729 / 875 defects caught, none escaped. `Sinks.S1` to `S10` pass at 8x8/1if and 1x1/1if.
- `fw_coverage.py --check`: PASS / PASS, both changed files at 100 % lines and branches after exclusions.
- `plat_ledger.py --self-test`: PASS with 8 of 8 controls / PASS with 9 of 9. `test_ctrl_memory.py`: 0 failures / 0 failures.
- `make -C tb/verilator/avtp_rxmon` (pinned toolchain): PASS, CTXFMT N=8 96/96, engine plants 5/5. On the composition the sweep ran it too: 65 of 65 suites, 2,713,122 checks, 0 in-suite failures, the 4 declared skips tsn_fuzz's external-generator campaigns.
- Twin and plants: on the lane, dev-soft-core's own result (the owed row `split-talker-failed`; plant `srp-plus-k` escapes), with captures byte-identical to `cb96336d`, which was run here too. On the composition: 0 findings, every plant refused.
- Docs workflow steps: lane, every step dev-soft-core has passes; composition, 97 of 97.
- Split boot simulation: lane 8x8 PASS. Composition 8x8 PASS: 28 context writes before ready, ready at 67.328 against the train head's 67.134 ms. Composition 1x1 PASS: no context writes, 27.936 against 27.981 ms.
- CPU-budget rows carry: the images are hash-equal to the train's recorded ones (1x1 `55484254e638ed7f`, 8x8/1if `175418f4b5b1a9d4`), and no input of them changed.
- A correction to round 1: its "1,546 / 1,778" planted-defect totals also counted the gate's 81 / 87 arm lines. The defects were 1,465 / 1,691.

Acceptance criteria:
- Inputs 1-7 receive, alone and all at once: met in simulation, as in round 1 ([CF2]; the product image writes the words before ready). On hardware this is the bench's stream item.
- A test that fails on the current code: met (S1, and now S6 for the deferred path).
- The bench's stream, power-cycle and soak items at 8x8/1if: not run here (no hardware in this lane).

Open risks/questions:
- A refused waiting change is answered ENTITY_MISBEHAVING at the wait's bound (100 ms), the core's answer for a change not applied, not STREAM_IS_RUNNING.
- During that wait the datapath's copy of the face (`F_FMT_IN`, the map's channel clip for inputs above 0) may hold the refused value until the face republishes the values in force. That is the face's existing rollback path.
- For input 0, the CRF input and STREAM_OUTPUTs, which have no context here, the core still does a waiting change again without repeating its bound or running check. Repeating it there is a core change that moves every CPU-budget image; a ticket of its own is proposed.
- ROM debt: on dev-soft-core the product SoC build names no entry, so an 8x8/1if product build there is held to 56. The train plans product images at their own entry.
