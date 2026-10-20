[R673] NEGATIVE - exact head 75db4b57cff47bb614d14dead084649a4c2aa2a3

# R673-1: internal cleared-context review of PR #769 (Closes #765, Relates to #762)

- Head `75db4b57cff47bb614d14dead084649a4c2aa2a3`, tree `f974f88ec16ad996db74419f368fd247f6883813` (verified in the review clone, `receipts/clone_integrity.txt`).
- History: the lane's three commits (`31903ec1`, `91aaa6bd`, `cc71db3a`), the merge of PR #767's round-2b head (`2f33a9ce`), `4605409b`, the merge of dev `78ca9bdf` (`7f84892a`, parents `4605409b` and `78ca9bdf`), and `75db4b57`. Nothing is rewritten, and every commit message is one line (`receipts/ancestry_and_rtl_scope.txt`).
- The live remote `dev` read `78ca9bdf104819265588726bce4322696c38b8c2` during this review, an ancestor of the head. Against it, the lane's RTL delta is `KL_avtp_rx_monitor_ctx.sv` (+19/-12) and `KL_crf_rx.sv` (+9/-4). `milan_datapath.sv` is byte-identical to dev.
- Reconstructed from:
  - AGENTS.md, CONTRIBUTING.md (by reference) and docs/README;
  - the #765 issue body, the assignment, the round-1 STOP ruling (issuecomment-6268149013), the round-1c assignment (issuecomment-6292906653) and both REVIEW READY comments;
  - the PR body;
  - `git diff 4191b098..75db4b57` and `git diff 78ca9bdf..75db4b57`;
  - the public evidence tree `94c54c2b:review-evidence/765-r1` (round-1c receipts).
- Prior public review findings on PR #769: none existed when this round started. The PR had 0 reviews, 0 review comments, and its only issue comment was the review-start notice. There is nothing to resolve or retain.

## Verdict

NEGATIVE. The shipped behaviour is right, and every executable claim I re-ran held:
- both engines count and discard a PDU whose subtype or channel count differs from the current format;
- #762's stopped-input rules are byte-identical to dev;
- the `[762-DP]` case keeps its meaning, and its wiring plant is still caught;
- the resource gate passes on the public receipts;
- no port, parameter or register-layout change.

Two MINOR findings remain open, so the verdict is NEGATIVE. Both concern prose that still states the superseded "every channel count of the family" reading as the rule, which #765 retires:
- F1 is in the reviewed delta: a comment now contradicts the code directly under it.
- F2 is in the flat test instrument and its campaigns, which the PR left in place.

Neither is RESIDUE. Each one cites a deprecated clause as the governing rule (a clause claim), and F2 also covers a generated verification record.

## Findings

### F1: MINOR | Docs, Tests, Conformance

**Where:** `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:493-501`. The lockstep reference's format-compare comment contradicts the compare beneath it.

**Evidence:**
- The comment block still reads "reference aaf_pdu_format_matches, FAMILY compare (Milan BAF v1.1 Section 4 + USER 08-07 ...) ... the configured format is the NOMINAL selection, never an acceptance bound, so the wire's channels_per_frame does not appear here at all".
- This PR inserted `(p_cpf_w == f_cpf_w)` and `(p_cpf_w != 10'd0)` at `:506-509`, in the same expression, five lines below.
- The comment also cites the Base Audio Formats v1.1 reading as the basis. #765 records that reading as deprecated (Milan v1.0 Table 1.2) and replaced by Milan v1.2 4.4.2.2, Table 5.6 and Table 6.2. The engine's own comment was corrected (`hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:512-521`); this copy was not.

**Impact:** a reader of the lockstep oracle is told that the channel count is not compared and that a deprecated clause governs, in a file this PR edited. That is the reading the issue's "Source" paragraph asked to retire.

**Required outcome:** the comment says what the lines below it compare: the current format including the 10-bit channel count, on the Milan v1.2 4.4.2.2 / Table 5.6 / Table 6.2 basis (#765). Alternatively it says plainly that the family reading of dev `e8454e27` is superseded for these lines. It no longer says channels_per_frame "does not appear here".

**Verification:** read `:493-509` at the fixing head; `scripts/docs_check.py` rc 0; avtp_rxmon lockstep N=1 116/0 and N=8 119/0; `lockstep_mutants.py` 14/14.

### F2: MINOR | Docs, Tests, Conformance

**Where:** the flat instrument's comment, its avtp_rxmon case banner, the tsn_fuzz AAF campaign's rationale and the generated record in the RTL folder still present the superseded reading as the listener's Milan rule.

**Evidence:**
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor.sv:182-187` reads "CHANNELS UNBOUNDED (Milan BAF v1.1 Section 4 + USER 08-07 ...) - a Base Listener supports ALL channel counts of its rate family, so the configured format never bounds acceptance".
- `tb/verilator/avtp_rxmon/sim_main.cpp:458-459` has the `[28]` banner "channel FREEDOM (Milan BAF Section 4 + USER 08-07: accept EVERY channel count ...)".
- `tb/verilator/tsn_fuzz/fuzz_aaf.py:141-148` and `:174-176` read "the listener follows WIRE TRUTH for the channel count rather than rejecting a PDU that disagrees with the bound format's declared channels". Its section "wire-truth channel count (declared-vs-wire mismatch)" grades 20 checks such as "channels_per_frame=N: accepted (wire truth)" and "not flagged unsupported".
- That section is published as passing in `hdl/ieee1722/avtp/doc/TEST_RESULTS.md:29,96-120`, a file "written into the folder of the RTL it validates".
- After #765 the device listener does the opposite: `KL_avtp_rx_monitor_ctx.sv:526`, FR-STR-03, and the new 4.4.2.2 row of the compliance matrix.
- The PR's known limitations disclose that the flat instrument "keeps no channel compare". They do not disclose that its comment, its `[28]` case and the tsn_fuzz campaign (cited in the PR as "AAF/AVTP 164/0") state that behaviour as Milan-conformant listener behaviour.

**Impact:** the tree carries two contradictory statements of the same Milan rule. The one sitting next to the shipped engine, in the same folder, and the one in a passing verification record both say a channel-count mismatch must be accepted. A cold reader or a future change can restore the retired reading on that authority.

**Required outcome:** at the fixing head, these texts no longer present the BAF v1.1 / "wire truth" reading as the listener's rule. Either:
- (a) they state that the flat test instrument keeps the family compare on purpose, that the device listener rejects a channel-count mismatch (#765; Milan v1.2 4.4.2.2, Table 5.6, Table 6.2), and the generated record is regenerated from the corrected campaign text; or
- (b) the flat instrument and its campaigns adopt the current-format compare.

Moving this to another Issue does not resolve it.

**Verification:** read the four locations at the fixing head; tsn_fuzz with tsn-gen at the CI pin, AAF/AVTP all pass and `TEST_RESULTS.md` regenerated rather than hand-edited; avtp_rxmon flat leg 97/0 (or its updated count); docs gates rc 0.

### S1: SUGGESTION | Tests

**Where:** `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:522`. The AAF engine's subtype term has no engine-level check that can fail.

**Evidence:**
- Planting `wire fmt_ok_w = 1'b1 && ...` (the subtype term dropped, `receipts/unit-probes/rxm_nosubtype.diff`) leaves the N=4 harness at 147 checks, 0 failures.
- The lockstep harness drives `subtype_i = 0x02` only (`tb/verilator/avtp_rxmon/sim_lockstep.cpp:275`).
- By search, no milan_dp stimulus puts a non-AAF subtype on an AAF input's stream_id.
- Only the flat instrument's `sim_main.cpp:252` tests that case.

**Status:** this term predates the lane, and the frozen case list does not name it. A `[UF]` case with a CRF-subtype PDU on an AAF input's stream_id, plus its mutant, would give acceptance criterion 1 executable evidence on the shipped engine for subtypes too.

### S2: SUGGESTION | Tests

**Where:** `KL_avtp_rx_monitor_ctx.sv:521,527`. The zero-count term is untested on the engine.

**Evidence:** dropping `(p_cpf_w != 10'd0)` (`receipts/unit-probes/rxm_nozero.diff`) survives the N=4 harness, 147/0. The comment's claim "rejected even against itself" has no check.

**Status:** reachable only with a zero-count current format.

### S3: SUGGESTION | Tests

**Where:** `tb/verilator/milan_dp/sim_main.cpp:1252-1254,1371,1531`. On the shipping AX 1x1 leg the acceptance-gate PDU is not a whole-frame PDU.

**Evidence:**
- `mkaaf` now writes the declared count (8 on `endstation_ax7101_1x1_tdm8`) but keeps `stream_data_length` 48, which is 1.5 sample frames at 8 channels.
- The check keeps its name "a conformant PDU is ACCEPTED".
- The code comment at `:1229-1232` discloses this, and the gate's subject (the header compare) is kept: 233/0 on the leg.
- At `:1531` the rebase comment "the 2ch default now ACCEPTS the bisect probes above" is no longer true on that leg: `[wire86] FRX delta=0 UNSUP 0x0->0x200` in `receipts/milandp_pool.log`. That line is printf only, with no check.

**Status:** make the length `24 * kIn0ChansTb` as `sim_nxn.cpp` does, or name the check for what it grades.

No RESIDUE: the comment rule (no lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs in source comments) was searched over every added source line of `78ca9bdf..75db4b57` (hdl, tb, scripts, sw), and there were no matches.

## Lens results (all five applied at 75db4b57)

### Conformance: UNCLEAN (F1, F2 open)

The shipped behaviour conforms, by source reading and by test.

**AAF input:**
- `KL_avtp_rx_monitor_ctx.sv:497-528` reads the current format's channels_per_frame at `[31:22]` (IEEE 1722-2016 I.2.4 layout: subtype `[63:56]`, nsr `[51:48]`, format `[47:40]`, depth `[39:32]`) and the PDU's full 10-bit field at `fsh[49:40]` (7.3 Figure 26).
- A mismatch sets only the UNSUPPORTED_FORMAT interval flag (`:592-594`). It has no accept pulse (`:1001-1007`), so nothing is emitted (4.4.2.2) and UNSUPPORTED_FORMAT counts once per interval (Table 5.6).
- `[UF1a-5e]` pass, including a 264-channel PDU and both format paths (LCTX and `fmt0_i`).

**CRF input:**
- `KL_crf_rx.sv:323-335,370,393` makes any stream subtype on the sid a hit; a non-CRF subtype is not `w_fmt_ok` and counts `w_ev_uf_w`.
- The parser pulses only subtypes up to 0x07 with sv=1 and version 0 (`avtp_stream_parser.sv:185,202-208`), so the comment's premise holds.
- `[FMT-a1..c2]` pass.

**Spec and docs:** the FR-STR-03 text and status row, the 4.4.2.2 compliance row and `CRF_STATUS[15:8]` match the RTL.

**Open:** F1 and F2 misstate the governing clause in the tree.

### RTL: CLEAN

Covering round R673-1, head 75db4b57. Artifacts and checks:

- `KL_avtp_rx_monitor_ctx.sv:497-528`, `:934-1034` (format load: `fmt0_i` alias for stream 0, LCTX w2/w3 otherwise):
  - widths are 10 against 10;
  - no new state, FSM state or port;
  - the 8-bit `wire_chans` path is unchanged and updates only on accept.
- `KL_crf_rx.sv:323-335,370-406,587-636`: the widened hit adds one equality to the format term.
- Stop gating is unchanged on both engines:
  - `:1029-1033` and `KL_crf_rx.sv:373,406,564` are byte-identical to dev (`receipts/rtl_delta_vs_dev.diff`);
  - a reject never reaches `w_acc`, the accept branch or `sil_ms_r`, so it cannot reach the stop-gated interruption events.
- `milan_datapath.sv` is identical to dev, including `.stopped_i` at `:6308`.
- No added or removed port, parameter or localparam declaration (`receipts/interface_scope.txt`; its only pattern hits are comment words).
- Public route receipts at this head (`round1c/route/head-75db4b57`):
  - `commit.txt` = 75db4b57;
  - fully routed, 0 routing errors;
  - WNS +0.137 ns, WHS +0.024 ns;
  - `pp_resource_gate.py check --endpoint route-1x1`: RESULT PASS, LUT 49,857 against 49,613 (+244, tolerance 500);
  - `avtp_rx_monitor` 697 LUT, `crf_rx` 282 LUT (hierarchical place report).

### Robustness: CLEAN

Covering round R673-1, head 75db4b57.

**CRF reject path.** I planted my own mutants, each caught by the named check:
- a CRF format reject that drops the lock fails `[FMT-b2]` (`receipts/unit-probes/crf_lockdrop.diff`);
- a CRF reject that advances the sequence cursor fails `[FMT-c1]` (`crf_seqadv.diff`).

**AAF reject path:**
- the sequence is unmoved (`[UF2f]`/`[UF2g]`);
- the high channels_per_frame bits are compared (`[UF3]`);
- the current format follows a controller's change (`[UF4]`, `[UF5d]`).

**Code paths read:**
- a stopped input still counts a reject (`w_hit` and `iv_events` are not stop-gated, per 5.3.8.10);
- an unbound CRF sink ignores everything (`en_i`);
- a reject does not refresh either silence watchdog;
- there is no new reset-sensitive state.

**Limitations (disclosed, predating the lane, not opened here):**
- inputs above 0 take their format only from LCTX w2/w3, and no firmware writes them (`milan_datapath.sv:6329`);
- the pruned 1x1 short-frame depacketizer window.

### Tests: UNCLEAN (F1, F2 open)

Everything here was re-run by this round with the pinned Verilator 5.050 (identity printed in the logs), in clean copies of the head.

**avtp_rxmon** (`receipts/rxmon.log`), rc 0:
- flat 97/0, NX 147/0, lockstep N=1 116/0 and N=8 119/0;
- `lockstep_mutants.py` 14/14;
- `format_mutants.py` 6/6: each of the five plants fails its named `[UF]` check, and the clean control passes.

**crf_rx** (`receipts/crfrx.log`), rc 0:
- unit 15,379/0, discontinuity 2,201/0, talker_step 69/0;
- `mutants.py` 21/21, with `aaf_ignored` failing `[FMT-b3]`, `aaf_accepted` failing `[FMT-b1]` and `crf_rejected` failing `[FMT-a1]`.

**milan_dp prefix legs** (`receipts/milandp.log`):
- gptp 182/182 and gptp-lat 182/182;
- counters-1, -8, -1-frames and -8-frames all RESULT PASS.

**milan_dp ordinary legs** (`receipts/milandp_pool.log`), all failures 0, sim_pool rc 0:

| Leg | Checks |
|---|---|
| base | 236 |
| notify | 424 |
| crflic | 416 |
| dynmap | 201 |
| nxn | 1983 |
| nxndv | 1985 |
| nxn8 | 3767 |
| nxn4c | 1983 |
| nolpf | 236 |
| prune | 33 |
| ax1x1 | 233 |
| aclk | 193 |

- `render_mutants` 6/6.
- `unb-mutants` (`receipts/unbmut.log`): 6/6, rc 0.
- The first `make run` exited 2 only because this round passed `SIM_JOBS=6` and `sim_pool` refused it (ceiling 2). Every leg had already built; the pool was re-run at 2.

**`[762-DP]`:**
- Each of the five legs that run it logs input 0's current format: dynmap 8, nxn 4, nxndv 4, nxn8 8, nxn4c 4.
- The dynmap block reads:
  - stopped gap: SEQ_NUM_MISMATCH +1, STREAM_INTERRUPTED +0;
  - stopped silence: MEDIA_UNLOCKED +1, STREAM_INTERRUPTED +0;
  - after START: MEDIA_LOCKED +1, SEQ_NUM_MISMATCH +1, STREAM_INTERRUPTED +1.
- `75db4b57` changes only the stimulus lines; no check or expectation changed.

**Probes** (`receipts/dp-probes`):
- dev's fixed 2-channel stimulus put back (`dp6_stim2ch.diff`) fails exactly 4 `[762-DP]` checks on dynmap (201/4) and nxn4c (1983/4). The current-format stimulus is load-bearing.
- #762's tie-off plant at `.stopped_i` (`dp7_tie0.diff`) fails exactly "[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0" and "[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0" on dynmap.
- The public receipt `round1c/dp762-mutants/SUMMARY.tsv` records all three plants on both legs, and agrees.

**Open:**
- F1 (the oracle's stated contract contradicts it);
- F2 (a passing campaign grades the retired rule as listener behaviour).

S1, S2 and S3 are optional.

### Docs: UNCLEAN (F1, F2 open)

**Checked and accurate:**
- `docs/reference/FR_NFR.md:172,271`;
- `docs/reference/MILAN_COMPLIANCE_MATRIX.md:190`;
- `docs/reference/REGISTER_MAP.md:861`;
- `docs/design/MEDIA_CLOCK_FOLLOWING.md:315,458-459` (line references `:497-528` and `:512-528` checked);
- `docs/testing/TESTING.md` (avtp_rxmon and crf_rx rows);
- `tb/verilator/milan_dp/README.md:1199-1201`;
- `scripts/measure_test_evidence_readers.py`;
- the PR body's figures (LUT and timing, mutant tallies, leg counts and the five `[762-DP]` legs), against the receipts above.

**Gates** (`receipts/static/gates.tsv`):
- rc 0: `lint_rtl --check`, `docs_check`, `check_doc_paths`, `measure_test_evidence --check`, cpp/py/sv idiom and port contracts;
- `check_em_dash` was not judged here because its pinned Markdown renderer is not installed and no shared install is allowed. The author's receipt shows rc 0.

**Open:** F1, F2.

## Reviewer-owned ledger

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `KL_avtp_rx_monitor_ctx.sv:497-528,592-604,1001-1034`; `KL_crf_rx.sv:323-406,587-636`; `avtp_stream_parser.sv:185-208`; FR_NFR, compliance matrix and REGISTER_MAP rows; `[UF]`/`[FMT]` logs; `KL_avtp_rx_monitor_ctx_ref.sv:493-509`; `KL_avtp_rx_monitor.sv:182-187`; `fuzz_aaf.py:141-176`; `avtp/doc/TEST_RESULTS.md` | R673-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| RTL | CLEAN | `receipts/rtl_delta_vs_dev.diff`; `receipts/interface_scope.txt`; `milan_datapath.sv:6289-6330` (identical to dev); route receipts `round1c/route/head-75db4b57` (check.log, route status, place hierarchy, timing summary) | R673-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| Robustness | CLEAN | reject paths in both engines; `receipts/unit-probes/` (crf_lockdrop, crf_seqadv); `[UF2f-g]`, `[UF3]`, `[UF4]`, `[UF5]`, `[FMT-b2]`, `[FMT-c1]`; stop gating `KL_avtp_rx_monitor_ctx.sv:1029-1033` and `KL_crf_rx.sv:373,406,564` | R673-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| Tests | UNCLEAN (F1, F2) | `receipts/rxmon.log`, `crfrx.log`, `milandp.log`, `milandp_pool.log`, `unbmut.log`, `unit-probes/`, `dp-probes/`; `format_mutants.py`; `crf_rx/mutants.py`; `sim_nxn.cpp:1147-1189,6653-6775`; `sim_main.cpp`; `sim_prune.cpp`; `stream_counters.hpp` | R673-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |
| Docs | UNCLEAN (F1, F2) | the docs listed under Docs above; `receipts/static/gates.tsv`; PR body against the receipts | R673-1 | 75db4b57cff47bb614d14dead084649a4c2aa2a3 |

## Real limits of this round

**Not run by this round:**
- Vivado route-1x1 and the resource gate (the public receipts at this head were read instead);
- Yosys, xvlog, the full suite sweep, tsn_fuzz and the builder bank (not allowed, or left to the author's receipts);
- `make dynmap-mutants`;
- `check_em_dash` (renderer missing).

**Context:** no manager source bank exists at this head, and none is inferred. Hosted CI contexts were not inspected. Physical calibration was not run. No hardware or field proof is claimed.

**Probe hygiene:** probes ran only in copies under this packet's scratch area. The review clone is byte-identical to the head: index modes and blobs equal the HEAD tree, the worktree is clean, and the submodule gitlinks are unchanged (`receipts/clone_integrity.txt`).

## Pending manager duties

- Build and validate the current-dev merge candidate at the merge turn. Live dev was `78ca9bdf` during this review.
- Own hosted and replica acceptance: `rtl-fast`, plus exact-head `verilator-suites` and `yosys-portability` after ready.
- Re-review at the head that answers F1 and F2. Those lenses, and any lens whose scope the fix touches, must be covered again at that head.
- File the work the lane recommended but could not file:
  - the pruned 1x1 short-frame depacketizer window: a bare 86-octet 2-channel frame is accepted but never emitted (`tb/verilator/milan_dp/sim_prune.cpp:93-99`);
  - inputs above 0 read their current format only from LCTX w2/w3, which no firmware writes, so SET_STREAM_FORMAT does not reach them;
  - optionally S1 and S2.

R673-1 FINISHED
