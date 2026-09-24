# [A230] handoff: #536 / PR #543, correction round 1

## State

- Lane: `$LANES/536-aecp-model-mvu`, branch `536-aecp-model-mvu`.
- Round start head: `612db13c244335b0fa3467d02ebab1c350b01990` (the head
  R280-1 and R281-1 reviewed). Base `dev`
  `26d855a9176d63625e6635a029a0c44e3d57ce9a`.
- New head: **`fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad`**, tree
  `24a2b1c9bd657d2d14b5e814f18ec349108ffc1f`. Worktree clean.
- Public comment: `[A230] REVIEW READY` on #536,
  https://github.com/kebag-logic/milan-fpga/issues/536#issuecomment-5806421639
- **Not pushed; the PR is not edited.** Both were outside this assignment.
  PR #543 still shows `612db13c2`.
- Submodules untouched and at their pins: `protocol-processor`
  `424c688fa2205b934a7689a58f2aa766420f2326`, `gptp-processor`
  `c1b617435824929a790739ea8585c3fe1a328cc0`. No RTL, processor, firmware or
  gitlink change (`gates.log`, the empty `git diff --stat` over those paths).
- Commits this round (one-line subjects, no bodies, no trailers):

| Commit | Finding | Subject |
|---|---|---|
| `8179587eea475cc1d994589c31d9ad4447a15571` | F2 | Send each Milan MVU command row in its own figure, so SET_SYSTEM_UNIQUE_ID is echoed at cdl 28 and SET_MEDIA_CLOCK_REFERENCE_INFO at cdl 92 (#536) |
| `3753b57494e8aec8bcc47c8bc8cfd2093456fe2e` | F1 | Grade each protocol_id octet, an over-length GET_MILAN_INFO and every other command message_type against the MVU sub-decode (#536) |
| `bfe2e5c797b6abcf3900aee5585650cb47977729` | F3 | Cite IEEE 1722.1-2021 9.6 and Table 9-6 for the MVU NOT_IMPLEMENTED status, and Section 4.2.4 for the protocol_version quotation (#536) |
| `fb84de54ee9c1e3a2b51d2a239efbc04e4a22bad` | F1 | Move protocol_id octet @26 one nibble at a time, where Milan 5.4.3.2.1 ends the OUI-36 and starts the MVU protocol id (#536) |

## Per-finding resolution

R280-1 and R281-1 found the same three defects; R281-1 also retained
R280-F3(a). All are MINOR.

| Finding | Lenses (as filed) | What changed | Where | Failing arm |
|---|---|---|---|---|
| R280-F1 = R281-F1 | Tests, Robustness | The guard outline gains one row per protocol_id octet @22 to @27 (pp_top M8's `FF` values) and one per nibble of @26 (`D1`: OUI-36 `...0A-D`; `C2`: protocol id `0x200`), all echoed; GET_MILAN_INFO at cdl 24 and cdl 112, both served (status 0, cdl 32, Figure 5.4 body). A new outline sends the served GET_MILAN_INFO frame with only its message_type changed, to 0, 2, 4, 8, 10, 12 and 14, each echoed NOT_IMPLEMENTED under its own type at cdl 20. The feature comment states the four comparison terms, the nibble boundary, and that the length is a floor. | feature :156-225; steps `step_send_mvu_shaped` (a cdl past 20 carries that many more octets), `step_send_mvu_bytes_other_type` | `mutations.log`: each octet's comparison dropped fails exactly that row; @26 cut to either nibble fails exactly the other nibble's row; each extra message_type accepted fails exactly its row; the exact length guard fails cdl 24 and 112; a cap at Figure 5.3 plus 4 fails cdl 112 only. `r280_arms_rerun.log`: R1 to R5 red. `r281_arms_rerun.log`: `mt_guard_dropped`, `len_exact_20`, `pid_head_22_23_dropped`, `pid_24_25_dropped`, `pid_26_dropped`, `pid_only_27` killed. |
| R280-F2 = R281-F2 | Conformance, Tests, Robustness | `MVU_COMMAND_FORMS` (model) gives each Table 5.18 command its own figure: `0x0000` and `0x0002` Figure 5.3, `0x0001` Figure 5.5 (system_unique_id `0x0102030405060708`, non-zero per 5.4.4.2), `0x0003` Figure 5.6 (flags `0x03`, default_mcr_prio 0, user_mcr_prio `0x80`, reserved quadlet, name "DEFAULT" zero padded to 64), `0x0004` Figure 5.7 (clock_domain_index 0). The rows carry a `form` column and cdl 28, 20, 92, 20; the step refuses a row whose figure is not the command's. `build_mvu_command` gains `from_32`. | model :660-696; steps `step_send_mvu` (:390); feature :116-139, :151 | R280 R10 and "the MVU echo capped at 8 payload octets" each fail exactly rows `0x0001` and `0x0003`; either form truncated, either cdl cell set back to 20, and a wrong figure name each fail exactly their row. |
| R280-F3(a), retained by R281-1 | Conformance, Docs | The MVU block cites Milan Table 5.19 and IEEE 1722.1-2021 Table 9-6 for the status, quotes 9.6.5.3.1 ("the appropriate details from the command and an appropriate status code"), says no clause sizes an MVU refusal and the command-length echo is the engine's choice, and names 9.3.5.3.3 as the AEM rule. The steps header gains the IEEE 9.6 entry. | feature :104-110; steps header :84-98 | Text. Checked against the Milan v1.2 and IEEE 1722.1-2021 PDFs in `$WORKSPACE_HOME/standards` (9.3.5.3.3 is the AEM processCommand; 9.6.2.3 Table 9-6; 9.6.5.3.1). |
| R280-F3(b) = R281-F3 | Conformance, Docs (R281: Docs, Conformance) | The model comment quotes 5.4.4.1 ("The value of this field is 1") and attributes "A PAAD shall set the value of the protocol_version field in the GET_MILAN_INFO response to 1" to Section 4.2.4. The feature comment cites both. | model :81-84; feature :143 | Text, same check. |

Not taken (optional, no effect on coverage): R280-S1 (the MVU gate regex
fails open on a `[14:0]` or `16'd` declaration), R280-S2 (`SERVED_MVU` vs the
ledger's `served_mvu_operations`, which needs `scripts/`). Out of scope and
left: R280-O1 = R281-S1 (the stale "NOTE ON THE DECODE", present at base),
R280-O2 (the dated 312 total in `tests/README.md`), R280-O3 (the 5.4.4.1 NOTE).
O1 is a candidate for its own Issue.

## What the model change is, and is not

`git diff 612db13c2 fb84de54e -- tests/steps/aecp_engine_model.py` touches
only the protocol_version comment, `build_mvu_command` (the `from_32`
parameter) and the new `MVU_COMMAND_FORMS` table. The mirror of the engine
(`deliver`, `_mvu_command_type`, `_mvu_program`, `_assemble`) is byte for
byte what R280-1 and R281-1 executed against the RTL. Every anchor both
reviewers' mutation scripts use still matches exactly once.

## Evidence (all at `fb84de54e`, in this packet)

- `gates.log`: full behave **14 features / 343 scenarios / 1736 steps
  passed** (round start 14 / 326 / 1600); contract feature 59 / 435 (round
  start 42 / 299); `check_py_idiom` exit 0 at
  its ratchets (long function 9, long module 10, too many parameters 7);
  `docs_check` 0 findings; `check_feature_status` 0 findings;
  `check_em_dash --base 26d855a9` 0 findings over 2 added lines;
  `git diff --check 26d855a9 HEAD` clean; worktree clean.
- `mutations.py` / `mutations.log`: 40 arms on a disposable copy of `tests/`
  (the lane is never written), each required to fail exactly its expected
  scenarios by feature line: **40 of 40 RED-EXACT**, both controls green,
  lane worktree clean afterwards.
- `r280_arms_rerun.log`: R280-1's `r280_mutations.py`, unmodified: R1 to R8,
  R10, R11 red; R9 survives, the equivalent mutant R280-1 already classified.
- `r281_arms_rerun.log`: R281-1's `mutate_model.py`, unmodified: baseline
  green, all nine arms killed.
- `xcheck_rows_vs_rtl.py` / `xcheck_rows_vs_rtl.log`: each of the 26 new or
  changed rows is built as its step builds it and matched (message_type, cdl,
  every octet from @22 to the end of the payload) against the frames the
  pinned RTL answered in the R280-1 and R281-1 receipts, using only frames
  addressed to the bench's own entity; the head model is then fed each
  matched receipt frame. **23 rows match an RTL-answered frame, and the model
  equals the RTL on every one (0 mismatches).** Three rows have no executed
  frame: `00-1B-C5-0A-D1-00` and `00-1B-C5-0A-C2-00` (the engine compares @26
  as one byte, `KL_aecp_engine.sv:3193`, so any value but `C1` is refused;
  not executed) and cdl 24 (differs from R281-1 `x_overlong_cdl24` only at
  @33..@35, fill octets past Figure 5.3 that the sub-decode does not read).

Reproduce from the lane root (`<ev>` is `review-evidence/536-r1` from
`origin/536-review-evidence`, `<scratch>` any empty directory):

```sh
python3 -B <packet>/mutations.py . <scratch>
PYTHONDONTWRITEBYTECODE=1 python3 -B <ev>/reviews/R280-1/scripts/r280_mutations.py . <scratch>/r280
python3 -B <ev>/reviews/R281-1/scripts/mutate_model.py --clone . --scratch <scratch>/r281 --out <scratch>/r281.log
python3 -B <packet>/xcheck_rows_vs_rtl.py . <ev>
```

## Things a reviewer should know

- `mutations.py` hard-codes the feature line of each row at `fb84de54e`; a
  later edit to the feature above line 233 moves them.
- The step `the controller sends Milan MVU command_type {word} to the AECP
  engine` is gone: the form-carrying step replaces it, and keeping both would
  make behave's parse matcher ambiguous. Nothing else used it.
- The Figure 5.6 and 5.7 rows address clock domain 0, the one CLOCK_DOMAIN
  of the 8-descriptor image. The `0x0004` Figure 5.7 frame is byte-identical
  to the previous Figure 5.3-shaped `0x0004` frame (clock_domain_index sits
  where reserved was, both 0), which is why its row changed only its label.
- The message_type 0 row puts `0x001B` (DECREMENT_CONTROL, IEEE Table 7-125)
  in the AEM command_type field. It is not served; the whole-opcode sweep
  already asserts NOT_IMPLEMENTED for it, so a future pin serving it would
  turn both red together.
- Ignored `__pycache__` directories exist in the lane (`tests/steps`,
  `avdecc`, `sw/builder`, `sw/litex/platforms`, `tb/tools`). They date from
  01:59, before this round started at 04:16; every command here ran with
  `-B` / `PYTHONDONTWRITEBYTECODE=1`, and they were left as found.
- The Milan v1.2 and IEEE 1722.1-2021 texts were read this round (local
  reference copies in `$WORKSPACE_HOME/standards`, not republished).

## Lens notes for the re-review

- RTL: no RTL, processor or gitlink change; the model's mirror is unchanged
  (see above). The changed model artifacts are the command builder and a
  comment.
- Conformance, Robustness, Tests, Docs: every changed artifact is in the
  three test files and `tests/README.md:90`; `docs/MILAN_V12_ROADMAP.md` is
  unchanged this round.

## Next steps for the lane owner

1. Push `536-aecp-model-mvu` (`fb84de54e`) to PR #543 and replace the PR body
   with `PR-BODY.md`.
2. Publish this packet beside the round-1 evidence.
3. Run the local workflow replica from a clean trusted `dev` worktree
   (`python3 -I <trusted-dev>/scripts/act_ci.py --pr 543`) and collect the
   hosted runs at the new head.
4. Route the re-review to R280 and R281 at `fb84de54e`.
