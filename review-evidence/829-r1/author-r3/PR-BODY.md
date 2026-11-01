[A725d]

## Contents

- **[Round 3](#round-3)** — What the two reviews of `2d534bec` found and how each item closed.
- **[Round 2](#round-2)** — What the two reviews of `4cda0aa0` found and how each item closed.
- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Round 3

Both reviews of `2d534bec` were NEGATIVE on one shared MINOR, and every earlier finding stayed closed. No RTL changed in this round.

Gate 1h read raw text, so a binding or default that was commented out, in a block comment or in a dead `ifdef` passed it. With the octet binding cut that way, the plane would lose every frame behind a green gate.

**The fix.** The gate now reads what the build's front end reads: `sv2v --pass-through` on the defines and include directories that `syn/yosys/run.sh --emit milan_datapath` states. Comments and dead arms are gone before the gate looks, and no model of that layer is left in the gate. The same front end stands behind `syn/ooc/dp_srcs.py`, and all four builder jobs already install it. No `sv2v` on the path is a refusal, not a stand-down.

| Item | What closed it | Verified by |
|---|---|---|
| R761-2 F1, R762-F9: gate 1h read comments and dead arms | `_datapath_as_built` and `_datapath_shape_findings` in `sw/builder/test_builder.py`; 37 planted cuts and 6 equal spellings the gate must accept | The gate prints `37/37 cuts rejected, 6/6 equal spellings accepted`. Run on this head, both reviewers' own plant scripts report 17 of 17 and 14 of 14 refused, with the shipped text accepted |
| R761-2 RES1, R762-2-R1 | The `eth_rst` sentence moved to the end of the comment in `milan_soc.py`; the parsed program is identical | Read; `ast` comparison |
| R761-2 RES2 | The comment over `DATAPATH_SHAPE_WIRING` separates the two cuts' effects: the octet binding loses every frame, the tick binding is wrong by 2976 ns | Read |
| R761-2 RES3 | The lifecycle bullet below reads "See #833." | Read |
| R761-2 RES4 | The suite's `README.md` paragraph re-wrapped | Read |
| R762-2-R2 | The published round 2 handoff cites `KL_gptp_gmii_launch.sv:100` for the clause; it is at `:101`. Corrected in this round's handoff. The published packet is not regenerated here | Read |

**The controls.** For each of the two bindings: cut, tied to its default, scaled, through a no-op, on another parameter, bound twice, in a line comment, in a block comment, tied with the old text in a trailing comment, in a dead `ifdef`, and live only where the build does not define `SYNTHESIS`. For each default: moved, a `localparam`, shadowed beside the plane, in a line comment with a live default below, in a block comment with a live default below, and in a dead `ifdef` with a live default in its `else`. For the plane: renamed, a second plane, and the two bindings crossed. The gate must also pass a comment beside a binding, a binding in a live `ifdef`, and a comment inside a default, so it reads code and not a spelling.

**What the gate still does not see.** It parses and does not elaborate, so a `defparam` or a generate arm that never elaborates stays outside it. Its own comment says so.

Not taken, for their own Issues if wanted: R761-2 S1 and R762-2-S1, the same gap in gate 1g, which reads Python text; R762-2-S2, an elaboration of the plane's effective parameters; R761-2 S2, a route of `dev` to attribute the routed effect.

## Round 2

Both reviews of `4cda0aa0` were NEGATIVE, and both confirmed the MII logic correct. No RTL behaviour changed in this round.

**How the first report's "documentation gates rc 0" came to be false.** Round 1 ran three steps of `.github/workflows/docs.yml`, `docs_check`, `gen_toc --check` and `check_gptp_docs`, and reported them as the documentation gates. `check_doc_style.py` and `check_cpp_idiom.py` are steps of the same workflow and were never run. Every step of that workflow has now been run from the workflow's own list on clean clones of the head, and a step with no rc of 0 and no stated reason fails the check that produced the table below.

| Finding | What closed it | Verified by |
|---|---|---|
| R761-F1, R762-F1: style gate red | `GPTP_PLANE.md` and `CHANGELOG.md` reworded, facts unchanged | `check_doc_style.py` and `--selftest` rc 0 |
| R761-F2, R762-F2: idiom ratchet red | `-Wall -Wextra` on the MII build's own flag group; ratchet stays 0 | `check_cpp_idiom.py` rc 0, `build without warnings: 0 <= 0` |
| R761-F3, R762-F7: GMII `ready` called a constant | Corrected in `milan_soc.py`, `GPTP_PLANE.md`, `CHANGELOG.md`, `KL_gptp_gmii_launch.sv` and this PR; "cannot move" removed from `test_builder.py` | Read against the generated chain and the AX7101 export: a flop set to 1 and cleared by `eth_tx`'s reset, which `maceth_tx`'s reset follows by two clocks |
| R761-F4, R762-F8: fragment check could not fail on MII | The check reads 45 octets in the shape's own clocks; new control `mii_delta_forced_not_measured` | That defect stays green under the old check, and fails `fragment: the observer refused it, by measurement` under the new one |
| R761-F5, R762-F3: PHC arm missed the window's early end | A load now lands on the first symbol, and the arm reads the guard's reload; controls at 170 and 202 | Guard 188 or less fails the first-symbol load's own result. Guard 189 to 202 is caught by the reload check. 203 passes |
| R761-F7, R762-F5: check's name false on MII | The name states 1.754 ns on MII and one nanosecond on GMII; controls follow | All 13 controls caught under the new names |
| R762-F4: no gate held the datapath's shape wiring | Builder gate 1h, `test_gptp_datapath_carries_the_launch_shape`, with 7 planted cuts | The real cut of either binding in `milan_datapath.sv` fails it by name. At that head it was a text gate; see [Round 3](#round-3) |
| R761-F6, R762-F6: figures that did not trace | 10 controls at `4cda0aa0`, 13 at this head, 14 on the bench branch; checksum comparison published | The comparison receipt reads 126 of 126 |
| R761 RES1, R762-R4 | "at 80 MHz and at 100 MHz" in `sim_main.cpp`'s banner | Read |
| R762-R1 | `eth_rst` also clears the PHY stage on GMII and does not reach it on MII: the observer's port comment and `milan_soc.py` | Read against `gen_mac_tx_model.py` |
| R762-R2 | The digital bound covers two shapes; 100 Mb/s calibration stays open under #583: `GPTP_PLANE.md`, `KL_gptp_shadow.sv`, this PR | Read |
| R762-R3 | Range 631 to 675 ns added to the bench table | Polled values of the three runs |
| R761 S3 | IEEE 802.1AS-2020 11.3.9 is the timestamp point, as the RTL banners already said. 11.3.2 only lists message types, so it is gone from this PR | Read in the standard |
| R761 S6 | `mutants.py` removes the two binaries that hold a control's defect | Absent after a full run |

Not taken, for their own Issues if wanted: R761 S1 and S2 are answered to the maintainers as findings; R761 S4 and S5, and R762 S1, S3 and S4, were not assigned.

## Status

GREEN locally at this head on every `docs.yml` step that can run off the hosted runners and on `gptp_txts`, hosted runs and re-review pending — `829-mii-gptp` -> `dev`, head `cfb79922`. The full sweep is `2d534bec`'s: this round changes one builder test, one code comment and one paragraph of a guide.

The Arty's acceptance was shown on a bench branch: this PR's logic at `4cda0aa0`, the #583 clock ruling, and a runtime correction that is not in this PR. Rounds 2 and 3 change none of that logic. The reasons are under [Known limitations](#known-limitations--out-of-scope).

## Linked Issue / roles

Relates to #829
Relates to #583

Executor: `[A725d]`, continuing `[A725c]`, `[A725b]` and `[A725]`
Internal cleared-context reviewer: `[R761]`
External reviewer: `[R762]`

## Description

**The fault.** On the 100 Mb/s MII port the launch observer read one octet per clock, while `phy.sink` holds each octet for two.

The failing signal is `KL_gptp_gmii_launch.cand_r`. It falls at seam cycle 7 of the first frame, on the delimiter check, where the held preamble is read as the next octet.

No launch record came, so the ledger never drained, the engine's response claim held the next Pdelay_Req at the queue head, and the event queue filled.

The same bench at GMII timing passes at every cycle, with the delimiter at cycle 7 where the check expects it.

**What the first report said wrongly.** "Sends no frame" came from a capture on another link. On the Arty's own link gPTP frames do leave; what failed was timing them. `GM_LOSS_RECOVERY` and the plane's reset seal are not involved.

**The change.**

| Piece | Change | Why |
|---|---|---|
| `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv` | Counts an octet where `valid` and `ready` coincide | MII holds each octet for two clocks. GMII's `ready` is a flop that is 1 from the first clock after reset, and the observer's own reset covers that reset, so no octet is held there |
| `hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv` | Adds the first-symbol term to the reconstruction, and scales the PHC history guard to the window | The observer counts octet 0 on the edge that registers its high nibble, one clock after the reference plane |
| `KL_gptp_shadow.sv`, `milan_datapath.sv` | Carry `ETH_TICK_NS_P` and `ETH_CYC_PER_OCTET_P` to the two above | Defaults are the GMII shape |
| `sw/litex/milan_soc.py`, `sw/builder/endstation_builder.py` | State the MII shape per PHY model, and the builder's datapath parameters read the same table | One source for the shape |
| `sw/litex/gen_mac_tx_model.py`, `tb/verilator/gptp_txts/` | Convert the MII stages of the product's chain and run the closed loop on them | The regression below |
| Documents | `GPTP_PLANE.md` carries the MII terms, its bound and the receive distances | IEEE 802.1AS-2020 11.3.9, 8.4.3 |

**The constant at 100 Mb/s.** The correction is `(90 + 2 + 1) x 40 ns + 2 x 20 ns + 10 ns` = **3770 ns**, against 426 ns on GMII.

It lands on the registered launch of frame octet 0's low nibble, the first symbol after the start-of-frame delimiter. That is the message timestamp point of IEEE 802.1AS-2020 11.3.9, and 8.4.3 is the clause that corrects a timestamp to it. The pad oracle in `gptp_txts` grades that independently, inside 11 ns.

The fix sits in the observer and the ledger, and needs nothing from the fabric gPTP engine, so it stands for a Mark II port that keeps hardware timestamping in fabric.

**No GMII behaviour moves, and the netlist is not shown unchanged.** The generated GMII chain and its manifest are untouched, and both reviews proved the observer and ledger equivalent to the base at GMII defaults with `ready` high. The head's observer does take a `ready` connection the base has not got, so the AX7101 export differs from the base by that one line. The 1x1 route passes its record: see [How to validate](#how-to-validate). No route of the base exists, so the routed effect of this PR alone is unknown.

**Regression.** `make -C tb/verilator/gptp_txts run-mii` runs the closed loop on the MII shape at both 80 MHz and 100 MHz MAC system clocks. Without the fix it fails at `launch: an isolated exchange completes`; `mutants.py` keeps that as the control `mii_observer_ignores_ready`, with six more on this shape: the first-symbol term, the transmit tick, the measured distance, and the history guard at three values. That makes 13 controls at this head with the six GMII ones. It was 10 at `4cda0aa0`. The 14 once reported belong to the bench branch, whose four extra controls are the writable pair's.

**The plane does not need a link event.** After every reset and flash with the Arty on its current link it measured peer delay within seconds, and `make -C tb/verilator/milan_dp gptp` publishes peer delay with the link up from reset and never toggled. Earlier readings of `GPTP_PDELAY` = 0 went with a link partner whose follow-ups never reached the MAC; see the record on #829.

## Authoritative references

- IEEE 802.1AS-2020 11.3.9: event message timestamp point, the first symbol after the delimiter
- IEEE 802.1AS-2020 8.4.3: generation of event message timestamps, and the correction to the reference plane
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
python3 sw/builder/test_builder.py --gates test_gptp_launch_shape_follows_the_phy,test_gptp_datapath_carries_the_launch_shape
cd tests && behave
python3 scripts/lint_rtl.py --check
python3 scripts/check_doc_style.py
python3 scripts/check_cpp_idiom.py
git diff --check "$(git merge-base dev HEAD)" HEAD
bash scripts/run_all_suites.sh <logs> --wait
```

Expected result / pass criteria: every command exits 0, and `gptp_txts` prints a mean reconstruction error inside 1.754 ns on the MII shape and 1 ns on GMII.

Evidence on this head, `cfb79922`:

| Gate | Result |
|---|---|
| `docs.yml`, every `run:` step on clean clones of this head | 64 steps rc 0; 31 hosted-only or package-install steps not run, each with its reason in the receipt |
| Builder legs 0 and 1, `--require-rv32`, as `docs.yml` runs them | rc 0 and rc 0, 1 and 16 arms not run. Gate 1h ran in leg 1: `37/37 cuts rejected, 6/6 equal spellings accepted` |
| `make -C tb/verilator/gptp_txts` | 95 of 95 in each of its three runs; 13 of 13 controls caught |
| `check_doc_style.py`, `check_cpp_idiom.py` | rc 0 as `docs.yml` steps |
| `git diff --check` against the merge base | rc 0 |
| The reviewers' plant scripts, on a clean clone of this head | 17 of 17 refused; 14 of 14 refused and the shipped text accepted |
| Hosted workflows and the local replica | Not run: they need the pushed head |

Evidence on `2d534bec`, not repeated, because this round changes no RTL and only one builder test:

| Gate | Result |
|---|---|
| Full suite sweep, four shards | 65 of 65 suites, 2,192,435 checks, 0 in-suite failures, no shard rerun |
| `behave` | 508 scenarios, 2330 steps, 0 failed |
| Builder legs 0 and 1 where the SoC can elaborate | rc 0 and rc 0, 1 arm not run in each. Tree clean after |
| `lint_rtl.py --check --self-test` | PASS, 89 at ratchet 89 |
| `gptp_shadow`, `gptp_plane`, `milan_dp gptp`, `gptp-lat`, `test_gptp_tx_timestamp.py` | rc 0 each |
| AX7101 1x1 route, recipe of `PP_SHADOW_BASELINE_RECIPE.md`, against `route-1x1`, at `4cda0aa0` | PASS, rc 0. Not repeated: this round's RTL edits are comment-only |

The AX7101 route ran at `4cda0aa0`. Round 2 changed only comments in the RTL and in `milan_soc.py`, and that is shown rather than assumed: the preprocessed RTL, the converted plane and the exported SoC top with comments removed are each byte-identical to `4cda0aa0`'s. So the route was not repeated. Round 3 touches no `hdl/` file, and `milan_soc.py`'s parsed program is unchanged.

| AX7101 1x1 figure | Record | `4cda0aa0` |
|---|---:|---:|
| LUT | 52012 | 51994 |
| FF | 53707 | 54101 |
| Slice | 15780 | 15841 |
| RAMB36 / RAMB18 | 74 / 27 | 74 / 27 |
| DSP | 13 | 13 |
| WNS, worst corner | +0.440 ns | +0.236 ns, floor +0.030 |
| WHS, worst corner | +0.036 ns | +0.036 ns, floor 0 |

WNS fell by 0.204 ns against the record, inside the gate's tolerance. Only the one shipping directive ran, so the route is judged with `--shipping-selection`, not on its three-directive set. The record's baseline is an older `dev`, so this delta is not all this PR's, and slices are 15841 of 15850.

A second route, on the bench branch at `b474b534` with the writable logic present and its key off, matches `4cda0aa0`'s at all 126 implementation checksum lines. That compares the two routes with each other and says the bench key off moves nothing. It does not compare this PR with `dev`. The comparison is published as a small text receipt, with each route's head and what it covers.

Bench, on the Arty at 100 Mb/s, on a bench branch carrying this PR's logic at `4cda0aa0`:

| Check | Clause | Result |
|---|---|---|
| asCapable, sync to the bench grandmaster, 10 min 40 s | IEEE 802.1AS-2020 11.2, 10.2 | Held throughout, grandmaster the bench's, Announce 1/s and Sync 8/s on the capture |
| Peer delay under the bench's tap compensation | Milan v1.2 4.2.6.1.1 | 650 to 654 ns row means, range 631 to 675 ns |
| One stream connection with the reference peer | Milan v1.2 5.5; IEEE 802.1Q-2022 35 | 460,354 frames on the capture at 7999.8/s, no sequence break; `FRAMES_RX` and `TIMESTAMP_VALID` 459,823, no late, early or mismatched frame; Talker Advertise and Listener declarations on the wire |

## Known limitations / out of scope

- **The calibration is not here.** The Arty's stamp correction is a board fact, not this fault. A measured 1509 ns sum and a runtime correction go with #583, as separate commits on the bench branch.
- **Without that correction this head does not reach asCapable through a tap.** Direct to the switch it reads peer delay 748 to 756 ns, 45 ns inside the bound.
- **The bench figures were taken under an inline tap and a compensation.** The tap's own transit is about 860 to 930 ns, above the 800 ns bound by itself, so the run wrote extra egress to bring the delay to 650 ns. That leaves the synchronized offset wrong by about 230 ns, as measured on the same capture. It proves the plane follows; it does not prove the offset.
- **One check is owed with the tap out.** True pair written, peer delay near zero, asCapable and sync. It needs a person at the bench.
- **The split is assigned, not measured.** No arrangement of one tap clock can measure it.
- **The digital bound covers these two shapes only.** 100 Mb/s physical calibration stays open under #583. At 10 Mb/s the same octet takes 800 ns and this correction is wrong.
- **`gptp_shadow`'s process-cleanup lifecycle test can fail under heavy load.** Its cause is not established, and it also fails on `dev`. See #833.
- **Queued frames leave the MII pads 480 ns apart**, against the 960 ns of IEEE 802.3 4.4.2. LiteEth counts that gap in clocks, so this predates this PR. Bench stream frames came from the peer, and the Arty's own frames on the captures were about 4.8 us apart at the closest.
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

