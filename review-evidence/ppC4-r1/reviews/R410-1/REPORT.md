[R410] NEGATIVE - exact head a9ce0fa2e0b8b120703c6e541668d4281cec286e

# R410-1: internal independent review of processor PR #137 (lane C4, ACMP; closes #45, #47, #48)

- Repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
- Exact head: `a9ce0fa2e0b8b120703c6e541668d4281cec286e`, tree `7d1bfe6e68b3ce9555e32eb1e9fb14220b98f43e` (verified: `git rev-parse`, `git write-tree`)
- Source base: `b2db3a970cedbbff2f8ba813acb96122c442bc58` (processor `main`, includes PRs #132 and #133)
- Review start: PR #137 comment 5903336289. Assignment: #45 comment 5891906554.
- Round: R410-1, cleared context, own detached clone. No GitHub writes, no source edits, no commits.

## Verdict

NEGATIVE, on one open MINOR docs and traceability finding (F-1). The tests, the mutation driver and the suite records
are sound. Every acceptance item of #45, #47 and #48 is met by a named check. All 19 recorded mutants were
re-measured KILLED with the recorded failure counts. Six further reviewer-owned probe mutants were also KILLED.
F-1 is a one-row fix in `docs/00_MILAN_COMPLIANCE_REVIEW.md` F00.2, or an explicit maintainer decision to defer it.

## Reconstruction (order followed)

1. Contributor guidance: the repository has no `AGENTS.md` or `CONTRIBUTING.md` (`git ls-files` shows neither). I read
   `README.md` ("Building and checking") and `docs/README.md` (ID registries, single-source rules, citation and editing
   workflow) as the conventions.
2. Frozen acceptance: the bodies of #45, #47 and #48. #47 and #48 have no comments. On #45 there are the assignment
   5891906554 (items in order, each issue's own list is the bar, STOP before any port or parent-visible change), TAKEN
   and REVIEW READY. There are no further scope decisions.
3. Authorities: Milan v1.2 §5.5.2.2, §5.5.3.1, §5.5.3.5.18/.25/.36/.42/.45, §5.3.8.5/.9 as cited, and IEEE 1722.1-2021
   Table 8-2 and §8.2.1.6. The spec PDFs are not distributed, so I checked them against the in-repo authorities that
   quote them: 03 V3, 05 F05.14 (the GET_RX_STATE forms), 09 F09.4 and 00 §6/§7. IEEE 802.1Q §35.2.2.7.2 gives the
   Listener FourPackedType.
4. The diff `b2db3a97..a9ce0fa2` (8 files, +1038/-7, all under `tb/`) and its six commits.
5. Public evidence: `kebag-logic/milan-fpga@2aa6c820:review-evidence/ppC4-r1`. It holds only `MANIFEST.json`,
   `author/HANDOFF.md` and `author/PR-BODY.md`. No manager bank receipt is published there, and there are no manager
   evidence comments on the issues or the PR (see Limits).
6. Prior public review findings on PR #137: none exist at this head. There are no PR reviews, and the only issue
   comments are the two review-start notices. Nothing needs to be resolved or retained.

## Acceptance, item by item

| Issue item | Graded by | Reviewer evidence | Met |
|---|---|---|---|
| #47-1 msg 3,5,7,9,11,13,14 inert in a probing state (no frame, write-back, timer op, notify; one RX free) | `tb/acmp_listener` B13, `tb/acmp_listener/sim_main.cpp:1218-1253`. Adds 15, both PRB_W_RESP and PRB_W_RESP2, each shaped as the perfect probe answer | suite 2988/2988 PASS (5.050 and 5.052); probes `R-msg_ok_admits_11`, `R-msg_ok_admits_13` KILLED on their own B13 arms | yes |
| #47-2 guard per term | B14, `:1260-1293`, with a positive control (the exact answer settles) | `guard_*_dropped` KILLED 50/40/30 of 2984 | yes |
| #47-3 pp_top: one response type, one reserved type; no ACMP frame, no slot leak | `tb/pp_top` AI1-AI3, `tb/pp_top/sim_main.cpp:8981-9013` (msg 7 and 14 through the real steer; duplicate probe at T-ACMP-CMD) | AC 42/42; `msg_ok_forced@pp_top` KILLED on AI3, which proves the frames reach the listener | yes |
| #47-4 `txn_msg_ok_w` forced-1 mutation, recorded in the listener README | `acmp_mutants.py:70-78`; `tb/acmp_listener/README.md:66-93` | KILLED, 93 of 2988 as recorded | yes |
| #45-1 rx_validator cdl>44 (96-B): committed, header field-exact, slot = cdl+12, no rx_length | F29, `tb/rx_validator/sim_main.cpp:766-797`; `run_case` also compares the slot bytes exactly with the model (`:366-368`) | 495/495; probe `R-acmp_slot_truncated_at_56` KILLED ("slot bytes exact (got 56 want 96)") | yes |
| #45-2 pp_top long BIND_RX and long PROBE_TX get the same byte-exact 56-B responses | AL1-AL4, `:9021-9069`; AL2 compares with AI1's 56-B response byte for byte and regenerates PROBE_TX #2 from the long command | AC 42/42 | yes. AL3 grades the DEST_MAC_FAILED form (no allocator on this model); see Limits |
| #45-3 cdl != 44 rejection mutation, recorded in the suite README | `acmp_mutants.py:90-101`; `tb/rx_validator/README.md` M5; `tb/pp_top/README.md` | KILLED, 27 of 495 and 19 of 42 as recorded | yes |
| #48-1 bind, real PROBE_TX_RESPONSE SUCCESS, bound sid/dmac/vlan, settled GET_RX_STATE byte-exact | AS1-AS2, `:9079-9132`; expected forms agree with 05 F05.14 | AC 42/42; `bound_*` mutants KILLED | yes |
| #48-2 matching Advertise gives Listener Ready New plus the SETTLED_RSV_OK form; near miss (DA, VLAN) gives neither | AS3-AS5, `:9139-9214`; AS5 holds 11.5 s past the settle | `matcher_da/vid_ignored` KILLED; probes `R-matcher_sid_ignored`, `R-tkreg_event_not_routed` and `R-listener_ignores_tkreg` KILLED (AS5 detects a sink left in SETTLED_NO_RSV even when the trace still shows the event) | yes |
| #48-3 UNBIND_RX from settled gives Lv on the wire and clears the bound view | AS6, `:9221-9265` | `st_ls_teardown_*`, `bound_view_not_cleared` KILLED | yes |
| #48-4 st_ls_r op-code and sid/DA swap mutations, recorded | `acmp_mutants.py:113-160`; `tb/pp_top/README.md:1129-1229` | all 12 settle-path mutants KILLED with the recorded counts | yes |

## Findings

### F-1: MINOR. Lenses: Docs, Conformance (compliance traceability)

- **Location:** `docs/00_MILAN_COMPLIANCE_REVIEW.md:509`, the F00.2 row for GAP-15, "Open residue" =
  [#45](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/45). The column definition is
  at `:513-517`.
- **Authority and evidence:**
  - #45's body: "This ticket also carries the GAP-15 residue of F00.2 (tolerance category: no suite feeds an ACMPDU
    longer than 56 bytes)."
  - The F00.2 caption says a linked issue "tracks what is still unimplemented or ungraded", and that "none found" means
    "the resolution is implemented and a suite of the named category grades it".
  - PR #137 has `Closes #45` and now grades the TOL residue (F29 and AL).
  - The PR body's "What remains" itself says the row goes stale on merge and that the lane left it untouched.
  - Precedent: the PR that resolved #55, #56 and #77 updated its F00.2 cell in the same change (`05fd9e1`, GAP-03 row,
    "resolved by waiver").
  - The diff touches no file under `docs/` (`git diff --name-only b2db3a97..a9ce0fa2`, receipt 22).
- **Impact:** on merge, #45 closes automatically. The normative compliance review then names a closed ticket as the
  open, ungraded residue of GAP-15. That misstates the compliance evidence for REQ-ACMP-001 to anyone who uses 00 as
  the "compliance reviewer" entry point (docs/README §1 paths by role). `make check` cannot catch this, because it
  checks links, not issue state.
- **Required outcome:** in this PR, update the GAP-15 cell of F00.2 to what is true after #45 closes: "none found"
  under the table's own rule, or the ticket that still carries GAP-15 residue if the maintainer knows of one.
  Alternatively, get an explicit public maintainer decision that defers the edit to a named tracking issue.
- **Verification:** `git diff b2db3a97..<new head> -- docs/00_MILAN_COMPLIANCE_REVIEW.md` shows the F00.2 GAP-15 cell
  changed and nothing else in 00 (or a linked maintainer decision exists); `make check` rc 0.

### Suggestions (do not affect the verdict)

- **S-1 (Tests).** `tb/pp_top/sim_main.cpp:9252-9261`, AS6's quiet window. `get_rx_state()` (`:8914-8918`) waits with
  `wait_acmp`, and `wait_frame` (`:1841-1852`) pops and discards every non-matching queued frame. So an ACMP frame
  emitted between the UNBIND_RX_RESPONSE and the GET_RX_STATE_RESPONSE (up to about 0.9 s, while the Lv is awaited on
  the MSRP queue) is dropped without being graded, and the 1.5 s "no ACMP frame" check starts only after it. This is
  not required by #48 item 3. A `q_acmp` emptiness check before the GET_RX_STATE feed, or a non-discarding wait, would
  make "nothing probes the sink afterwards" (README, AS6) hold from the unbind on. The same discard pattern precedes
  the AS1-AS4 GET_RX_STATE checks, where no extra frame is expected.
- **S-2 (Docs, pre-existing, outside this diff).** `docs/architecture/09_verification.md:62` labels the 96-B form "2013
  96-B ACMPDU". The new F29 and AL tests (correctly, per their cited IEEE 1722.1-2021 §8.2.1.6 and Figure 8-1) treat
  the cdl-84 form as the 2021 layout. A maintainer may want the 09 row to say which edition. I could not re-check this
  against the non-distributed spec text.

## Lens analysis

**Conformance.**
- The message-type codes match IEEE 1722.1 Table 8-2 as cited. The listener's owned set {1, 6, 8, 10} and the top's
  steer (everything but {0, 2, 4, 12} to the listener) are what B13 and AI exercise.
- The GET_RX_STATE expected frames match 05 F05.14 row by row:
  - unbound: all 0;
  - probing: bound values, cc 1, FAST_CONNECT, stream 0;
  - settled: plus the response's {sid, DA, VLAN}.
- The Listener Lv and New vectors carry FourPackedType Ready (802.1Q §35.2.2.7.2).
- The 96-B form puts cdl 84 in the right header bits and patterns the 40-byte tail.
- UNCLEAN only through F-1's traceability record. No behavioural non-conformance was found, and there is no RTL change
  to judge.

**RTL.**
- `git diff b2db3a97..a9ce0fa2 -- hdl` is empty. The only non-suite source is `tb/pp_top/pp_top_wrap.sv`, which
  connects the top's existing `acmp_bound_eid/sid/dmac/vlan_o`. Its widths (8×64/64/48/12) equal
  `protocol_processor_top.sv:611-619` at the default `N_STREAM_IN_P = 8`, which the wrap does not override
  (`pp_top_wrap.sv:453-472`).
- The unique-warning delta of the pp_top build, base to head, is exactly the removal of the four matching PINMISSING
  warnings (receipt 18). `lint_hdl.sh` passes with 41 LINT OK (receipt 17).
- The glue the tests target (`st_ls_r` at `protocol_processor_top.sv:2466-2473`, the bound-view latch at `:1659-1675`,
  the matcher at `KL_srp_listener_fsm.sv:408-413`) is exactly what the mutants edit. Every edit anchor occurs once.
- CLEAN.

**Robustness.**
- The suites are deterministic and pass under two Verilator versions:
  - 5.050: acmp_listener 2988/2988, rx_validator 495/495, pp_top 7930/7930 over both builds;
  - 5.052: the first two, plus pp_top `--acmp-only` 42/42.
- AC runs on its own fresh model, so the main DUT timeline is untouched. The byte-exact MRPDU checks are aligned into
  LeaveAll-free windows (`la_window`, `sync_join`).
- The driver works only in private copies. `plant()` refuses any edit whose anchor does not occur exactly once. A
  refused edit, a failed build or a missing tally never counts as a kill (`acmp_mutants.py:166-217`).
- `main()` gates keep `--gsi-internal-only`, `--name-writes-only` and `--d3-only` free of AC.
- My clone stayed byte-exact throughout (receipt 40).
- CLEAN.

**Tests.**
- The checks discriminate:
  - all 19 recorded mutants were KILLED by their named checks, with the recorded failure counts (receipts
    `mutants/records.jsonl`, `13-acmp_mutants-entrypoint.log` rc 0 "19 of 19 KILLED; goldens PASS");
  - six reviewer-owned probes outside the author's table were KILLED on the intended checks (`reviewer-probes/`):
    matcher ignores stream_id; TK_ATTR_REGISTERED not routed; listener ignores TK_REG (AS5 alone catches it); ACMP
    slot truncated at 56 B (F29 catches it); listener admits msg 11 only; listener admits msg 13 only.
- Other entry points that build the changed suites all pass at the head:
  - `gsi_mutants.py` rc 0 (20 detected, golden and restored PASS);
  - `name_wr_mutant.py` rc 0;
  - `d3_mutants.py`: goldens PASS and a sample of 8 of 83 KILLED;
  - `make check`, `gen_matrix.py --check` and `git diff --check` rc 0.
- The drivers the author did not re-run (`tb/srp_top` mutants, `tb/nvm_port` figures, `syn/yosys/run.sh`,
  `tb/srp_admission/mutants.py`, `tb/acmp_talker/retry_mutants.py`) have byte-identical inputs at base and head. None
  of their directories, `hdl/`, `tb/common/` or `scripts/` changed, and none of them references a changed suite
  (receipt 22).
- CLEAN (S-1 is a suggestion only).

**Docs.**
- The suite READMEs are accurate against measurement:
  - listener 2988 and the B13/B14 table;
  - validator 495 and M5 (27 FAILs);
  - pp_top section AC, `--acmp-only` and the 14-row mutant table (every "failing checks" figure equals my tally).
- The PR body's claims (no `hdl/` or `docs/` change, the suite totals, 19/19) agree with the tree and my runs.
- UNCLEAN on F-1.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-1) | #45/#47/#48 acceptance; 05 F05.14, 03 V3, 09 F09.4, 00 F00.2/§6; B13/B14, F29, AI/AL/AS expected frames | R410-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| RTL | CLEAN | empty `hdl/` diff; `pp_top_wrap.sv` port hookup versus top `:611-619`; warning delta; `lint_hdl.sh` 41 OK; mutant anchors in top, listener, validator, matcher | R410-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| Robustness | CLEAN | two-tool suite runs; fresh-model AC; LeaveAll alignment; driver refusal and kill rules; main() flag gating; clone integrity | R410-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| Tests | CLEAN | 19/19 recorded mutants re-measured; 6 reviewer probes; driver entry point; gsi, name-write and D3-sample drivers; untouched-driver input check | R410-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |
| Docs | UNCLEAN (F-1) | 3 suite READMEs versus tallies; PR body claims; `docs/00` F00.2; `make check` | R410-1 | a9ce0fa2e0b8b120703c6e541668d4281cec286e |

## Commands and receipts (all foreground; at most 8 concurrent build jobs; disposable trees under `scratch/`)

- `receipts/00-tool-identity.txt`: the requested pinned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator`
  is **absent**. I used an equivalent wrapper of `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`
  (Verilator 5.050 rev v5.050, binary sha256 recorded) and the system Verilator 5.052 for cross-checks.
  `scripts/verilator-capped.sh` rewrites the suites' `--build -j 0` to a fixed job count.
- `10`/`11`/`12`: acmp_listener, rx_validator and full pp_top (both builds) under 5.050, all rc 0.
- `30`/`31`/`32`: the same suites under 5.052 (pp_top `--acmp-only`), all rc 0.
- `mutants/`: golden and 19 mutants via `scripts/run_acmp_mutants_chunk.py`, which calls the driver's own `judge()`.
- `13` and `driver-entrypoint/results.json`: `python3 tb/pp_top/acmp_mutants.py --jobs 2`, rc 0.
- `reviewer-probes/` plus `scripts/reviewer_probes.json`: the six probes.
- `14`/`15`/`16`/`17`: `make check`, `gen_matrix.py --check`, `git diff --check` and `lint_hdl.sh`, all rc 0.
- `18`: the pp_top warning delta. `19`/`20`/`21`: gsi, name-write and D3 sample drivers, rc 0.
- `22`: untouched-driver inputs. `40`: clone integrity (HEAD, tree = write-tree, empty porcelain, every tracked blob
  hash and mode equal; the repository has no gitlinks).
- Receipts had the home-directory prefix replaced by `$HOME`; no other edits.

## Real limits

- The requested pinned Verilator path does not exist. I used a 5.050 of the same version from another manager scratch
  (identity recorded) plus the system 5.052. The manager should confirm tool identity for acceptance.
- I did not run the full processor bank (`run_suites.sh` over 33 suites), parent banks, Yosys, the builder or hosted/act
  jobs, as the assignment requires. The 30 unchanged suites have byte-identical inputs at base and head.
- `d3_mutants.py` was sampled (goldens plus 8 of 83), not run in full. The author reports 83/83.
- The public evidence commit holds no manager bank receipt, so I could not inspect the "manager source static/builder
  and native banks passed" statement from public evidence.
- AL3 grades the long PROBE_TX only on the DEST_MAC_FAILED answer, because this model wires no allocator. The SUCCESS
  talker path with a long command is not exercised at the top. #45 item 2 is still met (byte-identical answer for both
  forms).
- Spec clauses were checked against the in-repo quoting authorities, not the copyrighted PDFs.
- Physical calibration NOT RUN. No hardware was used, and field skips are not hardware proof.

## Pending manager duties

- Rule on F-1: a docs row fix in this PR, or a recorded deferral.
- Run and post the donor full bank and the parent consumer bank at milan-fpga dev `ec0cc0c1` with the combined #132
  and C1 parent adaptation applied. That includes the `DUT_READER_DISPOSITIONS` entries for `acmp_mutants.py` and
  `d3_mutants.py` in `measure_test_evidence.py`, and confirming the five gitlink-only failures attribute to #132/#133.
- Build and verify the final current-dev candidate at the merge turn (source base `b2db3a97`, live dev `ec0cc0c1`).
- Own hosted/act acceptance, and confirm the pinned Verilator identity.
- Obtain the second independent positive review (R411) before merge.

R410-1 FINISHED
