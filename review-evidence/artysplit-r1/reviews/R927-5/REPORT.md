[R927] NEGATIVE - exact head c0b625d1792e61b8e99944daea65b842e6b9dcde

# R927-5: internal cleared-context re-review of PR #1004 (relates to #878), rounds 9 to 11

Head `c0b625d1792e61b8e99944daea65b842e6b9dcde`, tree `1f528462806ea0a8262320787e7c3cbb2431b0f7`. Delta since my last reviewed head: `011aaa6f..c0b625d1`, 19 first-parent commits. These include the merge `aa53840d9` of live dev-soft-core `0b594023`, the 100 Mb/s egress gate, the Arty bind-save bounds, the bare-metal rewording, the console coverage exclusion and the regenerated register reference. Evidence: `review-evidence/artysplit-r1/author-r10` and `author-r11` at evidence commit `3e8f3014f28d13bd008b06ec43f919d282d681ee`.

**Verdict: NEGATIVE.** Five new MINOR findings are open: F1 under `Tests`, F2 and F3 under `Docs`, F4 under `Conformance` and `Docs`, and F5 under `RTL` and `Docs`. Only `Robustness` is covered clean at this head.

**What does hold, from my own runs at this head:**
- The round-10 census extract regrades identically at the head: 159 of 159 cases and the cross-case step PASS, line for line equal to the author's round-11 log. The no-`srp-bound` copy is refused by the #977 disposition.
- The 100 Mb/s egress row is 505.738 us from the published observations, byte-identical to the author's grade. The replay agrees exactly with the testbench in every case (0 ps).
- The fixed path measures 312.5 ns on the converted MII chain, stated as 320 ns.
- The egress self-test passes (17 of 17), and so does the census-extractor self-test (6 of 6).
- The merge resolution is meaning-preserving.
- The only firmware-side change since `640699e6` is a comment in `ctrl_loop.h`, identical once comments are stripped (667 lines both). So the three shipping ELFs cannot differ from `640699e6`'s, and the author's receipt states the three hashes.
- The prior internal findings R927-3 F2 and RS-1 are closed at their cause.

## 1. Scope reconstructed from public state

| Authority | What it requires of this delta | Where checked |
|---|---|---|
| Egress ruling on #1020 (comment 7216971645), merge gate on #1004 (7216972073) | At 100 Mb/s `T_egress` is a held row. The 147 retained traces' commits are replayed through the shipping TX queue (rings, store-and-forward FIFO, 80 ns per wire octet, SR and gPTP frames). Two conditions: (a) every commit's free-space test keeps its census outcome, and if it does not, the census is re-run at link rate (item 3); (b) the largest commit-to-last-octet wait × 1.05 plus the fixed path is at most 1000 us. A grader with planted defects is required, and FR_NFR 3.4.1 states the row with 254 records | §2, F1, F4 |
| Bind-bound ruling (7221391389) | The in-flight bound at `arty-1x1` is the rest of the save plus one save, from the census model's save time. The burst count follows the same rule. State the bench figure beside it and say which one the rule uses | §2 |
| Held-egress ledger ruling on #1020 (7234489667) | The USB-network Arty is its own ledger point (62.14 ms, `USB_NET_PATH.md`). The 1x1 Arty's figures are unchanged | §2: no 62.14 ms point is in this tree, which is correct, since it belongs to #1020. `egress_ledger.ARTY` (`egress_ledger.py:96-99`) is unchanged across the delta, as the ruling requires |
| AGENTS.md §6 and §7, and the owner's comment rule | Lens coverage per head; no comment IDs in source comments | Ledger; RS-4 |

## 2. Delta checks

| Item | Result | Evidence |
|---|---|---|
| Merge `aa53840d9` | The tree differs from `git merge-tree 011aaa6f 0b594023` in three files only. In `ctrl_mutants.py`, the one conflict, the lane's fixture import is kept and dev's `CDL_BOUND` moves to `ctrl_mutant_fixtures.py:54`. It is used by all five pin mutants (`ctrl_mutants.py:579-591`), and their strings equal dev's. In `run.py`, a docstring is reflowed and a comment removed. No lane label from dev's side returned | `git diff <auto-merge> aa53840d9` |
| Gateware inputs changed by the merge | Only the `gptp-processor` gitlink (`3ce71b76`) and `syn/yosys/rom_digests.tsv`. Builder outputs differ only in `gptp_ucode.hex` (author `builder/builder-split.log`) | `git diff --stat 011aaa6f aa53840d9 -- hdl configs sw/litex syn gptp-processor` |
| (a) free-space outcomes | Item 3 applies: the instant-egress replay changes 11 of 159 outcomes (author `egress/all.log`). So the census runs drained at link rate: `sim_main.cpp:150,170,259` drives the mailbox's `tx_ready` from `egress_queue.hpp`, and each TX_TAIL read the firmware makes is its own against the link-rate tail | Code read; `grade.py:276-277` skips the new lines; census source head `7bc47c0e`, after which nothing in firmware, RTL or the testbench changed (`git diff --stat 7bc47c0e c0b625d1`) |
| (b) the row | `EGRESS100 wait 426.470 us + gPTP 54.88 us, x 1.05, + fixed 0.32 us = 505.738 us`, PASS. 159 cases, 27,924 records, 44 of them held, in `aecp-outputs` (18) and `backlog-owed` (26). At most 19 records queued at once | `receipts/egress-packet.log` (byte-identical to the author's `consistency/extract-egress.log` on every GRADED, EGRESS100 and RESULT line), `receipts/egress-packet-summary.txt` |
| Queue constants against sources | Gasket `GAP_CYCLES(512)`: its counter loads `GAP_CYCLES-1` and gates while counting, so 513 is used (`hdl/common/tx_ifg_gasket.sv:36-51`). CDC depth 16+1, store-and-forward FIFO 512/8, overhead 60/4/8/12 (`sw/litex/milan_soc.py:1483-1499`). Rings 128/256/512/128/512 hold 21+42+85+21+85 = 254 six-word records (21,336 wire bytes). The gPTP burst works out to 686 octets = 54.88 us | Hand arithmetic |
| Fixed path | 312.5 ns at most over 7 lengths × 64 phases; stated 320 ns; PASS | `receipts/egress-fixed.log` (pinned Verilator 5.050, identity `Verilator 5.050 2026-07-01 rev v5.050`) |
| Grader self-tests | `egress_mii --selftest` 17/17. `--structural`: 391.51 us, 2177.82 us, 2646.82 us. `census_extract --selftest` 6/6 | `receipts/egress-selftest.log`, `egress-structural.log`, `census-extract-selftest.log` |
| Census regrade at the head | `RESULT: PASS cases=159 worst_pass_cycles=143181` and the cross-case PASS. Every PASS/RESULT line equals the author's `author-r11/receipts/consistency/extract-regrade.log` | `receipts/regrade-r10-extract.log`, `.rc` = 0 |
| Control | 158 cases reproduce, then the run is refused: `REFUSED #977 ... graded srp-kept alone` and `owner model or case count differs from the published qualification`, exit 1. Every PASS/REFUSED/RESULT line equals the author's `author-r10/receipts/extract/extract-control.log` | `receipts/regrade-control.log`, `.rc`, `control-build.log` |
| Bind bounds | 188.8 ms × 2 = 377.6 ms, stated as 400 ms (rounded up to 50 ms, as 450 and 950 are). Burst saves: floor((630 − 100) / 188.8) + 2 = 4. The bench figure (245 ms, giving 490/500) is stated beside it, with the rule's choice. The measured 369.2 ms and 4 saves are within both. `selftest_bind.py:290-293` holds the targets to all three points | `bind_save.py:51-60`, `SPLIT_CONTROL_MEMORY.md:3541-3548` |
| ELF identity to `640699e6` | `git diff 640699e6 c0b625d1` touches 11 files. The only one under firmware, HDL, configs, the builder or third-party is `ctrl_loop.h`, a 2-line comment edit; comment-stripped it is identical (667 lines, sha256 prefix `13cad03c` both). No gitlink changed. `register_descriptions.json` feeds only the documentation generators. The author's `identity/product-identity.json` gives `f17d1a9d`, `0f1450ac` and `6e0a5412` at both heads | `receipts/ctrl_loop-comment-identity.txt` |
| Console coverage exclusion | The arc is infeasible: `lat` returns unless `c->len == 15`, and the name walk compares `at` ≤ 3 with it (`sw/firmware/ctrl/plat/ctrl_plat_console.c:178-185`) | Code read |
| Register reference, test-evidence, bare-metal, inventory gates | All exit 0. Register reference: `fresh (203 registers, 34 modules, 240 files)`. Bare-metal: 0 findings, 1981 files. The fingerprint is of comment-stripped sources (`scripts/gen_register_reference.py:361-378`) | `receipts/gate-*.log` |
| Commits | 19 of 19 one-line; `git diff --check 011aaa6f c0b625d1` clean | — |

## 3. Findings

### F1. MINOR. The egress grade's planted defects never test that an unheld record is graded, so an over-exclusion defect passes the gate vacuously

- **Lenses:** `Tests`.
- **Artifact:** `tb/verilator/ctrl_service_budget/egress_mii.py:412-422` (`mark_held`), `:544-558` (`plants`) and `:578-608` (`run_controls`). The only control that grades a hold, at `:601-603`, requires `wait_ps == 0`.
- **Evidence:** `scripts/probe_overexclusion.py` plants `mark_held` marking every record held. The result is `MISSED all-held`: every control still passes. On a synthetic two-frame unheld case, the grade then reports `wait_ps=0` and verdict PASS, where the shipping grade gives 288,507,500 ps (`receipts/probe-overexclusion.log`). The nine shipped plants test only one direction (`held-counted`).
  - The ruling requires a grader "with planted defects" for 2(b), and the row's value depends entirely on which records `mark_held` leaves to the ledger.
  - At this head the shipping grade is not over-excluding: 44 of 27,924 records are held, in the two cases README line 266 names. Nothing pins that count, though.
- **Impact:** a regression in `hold_windows` or `mark_held` that leaves every record (or every record after a hold) to the ledger would report a small row and pass, both in `--selftest` and on the packet.
- **Required outcome:** a control that holds `grade_case` on an unheld record to its hand-computed wait, with a plant that marks every record held caught by it.
- **Verification:** `egress_mii.py --selftest` shows the new plant `CAUGHT`, and `probe_overexclusion.py` reports `CAUGHT all-held`.

### F2. MINOR. Section 15 and the PR body report two measured figures that are not the qualifying link-rate census's

- **Lenses:** `Docs`.
- **Artifact:** `docs/design/SPLIT_CONTROL_MEMORY.md:3581-3582` ("observed maximum whole pass in that campaign is 143165 cycles, or 1.7895625 ms") and `:3594` ("61.80119 to 63.30645 ms"). Also the PR body's owner-bound table ("Longest whole pass | 143165 cycles, 1.7895625 ms") and the line after `kept_grade` ("61.80119 to 63.30645 ms").
- **Evidence:** the qualification that the head's model equals (the link-rate census, `published-qualification.json` `3075a3eb...`) records `worst_pass_cycles: 143181`. So do `census/qualify.log`, `derivation/census.log`, `extract/regrade-full.log` and my regrade. Its held-egress range is 61.80119 to **63.31139** ms (`receipts/regrade-r10-extract.log:178`, `backlog.owed_behind3.if0`). Neither 143165 nor 63.30645 appears in any published round-10 or round-11 receipt. Both apparently come from the instant-egress merge campaign, which the same section says changes 11 of 159 outcomes at 100 Mb/s.
- **Impact:** the authoritative design record and the PR state measurements of a superseded campaign as the installed row's. Both stay within their bounds (2 ms; ledger 63.51 ms), so no verdict changes, but a cold reader cannot reproduce either figure.
- **Required outcome:** state the link-rate census's figures (143181 cycles, 1.7897625 ms; 61.80119 to 63.31139 ms). Alternatively, name both campaigns, with the superseded one's figures bound to a published receipt.
- **Verification:** the figures in section 15 and the PR body equal `census/qualification.json` and the regrade log at the evidence commit.

### F3. MINOR. The service README names the superseded 147-case qualification as the installed row's and says its model is `arty_grade.py`'s

- **Lenses:** `Docs`.
- **Artifact:** `tb/verilator/ctrl_service_budget/README.md:229-231`.
- **Evidence:** at the head, `arty_grade.inspect()`'s model equals the 159-case qualification (`3075a3eb...`, in `author-r10/receipts/census-extract/`) and not `076e7cc7...`. The two differ in `load` (0.50140 against 0.50048), in `rec.adp`, `item.aecp` and `timers`, and in every row (`receipts/qualification-model-compare.txt`: `head==q147 False head==q159 True`). The lines predate the delta, but the delta's `563ee9105` raised the statements and made them false.
- **Impact:** the README's qualification citation, its hash and its "model is `arty_grade.py`'s" claim are wrong at the head. `receipt_regrade.py` compares an extract against its own copy, so no gate catches this.
- **Required outcome:** cite the 159-case qualification (an evidence-pinned link, its SHA256 and its 159 groups), and keep 147/`076e7cc7` only as history.
- **Verification:** the cited file's `model` equals `arty_grade.inspect()` at the head.

### F4. MINOR. FR_NFR 3.4.1 calls AECP's admission burst the structural maximum, with "each waits at most 391.5 us", which the census and the rings-at-capacity figure both exceed

- **Lenses:** `Conformance`, `Docs`.
- **Artifact:** `docs/reference/FR_NFR.md:511-512` (section 3.4.1). Also the PR body: "is the structural maximum FR_NFR 3.4.1 states".
- **Evidence:**
  - `structural()` (`egress_mii.py:489-529`) queues AECP's 16 × 1,514-byte records alone on an otherwise empty queue.
  - The census's own largest unheld wait is 426.47 us, a 550-byte AECP notice with 9 records queued, which is above that "at most 391.5 us".
  - The next sentence gives a 2.65 ms envelope for the 254 least records, above the row's 1 ms.
  - No public ruling names the AECP burst as the structural maximum. I searched #878, #1004, #1011, #1018 and #1020.
- **Impact:** the normative text reads as a structural bound that the measured row already exceeds, and it says nothing about whether the 2.65 ms envelope is reachable or who owns it. A reader cannot tell that the row is census-held rather than structurally bounded.
- **Required outcome:** say what the AECP figure bounds (one source's admission on an otherwise idle queue). State that the 100 Mb/s row is census-held under the ruling, with the structural envelope (254 records, 2.65 ms) outside it and named as open, or obtain a ruling that it is unreachable.
- **Verification:** the FR_NFR paragraph and the PR body no longer give a "maximum" below a measured wait, and the 2.65 ms envelope has a stated owner or disposition.

### F5. MINOR. The merged image's routing, timing and utilization have no published receipt

- **Lenses:** `RTL`, `Docs`.
- **Artifact:** the PR body, "Source and image": bitstream `82a226e3...`, routed checkpoint `6aec5a4a...`, "zero failing endpoints in all twelve reports", 33077 LUTs, +62 against round 7. Also the Definition of done: "Image routed and timing-qualified at every corner; post-route utilization compared" is ticked, and "+62-LUT routed delta accepted or explained by review" is not.
- **Evidence:** the merge changes a gateware input (the `gptp-processor` pin, so `gptp_ucode.hex`), so the image at the head is not round 7's. The evidence tree at `3e8f3014` (`author-r10`, `author-r11`, and the round-9/10 receipts commit `e62c5ed3`) holds no timing report, utilization report, checkpoint or bitstream hash for it. The only matches for `82a226e3`, `6aec5a4a` and `33077` are the PR-body copies and coincidental substrings. Round 7's routed evidence (`author-r7/receipts/timing-r7/`) is published, which was the precedent for R928-2-F2.
- **Impact:** the timing closure and LUT figures of the image that would merge rest on the PR body alone. The +62-LUT item the PR leaves to review cannot be judged from public bytes.
- **Required outcome:** publish, for the selected implementation of the merged image, the post-route timing summaries at every corner and the utilization report, bound by hash to the checkpoint and bitstream and to the firmware ELF `f17d1a9d`. Attribute the +62 LUTs, for example with a hierarchical utilization comparison against round 7 locating the delta in the gPTP processor's microcode ROM.
- **Verification:** a cold reader can open those receipts at an evidence commit, and their figures equal the PR body's.

### RESIDUE (wording only; exact fixes)

- **RS-4 (new; source-comment rule).** `tb/verilator/ctrl_service_budget/egress_mii.py:4-5` shows issue-comment IDs in a source docstring.
  - Fix: replace "PR #1020's 100 Mb/s ruling (comment 7216971645) makes" with "PR #1020's 100 Mb/s ruling makes".
  - Fix: replace "as a merge gate (comment 7216972073):" with "as a merge gate:".
  - No other new instance is in the lane's own delta: I grepped `aa53840d9..c0b625d1` for comment IDs, reviewer and author IDs, lane and bench labels, and round numbers.
- **RS-5 (new).** `tb/verilator/ctrl_service_budget/egress_fixed.py:11` gives the usage `python3 -I egress_fixed.py BUILD_DIR`. Under `-I` the script's directory is not on `sys.path`, so `import egress_mii` fails (`receipts/egress-fixed-isolated-usage.log`, `ModuleNotFoundError`). It runs and passes without `-I`.
  - Exact fix: "usage: python3 egress_fixed.py BUILD_DIR". SG-11 covers the code alternative.
- **RS-2 (retained, widened).** `author-r8/receipts/INDEX.md:5`, `author-r10/receipts/INDEX.md:5` and `author-r11/receipts/INDEX.md:5` all say "Prepared locally; nothing has been posted or pushed." So do the REVIEW-READY lines ("nothing pushed or posted") and HANDOFF line 4 of both packets. All of these packets are published. Fix: delete the sentence, or prefix it with "When written:".
- **RS-3 (retained, updated).** The PR body's "Reproduce and inspect" says "`receipts/census-extract/`" and pins no evidence commit.
  - Fix: link [`author-r10/receipts/census-extract/`](https://github.com/kebag-logic/milan-fpga/tree/3e8f3014f28d13bd008b06ec43f919d282d681ee/review-evidence/artysplit-r1/author-r10/receipts/census-extract) at evidence `3e8f3014`.
- **RS-1:** closed (§4).

### SUGGESTION

- **SG-8 (model fidelity).** The RTL merges the control lane in two places, each a round-robin packet arbiter: first with gPTP after the gasket, then with the data lane at the boundary (`hdl/milan/milan_datapath.sv:1684-1686`, `:9202-9214` and the gPTP merge note after `:9285`). `egress_queue.hpp` (`grant`) and `egress_mii.Queue.grant` model one alternation against SR and gPTP together. So a control frame can wait for one frame of each in the RTL but only one in the model.
  - The grade's whole-gPTP-burst term covers this for (b).
  - Say so in the header comment, or model the two merges.
- **SG-9.** Route the rings-at-capacity envelope (2.65 ms, above 1 ms) to a decision or an issue, since the author flags it as open. This goes with F4.
- **SG-10.** The phase sweep (`egress_mii.py:441-446`) replays phases 1 to 7 with phase 0's commit times and does not check ring room at those phases.
  - State that 2(a) holds at the testbench's phase 0, or check ring occupancy at each commit in each phased replay.
- **SG-11.** Insert `HERE` into `sys.path` before `import egress_mii` in `egress_fixed.py`, as `packet_rows` does, so the repository's `-I` convention works. Consider adding it to the author's standing gate list.
- **SG-12 (outside the delta).** `tb/verilator/ctrl_service_budget/README.md:246`, "Numbered text parts stay below 190 KB", describes full packets. The compact extract's parts are up to 14,000,000 bytes. Say which applies.
- **Retained optional items:**
  - R927-3 SG-3, partly adopted: inventory-hash-mismatch and dropped-read-label plants are still absent from `census_extract --selftest`.
  - SG-5 and SG-6, outside the delta.
  - SG-7: a republication note beside the round-8 extract.
  - R927-2 SG-1, SG-2, SG-4, SG-5 and SG-7.

## 4. Prior findings of my own rounds at this head

| Finding | Status | Cause-level evidence |
|---|---|---|
| R927-3 F2 MINOR (`Tests`, `Docs`): the "generated outputs unchanged" receipt is empty | **CLOSED** | `author-r10/receipts/builder/builder-split.log` records the command, four heads and IDENTICAL for 4adfa9dc→011aaa6f and aa53840d9→fb4b456a4, both placements, exit 0. `builder-split.json` gives every output's SHA256 per head. The merge's one difference (`gptp_ucode.hex`) is stated as informative. This matches my R927-3 `builder-split-identity.txt` |
| R927-3 RS-1 (FILES.json coverage wording; qualification not inventory-checked) | **CLOSED** | `census_extract.py:11-15`, README lines 238-241 and the inventory check at `census_extract.py:199-204` |
| R927-3 SG-1 (part-limit disagreement) | **Adopted** | `census_extract.py:45-46` (`READ_LIMIT = PART_LIMIT + 1`), `:132`; self-test checks 1-3 |
| R927-3 SG-2 (an overlong line loops) | **Adopted** | `census_extract.py:73-77` refuses; self-test checks 4-6 |
| R927-3 SG-4 (qualification bound to the inventory) | **Adopted** | `census_extract.py:199-204` |
| R927-3 SG-3 | Partly adopted; remainder retained optional | See SUGGESTION |
| R927-4 RS-3; R927-3 RS-2 | Retained as residue | See RESIDUE |
| R927-3 SG-5, SG-6; R927-4 SG-7 | Retained optional | No delta touches them |

**The external reviewer's prior findings.** I read these after my own pass, verdict and ledger were written. The external reviewer decides whether their findings close; this table states whether each one's verification is met at this head.

| Finding | Status at `c0b625d1` | Cause-level evidence |
|---|---|---|
| R928-3-F1 MAJOR (published extract bytes) | Closed in R928-4; **remains closed** for the round-10 extract | My regrade of the published `author-r10` extract reproduces 159 of 159 and the cross-case step, and the control is refused (§2) |
| R928-3-F2 MINOR (inclusive part-size boundary) | **Verification met at its cause** | One contract across all readers. The writer gives at most `PART_LIMIT` (`census_extract.py:45,72-77`). The extractor's own regrade uses `READ_LIMIT = PART_LIMIT + 1` (`:46,132`). The CLI uses `part_limit + 1` (`receipt_regrade.py:192`), and so does `egress_mii.packet_rows` (`:640`). The README (lines 238-241) and the docstring (lines 11-15) say so. `census_extract --selftest` round-trips an exact-limit part and an exact-limit first part before another, and refuses at a limit of the part's size (checks 1-3, scaled to a 64-byte limit). I did not rerun the external grade-level exact-limit probe |
| R928-3-F3 MINOR (an overlong line prevents progress) | **Verification met at its cause** | `census_extract.py:73-77` raises when no newline ends within a part. Self-test checks 4-6 cover overlong-first, overlong-after-a-part and no-newline, each refused after at most one emitted part |
| R928-3-RS1 (round-7 INDEX wording) | Retained (residue) | `author-r7/receipts/INDEX.md:128-129` is unchanged at `3e8f3014` |
| R927-2-F2 (qualification pointer), closed by both reviewers at `011aaa6f` | **Regressed: reopened as F3** | Its closure read "its model equals current `arty_grade.py`". The delta's raised statements (`563ee9105`) make that false. The README lines are unchanged (now 229-231) |
| R928-2-F2 (routed comparison), closed at the round-7 image | Closed for round 7; **the merged image's equivalent is F5** | Round 7's reports are published. The merged image's are not |

## 5. Lens results at this head

```text
[R927] MINOR Tests — tb/verilator/ctrl_service_budget/egress_mii.py:412-422,544-608; receipts/probe-overexclusion.log — F1: an all-held plant is MISSED and the gate passes with wait 0. Applied otherwise clean: egress self-test 17/17, census_extract self-test 6/6, regrade 159/159 and control refusal equal the author's, fixed path 312.5 ns, bind self-test targets selftest_bind.py:290-293
[R927] MINOR Docs — docs/design/SPLIT_CONTROL_MEMORY.md:3581-3582,3594; tb/verilator/ctrl_service_budget/README.md:229-231; docs/reference/FR_NFR.md:511-512; PR body "Source and image" — F2, F3, F4, F5; RS-2 to RS-5 are residue only
[R927] MINOR Conformance — docs/reference/FR_NFR.md:511-512 against rulings 7216971645/7216972073 — F4. Otherwise: 2(a) by item 3 (sim_main.cpp:150,170,259, link-rate census at 7bc47c0e, the 11/159 replay), 2(b) at 505.738 us (receipts/egress-packet.log), 254 records, bind bounds 400 ms / 4 by 7221391389, held-egress ledger for this point unchanged by 7234489667
[R927] MINOR RTL — PR body bitstream 82a226e3 / checkpoint 6aec5a4a against evidence tree 3e8f3014 — F5: the merged image's routed evidence is unpublished. Applied otherwise clean: no lane HDL change; merge gateware delta = gptp-processor pin (3ce71b76) only; queue constants match tx_ifg_gasket.sv:36-51 and milan_soc.py:1483-1499; fixed path measured on mac_tx_chain_mii.v
[R927] PASS Robustness — census_extract.py:70-80,132,199-204 (overlong-line refusal, inclusive limit, inventory-bound qualification; self-test 6/6); egress_mii.py:316-338,429-434,646 (commit/departure mismatch raises, missing EGRESS refuses, queue-line mismatch refuses, manifest hash checked); sim_main.cpp:150,170,259,812 (gigabit points unchanged: egress_link false, EgressQueue prints nothing at octet_ps 0)
```

## 6. Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F4) | Rulings 7216971645, 7216972073, 7221391389, 7234489667; FR_NFR 3.4.1 at `:499-513`; section 15 at `:3496-3560`; `egress_mii.py`, `egress_queue.hpp`, `sim_main.cpp`, `bind_save.py:51-60`; my regrade, egress grade and control | R927-5 (not covering) | c0b625d1792e61b8e99944daea65b842e6b9dcde |
| RTL | UNCLEAN (F5) | Merge gateware delta; `tx_ifg_gasket.sv`; the `milan_datapath.sv` TX merges; `milan_soc.py` queue constants; the fixed-path run; PR-body image claims against the evidence tree | R927-5 (not covering) | c0b625d1792e61b8e99944daea65b842e6b9dcde |
| Robustness | CLEAN | `census_extract.py` refusals and limits; the `egress_mii.py` parse, refusal and hash paths; the testbench's gigabit path; merge resolution (`ctrl_mutants.py`, `ctrl_mutant_fixtures.py`) | R927-5 | c0b625d1792e61b8e99944daea65b842e6b9dcde |
| Tests | UNCLEAN (F1) | Egress self-test plus the over-exclusion probe; census_extract self-test; regrade and control; fixed path; bind self-test targets; coverage exclusion (`ctrl_plat_console.c:178-185`); test-evidence disposition | R927-5 (not covering) | c0b625d1792e61b8e99944daea65b842e6b9dcde |
| Docs | UNCLEAN (F2, F3, F4, F5) | FR_NFR 3.4.1; section 15; service README lines 228-268; gtest README and ratchet; register reference (gate fresh); the live PR body; the r10/r11 INDEX, REVIEW-READY and HANDOFF files | R927-5 (not covering) | c0b625d1792e61b8e99944daea65b842e6b9dcde |

## 7. Real limits

- **No ELF rebuilt by me.** The ELF identity rests on the source argument in §2 (only a comment changed, identical once stripped, no gitlink moved) and on the author's `identity/product-identity.json`. I did not build the three products.
- **No image built or routed.** F5 is about publication; I do not dispute the timing figures themselves.
- **The queue model is checked against its sources' constants and the fixed path, not cycle-for-cycle against the RTL.** The testbench and the grade run the same model, by design. SG-8 is the one structural difference I found.
- **No manager source bank** ran at this head, and none is claimed. Source execution evidence is the author's gate receipts plus my runs listed here.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Hosted state at query time (2026-11-28T11:42Z):**
  - 15 check runs completed with success: docs, elaborate, lint, `full-ci-gate` and others.
  - 1 skipped (`Physical gPTP (nightly and manual)`).
  - 51 queued or in progress; combined status `pending` (`receipts/hosted-checks-at-query.tsv`).
  - None is accepted here. The manager owns hosted and local-replica acceptance.

## 8. Pending manager duties

- A follow-up round must close F1 to F5, re-cover `Conformance`, `RTL`, `Tests` and `Docs` at its head, and carry RS-2 to RS-5 to the residue checklist.
- The current-dev merge-candidate validation (builder and native banks; source base `854bd723`, live dev `e275d795`), with receipts on the PR.
- Hosted and local-replica acceptance at the final head.
- The open #977 integration the PR names, maintainer merge authorization, and post-merge containment.

## 9. Reproduction (this packet)

- **Evidence:** fetched read-only (blobless, `--depth=2`) into a scratch bare repository. `git archive 3e8f3014` of `author-r10` and `author-r11` was extracted under `scratch/`.
- **Commands, from the clone at the head (bytecode off):**
  - `python3 -B -E -s tb/verilator/ctrl_service_budget/receipt_regrade.py <census-extract>` writes `receipts/regrade-r10-extract.log`.
  - `python3 -I scripts/make_control.py <census-extract> <copy>`, then the same regrader on the copy, write `receipts/control-build.log` and `regrade-control.log`.
  - `python3 -I -B tb/verilator/ctrl_service_budget/egress_mii.py --packet <census-extract> | --selftest | --structural` writes `receipts/egress-packet.log`, `egress-selftest.log` and `egress-structural.log`.
  - `python3 -I -B tb/verilator/ctrl_service_budget/census_extract.py --selftest` writes `receipts/census-extract-selftest.log`.
  - `PATH=<pinned Verilator 5.050>:$PATH python3 -B -E -s tb/verilator/ctrl_service_budget/egress_fixed.py <build>` writes `receipts/egress-fixed.log`.
  - `python3 -I -B scripts/probe_overexclusion.py <clone>` writes `receipts/probe-overexclusion.log`. It monkeypatches in process; no file changes.
  - The documentation gates write `receipts/gate-*.log`. The register reference ran with an existing documentation virtual environment that provides `wavedrom`.
- **Clone after the runs (`receipts/clone-restore.txt`):**
  - HEAD is `c0b625d1`, and the index tree equals the HEAD tree `1f528462` (2014 entries).
  - `diff-index` and `diff-files` are clean, and status including ignored files is empty.
  - The six gitlinks equal HEAD, and no `__pycache__` was written.

R927-5 FINISHED
