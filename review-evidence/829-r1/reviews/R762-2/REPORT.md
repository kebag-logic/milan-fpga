[R762] NEGATIVE - exact head 2d534bec9348557a9407d3024c0b199c0ebc8bce

# R762-2: external review of issue #829 / PR #831, round 2

Tree `8ed7e82fcd001d9965a3e6bd9f33b741dae4dbf0`. Delta judged: `4cda0aa0..2d534bec`, 10 commits, against source base `1f29f189279f9fc0132f4918e47342b87d22f33a`.

**Every round-1 finding and residue item is closed, and the RTL change really is comment-only. One new MINOR keeps this NEGATIVE:** gate 1h, added to close my F4, reads comments. So a commented-out binding, which is the same defect as a deleted one, passes it. The fix is one line, and I tried it on a disposable copy. `Conformance`, `RTL`, `Robustness` and `Docs` are clean; `Tests` is unclean on that finding alone.

## Findings

### R762-F9: MINOR: gate 1h accepts a binding cut that is spelled as a comment

- **Lenses:** Tests
- **Path:** `sw/builder/test_builder.py:18311-18325` (`_datapath_shape_findings`), over `hdl/milan/milan_datapath.sv:92-93,8885-8886`
- **Authority and evidence:** AGENTS section 6, `Tests`: each new test can fail for the defect it claims to detect. The gate's own comment names that defect: cut a binding and the plane keeps GMII's default. Its regexes run on the raw text, comments included. I planted 14 cuts on a disposable copy and ran the committed gate by name each time (`receipts/gate_1h_cuts.log`):

| Planted in `milan_datapath.sv` | Gate 1h |
|---|---|
| Shipped text, no cut | accepts, rc 0 |
| Either binding deleted; either tied to its default; the two swapped; either default moved; the instance renamed; a no-op `+ 0` in the binding | refuses, rc 1, each by name |
| Tick binding in a block comment | refuses, but only because the gate's own control reports it "planted nothing", not by naming the cut |
| `// .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),` | **accepts, rc 0** |
| `// .ETH_CYC_PER_OCTET_P(GPTP_ETH_CYC_PER_OCTET_P),` | **accepts, rc 0** |
| `.ETH_TICK_NS_P (8), // .ETH_TICK_NS_P (GPTP_ETH_TICK_NS_P),` | **accepts, rc 0** |
| Default in a comment, with `= 40` on the next line | **accepts, rc 0** |

  `lint_rtl.py --check` also stays at PASS, 89 at ratchet 89, with the tick binding commented out: `receipts/lint_commented_binding.log`. The gates that my round-1 F4 ran against a deleted binding could not see this cut either. So gate 1h is the only holder, and it has this gap.
- **Why this is not RESIDUE or a SUGGESTION:** it changes test code and a gate's verdict. It is also the same class as my round-1 F3 and F8, where a later cut stays green. The shipped wiring is correct, so nothing is wrong on either board today.
- **Impact:** with the binding commented out, the Arty plane expects 45 cycles, the observer measures 90, and every frame is lost unmeasured. That is this issue's visible failure, behind a green gate.
- **Required outcome:** the gate judges the RTL with comments removed, and its planted list includes a commented cut so that the property holds. One way, in the reader: `rtl = re.sub(r"/\*.*?\*/|//[^\n]*", "", rtl, flags=re.DOTALL)`.
- **Verification:** those four cuts give rc 1, by name, and the shipped text gives rc 0. With that one line in a disposable copy, all 14 cuts are refused and the shipped text is accepted: `receipts/gate_1h_cuts_with_comment_strip.log`. A reviewer re-runs `scripts/gate_1h_cuts.py` on the new head.

## Residue, wording only

| ID | Path | Exact fix |
|---|---|---|
| R762-2-R1 | `sw/litex/milan_soc.py:2092-2096` | "That is what makes ... a fact of the wiring" now follows the sentence saying `eth_rst` does not reach the PHY stage on MII, so "That" reads as the wrong sentence. Move the `eth_rst` sentence after it |
| R762-2-R2 | `review-evidence/829-r1/author-r2/HANDOFF.md`, R761 S3 row | It cites `KL_gptp_gmii_launch.sv:100`. The citation is at `:101` at this head. The clause and the file are right. Correct it if the packet is regenerated |

## Suggestions

- **R762-2-S1, Tests:** gate 1g (`_launch_shape_findings`) uses `old not in soc`, so by reading it has the same comment gap. I did not plant this one. It predates this round, and it is worth fixing alongside F9.
- **R762-2-S2, Tests:** no text gate can see every cut; for example, `defparam` or a dead generate branch would pass. An elaboration that reads the plane's effective parameters on the Arty shape would close the class. It is not required here.
- **Retained, for their own Issues:** R761 S4 (the command table's pins, and this round edits `mutants.py` again), R761 S5 (the fragment arm's bubble), R762-S1 (receive range is a sample) and R762-S3 (no runtime refusal at 10 Mb/s).

## The eight requested checks

| # | Check | Result | Receipt |
|---|---|---|---|
| 1 | Round-1 findings and residue | All closed; see "Prior public findings" | below |
| 2 | Style and idiom gates | Local: `documentation style: OK (23 current documents)`, selftest OK, `build without warnings: 0 <= 0`, each rc 0. Hosted `docs-gates-0`, job 124961954901, on this exact head: **success**, including step 15 "Concise audience documentation gate" and step 44 "C and C++ idiom gate". `docs-gates-1` and `-2` also succeeded | `receipts/check_doc_style.log`, `check_cpp_idiom.log`, `hosted_docs_gates_0.txt`, `hosted_gate_1h.txt` |
| 3 | GMII `ready` | **Stated as a flop everywhere and correct.** Found in `milan_soc.py:2085-2087`, `GPTP_PLANE.md:286-290`, `CHANGELOG.md`, `KL_gptp_gmii_launch.sv:35-36,364-366` and the PR table. My AX7101 export has the flop set to 1 and cleared by `eth_tx_rst`. The observer's `maceth_tx_rst` synchronises `eth_tx_rst \| eth_rst` through two stages, so it releases after `ready` is 1. "Cannot move" and "folds away" are gone from `test_builder.py`, the plane text and the PR body | `receipts/ax_export_ready_lines.txt` |
| 4 | Three weak checks | **All bite.** Fragment: forced distance on MII stays green at 95 of 95 under the old check, and fails `fragment: the observer refused it, by measurement` under the new one. PHC: I confirm the load lands at the window's early end, because guard 188 fails the frame's own result and 189 passes it. 3770 / 20 is 188.5, so that is the exact boundary. 189 and the controls at 170 and 202 fail or are caught as stated, and a planted GMII floor of 63 fails too. Bias: the two names and limits are 1.754 ns and one nanosecond | `receipts/spot_mutants.txt`, `spot/`, `gptp_txts-all.log` |
| 5 | Gate 1h | **Not fully.** It refuses every cut in live code, and the planted comment cuts escape (F9). It is registered and runs in one builder leg per the author's log; hosted legs succeeded, and I did not read their logs | `receipts/gate_1h_cuts.log` |
| 6 | Comment-only RTL | **True.** Only `KL_gptp_gmii_launch.sv`, `KL_gptp_shadow.sv` and `milan_soc.py` among build inputs differ. Preprocessed text is identical for both, 302 and 668 lines. `milan_soc.py`'s parsed program is identical. The exported AX7101 top is identical at 29720 lines with comments, blanks and each tree's root removed; `xdc`, memory init, ROM init and `csr.csv` match; `tcl` differs only by my output path. **One precision:** converting the raw sources differs in 7 lines, all elaboration-refusal texts that name a source line, because the comments moved those lines. Normalising `line:col` makes the output identical, and none of those branches elaborates | `receipts/comment_only.log`, `ax_export_compare.txt` |
| 7 | Citation | **Correct,** read in a local copy of the standard. 11.3.9 is "Event message timestamp point": "the beginning of the first symbol following the start of frame delimiter". 8.4.3 is timestamp generation and the correction to that point. 11.3.2 is "Message types contained in each message class", so it was the wrong citation. The oracle's `pad_at_first_symbol` lands on exactly that symbol on both shapes (read at `sim_main.cpp:495-556`, and bounded by the 188/189 result) | standard, not published |
| 8 | Figures | **13 controls reproduced,** `controls: 13 failures: 0`. 95 of 95 in all three runs; 89 + 6 = 95, and 18 more checks over three runs matches the sweep's delta. The 126 receipt has 126 equal rows, and it says itself that it compares `4cda0aa0` with the bench branch and not with `dev` | `receipts/gptp_txts-all.log`; public `author-r2/receipts/ax7101/checksum-comparison.txt` |

**Check 8, judged: the record comparison is enough for what this PR claims, and it would not be enough to claim "unchanged".**

- **The premise needs correcting.** The elaborated AX7101 default is not unchanged. Its top gains one line, `.gmii_tready_i (milansoc_milanmac_phy_sink_ready)`, and the observer gates on that flop. The published synthesis stats for the observer show about 2 more LUTs and 3 more muxes. The 1 extra flop there appears to be that test wrapper's own `ready` register, which already exists in the real chain.
- **What rests on what.** "GMII behaviour unchanged", the acceptance wording, rests on the equivalence proofs with `ready` high, the census of no held octet over more than 100,000 valid clocks, and the reset order in check 3. None of those depends on a route, and this round's comment-only result leaves them all in force. So a route of `dev` adds nothing to that claim.
- **What the route shows.** It shows this logic closes and fits within the gate's tolerances on one placement. It cannot attribute anything to this PR, because the record's baseline is an older `dev`: FF +394, slice +61 and WNS -0.204 ns are mostly not this PR's. The PR body says exactly that, so nothing is overclaimed.
- **The remaining risk is margin.** Slices are 15841 of 15850, and `AREA_BUDGET.md:143` calls that row the binding limit. The candidate route at the merge turn should settle it. A separate `dev` route is not needed.
- **One thing for the manager to see.** The owner's 2026-11-01 14:10 comment says the AX7101's "shipping image must not change". Its subject is the bench's writable-correction key, which is not in this PR, so I read no conflict with the acceptance wording. But this PR does change that image by one net, and the PR body says so. If the owner meant the sentence more widely, that is the owner's call.

## Clean lenses

```text
[R762] PASS Conformance — tb/verilator/gptp_txts/sim_main.cpp:495-556 and receipts/spot_mutants.txt, against IEEE 802.1AS-2020 11.3.9 and 8.4.3 and #829's acceptance — the oracle grades the clause's first symbol, the corrected citation matches the clause, and the logic behind the acceptance is unchanged by check 6, so round 1's reproduction stands
[R762] PASS RTL — receipts/comment_only.log, receipts/ax_export_compare.txt, and the export's ready flop and reset chain — no behaviour moves in the delta, and the corrected statements about GMII ready and eth_rst match the generated chain and the AX7101 export
[R762] PASS Robustness — receipts/spot_mutants.txt and sim_main.cpp:965-1020 — no RTL changes; the PHC load now reaches the window's early end with the exact boundary shown, the fragment refusal is real on MII, and the GMII guard floor is held
[R762] PASS Docs — CHANGELOG.md, docs/design/GPTP_PLANE.md:276-375, tb/verilator/gptp_txts/README.md, PR #831 body, #829 REVIEW READY — figures and clause trace, gates pass locally and hosted, facts in the reworded text match the prior text, and the correction of 14 and 126 is public; two residue items only
```

Comment rule: the delta's added lines carry no new lane label, review round, reviewer ID or comment ID. Commits: 10, each one line with no trailer.

## Ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | IEEE 802.1AS-2020 11.3.9, 11.3.2, 8.4.3; `sim_main.cpp:495-556`; #829 acceptance and comments; `receipts/spot_mutants.txt`, `comment_only.log` | R762-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| RTL | CLEAN | `KL_gptp_gmii_launch.sv`, `KL_gptp_shadow.sv`, `milan_soc.py`, AX7101 export, `generated/mac_tx_chain.v`; `receipts/comment_only.log`, `ax_export_compare.txt` | R762-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| Robustness | CLEAN | Fragment and PHC arms, GMII and MII; `receipts/spot_mutants.txt`, `spot/`, `gptp_txts-all.log` | R762-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| Tests | **UNCLEAN**: F9 | `test_builder.py` gate 1h, `sim_main.cpp`, `mutants.py`, suite `Makefile`; `receipts/gate_1h_cuts.log`, `gate_1h_cuts_with_comment_strip.log`, `lint_commented_binding.log`, `gptp_txts-all.log` | R762-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |
| Docs | CLEAN | `CHANGELOG.md`, `GPTP_PLANE.md`, suite `README.md`, PR #831 body, #829 comments, public `author-r2` packet; `receipts/check_doc_style.log`, `gen_toc.log`, `docs_check.log`, `check_gptp_docs.log`, `hosted_docs_gates_0.txt` | R762-2 | `2d534bec9348557a9407d3024c0b199c0ebc8bce` |

## Prior public findings

I read R761-1 and my own R762-1 after my pass over the diff and after the gate cuts had run. No R761-2 report was read.

| Item | State at this head | Basis |
|---|---|---|
| R762-F1, R761-F1: style gate | **Closed** | Check 2 |
| R762-F2, R761-F2: idiom ratchet | **Closed** | Check 2; `scripts/` is unchanged, ratchet 0 |
| R762-F3, R761-F5: PHC arm | **Closed** | Check 4 |
| R762-F4: datapath wiring | **Closed as written:** a cut binding now fails a named check. Its remaining gap is new, F9 | Check 5 |
| R762-F5, R761-F7: bias name | **Closed** | Check 4; `sim_main.cpp:92-97` |
| R762-F6, R761-F6: figures | **Closed** | Check 8; #829 comment 6563126522 corrects both |
| R762-F7, R761-F3: GMII `ready` | **Closed** | Check 3; export lines 21667-21669, 21596, 32558, 32681 |
| R762-F8, R761-F4: fragment on MII | **Closed** | Check 4 |
| R762-R1, `eth_rst` reach | **Closed**, with R762-2-R1 on the sentence order | `KL_gptp_gmii_launch.sv:150-153`; export lines 16170, 32555 |
| R762-R2, digital bound | **Closed** | `GPTP_PLANE.md`, `KL_gptp_shadow.sv:91-93` |
| R762-R3, bench range | **Closed** | PR bench table; the bench was not re-run |
| R762-R4, R761 RES1 | **Closed** | `sim_main.cpp:14-15` |
| R762-S2, R761 S1 | Tracked by #832, not a finding here | Issue is open |
| R762-S4, R761 S2 | Tracked by #833, not a finding here | Issue is open |
| R761 S3, citation | **Closed** | Check 7 |
| R761 S6, stale binaries | **Closed** | Neither binary exists after my full run |
| R761 S4, S5; R762-S1, S3 | Retained as suggestions | Not assigned; none changes this verdict |

## Real limits

- **No route or synthesis here.** Comment-only is shown up to the exported top and the sources Vivado reads. I did not run Vivado, so the claim that `4cda0aa0`'s route still describes this head rests on that text identity.
- **Evidence.** All 959 entries of the public `829-r1/MANIFEST.json` match their published hashes, and it lists every file in the tree. The evidence commits show no signature, so this checks integrity against the manifest, not authorship. Of the author's 64 `docs.yml` steps, I re-ran the style, idiom, TOC, docs and gPTP-doc gates, and read the hosted jobs.
- **Not re-run:** round 1's equivalence proofs, the receive distances, the full sweep, behave, builder legs, and all bench figures. The check 6 identity is why the first two still hold. The rest are the author's receipts.
- **Hosted state when read:** `docs-gates-0`, `-1`, `-2` succeeded on this head. The `docs` run as a whole, `rtl-full`, `elaborate` and `rtl-fast` had not finished, so I claim nothing from them.
- **The gate cuts are a sample.** F9 names the comment class I found. It does not prove no other spelling escapes.
- **Two of my own first receipts were wrong, and I corrected them.** My first `sv2v` list failed on both sides with equal hashes, and my first export compare read DIFFERENT because of my tree paths. Both were fixed before anything was concluded, and the published scripts are the corrected ones.
- **Job limit.** The suite's Verilator flags use `-j 0`, so my six concurrent spot builds could briefly exceed 16 compile jobs. The results don't depend on load; the lifecycle test was not run.
- **Clone state:** head and tree exact, `git status` clean, 1461 blobs and modes re-hashed with 0 mismatches. The five initialised gitlinks match, and `external` is uninitialised, as it was at the start: `receipts/final_clone_integrity.txt`.

## Pending manager duties

- Carry F9 and the two residue items to the author, then re-review `Tests` on the new head. A change confined to `test_builder.py` does not touch the scope of the other four lenses.
- Hosted and act acceptance at the final head. Candidate merge validation against current `dev`, including the candidate route's slice row.
- The tap-out check and physical calibration stay owed through #583. Nothing here is hardware proof.
- The AX7101 image note under check 8, if the owner's wording needs confirming.

R762-2 FINISHED
