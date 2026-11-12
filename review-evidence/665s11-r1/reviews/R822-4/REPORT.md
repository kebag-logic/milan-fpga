[R822] POSITIVE - exact head 049f0e4dd7b0b514d1ea9689822901750129c044

# R822-4: external review of PR #881 (issue #871, S11 AECP REBOOT), round 4 delta

- **Head under review:** `049f0e4dd7b0b514d1ea9689822901750129c044`, tree `dd6d3e4c734b8b26d19d5f33fcc45fa4b2a67b35`. The live PR head equals it. It is one commit with one parent, the previously reviewed head `6171d65473`.
- **Ruling under review:** the round 4 ruling, #871 issuecomment-6809457669, which accepts option (b) for AECP under item 4. It asks for the reason AECP has no B20 defect, and the three AECP layers' defects named, in B21's form. They go in four places: B20's comment, the loop-on defect's entry in `plat_mutants.py`, `REBOOT_RESET.md:309` with `plat/README.md:127`, and the PR body's ruling rows. Docs and comments only.
- **Delta (`6171d654..049f0e4d`):** four files, 22 insertions and 5 deletions.
  - Files: `docs/design/REBOOT_RESET.md` (1 line), `sw/firmware/ctrl/plat/README.md` (1 line), `sw/firmware/ctrl/test/plat_mutants.py` (5 comment lines added) and `sw/firmware/ctrl/test/test_plat_boot.cpp` (15 comment lines added, 3 removed).
  - Every changed line in a code file is a comment line (`receipts/delta-scope.txt`). No firmware, HDL, testbench or test logic changed.
  - `git diff --check 1d6bf555 049f0e4d` is clean.
- **Verdict: POSITIVE.** All five lenses are clean at this head. There is no open BLOCKER, MAJOR or MINOR. Two RESIDUE items are new and one is retained, all for the manager's checklist. Suggestions are listed at the end.

## Inputs, in order

1. AGENTS.md. CONTRIBUTING.md and docs/README were used only as the lens and authority map.
2. The round 4 ruling (issuecomment-6809457669).
3. The delta `6171d654..049f0e4d`, read in full, then the code it describes:
   - `aecp/aecp.c:194-208, 400-406, 635-643`;
   - `plat/ctrl_plat.c:170-180, 347-387`;
   - `test_aecp.cpp:1836-1872`;
   - `test_plat_boot.cpp:60-91, 922-1003`;
   - `plat_mutants.py:240-315`;
   - `aecp_mutants.py:830-844`.
4. The author's REVIEW READY for this head (issue #871, comment 6810579220) and the PR body.
5. The author's round 4 packet `review-evidence/665s11-r1/author-r4` at `de309102`.
6. The hosted check-run list at the exact head.
7. The round 3 reviews' findings (R822-3, comment 6809438458; R821-3, comment 6809453671), used only to resolve or retain each finding below.

## What I executed (receipts under `receipts/`)

All plants were written into copies under the packet's `scratch/` directory. The review clone was only read. After the probes its worktree, index and gitlinks are identical to the head (`receipts/integrity.txt`, `clone-status-before.txt` = `clone-status-after.txt`, both empty).

| Run | Result | Receipt |
|---|---|---|
| Packet manifest: every `author-r4/` entry of `MANIFEST.json` hashed against the published blob (`scripts/verify_manifest.py`) | 1029 entries, 1029 present, 0 mismatched, 0 unlisted | `manifest-author-r4.txt`, `.rc` |
| Table controls at the head: `ctrl_mutants.unnamed_tests()` on the full table, and `aecp_mutants.controls()` | no test named by no defect; AECP table drift control passes | `probes/result.json` |
| Table counts | 592 control defects (matches the author's "592 of 592"); 22 `plat-reboot-*`; 14 AECP `reboot-*` | reviewer command output, recorded in this report |
| The two platform defects the delta names, through the head's own `ctrl_mutants.campaign` (`scripts/r822_4_probes.py`, 16 jobs) | `plat-reboot-transmits-after-the-departing`: `[ok]`, **88 checks failed**, matching the author's REVIEW READY figure. `plat-reboot-takes-aecp-frames-after-the-success`: `[ok]`, 12 checks failed, its first on "B19 no AECP frame is taken after the REBOOT's SUCCESS". 2 of 2 caught | `probes.log`, `probes.rc` (0) |
| The two AECP defects the delta names, through the head's own `aecp_mutants.campaign` | `reboot-serves-after-its-success` and `reboot-probes-after-its-success` are each caught by `Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete` on their own words | `probes/aecp-results.json`, `probes/reboot-*.log` |
| Falsification of "B20's AECP check has no defect of its own": platboot1 with the loop-on defect alone, then paired with each AECP silence defect | rc 1 in all three runs. B20 fails on its ACMP, MAAP, SRP, "no other channel" and "no frame but ADP's" words. **It never fails on "B20 no AECP transmission starts after ENTITY_DEPARTING"**, even with two layers lifted | `probes/b20-loop*--platboot1.log`, `probes/result.json` |
| Hosted check runs at the exact head (read only) | `total_count` 0: no hosted run is recorded against `049f0e4d` | `hosted-checks.txt` |

## Ruling items, verified at this head

| Ruling place | Present | Where, and what it states |
|---|---|---|
| B20's comment | yes | `test_plat_boot.cpp:954-958` above `B20NoOtherChannelTransmitsAfterTheDeparting`, and its header entry at `:66-75`. They give the reason ("AECP starts no frame after its SUCCESS") and the three layers: the loop's stop, `plat-reboot-transmits-after-the-departing`; the receive gate, `plat-reboot-takes-aecp-frames-after-the-success`, caught by `NoFrameOfAnyChannelIsTakenFromTheSuccess` and `TheGateHoldsWhileTheResponseCannotBeHandedOver`; and AECP's own silence, `reboot-serves-after-its-success` and `reboot-probes-after-its-success`. The form matches B21's comment at `:1002-1003`: a reason, plus the test or defect that carries the property |
| The loop-on defect's entry | yes | `plat_mutants.py:254-258`, directly above `m("plat-reboot-transmits-after-the-departing", ...)`. It gives the same reason and the same three layers, each with the words that catch it. The form matches `channel_wait_mutants`' docstring for B21 (`:310-311`) |
| `REBOOT_RESET.md:309` with `plat/README.md:127` | yes | Both carry the reason and all four defect names. The section 8 row also says the loop's stop is caught "on the ACMP, MAAP and SRP checks" |
| The PR body's ruling rows | yes | A new round 4 table. The two round 3 rows ("No channel but ADP's ENTITY_DEPARTING ...", "A planted defect per channel ...") now state the reason and the three layers' defects |
| Docs and comments only | yes | `receipts/delta-scope.txt` shows no non-comment line changed in any code file |
| Each named defect exists and is caught | yes | All four are present in their tables (`probes/result.json` `present`), and each is caught on its own words at this head (table above) |

**The reason is true of the code.**
- The platform services the loop until `aecp_reboot_due`, and never after it (`ctrl_plat.c:377-387`).
- `aecp_reboot_due` holds until every REBOOT frame has completed, the SUCCESS response and its one unsolicited notification (`aecp.c:200-203`; `test_aecp.cpp:1844-1858`).
- From the SUCCESS, AECP takes no command (`aecp_ready`, `aecp.c:195-198`). After its owed frames, it starts no probe or notification (`aecp.c:635-643`).
- So for AECP to transmit after the DEPARTING, at least two independent layers must fail at once. The double-plant probes confirm the stronger point that in B20's scenario even such a pair does not reach the line. That is consistent with the accepted (b), and recorded as S1.

## Prior findings, resolved or retained at this head

| Finding | Status at `049f0e4d` | Evidence |
|---|---|---|
| R822-3 F1 = R821-3 F1 (MINOR): B20's AECP line has no planted defect and no recorded exclusion | **RESOLVED at its cause**, under the ruling's option (b) | The reason and the three layers' defects are stated in all four places (table above). The manager's acceptance is on #871 (issuecomment-6809457669). Each named defect is caught at this head |
| R822-3 RES1 = R821-3 RS1 (RESIDUE): `(B12)` in two new comments | **RESOLVED** | `test_plat_boot.cpp:79-80` and `:1003` now read `(TheResetWaitsForTheResponseToLeave)`, the test's name. The same commit adds new instances elsewhere; see RES-A |
| R822-3 S-a = R821-3 RS2: "in the pass that takes the REBOOT" read as covering all five channels | **RESOLVED** | `REBOOT_RESET.md:309` carries R821-3's exact fix word for word. `plat/README.md:127` carries the README fix |
| R821-3 RS3 (RESIDUE): the PR body's item 1 row still described round 2's B19 | **RESOLVED** | The PR body's round 2 row "1 Parity: from the SUCCESS no received frame of any channel is taken" now lists the five frames, B22, B23 and the five per-channel defects |
| R822-2 R2 (RESIDUE): when ADP's poll runs | **Retained**, not taken by the ruling | Unchanged at `REBOOT_RESET.md:290` and `plat/README.md:88` |
| R821-3 S7: B22's AECP words are required by no defect | **Retained** (suggestion, outside this delta) | `plat_mutants.py:270-274` requires B22's MAAP and SRP words only. `"B22 no AECP frame queued behind the REBOOT is taken"` (`test_plat_boot.cpp:1049, :1057`) is still in no `also` |
| R821-3 S8: header list style (B11 to B18 with the `B` prefix, B19 to B23 without) | **Retained** (suggestion) | `test_plat_boot.cpp:60-91` |
| R822-3 S-b = R821-2 S5: B20 does not check that the held frame is a DEPARTING | **Retained** (suggestion) | B20's body is unchanged |
| R821-2 S1 to S6 and the S4 export-tie decision | **Retained**; this delta does not touch their artifacts | S4 still needs the manager's decision |
| R822-2 S2: unsigned packet | **Retained as a limit** | The archive commit `de309102` is unsigned (`%G?` = N). I verified the published hashes against `MANIFEST.json` only |
| R821-1, R822-1, R821-2 and R822-2 findings resolved earlier | Unchanged | The delta changes no code they depend on |

## Findings

No BLOCKER, MAJOR or MINOR.

### RES-A RESIDUE: bench labels in a new source comment (owner comment rule)

- **Lenses:** Docs.
- **Where:** `sw/firmware/ctrl/test/plat_mutants.py:254-257`, new in this delta:
  - "caught on B20's ACMP, MAAP and SRP words. B20's AECP check has no defect of its own";
  - "(the receive gate, on B19's and B23's AECP words)".
- **Authority:** the owner's comment rule (2026-10-15). Source comments never show bench lane labels such as B17, and a new instance in the reviewed delta is RESIDUE.
  - The same commit removed `(B12)` from two comments for this reason. The new comment in `test_plat_boot.cpp:954-958` already avoids labels.
  - The PR body may keep the labels.
- **Impact:** wording only. No word, test or defect changes.
- **Exact fix:** in `plat_mutants.py:254-257`:
  - "caught on B20's ACMP, MAAP and SRP words. B20's AECP check" becomes "caught on NoOtherChannelTransmitsAfterTheDeparting's ACMP, MAAP and SRP words. Its AECP check";
  - "on B19's and B23's AECP words" becomes "on NoFrameOfAnyChannelIsTakenFromTheSuccess's and TheGateHoldsWhileTheResponseCannotBeHandedOver's AECP words".
- **Verification:** `git diff` of the comment, then `check_py_idiom.py` for the 120-column limit.

### RES-B RESIDUE: punctuation makes the section 8 list ambiguous

- **Lenses:** Docs.
- **Where:** `docs/design/REBOOT_RESET.md:309`: "AECP's check after the DEPARTING has no defect of its own, because AECP starts no frame after its SUCCESS: its three layers each carry one, the loop's stop (...), the receive gate (...) and AECP's own silence (...)".
  - The comma after "each carry one" lets "one" read as the first item of the list.
  - The README (`:127`) and the test comment already use a colon at that point.
- **Impact:** wording only.
- **Exact fix:** "... because AECP starts no frame after its SUCCESS. Its three layers each carry one: the loop's stop (...), the receive gate (...) and AECP's own silence (...)".
- **Verification:** read the row; the docs gates (`check_doc_style.py`, `docs_check.py`) stay rc 0.

### Retained RESIDUE

- **R822-2 R2:** "From the loop's last pass ... and ADP's poll until the port fires" at `REBOOT_RESET.md:290` and `plat/README.md:88`. Not taken by the round 3 or round 4 ruling. R822-2's exact fix still applies.

### Suggestions (do not affect coverage)

- **S1 (Tests, Docs): B20's AECP line is not reached even by a pair of defects in this scenario.**
  - With the loop serviced after the DEPARTING and either AECP silence defect also planted, B20 still passes on its AECP words (`probes/b20-loop-probes--platboot1.log`, `b20-loop-serves--platboot1.log`). B20 gives AECP nothing to receive or send in the window.
  - That is within the accepted (b). An optional clause in the B20 comment would make it explicit for a later reader: "and B20 gives AECP nothing to send, so the line holds even with two layers lifted".
- **S2 (Docs): "AECP starts no frame after its SUCCESS" is exact only in the repository's own sense.**
  - The REBOOT's own unsolicited notification is handed over after the SUCCESS response (`test_aecp.cpp:1844`, "the SUCCESS response, then one notification"). It completes before the loop stops (`aecp_reboot_due`).
  - The repository already treats those as the SUCCESS's own frames (`aecp.c:636-638`; `test_aecp.cpp:1863`), so the statement is not wrong.
  - For a cold reader, an optional precision: "AECP starts no frame after its SUCCESS but the REBOOT's own response and notification, which complete before the loop stops".
- **S3 (Docs): the README join reads as two list ends.** `plat/README.md:127`: "... while its SUCCESS cannot be handed over, and the MAAP, SRP and AECP frames queued with the REBOOT left in the pass that takes it, no ACMP, AECP, MAAP or SRP transmission ..., and the DEPARTING held ...". Optional: drop the first "and", or use "; " around the in-pass clause.
- **Retained from earlier rounds:** S7 and S8 (R821-3); S-b (B20's held frame not checked to be a DEPARTING); R821-2 S1 to S6.

## Lens results (this round, at `049f0e4d`)

```text
[R822] PASS Conformance - #871 issuecomment-6809457669 items vs test_plat_boot.cpp:66-75,954-958; plat_mutants.py:254-258; REBOOT_RESET.md:309; plat/README.md:127; PR body round 4 and round 3 rows - all four places state the reason and the three layers' defects in B21's form; the reason checked against aecp.c:195-203,635-643 and ctrl_plat.c:347-387 (Milan v1.2 5.6.3.3, IEEE 1722.1-2021 7.4.43 behaviour unchanged)
[R822] PASS RTL - receipts/delta-scope.txt (git diff 6171d654..049f0e4d: no HDL, testbench, firmware source or generated file; every code-file line changed is a comment) - lens inapplicable to the delta; R822-3's RTL verdict stands because nothing it depends on changed
[R822] PASS Robustness - ctrl_plat.c:377-387, aecp.c:195-203,635-643, receipts/probes/b20-loop*--platboot1.log - the layered silence after the DEPARTING holds with one and with two layers lifted; no behaviour changed in the delta
[R822] PASS Tests - receipts/probes.log, probes/result.json, probes/aecp-results.json - the four named defects exist and are caught on their own words (88 and 12 failed checks; both AECP defects caught); table controls pass; 592 / 22 / 14 counts; no test logic changed (delta-scope.txt)
[R822] PASS Docs - REBOOT_RESET.md:309, plat/README.md:127, test_plat_boot.cpp:66-80,954-958,1002-1003, plat_mutants.py:254-258, PR body - the ruling's text is present and accurate; R822-3 RES1 / R821-3 RS1, RS2 and RS3 resolved; RES-A and RES-B are RESIDUE (wording only) and leave the lens clean
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | ruling 6809457669; `test_plat_boot.cpp:66-75, 954-958`; `plat_mutants.py:254-258`; `REBOOT_RESET.md:309`; `plat/README.md:127`; PR body ruling rows; `aecp.c:195-203, 635-643`; `ctrl_plat.c:347-387` | R822-4 | `049f0e4dd7b0b514d1ea9689822901750129c044` |
| RTL | CLEAN | `receipts/delta-scope.txt` (no RTL, testbench or firmware source in the delta); prior RTL coverage R822-3 at `6171d654`, which nothing in this delta's scope has touched since | R822-4 (inapplicable delta; R822-3 basis) | `049f0e4dd7b0b514d1ea9689822901750129c044` |
| Robustness | CLEAN | `ctrl_plat.c:377-387`; `aecp.c:195-203, 635-643`; the double-plant probes `receipts/probes/b20-loop*` | R822-4 | `049f0e4dd7b0b514d1ea9689822901750129c044` |
| Tests | CLEAN | `receipts/probes.log`; `probes/result.json`; `probes/aecp-results.json`; `plat_mutants.py:240-315`; `aecp_mutants.py:837-843`; `test_aecp.cpp:1836-1872`; `test_plat_boot.cpp:922-1003` | R822-4 | `049f0e4dd7b0b514d1ea9689822901750129c044` |
| Docs | CLEAN (RES-A, RES-B and R822-2 R2 carried as RESIDUE) | `REBOOT_RESET.md:290, 309`; `plat/README.md:88, 127`; the delta's comments; PR body; REVIEW READY 6810579220 | R822-4 | `049f0e4dd7b0b514d1ea9689822901750129c044` |

## Real limits

- **One reviewer.** This is one external delta review. CONTRIBUTING's two-positive bar needs the internal review as well.
- **Not run at this head:** the full platform self-test (`test_ctrl_firmware.py --require-rv32 --self-test`) and the docs workflow.
  - For those I rely on the author's round 4 receipts. Their bytes match the manifest, and they show `fw_selftest.rc` 0, `diffcheck.rc` 0 and the docs table at 64 rc 0, 31 NOT RUN with reasons, 0 failed.
  - `fw_selftest.log` itself is published only as a hash (`round4/gates/lane/LARGE.tsv`). I reproduced the part of it this round's claim depends on: the four named defects, and the 88-check figure.
- **No cryptographic signature:** the evidence archive commit is unsigned. I checked manifest integrity only.
- **Order of reading:** the comment listing that showed the manager's review-start comment also showed the opening paragraphs of the two round 3 reports, before my own pass was complete. I read their findings sections only after my own pass over the delta, the code and the probes was complete.
- **Hosted evidence:** no hosted check run is recorded at `049f0e4d`. I claim nothing about hosted or act results.
- **Not covered:** no manager source bank and no current-dev merge candidate. Physical calibration was NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Carry RES-A, RES-B and the retained R822-2 R2 to the residue checklist.
- The internal review at this head.
- The current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b`): builder and native banks, with receipts linked on the PR.
- Hosted and act acceptance at the exact head. None is recorded yet.
- The still-open decisions:
  - R821 S4 (a 0 tie in the all-fabric top `.v`);
  - the new issue for the split boot simulation's unpinned hash seed;
  - #871 stays "Relates to" while acceptance item 1 is partial.
- Merge only on explicit maintainer authorization.

R822-4 FINISHED
