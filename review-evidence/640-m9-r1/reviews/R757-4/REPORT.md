[R757] NEGATIVE - exact head 22f3cedb420992b7b776c5a842b0b210ac4191d3

# R757-4: internal cleared-context review of PR #828 (issue #640), round 4

- Head `22f3cedb420992b7b776c5a842b0b210ac4191d3`, tree `aa3a82eae97231e462c5482c3d1f00a50b183004`.
- Round-4 delta: `69fd18f1..2322c6d7`. Six commits on three Markdown pages, 152 lines added and 32 removed. Then the merge of dev `1f29f189`, whose only effect on this PR's pages is one added line each in REQUIREMENTS.md and docs/README.md.
- The delta has no code, generator, gate, configuration or gitlink, and no mode change. This is a documentation-only round.
- **Reconstructed from:** AGENTS.md and CONTRIBUTING.md, docs/README.md; the #640 body and the 2026-10-31 owner decisions; my R757-3 report, read first; the delta and its commits; the author's round-4 packet `review-evidence/640-m9-r1/author-r4` at `993a5bb5` (HANDOFF.md, PR-BODY.md, models, gate receipts); the A720d REVIEW READY comment on #640.
- **Taken as given:** the owner decisions of 2026-10-31 are final and are not reviewed. The manager's convergence rule is applied: an item left open with a requirement and a verification row is not a defect, and a wrong statement of fact still is.
- **Order of reading:** I read R758-3 only after recording my findings and lens results. The section "Prior external findings" is that later pass.

## Verdict

NEGATIVE. Three MINOR findings are open, and round 4 introduced or restated all three. No BLOCKER or MAJOR is open.

- **Closed:** both R757-3 findings (N4, N5), both residue items (RR3, RR4), and the suggestions, each taken or declined with a reason. All three R758-3 findings and its residue are closed for what they named.
- **Models:** the flash, merge and conversion models reproduce their published output byte for byte, and every stated mutant fails. Three probes of my own drive those models.
- **Figures:** 365.10 ms, 2.917 ms, 2.744 µs and the 62.5 µs window are all right.
- **Gates:** 23 docs-gate commands re-run at this head all exit 0. The author's full docs-workflow receipts at this head all record rc 0, and their digests verify.

The open findings:

- **N6:** rule 1 reads a tu copy's own time, so "tu on both loses no sample" is false once that time runs about 0.75 ms or more ahead on a fast network at the 2 ms offset. From about 0.85 ms, audio is lost for the whole tu period with both networks delivering every packet.
- **N7:** "A tu copy with no valid reference cannot make one" contradicts the model. Built as written, a stream that starts with tu loses 22,452 of 24,000 samples.
- **N8:** the PR body says removing rule 4 fails 5 cases. The published model output says 7.

## Findings

### N6 MINOR - Conformance, RTL, Robustness, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:647, :616, :695, :711-712, :1219; PR body, Round 4 row "R758-3-F1" - rule 1 checks a tu copy's own time, so the no-loss claim for tu on both, and the stated loss-plus-tu gap, fail for a skewed time

- **Authority and evidence:**
  - **The claims:**
    - SE:711 "With both networks delivering, tu on both loses no sample."
    - The PR body: "so tu on both loses no sample while both deliver".
    - SE:695: loss plus tu "gaps for up to one presentation offset".
    - SE:1219, bench: "tu set on both networks by one talker, both up, no lost samples".
  - **The page's own reasoning:** SE:614-616 says a listener may stop trusting a tu copy's time, so "a tu copy's time names no packet" (IEEE 1722-2016 4.4.4.7).
  - **The rule:** rule 1 (SE:647) still applies the late and early check to that own time, before rule 4 ever reads the counted time. The model does the same (`merge_model.py:106`).
  - **Why a large skew is reachable:** a tu period exists because the time is uncertain. `docs/design/GM_LOSS_RECOVERY.md:190` has tu rise on a time step and hold for at least 0.25 s. At the 2 ms default offset, a copy arriving 60 to 180 µs after transmission has only about 0.73 to 0.85 ms of early margin.
  - **Probe** (`scripts/probe_merge_r4.py`, `receipts/probe_merge_r4.txt`, the author's model unchanged, every copy delivered, tu from packet 100):

    | Case | Samples missing | Copies failing rule 1 |
    |---|---|---:|
    | Both networks at 60 to 180 µs, skew up to +700 µs on both | 0 | 0 |
    | Same, skew +800 µs | 8,598 | 4,748 |
    | Same, skew +850 µs or more | 23,400, every tu sample | 7,800, every tu copy |
    | Same, skew -2,000 µs | 23,400 | 7,800 |
    | Same, tu 100 to 600, skew +1,000 µs | 3,000, the whole period | 1,000 |
    | Fast primary skew +1,000 µs, slow secondary 0 | 30 | 3,900 |
    | Primary cut, secondary tu for 250 ms, skew +2,500 µs | 12,000, that is 250 ms against the stated 2 ms | 2,000 |

  - **The fast-primary line's cause:** the primary's tu copies fail rule 1, so they never set `LAST_TU` (SE:886). The secondary's tu copies are then discarded by rule 2 until the primary's last clean time passes. That is the same 5-packet loss the rule was changed to remove, reached by another path.
  - **Other cases:** at skew -1,900 µs, 8,551 samples also land at wrong positions, because a lapsed head re-anchors on a skewed own time.
  - **Coverage:** the model and SE:1219 run tu on both only at skews of ±5 and ±200 µs. The time step is applied only as tu clears. The page's list of gaps (SE:723-738) does not mention this one.
- **Impact:**
  - A bench test written to SE:1219 can fail on a compliant talker, depending on the size of the step.
  - The reader of SE:711 and the owner reading the PR body get a stronger guarantee than the rules give.
  - A lane building the rules as written mutes a pair for the whole tu period, while both networks deliver every packet, on a time step of about a millisecond or more.
- **Required outcome**, either of these:
  - Rule 1's time check no longer reads the time of a tu copy with a valid reference, and rule 4 judges it by count. The control arm in the probe shows this loses nothing at +1,000, +2,000 and +5,000 µs, and in the fast-primary and cut cases. It passes 32 of the 33 model cases; the unpaired +40 jump changes and would need its own handling, so the probe is a control and not a prescribed design.
  - Or the rule stays, and the claims are bounded. SE:711, SE:695, SE:1219 and the PR body say the no-loss and one-offset statements hold only while a tu copy's own time passes the late and early check. The gap and its size go beside SE:723-738. Under the convergence rule this may be a new open design item with a requirement and a verification row.
  - In both cases, the verification row and the model add tu on both, and loss plus tu, at a skew beyond the check, with the stated result.
- **Verification:** re-run `scripts/probe_merge_r4.py` Arm A against the changed model, and read SE:711, :695 and :1219. Missing samples must be 0, or equal the stated gap.

### N7 MINOR - RTL, Robustness, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:678, :649, :675, :902 - "A tu copy with no valid reference cannot make one" contradicts rule 3's anchor and the model

- **Authority and evidence:**
  - Round 4 added SE:678 (`0f6ab84b`) as an unconditional rule.
  - SE:649 lets a tu copy with no reference anchor the head. SE:670 says a tu copy may anchor before any clean copy arrives.
  - The model, however, makes a reference at that anchor: `merge_model.py:170`, `self._seen(c, t, tu, seq, t)`. Without it, the next tu copy has no valid reference and rule 4 discards it.
  - **Probe** (Arm B, `receipts/probe_merge_r4.txt`), the model against the sentence as written, every copy delivered:

    | Case | Samples missing, model | Samples missing, as written |
    |---|---:|---:|
    | Unpaired, tu from packet 0 | 0 | 22,452 of 24,000 |
    | tu on both from packet 0 | 0 | 21,870 of 24,000 |
    | tu on both from packet 0, secondary faster | 0 | 21,864 of 24,000 |

  - The sentence changes behaviour, not just its description. The merge row (SE:1219) and the 33 cases have no case with tu from the first packet on an unpaired stream or on both networks. The only startup case has a clean partner, where the difference does not show. So the row cannot catch a lane that follows SE:678.
- **Impact:** a lane building SE:678 literally renders about one packet per head lapse on any stream that starts with tu set. A talker starting before its gPTP settles does that. The result is near silence, with the model and the verification row still green.
- **Required outcome:**
  - The page states that the anchoring tu copy makes the context's reference, as the model does. For example, at SE:678: "Only rule 3's anchor makes a reference from a tu copy." SE:902's "counted for a copy with tu set" gains the same exception.
  - The verification row and the model add tu from the first packet, on an unpaired stream and on both networks.
- **Verification:** those cases pass with 0 missing samples, and a mutation that withholds the anchor's reference fails them (`Literal` in the probe).

### N8 MINOR - Docs - PR body, Round 4 row "Merge model"; author-r4/HANDOFF.md:83 - the mutation count for rule 4 disagrees with the published output

- **Authority and evidence:** the PR body says "removing rule 4 fails 5", and the handoff says "`no_rule4` 5 cases". The published `merge_model.out` prints `no_rule4: caught by 7 case(s)`, and my re-run prints the same (`receipts/model/merge_model.txt:39`).
- **Why not RESIDUE:** this is a stated figure of executable evidence, and the owner's residue rule excludes figures.
- **Impact:** small. The mutation is caught either way, but a cold reviewer cannot reconcile the PR text with its evidence.
- **Required outcome:** the PR body reads "removing rule 4 fails 7".
- **Verification:** compare the PR body with `merge_model.out`.

## RESIDUE (wording only; each changes no figure, verdict, test or gate)

- **RR5** - SE:730, :735-736. "the partner carries the audio" assumes one network jumped. With both sequences jumping out of the span, both are discarded and the audio gaps until the head lapses. Arm C measures 24 to 30 samples missing, nothing outside the span, and no jumped duplicate, so the 22-packet bound holds.
  - Exact fix: SE:730 "Rule 4 discards them; an unjumped partner carries the audio." After SE:736, add a paragraph: "A jump on both networks gaps the same way."
- **RR6** - SE:1046. "A save waits for at most one compaction page." is now the fault-free case only, since SE:1123 adds one more.
  - Exact fix: "Fault-free, a save waits for at most one compaction page."
- **RR7** - SE:1008. Round 4 narrowed "A page failing read-back" to "A record page", which leaves a copy or replay page without a stated retry.
  - Exact fix: "Any non-header page failing read-back is rewritten further on."

## SUGGESTIONS (optional)

- **S4:** SE:1109-1110 requires that an all-zero header fail its check, and the flash model assumes it. Arm 3 of `scripts/probe_flash_r4.py` shows the requirement carries weight: with an all-zero header passing, 1,214 of 22,943 runs lose a change. SE:1224 could name "an all-zero header and an erased header fail #823's check".
- **S5:** the author's open point on the double fault. I accept the reading: the sector erase with saves held is a reported fault path outside the bound (SE:1115), like the record-page retry (SE:1009). So it does not breach "No flash erase may sit on the save path". NFR-REL-03 itself does not say reported faults lie outside it; one clause there would remove the question for the owner.
- **S6:** one failed header fits the slot, but a run of them does not, and the page does not say so. Under S1 and S2, a trigger at 392 free pages, one failed header and a restart take 17.78 s and at most 364 appended pages. A second failure in a row takes 33.52 s and up to 658 pages (`receipts/arith_r4.txt`). Nothing is lost in the model across two failures (Arm 1, 95,193 runs), but the slot can fill. The page could state what a persistent failure does.
- **S7:** after the switch-over the firmware AECP owner must raise `reboot_req_o`. Only the PR body says so, and no Mark II page mentions REBOOT. Lane 1's row in the area plan could carry it.

## Round-3 findings (R757-3) at this head

| Item | Closed by | Evidence at this head |
|---|---|---|
| N4 MINOR, failed header read-back | `309bfebc`, `b4b719ea` | **Closed.** Saves keep waiting while the header is zeroed, then erased if the zeroing fails its read-back (SE:1103-1118). The landing row is SE:1146, the power-cut rows SE:1154-1155. The test row SE:1224 and NFR-REL-03 (FR:476) name the case, including cuts before and after the standby's header sector is erased. See focus item 2 below |
| N5 MINOR, conversion error | `4d75675f` | **Closed.** The drift term covers latch to latch (SE:544-563, :571-577). E_x is 2.744 µs at SE:576, :604, :1219 and :1220. "2.210" has no hit on the four Mark II pages. See focus item 3 below |
| RR3 | `309bfebc` | **Closed.** SE:1153 reads as the exact fix |
| RR4 | `0f6ab84b` | **Closed.** SE:1219 reads as the exact fix plus "or rule 4", which is right because rule 4 is new |
| S1, odd copy time from the port 1 stamp | Not taken | Optional; the reason given (it changes the talker's conversion design) is acceptable |
| S2, a model deriving the error | `conversion_error.py` | **Taken.** Worst 2.640 µs over 201,280 cases, separation 2,916.999 µs |
| S3, a save during a save | `b4b719ea` | **Taken.** SE:1140 |

## What was checked, per focus item

1. **Round-3 findings:** see the table above.
2. **Header read-back:**
   - **Order:** no save can append while the failed header could still pass, in the page (SE:1106, :1117-1118) and in the model.
   - **Boot:** a zeroed or erased header fails its check, so boot keeps the old slot. A cut before the header reads back zeroed or erased may boot either slot, and both hold every durable save, because saves waited (SE:1154).
   - **365.10 ms:** 359.75 + 5.35 re-derived, and it counts one full `t_page` including the read-back (`receipts/arith_r4.txt`). The sum still over-counts, because a save cannot wait on the header and also arrive just after a save started. The 5.35 ms page is one more page and it is reported, as SE:1122 says.
   - **Tables:** every row of SE:1137-1147 and SE:1149-1156 holds against the ordering.
   - **Model** (`receipts/model/compaction_model.txt`, rc 0, byte-identical to the published output): 84,674 runs lose nothing. The failing sequence boots with the save at all 18 cuts. `no_invalidate` loses 1,214, `ignore_zero_rb` 1,214, `split` 733, `no_replay` 2,704.
   - **My probe** (`receipts/probe_flash_r4.txt`): a header failing twice running loses nothing over 95,193 runs. Running the waiting save before the zeroing loses 338 of 22,943, so the order matters.
3. **Conversion error:**
   - **Bound:** the talker latches at most 125 µs before the stamp. A rendered copy arrives by capture + offset + 125 µs, and the stamp follows the capture. So arrival is within 2.792 ms for offsets up to 2.667 ms, and the latches lie at most 2.917 ms apart. The reverse separation is at most 125 µs.
   - **A4:** stated at SE:556-560 and supported. `docs/reference/MILAN_COMPLIANCE_MATRIX.md:191` records 5.3.7.6's fixed delay of 0 to 125 µs. A larger offset needs the 2 ms class A transit plus the talker's stamp to wire inside 2.792 ms, leaving 792 µs against a worst stated talker bound of 123.337 µs.
   - **Figures:** 200 ppm x 2.917 ms = 0.5834 µs; 2.000 + 0.584 + 0.160 = 2.744 µs.
   - **Window:** margin 62.5 - 2.744 - 0.55 = 59.2 µs, neighbours 121.7 µs apart. It holds.
   - **Model:** rc 0, byte-identical, worst 2.640 µs.
   - **Bench row:** SE:1220 carries 2.792 ms and 2.744 µs.
4. **Listener merge:**
   - **Rules:** the page's rules 1 to 8 match the model line by line, except N7.
   - **LAST_TU:** defined at SE:886, reset 0, with reserved bits 31:13 filling the word; all LCTX_STATE bits are assigned.
   - **Rule 2:** holds a tu copy only while a clean partner can still come. The tu-on-both cases lose nothing at the stated skews.
   - **Rule 4:** an unplaceable tu copy is discarded and counted in `SE_MERGE_TU` (SE:650, :810), never written and never a duplicate.
   - **Milan v1.2 4.4.2.3:** the free-wheel "for an appropriate amount of time" belongs to the media clock servo as SE:717-718 says, consistent with `docs/design/MEDIA_CLOCK_FOLLOWING.md:666`. The stated gaps at SE:723-738 are correct as far as they go; N6 and RR5 are what they miss.
   - **Model** (`receipts/model/merge_model.txt`): rc 0, 33 PASS, byte-identical. `exact` fails 33, `own_time` 4, `no_rule2` 5, `r3_rule2` 13, `no_rule4` 7 (N8).
   - **Time step:** `probe_tu_step.py` reproduces; the pair loses no more than one network alone, so SE:721 holds.
5. **Open design items:** items 1 and 2 (SE:1236-1237) each carry a requirement and a verification row with a failing condition. Lane 6 owns them, and it exists at AP:276. Neither requirement is wrong, unsafe or unverifiable, so neither counts against the verdict.
6. **REQUIREMENTS.md scoping and the merge:**
   - **Scoping:** dev's line (REQUIREMENTS.md:472, the soft reset is the controller's AECP REBOOT) names no placement. AECP is among the control functions scoped at REQUIREMENTS.md:25-33, so the scoping covers it.
   - **Merge result:** against the pre-merge commit `2322c6d7`, the merge adds one line each to REQUIREMENTS.md and docs/README.md and removes nothing, and it changes none of the other five PR pages (`receipts/merge_effect.txt`). Dev changed nothing else in those two files or under `.github/`.
7. **Docs workflow:**
   - **My runs** (`receipts/gates/`, `receipts/gates_summary.tsv`): 23 commands in a pinned-renderer venv (cmarkgfm 2025.10.22, html5lib 1.1, PyYAML), all rc 0:
     - `docs_check.py`, 0 findings over 213 pages;
     - `check_em_dash.py --base 1f29f189`, 0 over 1,778 added lines in 7 pages, and its self-test;
     - `check_baremetal_only.py --check`, 0 over 1,434 files, and its self-test (867 arms);
     - `check_doc_paths.py`, 1,084 paths;
     - `gen_toc.py --selftest`, `--verify-anchors` (578 links) and `--check`;
     - the doc style, gPTP docs, DOC_MAP, time-sync, solution, submodule, feature-status, traceability and archive gates;
     - `git diff --check 1f29f189 HEAD`.
   - **Style probe:** `check_doc_style` `analyze()` over every changed block of the 7 touched pages finds 0 (`receipts/style_touched.txt`).
   - **Author receipts:** all 50 rc files at this head record 0, including both builder legs, the RV32 SDK, CI events and the act-runner contract. I did not re-run the submodule, SDK or builder steps. The delta has no file they scan.

### Commit shape, comment rule and privacy

- **Commits:** six one-line subjects with no bodies or trailers, then a merge with parents `2322c6d7` and `1f29f189`. The first-parent count from `e5b8405d` is 31, as the PR body says.
- **Comment rule:** no source file is in the delta, so no new instance is possible.
- **Privacy:** a grep of the added lines finds no private path, host, lane label, round or reviewer label.

### Evidence integrity

- **Manifest:** `MANIFEST.json` at `993a5bb5` lists 119 `author-r4` files. All match their published digests, with none missing and none unlisted (`receipts/evidence_integrity.txt`).
- **SHA256SUMS:** 106 of 118 entries verify. The 12 that do not are exactly the path-redacted files, which the manifest flags as such.
- **Live PR body:** equals the packet's PR-BODY.md apart from a trailing newline.
- **Signature:** the hosting service reports evidence commit `993a5bb5` as unsigned. I verified the packet by its digests, not by a commit signature.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N6) | NFR-REL-03 (FR:476); SE:530-577 against IEEE 802.1AS-2020 B.1.1, B.1.2, B.3, Milan v1.2 5.3.7.6 (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:191`) and IEEE 802.1BA-2011 6.5 as cited; SE:611-738 against IEEE 1722-2016 4.4.4.6, 4.4.4.7 and Milan v1.2 4.4.2.3, Annex D.3; REQUIREMENTS.md:25-33, :472 against dev `1f29f189` | R757-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| RTL | UNCLEAN (N6, N7) | merge rules SE:641-671 against `merge_model.py:103-186`, line by line; reference upkeep SE:673-687; LCTX_STATE and counters SE:808-810, :881-887, :902-903; window arithmetic `receipts/arith_r4.txt`; `receipts/probe_merge_r4.txt`. Code and registers the delta does not touch keep their R757-3 result | R757-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| Robustness | UNCLEAN (N6, N7) | failed header SE:1101-1125, landing and power-cut tables SE:1137-1156, `receipts/probe_flash_r4.txt`; merge under skew, startup tu, sequence jumps on one and both networks and time steps, `receipts/probe_merge_r4.txt`, `receipts/model/probe_tu_step.txt`; open design items SE:1236-1237 | R757-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| Tests | UNCLEAN (N6, N7) | three author models with every mutant, re-run, plus the time-step probe (`receipts/model/`); verification rows SE:1219, :1220, :1224 and NFR-REL-03's test clause; 23 docs gates re-run (`receipts/gates/`); author gate receipts and digests (`receipts/evidence_integrity.txt`); hosted check runs (`receipts/hosted_checks.tsv`) | R757-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |
| Docs | UNCLEAN (N6, N7, N8) | SE, AP:313 and FR:476 in the delta; REQUIREMENTS.md and docs/README.md merge results (`receipts/merge_effect.txt`); style probe (`receipts/style_touched.txt`); em dash, TOC, anchor, path and bare-metal gates; PR body round-4 table and known limitations; RR5 to RR7 | R757-4 | 22f3cedb420992b7b776c5a842b0b210ac4191d3 |

## Prior external findings (R758-3), read after my findings and lens results

Written after I recorded my verdict and findings. Each R758-3 item (issuecomment-6554550201) is resolved or retained at this head as follows.

| R758-3 item | At this head |
|---|---|
| F1 MINOR, tu on both | **Resolved for what it named:** rule 2 (SE:648), `LAST_TU` (SE:886), "tu on both networks" (SE:700-738), row SE:1219. Model cases at its latencies and onsets lose 0 samples, against its 30, 84 and 60, and `r3_rule2` fails 13. **New in the same area:** N6. A tu copy whose own time fails rule 1 still loses audio with both networks up. Its note that one firmware gPTP daemon can set tu on both ports makes that reachable |
| F2 MINOR, tu copy far from the head | **Resolved:** rule 4 (SE:650, SE:625-628), `SE_MERGE_TU` (SE:810), open design items 1 and 2. A jump of ±40 writes nothing outside the span and counts no duplicate; `no_rule4` fails 7. **New in the same area:** N7 and RR5 |
| F3 MINOR, intact header | **Resolved:** as N4 above |
| R1 RESIDUE | **Resolved:** SE:1263 and AP:313 carry its words, split into two sentences for the word limit |
| S1 | **Taken:** SE:1095-1096 |
| S2 | **Taken:** SE:568-569 |
| S3, carried | **Not taken, with a stated reason.** It is optional, so nothing is retained |

Prior rounds' findings were recorded as closed in R757-3, and the delta does not reopen them. There are no other public findings on #828 at this head.

## Real limits

- **Not re-run:** the submodule-dependent docs-workflow steps (HDL reference, RV32 SDK, builder legs, code ratchets, NVM, CI events, act contract). The clone has no submodules checked out. The author's published receipts at this head are the source-head evidence for them.
- **Hosted runs** (`receipts/hosted_checks.tsv`, 08:17 UTC): 19 completed successfully, 22 skipped, 3 in progress (`docs-gates-0`, `docs-gates-2` and one fail-fast context). `docs-gates-1`, `docs-check-no-git`, `wire-accountability`, `rtl-fast`, `elaborate`, `bdd-conformance` and `full-ci-gate` had succeeded. Skipped contexts are not executed evidence.
- **Standards:** no clause text was opened this round. IEEE 802.1AS-2020, IEEE 1722-2016, IEEE 802.1BA-2011 6.5 and N25Q128 5.1.2 are applied as the page and the handoff cite them. Milan v1.2 5.3.7.6 and 4.4.2.3 are checked only against the repository's own records of them.
- **Models:** every result comes from the author's host models and my probes on them, not from an implementation. The probes' skews and latencies are chosen to show the boundary; I did not measure how far a real talker's time steps.
- **Not used:** hardware, bench, act, a hosted re-run and the builder bank. Physical calibration was not run, and field skips are not hardware proof.
- **Manager bank:** no manager source bank ran at this head, and this round claims none.
- **Clone state:** the clone equals HEAD. The index tree is `aa3a82ea`, the mode, blob and path listings are identical, the worktree is clean, and the six gitlinks are unchanged. One ignored `scripts/__pycache__/`, created by this round's style probe, was removed (`receipts/clone_integrity.txt`).

## Pending manager duties

- Accept the hosted `docs-check` at this head, once `docs-gates-0` and `docs-gates-2` complete with all three legs executed.
- Accept `verilator-suites` and `yosys-portability` as skipped contexts for a documentation-only head.
- Validate the current-dev merge candidate at the merge turn, with the builder and native banks. Source base and live dev are both `1f29f189`.
- Get owner approval of the requirement text, and of the open owner decisions in the area plan.
- Carry RR5, RR6 and RR7 to the residue checklist.

R757-4 FINISHED
