[R720] NEGATIVE - exact head d27a1654285614ded5093cb58f58bceed551fdae

# R720-1 external independent review: FPGA-gPTP PR #92 (issues #89, #90, #91)

- Head `d27a1654285614ded5093cb58f58bceed551fdae`, tree `24e09cd91fa7280c67eed2d15d70dd63fe73aaaa`; base main `55680bff`.
- Scope: issue bodies #89/#90/#91, the assignments (issue #90 comment 6434675577 with its #89 scope addition, issue #89 comment 6434676256), PR #92 body, `git diff 55680bff..d27a1654` and its five commits, and the published author evidence at milan-fpga `21fb280b` `review-evidence/gptp90-r1` (117 blobs, each verified against its git blob id).
- No earlier public review findings exist on PR #92. The PR carries only the two "review started" notices. No PR reviews or line comments exist, so nothing needs resolving or retaining.
- Verdict: one open MINOR (F1), so the verdict is NEGATIVE. Everything else the assignment asks for holds at this head and was re-executed here (see the checklist).

## Findings

### F1: MINOR. Sync receipt aging ignores gmPresent when the elected grandmaster has priority1 255
- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `hdl/ucode/gen_gptp_ucode.py:2112-2132` (`prog_leg_srto`): it ages whenever the role is `ROLE_SLAVE_C`, meaning a peer is elected and the port is asCapable.
  - `hdl/ucode/gen_gptp_ucode.py:1780-1786` (adoption starts the 375 ms watch for any new grandmaster).
  - `hdl/ucode/gen_gptp_ucode.py:1041-1047` (the aged mark then drops every Announce).
  - The claim in the file header `:10-13` and the PR body: "exactly as on announce receipt timeout … && gmPresent".
- **Authority:**
  - 802.1AS-2011 10.3.11, Figure 10-13 as corrected by Cor1: CURRENT goes to AGED on `currentTime >= syncReceiptTimeoutTime && gmPresent`. The assignment's check (1) is worded the same way: "on sync receipt timeout with gmPresent".
  - gmPresent is the per-time-aware-system global of 802.1AS-2011 10.2.3. PortRoleSelection's updtRolesTree() (10.3.12) sets it TRUE only when the grandmaster's priority1 is below 255.
  - The microcode uses "a peer is elected" (`FL_PRESENT_C`) in place of gmPresent. That is wider than the standard's term when the elected grandmaster is not grandmaster-capable.
- **Evidence (executed):**
  - A reviewer-only observation phase was planted at the end of the engine suite's priority1-255 pass. It was not committed (`scripts/p255_probe.py`, receipts `receipts/p255-probe-head.log`, `receipts/p255-probe-base.log`).
  - The setup: this plane is master, and one usable pair clears any earlier mark. A better peer then announces every second for 6 s and never sends Sync. Its grandmaster has priority1 255, so gmPresent is FALSE.
  - **At base `55680bff`:** the plane elects that peer and stays its slave throughout (`flags=5`, gm `0x…0101`).
  - **At head:** it elects the peer (`flags=5`), then ages it within one second (`flags=e`, grandmaster thisClock). It then drops every later Announce for the rest of the 6 s, because the aged mark clears only on a usable Sync pair, which such a domain need not send.
  - Both runs: 53/53 of the pass's own checks and rc 0. No existing check covers this case.
- **Impact:**
  - This applies to a supported configuration: the `--p1 255` (not grandmaster-capable) image, which the suite's fourth pass builds.
  - Facing a better non-grandmaster-capable peer that sends no Sync, the plane leaves the role the standard keeps it in. It then publishes itself as a synchronised master (bits 1 and 3) and ignores the better root's Announces indefinitely. The result is a lasting BMCA disagreement on the link.
  - Base did not do this. The new rule's clause claim ("exactly … && gmPresent") is inaccurate for this input.
  - The shipping priority1 248 image cannot elect such a peer, because priority1 is the first compared field. The default build is therefore unaffected.
- **Required outcome:** one of the following.
  - (a) Gate the Sync-receipt aging on the elected grandmaster's priority1 being below 255. For example, test `S_BESTPV[63:56] != 255` before `BECOME` in `prog_leg_srto`, or do not start the adoption watch for such a grandmaster. Add a named check in the priority1-255 pass with a planted mutant that fails it, regenerate the four images through the generator, and keep the ROM inside budget.
  - (b) Record an owner or manager scope decision that a grandmaster with priority1 255 is out of scope for #89. Then correct the generator header, `docs/INTEGRATION.md` "Departure of the elected peer" and the PR body: they must say that gmPresent is taken as "a peer is elected" and that this deviates for priority1-255 grandmasters.
- **Verification:**
  - Rerun `scripts/p255_probe.py` against the fixed tree, or the new named check. The plane must stay slave of the priority1-255 peer for at least 3 s without Sync.
  - The full engine suite and mutation arm must stay green.

### F2: RESIDUE. Pronoun now binds to the wrong bullet
- **Lenses:** Docs.
- **Where:** `docs/TEST_DEVELOPER.md:118-128`. Nine bullets were inserted between "Keeps it through a receipt timeout queued behind mastership." (line 118) and "Clears it on every handover to a peer." (line 128). The "it" on line 128 now follows "Resets an exchange answered by duplicate responses." instead of "Publishes sync-ok in every master cycle."
- **Authority/evidence:** `git diff 55680bff..d27a1654 -- docs/TEST_DEVELOPER.md`. At base the two "it" bullets were adjacent, lines 118-119.
- **Impact:** wording only. No measurement, test, code or claim changes.
- **Required outcome (exact fix):** move the nine inserted bullets so they follow "- Clears it on every handover to a peer.", or change line 128 to "- Clears sync-ok on every handover to a peer."
- **Verification:** `make docs` rc 0 and a read of the list.

### F3: SUGGESTION. No test separates a second response from a different responder that sends its own Follow_Up
- **Lenses:** Tests.
- **Where:** `hdl/ucode/gen_gptp_ucode.py:1259-1272` (the reset applies "from any responder"); `docs/INTEGRATION.md` "That reset also counts one, from either responder".
- **Evidence:**
  - By inspection, the arm sums every matching response regardless of its source, so the behaviour is correct.
  - The harness's two-identity shape (`PD_DUAL`) sends only the first responder's Follow_Up. Under that shape, a regression to "the last responder owns the pairing" would also lose the exchange.
  - A reviewer mutant restricting the reset to same-source responses (probe R6) could not be planted: the generator refused the image for lack of ROM space.
- **Suggestion:** add a shape where the second responder also sends its own Follow_Up, and check that no exchange completes.

## Assignment checklist at this head

1. **#89.**
   - Slot 4 expiry with role slave (a peer is elected, the port is asCapable) branches to `BECOME` (`gen_gptp_ucode.py:2125-2131`). The watch is `SYNC_RTO_MS_C = 375` (3 × 125 ms).
   - Usable pairs restart it in both roles (`prog_leg_srwatch`), and adoption starts it.
   - The aged mark (`S_SRTO`, scratch 46) suppresses Announces until a usable pair or an asCapable rise clears it. The only asCapable setter clears it, so no reset can carry a stale mark into a live port.
   - Recovery happens on the first usable pair heard as master, and the peer is re-elected once.
   - Phase 12, the end-of-run phase 39 and the adapted phases prove takeover timing, the three unusable shapes, holding for 3 s without re-election, recovery, 250 ms Sync and a 60 ms Follow_Up.
   - Reviewer probes R1 (rise keeps the mark), R2 (pair keeps the mark), R3 (no mark recorded), R7 (wrong role tested) and R8 (slave pair does not restart the watch) are all caught.
   - **Exception:** the gmPresent term (F1).
2. **#90.**
   - `S_PDLOST = (S_PDLOST + 1) & (S_PDGOT − 1)` and the clear at `LOST_CLEARS_AT_C = 5` implement Figure 11-8 RESET with allowedLostResponses 3. Losses 1-4 keep asCapable and the 5th clears it.
   - Phase 25 covers no response, no Follow_Up, a duplicated response and three responses.
   - `S_PDGOT` takes only the values 0 and 1, because every writer writes 0, 1 or `S_PDSTEP`.
   - Recovery: the clear writes `S_PDOK = 0`, so `ASCAP_UP_C = 2` good exchanges re-earn asCapable (Milan v1.2 4.2.6.2.4). Probe R9 (ladder kept) is caught, and so is R4 (count not restarted).
   - Probe R5 (init leaves `S_PDGOT` unset) survives. It is an equivalent mutant: it only adds one count to the boot request while asCapable is already false.
3. **#91.**
   - `S_RSPSEQ += seq | RSP_ARMED_C`. A second matching response pushes the cell to at least `2 * RSP_ARMED_C`, which no Follow_Up can match, and keeps it nonzero, so no later response re-arms.
   - The interval then counts as lost at the next beat, and the next request still waits for the 1 s beat (Cor2).
   - A response after completion or freezing still reaches only the 4.2.6.2.5 bookkeeping.
   - Controls "a second response re-arms the pairing" and "a third response re-arms the reset exchange" are caught.
4. **Mutation arm.**
   - Re-executed here in parallel through the tree's own `run_mutant()`: control pass, and 91/91 caught, each through every check it names (`receipts/mutants-author/summary.tsv`). Base had 72 controls.
   - Each of the 106 new or changed checks maps to failing mutants in the author coverage map. My static extraction (`receipts/new-check-names.txt`) finds no new check outside the map. Its 12 "NONE" rows are artefacts of my template expansion, not real check names.
   - All four images regenerate byte-identically from the generator with each consumer's own arguments, at both head and base (`receipts/regen-images-*.log`).
   - Shipping usage is 1,018 of 1,024 words and seeded images use 1,019. `FUTO@190`. These match `docs/MANAGER.md`.
5. **Parent companion patch.**
   - sha256 `1651cb5a2919e98cefd00aca19460227f57b7fabd3fae0b891495a5954eecdcb`.
   - It touches only `docs/testing/TESTING.md`, two `gptp_plane` test files and two `milan_dp` test harnesses. It contains no RTL, generator or gitlink change.
   - Every hunk changes an expectation of the retired behaviour: fourth→fifth loss, Sync aging, and keeping the selected peer fed with Sync. The exception is the drop-counter arm, which now holds dispatch with a held Pdelay_Resp instead of a stale Sync handler; its assertions are unchanged.
   - Executed here on a scratch milan-fpga `97aab1d0` with the gptp-processor tree at this head:
     - `milan_dp gptp` without the patch: rc 2, 167/185. The failing check set is identical to the author's receipt.
     - `milan_dp gptp` with the patch: rc 0, 185/185.
     - `milan_dp gptp-lat` with the patch: rc 0, 185/185.
   - The remaining consumer gates (`milan_dp_gptp`, `gptp_plane`, gm_steps and the rest) rest on author receipts. See the limits.
6. **No top-level change.** `git diff --stat` touches no `.sv`, Makefile or port list. Only internal scratch words 45/46 are new, and no top-level port, parameter or register map changes.

Other executed gates at head (pinned Verilator 5.050, wrapper sha256 `905795b9…`):
- Engine suite: 1,799/1,799 in each of the three image passes and 53/53 in the priority1-255 pass, rc 0.
- `make contract`, `make docs` and `make lint`: rc 0.
- The clone is byte-identical to the head after all probes (`receipts/clone-integrity.txt`). The repository has no submodule gitlinks.

## Ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | 802.1AS-2011 10.3.11/Fig 10-13, 11.2.15.3/Fig 11-8 with Cor1/Cor2; generator legs SRTO, SRWATCH, RX Sync/Follow_Up/Announce, BTCA adoption, PDREQ loss count, PDRESP arm, PDPOST verdict; p1-255 probe | R720-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| RTL | CLEAN | No HDL delta; µCPU CMP is an unsigned 32-bit compare (`KL_gptp_ucpu.sv:197-205`), so the role gates are exact; scratch 45/46 collision-free; ROM packing; four images regenerated byte-identical; lint | R720-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| Robustness | UNCLEAN (F1) | Aged-mark lifecycle over warm reset and asCapable lapse, master-role Sync intake (scratch/timer aliasing), PDGOT 0/1 invariant, RSPSEQ sum bounds, cease/resume interplay, queued-expiry paths | R720-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| Tests | UNCLEAN (F1; F3 suggestion) | sim_main.cpp phases 12/12b/15/18d/19-21/25/27/39 and slew phases; mutants.py named-verdict logic; 91 author controls re-run; 9 reviewer probes; parent companion legs | R720-1 | d27a1654285614ded5093cb58f58bceed551fdae |
| Docs | UNCLEAN (F1 claim; F2 residue) | HDL_DEVELOPER, INTEGRATION, MANAGER (ROM figures verified), SOURCE_EVIDENCE (L964 anchor verified), TEST_DEVELOPER, generator header/comments (comment rule: no lane, round, reviewer or comment IDs added), PR body | R720-1 | d27a1654285614ded5093cb58f58bceed551fdae |

## Real limits

- The normative texts of 802.1AS-2011, Cor1, Cor2 and Milan v1.2 were not available to me in this session.
  - Clause content is reconstructed from the issue and assignment text and from my knowledge of the standard.
  - The Cor1 change to Figure 10-4 (a master takes Sync, so an aged port sees recovery) is the author's reading. It is consistent with the assignment's automatic-recovery requirement, but I did not check it against the corrigendum text.
  - F1's subclause numbers for gmPresent (10.2.3, 10.3.12) are cited from memory. Its substance (gmPresent FALSE when the grandmaster's priority1 is 255) is the standard's definition.
- No physical calibration or hardware was run. Simulation only.
- Parent consumer gates other than the `milan_dp gptp` and `gptp-lat` legs were not re-executed, because full parent banks are out of my mandate. These are `milan_dp_gptp` (~85 min), `gptp_plane`, gm_steps, the builder and the idiom/lint gates. Their status rests on author receipts: base 15/15; head 12/15 without the patch; with the patch, gptp_plane, milan_dp_gptp and both milan_dp legs rc 0.
- The coverage claim that each unnamed new check has a failing mutant rests on the author coverage map. I re-verified the named checks only.
- The author's head-extras receipt shows `scripts/check_gptp_docs.py --with-submodule` rc 1. It reports only donor deep-link pins naming `55680bff`, which every gitlink bump must update.
- The repository has no hosted CI workflow. The exact-head commit status is "pending" with zero contexts, so no hosted evidence exists.

## Pending manager duties

- Merge-turn current-dev candidate on live dev `97aab1d0…`, with builder and native banks, plus the parent consumer list including the `milan_dp` `gptp`/`gptp-lat` legs.
- The parent companion change (sha256 `1651cb5a…`) and the donor deep-link pin updates for `check_gptp_docs.py --with-submodule` at the gitlink bump.
- Hosted/act acceptance.
- Carry F2 to the residue checklist.
- Issues #89/#90/#91 stay open until the parent companion lands, as the PR body states.

## Receipts

Listed in `MANIFEST.sha256`:
- `receipts/` holds engine run, mutation arms, reviewer probes, image regeneration, parent legs, the p1-255 probe, clone integrity and quick gates.
- `scripts/` holds the parallel mutation driver, reviewer probes, image regeneration, check-name extraction and the p1-255 probe planter.

R720-1 FINISHED
