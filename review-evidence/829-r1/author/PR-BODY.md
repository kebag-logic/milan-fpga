[A725b]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally, 65 of 65 suites with one shard rerun, review pending — `829-mii-gptp` -> `dev`, head `4cda0aa0`.

The Arty's acceptance was shown on a bench branch: this head, the #583 clock ruling, and a runtime correction that is not in this PR. The reasons are under [Known limitations](#known-limitations--out-of-scope).

## Linked Issue / roles

Relates to #829
Relates to #583

Executor: `[A725b]`, continuing `[A725]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

**The fault.** On the 100 Mb/s MII port the launch observer read one octet per clock, while `phy.sink` holds each octet for two.

The failing signal is `KL_gptp_gmii_launch.cand_r`. It falls at seam cycle 7 of the first frame, on the delimiter check, where the held preamble is read as the next octet.

No launch record came, so the ledger never drained, the engine's response claim held the next Pdelay_Req at the queue head, and the event queue filled.

The same bench at GMII timing passes at every cycle, with the delimiter at cycle 7 where the check expects it.

**What the first report said wrongly.** "Sends no frame" came from a capture on another link. On the Arty's own link gPTP frames do leave; what failed was timing them. `GM_LOSS_RECOVERY` and the plane's reset seal are not involved.

**The change.**

| Piece | Change | Why |
|---|---|---|
| `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv` | Counts an octet where `valid` and `ready` coincide | MII holds each octet for two clocks. GMII's `ready` is the constant 1, so that term folds away |
| `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv` | Adds the first-symbol term to the reconstruction, and scales the PHC history guard to the window | The observer counts octet 0 on the edge that registers its high nibble, one clock after the reference plane |
| `KL_gptp_shadow.sv`, `milan_datapath.sv` | Carry `ETH_TICK_NS_P` and `ETH_CYC_PER_OCTET_P` to the two above | Defaults are the GMII shape |
| `sw/litex/milan_soc.py`, `sw/builder/endstation_builder.py` | State the MII shape per PHY model, and the builder's datapath parameters read the same table | One source for the shape |
| `sw/litex/gen_mac_tx_model.py`, `tb/verilator/gptp_txts/` | Convert the MII stages of the product's chain and run the closed loop on them | The regression below |
| Documents | `GPTP_PLANE.md` carries the MII terms, its bound and the receive distances | IEEE 802.1AS-2020 11.3.2, 8.4.3 |

**The constant at 100 Mb/s.** The correction is `(90 + 2 + 1) x 40 ns + 2 x 20 ns + 10 ns` = **3770 ns**, against 426 ns on GMII.

It lands on the registered launch of frame octet 0's low nibble, the first symbol after the start-of-frame delimiter, which is the timestamp measurement plane of IEEE 802.1AS-2020 11.3.2 and 8.4.3. The pad oracle in `gptp_txts` grades that independently, inside 11 ns.

The fix sits in the observer and the ledger, and needs nothing from the fabric gPTP engine, so it stands for a Mark II port that keeps hardware timestamping in fabric.

**No GMII behaviour moves.** The generated GMII chain and its manifest are untouched. The AX7101 1x1 route of this head passes its record: see [How to validate](#how-to-validate).

**Regression.** `make -C tb/verilator/gptp_txts run-mii` runs the closed loop on the MII shape at both 80 MHz and 100 MHz MAC system clocks. Without the fix it fails at `launch: an isolated exchange completes`; `mutants.py` keeps that as the control `mii_observer_ignores_ready`, with three more for the first-symbol term, the transmit tick and the history guard.

**The plane does not need a link event.** After every reset and flash with the Arty on its current link it measured peer delay within seconds, and `make -C tb/verilator/milan_dp gptp` publishes peer delay with the link up from reset and never toggled. Earlier readings of `GPTP_PDELAY` = 0 went with a link partner whose follow-ups never reached the MAC; see the record on #829.

## Authoritative references

- IEEE 802.1AS-2020 11.3.2, 8.4.3: timestamp measurement plane
- IEEE 802.1AS-2020 11.2, 10.2: asCapable and synchronization
- Milan v1.2 4.2.6.1.1: `neighborPropDelayThresh`
- IEEE 802.3 22.2.3: MII nibble order
- `docs/design/GPTP_PLANE.md`, "The 100 Mb/s MII shape" and "The board's own latency corrections"
- `docs/integration/BOARD_PORTING_AX7101.md` section 6: measuring a port's latency
- DP83848 datasheet, SNLS250E: T2.4.2, T2.5.2, T2.6.1, T2.9.2

## How to get into the same state

```sh
git fetch origin
git switch 829-mii-gptp
git submodule update --init gptp-processor protocol-processor
```

## How to validate

```sh
make -C tb/verilator/gptp_txts              # both shapes, then every planted control
make -C tb/verilator/gptp_shadow
make -C tb/verilator/gptp_plane
make -C tb/verilator/milan_dp gptp
python3 sw/litex/test_gptp_tx_timestamp.py
cd tests && behave
python3 scripts/lint_rtl.py --check
git diff --check "$(git merge-base dev HEAD)" HEAD
bash scripts/run_all_suites.sh <logs> --wait
```

Expected result / pass criteria: every command exits 0, and `gptp_txts` prints a mean reconstruction error inside 1.754 ns on the MII shape and 1 ns on GMII.

Evidence on this head:

| Gate | Result |
|---|---|
| Full suite sweep, four shards | 65 of 65 suites, 2,192,417 checks, 0 in-suite failures. Shard 1's first run failed `gptp_shadow`'s process-cleanup lifecycle test on a heavily loaded host, with its RTL checks and controls passing; the shard rerun passed 17 of 17, and that test passed four more times alone on this head and four on `dev` |
| `behave` | 508 scenarios, 2330 steps, 0 failed |
| Builder legs 0 and 1, `--require-rv32` | rc 0 and rc 0, tree clean after; one gate not run in each leg, as on `dev` |
| `lint_rtl.py --check` | PASS, 89 at ratchet 89 |
| `docs_check`, `gen_toc --check`, `check_gptp_docs` | rc 0 |
| `git diff --check` against the merge base | rc 0 |
| AX7101 1x1 route, recipe of `PP_SHADOW_BASELINE_RECIPE.md`, against `route-1x1` | PASS, rc 0 |

| AX7101 1x1 figure | Record | This head |
|---|---:|---:|
| LUT | 52012 | 51994 |
| FF | 53707 | 54101 |
| Slice | 15780 | 15841 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 27 |
| DSP | 13 | 13 |
| WNS, worst corner | +0.440 ns | +0.236 ns, floor +0.030 |
| WHS, worst corner | +0.036 ns | +0.036 ns, floor 0 |

WNS fell by 0.204 ns against the record, inside the gate's tolerance. Only the one shipping directive ran, so the route is judged with `--shipping-selection`, not on its three-directive set.

Bench, on the Arty at 100 Mb/s, on a bench branch this head is carried on:

| Check | Clause | Result |
|---|---|---|
| asCapable, sync to the bench grandmaster, 10 min 40 s | IEEE 802.1AS-2020 11.2, 10.2 | Held throughout, grandmaster the bench's, Announce 1/s and Sync 8/s on the capture |
| Peer delay under the bench's tap compensation | Milan v1.2 4.2.6.1.1 | 650 to 654 ns |
| One stream connection with the reference peer | Milan v1.2 5.5; IEEE 802.1Q-2022 35 | 460,354 frames on the capture at 7999.8/s, no sequence break; `FRAMES_RX` and `TIMESTAMP_VALID` 459,823, no late, early or mismatched frame; Talker Advertise and Listener declarations on the wire |

## Known limitations / out of scope

- **The calibration is not here.** The Arty's stamp correction is a board fact, not this fault. A measured 1509 ns sum and a runtime correction go with #583, as separate commits on the bench branch.
- **Without that correction this head does not reach asCapable through a tap.** Direct to the switch it reads peer delay 748 to 756 ns, 45 ns inside the bound.
- **The bench figures were taken under an inline tap and a compensation.** The tap's own transit is about 860 to 930 ns, above the 800 ns bound by itself, so the run wrote extra egress to bring the delay to 650 ns. That leaves the synchronized offset wrong by about 230 ns, as measured on the same capture. It proves the plane follows; it does not prove the offset.
- **One check is owed with the tap out.** True pair written, peer delay near zero, asCapable and sync. It needs a person at the bench.
- **The split is assigned, not measured.** No arrangement of one tap clock can measure it.
- **No other link speed is qualified.** At 10 Mb/s the same octet takes 800 ns and this correction is wrong.
- **The engine's state stays unreadable.** `dbg_busy_o` stays open at `milan_datapath.sv`: publishing it costs logic on the AX7101 image.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied, the Arty's on the bench branch described above
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
