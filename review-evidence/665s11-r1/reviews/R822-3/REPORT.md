[R822] NEGATIVE - exact head 6171d65473875239d97e6f6b9327c394db65aab8

# R822-3: external review of PR #881 (issue #871, S11 AECP REBOOT), round 3 delta

- **Head under review:** `6171d65473875239d97e6f6b9327c394db65aab8`, tree `3db1feb17473d462b567347841f7219838d2b893`. The live PR head equals it. It is one commit with one parent, `d08d30c6ec`.
- **Delta (`d08d30c6..6171d654`):** six files. They are the two host test files, the two mutant tables, `docs/design/REBOOT_RESET.md` and `sw/firmware/ctrl/plat/README.md`.
  - No firmware source, HDL or testbench file changed (`receipts/delta-scope.txt`). So there is no firmware behaviour change, as the round 3 ruling (#871 issuecomment-6806697914) requires.
  - `git diff --check 1d6bf555 6171d654` is clean.
- **Inputs, in this order:**
  1. AGENTS.md.
  2. The round 3 ruling.
  3. The full delta, read before any other review.
  4. My own round 2 report and scripts.
  5. The author packet `review-evidence/665s11-r1/author-r3` at `5f043cf8`.
  6. R821-2 (issuecomment-6806677261). I read it only after my verdict and ledger were drafted.
  7. The hosted check-run list at the exact head.
- **Verdict:** NEGATIVE, for one open MINOR (F1) under Tests and Conformance.
  - Most of the ruling is met. Every receive-gate item and every ring-wait item is proved per channel, and both round 2 F1s are resolved at their cause.
  - The open item is B20's AECP line. It asserts "no AECP transmission starts after ENTITY_DEPARTING", but no planted defect reaches it, and the B20 scenario gives AECP nothing to send. The ruling's fourth bullet ("a planted defect per channel, failing by its own words") is therefore unmet for that one channel of its second bullet.

## What I executed (receipts under `receipts/`)

All probes ran on two disposable copies of the head, which are not published. The review clone was never edited.

| Run | Result | Receipt |
|---|---|---|
| My round 2 probes, script byte-identical to R822-2 (`scripts/r822_probes.py`, sha256 `ef03b0c6…`) | `clean`: platboot1, platboot2 and AECP core rc 0. **`gate-skips-maap-and-srp`: rc 1**, failing B19, B22 and B23 on their MAAP and SRP words (at round 2: rc 0). **`depart-ignores-maap-and-srp-rings`: rc 1**, failing B21 on its MAAP and SRP words (at round 2: rc 0). **`accepted-from-the-poll`: platboot1 rc 1** (B22 MAAP and SRP; B23 ADP, ACMP, MAAP and SRP) **and AECP rc 1** ("accepted at its SUCCESS, before any poll hands its frames over"); at round 2 both were rc 0. `no-adp-poll-in-state-2`: rc 1, as at round 2. `quiet-only-after-the-port`: rc 0, as at round 2 (S4, retained) | `probes/r2-rerun/` |
| The head's 22 platform REBOOT defects (`plat-reboot-*`), through `ctrl_mutants.campaign`, with the round 2 script unchanged | 22 of 22 caught on their own words | `campaign-plat.log`, `.rc` |
| The head's 14 AECP REBOOT defects (`reboot-*`), through `aecp_mutants.campaign` after its table-drift control | 14 of 14 caught, including the new `reboot-accepted-only-at-the-handover` | `campaign-aecp.log`, `.rc` |
| New probe `depart-past-the-aecp-ring`: the DEPARTING's wait skips AECP's ring | survives (rc 0). This is consistent with the author's equivalence argument; see "Ruling items" | `probes/r3/` |
| New probe `loop-after-the-departing`: the head's own B20 defect, with every failing check listed | rc 1. B20 fails on its ACMP, MAAP and SRP words, the aggregate line and "no frame but ADP's". **The AECP line never fails** | `probes/r3/loop-after-the-departing--platboot1.log` |
| New probe `aecp-ready-ignores-the-reboot`: AECP's own refusal removed | platboot1 rc 0, because the platform gate alone holds AECP. The AECP core arm is rc 1 ("no command is taken after a REBOOT's SUCCESS"). This confirms the two-layer reading in `channel_gate_mutants`' docstring | `probes/r3/` |
| New probe `adp-restarted-after-the-departing`: ADP is re-enabled straight after its SHUTDOWN | rc 1, caught by `B12 the response has left, so ADP is shut down` | `probes/r3/adp-*` |
| The author packet at `5f043cf8`: 11 round 3 receipts against the archive's `MANIFEST.json` `published_sha256` | 11 of 11 match. `aecp_mutants.log` (head `6171d654`) has 153 `[ok]` lines. `reboot.log` (head `6171d654`) shows 12 of 12 plants and controls caught, PASS. `platmut4.log` shows 23 of 23 caught. `platmut3.log` (rc 1, the accepted-at-the-handover defect escaping B23) is an earlier pass that `platmut4` supersedes | `author-r3-verify.txt` |
| Review clone after all probes | HEAD, tree, `git ls-files -s` digest and submodule status are equal to the baseline, and the worktree is clean | `baseline-*`, `after-*`, `gitlinks-after.txt`, `clone-check.txt` |

Hosted evidence: the exact head has no check runs (the check-runs API returns an empty list). I claim nothing hosted. Hosted and act acceptance belong to the manager.

## Ruling items (issuecomment-6806697914), verified at this head

| Ruling bullet | Status | Evidence |
|---|---|---|
| 1. Every mailbox channel's receive is refused from the SUCCESS onward, each channel named | **MET** | B19 (`test_plat_boot.cpp:915`) puts one frame on each of the five channels: an ENTITY_DISCOVER, a BIND_RX, an AEM command, a MAAP PROBE for the entity's own range (`:358`, byte offsets per IEEE 1722-2016 B.2) and an MSRP PDU (`:369`). It checks each channel's `RX_TAIL` by name. Each of `plat-reboot-takes-{adp,acmp,aecp,maap,srp}-frames-after-the-success` (`plat_mutants.py:286-301`) is caught on that channel's B19 and B23 words (`campaign-plat.log`). AECP's defect opens both layers. My probe `aecp-ready-ignores-the-reboot` confirms that both layers exist |
| 2. No channel but ADP's ENTITY_DEPARTING starts a transmission after ENTITY_DEPARTING | **MET in the assertions, except AECP's proof (F1)** | B20 (`:947`, per-channel loop `:978-983`) checks ACMP, AECP, MAAP and SRP `TX_HEAD` by name. The head's defect reaches ACMP, MAAP and SRP by name, but not AECP (`loop-after-the-departing`). ADP sending anything but the DEPARTING is caught by B12's shutdown check (my ADP probe) |
| 3. Each assertion holds from the SUCCESS's own cycle | **MET** | B22 (`:1025`) queues the REBOOT, a second AEM command, a MAAP PROBE and an MSRP PDU, then runs one pass. MAAP and SRP are serviced after AECP in a pass (`loop/ctrl_loop.c:146-150`, channel order `MBX_CH_*` 0-4), so they fall in the window between acceptance (`aecp.c:405`) and the handover (`aecp.c:639-641`). B23 (`:1054`) holds AECP's transmit ring full, so `reboot == 1`, and checks all five channels. The AECP core test now requires acceptance straight after `aecp_rx` (`test_aecp.cpp:1842`). `plat-reboot-accepted-at-the-handover` and `reboot-accepted-only-at-the-handover` are caught on those words, and so is my round 2 `accepted-from-the-poll` |
| 4. A planted defect per channel, failing by its own words | **MET for bullets 1 and 3 and the ring wait; NOT MET for bullet 2's AECP line (F1)** | Gate: five per-channel defects. Wait: `plat-reboot-departs-past-the-{acmp,maap,srp}-ring` (`plat_mutants.py:304-310`), each caught on its B21 words. B21 (`:992`) holds each of those rings in turn. AECP's ring has no wait defect, and the author's reason is stated at `test_plat_boot.cpp:990-991`, `plat_mutants.py:305-306` and `REBOOT_RESET.md:309`. The reason is sound: `aecp_reboot_due` needs `tx_done` past `reboot_end`, and `tx_done` advances only when `TX_TAIL` passes the frame (`aecp_mbx.c:144-160`). Once due, the loop commits nothing more, so the AECP ring has drained. My `depart-past-the-aecp-ring` survives, as an equivalent mutant should. B20's AECP line has no such statement and no defect: see F1 |

## Prior findings, resolved or retained at this head

| Finding | Status | Evidence |
|---|---|---|
| R822-2 F1 (MINOR, Tests and Docs): MAAP and SRP not exercised by the gate or the wait | **RESOLVED at the cause** | Both of my round 2 verification probes now give platboot1 rc 1 on MAAP and SRP words. The evidence rows now match the tests: `REBOOT_RESET.md:309` and `plat/README.md:127,131,133`, and the counts are checked (62 platform defects, 22 of them REBOOT; 14 AECP REBOOT defects out of 153) |
| R821-2 F1 (MINOR, Tests and Docs): the gate is not proved on all channels, nor from the SUCCESS | **RESOLVED at the cause** | Its probes `gate-skips-maap-and-srp` and `gate-from-the-handover` make the same edits as my `gate-skips-maap-and-srp` and `accepted-from-the-poll`. Both now fail platboot1, and the AECP arm, on REBOOT words. The AECP core check sits before any poll. The author's re-run of R821's scripts is also published (`round3/probes/r821-*`) |
| R822-2 R1 RESIDUE: bench labels in new comments | **Resolved for the six lines named; new instances in this delta: RES1** | The header now names the tests (`test_plat_boot.cpp:61-80`). The `acmp_busy` comment was removed. `:203 (B12)` is pre-existing (#746) |
| R822-2 R2 RESIDUE: when ADP's poll runs, in three documents | **Retained** (not taken under the ruling) | Unchanged at `REBOOT_RESET.md`, `plat/README.md:88` and `ctrl_plat.h:37-38` |
| R822-2 S1: the gate's start point is not pinned | **RESOLVED** | By B22 and B23 and their defects |
| R822-2 S2: the author packet index; no signature | **Retained as a limit** | The archive commit `5f043cf8` and the head are both unsigned (the GitHub verification reason is "unsigned"). I verified the published hashes against `MANIFEST.json` only |
| R822-2 S3 = R821-2 S1: the CPU simulation's window AEM arrival is not graded | **Retained** | `tb/verilator/ctrl_reboot` is not in this delta |
| R822-2 S4: the store service before the port is not pinned | **Retained** | `quiet-only-after-the-port` still survives |
| R821-2 S2, S3, S5, S6, and the S4 decision | **Retained; outside this delta** | No delta file touches them. S4 (a 0 tie versus byte-identical exports) still needs the manager's decision |

## Findings

### F1 MINOR: B20's AECP line is reached by no planted defect

- **Lenses:** Tests, Conformance.
- **Where:**
  - `sw/firmware/ctrl/test/test_plat_boot.cpp:978-983`: the per-channel B20 loop, including `"B20 no AECP transmission starts after ENTITY_DEPARTING"`.
  - `sw/firmware/ctrl/test/plat_mutants.py:254-258`: the `also=` list names ACMP, MAAP and SRP only.
  - The claim, which names AECP: `docs/design/REBOOT_RESET.md:309` and `sw/firmware/ctrl/plat/README.md:127`, both "no ACMP, AECP, MAAP or SRP transmission after ENTITY_DEPARTING".
- **Authority:**
  - The ruling's bullets 2 and 4: "no channel but ADP's ENTITY_DEPARTING starts a transmission after ENTITY_DEPARTING" and "each comes with a planted defect per channel, failing by its own words".
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
- **Evidence (executed):**
  - `loop-after-the-departing` plants the head's own B20 defect, the loop serviced after the DEPARTING. B20 fails on the ACMP, MAAP and SRP words but never on the AECP word (`probes/r3/loop-after-the-departing--platboot1.log`).
  - B20's scenario has no AECP output source after the SUCCESS: no registered controller, and no pending notification or probe. AECP's own rule also refuses such output (`Core` test, defect `reboot-probes-after-its-success`). So no single platform defect can make that line fail.
  - The author handled the same situation for B21's AECP ring by excluding it with a stated, checkable reason. B20 has neither an exclusion nor a defect.
- **Impact:**
  - The AECP channel's "nothing after the DEPARTING" property rests in fact on AECP's core rule, which is tested and planted, and on the gate. The B20 integration line adds no proof for it.
  - The evidence row presents AECP alongside the three channels that are proved at platform level. A reader of section 8 cannot tell which.
  - The code is not in question. The firmware is unchanged and AECP starts nothing after its SUCCESS.
- **Required outcome:** Either of the following:
  - (a) A planted defect is caught on `"B20 no AECP transmission starts after ENTITY_DEPARTING"`. For example, give B20 an AECP output source (a registered controller and a pending unsolicited notification), and plant a defect that opens both layers, as `plat-reboot-takes-aecp-frames-after-the-success` does for the gate. That is, the loop is serviced after the DEPARTING and AECP's no-output-after-SUCCESS guard is off. Add the AECP word to that defect's expected words.
  - (b) The AECP exclusion is stated, with its reason, in the B20 comment, in `plat_mutants.py` beside the B20 defect, and in `REBOOT_RESET.md:309` and `plat/README.md:127`, as is already done for B21. The reason is that AECP starts no frame after its SUCCESS (`aecp.c`, `Core.RebootIsAnswered…`, `reboot-probes-after-its-success`), so no platform defect reaches that line. The ruling's owner then accepts the exclusion against bullet 4.
- **Verification:**
  - For (a): `python3 -B scripts/r822_reboot_campaigns.py <tree-copy> <out> plat` reports the new or extended defect `[ok]` with the AECP B20 word among its expected words. `scripts/r822_r3_probes.py` `loop-after-the-departing`, or the new defect, lists `B20 no AECP transmission starts after ENTITY_DEPARTING` among the failures.
  - For (b): read the four places, and check the ruling owner's acceptance.

### RES1 RESIDUE: bench labels in two new source comments (owner comment rule)

- **Lens:** Docs.
- **Where:**
  - `sw/firmware/ctrl/test/test_plat_boot.cpp:73`: `//       whose completion aecp_reboot_due waits for (B12)`.
  - `sw/firmware/ctrl/test/test_plat_boot.cpp:991`: `// once the loop has stopped, and aecp_reboot_due waits for those (B12)`.
  - Both lines are new in this delta. The round's REVIEW READY says "The comment lines this round rewrote name the tests, not bench labels". These two do not. `:179 (B18)` and `:203 (B12)` are pre-existing (#746).
- **Exact fix:** Replace `(B12)` on both lines with the test's name, `(TheResetWaitsForTheResponseToLeave)`. Equivalently, drop the parenthesis.

### Suggestions (do not affect coverage)

- **S-a (Docs): one phrase in the evidence row reads wider than the in-pass test.**
  - `REBOOT_RESET.md:309` says "a frame on each of the ADP, ACMP, AECP, MAAP and SRP channels left in its ring after the SUCCESS, in the pass that takes the REBOOT, and while its SUCCESS cannot be handed over". `plat/README.md:127` uses a parenthetical form of the same phrase.
  - In the REBOOT's own pass, only AECP, MAAP and SRP come after the acceptance. ADP and ACMP are serviced before AECP (`ctrl_loop.c:146-150`). That is what B22 tests. The sentence is true as a property, but the test's comment at `test_plat_boot.cpp:1022-1024` is more precise.
  - Suggested wording: "...left in its ring after the SUCCESS and while its SUCCESS cannot be handed over, and the AECP, MAAP and SRP frames queued with the REBOOT in the pass that takes it".
- **S-b (Tests): B20's held frame is not checked to be a DEPARTING.** This is R821-2 S5, still applicable. The new per-channel lines do not change it.

## Lens results (this round, at `6171d654`)

```text
[R822] MINOR Conformance — sw/firmware/ctrl/test/test_plat_boot.cpp:978-983, plat_mutants.py:254-258 — F1: ruling bullet 4 unmet for bullet 2's AECP line (every other bullet met: see "Ruling items")
[R822] PASS RTL — receipts/delta-scope.txt (no firmware, HDL or testbench source in d08d30c6..6171d654); ctrl_plat.c:170-203,349-375, aecp.c:195-206,405,639-641, aecp_mbx.c:144-160, ctrl_loop.c:121-161 re-read as the tests' basis — prior RTL verdict at d08d30c6 carried; the delta changes nothing it depends on, and the B21 AECP exclusion's equivalence is confirmed (depart-past-the-aecp-ring survives)
[R822] PASS Robustness — test_plat_boot.cpp:992 (each of the ACMP, MAAP and SRP rings held in turn, with a reboot each), :1025 (same-pass queueing), :1054 (AECP transmit ring full, then room); campaign-plat.log 22/22; probes/r2-rerun; probes/r3 (adp-restarted, aecp-ready-ignores-the-reboot) — held, full and ordering paths per channel
[R822] MINOR Tests — test_plat_boot.cpp:978-983 — F1: the AECP word is unreachable by any planted defect (loop-after-the-departing log); every other new line is reached by its own defect (campaign-plat.log, campaign-aecp.log, probes/r2-rerun/results.json)
[R822] PASS Docs — docs/design/REBOOT_RESET.md:308-309, sw/firmware/ctrl/plat/README.md:127,131,133 against plat_mutants.mutants() (62 in total, 22 REBOOT) and aecp_mutants.DEFECTS (153, of which 14 REBOOT); added comments in test_plat_boot.cpp:61-80,180-184,347-384,907-913,990-991,1022-1024,1052-1053 and plat_mutants.py:262-310 — counts and statements match the tests; RES1 is RESIDUE only; S-a is optional
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | The ruling's four bullets against B19-B23 and `test_aecp.cpp:1842`; protocol-processor 6.11 acceptance at the SUCCESS, via `aecp.c:405,639-641`; `ctrl_loop.c:146-150` | R822-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |
| RTL | CLEAN | `receipts/delta-scope.txt` (no source change); gate, depart and AECP completion re-read; `depart-past-the-aecp-ring` | R822-3 (carried from R822-2 at d08d30c6, whose scope this delta does not touch) | 6171d65473875239d97e6f6b9327c394db65aab8 |
| Robustness | CLEAN | B21 per ring, B22 same pass, B23 full transmit ring; my campaigns and probes | R822-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |
| Tests | UNCLEAN (F1) | `test_plat_boot.cpp` delta; `test_aecp.cpp:1842`; `plat_mutants.py:247-310`; `aecp_mutants.py:829-832`; campaigns 22/22 and 14/14; 9 probes | R822-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |
| Docs | CLEAN (RES1 is RESIDUE; S-a optional) | `REBOOT_RESET.md:308-309`; `plat/README.md:127-133`; the added comments | R822-3 | 6171d65473875239d97e6f6b9327c394db65aab8 |

## Real limits

- **Host tests:** I ran the host `platboot` arm at one interface for each probe, and at one and two interfaces for the clean control. I also ran the AECP core arm (`Core.Reboot*`, app mode, two interfaces). I did not run the full control campaign (592) or the full AECP campaign (153). For those I rely on the author's receipts:
  - `aecp_mutants.log`: 153 `[ok]` lines at `6171d654`, hash-verified.
  - `fw_selftest`: published as rc 0 with a hash in `LARGE.tsv`. The log itself is not in the archive, so its "592 of 592" is unverified by me.
- **CPU simulation:** I did not run the CPU REBOOT simulation (`tb/verilator/ctrl_reboot/run.py`) at this head. No file of it is in the delta. The author's `reboot.log` at `6171d654` (12 of 12, PASS) is hash-verified. No Verilator was used.
- **Signatures:** neither the author packet nor the head carries a cryptographic signature. I verified the archive's `MANIFEST.json` hashes only.
- **Not run:** docs gates and workflow steps. I relied on the author's `round3/gates/docs` receipts, and checked only their presence.
- **Hardware:** physical calibration NOT RUN. Field skips are not hardware proof.
- **Manager validation:** no manager source bank exists at this head, and I claim none.

## Pending manager duties

- Rule on F1's route: (a) a defect that reaches the AECP line, or (b) a stated exclusion, which the ruling's owner accepts.
- Carry RES1 and R822-2 R2 to the residue checklist.
- Decide R821 S4: a 0 tie that changes the all-fabric export, against the port comment.
- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`) with the builder and native banks, and own hosted and act acceptance. The exact head has no hosted check runs.
- File the split boot simulation's unpinned hash seed as a new issue, as the author's open risks note.

R822-3 FINISHED
