[A775] STOP — round 3, head `f1f21546294b076d6c21187d5aafb67ab547123e` (local, not pushed)

**Why: the 8x8/2if size fixture's ROM cap, 58.5 RAMB36, cannot be held** (round 3 assignment item 4; #895 acceptance 5; #905 acceptance 5). No bound, cap, ceiling or ledger entry was changed.

| 8x8/2if image (rom / sram, B) | cap | #810's head `084cf7a8` | the sync merge `cd6d79b6` (no #905 code) | head |
|---|---:|---|---|---|
| size fixture | 58.5 | 123,808 / 113,168: 58.5 | 124,832 / 113,216: 58.5, 96 B of rom left | **125,576 / 113,232: 59.0, refused** (648 B past 124,928) |
| CPU budget harness, `answering-every-port` arm | 58.5 | 124,116 / 113,232: 58.5 | **125,140 / 113,280: 59.0, refused** (212 B past) | 125,884 / 113,296: 59.0 (956 B past) |
| CPU budget harness, `valid-destinations` arm | 58.5 | (no such arm) | **124,992 / 113,216: 59.0, refused** (64 B past) | 125,736 / 113,248: 59.0 (808 B past) |
| target platform | 60.5 (plans 60.0) | 128,960 / 114,160: 59.5 | 129,984 / 114,224: 60.0 | 130,728 / 114,224: 60.0 (344 B left) |

- **The merge alone already puts both harness arms past the cap.** #810's own section 5 records that cap as fully used. #895's Talker declarations add about 1 KB of rom at that point.
- **The #905 fix then takes the fixture past it too.** It costs 600 to 744 B of rom an image, and 0 to 32 B of sram.
- **So at 8x8/2if neither the fixture nor its harness arms link under the ledger.** No harness leg and no gate pass ran.
- **To go on:** the S2b names patch has to recover at least 956 B of rom at that point (the `answering-every-port` arm's image), or the owner rules on the point.
- **Every other point holds.** Fixture 38.5, 42.0 and 52.0; platform 40.0, 43.5 and 53.0 (each at most 56). `plat_ledger.py` passes: the platform's images and the ledger keys, `ctrl_plat` unchanged at every point.
- **How measured:** RV32 images linked on each shape's own split export and runtime (`plat_ledger.py`'s), at all three commits, from clean clones.

**Item 1, the sync.**
- One merge, `cd6d79b6`, of `665-s2b-cycles` at `084cf7a8` (#810 is open, not in dev-soft-core). Submodule pins are equal on both sides.
- 8 files conflicted, the same 8 as the bench lane's merge. Each was resolved from the composed tree:
  - **`load_grade.py`:** each stated cost is the larger of the two sides' (24 keys), the same values as the bench lane's merge. The comments are #810's with #895's sentence.
  - **`ctrl_memory.py`:** #810's stage of 13,594 with #895's `ctrl_plat` of 20,352. The ledger docstring and `test_ctrl_memory.py` take #810's side.
  - **`coverage.ratchet`:** `srp_mbx.c` from #895, `nvm_*` from #810.
  - **`SPLIT_CONTROL_MEMORY.md`:** #895's section 5 table kept as of `18300f6e`. Section 13's figures are #810's.
  - **Both READMEs:** #810's, with #895's platform figures.
- The split boot simulation reaches ready at 1x1/1if, 8x8/1if and 8x8/2if, at the merge (26.276, 65.007 and 67.062 ms) and at the head (26.278, 65.118 and 67.208 ms). Each run has 0 findings.

**Item 2, #905** (`3496eaa3`, `1aa59f75`, `99b71b44`, `f1f21546`; an earlier design `e9011df6` is superseded in code):
- **Who writes the ID.** The MAAP adapter, which owns DA_GATE, writes each source's SRC_SID_LO and SRC_SID_HI (`mbx_pub_src_sid`, one register a write).
  - The value comes from the declaration owner's source port, the port `acmp_declaring` reads.
  - In the platform that is `ctrl_plat.c` `stream_id()`: the entity's MAC and the output's unique ID. It is the ID the Talker declares and GET_TX_STATE answers. No literal is used.
- **When.** `maap_mbx_start` writes every source's ID before any pass runs and before any DA_GATE bit opens, so before any declaration or PROBE_TX response (`KL_mbx_pkg.sv:345`).
- **Before every reopening.** A closed source opens only once its ID has been written since it last opened. The poll writes it one word a poll, the low word first, read from the port just before, in a poll that writes no gate. The gate holds the source closed meanwhile.
- **What that covers.** A changed gate is re-published with a fresh ID, and a stream_id changed while the gate was closed reaches the register before frames do.
- **Bounds unchanged.** The poll's one publication write is "a changed gate, or else one SRC_SID word", so `MAAP_MBX_*_MAX` and every composed pass bound keep their values. `range()` is untouched, and so are the plant anchors on it.
- **Unit tests,** `SrpGate.F905A*` (4), at 1x1/1if, 1x1/2if and 8x8/2if. Each checks a history of publication writes: the ID at each opening, no word written while the bit is open, and both words written again between a closing and a reopening.
- **Five plants** in `srp_talker_mutants.py` (34 in all), each caught on its words at 8x8/2if and 1x1/1if:
  - the gate opening before the ID is written (`unwritten-at-start`, `opens-before-its-high-word`);
  - a stale ID after a change (`never-held`, `written-mark-kept`);
  - word order (`words-swapped`).
- **Other checks.** The full firmware suite passes on a clean clone of the head (71 arms). Coverage is 100 %: `maap_mbx.c` 158/158 lines and 92/92 branches, `mbx.c` 365/365 and 186/186. The control campaign, cut to the 80 mutants this change can reach, catches all 80.
- **Simulation check.** New `[SID]` grade in srptx's licence scenario, on the twin's split half: the platform firmware on `KL_mbx` and `milan_datapath`. A stream must leave, and every stream frame's AVTPDU stream_id must be one the split's own Talker Advertise declared.
  - At the head: 119 stream frames, each carrying `0200000000010000`, the declared ID.
  - #810's head's own capture, graded by the new grade, is refused: 119 frames carry `0000000000000000`.
  - The capture plant `stream-id-unwritten` is refused, and so is the code arm "no source's SRC_SID written". The arm was run by hand with `srptx_mutants.py`'s own build and run, because its clean control is refused by the finding below.
- **#905's acceptance.** Items 1, 2 and 3 are met. Item 5 is not (the cap above), so the PR body says "Relates to #905", not "Closes". Item 4 is the bench run.

**Item 3.** R835-2-RS1 is taken word for word in `srp_bounds.h` (`fa3f31ee`). R836-2-RS1 is taken in the round 3 PR body's acceptance-4 introduction: analytical tables are kept apart from measured margins. The round-2 comment it names is not edited.

**Acceptance 4 at the head against #810's head `084cf7a8`.** These figures are analytical, from the composed tables. They were not re-measured on this head's legs (the STOP).
- 1x1/1if load: 0.503 at the pin and 0.501 with tsn-c-stack#32 (≤ 0.70, `load_grade.py --check` rc 0). Base 0.501 / 0.499, so +0.002 / +0.002.
- 1x1/1if rows R4, R5 and R6: +0.56, +0.22 and +0.22 ms.
- 8x8/2if load: +0.001 in both columns. Rows R4, R5 and R6: +0.96, +0.30 and +0.28 ms.
- Queued notices and pass costs: unchanged.
- `flip_grade.py --check` exits 1 at both commits, with the same OVER set.

**Found, each for its own issue (neither caused by #905):**
- **srptx `[TIME]`, already present at #810's head.** Every scenario reports a "requested" transmit opportunity at each whole second, 400 to 800 ms after lwSRP's last idle poll: 47 findings on the licence scenario at `084cf7a8` and 45 here. So `make srptx` fails at #810's head already, and so must `srptx-plants`' controls and `srptx-mutants`' clean control there, which each require a capture with no finding (run here at this head, not at `084cf7a8`). The suite README's "no finding" was #867's head's.
- **srptx hold `[TX]`, since #895 (it appears at the merge and not at `084cf7a8`).** With the boot-time Talker Failed gone, the 3 s MAC hold no longer fills the SRP transmit ring: 176 MRPDUs and no refusal, where `084cf7a8` refuses a 30-word record at 507 of 512 words. The check's full-ring retention path is no longer exercised.

Receipts: the round's handoff and receipts index (manager-side). Nothing pushed; no PR edited. Round 2's pending manager duties are unchanged.
