[R459] NEGATIVE - exact head 9160f7d7f005050887cab942710940b91e34fc65

# R459-2: external independent review of milan-fpga #230 / processor PR #154 (round 2)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan, PR #154 (`pp230-srp-area` -> `main`).
- Exact head `9160f7d7f005050887cab942710940b91e34fc65`, tree `bd926d188f3205a819e9248ed1a07dae14098e7f`. Source
  base `c4cb84ff8cecad19bedaa85dde594a8ed68012f6`.
- Review role: external reviewer, cleared context, isolated detached clone. Round R459-2: a delta review of
  `65324390..9160f7d7` against round 1 (R459-1, R458-1) and the round-2 assignment (#230 comment 5978448959).
- Verdict: **NEGATIVE** on one MINOR (Tests, Docs): a summary sentence in the committed `tb/srp_top/README.md`
  claims coverage that its own table contradicts for one cell. It needs a one-sentence README fix and no HDL change.
  Everything else checks out:
  - The RTL is byte-identical to round 1's.
  - Both merges keep both sides.
  - The committed campaign is 126/126, and every per-control, per-shape count matches the PR body cell for cell.
  - Every non-vacuous probe of mine, and every R458-1 probe, is killed by a named committed check.
- One RESIDUE: the PR body's "head" wording predates the manager's merge.

## 1. What was reconstructed (in order)

1. Repository guidance. The processor repository has no `AGENTS.md` or `CONTRIBUTING.md` at this head. I used
   `README.md`, `docs/README.md` and `docs/guides/hdl-engineer.md` §3, as in round 1; none of them changed since.
2. Issue kebag-logic/milan-fpga#230: the body (scope, acceptance) and all 7 comments. These include:
   - the scope addition (5967853024);
   - the lane (5974045353);
   - ruling (b) (5977836860);
   - the round-2 assignment (5978448959);
   - REVIEW READY at `1199255` (5979936594).
3. PR #154: the body at the exact head (`receipts/public/pr154_body.md`) and all 7 comments. These include the
   manager's F1/F2 note (5978368336), R459-1 (5978360032) and R458-1 (5978441050); the R458-1 report was read only
   after my verdict, see §2. The PR has 0 reviews and 0 review comments.
4. Interfaces and authorities: `KL_srp_top`, the talker and listener FSMs, admission, and the processor top's
   binding, as in round 1. They are unchanged here, since `hdl/srp` is byte-identical (§4.2).
5. `git diff c4cb84ff..9160f7d7` and history, focused on the delta `65324390..9160f7d7`:
   - 82 files;
   - two lane-side merges and seven lane commits;
   - the manager's `--no-ff` merge of `main` `c050d971` (PR #153).
6. Public evidence:
   - milan-fpga `8dca0983` `review-evidence/pp230-r1` (round 1).
   - The same evidence branch now at `00f848e5` (`pp230-review-evidence`). It holds round 2's `author-r2/HANDOFF.md`,
     `PR-BODY.md` and `lockstep-r1/`, and `06fe795b`'s eight Vivado runs.
   - The PR body equals `author-r2/PR-BODY.md` apart from a trailing newline.
   - Seven `author-r2` files equal the published digests in `MANIFEST.json`.
   - The `lockstep-r1` digests equal HANDOFF R2.4.6.
7. Hosted checks at the exact head (read-only, last read about 15:15 local):
   - docs-gates and portability: success, on push and on pull_request (executed).
   - suites: `in_progress` on both runs. That is not an executed result.

My verdict and ledger were written before I read the R458-1 report (`receipts/verdict_before_reading_prior_findings.md`,
sha256 `d4a4f2bc...`).

## 2. Prior public review findings at this head

| Finding | Disposition at `9160f7d7` | Evidence |
|---|---|---|
| R458-1 F1 (MINOR, Tests): storage paths and the N <= 2 arm untested; eight probes survive | **Resolved** | WK1-WK8 (`tb/srp_stream_fsms`) and TF1-TF5 (`tb/srp_top`) run at 1/1, 2/2, 3/5 and 9/9 in the default `make`. R458-1's 17 published probe edits are byte-identical to the committed patches (`receipts/r458-1_probe_patch_identity.txt`). All 17 are KILLED in my run of the committed campaign, the eight former survivors included (§4.4). The lane's lockstep bench is published (`lockstep-r1/`) |
| R458-1 F2 = R459-1 F1 (MINOR): area figures on unpublished receipts | **Resolved** (`06fe795b`) | All eight HANDOFF §5.6 log-digest prefixes match `MANIFEST.json`'s original SHA-256. Spot re-derivation from the published route reports: LUT 51,434 -> 51,005, FF 59,691 -> 57,262, slices 15,847 -> 15,837, `u_srp` 4,340 (180) / 6,263 -> 3,711 (298) / 3,839, 0 routing errors (107,053 / 104,430 routed nets), WNS/WHS +0.079/+0.014 -> +0.354/+0.036 ns. All equal the PR body |
| R458-1 F3 (MINOR): control-count sentence | **Resolved** | The PR body (lines 195-217) and HANDOFF §4.2 now give round 1's table with a "Caught at" column. My recount: 6 at four shapes, 4 at three, 5 at two, 1 at one, as both state. The new table's summary (18 / 1 / 6 / 4; slopes 4 of 5) also recounts exactly (§4.5) |
| R459-1 F2 (MINOR): PR-body coverage overclaim | **Resolved** | Body line 253: "caught at one to four of the four shapes (Round 2 above has each row)", which is accurate |
| R459-1 R1 (RESIDUE): "10 section 5.1" | **Resolved** in the body | It is named in full at lines 24, 29, 71 and 80. Commit `df02e64`'s subject repeats the short form (body line 243 says so); history is not rewritten, as in round 1's disposition |
| R459-1 R2 (RESIDUE): "all rc 0" header | **Resolved** | Line 245 now reads "## Validation (all rc 0 except parent gate 16, recorded against #643; no pipes)" |
| R459-1 S1 / R458-1 S1 (SUGGESTION) | **Taken** | `docs/guides/hdl-engineer.md:88-93` names `wtsp_r`, `g_wid_ram.wid_r`, `g_wsid_ram.wsid_r`, `slope_q_r` and the FIFOs, correctly. The FIFO full guard is now exercised (TF4/TF5) |
| R459-1 S2 (SUGGESTION): commit a lockstep bench | **Addressed differently, as assigned** | Directed arms are committed (the assignment preferred them over a frozen base copy), and the round-1 bench is published with digests |
| R458-1 O1 (observation, outside the diff) | Not this PR's | Not re-examined |

## 3. Findings

### R459-2-F1 (MINOR): the srp_top README's coverage sentence overstates one cell

- **Lenses:** Tests, Docs.
- **Artifact:** `tb/srp_top/README.md:620-622`. It says: "Every control is caught at every shape where its arm is
  elaborated and the edit is not equivalent by construction."
- **Evidence.** The README's own row for `wsid-flops-of-control-sink` (`:606`) is "0 (equivalent in simulation)" at
  1/1, "1 of 4". Its legend (`:568-575`) explains: "Verilator reads a single 64-bit packed element at an out-of-range
  index as element 0, so the edit reads sink 0 there too".
  - At 1/1 the flop arm `g_wsid_flops` is elaborated (`N_SINKS_P = 1 <= 2`).
  - WK6 parks the control face on index 1, which is out of range for one sink.
  - Under the language's 4-state semantics, `sid_r[ctl_sink_i]` then reads X, not sink 0. The edit is therefore not
    equivalent by construction; only the simulator makes it so.
  - My run confirms the receipt: `receipts/mutants/arms/wsid-flops-of-control-sink.log` has failing lines only at
    `[2/2]`.
  - My simulator probe confirms the cause: `receipts/oor_check.txt`, where a 64-bit one-element packed array read at
    index 1 returns element 0 and a 48-bit one returns 0.
  - The table, the legend and every count are right. Only the summary sentence is wrong.
- **Authority.**
  - The round-2 assignment, item 2 (5978448959): state the per-control shape counts exactly as the table shows them.
  - The owner rule of 2026-10-02: a claim about test results is not wording-only residue. The same class was MINOR in
    R459-1 F2 and R458-1 F3.
- **Impact.** The committed README asserts complete coverage of non-equivalent edits wherever their arm is elaborated.
  One elaborated, non-equivalent cell is uncaught. The underlying coverage is sound: the same arm code is caught at 2/2,
  which is the shipping 1x1 shape's two contexts per FSM (stream plus CRF).
- **Required outcome.** Amend the sentence in a test- and documentation-only commit with no HDL change. For example:
  "Every control is caught at every shape where its arm is elaborated and the edit is not equivalent by construction,
  except `wsid-flops-of-control-sink` at 1/1, which only the simulator's out-of-range read makes equivalent (above)."
- **Verification.** Every 0 cell in the README table is either n/e, equivalent by construction, or the named exception.

### R459-2-R1 (RESIDUE): the PR body's "head" predates the manager's merge

- **Lenses:** Docs.
- **Artifact:** PR #154 body, three places:
  - line 9: "Head `1199255`.";
  - line 255: "**Processor suites, at the head.** ... `run_suites.sh`: 33 suites, 1,021,469 checks";
  - line 263: "run at the merge commit `4994ada` (their inputs equal the head's)".
- **Evidence.**
  - At `9160f7d7`, the manager's merge of `main` `c050d971` (PR #153) changes `tb/aecp_notify` and
    `tb/pp_top/notify_mutants.py`.
  - The notify suite's last tally is 14 at `1199255` and 30 at `9160f7d7` (`receipts/notify/`). So the 1,021,469
    total is `7365022`'s, and the notify campaign's inputs differ from the exact head's.
  - Line 280 records the merge. Every figure is accurate for the commit it was measured at, so the fix changes no
    figure.
- **Exact fix.**
  - Line 9: "Head `9160f7d7` (the manager's `--no-ff` merge of `main` `c050d971` onto the lane's `1199255`)."
  - Line 255: "**Processor suites, at `7365022`** (the lane's head before the manager's merge; `1199255` adds only a
    README)."
  - Line 263: "(their inputs equal `1199255`'s)".

## 4. Lens evidence

### 4.1 Conformance: CLEAN

- **Ruling (b) and behaviour identity.** `hdl/srp` is byte-identical to `25847d07` and `65324390` (`git diff --quiet`).
  Round 1's lockstep equivalence (R459-1 §4.3) therefore carries unchanged. No port, parameter or register changed.
- **HDL provenance at the head.** The head's HDL equals `main` `c050d971`'s, plus exactly the four SRP files of
  `25847d07`. `main` never touched `hdl/srp` after `c4cb84ff`, so neither merge brings SRP HDL. The area delta, base
  `c4cb84ff` against this RTL, stands.
- **Merges keep both sides.** I ran a three-way per-path blob check on `4994ada` (parents `65324390`, `83999eba`) and
  on `9160f7d7` (parents `1199255`, `c050d971`). Every path takes the changed side, no path changed on both sides, and
  0 mismatch. There are no mode changes and no gitlinks.
- **PR #153's scope.** `83999eba..c050d971` touches 7 files: notify RTL, its suite and README, the notify campaign, and
  the notify rows of `06_aecp_engine.md`, `09_verification.md` and `tb/pp_top/README.md`. None of them is in common
  with the lane.
- **Acceptance.**
  - The area criteria rest on `06fe795b` (§2).
  - The 100 MHz criterion is judged at 50 MHz: route WNS is +0.354 ns at the head.
  - "Documented in #229" is a pending manager duty (§7).

### 4.2 RTL: CLEAN

- No HDL changed in round 2.
- R459-1's `make_controls.py`, run unchanged, found each of its 16 search strings exactly once at the head, so every
  edited RTL line is as reviewed in round 1.
- `scripts/lint_hdl.sh` at the head: rc 0, 41/41 (`receipts/scoped/lint_hdl.log`).
- Round 1's RTL lens (single writers, valid gating, index ranges, X-safety, mapping) applies byte for byte.

### 4.3 Robustness: CLEAN

- **The one forced state** (`tb/srp_top/srp_store_wrap.sv:164-169`; Decision `:20-27`). It cannot mask a real defect:
  - **What it forces.** It forces only `tm_st_r`, the issue state, to its idle encoding. The FIFO write enables,
    addresses, data, pointers, count and full guard all run as unforced RTL.
  - **What happens while held.** `tf_pop_w` is 0, so nothing drains. The scoreboard checks that no FSM op leaves while
    held, and that the refusal model is independent of the DUT (`store_main.cpp:184-188`). Released, exactly 32 ops
    leave per FIFO, in order and unmodified.
  - **My receipt, at every shape.** 36 ops are offered and 4 refused per FIFO (60 offered and 28 refused for the 3/5
    listener), and 32/32 are issued after release.
  - **Defects on the drain path** are covered unforced by TF1-TF3. In the natural arm, both FSMs offer in one clock
    2/4/7/18 times, and a two-word talker FIFO is selected 1/2/4/19 times (at 1/1 too).
  - **Defects on the full path** are covered by TF4/TF5: `tf-full-guard-31` and both `*-write-ignores-full` edits are
    killed at all four shapes.
  - **The one corner the hold does not reach** is a push and a pop on the same clock at full. That logic is unchanged,
    and it was already shown equivalent to base by R459-1's full-boundary lockstep probe, which drained with pushes
    ongoing.
- **Workaround 1: the TM_SEL encoding** (`srp_store_wrap.sv:105-107`). It cannot drift silently:
  - **Re-encoding probe** (`receipts/tmsel/`). I re-encoded `tm_st_e` in the RTL (TM_SEL = 1, TM_POP = 0), a
    behaviour-neutral edit that makes the wrap's named encoding stale. The arms then fail loudly at 1/1 and 9/9:
    the "TF4 precondition" fails (688 and 821 ops issued while held), and TF4 fails.
  - **The hierarchical reference** `u_dut.TM_SEL` stops Verilator 5.050 with an internal error (`V3Width.cpp:9628`).
    The wrap's reason holds; HANDOFF's "signal 11" may be a different spelling of the same reference.
- **Workaround 2: the 64-bit out-of-range alias** (`receipts/oor_check.txt`). It is confirmed as described.
  - **Effect on the 1/1 flop-arm claim.** The claim still holds at the arm level:
    - The flop arms run at 1/1 and are caught there for every non-index defect (`talker-vid-unreset`,
      `wid-flops-da-of-gate-source`, the TSpec rows).
    - Index-selection edits at one context are equivalent (in-range) or simulator-aliased (out-of-range).
    - The identical arm code is killed at 2/2.
  - **Only the README's summary sentence overclaims** (F1).
- **Unreset memories.**
  - The walk arms build with `--x-initial unique` and run with `+verilator+rand+reset+2`, as the README says.
  - The store arms use the default (zero) initialisation, and the README makes no random-start claim for them. Every
    issued word carries an owner tag of at least `0x40`, so a read before write of a zero word would still mismatch.
- **Parked indices.** WK1 and WK6 park the idle gate and control faces on `0xF`, cut to each FSM's index width. That
  gives 1 at one and two contexts, 3 at three, 7 at five and 15 at nine. The index is out of range at 1, 3, 5 and 9
  contexts, and in range (the last context) at 2.

### 4.4 Tests: UNCLEAN (F1)

- **Positive, at the head** (`receipts/positive/`, default `make` in a `git archive`), all rc 0:

  | Suite | Arms per shape (1/1, 2/2, 3/5, 9/9) | Suite tally |
  |---|---|---|
  | `srp_top` | TF: 15, 15, 15, 15 | 2,200 |
  | `srp_stream_fsms` | WK: 23, 30, 43, 79 | 1,219 |
  | `srp_admission` | - | 1,138 / 12,615 / 41,012 / 201,073 / 991,231 at N = 1 / 2 / 3 / 5 / 8 |
  | `srp_decoder` | - | 190 |
  | `srp_encoder` | - | 581 |

  The STORE lines (offered, issued, both, deep, MRPDUs, refused) equal HANDOFF R2.4.2 and the README table cell for
  cell.
- **Committed campaign** (`tb/srp_top/mutants.py --jobs 7`, `receipts/mutants/campaign.log`): rc 0, 126 checks,
  126 PASS, assertion coverage 78/78.
  - The 14 positive controls pass.
  - All 33 new arms are KILLED by their named check.
  - Round 1's 73 arm labels over 78 runs keep identical verdicts, failure counts and failing tags against my R459-1
    receipt.
- **Per-shape counts, row by row** (`scripts/summarize_r2.py` -> `receipts/mutants/per_shape_vs_body.md`): all 29
  TF/WK rows (named checks, the four shape cells, "Caught at") equal the PR-body table, with 0 differences.
- **Slope rows.** My one-shape-at-a-time runs (`receipts/slope/slope_shapes.log`) give all 20 cells equal to the
  PR-body table, including the 41,009 / 201,068 / 991,223 totals for `slope-read-source-0`. N = 1 passes for all four
  (equivalent).
- **My round-1 probes and plants, run UNCHANGED** (`scripts/r1_controls_vs_committed.sh`, `receipts/r1controls/`).
  R459-1's `make_controls.py` and the stall probe's defect edit (its `stall2` text, without the stall) were applied
  to the head's `hdl/srp`. Each committed suite that builds the edited file then ran its full default `make`.

  | Control | Declared | Committed suites (rc, failing, named arm checks) |
  |---|---|---|
  | `tf-ls-head-reads-tk-ram` | catch | srp_top rc 2, 24 (TF1-TF5) |
  | `tf-tk-head-reads-next` | catch | srp_top rc 2, 14 (TF1, TF4) |
  | `tf-ls-write-ignores-full` | catch at full | srp_top rc 2, 4 (TF5) |
  | `tf-tk-write-at-rptr` | catch | srp_top rc 2, 9 (TF1, TF4) |
  | `tf-tk-write-ignores-full` (stall probe's defect) | catch | srp_top rc 2, 4 (TF4) |
  | `wtsp-written-on-close` | catch | srp_top rc 2, 2; srp_stream_fsms rc 2, 4 (WK3) |
  | `wtsp-prio-rank-swapped` | catch | srp_top rc 2, 2; srp_stream_fsms rc 2, 82 (WK1-WK5) |
  | `wtsp-read-at-source-0` | catch | srp_top rc 2, 1; srp_stream_fsms rc 2, 50 (WK1-WK5) |
  | `wid-ram-read-neighbour` | catch | srp_top rc 2, 26; srp_stream_fsms rc 2, 94 (WK1-WK5) |
  | `wid-flops-vid-of-source-0` | catch | srp_top rc 0; srp_stream_fsms rc 2, 6 (WK1-WK5, at 2/2) |
  | `wsid-ram-written-on-teardown` | catch | srp_top rc 0; srp_stream_fsms rc 2, 2 (WK7, at 3/5 and 9/9) |
  | `wsid-flops-read-sink-0` | catch | srp_top rc 0; srp_stream_fsms rc 2, 4 (WK6-WK8, at 2/2) |
  | `slope-store-at-stage-1-index` | catch | srp_top rc 2, 673; srp_admission rc 2, 1,333 (incl. "round publishes the greedy walk ...") |
  | `slope-read-source-0` | catch | srp_top rc 2, 217; srp_admission rc 2, 578 (same named check) |
  | `tf-tk-same-entry-bypass` | equivalent | srp_top rc 0; pp_top rc 0, 10,416 checks |
  | `wid-threshold-ram-from-1` | equivalent | srp_top, srp_stream_fsms rc 0; pp_top rc 0, 10,416 |
  | `wid-threshold-flops-always` | equivalent | srp_top, srp_stream_fsms rc 0; pp_top rc 0, 10,416 |

  - All 14 non-vacuous probes are killed by a named committed check.
  - The 3 equivalent edits stay silent everywhere.
  - Every failing count equals HANDOFF R2.4.5's table.
- **Named checks can fail for their defect.** Each of the 33 committed patches is the exact edit of a reviewer probe
  or lane control: mine checked edit by edit against `make_controls.py` and the `stall2` text, and R458-1's by byte
  comparison.
- **Two FIFO controls at 1/1.** `tf-head-at-write-pointer` and `tf-listener-push-dropped` are now caught at 1/1 (2
  and 1 failing checks), as the assignment required.
- **F1** is the one Tests gap: a claim about the tests, not a test defect.

### 4.5 Docs: UNCLEAN (F1; R1 residue)

- **PR body against HANDOFF.** All 59 body table rows match HANDOFF rows (commit table aside). The 29 control rows
  and 4 slope rows equal my receipts.
- **Summary counts.**
  - New table: 18 at four shapes, 1 at three, 6 at two, 4 at one; slopes 4 of 5.
  - Round 1's table: 6 / 4 / 5 / 1.
  - Both recounted exactly.
- **Committed prose.**
  - `docs/architecture/10_srp_engine.md:219-222` (arms at four shapes; every review probe a killed control): true.
  - `docs/guides/hdl-engineer.md:88-93` (asynchronous-read RAMs and the registered FIFO read): true.
  - `tb/srp_stream_fsms/README.md` (shapes, random initialisation, WK table, tallies 23/30/43/79): true.
  - `tb/srp_top/README.md`: the FIFO-arm section, its table, the Verilator note and the control table are true. The
    summary at `:620-622` is F1.
- `make check` at the head: rc 0. It reports 41 mermaid and 18 wavedrom blocks, 1,131 links, 115 REQ rows, 94 matrix
  rows with 0 untested, and 28 parameters (`receipts/scoped/make_check.log`).
- R1 (residue) is above.

## 5. Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Ruling (b); `hdl/srp` byte identity to `25847d07`/`65324390`; HDL provenance against `main` `c050d971`; three-way merge check of `4994ada` and `9160f7d7`; PR #153's scope; area evidence `06fe795b` (eight digests, route figures and WNS/WHS re-derived) | R459-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| RTL | CLEAN | No HDL delta; `make_controls.py` search-string identity; `lint_hdl.sh` 41/41; round 1's RTL lens carried byte for byte | R459-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| Robustness | CLEAN | The forced state (`srp_store_wrap.sv:20-27,164-169`, `store_main.cpp:164-220,473-518`); the TM_SEL re-encoding and hierarchical-reference probes; the out-of-range alias probe; parked indices (WK1, WK6); random-start walk arms; full guard at all four shapes | R459-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| Tests | UNCLEAN (F1) | Positive SRP suites at the head; `mutants.py` 126/126, 78/78; 29 per-shape rows and 20 slope cells against the body; round-1 labels; my 17 round-1 controls unchanged against the committed suites; R458-1's 17 probe edits against the patches | R459-2 | 9160f7d7f005050887cab942710940b91e34fc65 |
| Docs | UNCLEAN (F1; R1 residue) | PR body (all tables and summaries) against HANDOFF and receipts; `tb/srp_top/README.md`; `tb/srp_stream_fsms/README.md`; `10_srp_engine.md:219-222`; `hdl-engineer.md:88-93`; `make check`; prior residue R1/R2 | R459-2 | 9160f7d7f005050887cab942710940b91e34fc65 |

## 6. Real limits

- **Not run by me** (not allowed here):
  - the full `run_suites.sh`, the Yosys gate, the pp_top/maap/adp/notify/d3 campaigns, and `nvm_port` figures;
  - the parent consumer set of 17, the builder, and the parent gate 16 at dev `fea346e7`;
  - the Vivado runs.

  The PR body's figures for these are the author's, at `7365022`/`4994ada`/`1199255`.
- **Manager's bank results.** The brief states the manager's source static/builder and native banks passed at this
  head. At my last read I found no public receipt of them: the evidence branch is at `00f848e5`, 12:32, and body line
  280 states a re-run without figures.
- **R458-1's `lockstep/probes.py`** was not executed by me. Its probe table was compared byte for byte with the
  committed patches, which my campaign run executed.
- **Hosted `suites`** were `in_progress` on both runs at my last read, so they are not an executed result.
- **Simulation only.** This is simulation, not formal equivalence. The FIFO full boundary is reached only through the
  test-only hold (§4.3).
- **No hardware run.** Physical calibration was NOT RUN, and field skips are not hardware proof.
- **Run hygiene** (no result is affected):
  - My first round-1-controls launch was stopped by me before any result, to keep memory under the cap, then rerun
    complete.
  - My first slope-runner attempt failed to build because my copy lacked `tb/common`. It was rerun complete; the
    failed attempt is not a receipt.
  - The unit reached `memory.max` under page-cache reclaim, with 0 OOM kills.

## 7. Pending manager duties

- **F1:** a one-sentence fix in `tb/srp_top/README.md:620-622` (new head, no HDL change), then a re-review of that
  delta.
- **R1:** amend PR-body lines 9, 255 and 263 as given (residue checklist).
- **The final current-dev candidate** at the merge turn: source base `c4cb84ff` onto live dev `fea346e7`, with c8,
  p2-p1, c10 and the #232 xvlog patch. It includes the parent consumer set of 17, where gate 16 should now pass with
  #643 fixed; I did not verify that.
- **Hosted acceptance:** `suites` at the exact head.
- **Publish** the manager's bank receipts at `9160f7d7`.
- **#230's "documented in #229"** item, and closing #230 manually at the processor merge (ruling 5977836860).

## 8. Receipts

`MANIFEST.sha256` lists every published file, with paths relative to this packet. Local paths, user and host names
are redacted as `<PACKET>`, `<CLONE>`, `<HOME>`, `<USER>`, `<HOST>`, `<VERILATOR_IMAGE>`,
`<VERILATOR_WRAPPER_DIR>` and `<TMP>`.

- **Scripts:** `scripts/` (see `scripts/README.md`).
  - Verilator 5.050 identity: `--version` "Verilator 5.050 2026-07-01 rev v5.050"; wrapper SHA-256
    `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`.
- **Raw logs and rc files:** `receipts/{positive,mutants,slope,r1controls,tmsel,notify,scoped,oor}/`.
- **Public inputs as fetched:** `receipts/public/`.
- **Clone integrity after the review** (`receipts/clone_integrity.txt`):
  - HEAD is `9160f7d7...` and the tree is `bd926d18...`;
  - `git status --porcelain --ignored` is empty, and the index and work tree equal HEAD;
  - all 552 tracked blobs and modes are re-hashed equal;
  - there are 0 gitlinks, and none are required;
  - no file in the clone was edited. Every probe ran on `git archive` copies under the packet's scratch directory.

R459-2 FINISHED
