# HANDOFF round 2, [A784], lane 917 (#917, PR #918, part of #665)

Status: DONE at 8f73ade5; REVIEW READY posted once on #917 (issuecomment-6902798240); not pushed

- Branch: 917-aecp-hold, base origin/dev-soft-core cec88385ad. Round 1 head 3926c271 (REVIEW READY #917
  issuecomment-6899259827). Round 2 head **8f73ade5** (one commit on 3926c271), not pushed: the manager pushes it
  to PR #918 and replaces the PR body with PR-BODY.md (whole PR, with a Round 2 section).
- Reviews answered: R845-1 NEGATIVE (PR #918 issuecomment-6899723183, `review-evidence/917-r1/reviews/R845-1/REPORT.md`
  on 917-review-evidence), R846-1 NEGATIVE (issuecomment-6899591157, `.../R846-1/REPORT.md`); the manager's
  ruling on R846-1 F2 in the round-2 brief.
- Resume after a host restart: nothing of round 2 had started when the session was cut (empty output dir, no
  round-2 comment, no unit of this lane running); every gate below ran afterwards, on clean clones of 8f73ade5.
- Comment: REVIEW-READY text in comments/REVIEW-READY.md, posted once on #917 (issuecomment-6902798240).

## 1. Findings and their closure (lines at 8f73ade5)

| Finding | Closure (file:line) | Verification |
|---|---|---|
| R845-1 F1 MINOR (Tests, Robustness, Docs): free space past a held record, no check that can fail | B7 in `check_held_space_and_refusals`, `tb/verilator/mbx/suite.hpp:1652-1692` (called at `:1645`): the AECP ring filled to room for one record (`rec = 2 + (bytes+3)/4`, `fill = words/rec - 1`, refills past the burst), the held "last" takes it, the next frame counts in RX_DROP not RATE_DROP, every unread record and the held one byte for byte. Arm `rx-space-from-the-committed-head` (+`-axil`), `tb/verilator/mbx/mutants.py:679` (`used_w = head_r[ch_r] - tail_w`). README row of `rx-tail-inside-the-held-record-frees-space` corrected, `tb/verilator/mbx/README.md:452`; new rows `:453-455`. | Both arms caught by "B7 with the ring holding room for one record, the held one takes it: the next frame counts in RX_DROP" (got 0 exp 1): `receipts/mbx/round2-arms.log`, `receipts/mbx/mutants-full-8f73ade5.log` (242/242) |
| R845-1 F2 MINOR (Tests, Robustness): filtered and runt frames behind a held one | B8, `suite.hpp:1694-1720`: a foreign-target command, a 22-byte frame cut inside target_entity_id, a 14-byte stub, all behind a held record: RATE_DROP + RX_DROP + mismatches 0, no ERR, the held record committed whole. Arm `rx-refused-behind-held-counted`, `mutants.py:683` (`rule_pass_w` dropped from `vd_rate_r`). | Caught by "B8 a frame the filter refuses behind a held one counts nowhere" (got 2 exp 0) |
| R845-1 F3 MINOR (Tests, Robustness): close with a frame held, not graded | Behaviour kept as documented (`docs/design/MAILBOX_SPLIT.md:296-299`) and graded: B9, `suite.hpp:1722-1745` (`FILTER_EN` cleared while held; waits for the refill; committed whole; the closed channel takes and counts nothing more). Arm `rx-release-gated-on-open`, `mutants.py:687`. | Caught by "B9 a frame held when its channel closes is still committed at the next refill" (got 16 exp 17) |
| R845-1 R1 / R846-1 R1 (residue): issue-comment ID in source comments | `KL_mbx_rx.sv:39`, `mailbox.yaml:1098`, `suite.hpp:785`, `:1544`, `mutants.py:647`: "#917; #665 ruling item 2" / "#665 ruling item 2". Prose pages keep the link (MAILBOX_SPLIT.md:275). | `git diff cec88385..8f73ade5` adds no line with `6894152131`; a grep of every source type in the tree finds none |
| R845-1 R2 (residue): "What is dropped" overstated | `MAILBOX_SPLIT.md:306-311` (the reviewer's wording, plus the filtered and RX_DROP cases); `KL_mbx_rx.sv:46-49` and `mailbox.yaml:1098` say the same. | B7 (RX_DROP), B8 (counted nowhere) |
| R845-1 S1 (suggestion): state the one-in-flight limit | Taken: `MAILBOX_SPLIT.md:312-317` "Its limit"; PR body Known limitations. | B1 |
| R846-1 F1 MINOR (Conformance, Docs): 9.2.2.4 for one in flight; the bench deadline called a timeout | One in flight is #917's measured workload; a controller may pipeline (9.2.2); timeout and retry 9.3.2.6, 9.3.6: `KL_mbx_rx.sv:38-43`, `MAILBOX_SPLIT.md:277-281`, `suite.hpp:393-400` (B0's deadline is next-refill delivery, not the 250 ms timeout), `suite.hpp:1544-1549`, PR body Description and references. 9.2.2.4 remains only as the message_type cite in the filter tables (unchanged lines). | Clauses checked in IEEE 1722.1-2021 (9.2.2 pipelining; 9.3.2.6 250 ms timeout, respond within 240 ms; 9.3.6 the in-flight list); B0, B1, B2 green and `rx-drop-instead-of-hold` caught by B0 |
| R846-1 F2 MAJOR (Conformance, Tests, Docs): ingress allowance and budget attribution | Section 2 | Section 2 |

## 2. R846-1 F2, as the manager ruled

- **Allowance per path, stated once.** `docs/reference/FR_NFR.md:422-425` (3.4.1): a token record 64 clocks /
  1 ms; a held record one refill period of its channel plus 1 ms. `MAILBOX_SPLIT.md:300-305` ("Its ingress
  allowance") links there and to the generated table; it restates no figure.
- **Derived, never mirrored.** `sw/mailbox/mailbox_emit.py:217-231` (`T_INGRESS_MS = 1`): the channel table of
  `docs/reference/MAILBOX_CONTRACT.md` gains "Ingress allowance, held record" = `refill_ms + 1` (adp 11, acmp 6,
  aecp 6, maap 21, srp 3 ms). Package, skeleton and C header byte-identical; `gen_mailbox --check`,
  `--crosscheck`, `--selftest` pass. The budget harness reads `refill_ms` from the contract (`held.py:28-30`)
  and states `INGRESS_MS = 1.0` as FR_NFR's T_ingress (`held.py:20-21`).
- **Margins recomputed.** `FR_NFR.md:429-434`, token / held, at the 20 ms bound and at the 10 ms proposal: ACMP
  178/173 (188/183), AECP 240 ms 218/213 (228/223), AECP 250 ms 228/223 (238/233), MVU 218/213 (228/223). A
  search of the docs for other numeric margins that subtract T_ingress found none (the IN_PROGRESS and
  notification rows of the ceiling table state no margin figure).
- **Attribution.** `tb/verilator/ctrl_service_budget/held.py:33-70`; `grade.py:149-170` (`last_frame`, `owner`),
  `:199` (RXH/RXR), `:266` (unserved), `:364` (the rxh start), `:480`, `:618` (ingress fields); observation in
  `observe.vlt:41-42` (hold_w, rel_w), `build.py`'s `rx_hold` and `rx_release` accessors, `sim_main.cpp:120-124`.
  A commit is credited to its own held frame; a commit on a channel holding none (a duplicate, another
  channel's), a second hold, a commit not after its frame's last byte or past the allowance (misordered, late)
  are refused; a record never committed is refused and not served (missing).
- **Scenario.** Group `aecp-held`, `held.py:88-119`; point `8x8-1if` added (`run.py:40-42`).
- **Negative control.** `selftest_mutants.py:446`: `held.release` replaced by the old `owner()` rule; caught by
  "a held record's commit belongs to its own held frame, measured from its last byte".
- **Results, no bound changed.** 1x1: 5.236 ms (ingress 4.986 of 6), bound 20, rc 0, 0 refusals, misses and share
  overs. 8x8/1if: 5.114 ms (ingress 4.986 of 6), 0 refusals, misses and share overs; rc 1 from three STATED
  lines only (section 4). On the real logs (`receipts/budget/held-*/attribution-evidence.txt`): one RXH and one
  RXR each, the held record credited to the probe, the two followers refused, the old rule refusing the log
  ("the receive commit at 100500065 follows no frame").
- **Population.** Not rerun: the round-2 grader regrades the recorded cec88385 and 84d8a214 1x1 logs with
  `table.md` and 94/94 group grades byte-identical (`receipts/budget/regrade/`). Those logs hold nothing: under
  the round-1 grader a hold's commit would have followed no frame, a refusal, and both recorded runs have 0.

## 3. Gates at 8f73ade5 (clean clones; receipts/INDEX.md lists every file)

| Gate | Result | Receipt |
|---|---|---|
| Local: lint_rtl --check, gen_mailbox --check/--crosscheck/--selftest, docs_check, check_doc_paths, check_em_dash --base cec88385 and --selftest, py/cpp/sv/sh idiom gates | all rc 0 (lint 89 <= 89; the py long-module and long-function and the cpp long-function counts at their ratchets) | `local/local-gates-8f73ade5.txt` |
| Native shard 1/4 (holds mbx) | 17 of 17 pass: 16 in the shard run (`mbx`: 622 Wishbone, 667 AXI4-Lite, 32 co-simulation, 629 and 674 at two interfaces, 547 on the host model, 13 of 13 quick mutants, the mover 24 of 24), and `milan_dp_render`, which the shard's 1800 s wall clock cut under CPU contention (result unknown), rerun on a fresh clean clone: PASS | `sweep-8f73ade5/` |
| `make -C tb/verilator/mbx mutants` | 242/242 caught after 4 positive controls | `mbx/mutants-full-8f73ade5.log` |
| Round-2 arms one at a time | the three new arms and the corrected-row arm caught by their named checks | `mbx/round2-arms.log` |
| Workflows step by step (rtl-fast, elaborate, docs, rtl yosys shards 0-3, yosys-portability, full-ci-gate, yosys-tool) | 139 steps rc 0, 226 not run with a stated reason (hosted orchestration, package installs this host already has), 0 bad; firmware control mutants 699 of 699 caught | `workflows/` |
| CPU budget self-test | 0 failures, 214 mutants caught (213 at 3926c271) | `budget/selftest/` |
| Held legs 1x1, 8x8/1if; the no-hold `aecp` control at 8x8/1if | as section 2; the control 25/25 rows within budget, 0 hold lines, the same three STATED lines | `budget/held-*`, `budget/aecp-8x8-1if-control/` |
| KL_mbx_rx sv2v, 3926c271 against 8f73ade5 | byte-identical (50b2e99a...), 0 non-comment lines changed: no route needed | `sv2v/rtl-comment-only.txt` |
| Firmware images against cec88385 | 46 fixture images identical; split 1x1/1if bb04b696 145,496 B and 8x8/1if 506a1ae4 158,176 B, ROM banks and xdc identical to round 1 and the base | `images/` |

## 4. Open risks / questions

- **8x8/1if STATED lines (not rows, not a STOP).** Three link-up MRPDU build passes over `ctrl_loop.h`'s
  stated costs, which `MBX_N_IF == 1` selects with the 1x1 figures: 120,704 and 117,875 CPU cycles against
  101,000, a build-one pass of 95,723 against 43,000, at about 113.6, 311.2 and 511.2 ms, during ready(). The
  existing `aecp` group (no hold, 0 RXH/RXR lines) shows the same three at the same cycles, so they are the
  point's, not #917's; every row of both groups is within its bound. No cost or bound changed. For #914's
  8x8/1if measurement (the stated costs or the point's figures need an owner).
- **8x8-1if is a new harness point** (`run.py:42`), added for the ruling's "1x1/1if and 8x8/1if"; this lane has
  not run the 94-group population there.
- **Hardware acceptance owed**: three descriptor walks with none unanswered, on the test machine. `Closes #917`
  in the PR body would close the Issue at merge before that; the manager may prefer to keep it open.
- **Directive choice** (unchanged from round 1): AltSpreadLogic_high and ExtraTimingOpt meet the #870 hold floor
  (+0.030 ns); ExtraPostPlacementOpt reaches +0.016 ns (it meets #818's WHS >= 0).
- **Pre-existing**: the budget harness cites MAILBOX_SPLIT.md by line number, stale at the base; worth an Issue.
- **Lens coverage**: KL_mbx_rx.sv changed only in comments (sv2v identical) since 3926c271, where both reviewers
  found the RTL lens CLEAN; whether that stands is the reviewers' call. Every other lens's artifacts changed.

## 5. Process notes

- Every command ran in the foreground (waits under 10 minutes), heavy work in transient units with MemoryMax
  10G on CPU ranges from cpu_ranges.py; one budget build per clone (the 8x8/1if leg moved to its own clone when
  two would have shared one).
- No push, no PR edit, no comment but the one REVIEW READY; nothing deleted but this lane's own scratch.
