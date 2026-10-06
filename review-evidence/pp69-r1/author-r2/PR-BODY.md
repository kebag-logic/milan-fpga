[A550]

Closes #69

The #69 lane (assignment: #69 comment 6010216843; round 2: comment 6016201199). Branch `pp69-if-seam`, cut from `main`
`e6a759de`, with `main` `86a7b0c5` merged at `cb730a2`. Head: `75c4eee`.

P-N-AVB-INTERFACES, the redundancy seam, is threaded through the fabric build rather than closed by decision. The top exposes it as
`N_AVB_IF_P` (1 or 2, default 1). At 1 no cell changes anywhere, and the OOC 1x1 delta is **0 LUT, 0 FF**. At 2 the seam is keyed
in ADP, on every transaction, in the registry (each row's port, and the depth: P-N-CONTROLLERS rows per interface) and in the
AVB_INTERFACE counter rows. Three suites build it at 2, and the real top is linted at 2 on every run of `tb/pp_top`.

Round 2 fixes the three findings of review R512-1, each in the RTL or the checks rather than in the documents alone:
- **F1.** A command now cancels every live probe it supersedes, one per cycle, and a superseded probe's late report touches
  nothing.
- **F2.** The top-level checks now grade where the registry port comes from.
- **F3.** The registry depth is keyed per interface.

| Commit | What |
|---|---|
| `1673e56` | RTL: `protocol_processor_top.sv`, `KL_aecp_notify.sv`; the trailing context of two ADP patches; F01.5, REQ-SCP-003, 02, 06, the integrator guide and diagram 21 |
| `3b6a25b` | The checks: `tb/adp_engine` section IF, `tb/aecp_notify` sections PT and CK, `tb/pp_top` section IF and `if-guards`; 09 section 8.9 |
| `a8f7983` | The controls: nine `if-` arms in the ADP campaign, seven arms in `notify_mutants.py` |
| `c3cac3a` | The suite READMEs: sections, builds and mutation records |
| `d723574` | A failing control for every new check: seven more `if-` arms, two AVB_INTERFACE counter arms, PT1 folded into PT2 |
| `cb730a2` | Merge of `main` `86a7b0c5` (#134, #22) |
| `3323904` | Round 2, F1 and F3: the registry depth per interface and every superseded probe cancelled; `tb/aecp_notify` sections PD and CA; REQ-SCP-003, REQ-AEM-016, F01.5, 06, the integrator guide, 09; the round-end line of two arms refreshed |
| `fc9bc43` | Round 2, F2: `tb/pp_top` IF3 and IF3b run REGISTER and DEREGISTER after a frame on the other interface; README and 09 |
| `75c4eee` | Round 2: a failing control for every new check (ten for `tb/aecp_notify`, the reviewer's P1 and P2 at the top) and the records |

## 1. The seam

**Top.** `parameter int unsigned N_AVB_IF_P = 1` (F01.5 P-N-AVB-INTERFACES). The top refuses any value other than 1 or 2 at
elaboration, with a message naming it. The count reaches:
- `KL_adp_engine` `.N_IF_P (N_AVB_IF_P)`, replacing the literal `1`, and the F08.4 timer map;
- `rx_if_index_i[1:0]`, a new top input with default `2'd0`. It is read with the frame's last byte, and only above 1. It is carried
  to the header beat and drives every transaction's `interface_index`. A one-interface parent leaves it unconnected.

**Registry.** With `N_IF_P` above 1, `KL_aecp_notify` keys three things.
- *Port.* Each row stores its port, the AVB interface its REGISTER arrived on. REGISTER and DEREGISTER walk for the whole Milan
  v1.2 5.3.4.2 tuple {Entity ID, MAC, port}. The port is `rgy_port_i`, which the top latches from the ingress interface of the
  command the engine is running.
- *Depth.* The registry holds P-N-CONTROLLERS rows per interface (round 2, F3). Row r is {index, port}, so r = index × N_IF_P
  + port, and a REGISTER claims a row of its own port. One interface's rows run out without touching the other's, so a
  two-interface build holds Milan's minimum on each interface.
- *Probes.* A row's index is its 4-bit CA owner and its timer owner-tag entry. Those therefore keep P-N-CONTROLLERS values, and
  no port, parameter or tag range changes. An expiry is decoded to its row from the tag's index and the slot's port. The rows of
  one index, one per port, take turns at the CONTROLLER_AVAILABLE probe, and none starts within three cycles of a cancel.
  `KL_pp_originator` takes a cancel at once, or one cycle late behind the single response that can hold its action lane, so a
  cancelled exchange's last report lands while no probe of its owner is live.
- *Cancels (F1).* One command from a controller registered on both interfaces cancels both of its live probes, one per cycle.
  A response or failure is taken only for its owner's live probe, so a superseded probe's late report touches nothing.
- At 1 the port, the turns and the cancel bits are not generated, and the one-interface expressions are unchanged.

**Counters.** The Table 5.22 GET_COUNTERS rows are keyed per interface. AVB_INTERFACE 1 gets the slot after CLOCK_DOMAIN 0, so it
has a one-second window of its own. The processor's own counters (snapshot words) are not keyed: they count the shared trunk and
engines, and keying them would change the register map. The Milan Table 5.1 AVB_INTERFACE counters are the integrator's
(GAP-05).

**Not keyed, by design** (the banners, F01.5 and REQ-SCP-003 name each one):
- the MAC trunks (no egress index);
- the class-D levels;
- the SRP engine;
- the availability monitor, which matches {Entity ID, MAC} on any interface, because a command on either proves the controller
  alive;
- the GET_AVB_INFO and GET_AS_PATH pushes, on AVB_INTERFACE 0;
- the side-port snapshot and `adp_next_avail_index_o`, which show interface 0.

## 2. No change at count 1

**Yosys statistics.** `stat -json` after `hierarchy -check; proc; opt_clean`, for all 42 tops of `syn/yosys/run.sh`:
- Main `86a7b0c5`, the round-1 head `cb730a2` and this head: every cell count of every module is identical, with two derived
  module names masked.
- Round 1 against main: the top gains one port (`rx_if_index_i`) and `KL_aecp_notify` one (`rgy_port_i`, 2 bits), and the
  derived names of `KL_adp_engine` and `KL_aecp_notify` change because both instances now pass the count.
- Round 2 against `cb730a2`: 40 of 42 statistics files are byte-identical. The other two, `KL_aecp_notify` and the top, differ
  only in wire counters: wires 6030 to 6046, wire bits 56480 to 56609. These are the generate wires that the one-interface branch
  drives with constants or with the old expressions.

**OOC 1x1**, by the parent's recipe for the standalone shadow (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`): parent dev `28f9666f`
with the 148 patch, shape ax7101, Vivado 2026.1, `xc7a100t-fgg484-2`.

| `KL_pp_shadow` 1x1 | LUT | FF | RAMB tiles | DSP |
|---|---:|---:|---:|---:|
| main `86a7b0c5` | 23,179 | 19,779 | 17.5 | 8 |
| head `75c4eee` | 23,179 | 19,779 | 17.5 | 8 |
| delta | **0** | **0** | 0 | 0 |

The cell census (`baseline_cells.tsv`) is byte-identical at both, as are the parameters and the chparam list. The hierarchy
report is identical past its dated header, and the image list differs only in the measurement directory.
`syn/ooc/pp_resource_gate.py check --endpoint ooc-1x1` passes at both. Round 1 measured `e6a759de` against its own head at
23,211 LUT and 19,777 FF at both ends, also a 0 delta.

## 3. Two interfaces

Each new check fails under at least one planted control (section 5).

- **`tb/adp_engine`, second build `interfaces`**: `KL_adp_engine` at `N_IF_P=2`, IF0 to IF9. These cover per-interface advertise
  machines, byte-exact ENTITY_AVAILABLE and ENTITY_DEPARTING per interface, restarts per interface, and ingress keyed by
  interface.
- **`tb/aecp_notify`, third build `interfaces`**: `KL_aecp_notify` at `N_IF_P=2`, `N_CTRL_P=2`, 19 checks.
  - PT2 to PT7: the registry tuple.
  - CK1 to CK5: the AVB_INTERFACE counter rows.
  - PD1: each interface holds `N_CTRL_P` entries of its own; the third REGISTER on either port is refused.
  - PD2: each row arms its own TIME_LIMITED and monitor slots under its index's owner tags.
  - PD3: an expiry is decoded to its row from its tag and slot.
  - CA1: R512-1's probe P3. E is registered on both ports and both probes are out; one command from E cancels both.
  - CA1b: a TIME_LIMITED drain's cancel and a command's cancel in the same cycle are both sent.
  - CA2: the cancelled exchanges' late failures and responses touch nothing.
  - CA3: the rows of one CA owner take turns, and a failure is the live probe's.
  - CA4: the settle. The next probe of the owner starts at least four cycles after the cancel, and the cancelled exchange's
    response, two cycles after the cancel, is not taken for it.
- **`tb/pp_top`, seventh build `interfaces`**: the real top at `N_AVB_IF_P=2`, with `rx_if_index_i` driven by the bench.
  - IF1: each interface advertises.
  - IF2: ENTITY_DISCOVER restarts the receiving interface's machine.
  - IF3 and IF3b (round 2, F2): the MAC TX is held, so a lock-change push to the controller cannot leave, and the notification
    block holds the engine's command path. The controller's REGISTER, and later its DEREGISTER, come in on interface 1, then a
    frame on interface 0, and only then does the TX resume. The REGISTER still makes interface 1's entry: the next lock reaches
    the controller at sequence_ids 0 and 2, and the unlock at 1 and 3. The DEREGISTER removes interface 1's entry: the last
    unlock reaches interface 0's entry at 5, not interface 1's at 3.
- **`tb/pp_top` `if-guards`**: the real top is linted clean at 1 and 2, and refuses 0 and 3 by name.

## 4. Docs

- The banners of `KL_aecp_notify.sv` and `protocol_processor_top.sv`.
- `docs/architecture/01_overview.md` section 7, P-N-AVB-INTERFACES and P-N-CONTROLLERS: the depth is keyed, and a two-interface
  build holds Milan 5.3.4.2's minimum on each interface.
- `docs/00_MILAN_COMPLIANCE_REVIEW.md`: REQ-SCP-003's Arch cell names what is keyed and what is not. REQ-AEM-016 is scoped to
  P-N-CONTROLLERS rows per AVB interface, at P-N-AVB-INTERFACES 1 and 2.
- Also: 02; 06 sections 6.6 and 7 and the storage table; 09 section 8.9; the integrator guide; diagram 21; the three suites'
  READMEs. Each states what the checks grade.

## 5. Before the RTL edits, and the controls

Every edit was first drafted in a scratch copy. Each base line it removes or modifies was searched with `git grep -n -F`, as the
full line and stripped, across `tb/**/*.patch` and the exact-text tables (`tb/**/*.py`).
- Round 1: 42 searches, 2 with a match: the trailing context line of two ADP patches, refreshed.
- Round 2: 136 searches, 2 with a match. Both are the round-end line `if (em_ix_r == CIX_W_C'(N_CTRL_P - 1)) ...`, which
  becomes `N_ROW_C`. Its users are `tb/pp_top/mutations/fanout-never-ends.patch` and `notify_mutants.py`'s `ROUND_END`. Both
  were refreshed; at one interface `N_ROW_C` equals `N_CTRL_P`.

Every arm plants, checked without simulating: patches through `git apply --check` from the tree root, and exact-text arms through
each driver's own `plant()` or counting rule.

| Tree | Patches and `plant()` arms | Other exact-text anchors |
|---|---:|---:|
| `cb730a2` | 506 of 506 | 96 of 96 |
| head `75c4eee` | 518 of 518 (506 + 12 new notify arms) | 96 of 96 |

The 96 other exact-text anchors are, by each driver's own rule:
- 70 arms of `tb/acmp_talker/retry_mutants.py`, plus its 2 BFM-probe anchors;
- 20 of `tb/pp_top/gsi_mutants.py`;
- 3 of `tb/srp_admission/mutants.py`;
- 1 of `tb/pp_top/name_wr_mutant.py`.

That is 94 arms and 2 probe anchors.

**Planted identity.** 138 arms at `cb730a2` plant into a file round 2 changes. For 133 of them, the planted base with round 2's
diff applied equals the planted head byte for byte. The other five overlap a round-2 hunk:
- two plant on the refreshed round-end line itself;
- two are equal once the diff is applied with fuzz;
- one is equal but for the `N_CTRL_P` to `N_ROW_C` sizing hunk next to its anchor.

All five are the same design at one interface.

The round-2 controls (`tb/pp_top/notify_mutants.py`), each KILLED:

| Arm | Planted | Fails |
|---|---|---|
| `cancel_one_per_command` | a cancel not sent in its cycle is dropped (R512-1's P3) | CA1, CA1b |
| `report_fail_ignores_probe` | a failure taken for its owner's last row, live probe or not | CA2, CA3 |
| `report_rsp_ignores_probe` | a response likewise | CA2 |
| `owner_turns_dropped` | a probe no longer waits for its owner | CA3, CA4 |
| `settle_dropped` | no settle after a cancel | CA4 |
| `depth_shared` | a REGISTER claims any free row | PD1, PD2, PD3, CA1, CA2, CA1b |
| `depth_not_keyed` | P-N-CONTROLLERS rows in all | PD1, PD2, PD3, CA1, CA2, CA1b, CA3, CA4 |
| `registry_tag_port_bits`, `monitor_tag_port_bits` | an owner tag from the row's port bits | PD2 |
| `expiry_port_dropped` | an expiry decoded to the port-0 row | PD3, CA1, CA3, CA4 |
| `rgy_port_from_latest_frame` | R512-1's P1: the registry port from the latest frame's interface | pp_top IF3, IF3b |
| `dereg_matches_other_port` | R512-1's P2: DEREGISTER matches the other port | pp_top IF3b |

Round 1's controls all stay KILLED:
- in ADP: `if-ingress-*`, `if-egress-collapsed`, `if-pdu-index-collapsed`, `if-gm-*`, `if-link-*`, `if-aidx-reset-by-index`, and
  the `if-top-*` arms on pp_top IF and `if-guards`;
- in `notify_mutants.py`: `port_not_*`, `avb_counter_*` and `rgy_port_tied_zero` (pp_top IF3 and IF3b).

## 6. Validation

Base `cb730a2` against head `75c4eee`, on clean extractions, every command rc 0 and never piped, with the pinned Verilator
5.050.

**Processor gates**

| Gate | base | head |
|---|---|---|
| `scripts/run_suites.sh` | 1,028,263 checks, 0 failing | 1,028,271 checks, 0 failing |
| `scripts/lint_hdl.sh` | rc 0 | rc 0, same log |
| `syn/yosys/run.sh` | rc 0 | rc 0 |
| `make check` | rc 0 | rc 0 |
| `scripts/gen_matrix.py --check` | rc 0 (94 rows, 0 untested) | rc 0 |

Suite records are identical except `aecp_notify`, which goes from 56 to 64 (its third build, 11 to 19) with the total.

**Campaigns.** Every driver whose campaign builds a changed file, at both sides. Records are compared per arm and per
`results.json` row.

| Campaign | base | head | Records |
|---|---|---|---|
| `tb/pp_top/notify_mutants.py` | 65 of 65 | 77 of 77 | 62 identical; 12 head-only arms; the three goldens gain the new checks; round 1's #69 arms move in text, two in their check sets |
| `tb/pp_top/d3_mutants.py` | 110 of 110 | 110 of 110 | 116 identical |
| `tb/adp_engine/mutants.py` | 62 of 62 | 62 of 62 | 58 identical; 4 move in IF3's text only, same failing checks |
| `tb/pp_top/aecp_mutants.py` | 67 of 67 | 67 of 67 | 67 identical |
| `tb/pp_top/aecp_dispatch_mutants.py` | 44 of 44 | 44 of 44 | 44 identical |
| `tb/pp_top/acmp_mutants.py` | 33 of 33 | 33 of 33 | 37 identical |
| `tb/pp_top/gsi_mutants.py` | 20 detected | 20 detected | 44 identical |
| `tb/pp_top/name_wr_mutant.py` | killed | killed | 6 identical |
| `tb/pp_top/ctr_mutants.py` | 18 of 18 | 18 of 18 | 18 identical |
| `tb/maap/mutants.py` | 32 of 32 | 32 of 32 | 32 identical |

**Parent consumer set of 17**, at parent dev `28f9666f` with the 148 and 22 patches. No other parent patch is needed:
`N_AVB_IF_P` defaults to 1 and `rx_if_index_i` to `2'd0`. All 17 are rc 0 at both sides.
- 11 logs are identical (01, 03 to 08, 10, 11, 13, 17).
- 12 pp_shadow, 14 nvm quick, 15 milan_dp and 16 render have identical tallies and PASS counts.
- 02 py idiom has +61 lines, the new arms.
- 09 xvlog: PASS at both, 0 findings, equal to the ratchet the 22 patch sets. The logs differ only in the pinned processor
  commit.

**Interfaces added**, and nothing else:
- the top's `N_AVB_IF_P` and `rx_if_index_i`;
- `KL_aecp_notify`'s `N_IF_P` and `rgy_port_i`.

Round 2 adds none, and changes no register map.
