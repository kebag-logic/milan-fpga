# 74-a207 handoff: #74 item 2 / PR #528, Docs-only follow-up

- Role: [A207], author. Assignment: issuecomment-5797374041.
- Lane: `$LANES/74-junction-chatter`, branch `74-junction-chatter`.
- Base head: `553edeb86b9144f7b15721255fbe5ad11ef1fe36`.
- New head: `2accfadfd3d4d8a318e3e714ee0dc87fc84e4164`, one commit. It is
  **not pushed**. No PR edit and no merge.

## Findings answered

These are R262-1 F2 and R263-1 F1, the same MINOR (Docs).

- **Passage law.** `docs/reference/REGISTER_MAP.md` `SLIP_TDM` paragraph:
  - The NET count (dups minus skips) is the slip count, +1 slow and -1 fast,
    from the first frame on and below the ceiling.
  - Each half is exact only while the marker dithers over two adjacent cycles,
    which is what [G9] grades with no jitter.
  - A wider dither, such as the 1-edge FIFO jitter model, adds balanced pairs.
- **INTERNAL reading row** and **ceiling row:** made consistent with the
  passage law (the net count at 0.51/s; 35.6 h holds at one dup per slip).
- **Lock clearance:**
  - The paragraph now states the clamp `[K, DIV_C-K]`, with the default
    K = `DIV_C/128` = 16 cycles at 100 MHz, just under 1/128 sample.
  - The marker dithers around that target, and [G7]/[G8] grade a floor of 12
    cycles.
  - The "at least 1/128 sample" claim is gone.
- **Aligner banner:** `hdl/ieee1722/crf/KL_media_grid_align.sv:84-89`.
  - The clearance sentence now carries the same claim.
  - The edit is COMMENT-ONLY: the one hunk sits inside the `/* */` banner,
    and `verilator -E -P` output of the old and new file is byte-identical
    (sha256 `e3a16b18...79a9`).

## Deliberately untouched

- **Checked and passed by both reviewers:**
  - the `TIME_SYNC.md` lock-target row;
  - the `KL_chan_map_capture.sv:502-515` banner.
- **Optional suggestions not taken:**
  - R262 S1 (an acquisition note);
  - CHANGELOG (R262 S2, R263 S4);
  - test suggestions (R262 S3, R263 S1-S3).
- **O1/O2:** a manager decision (new Issues).

## Gates at the new head (all rc 0)

- `docs_check`, `check_doc_style`, `gen_toc --check`,
  `gen_toc --verify-anchors`;
- `check_em_dash --base ede8d48e` (0 findings over 54 added lines);
- `gen_module_matrix --check`;
- `git diff --check` (base..HEAD and HEAD~1..HEAD).

## For the manager and the reviewers

- **Push.** Push `2accfadf` to PR #528. Hosted contexts rerun on that head;
  the `.sv` path may retrigger RTL workflows.
- **Lens scope.** R262 and R263 re-cover Docs at `2accfadf`.
  - Whether a comment-only banner edit disturbs the four lenses banked at
    `553edeb8` is the reviewers' call.
  - R263's Conformance artifact listed `KL_media_grid_align.sv:72-86`.
