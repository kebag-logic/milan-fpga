[R852] NEGATIVE - exact head afa3ea19d6a1075382c63e4fc1e188a9aadf33bb

External independent review, R852-1, issue #919 / PR #933. All five lenses were applied. One MAJOR and one MINOR remain open. A separate source-comment RESIDUE does not affect the verdict. No source was changed and nothing was published to GitHub.

The decisive defect is recovery from a failed advertisement write: the registers can become correct while the PHY continues using the abilities from the earlier negotiation. The existing suite passes this condition because it checks registers and restart count without modelling negotiated abilities separately.

**Identity, authority and independence.** Tree: `406dc4ba57ae0b7e1f06f5e400356872cabc32af`. All source paths below refer to [this exact head](https://github.com/kebag-logic/milan-fpga/tree/afa3ea19d6a1075382c63e4fc1e188a9aadf33bb). Reconstruction followed AGENTS.md / CONTRIBUTING.md, docs/README.md, the frozen [issue #919](https://github.com/kebag-logic/milan-fpga/issues/919) and public decisions, linked requirements/interfaces, original-base diff/history, then public executable evidence. Authorities included:

- [Advertisement scope addition](https://github.com/kebag-logic/milan-fpga/issues/919#issuecomment-6907491954), #840 and the 2026-11-05 gigabit-only decision.
- [Rehearsal finding 12](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899519003) and [ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6899740728).
- [Timing/backlog ruling](https://github.com/kebag-logic/milan-fpga/issues/919#issuecomment-6907583837) and [product-ledger ruling](https://github.com/kebag-logic/milan-fpga/issues/923#issuecomment-6906679024).
- REQ-MAC-03, IEEE 802.3 clauses 22/28, Milan v1.2 4.2.6.2.5, IEEE 1722.1-2021 AVB_INTERFACE counters, the register/mailbox contracts and split architecture.

The evidence examined comprises the public `author-r1` and `author-r2` directories in [archive c129707b](https://github.com/kebag-logic/milan-fpga/tree/c129707b2d1d3b84c746849c9201b96ef2b1499d/review-evidence/919-r1), [REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/919#issuecomment-6929222018), and public issue/PR comments. No private author material or another reviewer's report was read. `INDEPENDENT.txt` records the independent verdict and ledger before prior PR findings were sought. The subsequent inspection returned two review-start comments, zero submitted reviews and zero review threads: no prior public findings on PR #933 required resolution or retention. The separate internal round remained in flight; its result is not assumed.

**R852-F1 — MAJOR — Conformance, RTL, Robustness, Tests, Docs — advertisement recovery can leave the old negotiation active.**

Artifacts: `sw/firmware/ctrl/plat/ctrl_plat_phy.c:228` through the restart/readback cases at 248; `sw/firmware/ctrl/test/test_plat_phy.cpp` P15; `sw/firmware/ctrl/test/phy_peer.hpp:145`; `sw/firmware/ctrl/plat/ctrl_plat_phy.h:35` and `:43`; `sw/firmware/ctrl/plat/README.md:92`; packet files `retry_probe.cpp`, `retry-probe.log`, `retry-control.log`.

Authority/evidence: #919 requires the gigabit-only advertisement written and verified at boot and after every loss; #840 requires a 100BASE-TX-only partner to get no physical link. Clause 28.2.4.1.3 couples a changed advertisement with renewed negotiation: readback alone does not activate the new abilities. The mechanism was cross-checked in the public [IEEE 802.3-2012 text, section two, page 300](https://www.my-wire.de/schnittstellenbeschreibung/ethernet.pdf); this is corroboration of the cited mechanism, not a claim to have inspected a later complete edition.

The first attempt writes registers 9 and 4, restarts, then verifies. `ADV_RESTART` sets `ADV_RESTARTED` before verification succeeds. If register 4's write was dropped, that restart uses its old 10/100 advertisement. Later polls repair register 4, but `ADV_SET_LOCAL` skips further restarts because the flag remains set. Successful readback clears the owed state without making the repaired advertisement active.

The disposable probe adds a negotiation latch to the existing pin-level peer, drops register 4 writes during the first poll, then allows all accesses for ten more periods. Its partner supports 100BASE-TX full duplex alone. The result is:

```text
register4=0001 advertised-at-last-restart=01e1 active-Mbps=100 restarts=1 owed=0 published=0
```

All original 32 tests, including P11–P16, still pass; the added test fails its two active-advertisement/link assertions. With the fault disabled, all 33 tests pass and active speed is zero. This is a model counterexample to the generic management contract, not physical PHY evidence or a claim that every PHY implements this identically. The model keeps negotiated abilities separate from subsequently writable configuration registers.

Impact: a recovered management-write fault can leave the forbidden 100 Mbps physical link established while firmware reports down, recreating #840's silent-link outcome. P15's fixed “once” restart expectation enforces the defective retry behaviour. The header/README's unconditional no-100-link and retry claims consequently do not hold.

Required outcome: eventual success after a failed advertisement attempt must make the verified abilities govern negotiation. A healthy retained advertisement and the restart's own latched loss must still avoid a restart loop. Update the docs and regression oracle to express that distinction; no specific implementation is prescribed.

Verification: retain P11–P16 and existing no-loop controls; add a peer that latches negotiation abilities and failed-write/recovery cases at boot and after a loss. Check both readback and active negotiation with a 100BASE-TX-only partner. Re-run the focused probe and relevant campaigns at the corrected head. All five lenses remain UNCLEAN: protocol outcome, firmware FSM/interface, transient-fault handling, regression oracle, and documented retry/conformance claim.

**R852-F2 — MINOR — Conformance, Docs — numerical frame/work counts contradict the implementation.**

Artifacts: `sw/firmware/ctrl/plat/ctrl_plat_phy.h:57`, `:58`, `:59`, `:169`; `sw/firmware/ctrl/plat/README.md:94`; `ctrl_plat_phy.c:63` and its frame loop/advertisement stages.

Authority/evidence: the header calls nine additional frames “seven reads and three writes”; header and README say a frame occupies 65 bit periods. The full-preamble Clause-22 frame is 32 + 14 + 2 + 16 = 64 bits, matching the constant, loop and pin peers. The full advertisement sequence has six reads (15, 4, 9, 0, 4, 9) and three writes (9, 4, 0), nine frames. A retained advertisement after loss omits the restart write.

Impact: the authoritative step-work description contradicts both the protocol/frame count and its own total. This does not disprove the measured 155 us admission figure. It is MINOR rather than wording-only RESIDUE because the correction changes explicit numerical protocol/work-count claims.

Required outcome: state “six reads and three writes” for the full additional sequence and “64 bit periods” in both descriptions, retaining the conditional restart omission. Verification: recount the state/register sequence and compare docs, constant, loop and frame tests. Conformance and Docs remain UNCLEAN until corrected and re-reviewed.

**R852-R1 — RESIDUE — Docs — new source comments contain prohibited workflow references.**

Artifact: added commentary in `sw/litex/ctrl_memory.py:237`–`:238` and `:256`, relative to the merged base.

Authority/evidence: the owner's 2026-10-15 source-comment rule permits behaviour/reason and issue/requirement IDs, but excludes issue-comment IDs and lane names. New commentary includes `issuecomment-6906679024` and `S14`.

Impact: comment-style residue only; no measurement, generated artifact, code behaviour, privacy rule or conformance claim changes. Existing base instances are not re-filed.

Exact fix: replace the comment's parenthetical beginning with `product_point` through the issue-comment ID with “(`product_point`, #919 and #923)”; replace “supersedes the cap until S14” with “supersedes the cap until the hybrid XIP work (#665 decision D3)”. Keep numerical allowances and behaviour unchanged. Verify the comment diff. This does not leave a lens unclean; carry it on the manager's residue checklist.

**Five-lens examination.**

Conformance: `ctrl_plat_phy.c:152` probes one PHYID1 address per opportunity, advances on zero/all-ones/no-ack, and has no blocking address scan. BMSR publishes latched loss before the current-state reread. Forced mode, negotiated gigabit and fallback common-mode resolution publish speed/duplex. Header `:182` derives 125 ms from half `MILAN_NVM_HEARTBEAT_MS`, matching the release's `PHY_POLL_NS`; the release poll and host tests were the behavioural comparator. Nominal advertisement writes/readbacks meet the added scope. F1 is the recovery exception; F2 is the numerical contract discrepancy.

RTL/architecture: each admitted call performs at most one 64-bit MDIO frame. `ctrl_plat_phy_store_step()` at `ctrl_plat_phy.c:306` detects an advancing CAPTURE–VERIFY save step and withholds PHY work in that call. `ctrl_plat.c` binds it into THE STEP; `ctrl_loop.h` supplies its pass-class/age contract. Identity failure leaves MDIO unarmed; later refused boot stages still poll. MDC drive/turnaround/release, calibrated half-period, wrap-safe time, field widths and synchronized consumers were examined. There is no RTL delta from `70f4056f`; the firmware FSM remains in this lens and F1 prevents a clean result.

The link edge was traced beyond the host test model:

| Consumer | Exact-head artifacts/path | Result and limit |
|---|---|---|
| Link/speed/duplex | `sw/litex/milan_soc.py:1985`, `:2013`, `:2204`; `hdl/milan/milan_datapath.sv:3351` | Status fields feed synchronized MAC inputs and `eff_link_w`, with the existing software/link-guardian gates. Separated down/up publications reach the edge logic. |
| AVB_INTERFACE counters | `milan_datapath.sv:4033`, `:4058`, `:4078` | Previous effective link detects edges and increments LINK_UP/LINK_DOWN slots. Latched down and recovered up occupy separate frame opportunities. No nominal poll-driven double increment found. |
| GET_COUNTERS notifications | `milan_datapath.sv:4036`, `:9547`, `:10073`; `milan_soc.py:2957`, `:2969`; `sw/firmware/ctrl/app/ctrl_app_aecp.c:158`; MAILBOX_CONTRACT.md CTR/CTRCHG | Dirty bits reach pending-event arbitration/mailbox, then AECP family notifications; the counter face supplies actual counters. Contractual coalescing/holdoff means a rapid flap need not produce two wire notifications, though both counters change. |
| gPTP cease/asCapable | `milan_datapath.sv:9129`; `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv:711`; `gptp-processor/hdl/top/KL_gptp_engine.sv:624`, `:1123`; `gptp-processor/hdl/ucode/gen_gptp_ucode.py:2186` | Effective link reaches `port_enabled_i`; edges schedule NOTEN and a rise schedules a beat. NOTEN clears cease state/count and enters the bad-Pdelay path; asCapable must be earned again. This connects Milan's cease-ending duty. Host L4 checks the modelled enable edge, not a complete gPTP execution. |
| Other link consumers | `milan_datapath.sv:10081`; `milan_soc.py:2971`; mailbox LINK/event and control-loop dispatch | The same effective link still feeds mailbox level/events for ADP, MAAP and SRP. No private PHY-only link path bypasses these consumers. |

Robustness: P1–P16 and B11/B12/L1–L4 were examined and run for one and two interfaces. They exercise missing/invalid addresses, no-ack, latched/sustained loss, incomplete negotiation, master/slave fault, forced/negotiated modes, no-MDIO configuration, clock wrap, admission room, store/PHY exclusion, retained/reset advertisements and retries. F1 exposes the missing negotiated-state oracle despite these passing cases.

Tests: `focused.py` ran both composed 32-test platform suites and generated-bus-map checks concurrently, all rc 0. `controls.py` passed the six boot native-grader controls; its separate memory-test import stopped because `migen` is absent, retained in `ledger-controls.log`/`.rc` as an environment limit. `ledger_check.py` subsequently passed eight dependency-free synthetic-map checks for valid allowances, missing allowance, wrong symbols and half-tile excess. Those checks are not new linked-image measurements. The retry fault run returns 1 (32 original tests pass, one added fails); the no-fault control returns 0 (33 pass). No existing test was weakened or tracked source edited.

Docs: the PHY header/platform README, SPLIT_CONTROL_MEMORY.md, mailbox/register/interface authorities, boot README, scope/rulings and PR evidence were compared with code and receipts. F1 affects the retry/no-100-link claim; F2 corrects numerical descriptions; R1 is separate residue. Boot stand-in identity/asCapable/Pdelay words were not accepted as real gPTP proof; expected split-versus-release smoke differences remain explicit.

**Public source-head execution audit.** `evidence_audit.py` verifies the following independently from the immutable author archive; these are author executions, not manager or reviewer full-bank executions.

| Evidence | Audited result | Limit |
|---|---|---|
| Clean-clone workflow inventory | 118 executed steps, corresponding rc files all 0; 130 explicitly NOT RUN | Not 248 executed passes or hosted acceptance. Interrupted census attempts are separate from final success. |
| Control campaign | 760/760 caught; all 18 advertisement plants matched by name, including `plat-phy-100base-tx-advertised` | Does not cover F1's absent negotiated-state oracle. |
| AECP / SRP campaigns | Terminal receipts PASS, rc files 0 | Large logs represented by archive hashes/tails; not locally replayed. |
| PHY coverage | 173/173 lines, 160/160 branches | Coverage is not semantic completeness. Inherited stale rows are not findings. |
| Four-shard sweep | 15 + 17 + 17 + 16 = 65 suites; 2,713,040 checks; zero failures/timeouts; result records name the exact head | No reviewer full-bank run. |
| Exact-head boot | 59 frames, 10 publications, 7 polls; boot writes 9=0x200, 4=0x1, 0=0x1200; two losses each rewrite 9/4 and verify | Grader checks writes as well as link publication. Longest frames: 144.81 us (1×1), 145.69 us (8×8), below 155 us. The earlier 145.37 us figure predates advertisement work. |
| Poll / MDC observations | Starts about 125 ms apart; latched `[0,13]`, down `[0,0]`, return `[13]`; return within 126.604 ms. MDC minimum high/low/period 950/1120/2260 ns | Within the 250 ms publication allowance and above cited 160/160/400 ns MDC minima in simulation. Not physical calibration. |

**Merge preservation, memory and train overlap.** The original diff `659d7687..afa3ea19` has 74 changed paths; the delta from merged base `70f4056f` has 30. Both parents of merge `8670bfb0` and its six resolutions were examined: SPLIT_CONTROL_MEMORY.md, platform README, `ctrl_plat.c`, `coverage.ratchet`, `ctrl_memory.py`, `ctrl_memory_ledger.py`. They retain the base's composed name/declaration/ledger changes and the PHY integration; later measured ledger values replace intermediate values. No dropped-side defect was found. Inherited name-run and SRP publication changes were distinguished from the PHY delta.

Final linked-image receipts report 1×1/1if 43.5 tiles (`ctrl_plat` 17,600 B), 1×1/2if 44.5 (19,136 B), 8×8/1if 56.5 (18,240 B), and 8×8/2if 61.0 (20,416 B). `product_point()` selects the shipping 8×8/1if entry only when both `nvm_stage=13,594` and `ctrl_plat=18,240` match. The SoC and image linker use that selection; ordinary budget remains 56 and two interfaces require the explicit allowance. Published linked-image controls pass at all four points, with eight planted controls. Independent synthetic checks confirm selection/refusal boundaries.

[PR #931](https://github.com/kebag-logic/milan-fpga/pull/931), inspected through its public description at `70c100da36330bb3862d76fa6eb003091775f310`, introduces the same product-entry mechanism as `own_point`, versus this PR's `product_point`. It also records size-fixture allowance 59.5 versus this PR's 59.0 and overlapping platform entries/keys. The train must reconcile the helper, call sites, tests and ledger and measure the composed image. Matching standalone size keys do not prove the combined object/ROM size. This is an integration duty, not a defect in this isolated head or approval of PR #931.

**Budget, route and release-image evidence.** Budget 1×1 regrade is rc 0. The 8×8/1if regrade is rc 1, with exactly 11 stated-cost lines: four poll-base, three ACMP-item and four declined-ACMP. Neither shape has a pass over the per-pass share; the seven held-egress backlog misses remain the base's result under the ruling. The author image-identity receipt compares base/source budget ELFs byte-for-byte. The reviewer confirmed no changes to RTL or either budget-harness directory from `70f4056f`. The stated costs remain #914's per-shape issue, not a new #919 regression. The harness does not execute the platform PHY: the scheduling argument is exclusive substitution of a <155 us frame for a save step budgeted at 770 us, supported by B12 and boot measurements, not a claim the budget run measured PHY work.

Routes and original budget/image comparisons ran at `c805f699`. The reviewer confirmed the final delta changes only PHY-header comments, boot README and native-control fixture; firmware header tokens are identical. The author's final relink receipt reports identical route ROM words, load segments and symbols for both shapes. This supports carrying the route receipts to this source head; the reviewer did not reroute.

| Image / directive | Worst setup / hold slack (ns) | Recorded result |
|---|---:|---|
| 1×1 ExtraPostPlacementOpt | +0.414 / +0.015 | Hold floor missed |
| 1×1 ExtraTimingOpt | +0.176 / +0.032 | Floors met |
| 1×1 AltSpreadLogic_high | +0.090 / +0.036 | Floors met |
| 8×8 ExtraPostPlacementOpt | +0.189 / +0.031 | Floors met |
| 8×8 ExtraTimingOpt | +0.005 / +0.036 | Setup floor missed |
| 8×8 AltSpreadLogic_high | +0.002 / +0.036 | Setup floor missed |

Those misses are owed to #927, not findings here. Release comparison reports identical `bios.bin`, disassembly and debug-stripped ELF for both release shapes against `70f4056f`; whole ELF/archive bytes differ in embedded build-directory debug strings. The 1×1/8×8 `bios.bin` hashes are `860d4771decf5b92bd167e57c690892d665eec8075902a3468b68e3b3f56041f` and `d8851b6d470e811cfd1c95b3aa3a6d3e9c367f3e1fddaac38270d484291aea99`. The final diff changes no release-image input. This is audited author comparison evidence, not an independent rebuild or a claim of identical whole debug ELFs.

**Reviewer-owned completion ledger.** Every lens was applied at this head; none is banked clean while F1 is open. F2 also leaves Conformance/Docs unclean. R1 does not affect coverage.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN — F1, F2 | #919/#840 scope; release PHY poll; `ctrl_plat_phy.c:152`, `:228`; header `:57`; Clause 22/28; retry receipts | R852-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| RTL | UNCLEAN — F1 | `ctrl_plat_phy.c:228`, `:306`; `ctrl_plat.c`; `ctrl_loop.h`; SoC/RTL consumer table; merge resolutions | R852-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| Robustness | UNCLEAN — F1 | P1–P16; B11/B12/L1–L4; `phy_peer.hpp`; `retry_probe.cpp`; fault/control logs | R852-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| Tests | UNCLEAN — F1 | platform/map/native-control/ledger/retry receipts; immutable campaign, coverage, boot, budget and sweep evidence | R852-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |
| Docs | UNCLEAN — F1, F2 | PHY header, platform README, SPLIT_CONTROL_MEMORY.md, boot README, interface authorities, public claims | R852-1 | afa3ea19d6a1075382c63e4fc1e188a9aadf33bb |

**Reproduction, integrity and limits.** From this checkout run the packet's `focused.py`, `controls.py`, `ledger_check.py`, `retry_probe.py`, and `retry_probe.py --control` with Python 3. Builds and probes stay under the packet's `scratch/`; checkout source is untouched. `controls.py` retains its missing-`migen` limitation. `evidence_audit.py` reads archive `c129707b2d1d3b84c746849c9201b96ef2b1499d` through Git (object required locally) and emits hashes for 147 inspected immutable artifacts in `evidence-index.sha256`.

`integrity.py` checks actual Git-blob bytes, regular/symlink/executable modes, HEAD/tree, index and the five required initialized submodules recursively. `integrity.log` records all passing and a clean root status. Legacy `external` stays uninitialized at its unchanged gitlink. No source restoration was necessary because added code lived solely in the packet.

No full parent/processor/gPTP/synthesis/builder bank, route, hardware or container execution was performed by this review. Physical calibration is NOT RUN; field skips and stand-ins provide no hardware proof. Full author campaigns were audited, not replayed. Hosted jobs were not inspected; no executed-versus-skipped hosted acceptance is asserted. Known #929 base gates, inherited ratchet rows and redone host interruptions are not findings.

The manager still owns publication; F1/F2 correction and independent re-review; R1's residue checklist; reconciliation with PR #931 and the train; final current-dev merge-candidate builds and builder/native banks with linked receipts; hosted/act acceptance; two independent positive reviews and the complete merge/containment procedure. No manager source bank ran at this exact head. Source base `659d7687`, merged source base `70f4056f`, and live dev `6b66f66d89cf25d2717687bcc2c3bf617685a99a` are distinct. This report validates no future merge result and authorizes no merge.

Only REPORT.md and files listed in MANIFEST.sha256 are intended for publication. Scratch trees and extracted archives are excluded.

R852-1 FINISHED
