[R851] NEGATIVE - exact head afa3ea19d6a1075382c63e4fc1e188a9aadf33bb

Internal cleared-context review R851-1 of issue #919 / PR #933 (`919-phy-link` -> `dev-soft-core`). Tree `406dc4ba57ae0b7e1f06f5e400356872cabc32af`. All five lenses were applied at this head. One MAJOR and three MINOR findings are open, and one RESIDUE is recorded. Every lens is UNCLEAN.

The decisive defect was first published by the external round R852-1 (its F1). This round reproduced it at this head with a probe of its own and retains it as MAJOR. This round's own findings are a test gap in the same restart decision (two surviving mutants, one run through the whole unit gate), and a fit-page statement that the merge kept and that the head's code contradicts.

## Contents

- [Identity, authority and independence](#identity-authority-and-independence)
- [Findings](#findings)
- [Prior public findings: resolved or retained](#prior-public-findings-resolved-or-retained)
- [The focus items, checked against code and receipts](#the-focus-items-checked-against-code-and-receipts)
- [What this round executed](#what-this-round-executed)
- [Reviewer-owned completion ledger](#reviewer-owned-completion-ledger)
- [Limits](#limits)
- [Pending manager duties](#pending-manager-duties)
- [Reproduction and packet](#reproduction-and-packet)

## Identity, authority and independence

- **Head:** `afa3ea19d6a1075382c63e4fc1e188a9aadf33bb`, the isolated detached clone at that head. The submodule gitlinks are gptp-processor `135afd04`, protocol-processor `a9e84b66`, lwSRP `08ee86e8`, tsn-c-stack `715589c1` and verilog-axis `48ff7a7e`. `external` is not initialised.
- **Bases:** original base `659d7687`. Merged base `70f4056f`, through the `--no-ff` merge `8670bfb0` (parents `55769f09`, `70f4056f`). Live dev is `6b66f66d89cf25d2717687bcc2c3bf617685a99a`. These are distinct; this round validates no merge candidate.
- **Order of reading:**
  1. AGENTS.md, CONTRIBUTING.md and docs/README.md.
  2. Issue #919's body, scope addition 6907491954 and ruling 6907583837.
  3. The rehearsal report #665 6899519003 (finding A/12), ruling 6899740728 and the sync STOP 6903515775; #923's ruling 6906679024; #920's 6908928237.
  4. REQ-MAC-03, `docs/reference/REGISTER_MAP.md` MAC_STATUS, `ctrl_loop.h`, and the release's `phy_link_tick` on dev-soft-core and `phy_advertise_gigabit_only` on dev `6b66f66d`.
  5. `git diff 659d7687..afa3ea19`, the lane delta `70f4056f..afa3ea19`, and the history.
  6. The author archive `c129707b` (author-r1, author-r2), REVIEW READY 6929222018, and the PR body.
- **Independence:** no private author material, no lane scratchpad and nothing under the management tree were read. The PR's public comments were fetched after this round's own pass over the diff, its merge replay, mutation probes, image links and coverage probe. They were fetched before this round's verdict and ledger were written down. That ordering deviates from the instruction to write the verdict and ledger first, so it is disclosed here. `INDEPENDENT.txt` and `receipts/independence_timestamps.txt` record what this round held before the fetch: findings F2, F3 and R1, the suggestions, and a NEGATIVE direction, each with an artifact older than the fetch. F1 and F4 entered this round from R852-1 and were checked against the code with this round's own probe and recount.

## Findings

### R851-F1 - MAJOR - Conformance, RTL, Robustness, Tests, Docs - a failed advertisement write is repaired without a restart, so the earlier negotiation stays active (retains R852-F1)

- **Artifacts:**
  - `sw/firmware/ctrl/plat/ctrl_plat_phy.c:223-233`: `ADV_SET_LOCAL` skips the restart once `CTRL_PLAT_PHY_ADV_RESTARTED` is set, and `ADV_RESTART` sets that bit before the read-back verifies.
  - `ctrl_plat_phy.c:234-240`: `ADV_CHECK_GIG` clears the owed state on read-back alone.
  - `sw/firmware/ctrl/test/test_plat_phy.cpp:564-598`, P15 (`:575` "restarts negotiation once, not each poll"): this encodes the behaviour.
  - `sw/firmware/ctrl/plat/ctrl_plat_phy.h:35-36` and `:43-47`, and `sw/firmware/ctrl/plat/README.md:92`: these claim no 100 Mb/s link and a verified advertisement.
- **Authority/evidence:** the scope addition (#919 6907491954) requires the advertisement "written and verified at boot and after every link loss". #840 and the owner's 2026-11-05 decision require 1000BASE-T alone, so that a partner without it gets no link. IEEE 802.3 28.2.4.1.3 ties a changed advertisement to renewed negotiation, so a read-back alone does not make it active.
  - **This round's probe** (`scripts/retry_probe.sh`, `receipts/retry_probe.log`) uses the head's `ctrl_plat_phy.c` with a copy of `phy_peer.hpp` that records register 4 at each restart. The boot's register-4 write is dropped once, and every later access is answered.
  - Result: `register4=0001 advertised-at-last-restart=01e1 restarts=1 adv-owed=0`. The only restart ran on 100BASE-TX advertised. Later polls repair and verify register 4 with no further restart. The added test fails, and the 16 original tests pass.
- **Impact:** after a transient management fault, the PHY keeps the negotiation it made with 10/100 advertised. With a 100BASE-TX-only partner the physical link can stay up at 100 Mb/s while the firmware publishes it down. That is #840's silent-link outcome. It lasts until the next physical link loss, and the documented guarantee does not hold.
- **Required outcome:** once a write has been repaired, the verified advertisement must govern the PHY's negotiation. The restart's own latched loss, and an advertisement the PHY still holds, must still cause no restart loop. The header, the README and P15 must state that distinction. No implementation is prescribed.
- **Verification:**
  - A test whose peer latches the advertised abilities at each restart, over a dropped write at boot and after a loss, with a 100BASE-TX-only partner.
  - `retry_probe.sh` passes on the corrected head.
  - P11-P16 and the no-loop arm (P13) stay green, and the control campaign catches every plant.

### R851-F2 - MINOR - Tests - the after-loss restart decision is graded only on a PHY that lost both registers

- **Artifacts:** `sw/firmware/ctrl/test/test_plat_phy.cpp:545-562` (P14 sets `regs[4] = 0x01e1` and `regs[9] = 0x0300` together), and the decision at `ctrl_plat_phy.c:226-227`.
- **Authority/evidence:** AGENTS.md section 6, Tests: "each new test can fail for the defect it claims to detect". The decision reads both registers (`gigabit_only(local, gig)`), but no test takes one of them away alone. Two mutants survive (`receipts/probe_mutants.txt`):
  - m3 reads register 4 as held (`gigabit_only(0u, gig)`). It survives all 16 PHY tests, and it also survives the **whole unit gate**: `test_ctrl_firmware.py --require-rv32` on a clone carrying it ends `test_ctrl_firmware: PASS` (`receipts/m3_mutant.diff`, `receipts/m3_unit.log`, `m3_unit.rc` 0). That gate covers the composed platform boot at one and two interfaces.
  - m3b reads register 9 as held. It survives the 16 PHY tests.
  - The split boot simulation's PHY always keeps both registers after a loss, so it cannot see either mutant.
- **Impact:** if a PHY lost only register 4 (10/100 advertised again) behind a loss, a defect that skips its restart would pass every gate. The negotiation would then run with 100BASE-TX advertised. That is the "100BASE-TX left advertised after a loss" case the focus names. The code at this head is right; the oracle is missing.
- **Required outcome:** the after-loss restart is graded with register 4 lost alone and with register 9 lost alone, each requiring one restart.
- **Verification:** m3 and m3b are each caught by name (`scripts/mutants.sh`). They can be added as plants in `plat_mutants.py`.

### R851-F3 - MINOR - Docs - the fit page's section 3 still states the platform entry as 60.5 "since the split's PHY poll", refused at 61.0

- **Artifacts:** `docs/design/SPLIT_CONTROL_MEMORY.md:143` and `:147`, against `:146`, `:148`, section 5's `:283` and `sw/litex/ctrl_memory.py:274` (entry 61.0).
- **Authority/evidence:** AGENTS.md section 6, Docs ("changed contracts are reflected in authoritative docs"). Two statements contradict the head's ledger:
  - `:143` is the lane's round-1 sentence: "It is 60.5, that decision's cap, since the split's PHY poll (#919) ... ROM debt of 4.5 RAMB36 ... refused at 61.0".
  - `:147`'s "60.5 for the platform's, which their entries now hold; ... refused ... at 61.0" no longer holds.
  - On this branch's line the entry went 60.5 by #895 (`:146`), then 61.0 by the PHY poll (`:148`, `:283`), and it is refused at 61.5.
  - The merge replay (`receipts/merge_replay.txt`) shows `:143` was carried in automatically, outside the six conflict hunks. Every hunk around it was resolved and restated, but this line was not.
- **Impact:** the authoritative ledger page gives two causes for 60.5 and two refusal points for the same image. A cold reader cannot tell the head's refusal point (61.5) from section 3.
- **Required outcome:** section 3 states one history: 60.0, then 60.5 (#895), then 61.0 (#919, #840), refused at 61.5. The round-1 sentence is removed or marked as pre-merge, and `:147` is restated or dated.
- **Verification:** reread section 3 against `ctrl_memory.LEDGERED` and section 5. The docs gate stays rc 0.

### R851-F4 - MINOR - Conformance, Docs - the frame and work counts the header and README state are wrong (retains R852-F2)

- **Artifacts:** `sw/firmware/ctrl/plat/ctrl_plat_phy.h:57-59` ("nine more frames, seven reads and three writes ... a whole Clause-22 frame of 65 bit periods") and `sw/firmware/ctrl/plat/README.md:94` ("A frame is 65 bit periods").
- **Authority/evidence:**
  - This round recounted the stages at `ctrl_plat_phy.h:205-214`. The advertisement is six reads (15, 4, 9, 0, 4, 9) and three writes (9, 4, 0), nine frames in all, and two writes when no restart is due.
  - A frame is 64 bit periods: `CTRL_PLAT_PHY_FRAME_BITS` 64 (`ctrl_plat_phy.h:169`), the loop at `ctrl_plat_phy.c:72`, the comment at `ctrl_plat_phy.c:62`, and 22.2.4.5's 32 + 14 + 2 + 16.
- **Impact:** the THE STEP description contradicts its own total and the frame format. The measured 155 us admission is unaffected. The counts are numerical protocol claims, so this is not RESIDUE.
- **Required outcome:** six reads and three writes, and 64 bit periods, in both places.
- **Verification:** a recount against the stage table and `CTRL_PLAT_PHY_FRAME_BITS`.

### R851-R1 - RESIDUE - Docs - new source comments carry an issue-comment ID and a lane name (also R852-R1; found independently)

- **Artifacts:** `sw/litex/ctrl_memory.py:237-238` (`issuecomment-6906679024` in a `#:` comment) and `:256` ("which supersedes the cap until S14").
- **Authority:** the owner's 2026-10-15 comment rule. A new instance in the reviewed delta is residue; base instances are tracked by #746.
- **Exact fix:**
  - `:237-238`: write the parenthetical as `(product_point, the owner's standing rule of 2026-11-15 as #923's ruling of 2026-11-16 applies it)`.
  - `:256`: replace "until S14" with "until the hybrid XIP work (#665 decision D3)".
  - The ledger entries' reason strings at `:283-295` repeat both, as the base's existing entries do. They are data, not comments; the manager may carry them on the same checklist line.
- **Effect on the review:** none. No figure, behaviour or artifact changes, and the residue does not affect the verdict or any lens.

### Suggestions (optional; they affect no lens)

- **S1 - Robustness - `ctrl_plat_phy.c:41-46`.** Where arming's timed run does not show a turn alone holds 200 ns, the spin falls back to `CYCLES_HALF` = 20 turns. At about 27 cycles a turn, that puts a frame near 64 x 2 x 20 x 27 cycles, about 0.69 ms. `CTRL_PLAT_PHY_STEP_US` (155 us) would then not bound the frame, and a pass could overrun THE SHARE.
  - The fallback is MDIO-safe but budget-unsafe.
  - On the split CPU the run takes about 276 us against the 205 us threshold, so it is not taken; the boot simulation measures 144.81 and 145.69 us.
  - Either state the fallback's cost or refuse to poll on it.
- **S2 - Robustness - `sw/firmware/ctrl/plat/ctrl_plat_gen.py:148-153`.** A split SoC export with none of the three PHY rows links an image whose poll arms nothing, silently. That is the rehearsal's defect class.
  - The product SoC's MilanMAC carries the rows whenever the board routes MDIO, and the release passed its link flap on the same SoC, so this head is not affected.
  - A gate that refuses a split platform image without the rows, on a board whose release image polls, would close the class.
- **S3 - Conformance (ruling wording).** Ruling #665 6899740728 item 4 says "no pass carries both a store step and a PHY poll slice". The head lets a frame follow a store step from the OFF, IDLE or HELD phase, and keeps it off a save's step (CAPTURE to VERIFY).
  - `nvm_store.c` shows such a step only judges whether a save is due; `nvm_capture_begin` does not touch flash.
  - The reading is published in `ctrl_plat_phy.h:63-70` and the PR body.
  - The manager may record whether the ruling meant a save's step.

## Prior public findings: resolved or retained

The prior public findings on this PR are R852-1's, the external round's NEGATIVE of 2026-11-16 at this same head. The PR has no submitted reviews and no review threads.

| Prior finding | This round at `afa3ea19` | Evidence |
|---|---|---|
| R852-F1 MAJOR, advertisement recovery leaves the old negotiation active | **Retained**, as R851-F1, MAJOR | Reproduced with this round's own probe: `receipts/retry_probe.log` |
| R852-F2 MINOR, numerical frame/work counts | **Retained**, as R851-F4, MINOR | Recount at `ctrl_plat_phy.h:205-214`, `:169`; `ctrl_plat_phy.c:62`, `:72` |
| R852-R1 RESIDUE, issue-comment ID and lane name in comments | **Retained**, as R851-R1 | Found by this round before the fetch (`INDEPENDENT.txt`) |
| R852's "no dropped-side defect" in the merge | **Not retained** as a clean result | R851-F3: the round-1 line at `SPLIT_CONTROL_MEMORY.md:143` was merged in outside the conflict hunks |

## The focus items, checked against code and receipts

**(1) `ctrl_plat_phy.c` against the release's `phy_link_tick`** (`milan_baremetal.c:1048-1082` here, and dev's `phy_advertise_gigabit_only`):

- **Probe.** One PHYID1 address per call, and a miss (`id` 0, 0xffff or no acknowledgement) publishes 0. The next address is due at once, there is no scan, and the address wraps at 32 (`:152-162`, P1, P5). A found PHY goes straight to BMSR in the same poll, as the release does.
- **Latched loss.** A link published up and read down publishes 0 first (`:167-170`). The second BMSR runs only while the published link is down, as in the release (`:171-173`). The boot simulation shows `[0, 13]` after the latched loss, `[0, 0]` after the down, and `[13]` after the return. There is no missed edge: each edge is a published level change, separated by at least one frame and by the advertisement's frames after a loss. There is no double count: republishing an unchanged word is not an edge.
- **Resolution.** Forced mode, 1000BASE-T through 9 and 10 with the fault, and 4 and 5 for the highest common mode. Every arc matches the release, and words 13, 5, 11, 3, 9 and 1 are the release's (`:179-256`, P4, P5).
- **Pace.** `CTRL_PLAT_PHY_POLL_US = MILAN_NVM_HEARTBEAT_MS * 1000 / 2` = 125 ms. The release's `PHY_POLL_NS = NVM_HEARTBEAT_NS / 2` reads the same `MILAN_NVM_HEARTBEAT_MS` (250, `scripts/nvm_shape.py:145`). The wrap-safe test is `:276-279` (P2, P10).
- **No blocking poll.** At most one frame a call (`:291-298`, P7), taken only with 155 us of room. Arming's calibration spins 1,024 turns once, before the loop runs.
- **Pass class.** The frame is THE STEP's work. It is withheld in a call whose store took a save's step (`:307-316`, B12). The stated 155 us bounds the measured 144.81 us (1x1/1if) and 145.69 us (8x8/1if) by construction. The 145.37 us figure in the brief was the round-1 head's, before the advertisement; the head's header (`:183-191`) states the current figures.
- **Advertisement.** At boot: register 9 `0x0200`, register 4 `0x0001` and register 0 `0x1200`, read back. After each loss: 9 and 4 rewritten and read back, with no restart where the PHY holds them. This was graded in the boot simulation. The values are dev's release init's. The exception is the recovery case, R851-F1.

**(2) The link edge's consumers on the split (RTL unchanged, `git diff 70f4056f afa3ea19 -- hdl` empty):**

- The CSR (`milan_soc.py:1985`) goes through `MultiReg` (`:2013`) to `i_link_up`, then to `eff_link_w` (`milan_datapath.sv:3351`).
- The LINK_UP and LINK_DOWN counters are `:4033-4059`, read at `:4078-4079`.
- The counter-change notification goes through COUNTERS_CHANGED to `ctrl_app_aecp.c` (plant `plat-link-counter-change-dropped`, L3).
- gPTP's `port_enabled_i` is `:9129`; its edge ends the Pdelay_Req cease and re-earns asCapable (Milan v1.2 4.2.6.2.5; L4 in the host model).
- The mailbox's `o_ctl_link_up` is `:10081`, which feeds ADP, MAAP and SRP.
- These paths were read at the head. The datapath consumers are not simulated with the firmware, and the bench run is the gating run's.

**(3) Tests:**

- P11-P16 are present and pass: 16 of 16 in this round's suite build, and inside the unit gate.
- The 44 PHY plants, with the 18 advertisement plants among them and `plat-phy-100base-tx-advertised` first, are each caught by name in the author's campaign log at `afa3ea19`: `mutants: 760 of 760 caught` (`workflows/logs/rtl-fast__firmware-control-mutants__ci_step_9.log` in the archive). This round's own mutants m1, m2, m4, m5, m7 and m8 are caught. m6 is equivalent, since -1 reads as all ones. m3 and m3b survive (R851-F2).
- Coverage, reproduced by this round: `ctrl_plat_phy.c 173/173 lines, 160/160 branches`, `firmware coverage: PASS (40 files)` (`receipts/fw_coverage.log`).
- The boot simulation grades the writes. Its plant `phy-unadvertised` is caught (`receipts/boot_self.log`).

**(4) The merge and the ledger:**

- The replay of 55769f09 + 70f4056f gives six conflicts: `SPLIT_CONTROL_MEMORY.md`, `plat/README.md`, `ctrl_plat.c`, `coverage.ratchet`, `ctrl_memory.py` and `ctrl_memory_ledger.py`.
- `ctrl_plat.c` keeps both sides: dev's `AECP_ENTITY_NAME_RUNS` and the lane's THE STEP binding. The ratchet and ledger sizes are restated at the head (17,600, 19,136, 18,240 and 20,416). `ctrl_memory.py`'s text takes dev's side, then restates it.
- The one defect is the automatically merged doc line, R851-F3.
- The ledger agrees with the PR body at every point. 8x8/1if is 56.5 by `platform-8x8-one-interface` (`product_point`, by the image's symbols), and 8x8/2if is 61.0 (`receipts/ledger_self.log`: 4 points PASS and 8 of 8 controls). This round's link of the head's 8x8/1if platform image plans `"ledgered": "platform-8x8-one-interface"`, 56.5. `test_ctrl_memory.py` gives PASS.
- **Overlap with PR #931** (`70c100da`, `receipts/pr931_ledger_70c100da.diff`): the same entry names and figures, through a different mechanism. #931's `own_point` matches any ledgered entry by its symbols. This PR's `product_point` matches only entries flagged `product=True`, so its SoC build plans 8x8/2if only by name. #931 also raises the size fixture to 59.5.
- **What the train must reconcile:** the helper and its semantics (any entry, or product entries only), the call sites in `milan_soc.add_ctrl_memory` and `ctrl_plat_image.py`, the tests, and the entries. The composed image must also be measured. As an estimate only, this head's 8x8/1if `rom` of 132,148 B plus #923's 2,168 B passes the 133,120 B that 56.5 holds, and 8x8/2if likewise passes 61.0's 135,168 B.

**(5) The CPU budget.** This round linked the harness image (`ctrl_srp_image.py --interfaces 1 --with-aecp --layout split`) from the base `70f4056f` and from the head with the same flash map and runtime archives (`receipts/harness_image_identity.txt`).

- 1x1/1if gives `10684d74...` at both, and 8x8/1if gives `2cf4e51a...` at both. These are byte-identical and equal to the author's recorded hashes.
- The harness testbench and RTL have no diff from `70f4056f`.
- The author's regrades then carry the base's verdict:
  - 1x1/1if: rc 0, 96 groups, 0 of 130,341 passes over the share.
  - 8x8/1if: rc 1, with exactly 11 `STATED` lines (four polls-base, and seven ACMP-item or declined-offer lines in `backlog-owed`), 0 of 270,769 passes over the share.
  - At both points the 7 misses are the `backlog-owed` held-egress rows.
- These are #914's per-shape statements and the base's ruled rows, not findings. The harness composes no platform, so the PHY's place in the pass classes rests on construction (155 us of room per frame, no frame beside a save's step) and on the boot simulation's measurement, not on the harness.

**(6) Timing, the release image, and the c805f699 claim:**

- Timing is recorded as owed to #927 per ruling 6907583837. That is not a finding.
- The release firmware's inputs (`sw/firmware/milan_baremetal`, `nvm_hosttest`, `sw/litex/patches`) have no diff from `70f4056f`. The author's byte comparison stands; this round did not rebuild the release image.
- `git diff c805f699 afa3ea19` touches three files: one comment block in `ctrl_plat_phy.h`, and the boot simulation's `README.md` and `run.py`.
- This round linked the platform image at both commits with the same inputs (`receipts/platform_image_c805_vs_head.txt`): 1x1/1if `ff38341d...` and 8x8/1if `76ea1fbd...`, byte-identical at both. The harness image is identical too, as in (5). So the routes' and harness's inputs at `c805f699` are this head's.

**(7) Gates.** The author's receipts at `afa3ea19` were audited:

- 118 step logs, each rc 0, with 130 steps NOT RUN for a stated reason.
- Every step log names the head.
- The census's two timed-out attempts are kept separately.
- Control campaign 760 of 760.
- The four sweep shards (15 + 17 + 17 + 16 = 65 suites).

Exact-head hosted evidence (`receipts/hosted_check_runs.txt`, read at review time): 4 check runs had completed with success (`wire-accountability`, `full-ci-gate`, `docs-gates-0`, `docs-check-no-git`). One was skipped (`Physical gPTP`), and the rest were queued or in progress. The manager owns hosted and act acceptance.

## What this round executed

All runs below were at the exact head unless marked, on this round's clone or on disposable shared clones under the packet's scratch.

| Run | Result | Receipt |
|---|---|---|
| `test_ctrl_firmware.py --require-rv32` (every arm, platboot at 1 and 2 interfaces, platmap, platrv32) | rc 0, `test_ctrl_firmware: PASS` | `receipts/fw_unit.log` |
| `fw_coverage.py --check` | rc 0, `ctrl_plat_phy.c 173/173, 160/160`, PASS on 40 files | `receipts/fw_coverage.log` |
| Split boot simulation 1x1/1if | rc 0, PASS; PHY lines equal to the author's at `afa3ea19`; 59 frames, longest 144.81 us; MDC 950/1120/2260 ns | `receipts/boot_1x1.log` |
| Split boot simulation 8x8/1if | rc 0, PASS; PHY lines equal to the author's; longest frame 145.69 us | `receipts/boot_8x8.log` |
| Split boot simulation self-test | rc 0: 6 of 6 native controls, 6 of 6 plants caught (`phy-unpublished`, `phy-loss-not-latched`, `phy-unadvertised` among them), 0 placement controls wrong | `receipts/boot_self.log` |
| `plat_ledger.py --self-test` | rc 0: 4 points PASS, 8 of 8 controls | `receipts/ledger_self.log` |
| `sw/litex/test_ctrl_memory.py` | rc 0, PASS | `receipts/test_ctrl_memory.log` |
| Harness image, base against head | byte-identical at both shapes | `receipts/harness_image_identity.txt` |
| Platform image, `c805f699` against head | byte-identical at both shapes | `receipts/platform_image_c805_vs_head.txt` |
| PHY suite mutants m1-m8, m3b | m3 and m3b survive; m6 equivalent; the rest caught | `receipts/probe_mutants.txt` |
| Unit gate on a clone carrying m3 | rc 0: the mutant survives every arm | `receipts/m3_unit.log`, `receipts/m3_mutant.diff` |
| Recovery probe (R851-F1) | rc 1: the added test fails, 16 pass | `receipts/retry_probe.log` |
| Merge replay | six conflicts; the resolutions and the automatically merged doc line traced | `receipts/merge_replay.txt` |
| Clone integrity after every run | PASS: HEAD and tree, index unchanged (1,636 entries), every blob's bytes and mode, no untracked or ignored file, five submodules at their gitlinks and clean | `receipts/integrity.log` |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F4 | `ctrl_plat_phy.c:129-316` against the release's `phy_link_tick` (dev-soft-core) and `phy_advertise_gigabit_only` (dev `6b66f66d`); `ctrl_plat_phy.h:28-47`, `:181-191`; scope addition 6907491954; ruling 6899740728 item 4; REQ-MAC-03; `retry_probe.log` | R851-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| RTL | UNCLEAN: F1 | the firmware FSM `ctrl_plat_phy.c:129-272` (stage table, widths, wrap and room arithmetic); THE STEP client `:307-316` against `ctrl_loop.c:255-345` and `nvm_store.c:797-875`; `ctrl_plat.c:250-305`; the consumer path `milan_soc.py:1985-2013`, `milan_datapath.sv:3351`, `:4033-4079`, `:9129`, `:10081`; empty `hdl` diff | R851-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| Robustness | UNCLEAN: F1 | no acknowledgement, NAK, all-ones, absent PHY, clock wrap, refused stage, identity guard and no-MDIO paths (P1-P16, B11, B12); `retry_probe.log`; S1-S2 | R851-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| Tests | UNCLEAN: F1, F2 | `test_plat_phy.cpp`, `phy_peer.hpp`, `test_plat_boot.cpp` B11/B12/L1-L4, `plat_mutants.py`'s 44 plants; `fw_unit.log`, `fw_coverage.log`, `boot_self.log`, `probe_mutants.txt`, `m3_unit.log` | R851-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| Docs | UNCLEAN: F1, F3, F4 | `ctrl_plat_phy.h`, `plat/README.md:85-100`, `SPLIT_CONTROL_MEMORY.md:130-150`, `:270-290`, `:395-412`, `ctrl_split_boot/README.md:95-110`, `REGISTER_MAP.md:425`, the PR body; R1 recorded as residue | R851-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |

No lens is banked clean at this head. A corrected head re-opens every lens it touches. A fix to F1 touches all five.

## Limits

- **Not run by this round:** the CPU budget harness, the routes, the release-image rebuild, the four-shard native sweep, the AECP, SRP and control mutation campaigns, and the workflow step census. For these, this round audited the author's receipts and checked their inputs: harness and platform images byte-identical, release inputs unchanged.
- **Not run at all:** no full parent, processor, gPTP, Yosys or builder bank, no hardware, no container. Physical calibration is NOT RUN. Simulated MDC timing and the boot simulation's stand-in registers are not hardware proof.
- **Toolchain:** the unit and coverage gates ran on the host's gcc 16 with its GoogleTest 1.18. The pinned 1.14 headers fail `-Werror=sign-compare` under gcc 16 in tsn-c-stack's `test_adp.cpp`, an environment mismatch outside this diff. CI uses Ubuntu's 1.14 with its own compiler.
- **Parallel jobs:** the two boot simulations ran concurrently, and `run.py` invokes `make -j16` itself, overriding the job count passed in. For their compile phases the round briefly exceeded 16 parallel jobs.
- **The clone's `.git`:** this round fetched objects and refs into the clone's `.git` (dev `6b66f66d`, the evidence archive `c129707b`, PR #931's `70c100da`). Tracked bytes, the index and the gitlinks are unchanged (`receipts/integrity.log`). Build byproducts the gates left in the clone (Python caches, `configs/generated/*.hex`, `sw/builder/out/`, all created during this round) were removed before the final integrity check.
- **Independence:** the reading-order deviation is described under [Identity, authority and independence](#identity-authority-and-independence).

## Pending manager duties

- Publish this report.
- Carry R851-R1 (with R852-R1) to the residue checklist.
- Correct F1, F2, F3 and F4, then re-review the corrected head with every lens.
- Record the ruling-wording question in S3, if wanted.
- Reconcile this PR with PR #931 in the train: the helper semantics, the call sites, the tests and the entries, measuring the composed 8x8 images.
- Build the current-dev merge candidate with the builder and native banks, and link their receipts. No manager source bank ran at this exact head.
- Hosted and act acceptance.
- Timing per #927.
- The bench gating run: the tap link flap and gPTP resume within 5 s.
- Two independent positive reviews and the full merge and containment procedure.

## Reproduction and packet

Export `PACKET` (this directory), `CLONE` (a clean clone at the exact head with its five submodules), `LITEX` (the product LiteX tree with its venv), `RV32_SDK` (the pinned RV32 SDK's host directory) and `TOOLS` (the pinned tools: Verilator 5.050, sv2v). Then run:

- `scripts/launch.sh fw_unit python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-dir $PACKET/scratch/fw-unit --jobs 4`, which also provides the generated headers the probes use;
- `scripts/boot.sh boot_1x1 endstation_ax7101_1x1_tdm8 $PACKET/scratch/boot-1x1`, `boot_8x8` with `endstation_ax7101_8x8`, and `boot_self ... --self-test`;
- `scripts/ledger.sh ledger_self $PACKET/scratch/ledger --self-test`;
- `scripts/mutants.sh`, `scripts/retry_probe.sh` and `scripts/harness_image_identity.sh`, the last after a base clone at `70f4056f` in `$PACKET/scratch/basetree`;
- `scripts/integrity.sh`.

In receipts, `<packet>`, `<clone>`, `<litex>`, `<rv32-sdk>`, `<tools>` and `<home>` stand for those locations. Only `REPORT.md` and the files listed in `MANIFEST.sha256` are for publication; `scratch/` is not.

R851-1 FINISHED
