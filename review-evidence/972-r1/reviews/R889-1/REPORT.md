[R889] NEGATIVE - exact head 0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b

# R889-1: internal cleared-context review of PR #974 (issue #972)

- Head under review: `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b`, tree `4a0fc0a2ee1159adffb276c1c00ef936c51b313f`. Six commits on the flip PR's reviewed head `dd163e41`. Code head is `48c39b5b`.
- Submodule gitlinks are unchanged from `dd163e41`, and the tsn-c-stack gitlink is at its pin `715589c1`. Evidence: `receipts/clone-integrity.txt`, and `git diff dd163e41..HEAD -- third_party` is empty.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
- Verdict: NEGATIVE. Two MINOR findings are open: F1 and F2. There is also one RESIDUE (F3) and one SUGGESTION (S1).

## Reconstruction (public state only)

- Read: AGENTS.md, CONTRIBUTING.md (by reference from AGENTS.md), the #972 body, the executor's TAKEN and REVIEW READY comments, and the #970 ruling (issuecomment-7080789556). Also read: the PR #974 body, the review-start comment, `dd163e41..0f508a01` diff and history, the cited sources (`ctrl_plat_phy.[ch]`, `ctrl_plat.c`, `milan_datapath.sv`, `KL_link_guard.sv`, `milan_csr.sv`, FR_NFR sections 2.1.1 and 3.4.1, `397_SERVICE_BUDGET.md`), and the public packet `review-evidence/972-r1` at `7a5e1e9a`.
- Frozen acceptance of #972:
  - (a) the boot forms its link once, with no restart where the PHY already holds the advertised abilities;
  - (b) the datapath does not transmit before the firmware has published the link;
  - (c) bench criterion: first ENTITY_AVAILABLE within the declared discovery time at 1x1/1if and 8x8/1if (the manager's re-run, after merge);
  - (d) a host test or the boot simulation covers both the restart and no-restart paths, with plants;
  - (e) #840's link-speed behaviour is unchanged.
- Prior public review findings on PR #974: none. The PR carries only the review-start comment and no reviews. The issue carries no review round. Nothing needed resolving or retaining.

## Results against the focus items

1. **Cause: confirmed from the RTL and firmware at this head.**
   - `milan_mac_link_status` resets to 13: link up, 1000 Mb/s, full duplex (`boot_soc.py:73-84` mirrors `milan_soc.py` MilanMAC).
   - `eff_link_w = i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)` (`hdl/milan/milan_datapath.sv:3407`).
   - `LINK_CTRL[0]` (sw_link) resets to 1 (`hdl/common/csr/milan_csr.sv:1613`). `link_est_o = rx_alive_r`, which resets to 1 (`hdl/common/KL_link_guard.sv:166,320`).
   - So the datapath's effective link is up from reset until the firmware's first write.
   - At `dd163e41`, the arm set `adv = OWED | RENEGOTIATE`, so the boot restarted negotiation whatever the PHY held.
2. **Fix: checked.**
   - `ctrl_plat_phy_arm` writes link down right after the MDIO-present check and before its calibration spin and any frame (`sw/firmware/ctrl/plat/ctrl_plat_phy.c:40`). It owes `ADV_OWED` alone (`:41`).
   - The restart is skipped only where registers 4 and 9, as read, are gigabit-only (`:231-234`).
   - GIG_PEER and THE OUTCOME are unchanged (`:249-268`).
   - The PR changes no RTL and no SoC file.
   - However, the no-restart decision reads only registers 4 and 9. It never looks at register 0, so the boot no longer enforces autonegotiation enabled with isolate and reset clear (**F1**).
   - The window before the arm is real at the datapath level (**F2**).
3. **Group G: checked and executed.**
   - The draws are literal: 4,000 / 2,000 / 4,000 / 5,000 ms (`test_adp.cpp:562-567`).
   - Head `adp` arm passes 58 of 58 (`receipts/head-adp.log`).
     - G1: 64 distinct delays, latest 3,990 ms, quarters 17 / 9 / 19 / 19.
     - G2: latest 1,981 ms, halves 18 / 14.
     - G4: latest change-to-frame 3,994 ms.
   - All 8 plants of `adp_first_mutants.py` are caught by their named G (or A9) test and words, through the tree's own `plant()` and `caught()` (`receipts/plants-adp1.log`, `receipts/plants-adp2-walk-unbuilt.log` for the first two lines, `receipts/plants-adp3.log`).
   - The walk-arm kills of the 3 moved plants were not rebuilt here. They are unchanged from the base campaign, and the author's shard receipts report 832 of 832.
   - G4's grandmaster-change delays split 6 / 26 across the two halves. A simulation of the stack's xorshift draw in G4's order shows that split is a fixed-seed outcome at the fair-draw rate (0.00061 against 0.00054), not a biased generator (`receipts/xorshift-pairs.txt`).
4. **FR_NFR 2.1.1: checked term by term.**

   | Term | Bound | Source checked |
   |---|---:|---|
   | Link publication | 250 ms | `397_SERVICE_BUDGET.md` "PHY poll derivation and simulation", lines 3-12; `run.py:110` `PUBLICATION_MS = 250.0`; `CTRL_PLAT_PHY_POLL_US` 125 ms |
   | Link-guard settle | 0 ms added | `KL_link_guard.sv:31,82`: 2,097,152 cycles, 41.94 ms at 50 MHz, inside the 250 ms |
   | LINK event | 30 ms | FR_NFR section 3.4.1: ADP's 30 ms row, line 403 |
   | Draw | 4,000 ms | Milan 5.6.3.5.3, Table 5.50 |
   | Expiry to frame | 30 ms | FR_NFR section 3.4.1, ADP row |
   | Egress | 1 ms | `ctrl_loop.h:467` |

   - The sum, 4,311 ms, is arithmetically correct, and the stated 1,689 ms margin is correct.
   - The 250 ms publication term is more conservative than the ruling's "125 ms ... roughly 4.2 s", and it is cited.
   - The declared time is used in FR_NFR 2.1.1, `MAILBOX_SPLIT.md:536-539` and `test_adp.cpp` (`kDiscoveryMs`).
   - Anchors resolve (`receipts/docs/venv-*gen_toc*`).
5. **Host tests and boot simulation.**
   - `platboot1` and `platboot2` at head pass 55 of 55 each; `platboot1` at base passes 52 of 52 (`receipts/head-platboot1.log`, `head-platboot2.log`, `base-platboot1.log`).
   - P19, P20, P21 and L4 pass in both arms.
   - PHY plants re-planted and caught by their named tests and words: `plat-phy-boot-restarts-whatever-held` (P19, P11), `plat-phy-arm-publishes-nothing` (P20, L4) and `plat-phy-outcome-unchecked` (P18 ×2, P21) (`receipts/plants-phy.log`).
   - Boot simulation:
     - Native controls at head: 6 of 6 as required (`receipts/bootsim-native-controls.log`).
     - Its PHY grade, run on its own stand-in rows (`scripts/grade_arm.py`, `receipts/bootsim-grade-arm.log`), passes the valid run and raises the #972 finding for three defective arms: no arm publication, the arm after the first frame, and the arm publishing link up.
     - The boot simulation exercises the restart path only: its PHY starts at defaults, and the published run shows the boot's `0x1200` write. The no-restart path is the host's (P11, P19, P21). Acceptance (d) allows either.
   - Published author receipts read:
     - firmware shards 0-3 at `48c39b5b`: PASS, 832 of 832 caught;
     - boot simulation at `ba0f80ed`: 1x1 and 8x8 PASS, arm at 2.636 / 4.434 ms, self-test 7 of 7 plants with `phy-arm-unpublished` caught;
     - images: `ctrl_plat_phy.o` alone differs, `ctrl_plat_phy_arm` 176 to 192 B, fixtures identical;
     - CPU harness images: byte-identical sha256;
     - ledger: 45 RAMB36, rom +16 B, PASS.
   - These are the author's receipts. I did not re-run them.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests, Docs - `sw/firmware/ctrl/plat/ctrl_plat_phy.c:231-234` (with `:41`) - the boot's no-restart decision ignores register 0, so a held 4/9 advertisement leaves a forced or isolated PHY as it is

- **Authority/evidence.**
  - Acceptance (e): #840's link-speed behaviour unchanged. The MAC runs at 1 Gb/s only, and a 100 Mb/s link must not be published.
  - The header's THE ADVERTISEMENT says register 0 "enables and restarts autonegotiation with reset and isolate clear (22.2.4.1)". IEEE 802.3 22.2.4.1.4: with autonegotiation disabled, the forced speed bits are in force. 22.2.4.1.6: isolate cuts the PHY off the MII.
  - At `dd163e41` the boot always wrote register 0. At this head, the skip at `:231-234` judges only `phy->local` and `phy->gig` as read. It skips the `ADV_RESTART` stage, the only write of register 0, even though `phy->control` was read at `ADV_CONTROL`.
- **Probe** (`scripts/probe_bmcr.cpp.inc`, appended to `test_plat_phy.cpp` in disposable copies of head and base; `receipts/probe-bmcr-head.log`, `receipts/probe-bmcr-base.log`):
  - X1. Registers 4 and 9 hold 0x0001 / 0x0200; register 0 = 0x2100 (forced 100 Mb/s full duplex); link up.
    - Head publishes word 11 (100 Mb/s full duplex, up), restarts 0, and register 0 stays 0x2100.
    - Base publishes 13 (1000 Mb/s full duplex) after one restart, with register 0 at 0x3100.
  - X2. Register 0 = 0x1400 (isolate set).
    - Head publishes 1000 Mb/s up with isolate still set, restarts 0.
    - Base clears isolate (0x1000) after one restart.
- **Impact.**
  - The datapath sees a published link that carries no traffic: a 100 Mb/s link the MAC is silent on, or an isolated PHY. ADP advertises into it.
  - Nothing recovers it, because no loss occurs. THE OUTCOME never runs on a forced mode, and it cannot see isolate.
  - Precondition: a warm boot, such as a gateware reload or a CPU-only reset, after something left register 0 in that state while 4/9 hold the advertisement. Power-up defaults do not hold 4/9, so they still restart.
  - The same gap already existed after a link loss (#919). That part is pre-existing; this PR extends it to the boot.
  - Neither the header nor the README states that register 0 is not enforced at boot when 4/9 hold. The PR states #840's behaviour is unchanged.
- **Required outcome.** Either of:
  - the boot (and preferably the loss path) restarts, or at least writes register 0, unless register 0 as read already holds autonegotiation enabled with isolate and reset clear; plus a host test of a forced-mode PHY and an isolated PHY holding 4/9, and a plant;
  - or a recorded maintainer decision accepting the corner, with `ctrl_plat_phy.h`, the platform README and the PR stating it.
- **Verification.**
  - X1 and X2 (`scripts/probe_bmcr.cpp.inc`) pass at the fixed head.
  - P11, P19 and P21 still pass: a PHY holding 4/9 with register 0 at 0x1000 is still not restarted.
  - The new plant is caught by its named test.

### F2 - MINOR - Conformance, RTL, Robustness - `ctrl_plat_phy.c:40`; `hdl/common/csr/milan_csr.sv:1613`; `milan_soc.py` MilanMAC `link_status` reset - acceptance (b) is met only from the arm on, and the decision the executor requested is unrecorded

- **Authority/evidence.**
  - #972 acceptance (b): "the datapath does not transmit before the firmware has published the link".
  - `eff_link_w` (`milan_datapath.sv:3407`) is up from reset: `link_status` resets to 13, `LINK_CTRL[0]` resets to 1, and `rx_alive_r` resets to 1. It stays up until the arm's write, 2.636 ms at 1x1 and 4.434 ms at 8x8 (published boot-simulation receipt at `ba0f80ed`).
  - The executor states this as open question 1, "Decision needed" (REVIEW READY, issuecomment-7082983553). No maintainer decision exists on #972 or #974 at review time.
  - The supporting assumption is not established by any artifact in the tree. That assumption is that a power-up's or a REBOOT's PHY has no link in that window.
- **Impact.**
  - A gateware reload that keeps the PHY's link can give the gPTP plane, the fabric MAAP engine and the mailbox LINK level a link for up to 4.4 ms. Section 7's "all acceptance criteria are met" cannot be read off the tree.
  - Per AGENTS.md section 2, a conflict between the issue and the implementation must be decided, not chosen privately.
- **Required outcome.** A recorded maintainer decision on #972. Either:
  - (i) acceptance (b) is restated to "from the firmware's arm", and the residual window is accepted, with its owner named;
  - (ii) or the window is closed, for example by resetting `link_status` link-down or `LINK_CTRL[0]` to 0, in this lane or a stated dependency, with a test that `eff_link` is low from reset to the first publication.
- **Verification.** The decision link. For (ii), the RTL test and the boot simulation's arm figure.

### F3 - RESIDUE - Docs - `sw/firmware/ctrl/test/adp_first_mutants.py:40` - a review finding ID in a source comment

- **Evidence.** The line reads `# #970, R888-1-F1: a LINK_UP delay narrowed to 0 to 0.5 s is not Milan's draw (the ruling on #970)`. It is a new instance in the reviewed delta, and the owner's comment rule (2026-10-15) forbids review rounds and reviewer IDs in source comments.
- **Why RESIDUE.** It is a comment only. It changes no plant, test or verdict.
- **Exact fix.** `    # #970: a LINK_UP delay narrowed to 0 to 0.5 s is not Milan's draw (the ruling on #970)`.

### S1 - SUGGESTION - Tests - `sw/firmware/ctrl/test/test_adp.cpp` (G1/G5 `covers(…, 4u, 8u)`, G2 `covers(…, 2u, 8u)`)

- The spread checks are graded on one fixed seed.
- Under a fair draw, a reseeded run fails "each quarter at least 8 of 64" about 1.7 % of the time, and G2's halves about 0.2 % of the time. G1's second quarter holds 9 at this head.
- An unrelated change to the model's clock skew or entity ID can therefore fail G1 with no defect. Consider stating the fixed seed in the test, or grading the spread with a looser bound or more link-ups.
- This does not affect coverage.

## Per-lens results (head `0f508a01`)

- **Conformance: UNCLEAN** (F1, F2).
  - Examined: #972 acceptance (a)-(e), the #970 ruling, `ctrl_plat_phy.c:28-50,224-268`, IEEE 802.3 22.2.4.1 and 28.2.4.1.3 as cited in `ctrl_plat_phy.h:28-80`, and FR_NFR 2.1.1 against its sources.
  - (a), (d) and FR_NFR are sound. (e) is broken by F1 and (b) is open by F2. (c) is the bench, the manager's.
- **RTL: UNCLEAN** (F2).
  - No RTL or SoC file is in the diff.
  - Examined `milan_datapath.sv:3389-3417` (`eff_link_w`, counters), `KL_link_guard.sv:159-177,320`, `milan_csr.sv:1613,2870` and `boot_soc.py:73-84` for the reset values the firmware's arm relies on.
  - The firmware's write is a full-word CSR write of 0 into a 4-bit field, the same word the probe-miss path already wrote. There is no width or speed-field side effect.
- **Robustness: UNCLEAN** (F1, F2).
  - Examined: warm-boot PHY states (X1, X2), no MDIO (P9), an unacknowledged read at ADV_CONTROL (resume, retried), a held advertisement with a 100 Mb/s negotiation in force (P21), a restart that latches a loss (P19 `restart_drops`), REBOOT re-arming (L2 counters), and the pre-arm reset window.
- **Tests: UNCLEAN** (F1: no test of a held 4/9 advertisement with register 0 forced or isolated).
  - Otherwise the tests are strong: the new P19/P20/P21/L4 and the G1-G4 kills were re-planted here and caught by name (`receipts/plants-*.log`), head and base arms run (`receipts/head-*.log`, `base-platboot1.log`), and the boot-simulation grade was probed (`receipts/bootsim-grade-arm.log`).
- **Docs: UNCLEAN** (F1: register 0's state at a held boot is unstated, and the PR's "#840 unchanged" claim is broken; F3 is RESIDUE).
  - Examined `ctrl_plat_phy.h:28-80,214-217,281-286`, `plat/README.md:105-113,154`, `tb/verilator/ctrl_split_boot/README.md:77-111`, FR_NFR 2.1.1, `MAILBOX_SPLIT.md:533-540`, the CHANGELOG entry and `DOCUMENTATION_AUDIT.md:306`.
  - Docs gates at head, 14 checks: all rc 0. Three ran with the pinned Markdown renderer in a private virtualenv (`receipts/docs/summary.txt`).
  - The comment-rule scan of the delta found only F3.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | `ctrl_plat_phy.c:28-50,224-268`; #972 acceptance; #970 ruling; FR_NFR 2.1.1 with its sources; `receipts/probe-bmcr-*.log` | R889-1 | `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b` |
| RTL | UNCLEAN (F2) | `milan_datapath.sv:3389-3417`; `KL_link_guard.sv:159-177,320`; `milan_csr.sv:1613,2870`; `boot_soc.py:73-84`; no RTL in the diff | R889-1 | `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b` |
| Robustness | UNCLEAN (F1, F2) | X1/X2 probes; P9, P16, P19, P21, L2, L4; the pre-arm window | R889-1 | `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b` |
| Tests | UNCLEAN (F1) | `test_plat_phy.cpp` P9/P11/P19-P21; `test_plat_boot.cpp` L2-L5; `test_adp.cpp` G1-G5; `plat_mutants.py`; `adp_first_mutants.py`; `run.py` `grade_phy` and plants; `receipts/plants-*.log`, `head-*.log`, `bootsim-*.log` | R889-1 | `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b` |
| Docs | UNCLEAN (F1; F3 RESIDUE) | `ctrl_plat_phy.h`; `plat/README.md`; `ctrl_split_boot/README.md`; FR_NFR 2.1.1; `MAILBOX_SPLIT.md`; `CHANGELOG.md`; `DOCUMENTATION_AUDIT.md`; `receipts/docs/` | R889-1 | `0f508a01b5d02fbf192ab08e4d8a5bf514b32a3b` |

## Real limits

- Not run here: the firmware gate's four self-test shards, `fw_coverage`, the twin, the CPU budget legs, `plat_ledger`, the image diff, the builder legs and the full docs workflow. For those I read the author's published receipts at `48c39b5b`, `ba0f80ed` and `0f508a01`. They are not reviewer execution.
- The split boot simulation was not built or run here: there is no product LiteX tree on this host, and Docker is outside this review. Only its native controls, run with no build, and its PHY grade on its stand-in rows were executed.
- The walk-arm kills of the three moved ADP plants were not rebuilt: the copy lacks the processor checkout's pin. Their `adp` G kills were.
- How the base tree was built: the head copy with `git diff dd163e41 HEAD` reverse-applied. lwSRP was used read-only from the clone's submodule.
- No hardware. Physical calibration NOT RUN, and the bench criterion (c) is not evidenced. Field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed.

## Pending manager duties

- A decision on F2. A path for F1: a fix, or a recorded acceptance.
- F3 goes to the residue checklist.
- The current-dev merge candidate's builder and native banks (base `dd163e41`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`), and hosted/act acceptance of the exact head.
- The bench re-run of #970/#972's discovery scenarios at 1x1/1if and 8x8/1if after merge, against FR_NFR 2.1.1's 6.0 s.
- A re-review of the corrected head under every lens a fix touches.

## Receipts

Every file listed in `MANIFEST.sha256` (paths relative to this packet):

- `scripts/run_arm.py`, `scripts/run_plants.py`, `scripts/grade_arm.py`, `scripts/xorshift_pairs.py`, `scripts/probe_bmcr.cpp.inc`
- `receipts/*.log` and `receipts/*.rc`: arms, plants, probes and the boot-simulation checks
- `receipts/docs/*`: docs gate logs and summary
- `receipts/xorshift-pairs.txt`
- `receipts/clone-integrity.txt`: HEAD and tree, index tree `4a0fc0a2…`, a clean status, and gitlinks equal to the head's

R889-1 FINISHED
