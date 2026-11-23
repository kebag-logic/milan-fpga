[R889] POSITIVE - exact head 77a74b2f4e289c5a5a89687e07a6925cfedf6860

Round R889-2, internal independent review of issue #972 / PR #974. This is a delta re-review, round 3.

- Head: `77a74b2f4e289c5a5a89687e07a6925cfedf6860`, tree `83462698a273b938f8cc108da7c6581acda83573`.
- Delta reviewed: `0f508a01..77a74b2f`, nine commits and 25 files. That runs from the head R889-1 and R890-1 reviewed to this head. The full source delta from `dd163e41` was used as context.
- Submodules: the tsn-c-stack gitlink is unchanged at `715589c1`, and so are the other five.
- Open findings: no BLOCKER, MAJOR or MINOR is open. Two RESIDUE items and three SUGGESTIONs are recorded below; none of them affects coverage.
- Prior findings:
  - R889-1-F1 / R890-1-F1 (BMCR ignored), R889-1-F2 / R890-1-F2 (the reset-to-arm window) and R889-1-F3 / R890-1-F3 (comment ID) are resolved at this head.
  - R889-1-S1 is not taken and is kept as a SUGGESTION.

This review is source-head review only:
- It is not a manager source bank, and none is claimed.
- It is not the current-dev merge candidate (live dev `e275d795`).
- It is not hardware proof. Physical calibration was NOT RUN, and the bench criterion is the manager's re-run after merge.

## Context reconstructed

- **Contract:** AGENTS.md and CONTRIBUTING.md.
- **Issue #972 acceptance, frozen:**
  - (a) the boot forms the link once;
  - (b) no datapath transmission before the firmware publishes the link;
  - (c) bench discovery time;
  - (d) host or boot-simulation coverage of the restart and no-restart paths, with plants;
  - (e) #840's link-speed behaviour unchanged.
- **The manager's scope decision on #972** (issuecomment-7083292610):
  - Split builds: the effective link is unqualified from reset until the firmware's verified publication, on a reload that kept the link and on the boot-refusal paths too.
  - This is an RTL change: fit and timing at both shapes, and an integration check from reset with the link retained and a planted premature qualification.
  - Builds without firmware PHY management keep reset-up, and are named as such.
  - #840: the no-restart path is taken only with BMCR autonegotiation enabled AND registers 4 and 9 holding the advertisement. A forced lower-speed PHY is renegotiated and never published up.
- **Authorities:** IEEE 802.3 22.2.4.1 (0.15 reset, 0.12 AN enable, 0.10 isolate, 0.9 restart, forced speed and duplex 22.2.4.1.4) and 28.2.4.1.3.
- **Author's handoff:** the [A820] REVIEW READY (issuecomment-7093468235) and the author-r3 packet at `f6dd644d`.

## Packet verification

`receipts/packet-verify.txt`, script `scripts/verify_packet.py`:
- All 238 `author-r3/` files match `review-evidence/972-r1/MANIFEST.json`'s `published_sha256`.
- 230 of 231 `receipts/INDEX.md` hashes match. The one that differs is `gates/d9e1d728/builder-leg-1.txt`, which the manifest marks `path_redacted`. INDEX records its `original_sha256` (c72c30cb…), so the difference is the documented redaction, not tampering.
- Exact-head receipts carry `HEAD 77a74b2f dirty 0`:
  - the firmware gate's four shards: 75 suite verdicts PASS in shard 0, `mutants: 837 of 837 caught` in shard 1, `test_ctrl_firmware: PASS` and `END rc=0` in each shard;
  - `linkreset` and its plants;
  - the split boot simulation;
  - docs steps, lint, Yosys and xvlog.
- Other receipts ran at earlier heads. Twin and `fw_coverage` ran at `d9e1d728`; images and CPU legs at `fc7504f1`; routes at `93d9eaaf`. `git diff-tree` per commit confirms that later commits touch only test code, the leg, READMEs and comments. `git diff 93d9eaaf..HEAD -- sw/litex hdl sw/firmware/ctrl/plat` is comment and README text only, so those receipts stand for this head's code.
- Hosted contexts at this head (`receipts/hosted-checks.txt`, read 06:50Z): every check run was still `queued`, so none had executed. This review makes no hosted claim; the manager owns hosted and act acceptance.

## Independent probes (this round)

`scripts/linkreset_probe.sh`; receipts `receipts/linkreset-*.txt` and `receipts/probe-refused-planted-*.txt`.

**Tool.** The scoped Verilator 5.050 was verified as `Verilator 5.050 2026-07-01 rev v5.050`.

**Rebuild.** I rebuilt both `linkreset` models at this head (`make build-linkreset-1x1 build-linkreset-8x8`). The word's reset was taken from `sw/litex/mac_link_status.py`: 12.

**Arms at head.** All four arms ran concurrently and all four PASS:

| Shape | published (publication at 1,500 ms) | refused |
|---|---|---|
| 1x1/1if | 0 frames before; first frame 0x88f7 at 1500.032 ms; effective link first up 1500.0003 ms; LINK_CTRL[0] and guard 1 throughout; 10 checks, 0 failures | 0 frames in 1,600 ms; effective link never up |
| 8x8/1if | identical figures | identical |

These match the author's `linkreset/run.txt`.

**Falsification probe.** The refused arm was rerun with the planted link-up word (13) at each shape. The author's plant covers only the published arm. Both shapes FAIL (rc 1):
- a Pdelay_Req at 1200.069 ms;
- "no frame crosses the MAC boundary before the firmware's publication" got=1;
- the effective-link and `o_ctl_link_up` checks fail as well.

So the refused arm can also fail for the defect it claims to detect.

**Restore.** The four generated paths were removed afterwards. `receipts/clone-integrity.txt` records:
- HEAD and tree are the exact head;
- `git write-tree` equals the head tree;
- no worktree or index diff, and 0 untracked or ignored entries;
- all six gitlinks are as pinned, and every submodule worktree is clean.

**Not rerun.** I did not rerun the firmware gate. P22/P23 and the five BMCR plants rest on the exact-head shard receipts and on `tests/regression-at-0f508a01.txt`: this head's suites against `0f508a01`'s `ctrl_plat_phy.c`, where P22 fails 27 checks and P23 13 and nothing else fails.

## Prior findings, resolved or retained

**R889-1-F1 / R890-1-F1 (BMCR ignored): RESOLVED.**
- `ctrl_plat_phy.c:122-126` `negotiating()` requires 0.12 set with 0.15 and 0.10 clear.
- The boot's and a loss's skip (`:257-258`) now also requires `negotiating(phy->control)`. So a forced (0x2100, 0x0000, 0x0140), isolated (0x1400) or resetting (0x9000) PHY is restarted whatever 4 and 9 hold. The restart write (`:165-166`) sets 0.12 and 0.9 and clears 0.15 and 0.10.
- CONTROL (`:209-210`): on a PHY the advertisement is for, BMCR not negotiating is link down and `renegotiate()`. So a forced mode is never published up, a lost restart included. A 10/100 PHY (`ADV_NONE`) keeps the release's forced words (`:211-214`).
- I traced the loss path. `publish()` (`:139-146`) may overwrite `RENEGOTIATE` with `OWED` when an up link is published down, but the next poll still restarts, because the skip's `negotiating()` term fails on the forced BMCR.
- The X1 and X2 scenarios of R889-1 (4/9 held, BMCR 0x2100 or 0x1400) are P22's first case and P22 case 3 (`test_plat_phy.cpp:952-993`). The no-loss forced and isolate cases are in P23 (`:995-1050`).
- P19 still proves BMCR 0x1000 with 4 and 9 held is not restarted.
- Five plants (`plat_mutants.py:598-616`) are each caught, per `tests/phy-plants.txt` (28, 12, 3, 26 and 3 checks failed). `plat-phy-outcome-uncounted` gains a P23 kill.

**R889-1-F2 / R890-1-F2 (reset-to-arm window): RESOLVED as the manager decided.**
- `milan_soc.py:2024-2047`: `link_up` resets to `mac_link_status.link_up_reset(fw_link_owner)`, where `fw_link_owner = ctrl_mailbox and hasattr(self.phy, "mdio")` (`:3930` passes `fw_link_owner=ctrl_mailbox`).
- The decision's named consumers are behind that word. `milan_datapath.sv:3407` `eff_link_w = i_link_up & cfg_sw_link & (cfg_linkg_dis | linkg_est_w)` feeds:
  - the gPTP port enable (`:9269`);
  - `o_ctl_link_up`, the mailbox LINK level (`:10221`);
  - the AVB_INTERFACE counters (`:4089-4115`, `ctr_link_q_r` resets 0).
  - `cnt_link_w` (`:3417`) is also gated by `i_link_up`.
  - The split prunes `KL_maap`.
- The milan_soc wiring is evidenced by:
  - `gateware/milanmac-reset.txt`: elaborated, mdio True, reset 12 owner / 13 not;
  - `gateware/link-status-exports.txt`: split exports `4'd12`, all-fabric `4'd13`, for both the initial value and the sys-reset assignment;
  - `gateware/routed-link-status.txt`: `4'd12` in all six routed images.
- `vivado/SUMMARY.txt`: all six routes meet #818's floor. The worst corner is 8x8 ExtraTimingOpt, WNS +0.059 ns and WHS +0.036 ns.
- The integration leg (`sim_link_reset.cpp`) runs at both shapes, from reset with retained PHY clocks and the MultiReg two-flop crossing modelled, with the firmware's own `ctrl_plat_csr.c` boot steps. My probe reproduced it.

**R889-1-F3 / R890-1-F3 (comment ID): RESOLVED.** `adp_first_mutants.py:40` reads `# #970: a LINK_UP delay narrowed ...`.

**R889-1-S1 (fixed-seed spread checks): RETAINED as SUGGESTION.** It is not taken (author's open risk 4), and it does not affect coverage.

## Findings at this head

### R889-2-R1 - RESIDUE - Docs, Tests - `tb/verilator/milan_dp/Makefile:915` - the leg's comment states the publication at 200 ms

- **Evidence.** The comment reads "Each shape runs published (the firmware's publication at 200 ms)". The recipe uses `LINKRESET_PUBLISH_MS = 1500` (`:937`), as the README and the receipts do. The 1,500 ms value is required: it lies after the plane's 1,200 ms boot cadence, which is what lets the plant be caught.
- **Why RESIDUE.** It is comment wording. It changes no recipe, figure or verdict.
- **Exact fix.** `# retained. Each shape runs published (the firmware's publication at LINKRESET_PUBLISH_MS, 1,500 ms)`.

### R889-2-R2 - RESIDUE - Docs - `tb/verilator/ctrl_split_boot/README.md:108` - a review round named in durable documentation

- **Evidence.** The line reads "At `0f508a01`, round 2's #972 head, the boot reached ready in ...". The owner's comment rule targets source comments, so this is borderline. It is recorded so the durable README does not carry review-round provenance.
- **Why RESIDUE.** It is wording only. The figures stand.
- **Exact fix.** "At `0f508a01`, an earlier #972 head, the boot reached ready in 27.978 and 67.228 ms; at `dd163e41`, before #972, in 27.952 and 67.223 ms."

### R889-2-S1 - SUGGESTION - Tests - `sw/litex/milan_soc.py:2031`, `:3930` - no regression gate holds the SoC's owner selection

- **Evidence.** All three test paths read the helper `mac_link_status.py` directly with `fw_link_owner=True`:
  - the `linkreset` leg (Makefile `LINKRESET_WORD`);
  - the host suites (`plat_arms.split_link_reset`);
  - the boot simulation (`boot_soc.py:77`).

  None of them elaborates `milan_soc.MilanMAC`. Two edits would therefore re-open #972 with every gate green:
  - dropping `fw_link_owner=ctrl_mailbox` at `:3930`;
  - a PHY wrapper without an `mdio` attribute.

  The wiring is evidenced today only by the one-off receipts `gateware/milanmac-reset.txt` and the routed images.
- **Suggestion.** Add a small LiteX elaboration check that asserts `link_status`'s reset per placement: 12 for split with MDIO, 13 for all-fabric. `sw/litex/test_retained_cdc_storage.py:218` already constructs `MilanMAC` this way. The check could also plant the call-site defect.

### R889-2-S2 - SUGGESTION - Tests - `tb/verilator/milan_dp/Makefile` `linkreset`, `linkreset-plants` - the leg is outside the hosted inventory

- The leg runs by name only (author's open risk 2, the README's `ORDINARY_CASES` note). Both shapes take about 3.5 minutes for four arms here.
- The manager may want it joined once a hosted timing figure exists, so that the decision's integration check keeps running after merge.

### R889-2-S3 - SUGGESTION - Tests - `tb/verilator/milan_dp/linkreset_plants.py:58-61` - plant the refused arm too

- The plant runs only the published arm. This round's probe shows the refused arm also fails under the planted reset (`receipts/probe-refused-planted-*.txt`).
- Adding the refused arm to the plant would record that sensitivity in the tree rather than in this report.

## Lens results (head `77a74b2f`)

[R889] PASS Conformance — `ctrl_plat_phy.c:122-135,203-218,251-260,307-312`; `milan_soc.py:2024-2047,3930`; `mac_link_status.py:30-48`; `gateware/*.txt`; `linkreset/run.txt` and this round's rerun — checked against #972 (a), (b), (d) and (e) and the [A10] decision's three bullets:
- (a) the held boot is still not restarted: P19; plant `plat-phy-boot-restarts-whatever-held` caught.
- (b) the effective link is unqualified from reset in split builds, at both shapes, on a retained-link reload and on an identity-refused boot. Reset-up is kept and named for all-fabric and no-MDIO builds.
- (e) BMCR per 22.2.4.1: a forced, isolated or resetting PHY is restarted and never published up.
- (c), the bench, is not run and is the manager's after merge.
- The author keeps the `LINK_CTRL[0]` and guard resets and holds the link down by the word alone. I read the decision's "This means" list as the factors of the effective link, whose AND is what must be unqualified, and the leg proves that this AND stays low. The interpretation is published as the author's open risk 1. Manager confirmation is listed below.

[R889] PASS RTL — `milan_soc.py:2024-2063` (CSRStorage reset, MultiReg crossings); `milan_datapath.sv:3375-3417,4089-4115,9269,10221`; `link-status-exports.txt`, `routed-link-status.txt`, `vivado/SUMMARY.txt` — checked:
- The only gateware change is a CSR field reset, a constant, with no new logic, CDC path or width change. The storage initial value and the sys-reset assignment are both `4'd12` in the split and `4'd13` in all-fabric.
- The MultiReg flops start at 0, consistent with the split's 0.
- The consumers are unchanged, and the split builds no `KL_maap`.
- Timing: six routes meet #818's floor, routed at `93d9eaaf`; no gateware changes after it.
- Yosys, lint (89 of 89), 511 behaviour scenarios and xvlog PASS at this head (`gates/77a74b2f/*`).

[R889] PASS Robustness — `ctrl_plat_phy.c:155-170,203-218,257-260,297-312`; `sim_link_reset.cpp:216-310` — checked:
- BMCR unacknowledged: falls through to link down, as before.
- BMCR all-ones: not negotiating, restarted with reset cleared.
- A PHY that keeps reverting to forced: published down every poll, restart every other poll, count saturating at 0xffff.
- A lost restart: published down and restarted next poll (P23).
- A loss with a forced BMCR (P22).
- A 10/100 PHY untouched.
- A CPU-only reset: the arm republishes link down (P20).
- An identity-refused boot never qualifies the link (Phy.B11, the leg's refused arm).
- A reload with the link retained (the leg).
- The 8x8/1if rom sits at exactly 139,264 of its 139,264 B. It is inside its ledger with zero headroom, which is a limit, not a defect.

[R889] PASS Tests — `test_plat_phy.cpp:903-1050` (P20-P23); `test_plat_boot.cpp` L2/L4/B11 restatements; `plat_mutants.py:598-616`; `plat_arms.py:85-92`; `sim_link_reset.cpp`, `linkreset_plants.py`; receipts `tests/phy-plants.txt`, `tests/regression-at-0f508a01.txt`, `firmware-gate-shard{0..3}.txt`, `split-boot.txt` — checked:
- P22 and P23 fail at `0f508a01`'s PHY code (27 and 13 checks) and pass here.
- Five new plants are each caught by named checks; campaign 837 of 837.
- The host fixtures start from the helper's reset, and P20 asserts it is link down.
- The leg can fail: the author's plant is caught at both shapes, and this round's refused-arm plant is caught too.
- The boot simulation is PASS at both shapes, with 7 of 7 plants.
- CPU-budget harness images are byte-identical to round 2, and all 63 probes are equal.
- R1 is RESIDUE; S1-S3 are suggestions.

[R889] PASS Docs — `ctrl_plat_phy.h:6-13,49-93`; `sw/firmware/ctrl/plat/README.md:103-110`; `docs/reference/REGISTER_MAP.md:519-536,4528` with `scripts/register_descriptions.json`; `docs/design/CSR_REGISTER_NOTES.md:164,196`; `docs/reference/FR_NFR.md:217-220`; `CHANGELOG.md`; `tb/verilator/milan_dp/README.md` (the #972 section); `tb/verilator/ctrl_split_boot/README.md`; `mac_link_status.py` docstring — checked:
- These state the split's link-down reset, `0x0000000C` against all-fabric `0x0000000D`, the BMCR rule and the leg.
- The "#840 unchanged" claim was removed and replaced by the tightened rule.
- "Fabric MAAP" was corrected for the split.
- Docs steps: 104 of 104 at this head.
- New source comments in the delta carry no review IDs, lane labels or comment IDs (grep of added lines). `B11`, `L2` and `L4` are the suites' own test IDs.
- R1 and R2 are RESIDUE.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #972 acceptance and the [A10] decision; `ctrl_plat_phy.c` (BMCR rule); `milan_soc.py` and `mac_link_status.py` (reset); gateware receipts; `linkreset` rerun | R889-2 | `77a74b2f4e289c5a5a89687e07a6925cfedf6860` |
| RTL | CLEAN | `milan_soc.py:2024-2063`; `milan_datapath.sv` `eff_link_w` and its consumers; exports and routed `4'd12`/`4'd13`; six routes against #818; Yosys, lint, xvlog | R889-2 | `77a74b2f4e289c5a5a89687e07a6925cfedf6860` |
| Robustness | CLEAN | `ctrl_plat_phy.c` state machine (forced, isolate, reset, lost restart, loss, unacknowledged, 10/100); refused and retained-link leg arms; image ledger | R889-2 | `77a74b2f4e289c5a5a89687e07a6925cfedf6860` |
| Tests | CLEAN | P20-P23, L2/L4/B11, five BMCR plants, the regression at `0f508a01`; `linkreset` and its plants; refused-arm plant probe; firmware gate shards; boot simulation; CPU rows | R889-2 | `77a74b2f4e289c5a5a89687e07a6925cfedf6860` |
| Docs | CLEAN (R1, R2 RESIDUE) | `ctrl_plat_phy.h`, plat README, REGISTER_MAP and descriptions JSON, CSR_REGISTER_NOTES, FR_NFR 2.1.1, CHANGELOG, both tb READMEs, helper docstring | R889-2 | `77a74b2f4e289c5a5a89687e07a6925cfedf6860` |

## Real limits

- **The firmware gate, twin, `fw_coverage`, image ledger, CPU legs, routes and builder legs were not rerun.** They rest on the author's signed receipts. Their heads are named above, and nothing later in their scope changed except comments and test code.
- **The leg has no receive stimulus.** It proves silence from reset with nothing arriving. A transmit provoked by inbound traffic before publication is not exercised. Untouched code keeps its prior verdict.
- **Hosted contexts were all queued and none executed at review time.** No hosted claim is made.
- **No hardware.** Physical calibration and the bench discovery-time criterion (c) were NOT RUN. Field skips are not hardware proof.
- **No concurrent report read.** No other reviewer's report for this round was read.

## Pending manager duties

- **Interpretation of the decision.** Confirm on #972 that the [A10] decision is met by the word's reset alone, with `LINK_CTRL[0]` and the guard keeping their resets (author's open risk 1). This review reads it as met.
- **Hosted inventory.** Decide whether the `linkreset` leg joins the hosted inventory (S2).
- **Rom headroom.** Note that the 8x8/1if rom has 0 B of headroom (author's open risk 3). The next firmware growth at that point needs a ledger decision.
- **Merge turn.**
  - Build and validate the current-dev merge candidate (builder and native banks), and record hosted and act acceptance at the exact head.
  - Run the bench after merge against FR_NFR 2.1.1 at 1x1/1if and 8x8/1if.
  - Carry R1 and R2 to the residue checklist.
  - Handle the tsn-c-stack PR #36 separately; the parent pin is unchanged.

R889-2 FINISHED
