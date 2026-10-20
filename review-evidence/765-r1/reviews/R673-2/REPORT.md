[R673] NEGATIVE - exact head d4a27e6334118c9eef1023aa27e9fd2b7de9f076

Internal cleared-context independent review, round R673-2, issue #765 / PR #769.

- Head `d4a27e6334118c9eef1023aa27e9fd2b7de9f076`, tree `a78b680bc9ffdbd43e25035ed8ece9e6b746d839`.
- Delta reviewed: `75db4b57..d4a27e63`, three commits: `059ecec1`, `11119970`, `d4a27e63`. This is round R673-1's head plus the round-2 answer.
- All five lenses were applied to the delta. The round-1 lens results were carried forward where the delta does not touch what they depend on.

This is a source review verdict. It is not merge authorization and not hardware qualification.

## Summary

Both round-1 findings are resolved at this head:
- **R673-1-F1:** the lockstep reference comment now states the current-format compare it sits above.
- **R673-1-F2, option (a):**
  - the four assigned locations and the PR's known limitations say that the flat test instrument keeps the family compare on purpose, and that the device listener rejects a channel-count mismatch;
  - `TEST_RESULTS.md` matches a fresh generator run byte for byte, apart from the timestamp.

The delta changes no SystemVerilog code token. The avtp_rxmon suite and the AAF campaign pass at this head in the reviewer's own runs.

One new MINOR finding (F1 below) keeps the verdict NEGATIVE. It comes from the wording the round itself introduced:
- The new texts say that the flat instrument accepts "any nonzero channel count" (in the AAF campaign section title, "any channel count").
- The flat instrument reads only the low eight bits of the 10-bit `channels_per_frame`. A reviewer probe shows that channel count 256 is rejected as UNSUPPORTED_FORMAT.
- The same section title also says the device listener rejects the probed counts, but it accepts the probe that matches its 8-channel format.
- The false statement is carried into the generated record `hdl/ieee1722/avtp/doc/TEST_RESULTS.md:29,96`. Under the owner rule that makes it MINOR, not RESIDUE.

## Findings

### R673-2-F1: MINOR | Docs, Tests, RTL

**Where:**
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:183-184`: "any nonzero channel count accepted".
- `tb/verilator/avtp_rxmon/sim_main.cpp:460-461`: the `[28]` banner says "any nonzero channel count is accepted here".
- `tb/verilator/tsn_fuzz/fuzz_aaf.py:143`: "accepts any nonzero channel count".
- `tb/verilator/tsn_fuzz/fuzz_aaf.py:176-177`: the docstring says "accepts any nonzero channels_per_frame; the device listener does not".
- `tb/verilator/tsn_fuzz/fuzz_aaf.py:178-179`: the section title "flat instrument family compare: any channel count accepted (the device listener rejects, #765)".
- That title is emitted into `hdl/ieee1722/avtp/doc/TEST_RESULTS.md:29` (summary row) and `:96` (section heading).
- The PR body's known limitations repeat "any nonzero channel count is accepted there", in the same paragraph that cites the generated record as saying so.

**Evidence:**
- **The flat instrument reads only the low eight bits.** `KL_avtp_rx_monitor.sv:178` declares `p_chans = fsh_i[47:40]`, and `:195` accepts on `p_chans != 8'd0`. It never reads the top two bits of the 10-bit `channels_per_frame`, `fsh_i[49:48]` (IEEE 1722-2016 7.3).
  - So a count of 256, 512 or 768 is rejected as if it were zero.
  - A count of 257 is accepted and reported as 1 channel on `wire_chans_o` (`:277`).
- **Probe.** `scripts/probe_flat_cpf256.sh` uses a disposable copy of the flat harness. It adds the top two bits to the stimulus and feeds two PDUs after `[28f]`. `receipts/probe_flat_cpf256.log` shows:
  - channel count 256: `frames_rx=3 unsupported=2`, so rejected and counted UNSUPPORTED_FORMAT;
  - channel count 257: `frames_rx=4 unsupported=2`, so accepted.
- **The section title overstates what the campaign measured.**
  - It says "any channel count accepted". The section probes only 1, 2, 3, 4 and 8 (`fuzz_aaf.py:180`).
  - Its parenthesis "(the device listener rejects, #765)" is wrong for the 8-channel probe. The campaign's format is 8 channels (`tb/verilator/tsn_fuzz/cosim_aaf.cpp:26`, `FMT[31:22] = 8`), and the device listener accepts a PDU that matches its current format.
- **It is in a generated artifact.** The text sits in a generated verification record and in a harness's console output, not only in a comment. Under the owner rule that rules out RESIDUE.

**Impact:**
- A reader of the instrument's contract, or of the record in the RTL folder, is told that the instrument accepts every nonzero 10-bit count. A test or campaign written on that basis fails, or passes for the wrong reason, at counts of 256 and above.
- The record also tells a reader that the device listener rejects every probed count, including the one it accepts.
- This is the text round 2 was assigned to make exact. The defect is small, but it states a width behaviour that the RTL does not have.

**Required outcome:** all six texts above, and the PR body, describe what the instrument does. For example:
- "a channel count whose low eight bits are nonzero (this instrument reads only channels_per_frame[7:0])"; or
- name the probed counts, for example "counts 1-8 accepted".

The parenthesis in the title says that the device listener rejects a count other than its current format's. `TEST_RESULTS.md` is regenerated through the campaign, not hand-edited.

Making the flat instrument read the full 10 bits is another valid outcome. That is a test-instrument RTL change, and the manager decides whether it belongs in this lane.

**Verification:**
- Read the listed lines at the fixing head.
- Run `make -C tb/verilator/tsn_fuzz aaf` with tsn-gen at `deca300c`: 164/0 and freshness PASS.
- Run `scripts/docs_check.py`: rc 0.
- Run the avtp_rxmon flat leg: 97/0.
- `scripts/probe_flat_cpf256.sh <repo> <scratch> <verilator>` gives a result that agrees with the new wording.

### R673-2-S1: SUGGESTION | Tests

**Where:** `tb/verilator/avtp_rxmon/sim_main.cpp:83,459`, the method `channel_freedom_accepts_every_count()`.

The `[28]` method's name still says "freedom" and "every count". That is the reading round 2 relabelled everywhere else in the file. The name predates the delta.

**Suggested change:** rename it with the F1 fix, for example to `flat_family_compare_accepts_other_counts`. No check changes.

### R673-2-N1: note, no finding

`tb/verilator/avtp_rxmon/sim_main.cpp:433` keeps "USER bug 6 repro" and "task #24". Commit `d4a27e63` rewrapped the comment around that line but did not change the line itself. These are inherited identifiers outside the comment rule's new-instance scope, and #746 tracks them.

The comment-rule scan of every line added in `75db4b57..d4a27e63` found none of the following: a lane label, lane name, review round, reviewer ID or issue-comment ID (`receipts/delta_comment_rule_scan.txt`, 0 matches). There is no RESIDUE in the source comments of the delta.

## Prior public findings at this head

These were read after this round's independent pass over the diff, and are resolved or retained as follows.

| prior finding | status at d4a27e63 | evidence |
|---|---|---|
| R673-1-F1 (MINOR) | **Resolved** | `KL_avtp_rx_monitor_ctx_ref.sv:493-501` now lists subtype, AAF format, nominal rate, bit depth and the full 10-bit `channels_per_frame` against the current format, nonzero, not sparse (#765; Milan v1.2 4.4.2.2, Table 5.6, Table 6.2). The comment matches the expression at `:502-509` term for term, and that expression matches the shipping `KL_avtp_rx_monitor_ctx.sv:522-528`. The "does not appear here" claim and the BAF v1.1 citation are gone. The code is unchanged (`receipts/sv_nocomment_delta.txt`). Lockstep N=1 116/0, N=8 119/0, `lockstep_mutants.py` 14/14 (`receipts/avtp_rxmon_make.log`). |
| R673-1-F2 (MINOR), option (a) | **Resolved as assigned.** F1 above is a new defect in the replacement wording, not a reopening of F2. | All four locations say the flat instrument keeps the family compare on purpose and the device listener rejects another count (#765, FR-STR-03): `KL_avtp_rx_monitor.sv:182-190`, `sim_main.cpp:460-463` (with `[10]` at `:246-248` and `[27]` at `:433-437`), `fuzz_aaf.py:141-149` and `:175-179`. None states the BAF v1.1 or "wire truth" reading as the listener's rule; the search is recorded under Docs. `TEST_RESULTS.md` was regenerated by the reviewer at this head, and the only difference from the committed file is the timestamp (`receipts/test_results_regen.diff`); freshness gate 1 PASS (`receipts/tsn_fuzz_aaf.log`). PR known limitations updated (`receipts/pr769_body_at_review.md`). |
| R673-1-S1, S2, S3 (SUGGESTION) | **Retained, optional.** They were not assigned, and the delta does not touch their artifacts. | Unchanged: `KL_avtp_rx_monitor_ctx.sv`, `tb/verilator/milan_dp/sim_main.cpp`. |
| R674-1-RES1 (RESIDUE) | **Resolved** | The PR body at review time contains 0 U+2014 characters (`receipts/pr769_body_at_review.md`). |

## Lens results

### Conformance: CLEAN

[R673] PASS Conformance - `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:497-528`; `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:493-509`; `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:182-190`; `fuzz_aaf.py:141-149`; `receipts/avtp_rxmon_make.log` ([UF], `format_mutants.py` 6/6) - every device-listener statement added by the delta was checked against the shipping compare, issue #765's clauses and FR-STR-03.

- **The claim is true of the shipping engine.** `KL_avtp_rx_monitor_ctx` compares the full 10-bit `channels_per_frame` with the current format's `[31:22]`. On a mismatch it counts UNSUPPORTED_FORMAT and gives no accept verdict, so the PDU is discarded. This is graded by `[UF2a-e]`, and `[UF3a]` covers a 264-channel PDU. The planted "family compare" and "low byte" mutants are each caught.
- **The citations are the issue's clauses.** Milan v1.2 4.4.2.2, Table 5.6 and Table 6.2 are the clauses #765 names.
- **The flat module is a test instrument.** By search, `milan_datapath.sv:6289` instantiates only `KL_avtp_rx_monitor_ctx`. The flat module is listed in the SoC source list, but nothing in `hdl/` instantiates it.
- **No clause misstatement remains.** F1 concerns the flat instrument's width behaviour, not a Milan clause.
- **Carried forward.** R673-1's acceptance-criteria evidence for the shipping engine and `KL_crf_rx` stands, because the delta changes no code (`receipts/sv_nocomment_delta.txt`).

### RTL: UNCLEAN (R673-2-F1)

[R673] PASS RTL (logic) - `receipts/sv_nocomment_delta.txt`; `receipts/delta_75db4b57_d4a27e63.diff` - with comments stripped and whitespace normalised, `KL_avtp_rx_monitor.sv` and `KL_avtp_rx_monitor_ctx_ref.sv` are token-identical at `75db4b57` and `d4a27e63`.

- No port, parameter, register-map or gitlink change. The six gitlinks are recorded in `receipts/clone_integrity.txt`.
- The route evidence that R673-1 examined at `75db4b57` stands for the logic.
- **The lens stays unclean because of F1.** The delta's new contract comment for the flat RTL module (`:183-184`) states a width behaviour the module does not have: it reads 8 bits of a 10-bit field.

### Robustness: CLEAN

[R673] PASS Robustness - `receipts/sv_nocomment_delta.txt`; `receipts/avtp_rxmon_make.log` ([UF2f-g], [UF3], [UF4], [UF5], `format_mutants.py` "low byte" mutant caught by [UF3a]); `receipts/probe_flat_cpf256.log` - the delta changes no reject, recovery, reset or boundary behaviour of the shipping engine.

- The shipping engine's 10-bit boundary is graded and mutation-tested at this head.
- The reviewer's boundary probe of the flat instrument confirms how it behaves: it rejects 256 and accepts 257. That behaviour is a property of the test instrument, inherited and not shipped. The defect is the delta's description of it, recorded as F1 under Docs, Tests and RTL.
- R673-1's Robustness result is carried forward.

### Tests: UNCLEAN (R673-2-F1)

[R673] PASS Tests (execution) - `receipts/avtp_rxmon_make.log`; `receipts/tsn_fuzz_aaf.log`; `receipts/test_results_regen.diff`; `receipts/author_r2_spotcheck.txt`.

- **avtp_rxmon at this head (reviewer run):** flat 97/0, NX 147/0, lockstep N=1 116/0, N=8 119/0, `lockstep_mutants.py` 14/14, `format_mutants.py` 6/6.
- **AAF campaign (reviewer run, tsn-gen built by the reviewer at `deca300c`):** 164 pass, 0 fail, 0 known gaps; freshness 1 PASS.
- **The regenerated record** differs from the committed file only in the timestamp.
- **No check changed.** The 20 count checks keep their expectations: the diff renames the labels and the method only.
- **Author receipts.** The published round-2 author receipts at `bf51200d` (`author-r2/receipts/r2-rxmon`, `r2-tsnfuzz`, `r2-builder`) carry head `d4a27e63` with rc 0, and their hashes match `MANIFEST.json`.
  - `r2-regen/rc` is 2. It records a pre-commit regeneration at `75db4b57` with an uncommitted worktree, not the exact head.
  - The exact-head runs (`r2-tsnfuzz`, and this reviewer's run) are rc 0.
- **The lens stays unclean because of F1.** The campaign's generated section title claims more than its five probes measure, and states the device listener's result wrongly for the matching probe. The `[28]` banner states a behaviour the probe falsifies at 256.

### Docs: UNCLEAN (R673-2-F1)

[R673] PASS Docs (other) - `receipts/docs_check.log` (0 findings across 210 md files); `receipts/delta_added_emdash.txt` (0 U+2014 added); `receipts/delta_comment_rule_scan.txt` (0 matches); PR body Round 2 table and known limitations against the head.

- The PR body's cited line ranges match the head: `:493-506`, `:182-190`, `:246-248`, `:433-437`, `:460-463`, `:141-149`, `:175-183` and `:491`.
- The commit messages are one line, with no trailers.
- `git diff --check 75db4b57 HEAD` is clean.
- **Search for the retired reading.** A repository-wide search for "wire truth", "channel freedom", "CHANNELS UNBOUNDED", "accept every format" and "USER 08-07", outside the history archive and the submodules, finds no text that presents the family reading as the listener's format rule. The remaining "wire truth" uses are about render or reporting paths: `KL_avtp_rx_monitor.sv:145`, `milan_datapath.sv:6251`, and the aaf modules.
- **The lens stays unclean because of F1** (the comment, the generated record and the PR text).

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `KL_avtp_rx_monitor_ctx.sv:497-528`; `KL_avtp_rx_monitor_ctx_ref.sv:493-509`; `KL_avtp_rx_monitor.sv:182-190`; `fuzz_aaf.py:141-179`; `milan_datapath.sv:6289`; `receipts/avtp_rxmon_make.log` | R673-2 | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| RTL | UNCLEAN (R673-2-F1) | `receipts/sv_nocomment_delta.txt`; `receipts/delta_75db4b57_d4a27e63.diff`; `KL_avtp_rx_monitor.sv:178,183-195,277`; `receipts/clone_integrity.txt` | R673-2 | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| Robustness | CLEAN | `receipts/avtp_rxmon_make.log` ([UF2f-g], [UF3]-[UF5], format mutants); `receipts/probe_flat_cpf256.log`; `receipts/sv_nocomment_delta.txt` | R673-2 | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| Tests | UNCLEAN (R673-2-F1) | `receipts/avtp_rxmon_make.log`; `receipts/tsn_fuzz_aaf.log`; `receipts/test_results_regen.diff`; `receipts/author_r2_spotcheck.txt`; `sim_main.cpp:243-262,430-482`; `fuzz_aaf.py:136-192` | R673-2 | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |
| Docs | UNCLEAN (R673-2-F1) | `receipts/docs_check.log`; `receipts/delta_added_emdash.txt`; `receipts/delta_comment_rule_scan.txt`; `receipts/pr769_body_at_review.md`; `hdl/ieee1722/avtp/doc/TEST_RESULTS.md` | R673-2 | d4a27e6334118c9eef1023aa27e9fd2b7de9f076 |

## Real limits of this round

**Not run by this reviewer:**
- Vivado route-1x1 and the resource gate;
- Yosys and xvlog;
- the full suite sweep, crf_rx, milan_dp, the builder bank, `make dynmap-mutants`.

None of these was needed: the delta changes no logic token. The author's round-1c figures at `75db4b57` stand for them, and the r2-builder receipts were checked by hash only.

**Em-dash gate:** `scripts/check_em_dash.py --base 75db4b57c` could not judge, because the pinned Markdown renderer is not installed (`receipts/check_em_dash.log`, rc 2). A direct search of the delta's added lines found 0 U+2014.

**Hosted CI:** a snapshot at review time is in `receipts/hosted_checks_snapshot.tsv`. Most exact-head contexts were queued or in progress, a few had passed, and Physical gPTP was skipped. No hosted acceptance is claimed, and skipped contexts are not counted as executed.

**Evidence context:**
- No manager source bank exists at this head, and none is inferred.
- Physical calibration NOT RUN. No hardware or field proof is claimed.
- The other reviewer's round-2 report was not read.

**Probe hygiene:**
- Probes and the tsn-gen build ran in copies under this packet's scratch area.
- The in-clone avtp_rxmon and tsn_fuzz runs left only ignored build directories, which were removed. The one tracked file the campaign rewrote, `TEST_RESULTS.md`, was restored from HEAD.
- After restoration: the worktree and index equal HEAD, `git write-tree` equals tree `a78b680b`, there are 0 ignored or untracked entries, and the six submodule gitlinks are unchanged (`receipts/clone_integrity.txt`).

## Pending manager duties

- **Merge candidate:** build and validate the current-dev merge candidate at the merge turn. Live dev is `78ca9bdf`.
- **Hosted acceptance:** own hosted and replica acceptance (`rtl-fast`, and exact-head `verilator-suites` and `yosys-portability`).
- **Fixing round:** assign the F1 wording correction and the regenerated `TEST_RESULTS.md`. Re-cover RTL, Tests and Docs at the fixing head, plus Conformance if that head touches the device-listener statements.
- **Optional:** S1 here, and R673-1 S1-S3.
- **New issues:** file the work the lane recommended:
  - the pruned 1x1 short-frame depacketizer window;
  - inputs above 0 read their current format only from LCTX w2/w3;
  - optionally, whether the flat instrument should read the full 10-bit `channels_per_frame`.

R673-2 FINISHED
