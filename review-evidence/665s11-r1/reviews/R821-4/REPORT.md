[R821] POSITIVE - exact head 049f0e4dd7b0b514d1ea9689822901750129c044

# R821-4: internal cleared-context review of PR #881 (issue #871, S11 AECP REBOOT on the split CPU), round 4 delta

- **Head and scope.** Head `049f0e4dd7b0b514d1ea9689822901750129c044`, tree `dd6d3e4c734b8b26d19d5f33fcc45fa4b2a67b35`. The delta is `6171d654..049f0e4d`: one author commit, made under the round 4 ruling (#871 issuecomment-6809457669). That ruling accepts option (b) for AECP in item 4 and allows comments and docs only.
- **Comments and docs only: verified.** `receipts/delta-scope.txt` (script `scripts/delta_scope.sh`) shows:
  - The delta touches four files: `docs/design/REBOOT_RESET.md`, `sw/firmware/ctrl/plat/README.md`, `sw/firmware/ctrl/test/plat_mutants.py` and `sw/firmware/ctrl/test/test_plat_boot.cpp`.
  - `test_plat_boot.cpp` with its comments stripped is identical at both commits.
  - The Python AST of `plat_mutants.py` is identical at both commits.
  - No firmware, HDL, testbench, generated or submodule file changed, and no file mode changed.
  - `git diff --check` against the merge base `1d6bf555` is clean.
  - The widest added line is 118 columns, and the delta adds no em dash.
- **Summary.** All four places the ruling lists now state why AECP has no B20 defect: AECP starts no frame after its SUCCESS. Each place names the three AECP-layer defects that cover the check, in the same form as B21's exclusion. I confirmed that each named defect exists in its table and is caught on its own words at this head (probes below). R821-3 F1 and R822-3 F1 are resolved by the manager's acceptance of option (b) and the text the ruling required. R821-3 RS1 to RS3 are resolved as written.
- **Open items.** None are blocking. One new RESIDUE: the new `plat_mutants.py` comment uses test-ID labels, against the owner comment rule. There are three SUGGESTIONs, and the prior residue and suggestions are listed below as retained.

## The ruling's four places, checked at this head

**The reason, in B21's form.** B21's form is the exclusion argued in its test comment, its mutant docstring, `REBOOT_RESET.md:309` and the PR row. Each of these four places now gives the same reason: AECP starts no frame after its SUCCESS, so B20's AECP check has no defect of its own. Each then names the three layers and their defects:

- the loop's stop: `plat-reboot-transmits-after-the-departing`;
- the receive gate: `plat-reboot-takes-aecp-frames-after-the-success`;
- AECP's own silence: `reboot-serves-after-its-success` and `reboot-probes-after-its-success` in `aecp_mutants.py`.

**The four places:**

| Place | Present | Notes |
|---|---|---|
| B20's comment, `test_plat_boot.cpp:954-958`, and its header entry `:66-75` | yes | Tests are named by name. The loop-on defect is "caught on this test's ACMP, MAAP and SRP checks". The gate defect is "caught by NoFrameOfAnyChannelIsTakenFromTheSuccess and TheGateHoldsWhileTheResponseCannotBeHandedOver". |
| The loop-on defect's entry, `plat_mutants.py:254-258` | yes | The content is correct, but it uses `B20's`, `B19's` and `B23's` (RS-A). |
| `REBOOT_RESET.md:309` with `plat/README.md:127` | yes, at exactly those lines | REBOOT_RESET also ties the loop-on defect to "the ACMP, MAAP and SRP checks". |
| The PR body's ruling rows | yes | The round 4 row (body line 47), the round 3 row "No channel but ADP's ENTITY_DEPARTING ..." (line 58) and the row "A planted defect per channel ..." (line 60). |

**Is the stated reason true at the head?** Read against the code:

- `aecp.c:197`: `aecp_rx_ready` refuses every command while `reboot != 0`.
- `aecp.c:635-643`: once the REBOOT is accepted, the poll returns before `asynchronous()` and `arm()`. So no probe, lock-expiry notification or unsolicited notification is started. Only the frames still owed are handed over (`transmit()`, `aecp.c:472-505`): the SUCCESS, then the REBOOT's own notifications.
- `ctrl_plat.c:347-387`: the loop is no longer serviced once `aecp_reboot_due`. ENTITY_DEPARTING is committed after that.

So by the DEPARTING, AECP has nothing to start. This holds even if the loop were serviced. The reason is correct. A wording precision is noted as S-B.

## What I executed

Everything ran in disposable copies under the packet's `scratch/`. The review clone was the read-only source root.

**Probes of the named defects, using the repository's own campaign code** (`scripts/probe_named_defects.py`; receipts `receipts/probe-plat.log` and `receipts/probe-aecp.log`, both rc 0):

| Probe | Result |
|---|---|
| Unplanted head (a no-op edit) | platboot1: 0 failed checks |
| `plat-reboot-transmits-after-the-departing` | **caught**. 22 distinct failed checks, including the B20 words for ACMP, MAAP and SRP and the aggregate line. The campaign tallies 88 because it runs the arm once per required word. |
| `plat-reboot-takes-aecp-frames-after-the-success` | **caught** on the B19 and B23 AECP words (12 failed checks) |
| AECP `reboot-serves-after-its-success` | **caught**, `Core.RebootIsAnsweredNotifiedAndDueOnlyOnceItsFramesComplete` "no command is taken after a REBOOT's SUCCESS" |
| AECP `reboot-probes-after-its-success` | **caught**, same test, "no probe or notification is started after a REBOOT's SUCCESS". The AECP table's drift and reader controls were run on the full table before filtering. |
| Reviewer-only combination: loop-on plus `reboot-probes-after-its-success` | B20's AECP words still pass. The 22 failures are identical to loop-on alone (`receipts/probe-combined-{both,loop}.platboot1.log`, script `scripts/probe_combined_log.py`). See S-A. |

**Docs and idiom gates on the clone** (`receipts/gate-*`):

- rc 0: `docs_check.py` (0 findings, 218 md files), `check_doc_paths.py` (1091 paths), `check_doc_style.py`, `check_cpp_idiom.py` and `check_py_idiom.py`.
- Could not judge: `check_em_dash.py --base 1d6bf555` and `gen_toc.py --check` / `--verify-anchors` both refused because the pinned Markdown renderer (html5lib) is not installed, and installing it is out of my scope. The delta adds no em dash and changes no heading or anchor (delta-scope receipt), and the author's `docs.yml` receipt covers these gates (next bullet).

**The author's round 4 receipts.** These are in archive `de309102`, `review-evidence/665s11-r1/author-r4/receipts/round4/`. That commit is unsigned (GitHub reason "unsigned"). Eight receipts match `MANIFEST.json`'s `published_sha256` (`receipts/author-r4-spotcheck.txt`):

- `lane/fw_selftest.rc` = 0 at head `049f0e4d`. `fw_selftest.log` is listed by digest only (`LARGE.tsv`), so its count of 592 rests on that rc and the PR.
- `lane/diffcheck.rc` = 0.
- `drivers/D.log` ends "docs-check done, failed 0".
- `docs-table.md` shows the docs.yml steps.

**Hosted evidence.** A read-only snapshot at 2026-11-12T00:44Z found no check runs, statuses or workflow runs for the head (`receipts/hosted-checks-snapshot.txt`). I claim nothing from it. The manager owns hosted and act acceptance.

**Restore check** (`receipts/restore-check.txt`):

- HEAD and tree are exact. `write-tree` is `dd6d3e4c`, and the worktree equals the index, which equals HEAD.
- The index modes and blobs equal the HEAD tree.
- All six gitlinks are at their recorded commits, with `external` uninitialised as at the start.
- The docs gates' child processes created three ignored `__pycache__/` directories during this session (`avdecc/`, `protocol-processor/hdl/aecp/desc/`, `sw/litex/platforms/`). I removed them, and none remain.

## Findings

### RS-A RESIDUE - Docs - test-ID labels in the new `plat_mutants.py` comment (owner comment rule)

- **Where:** `sw/firmware/ctrl/test/plat_mutants.py:254-258`, new in this delta. It reads "caught on B20's ACMP, MAAP and SRP words. B20's AECP check ..." and "(the receive gate, on B19's and B23's AECP words)".
- **Authority:** the owner comment rule of 2026-10-15: source comments never show bench lane labels. This is the same class as R821-3 RS1 and R822-3 RES1, which this round fixed in `test_plat_boot.cpp` by naming the tests. The `B19`/`B20`/`B23` Python constants in the code are identifiers, not comments, and are out of this finding.
- **Impact:** wording only. No code, test, figure or verdict changes.
- **Exact fix:** replace the five comment lines with these six (widest line 117 columns):

```text
        # The loop serviced after the DEPARTING, caught on NoOtherChannelTransmitsAfterTheDeparting's ACMP, MAAP
        # and SRP words. Its AECP check has no defect of its own, because AECP starts no frame after its SUCCESS;
        # each of its three layers carries one: this one (the loop's stop),
        # plat-reboot-takes-aecp-frames-after-the-success (the receive gate, on the AECP words of
        # NoFrameOfAnyChannelIsTakenFromTheSuccess and TheGateHoldsWhileTheResponseCannotBeHandedOver) and
        # reboot-serves-after-its-success and reboot-probes-after-its-success in aecp_mutants.py (AECP's own silence)
```

- **Verification:** `grep -n "B[0-9][0-9]'s" sw/firmware/ctrl/test/plat_mutants.py` prints nothing, and `check_py_idiom.py` gives rc 0.

### S-A SUGGESTION - Tests - B20's AECP check stays unreachable even with two of its three layers removed

- **Evidence:** the combination probe above. The loop serviced after the DEPARTING, plus AECP's poll falling through to `asynchronous()` after the REBOOT, gives the same 22 failures as the loop-on defect alone, and "B20 no AECP transmission starts after ENTITY_DEPARTING" passes. The reason is that B20 (`test_plat_boot.cpp:959-999`) registers no controller and delivers no AEM command in the window, so AECP has no asynchronous frame it could start.
- **Why this is not a finding:**
  - The ruling accepted option (b) knowing this (R821-3 F1 measured the same).
  - None of the four places claims that the check is live. They say it "has no defect of its own".
  - Each layer is independently caught.
- **Optional improvement:** give B20's window an AECP producer, such as a controller registered for unsolicited notifications with a change pending, or a lock expiring in the window. The combined defect would then redden the AECP line. This would be R821-3's option (a), which the ruling did not take.

### S-B SUGGESTION - Docs - "AECP starts no frame after its SUCCESS" is meant as "no new frame"

- **Where:**
  - `test_plat_boot.cpp:66-67,954`;
  - `plat_mutants.py:255`;
  - `REBOOT_RESET.md:309`;
  - `plat/README.md:127`;
  - the PR rows at lines 47, 58 and 60.
- **The precision:** with other controllers registered, the REBOOT's own notifications are handed over after the SUCCESS frame (`aecp.c:474-500`). The sentence holds as "starts no new frame". That is the convention AECP's own test words use ("no probe or notification is started after a REBOOT's SUCCESS"), and the B21 clause beside it ("holds only the REBOOT's own frames") covers the rest.
- **Optional wording:** "AECP starts no frame after its SUCCESS but the REBOOT's own notifications, which complete before the DEPARTING (`aecp_reboot_due`)".

### S-C SUGGESTION - Docs (PR body) - "on 88 failed checks" is the campaign's tally, not distinct checks

- **Where:** the PR's round 4 local-gates table (body line 145): "`plat-reboot-transmits-after-the-departing` on 88 failed checks". The REVIEW READY says the same.
- **What the number is:** platboot1 fails 22 distinct checks. `ctrl_mutants.campaign` runs the arm once for each of the defect's four required words and sums the failures. So 88 faithfully copies the receipt line, but it is 22 × 4.
- **Optional wording:** "22 failed checks in platboot1 (the campaign's tally of 88 counts one arm run per required word)".

## Prior findings, resolved or retained at this head

I read these only after my own pass over the diff.

| Finding | State at 049f0e4d | Evidence |
|---|---|---|
| **R821-3 F1** (MINOR, Tests and Docs): B20's AECP check has no stimulus and no defect, while the PR says every channel has one | **Resolved**, by option (b) as accepted in #871 issuecomment-6809457669 | The four places above state the reason and name the three defects. Each defect exists and is caught (probes). The PR rows no longer claim a B20 AECP defect: line 60 says "B20 has no AECP defect" and gives the reason. |
| **R822-3 F1** (MINOR, Tests and Conformance): B20's AECP line is reached by no planted defect | **Resolved**, under the same ruling | as above |
| R821-3 RS1 = R822-3 RES1: `(B12)` in two rewritten comments | **Resolved** | `test_plat_boot.cpp:80` and `:1003` now read `(TheResetWaitsForTheResponseToLeave)`. The pre-existing `(B18)` at `:186` and `(B12)` at `:210` are outside the delta and tracked by #746. |
| R821-3 RS2 = R822-3 S-a: "in the pass that takes the REBOOT" read as covering all five channels | **Resolved**, with the exact fix text | `REBOOT_RESET.md:309` and `plat/README.md:127` now match RS2's text verbatim. B22's words ("B22 no AECP/MAAP/SRP frame ... is taken") match. |
| R821-3 RS3: the PR's item-1 row described round 2's B19 | **Resolved** | PR body line 69 now carries RS3's exact text. |
| R822-2 R2 RESIDUE: when ADP's poll runs | **Retained**; not taken by the ruling | `REBOOT_RESET.md:290` and `plat/README.md:88` are unchanged in this delta |
| R821-3 S7: B22's AECP words are required by no defect | **Retained**; the delta changes no table entry (the AST is identical) | `plat_mutants.py`: no defect lists "B22 no AECP frame queued behind the REBOOT is taken" |
| R821-3 S8: the header list's B-prefix style is mixed | **Retained** | `test_plat_boot.cpp:56-80` |
| R821-2 S1 to S6 and R822-3 S-b (= S5) | **Retained**; the delta does not touch their artifacts | S4 (the 0 tie versus byte-identical exports) is still pending the manager's decision |
| R821-1, R822-1 and R821-2/R822-2 F1 | Resolved in earlier rounds. This delta changes nothing they depend on. | delta-scope receipt |

## Lens results (this round, at 049f0e4dd7b0b514d1ea9689822901750129c044)

```text
[R821] PASS Conformance - #871 issuecomment-6809457669 (option (b), four places) against test_plat_boot.cpp:66-75,954-958; plat_mutants.py:254-258; REBOOT_RESET.md:309; plat/README.md:127; PR body rows 47,58,60 - all four places state the reason and name the three defects; the reason checked against aecp.c:197,472-505,635-643 and ctrl_plat.c:347-387 (no new AECP frame once accepted; loop stopped at aecp_reboot_due; DEPARTING after it); no behaviour change in the delta (receipts/delta-scope.txt), so issue acceptance stays items 2-5 met and item 1 partial as ruled
[R821] PASS RTL - receipts/delta-scope.txt - no HDL, testbench, firmware source, generated file or gitlink in 6171d654..049f0e4d; the R821-3 RTL result (test HAL overrides, ctrl_loop.c service order, drained()) depends on nothing the delta changes and stands
[R821] PASS Robustness - receipts/delta-scope.txt; aecp.c:635-643; receipts/probe-combined-*.platboot1.log - no code change; the layered silence after the DEPARTING holds with the loop serviced (only ACMP, MAAP and SRP react); B21 per ring and B23 full ring are unchanged from R821-3
[R821] PASS Tests - receipts/probe-plat.log, receipts/probe-aecp.log; plat_mutants.py:247-310 (AST identical to 6171d654); aecp_mutants.py:837-843 - all four named defects exist and are caught on their own words at the head, the unplanted head fails 0 checks, and the author's fw_selftest.rc=0 at 049f0e4d is manifest-verified; S-A is optional and accepted by the ruling
[R821] PASS Docs - REBOOT_RESET.md:309, plat/README.md:127, test_plat_boot.cpp:66-80,954-958,1002-1003, plat_mutants.py:254-258, PR body lines 47,58,60,69,145 - the reason and the defect names are true against the tables and the code; RS1-RS3 are fixed as written; the docs/idiom gates give rc 0 (two need a renderer not installed here, covered by the author's docs.yml receipt); RS-A is RESIDUE only; S-B and S-C are optional
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | the round 4 ruling against the four places; `aecp.c:197,472-505,635-643`; `ctrl_plat.c:347-387`; delta scope | R821-4 | 049f0e4dd7b0b514d1ea9689822901750129c044 |
| RTL | CLEAN | `receipts/delta-scope.txt` (no HDL, testbench or firmware source in the delta); R821-3's RTL result carried, since nothing it depends on changed | R821-4 (carried from R821-3 at 6171d654) | 049f0e4dd7b0b514d1ea9689822901750129c044 |
| Robustness | CLEAN | delta scope; layered silence (`aecp.c:635-643`, combination probe logs); B21/B23 unchanged | R821-4 | 049f0e4dd7b0b514d1ea9689822901750129c044 |
| Tests | CLEAN (S-A optional) | `probe-plat.log` (4 runs), `probe-aecp.log` (2 defects), combination probes; `plat_mutants.py` AST; `aecp_mutants.py:837-843`; author `fw_selftest.rc` | R821-4 | 049f0e4dd7b0b514d1ea9689822901750129c044 |
| Docs | CLEAN (RS-A RESIDUE; S-B and S-C optional) | `REBOOT_RESET.md:309`; `plat/README.md:127`; `test_plat_boot.cpp` comments; `plat_mutants.py:254-258`; PR body; docs/idiom gate receipts | R821-4 | 049f0e4dd7b0b514d1ea9689822901750129c044 |

## Real limits

- I did not run the full firmware self-test (592), the full AECP campaign (153), the `ctrl_reboot` CPU simulation or `docs.yml`. They rest on:
  - the author's manifest-verified receipts: round 4 `fw_selftest.rc`, `diffcheck.rc` and the docs driver log;
  - round 3's receipts for the AECP driver and the REBOOT simulation, which a comments-only delta cannot change.
- `check_em_dash.py` and `gen_toc.py` could not judge on this host (the pinned renderer is not installed).
- The evidence archive commit `de309102` is unsigned. I verified the published hashes against `MANIFEST.json` only.
- Physical calibration was NOT RUN, and field skips are not hardware proof. No hardware was used.
- No manager source bank ran at this head, and I claim none. Hosted contexts show no runs at this head.

## Pending manager duties

- Carry RS-A, and the retained R822-2 R2, to the residue checklist.
- Decide R821 S4 (the 0 tie on `i_reboot_req` in the all-fabric instances), and open the issue for the split boot simulation's unpinned hash seed, both still pending from round 2.
- Hosted and act acceptance at the exact head.
- Build and validate the current-dev merge candidate at the merge turn (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`), with builder and native banks, and link the receipts.
- The second independent review and the full completion bar before any merge.

R821-4 FINISHED
