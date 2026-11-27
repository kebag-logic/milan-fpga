[R957] NEGATIVE - exact head 25ff0632c4ed312d57cad78783474308c92dd21f

# R957-2: internal independent review of PR #993 (#977), rounds 9 to 10d

- Head: `25ff0632c4ed312d57cad78783474308c92dd21f`, tree `a5fa7c04b11c14c919f821f0075888a0633532c9`. The PR is a draft against `dev-soft-core`.
- Previous reviewed head: `095995243bc354b8a41755f3fdfae343511cc668`. The delta is 73 commits: 36 lane commits, plus the merges of `dev-soft-core` `71bad8c0` (PR #1017, PR #1019) and of PR #1015's head `35d29eb7`.
- All five lenses were applied at this head. One MAJOR finding is open, so Conformance, RTL, Tests and Docs stay unclean. Robustness is covered clean.
- Every finding of round 1 (internal R957-1 and external R958-1) is closed at this head (section 2).

## 1. How the task was reconstructed

Read in this order:

1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
2. Issue #977: its body and frozen acceptance, and the rulings and owner decisions on it:
   - 7091882145, 7160202807, 7180135694 and 7210516620;
   - the scope of this round: 7210763364 (population bound V), 7212897415 (delivery bound, fourth hot window, three groups, S14), 7216582862 (alone records, base 350 / walk 150, THE SETTLE row term, no binding change in a record's pass);
   - the owner decisions 7213594113 (8x8/1if load ceiling 0.77) and 7217388999 (THE TRANSMIT's 8x8/1if figure 80 ms);
   - the owner's 2026-11-15 rule on loose block RAM (#665, issuecomment-6892332745).
3. The diff `09599524..25ff0632`, both as a whole and as the lane's net delta after the merges (`aad9a682..25ff0632`, 53 files).
4. The author's packet `review-evidence/977-r1/author-r10` at `da2acce9`.

The round-1 findings were read only after my own pass over the diff and my probes.

## 2. Round-1 findings, resolved at this head

| Finding | State | Evidence at `25ff0632` |
|---|---|---|
| R957-1-F1 MAJOR: a LeaveAll vector of no values ended the charge's Message walk | **Closed** | `srp_mbx.c:1048-1054`: only a VectorHeader of 0 ends the Message, and a 0-value vector skips its header and FirstValue. Plant `srp-977-charge-leaveall-ends-the-message` is caught at 1x1/1if and 8x8/1if (author's shard receipts at `25ff0632`, test `Srp.TheDrainChargesARecordTheTalkersItsVectorsCanRegister`, "a LeaveAll of no values ahead of two Talker values"). The group `srp-register-leaveall` in lwSRP's own shape is measured at both points (`agg-e59cf6ea.txt`, `regcost-*.txt`). |
| R957-1-F2 MAJOR: unpublished lwSRP pin | **Closed** | The pin is `e27b34c9`, the merge commit of lwSRP PR #22 (merged), and lwSRP `main` is identical to it (compare API: identical, 0 ahead / 0 behind). |
| R957-1-F3 MINOR: the alone rule was gated only on its settle condition | **Closed** | `drain-alone-past-a-tier-1-record` and `drain-alone-past-a-centisecond` are both caught (`[ok] mutant ... 1 check(s) failed`, shard receipts). |
| R957-1-F4 MINOR: the round-7 decision was not public | **Closed** | The STOP (7210514658) and the decision (7210516620) are on #977. The bound `ADP_MBX_LAT_LINK` 12 now reaches the base through #1015 (merged into `dev-soft-core` as `0b594023`), so it is no longer this PR's net delta. |
| R957-1-R1 RESIDUE: round labels, a comment ID and "S14" | **Closed** at the cited sites | `aecp_mbx.h:78`, `ctrl_loop.h:394-399`, `flip_grade.py:62-65`, `load_grade.py`, `poll_grade.py` and `whole_grade.py` no longer carry them. `ctrl_memory.py` names "the hybrid XIP lane's issue", the wording that finding proposed. New instances are listed in R1 below. |
| R957-1-R2 RESIDUE: stale PR title | **Closed** | The title is "Register Talkers at the MRP state machines' rate within THE SHARE (#977)". |
| R958-1-F1 MAJOR: the charge capped vectors at the sinks while bound and kept Talkers coexist | **Closed** by ruling 7210763364 | Kept ≤ min(SRP_KEPT_TALKERS, V − bound) (`srp_mbx.c:565-576`). The charge caps each vector at V and the fallback at V per 28 octets (`srp_mbx.c:1036`, `:1053`). `_Static_assert` at `srp_mbx.c:30`. Plants `keep-past-v`, `keep-bound-sinks-uncounted`, `charge-vector-at-the-sinks`, `charge-fallback-at-the-sinks`, `early-keep-bound-uncounted` and `early-keep-room-short` exist. The group `srp-register-population` (bound and kept at V) is measured. |
| R958-1-F2 MINOR: harness README ledger limits | **Closed** | `tb/verilator/ctrl_service_budget/README.md:422-423` state 62.5 and 58.5, which equal `ctrl_memory.LEDGERED` (`8x8-two-interfaces` 62.5, `8x8-one-interface` 58.5). |
| R958-1-F3 RESIDUE: round labels and the "arm A" label | **Closed** at the cited sites | `register_window.py:3-4` reads "the default (none) arm". The other sites are as for R957-1-R1. |

## 3. Findings at this head

### R957-2-F1 MAJOR (Conformance, RTL, Tests, Docs): the swap's deferred binding changes are source work that no load term counts, and counted they can put 8x8/1if over the owner's 0.77

This is open point (1), decided here.

**Location**
- `tb/verilator/ctrl_service_budget/load_grade.py:8-9`, the model's premise: "A pass's own cost (its events' fixed part and its polls' base) is not a source, so it is not a term".
- `load_grade.py:586-588`, the registration term.
- `sw/firmware/ctrl/app/ctrl_app_srp.c:140-207`, the delivery bound.
- `docs/design/SPLIT_CONTROL_MEMORY.md:2548` ("The load term counts neither").

**Authority**
- Acceptance 4 of #977: the owner bounds hold unmoved.
- Owner decision 7213594113: 8x8/1if at 0.77, decided on the "all-in" per-Talker cost.
- Ruling 7212897415, item 5, and ruling 7210763364, item 6: STOP if a load check fails, or if a restated cost pushes a load past its bound.
- The load model's own rule (`load_grade.py:15-16`): "No term is kept as a margin: each has its source, and one without a source fails".

**Evidence**
- The binding change and the loss completion run inside `deliver`, a poll, so they are part of a pass's polls base (`poll_grade.py:8`). The load grader leaves the base out of the load by construction and only reports it beside the load (`pass_own_us`, `load_grade.py:605-608`).
- `REGISTRATION_US` (190 µs at 8x8/1if) is the record's apply past the unit plus THE SETTLE's run after it (`regcost3.py`). It does not include the later deliveries.
- Under the delivery bound, a swap record (Lv of the registered kind with New of the other, IEEE 802.1Q-2018 35.2.6) leaves V Listener re-declarations, one binding change for each delivery. The design document says so itself (`SPLIT_CONTROL_MEMORY.md:2548`): "eleven passes of about 10,000 cycles, one binding change each".
- That work is caused by a source, the registering record, at the registration rate. The model's premise that the base carries no source work is therefore no longer true at 8x8/1if.
- The author's receipt (`postswap-8x8-1if.txt`) puts the added CPU share at:
  - 0.0019 when each pass's base is measured against the dearest base before the record (24,717 cycles), which gives a load of about 0.768;
  - 0.0136 when measured against the median base (13,249 cycles), which gives about 0.780, over 0.77.
- The dearest-before baseline is a lower bound on the added work. It subtracts the largest pre-record base, which is itself work the base carries and no term counts. The median is closer to a pass without the change.
- For scale: 0.0136 is about 70 % of the whole counted registration term (`registrations 0.019` in my `flip_grade.py --check --point 8x8/1if` run, `receipts/reviewer-checks-25ff0632.txt`).

**My decision on the author's question**
- The 350 µs base statement covers these passes in the rows. Each delivering pass is ≤ 33,565 cycles, against 35,000. The rows charge every pass its stated base, so the response-time rows hold them.
- It covers neither accounting in the load. The load excludes every pass's base by construction, so "which accounting the base already covers" has the answer "none".
- The work is real, sourced, and paid at the ruled rate. Under the more faithful baseline the 8x8/1if load check would fail.

**Impact**
- The 0.766 (against 0.77) evidence for acceptance 4 at 8x8/1if depends on an accounting choice the model does not state, and that choice leaves out sourced work.
- The load gate (`load_grade.py --check`, `flip_grade.py --check --point 8x8/1if`) cannot fail for the missing work.
- 1x1/1if is not at risk (0.524 against 0.70).

**Required outcome.** One of the following, recorded publicly before merge:
- (a) The deliveries' binding changes after a registering record become a sourced load term, or part of `REGISTRATION_US` (V a record at the registration rate, at a cost stated by the rule against a stated baseline), and the 8x8/1if load and flip checks pass with it.
- (b) If (a) does not fit under 0.77: the STOP to the owner that rulings 7212897415 item 5 and 7210763364 item 6 require.
- (c) A public owner or manager ruling that this work is outside the load model, with its reason written into `load_grade.py`'s premise and `SPLIT_CONTROL_MEMORY.md` section 13.

The executor may not choose between (a) to (c) privately (AGENTS.md section 2).

**Verification**
- For (a): `load_grade.py --check` and `flip_grade.py --check --point 8x8/1if` pass with the term present, and a planted control without the term is refused.
- For (b) or (c): the ruling link is cited in the PR body and in the two documents.

### R957-2-S1 SUGGESTION (Tests): the loss turn and the alternation's other direction have no test that can fail

- Location: `ctrl_app_srp.c:156-162` (`srp_loss_turn`), `:204-206` and `:165-170`.
- Probe: `scripts/deliver_probe.py` with the mutants in `scripts/deliver_mutants.tsv`. Receipts: `receipts/deliver-mutants.txt` and `receipts/deliver-control-8x8.txt`.
- These mutants pass the whole SrpBinding suite (20 of 20) at 1x1/1if and 8x8/1if:
  - the loss turn taken from the first sink;
  - the loss turn never advanced;
  - a loss always preferred over an owed binding change;
  - the loss chosen in a record's pass.
- These mutants are caught: the bind turn kept (D2), and a parked request unbound outside its turn (`ParkedReplacementRetiresThePreviouslyAcceptedBinding`).
- The surviving mutants are near-equivalent at the measured shapes:
  - At both one-interface shapes, any re-registration needs a record, and the record's SETTLE completes every loss.
  - At every shape a sink's loss cannot recur faster than a LeaveTime.
- So the ruled bound of 2 × CTRL_SRP_SINKS deliveries still holds. The code comment and `srp_deliver_mutants.py` nevertheless state "each the first owed from its turn" for losses too.
- Suggested: a D2-style test that re-latches one sink's loss before each delivery, and a plant for the loss turn. Alternatively, comment that the loss turn is a tie-break only.

### R957-2-R1 RESIDUE (Docs): comment-rule wording in the delta

All of these are wording only (owner rule 2026-10-15). Receipt: `receipts/comment-rule-scan.txt`.

- **Review-round labels.** Nine new source lines cite "#977's ruling on round 9's STOP":
  - `sw/firmware/ctrl/app/ctrl_app.h:107`
  - `sw/firmware/ctrl/app/ctrl_app_srp.c:142-143`
  - `sw/firmware/ctrl/test/srp_binding.hpp:235`, `:376`
  - `sw/firmware/ctrl/test/srp_deliver_mutants.py:3`
  - `sw/firmware/ctrl/test/test_plat_sinks.cpp:1626`
  - `tb/verilator/ctrl_service_budget/load_grade.py:363`
  - `tb/verilator/ctrl_service_budget/register_window.py:247`, `:287`

  Exact fix: replace "ruling on round 9's STOP" with "ruling of 2026-11-27 on the delivery bound", and keep the item numbers.
- **Ambiguous citations.** 13 new citations read "#977's ruling of 2026-11-27, item(s) N", for example `srp_mbx.c:557`, `:1017`, `srp_mbx.h:161` and `ctrl_loop.h:347`. Four rulings and decisions carry that date. Exact fix: "#977's ruling of 2026-11-27 on the population bound, item N".
- **Suggestion.** The debt owner "the hybrid XIP lane's issue" (`ctrl_memory.py:275-445`) is the wording round 1 proposed and is acceptable. Naming the issue number would remove the lane name altogether.

### R957-2-R2 RESIDUE (Docs): THE TRANSMIT's figure cites the row at the superseded SETTLE

- Location: `sw/firmware/ctrl/loop/ctrl_loop.h:394` and `docs/design/SPLIT_CONTROL_MEMORY.md:3093`. Both read "80 ms ... for the 79.48 ms of its row ... with its SETTLE".
- The graded row with the SETTLE of 425 µs is 79.49 ms. It is stated so at `SPLIT_CONTROL_MEMORY.md:2548`, and `flip_grade.py --check --point 8x8/1if` prints "HELD 8x8/1if: THE TRANSMIT's figure CTRL_LOOP_TX_MS 80 ms against its tx row by every source 79.49 ms".
- Exact fix: "for the 79.49 ms of its row (79.48 at the ruling's 415 us SETTLE)". The figure, 80, does not move.
- With the owner's decision taken, keeping `70468e2a` droppable no longer needs the older number.

### R957-2-R3 RESIDUE (Docs): the PR body's run counts

- Location: PR #993 body, "Measured at this head", row "Group runs": "289 + 2 pairs, every one exit 0 (...)". The same claim is in REVIEW-READY.md, "all exit 0".
- In each 289 at each point, 4 runs exit 1: srp-kept and srp-bound alone in two arms, refused by `kept_grade`'s pairing (`groups-e59cf6ea.csv`, `agg-e59cf6ea.txt`).
- Exact fix: "289 + 2 pairs: 285 exit 0, and the 4 single srp-kept and srp-bound runs are refused by `kept_grade`'s pairing and pass as the 2 pairs".
- In the packet only, `receipts/INDEX.md` lists `fwgate-shard{1,2,3}-*.txt.gz` and `harness-run.py_--self-test-*.txt.gz`, which are published as `.txt`.

## 4. Open points the author raised

1. **The post-swap delivering passes.** Decided in F1: the base statement covers them in the rows but not in the load. This needs a counted term, a STOP, or a public ruling.
2. **The 8x8/1if platform ROM entry, 60.5 → 61.0 RAMB36.** It conforms to the owner's rule of 2026-11-15:
   - an image past its entry raises it to its measured size at the next half tile, as named debt;
   - the image still has to fit the device and meet timing.
   - The facts: `rom` 147,712 B, 256 B past the 147,456 B of 60.5 (`plat_ledger.txt`, `elf-identity-final.txt`). The debt is named (`ctrl_memory.py`, `SPLIT_CONTROL_MEMORY.md:169`). The 8x8/1if route gives WNS +0.092 ns, WHS +0.036 ns, 0 routing errors and 100.5 BRAM tiles (`route-8x8-1if-e59cf6ea.txt`). No finding.
3. **The author's logged slips** (HANDOFF-r10d.md):
   - one `rm` ran before its log line, removing a packet copy of a failed route receipt (the scratch original was kept);
   - a build attempt was launched outside the build environment;
   - D6 failed at 1x1/2if and was fixed per shape in `e59cf6ea`;
   - six plants had lost their sites and were re-pointed in `2e466ae9`;
   - coverage found the untested `bind = n`, now covered by D7 and its plant;
   - one over-long Python line was wrapped.

   Each was caught by a gate or logged, and fixed before the head. None affects the head's bytes or evidence. No finding.

## 5. Checked within each lens

The lenses named in F1 stay unclean because of F1.

**Conformance**
- Ruling 7210763364:
  - V is 4 at 1x1/1if and 9 at 8x8/1if (`srp_mbx.h:161-171`);
  - the charges are 725 µs and 1,500 µs;
  - LeaveAll handling follows 10.8.1.2 and 10.8.2.8 (`srp_mbx.c:1048-1054`);
  - the four new groups are measured.
- Ruling 7212897415:
  - one delivery makes one of a binding change and a loss (`ctrl_app_srp.c:146-207`; stricter than "at most one each", in line with ruling 7216582862 item 2);
  - the fourth window is in the hot list (`filter-c63e9d58.txt`, 290 entries, 72 of 72 maps clean);
  - the three groups exist;
  - the S14 split is in `test_plat_sinks.cpp:1557-1649`, with plants `PAST` and `REBOUND_B`.
- Ruling 7216582862:
  - `CTRL_LOOP_ALONE_US` is 925 at 1x1/1if (87,826 × 1.05 → 925) and 1,840 at 8x8/1if (≤ 1,935, above the 1,805 that the measured 171,622 cycles state);
  - the base is 350 and the walk 150 (`poll_grade.py:158`);
  - the SETTLE row term is 105 and 425, the latter restated upward by the rule from 40,049 cycles;
  - the settles guard is in place (`ctrl_app_srp.c:149`).
- Owner decision 7213594113: `flip_grade.py:62-65` sets the ceiling at 0.77.
- Owner decision 7217388999: `CTRL_LOOP_TX_MS` is 80 at 8x8/1if, and the hold-off `(80+9)/10` stays 8 cs (`srp_mbx.c:58`).
- My reruns at the head (`receipts/reviewer-checks-25ff0632.txt`):
  - load: 0.524 and 0.766;
  - 1x1/1if rows: ACMP 29.51 (30), txL 48.08 (49), last notice 133.91 (135), tx 33.89;
  - 8x8/1if tx row: 79.49 against 80;
  - the 1x1/1if and 8x8/1if checks print `RESULT: PASS`, and `shape_costs --check` passes.
- Pass lengths from `agg-e59cf6ea.txt`: 1.557 ms and 1.930 ms, both < 2 ms. Over-statements: 0.

**RTL** (firmware architecture; there is no HDL or CDC change in the net delta)
- `deliver`'s bind and loss selection, its turns, and their reset in `ctrl_app_attach_srp` (`:236-238`).
- A bind candidate is never a loss candidate, since `delivered()` excludes pending and parked requests. So `k != bind` is redundant but harmless.
- `keep_talker`'s shrinking room once bound sinks grow. It is held by `count_kept` and the plants.
- `index_sinks` counts `bound_sinks`.
- Widths: the `uint8_t` turns hold indices below `CTRL_SRP_SINKS < 255` (`srp_mbx.c` `_Static_assert`).
- ADP's clock seed is wired at boot (`ctrl_plat.c:135-140`, `:401`), from #1015.

**Robustness: CLEAN**
- Parked, pending, settles and failed-bind retry paths. A refused `srp_mbx_bind` keeps `pending` and its turn advances.
- A LeaveAll vector of 0 values, and the fallback past eight Messages.
- Kept entries past V after a bind. Recomposition reset.
- Six mutation probes (S1): every one that changes reachable behaviour at the measured shapes is caught.

**Tests**
- D1 to D7 with their nine plants (`srp_deliver_mutants.py`).
- S14 and S14b with their plants.
- The control probe passes 20 of 20 at 8x8/1if (`receipts/deliver-control-8x8.txt`).
- The author's gate receipts at `25ff0632`:
  - shards 0 to 3 PASS, with 873 of 873 mutants caught in shard 1;
  - coverage PASS (40 files);
  - the hot-list check and self-test, `plat_ledger --self-test`, the twin, and the C++ and Python idiom gates.
- My reruns: `load_grade --selftest` 28 of 28, `flip_grade --selftest` 628 of 628, `shape_costs --selftest` 25 of 25, `kept_grade --selftest` 33 checks, and `check_py_idiom` rc 0 (`receipts/rv-*.txt`).

**Docs**
- `SPLIT_CONTROL_MEMORY.md:169-171` and `:2548`, `FR_NFR.md`, the SRP README `:152`, the harness README `:422-423`, `SUBMODULES.md` (pins `e27b34c9` and `5a07d9b7`).
- The PR body is byte-identical to the packet's `PR-BODY.md` (sha256 `0ecd6144…`).
- The docs workflow at `25ff0632` ran 100 of 100 steps.

**Integration**
- The merge `8d573763` resolved conflicts in `SPLIT_CONTROL_MEMORY.md` and `test_ctrl_firmware.py`. The second keeps both #1019's `[share]` slicing and #977's prefix filters. The `#1009` text the first resolution dropped is restored at `SPLIT_CONTROL_MEMORY.md:170` and `:332`.
- The merge `aad9a682` resolved conflicts only in the pin docs and the diagram (`receipts/lane-merges-remerge.txt`).
- `git merge-tree` of the head onto `dev-soft-core` `0b594023` (which contains #1015, #1017 and #1019) is clean, and its tree is `a5fa7c04`, the head's own (`receipts/merge-tree-dev-soft-core.txt`).
- The pins:
  - tsn-c-stack `0f72ca69..5a07d9b7` has an identical tree, and `5a07d9b7` is the merge of PR #41 and equals `main`;
  - lwSRP `73007b48..e27b34c9` adds comments and the `RX_KEPT` macro in `src/`, which is consistent with the 80 of 80 identical ELFs (`pins/elf-identity.txt`);
  - `70468e2a` (77 → 80 ms) gives 80 of 80 identical ELFs (`tx80-elf-identity-e59cf6ea.txt`);
  - the head's 80 ELFs equal `e59cf6ea`'s measured images, and both routed images are matched by hash (`elf-identity-final.txt`).
- The packet's manifest: 97 of 97 author-r10 files match their published sha256, and none is unlisted (`receipts/manifest-author-r10.txt`). The packet is hash-manifested. Its commit is not cryptographically signed.

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #977 acceptance and rulings 7210763364, 7212897415, 7216582862; owner decisions 7213594113, 7217388999; the #665 rule of 2026-11-15; `srp_mbx.c:30,557-576,1007-1056`; `srp_mbx.h:161-171`; `ctrl_app_srp.c:133-207`; `ctrl_loop.h:343-450`; `load_grade.py:1-30,560-608`; `poll_grade.py:100-159`; `rows_grade.py:99-103`; `flip_grade.py:62-65`; my `load/flip/shape --check` reruns | R957-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| RTL | UNCLEAN (F1) | `ctrl_app_srp.c:57-246`; `ctrl_app.h:103-110`; `srp_mbx.c` keep_talker, index_sinks, rx_charge; `ctrl_loop.h` shape table; `ctrl_plat.c:135-140,401`; `ctrl_split.ld` and hot-list receipts; the lwSRP `src/` diff `73007b48..e27b34c9`; the route receipts | R957-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| Robustness | CLEAN | `ctrl_app_srp.c:146-207` parked, pending, settles and failed-bind paths; `srp_mbx.c:1036-1056` zero-value and fallback paths; `srp_mbx.c:565-576` shrinking keep; probes `receipts/deliver-mutants.txt` and `deliver-control-8x8.txt` | R957-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| Tests | UNCLEAN (F1) | `srp_binding.hpp:376-520` (D1 to D7); `srp_deliver_mutants.py`; `srp_drain_mutants.py`; `sink_mutants.py:77-251`; `test_plat_sinks.cpp:1557-1649`; `test_port_loop.cpp`; `srp_mbx.cpp`; the author's gate receipts `r10d/gates/final/*`; my self-test reruns `receipts/rv-*.txt` | R957-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |
| Docs | UNCLEAN (F1) | `SPLIT_CONTROL_MEMORY.md:166-171,332,2548,3093`; `FR_NFR.md`; `sw/firmware/ctrl/srp/README.md`; `tb/verilator/ctrl_service_budget/README.md:418-423`; `SUBMODULES.md`; the PR #993 body; the packet REVIEW-READY.md, HANDOFF-r10d.md and INDEX.md | R957-2 | 25ff0632c4ed312d57cad78783474308c92dd21f |

## 7. Real limits

- Not run by this review: the firmware gate with planted defects, the CPU budget harness pools (578 runs and 4 pairs), the routes, the twin, coverage, the docs workflow, and ELF builds. Each was judged from the author's published receipts, whose hashes I verified, and from spot checks.
- `sw/litex/test_ctrl_memory.py` could not run here, because migen is not installed. I rely on the author's PASS receipt for it.
- My probes covered only `test_acmp_mbx.cpp`'s SrpBinding suite, at the two one-interface shapes, on disposable copies under `scratch/`. The pinned Verilator was not needed and not used. The clone was restored, and its tree, index and gitlinks were verified byte-exact (`receipts/tree-restore.txt`).
- F1's 0.0019 and 0.0136 shares are the author's measurement. I did not re-derive them from the raw harness logs, which are not published.
- No hosted run exists at this exact head: 0 check runs, 0 workflow runs, combined status pending with 0 contexts (`receipts/hosted-25ff0632.txt`).
- No manager source bank ran at this head, and none is claimed. Physical calibration was NOT RUN, and nothing here is hardware evidence.

## 8. Pending manager duties

- Bring F1 to a public decision: a counted term, a STOP to the owner, or a recorded ruling.
- Carry R1, R2 and R3 to the residue checklist.
- At the merge turn, build and validate the current-dev merge candidate. The source base is `dev-soft-core` `0b594023`, and the trial merge gives tree `a5fa7c04`. Live `dev` is `e275d795`.
- Own the hosted and act acceptance. The PR is a draft and has no exact-head hosted jobs yet.

R957-2 FINISHED
