[A564]

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

BLOCKED — round 1b STOP: packing 6/6 passes; timing 5/6 passes. `691-rx-iob` -> `dev`.
Unchanged local head: `35fb2a95007ce6dd1ec4f51c2dcb793800623cfd`.
This is a prepared description; the branch has not been pushed.

All three dev rows and the first two #645 overlay rows pass the required timing margin. The #645 overlay under `ExtraTimingOpt` returns rc 1 at qualification: Slow 0 C and 85 C WNS/WHS is +0.013/+0.069 ns; Fast 0 C and 85 C is +1.561/+0.036 ns. Slow WNS is 0.017 ns short of the +0.030 ns requirement. All six complete IOB checks report 21 PASS, one expected INERT and zero FAIL, including every required RX capture.

Ruling 6042557053 requires STOP on any failed row. No alternative directive, source change or further gate run followed the failure. Acceptance 4 is not met.

The complete builder rerun returned rc 0, with one absent retired-board calibration report explicitly NOT RUN. The final physical-clock leg passed 193 checks with zero failures, rc 0. Round 1 capture equivalence, three behavioral mutants, the preserved reset-before-D control, standalone simulations and Ethernet evidence remain retained. The earlier STOP arose from an execution-window limit; ruling 6042557053 authorized the completed long runs.

## Linked Issue / roles

Closes #691
Relates to #645 and #475.

Executor: `[A564]`
Internal cleared-context reviewer: `[R546]`
External reviewer: `[R547]`

## Description

The synthesis control-set heuristic could move the GMII receive reset into a LUT before capture D. That prevented IOB packing after unrelated logic changes. The new dependency patch samples data and valid without reset, samples reset alongside them, and masks the captured outputs with that sampled reset. This retains the original cycle latency, synchronous reset and last-byte behavior while removing the input-flop reset that the heuristic could remap.

| Changed area | Result |
|---|---|
| PHY patch and maintained patch series | Direct pad-to-capture D paths; reset acts after capture |
| Capture simulation and runner inventory | Exhaustive byte/reset/valid cases plus frame boundaries and active-frame reset |
| Placement fixtures and checker self-test | Preserved reset-before-D defect is rejected before routing |
| Build and patch documentation | Mechanism, unchanged contracts and validation entry points recorded |

Production capture uses no preservation attribute. The negative fixture preserves its inserted LUTs so synthesis cannot repair the deliberately planted defect. Default selection, register map and deployed image are unchanged.

## Authoritative references

- #691 acceptance criteria, assignment comment 6041364533 and continuation ruling 6042557053.
- #645 round-2d STOP comment 6041331463.
- #475 and `sw/litex/iob_pack_check.tcl`.
- `REQUIREMENTS.md`, Ethernet and verification requirements.
- `CONTRIBUTING.md`, section 3.
- `docs/integration/BUILDING.md`, IOB packing contract and section 5 timing margin; `docs/testing/RUNNING_TESTS.md`, AX7101 WNS >= +0.030 ns and WHS >= 0 per corner.

## How to get into the same state

Use the assigned local checkout and the pinned project dependency environment documented in `docs/integration/BUILDING.md`. Set `REPO` to the checkout, `SCRATCH` to a separate scratch directory and `PYTHON` to that environment's interpreter. The original environment must contain the preceding patch series. Copy the receiver package before applying this lane's additional patch.

```sh
cd "$REPO"
git switch 691-rx-iob
test "$(git rev-parse HEAD)" = 35fb2a95007ce6dd1ec4f51c2dcb793800623cfd
export REPO SCRATCH
"$PYTHON" - <<'SETUP'
import os
from pathlib import Path
import shutil
import liteeth
scratch = Path(os.environ["SCRATCH"])
deps = scratch / "deps"
deps.mkdir(parents=True, exist_ok=True)
shutil.copytree(Path(liteeth.__file__).parent, deps / "liteeth")
SETUP
git -C "$SCRATCH/deps" apply "$REPO/sw/litex/patches/0007-liteeth-gmii-rx-capture.patch"
export PYTHONPATH="$SCRATCH/deps"
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=0
export MILAN_LITEX_PYTHON="$PYTHON"
```

The second full-image input is `2525eae9567865a8bc741901914bdf5a1caf2c26` plus this branch's diff from `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. Its recorded overlay tree is `01f65c3b2693d2b1c494e0738b9562a1778740b5`. Keep that experiment in a separate scratch checkout.

## How to validate

```sh
cd "$REPO"
"$PYTHON" sw/litex/test_gmii_rx_capture.py
"$PYTHON" sw/litex/iob_pack_selftest.py
"$PYTHON" -c 'import sys; sys.path.insert(0,"sw/builder"); import test_builder as t; t.test_toolchain_patches_are_applied(); t.test_toolchain_patch_gate_bites()'
bash scripts/run_litex_sims.sh --selftest
bash scripts/run_litex_sims.sh "$SCRATCH/standalone-logs"
"$PYTHON" sw/litex/test_gmii_rx_capture.py --emit-dir "$SCRATCH/capture"
```

Expected results: 1,036 capture comparisons; 22 checker arms and 21 mutants with no failures; all five patch omissions detected; five standalone simulations passing, none skipped. The companion handoff supplies the physical fixture constraints and recipe, exact command receipts, artifact hashes, Ethernet/datapath evidence and complete gate table.

| Validation | Current result |
|---|---|
| Compact positive fixture at control-set threshold 100 | 9/9 required pads in ILOGIC |
| Preserved reset-before-D fixture | 9/9 refusals before routing; expected-refusal wrapper returns 0 |
| RX filter, RMON, TX reset and link guard | Pass |
| Datapath prerequisite legs and two mutation campaigns | Pass; each campaign detects all six controls |
| Final datapath leg and complete builder rerun | rc 0; 193/0 physical checks; one unavailable retired-board calibration arm |
| Lint, parser ratchet, source lists, documentation and style | Pass |
| Both full shipping projects | Elaborate successfully |
| Full-image packing and timing | Packing 6/6 passes; timing dev 3/3 and #645 2/3 passes; final row refused for setup margin |

The six-row sweep is complete below. Each corner cell is WNS / WHS in ns. The 0 C and 85 C endpoints repeat fixed Slow/Fast models. Every corner has zero TNS and THS. All Ethernet crossing reports retain the four 8 ns datapath-only checks; none has an Unsafe row or rejected-constraint diagnostic.

| Tree | Placement directive | Full IOB check | Slow 0 C | Slow 85 C | Fast 0 C | Fast 85 C | Result |
|---|---|---|---|---|---|---|---|
| dev + fix | ExtraPostPlacementOpt | 21 PASS, 1 INERT, 0 FAIL | +0.492 / +0.040 | +0.492 / +0.040 | +1.660 / +0.007 | +1.660 / +0.007 | PASS |
| dev + fix | AltSpreadLogic_high | 21 PASS, 1 INERT, 0 FAIL | +0.064 / +0.052 | +0.064 / +0.052 | +1.638 / +0.029 | +1.638 / +0.029 | PASS |
| dev + fix | ExtraTimingOpt | 21 PASS, 1 INERT, 0 FAIL | +0.098 / +0.074 | +0.098 / +0.074 | +1.362 / +0.036 | +1.362 / +0.036 | PASS |
| #645 round 2d + fix | ExtraPostPlacementOpt | 21 PASS, 1 INERT, 0 FAIL | +0.238 / +0.102 | +0.238 / +0.102 | +1.518 / +0.036 | +1.518 / +0.036 | PASS |
| #645 round 2d + fix | AltSpreadLogic_high | 21 PASS, 1 INERT, 0 FAIL | +0.227 / +0.071 | +0.227 / +0.071 | +1.521 / +0.035 | +1.521 / +0.035 | PASS |
| #645 round 2d + fix | ExtraTimingOpt | 21 PASS, 1 INERT, 0 FAIL | +0.013 / +0.069 | +0.013 / +0.069 | +1.561 / +0.036 | +1.561 / +0.036 | FAIL |

The full recipe is AX7101, shipping 1x1 TDM8, eight wire channels, all-fabric control, 50 MHz Milan clock, inverted transmit clock and shipping floorplan. Synthesis uses `AreaOptimized_high`, optimization `ExploreArea`, and routing/physical optimization `AggressiveExplore`, with the default seed and 12 implementation threads. Cacheless bare-metal management, disabled playback/render low-pass filter, enabled loopback/fabric gPTP and 656/219 ns ingress/egress latency remain as selected by the shipping recipe. The handoff records complete commands, input identities and artifact hashes.

The failing Slow setup path runs from `pp_shadow/u_pp/u_notify/wr_ix_r_reg[1]` to `pp_shadow/u_pp/u_tx_arbiter/slot_r_reg[1]` in the 20 ns clock group. That is the report's observation; no cause or repair is asserted. The failed row's generated evaluation artifact is not a passing candidate.

## Known limitations / out of scope

Acceptance 4 is blocked by the #645 `ExtraTimingOpt` setup margin. The remaining complete local regression and portability gates were not started after the mandatory STOP. The builder's retired-board calibration arm lacks its saved report and is explicitly NOT RUN. The original datapath aggregate was interrupted; the previously completed constituents plus the rerun final physical-clock leg provide the recorded evidence, without a fresh aggregate verdict. Hosted checks and both independent reviews remain outstanding.

No physical acceptance, deployment or merge is claimed. There is no register-map change, and the shipping configuration remains selected as before.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [x] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
