[R719] NEGATIVE - exact head d27a1654285614ded5093cb58f58bceed551fdae

# R719-1 independent review: FPGA-gPTP PR #92 (issues #89, #90, #91)

- Repository: Mister-M-alt/FPGA-gPTP. PR #92, head `d27a1654285614ded5093cb58f58bceed551fdae`, tree `24e09cd91fa7280c67eed2d15d70dd63fe73aaaa`, base main `55680bff3b287b9a7b0c759f51471fa617c17335`.
- Role: internal independent reviewer, cleared context, round R719-1. Lenses: Conformance, RTL, Robustness, Tests, Docs.
- Authorities: IEEE 802.1AS-2011 with Cor1 and Cor2 (10.3.11 and Figure 10-13; Figure 10-4; 10.6.3.1; 11.2.15.3 and Figure 11-8; 11.5.3), Milan v1.2 Table 4.2 and 4.2.6.2.4/4.2.6.2.5. Scope: issue bodies #89, #90 and #91, assignments issuecomment-6434675577 (#90/#91), issuecomment-6434676256 (#89), the scope additions issuecomment-6434679304 and issuecomment-6434679552.
- No AGENTS.md or CONTRIBUTING.md exists in this repository at head. The process inputs were README.md, docs/README.md (truth order: RTL and generated microcode, then executable tests, then guides) and docs/TEST_DEVELOPER.md ("prove the test fails after mutation").

## Verdict

NEGATIVE. The three receipt rules are implemented through the generator, and the shipped tests and mutants do what the PR says. The issues' named acceptance tests all pass, and each named plant is caught. My probes found two reachable paths where the aged state of #89 is lost while the plane is master. In both, the aged grandmaster is re-elected on an Announce that 802.1AS-2011 10.3.11 ages at once. The plane then takes mastership back 375 ms later. These are F1 and F2, both MINOR. The parent companion patch leaves two parent documents stating retired counts and a stale scenario figure (F3, MINOR). One wording defect is recorded as RESIDUE (R1).

## Findings

### F1 - MINOR - A sync receipt timeout that expires while master is forgotten, so a lone recovered pair re-opens election indefinitely

- Lenses: Conformance, RTL, Robustness, Tests.
- Location: `hdl/ucode/gen_gptp_ucode.py:2112-2132` (`prog_leg_srto`). It stores the role it finds in `S_SRTO`, and only `ROLE_SLAVE_C` (5) is an aged mark. An expiry in the master role stores `ROLE_MASTER_C` (6), which `prog_rx_announce` (`:1045-1047`) treats as not aged.
  - `prog_leg_srwatch` (`:1015-1030`) arms timer slot 4 in the master role too, on every pair heard as master. So once a pair has been heard, the next expiry always happens as master.
  - Documented at `:18-25` ("The first usable pair re-opens election, and the peer's next Announce is adopted once") and `docs/INTEGRATION.md:603-613`.
- Authority: 802.1AS-2011 10.3.11, Figure 10-13 as corrected by Cor1. With `infoIs == Received`, CURRENT goes to AGED whenever `currentTime >= syncReceiptTimeoutTime && gmPresent`. Only a received Sync moves syncReceiptTimeoutTime (Figure 10-4, Cor1, which the PR itself cites).
  - So a superior Announce that arrives after syncReceiptTimeoutTime has passed is recorded and aged at once. It does not elect, whatever role the port held when the time passed.
  - Assignment #89 item 3: "An aged port must not oscillate while Sync recovers".
- Evidence: disposable probe `scripts/probe_reaging.sh` at head, receipt `receipts/runs/probe-reaging-head.log`. The probe starts from a slave of grandmaster GMS with usable Sync (phase 39's end state). Each round then runs:
  1. Sync stops, so the port ages and the plane is master.
  2. One usable pair is heard as master.
  3. Sync is dead again.
  4. GMS announces 624 ms after that pair, which is 249 ms after the port's sync receipt time has passed.
  - In 3 of 3 rounds, that Announce elected GMS (`elected_by_announce=1`, gm commit 0.3 ms after the Announce). The plane took mastership back 374.3-374.9 ms later (`grandmaster changes=2`).
  - Each sporadic usable pair therefore costs two grandmaster changes. Each change arms the parent's Annex B.1.1 holdover. A grandmaster whose Sync is mostly unusable makes the plane flap at the Announce rate. Under the clause it would stay master.
  - The control round (Announce 124 ms after the pair, inside the watch) re-elects, as the clause also does.
- Impact: grandmaster flapping with a partially broken grandmaster Sync. That is the oscillation #89 rules out, and a deviation from 10.3.11 timing. No test covers "one pair, then Sync dies again before the next Announce". The suite passes with the defect.
- Required outcome: an Announce received while the port's sync receipt time has passed (gmPresent) does not elect, whatever role the expiry found. For example, an expiry on an asCapable master that has heard a pair also leaves the aged mark. Automatic recovery on the first usable pair must stay as it is.
  - Add a named harness check for the probe's scenario, and a planted mutant (the role-only mark as at this head) that fails it.
- Verification: rerun `scripts/probe_reaging.sh <tree> <workdir>`. Each late-announce round reports `elected_by_announce=0 commits_naming_gm=0`, and the control round still re-elects. The engine suite and its mutation arm pass, with the new control caught by its named check.

### F2 - MINOR - BECOME leaves a parked Sync without its 125 ms Follow_Up watch, so a late Follow_Up clears the aged mark

- Lenses: Conformance, RTL, Robustness, Tests.
- Location: `hdl/ucode/gen_gptp_ucode.py:1860-1862` (`prog_become`) disarms timer slots 2, 4 and 5 but does not void `S_SYNCTS`. `prog_rx_followup` (`:888-892`) relies on the Follow_Up receipt timeout to zero `S_SYNCTS` ("a Follow_Up later than 125 ms pairs with nothing").
  - Since #89, a master pairs at `:910-913` and runs SRWATCH, which clears the mark (`:1028`). Before #89 a master never paired, so the stale `S_SYNCTS` was harmless.
- Authority: Milan v1.2 Table 4.2, followUpReceiptTimeout 125 ms, and the 802.1AS-2011 MDSyncReceive Follow_Up receipt timeout. A Follow_Up after that time is not usable. The PR body and `docs/INTEGRATION.md:603-605` state the same: "A port aged by Sync stays aged until usable Sync".
- Evidence: second probe in `scripts/probe_reaging.sh`, receipt `receipts/runs/probe-reaging-head.log`, line `PROBE parked`.
  - A Sync arrived 339 ms after the last usable pair, with no Follow_Up yet. The sync receipt timeout made the plane master 35.4 ms later. That Sync's Follow_Up arrived 200 ms after the Sync, beyond 125 ms.
  - It was paired as master, cleared the mark, and the next Announce elected the aged grandmaster (`elected_by_next_announce=1 commits_naming_gm=1`).
- Impact: a grandmaster whose Follow_Ups run late (more than 125 ms, with no Sync in between) can be re-elected on each such takeover, and the plane flaps. It also contradicts the PR's "not usable" definition.
- Required outcome: the master-role pairing never consumes a Sync whose Follow_Up watch has lapsed or was disarmed by BECOME. For example, BECOME voids `S_SYNCTS`, or keeps slot 5 running. Add a named check with a failing planted mutant.
- Verification: rerun the probe and expect `elected_by_next_announce=0 commits_naming_gm=0`. The engine suite and mutation arm pass.

### F3 - MINOR - The parent companion patch leaves parent docs stating the retired counts and a stale scenario figure

- Lens: Docs.
- Location: the companion patch `author/receipts/parent-companion-test.patch` (sha256 `1651cb5a2919e98cefd00aca19460227f57b7fabd3fae0b891495a5954eecdcb`, verified) applied to milan-fpga dev `97aab1d0`.
  - It renames the phc_step checks to "fifth unanswered request after a crossing exchange" and "fourth unanswered request after an unanswered crossing request". Parent `docs/design/GPTP_PLANE.md:130` and `:134` at `97aab1d0` still say "The fourth unanswered request after it clears asCapable" and "The third unanswered request after it clears asCapable". They describe that same regression.
  - It edits parent `docs/testing/TESTING.md:186`. The next line, `:187`, still says "16.992496440 simulated seconds over 849624822 cycles". The patched run at head records `simulated_duration_seconds=17.992742740 cycles=899637137` (`author/receipts/parent-companion-at-head/02-milan_dp_gptp.log:775`).
  - The public handoff says of the parent gPTP docs "Nothing in them is wrong about this change's behavior", which `GPTP_PLANE.md:130,134` contradicts.
- Authority: assignment #90 item 4 (docs and requirement rows). The parent docs truth order puts executable tests above guides, so after the bump these lines would contradict the tests.
- Impact: once the gitlink bump lands, the parent design doc and testing doc state counts and a measurement that are false. These are figures and behaviour claims, not wording only.
- Required outcome: the companion change, or the bump's recorded follow-up list, updates `GPTP_PLANE.md:130` to the fifth, `:134` to the fourth, and `TESTING.md:187` to the figure the patched run measures.
- Verification: the amended patch applies to `97aab1d0`, `scripts/docs_check.py` returns 0, and a text check of the three lines matches the patched run's log.

### R1 - RESIDUE - Dangling pronoun in the engine suite list

- Lens: Docs (wording only).
- Location: `docs/TEST_DEVELOPER.md:128`. Nine bullets were inserted at `:119-127` between "Keeps it through a receipt timeout queued behind mastership." (`:118`, "it" = sync-ok) and "Clears it on every handover to a peer." (`:128`). That "it" now follows "Resets an exchange answered by duplicate responses."
- Exact fix: change `:128` to "- Clears sync-ok on every handover to a peer.", or move the nine new bullets below `:128`.

### Suggestions (no effect on the verdict)

- S1 (Conformance): gmPresent approximation. Ageing keys on "a peer is elected" (`ROLE_SLAVE_C`), which is the engine's published gmPresent (#82). With a priority1 255 image that elects a priority1 255 peer, 802.1AS-2011 gmPresent is FALSE and no sync receipt ageing applies. The author recorded this as out of scope, and I concur; file an issue.
- S2 (Conformance): Figure 11-8 WAITING_FOR_PDELAY_RESP also goes to RESET on a Pdelay_Resp with a wrong sequenceId or another port's requestingPortIdentity. The engine ignores such a response. This is outside #91, and the author recorded it; file an issue.
- S3 (Robustness): a reflected own-clock Sync/Follow_Up would count as usable Sync while master. The author recorded this. Consider the IEEE 1588-2008 9.5.2.2 own-port filter on Sync receipt when F1/F2 are fixed.

## Check-by-check (manager items 1-6)

1. **#89.**
   - Timer slot 4 now reaches BECOME from SRTO in the slave role (`gen_gptp_ucode.py:2126-2131`). The watch is `SYNC_RTO_MS_C = 375`, which is 3 x 125 ms (10.6.3.1; Milan v1.2 Table 4.2), restarted by every usable pair (`:1015-1029`) and by adoption (`:1780-1786`).
   - Takeover timing is checked in phases 12 and 39 against [375 ms - 1 ms, 375 ms + 2 ms] from the last usable pair. That passes for all four shapes and for the never-usable grandmaster.
   - Automatic recovery on the first usable pair: yes. Resets: publish flags clear at reset (`hdl/top/KL_gptp_engine.sv:823-833`), the only mark reader runs behind the asCapable gate (`gen:1040` before `:1045`), and the asCapable rise clears the mark (`:2087-2089`). So no reset leaves a stale mark.
   - Oscillation: not met in two reachable cases, F1 and F2.
2. **#90.**
   - `S_PDLOST = (S_PDLOST + 1) & (S_PDGOT - 1)`, cleared at `LOST_CLEARS_AT_C = LOST_N_C + 2 = 5` (`:1637-1647`). `S_PDGOT` holds only 0 or 1: its writers are init (1), request (0), PDEPOCH (`S_PDSTEP` = 1), the verdict (1) and RESUME (1).
   - Init now sets `S_PDGOT`, so the boot request is never judged.
   - Phase 25 checks one loss kept, four kept and the fifth cleared, for no response and no Follow_Up. Recovery runs through the unchanged two-exchange ladder (Milan 4.2.6.2.4) at the start of each shape.
   - Met.
3. **#91.**
   - `S_RSPSEQ += sequenceId | RSP_ARMED_C` (`:1269-1272`). A second matching response leaves `S_RSPSEQ >= 0x20000`, which no Follow_Up's `seq | 0x10000` can equal, so a third response cannot re-arm. The request leg then counts the interval as lost.
   - Phase 25 covers duplicated and triple responses: one loss kept, four kept, fifth cleared, and no exchange completes (published delay unchanged).
   - Met.
4. **Mutants and images.** My parallel run of the tree's own mutation arm (same staging, generator, build and harness functions, shipping and priority1 255 passes) gave: clean control pass, 91 of 91 controls caught.
   - All 108 new or changed checks are failed by at least one control: the 104 names absent at base, plus four changed same-name checks. No control breaks the tree's named-check rule (`receipts/kill_map.json`).
   - Issue-required controls (`receipts/issue_required_controls.txt`), each caught by named checks:
     - "a sync receipt timeout only clears sync-ok" (105 FAIL lines);
     - "lost responses clear asCapable at the fourth";
     - "a second response re-arms the pairing";
     - "a third response re-arms the reset exchange".
   - Regenerating the four tracked images with the head generator and each Makefile's arguments is byte-identical (`receipts/regen_images.txt`): 1,018 of 1,024 words.
   - Met for the shipped checks. F1 and F2 add checks that do not yet exist.
5. **Parent companion patch.** The sha256 matches. It applies cleanly to `97aab1d0`.
   - Its test hunks change expectations of the retired behaviour: the fifth loss instead of the fourth, mastership at the 375 ms Sync timeout, and Sync pairs keeping an Announce-elected peer alive.
   - The full-queue drop arm changes its stimulus, not its expectations. A held Pdelay_Resp now blocks dispatch instead of a stale long handler, and the asserted counter properties are unchanged.
   - Author receipts (hash-verified against the published MANIFEST.json) show rc 0 with the patch at the head gitlink for `gptp_plane`, `milan_dp gptp`, `milan_dp gptp-lat`, `milan_dp_gptp` and `docs_check`.
   - I reran the cheap parent gates on a scratch parent at `97aab1d0`, with the gptp gitlink at `d27a1654` (tree `24e09cd9` verified), without and with the patch. `check_cpp_idiom`, `check_py_idiom`, `measure_naming --check`, `measure_test_evidence --check` and `docs_check` were rc 0 in both states.
   - Docs part: not met (F3).
6. **No top-level change.** The diff touches only `hdl/ucode/gen_gptp_ucode.py`, the four generated images, the engine harness, mutants and docs. There is no `.sv` change, no port, parameter or register-map change, and the ROM size is unchanged. Met.

Comment rule: added source lines name no bench lane label, lane name, review round, reviewer ID or issue-comment ID. The one "manager's ruling on #68" phrase is a re-flow of an existing comment. No RESIDUE.

## Lens evidence

- **Conformance.** Clause walk of `prog_leg_srto`, `prog_rx_announce`, `prog_rx_sync`, `prog_rx_followup`, `prog_leg_srwatch`, `prog_btca`, `prog_become`, `_tmr_pdelay_request`, `_pdresp_arm_the_pairing` and `_pdpost_verdict` against 10.3.11/Figure 10-13, Figure 10-4, 11.2.15.3/Figure 11-8 and Milan Table 4.2. Behavioural probes for F1 and F2.
- **RTL.**
  - Microcode branch-free role gate (`:880-887`): 5 maps to 0 and 6 to 1, every other role wraps, and RC is preserved to `:912`.
  - New scratch cells 45 and 46 do not collide with the engine's hard-coded cells (25, 41, and the 37/38 validity).
  - `S_SSEQFLY` is no longer aliased.
  - ROM 1,018/1,024. No RTL file changed.
- **Robustness.**
  - Warm and cold reset paths for `S_SRTO`, `S_SYNCSRC`, `S_PDGOT` and `S_RSPSEQ`.
  - The cease countdown freezes `S_PDLOST`, and RESUME re-seeds it.
  - The queued-SRTO-behind-BECOME path (#84) stays covered.
  - F1 and F2 are the open paths.
- **Tests.**
  - Engine suite at head, run by me: 1,799/1,799 in the shipping pass and each seeded pass, 53/53 priority1 255, rc 0 (`receipts/runs/engine-run.log`).
  - microCPU 768/768. Parser 337/337 plus mutants 9/9. tsngen 288/288 plus 4/4.
  - `make contract`, `make lint` and `make docs` rc 0.
  - Mutation arm 91/91 plus clean, and the kill map, as above.
  - Check-name inventory at base 1,412 and at head 1,503 unique names (`receipts/new_check_names.txt`, `receipts/removed_check_names.txt`).
- **Docs.** Diffs to HDL_DEVELOPER, INTEGRATION, MANAGER (1,018 words, `FUTO@190` matches the packer output), SOURCE_EVIDENCE (`#L964` resolves to `prog_leg_slew`, and `check_source_evidence` reports 20 exact) and TEST_DEVELOPER, plus the companion patch's parent docs (F3, R1).

## Prior public review findings

At this head, PR #92 has no submitted reviews and no review comments. Its only comments are review-start notices. There are no prior findings to resolve or retain.

## Hosted evidence

The commit has 0 check runs and no statuses (combined state `pending` with an empty list). No hosted job executed at this head, so none is relied on here.

## Ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `gen_gptp_ucode.py` receipt legs; 802.1AS-2011+Cor1/Cor2 10.3.11, Fig 10-4, Fig 10-13, 11.2.15.3, Fig 11-8, 11.5.3; Milan v1.2 Table 4.2; probe log | R719-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| RTL | UNCLEAN (F1, F2) | microcode diff, the four images (regenerated identical), engine scratch and reset RTL (unchanged), packer output | R719-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| Robustness | UNCLEAN (F1, F2) | reset and warm-reset paths, cease and resume, queued expiry, master pairing, probes | R719-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| Tests | UNCLEAN (F1, F2 uncovered) | `sim_main.cpp` diff, `mutants.py` diff, engine, microCPU, parser, tsngen suites, mutation arm 91/91, kill map 108/108 | R719-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| Docs | UNCLEAN (F3; R1 is residue) | five repository guides, generator docstrings, companion patch, and parent GPTP_PLANE.md/TESTING.md at 97aab1d0 | R719-1 | d27a1654285614ded5093cb58f58bceed551fdae |

## Real limits

- The 802.1AS-2011, Cor1, Cor2 and Milan v1.2 texts were not available locally. Clause readings come from the reviewer's reading of those figures. The PR's Cor1 Figure 10-4 citation (the parent condition struck) was not checked against the text.
- The long parent gates were not re-executed here: `milan_dp gptp`/`gptp-lat`, `milan_dp_gptp`, `gptp_plane`, `gm_steps`, builder, `xvlog`, `gptp_shadow` and `lint_rtl`. Their status rests on the author's hash-verified receipts. Only the cheap parent scripts were rerun.
- My mutation run used the tree's driver functions under a parallel scheduler, over the same two passes the tree's driver runs. The seeded passes ran in the engine suite run.
- No synthesis or OOC run (no vendor tool), no full `make` bank, no hardware. Physical calibration NOT RUN, and field skips are not hardware proof.
- No manager source bank ran at this head. None is claimed or inferred.

## Pending manager duties

- Current-dev merge-candidate validation (builder and native banks) at the merge turn, against live dev `97aab1d0f28bd753a3e11df6278d5cac54f964dd`, with receipts linked on the PR.
- Hosted and act acceptance.
- Landing the parent companion change with the gitlink bump, including the `check_gptp_docs.py --with-submodule` donor-link pins and F3's three lines.
- Carrying R1 to the residue checklist.
- Deciding on issues for S1 and S2.

## Workspace restore

The review clone was never modified. Every build, probe and parent snapshot ran in disposable copies under the packet's `scratch/`. At the end, HEAD is `d27a1654…`, tree `24e09cd9…`, and the index and worktree are clean, with no untracked or ignored files. Every tracked blob and mode matches `git ls-tree -r HEAD` (`receipts/restore_check.txt`). The repository has no submodule gitlinks.

## Receipts

`MANIFEST.sha256` lists every published file. Main items:
- `receipts/runs/` holds gate, suite, mutation and probe logs with rc files. `receipts/runs/RC-NOTES.txt` explains the return codes kept only on the console, and why `mutants-head.rc` is 1 (its own stricter text summary; the tree rule has 0 breaks).
- `receipts/kill_map.json`, `receipts/mutants-head-summary.json` and `receipts/mutants-head-controls.tar.gz` hold the mutation results.
- `receipts/regen_images.txt` holds the image regeneration check.
- `receipts/issues/` and `receipts/pr92.json` hold the public scope snapshots.
- `scripts/` holds `par_mutants.py`, `kill_map.py`, `list_checks.sh` and `probe_reaging.sh`, each taking tree and work directories as arguments.

Host paths in logs are replaced by placeholders.

R719-1 FINISHED
