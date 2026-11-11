[R821] NEGATIVE - exact head 6171d65473875239d97e6f6b9327c394db65aab8

# R821-3: internal cleared-context review of PR #881 (issue #871, AECP REBOOT on the split CPU), round 3 delta

- **Head and scope.** Head `6171d65473875239d97e6f6b9327c394db65aab8`, tree `3db1feb17473d462b567347841f7219838d2b893`. The delta is `d08d30c6..6171d654`: one author commit, made under the round 3 ruling (#871 issuecomment-6806697914).
- **What the delta touches.** `git diff --name-only d08d30c6ec..HEAD` names six files: `docs/design/REBOOT_RESET.md`, `sw/firmware/ctrl/plat/README.md`, `sw/firmware/ctrl/test/{aecp_mutants.py, plat_mutants.py, test_aecp.cpp, test_plat_boot.cpp}`. No firmware source changed, so there is **no firmware behaviour change**. `ctrl_plat.c` and `aecp.c` are byte-identical to `d08d30c6`. Code outside the delta keeps its R821-2 lens verdict, because nothing it depends on changed.
- **Summary.** My round 2 F1 is **resolved at its cause**. All of the following now hold, and my round 2 probes, run unchanged, fail on REBOOT words where they passed before:
  - every channel's receive is refused from the SUCCESS, each channel named;
  - the gate holds in the pass that takes the REBOOT;
  - the gate holds while the SUCCESS cannot be handed over;
  - the AECP core test checks acceptance before any poll.
- **Why NEGATIVE.** One new MINOR is open (F1, Tests and Docs). The ruling's second item asks that no channel but ADP start a transmission after ENTITY_DEPARTING, and its fourth asks for a planted defect per channel. For AECP the second item has no planted defect, and B20 gives AECP nothing to send. So B20's new AECP check cannot fail: I lifted both of the layers that keep AECP silent and it still passed. Unlike B21's AECP exclusion, no reason is recorded for this gap, and the PR says the item is met. Three RESIDUE items and one retained RESIDUE are listed for the manager's checklist.

## Findings

### F1 MINOR - Tests, Docs - B20's AECP check has no stimulus and no planted defect, but the PR says every channel has one

- **Where:**
  - `sw/firmware/ctrl/test/test_plat_boot.cpp:976-983` (B20's per-channel loop, which includes AECP at `:981`).
  - `sw/firmware/ctrl/test/plat_mutants.py:254-258`. The loop-on defect `plat-reboot-transmits-after-the-departing` requires the ACMP, MAAP and SRP words only.
  - The PR's round 3 ruling rows. "No channel but ADP's ENTITY_DEPARTING starts a transmission after it: yes" says B20 "checks ACMP, AECP, MAAP and SRP by name". "A planted defect per channel, failing by its own words: yes" lists no defect for B20 at all.
  - `docs/design/REBOOT_RESET.md:309`, which lists "no ACMP, AECP, MAAP or SRP transmission after ENTITY_DEPARTING" among what B11 to B23 prove.
- **Authority:**
  - The round 3 ruling, items 2 and 4: "no channel but ADP's ENTITY_DEPARTING starts a transmission after ENTITY_DEPARTING" and "each comes with a planted defect per channel, failing by its own words".
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect".
- **Evidence:**
  - **Static.** I imported the table at the head. Of the 22 REBOOT defects, none requires "B20 no AECP transmission starts after ENTITY_DEPARTING". Only `plat-reboot-takes-aecp-frames-after-the-success` names AECP at all, and it names B19 and B23 words, not B20.
  - **Executed.** `scripts/probe_r3.py`, receipt `receipts/probe-r3-all.log`, probe `aecp-transmits-after-the-departing`. The probe makes two edits:
    - it services the loop after the DEPARTING (the shipped loop-on defect's own edit);
    - it lifts the AECP core's silence once the REBOOT's frames are out (`aecp.c` poll: `return false` only while `reboot != 2`).
  - **Result.** platboot1 rc 1, with 22 failed checks: the generic B20 words, the ACMP, MAAP and SRP words, and "no frame but ADP's leaves". **"B20 no AECP transmission starts after ENTITY_DEPARTING" passes.** B20 delivers no AEM command after the DEPARTING and registers no controller that is owed a notification. So AECP has nothing it could send there, and its check is vacuous in this scenario.
  - **Contrast with B21.** B21's AECP exclusion is argued in the test comment (`test_plat_boot.cpp:990-991`), in the mutant docstring (`plat_mutants.py:304-306`), in `REBOOT_RESET.md:309` and in the PR row. B20's AECP omission is argued nowhere.
- **Impact:**
  - The head's behaviour is correct, and the property does hold in the product. Three layers keep AECP silent after the DEPARTING, and each has its own defect elsewhere:
    - the loop stopped: B20's ACMP, MAAP and SRP words under `plat-reboot-transmits-after-the-departing`;
    - the receive gate: B19 and B23's AECP words under `plat-reboot-takes-aecp-frames-after-the-success`;
    - AECP's own silence: the AECP table's `reboot-serves-after-its-success` and `reboot-probes-after-its-success`.
  - The problem is the evidence. One per-channel assertion that the ruling required cannot fail, and the PR records the item as met.
- **Required outcome (either):**
  - (a) B20 gives AECP something it would send after the DEPARTING under a defect, for example an AEM command delivered while the DEPARTING is held. A planted defect then fails on "B20 no AECP transmission starts after ENTITY_DEPARTING". As with the gate's AECP defect, that defect opens AECP's layers together.
  - (b) As B21 does, B20's comment, the loop-on defect's table entry, `REBOOT_RESET.md:309` and the PR ruling rows state why AECP has no B20 defect (the three layers above, each with its own defect). The manager then accepts this as meeting item 4 for AECP.
  - Option (b) is the smaller change. It needs the manager's acceptance because the ruling says "per channel".
- **Verification:**
  - For (a): the new defect gives platboot1 rc 1 on the AECP B20 words, and `python3 -I -B scripts/probe_r3.py <repo> <scratch> head` still passes.
  - For (b): a reading of the four places, plus the manager's acceptance recorded on the issue.

### RESIDUE

- **RS1 Docs: two new test-ID labels in rewritten source comments (owner comment rule).**
  - **Where:** `sw/firmware/ctrl/test/test_plat_boot.cpp:73` ("whose completion aecp_reboot_due waits for (B12)") and `:991` ("and aecp_reboot_due waits for those (B12)"). Both lines are new in this delta. The REVIEW READY says "The comment lines this round rewrote name the tests, not bench labels", but these two still carry the label.
  - **Exact fix:** in both places, replace `(B12)` with `(TheResetWaitsForTheResponseToLeave)`, which is how the rewritten header list keys the other tests.
  - The older `(B18)` at `:179` and `(B12)` at `:203` are not part of this delta and are tracked by #746.
- **RS2 Docs: "in the pass that takes the REBOOT" reads as covering all five channels.**
  - **Where:** `docs/design/REBOOT_RESET.md:309` ("a frame on each of the ADP, ACMP, AECP, MAAP and SRP channels left in its ring after the SUCCESS, in the pass that takes the REBOOT, and while its SUCCESS cannot be handed over") and `sw/firmware/ctrl/plat/README.md:127` (the same, in parentheses).
  - **What B22 covers:** a MAAP, an SRP and a second AECP frame only. ADP and ACMP are serviced before AECP in a pass (`ctrl_loop.c:146-150`), so in that pass their frames are taken before the SUCCESS exists, which is correct. Read as "after the SUCCESS", the sentence is vacuously true for those two channels. So this is wording only: the tests and the code are right.
  - **Exact fix for `REBOOT_RESET.md:309`:** "a frame on each of the ADP, ACMP, AECP, MAAP and SRP channels left in its ring after the SUCCESS and while its SUCCESS cannot be handed over, and a MAAP, an SRP and a second AECP frame queued with the REBOOT left in their rings in the pass that takes it".
  - **Exact fix for `README.md:127`:** "a frame on each of the five channels left in its ring from the SUCCESS and while its SUCCESS cannot be handed over, and the MAAP, SRP and AECP frames queued with the REBOOT left in the pass that takes it".
- **RS3 Docs (PR body): the item-1 evidence row still describes round 2's B19.**
  - **Where:** the PR's acceptance table, row "1 Parity: from the SUCCESS no received frame of any channel is taken". It still reads "host B19 (an ENTITY_DISCOVER, a BIND_RX and an AEM command after the SUCCESS ...)".
  - **Exact fix:** "host B19 (an ENTITY_DISCOVER, a BIND_RX, an AEM command, a MAAP PROBE and an MSRP PDU after the SUCCESS: each channel's `RX_TAIL` checked by name, nothing applied or answered), B22 and B23; defects `plat-reboot-takes-frames-after-the-success`, the five `plat-reboot-takes-<channel>-frames-after-the-success` and `plat-reboot-accepted-at-the-handover`".
- **Retained RESIDUE (R822-2 R2, not taken by the ruling):** "From the loop's last pass ... and ADP's poll until the port fires" is still at `REBOOT_RESET.md:290` and `plat/README.md:88`. R822-2's exact fix still applies.

### Suggestions (do not affect coverage)

- **S7 Tests.** B22's AECP words ("no AECP frame queued behind the REBOOT is taken") are required by no defect. Adding them to the `also` of `plat-reboot-takes-aecp-frames-after-the-success`, which opens both AECP layers, would pin them.
- **S8 Docs.** The rewritten header list keys B19 to B23 by name without their `B` prefix, while B11 to B18 in the same list still lead with it. One style throughout would help a reader searching for a test name.
- **Retained from R821-2, untouched by this delta:**
  - S1: `run.py` grades only the BIND_RX's arrival in the window;
  - S2: no CPU-simulation control for a frame after the port;
  - S3: `quiet-without-the-face-poll` escapes;
  - S4: the 0-tie export decision, which is still pending with the manager;
  - S5: B20 does not check that the held frame is an ENTITY_DEPARTING;
  - S6: why `aecp_reboot_accepted` takes no re-entry guard.

## Prior findings, resolved or retained at this head

I read these only after my own pass over the diff.

| Finding | State at 6171d654 | Evidence |
|---|---|---|
| **R821-2 F1** (= R822-2's ruling pair), the parity tests do not prove "any channel" or "from the SUCCESS" | **Resolved at its cause** | (1) B19 (`test_plat_boot.cpp:915-945`) sends a frame on each of the five channels and checks each channel's `RX_TAIL` by name. (2) B22 (`:1025-1051`) covers frames queued with the REBOOT in its own pass, and B23 (`:1054-1078`) covers frames that arrive while AECP's ring is full. (3) `test_aecp.cpp:1842` checks acceptance before any poll. (4) Defects: five per-channel gate defects, `plat-reboot-accepted-at-the-handover`, and AECP `reboot-accepted-only-at-the-handover`. My R821-2 probes, run unchanged (script sha256 equal to R821-2's manifest): `head` platboot1 rc 0; `gate-skips-maap-and-srp` rc 1 on the B19, B22 and B23 MAAP/SRP words; `gate-from-the-handover` rc 1 on the B22 and B23 words; AECP `head` rc 0; AECP `handover` rc 1 on "accepted at its SUCCESS, before any poll hands its frames over". My new probe `gate-one-pass-late` (acceptance latched at the end of the previous step) fails B22 on the MAAP and SRP words. So "from the SUCCESS's own pass" is pinned. |
| R822-2 F1, MAAP/SRP gate and wait | **Resolved** | B19 covers the MAAP and SRP channels. B21 holds the ACMP, MAAP and SRP rings in turn. `plat-reboot-departs-past-the-{acmp,maap,srp}-ring` are each caught on their own words (author `round3/campaigns/platmut4.log`: 23 of 23; the earlier `platmut3.log` shows one escape that was fixed before the head). I did not run R822-2's script. The author's receipt `round3/probes/r822.rc` is 0 and its log reports rc 1 for both probes. |
| R822-2 R1, labels in comments | **Resolved** for `:61, :65, :68, :170`. The rewrite added two new `(B12)` labels, recorded as RS1. | `test_plat_boot.cpp:61-80`, `:181-184` |
| R822-2 R2, ADP-poll wording | **Retained** (not taken by the ruling) | `REBOOT_RESET.md:290`, `plat/README.md:88` |
| R822-2 S1, gate start point | **Resolved** (B22) | probes `gate-from-the-handover` and `gate-one-pass-late` |
| R822-2 S2, stale INDEX | Not rechecked by size. `author-r3/receipts/INDEX.md` lists 182 `round3/` entries and the tree holds 182 such files. | `receipts/manifest-verify.txt` |
| R822-2 S3 / R821-2 S1, S4, and R821-2 S2 to S6 | Retained; the delta does not touch their artifacts | see Suggestions |
| R821-1 and R822-1 findings | Unchanged since R821-2 (resolved there). This delta changes none of the code they depend on. | R821-2 report |

## Lens results (this round, at 6171d654)

```text
[R821] PASS Conformance — git diff --name-only d08d30c6ec..6171d654 (six test/doc files; ctrl_plat.c, aecp.c, aecp_commands.c byte-identical); ctrl_plat.c:175-196,352-388 and aecp.c:195-208,402-406,635-642 re-read against protocol-processor 06_aecp_engine.md 6.11 and the round 3 ruling — no behaviour change, so the R821-2 conformance result (gate from the SUCCESS on every bound channel, loop stopped once the REBOOT's frames are out, DEPARTING last, port after ADP's ring) stands; ruling items 1 and 3 evidenced (probes above); item 2's behaviour holds for AECP by three layers (probe aecp-transmits-after-the-departing: AECP still silent), its evidence gap is F1 under Tests/Docs; issue acceptance 2-5 met, item 1 partial as ruled
[R821] PASS RTL — no HDL or firmware source in the delta; the test-only HAL overrides test_plat_boot.cpp:181-198 (busy_ch, aecp_full) read against mbx_hal_read32's contract and drained() (ctrl_plat.c:199-203): 16-bit tail/head compare, busy = head-1, full = head-TX_WORDS, both reset in SetUp (:262-263); ctrl_loop.c:143-150 service order by channel index is what B22 relies on
[R821] PASS Robustness — B21 per ring (test_plat_boot.cpp:992-1020) and B23 full AECP ring (:1054-1078) exercise the held-ring and backpressure paths the R821-2 Robustness result relied on by reading: the gate stays closed while the SUCCESS cannot be handed over and the REBOOT completes once the ring has room; REBOOT_RESET.md:295-298 still states the unbounded wait on a held ring; reload() between B21's channels restores a fresh boot
[R821] MINOR Tests — test_plat_boot.cpp:976-983, plat_mutants.py:254-258 — F1 (B20's AECP check has no stimulus and no defect; receipts/probe-r3-all.log)
[R821] MINOR Docs — PR round 3 ruling rows, REBOOT_RESET.md:309 — F1 (items 2 and 4 recorded as met per channel); RS1-RS3 RESIDUE; every other changed doc line checked: counts 62 platform / 22 REBOOT (imported reboot_mutants: 22 distinct), AECP 153 / 14 REBOOT (imported DEFECTS), control campaign 592 = 583 + 9, B11 to B23 present, MAAP PROBE layout against IEEE 1722-2016 B.2 and MSRP PDU against 802.1Q-2018 35.2.2 as the helpers' comments state
```

## Reviewer-owned ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | delta file list; ctrl_plat.c, aecp.c unchanged; 06_aecp_engine.md 6.11; round 3 ruling; probes | R821-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |
| RTL | CLEAN | no HDL/firmware in delta; test HAL overrides vs `drained()`; ctrl_loop.c service order | R821-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |
| Robustness | CLEAN | B21 per ring, B23 full ring, REBOOT_RESET.md section 8 bound | R821-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |
| Tests | UNCLEAN (F1) | test_plat_boot.cpp B19-B23, test_aecp.cpp:1842, plat_mutants.py:225-310, aecp_mutants.py:826-845; author campaigns; my probes | R821-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |
| Docs | UNCLEAN (F1); RS1-RS3 RESIDUE | REBOOT_RESET.md:262-309, plat/README.md:88,127-133, test header comments, plat_mutants.py docstrings, PR body, REVIEW READY | R821-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |

## What I executed

Everything ran in disposable copies under the packet's `scratch/`. The review clone was used read-only as the source root.

- **Archive check.** `scripts/verify_manifest.py` (R821-2's, unchanged) on archive `5f043cf8`, subtree `author-r3/`: 866 entries, 866 tree files, 0 mismatches, 0 unlisted, 20 path-redacted (`receipts/manifest-verify.txt`). I spot-read these round 3 receipts:
  - `campaigns/platmut3.log` (22 of 23, one escape);
  - `campaigns/platmut4.log` (23 of 23);
  - `campaigns/aecpmut3.log` (14 REBOOT, all caught);
  - `gates/lane/aecp_mutants.log`;
  - `gates/lane/{fw_selftest,aecp_mutants,reboot,diffcheck}.rc` (all 0);
  - `gates/lane/reboot.log` ("12 of 12", "ctrl_reboot: PASS (0 finding(s))");
  - `probes/final.txt` (the probe clone at the head, 0 changes).
  - `fw_selftest.log` is listed by digest only (`LARGE.tsv`). Its 592 count rests on the receipt's rc and the PR.
- **R821-2 probes, unchanged** (sha256 equal to R821-2's MANIFEST): `probe_plat.py all`, plus `probe_aecp.py head` and `probe_aecp.py handover` (`receipts/probe-r2-*.log`).
- **New probes** (`scripts/probe_r3.py`, `receipts/probe-r3-all.log`):
  - `head`: rc 0, B1 to B23 OK;
  - `gate-one-pass-late`: rc 1, B22 MAAP/SRP words;
  - `aecp-transmits-after-the-departing`: rc 1, but B20's AECP words pass (F1).
- **Hosted checks.** A read-only snapshot at 2026-11-11T23:10Z shows no check runs, statuses or workflow runs for the head (`receipts/hosted-checks-snapshot.txt`). There is no hosted evidence at this head yet. It is not acceptance evidence either way; the manager owns it.
- **Restore check (`receipts/restore-check.txt`).** HEAD and tree are exact. The worktree equals the index, and the index equals HEAD (write-tree `3db1feb1`). The index modes and blobs equal the HEAD tree listing. All six gitlinks are at their recorded commits, with `external` uninitialised as at the start. My probes' child processes left two ignored `__pycache__/` directories (`avdecc/`, `sw/litex/platforms/`), created during this session. I removed them, and none remain.

## Real limits

- I did not run the full firmware self-test, the AECP mutant campaign, the platform campaign, the `ctrl_reboot` CPU simulation or the docs gates myself. They rest on the author's archived receipts, which I verified against the manifest and spot-read.
- I did not run R822-2's probe script.
- Physical calibration was NOT RUN, and field skips are not hardware proof. No hardware was used.
- No manager source bank ran at this head, and I claim none.

## Pending manager duties

- Rule on F1's option (a) or (b).
- Carry RS1 to RS3 and the retained R822-2 R2 to the residue checklist.
- Decide R821 S4 (the 0 tie).
- Hosted and act acceptance at the exact head.
- Build and validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b`), with builder and native banks, at the merge turn.

R821-3 FINISHED
