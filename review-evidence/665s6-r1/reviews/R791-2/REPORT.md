[R791] NEGATIVE - exact head 526f937cde45e3a591fb3b9484ffdcaddbdfa144

# R791-2: internal cleared-context review of PR #853 (#665 S6a, the placement switch), round 2

- Head `526f937cde45e3a591fb3b9484ffdcaddbdfa144`, tree `e57b34a1f1d150cca37c2ffa8fb42001f05192ae`. The PR targets `dev-soft-core`.
- Source base `a9d69c77`. Round 1 head `6584b7bf`. The delta reviewed is `6584b7bf..526f937c`: 8 commits, 23 files, +688/-250.
- Authority, read in this order:
  - AGENTS.md and CONTRIBUTING.md;
  - issue #665's body and the S6 task card (issuecomment-6712890110);
  - the [A10] S6 round 1 ruling (issuecomment-6715535566), and the S6b rulings (6716584453, 6717765106) where they touch S6a;
  - the delta and its history;
  - the evidence branch at `1f33e530` (`review-evidence/665s6-r1/author-r2`).
- I applied the delta and every named round 1 finding at its cause before I read either round 1 report.

## Verdict summary

Every finding of both round 1 reviews is fixed as its verification step requires. I re-ran each reviewer probe that was given, and each holds at this head:

- the units in the two port names, carried through every binding with no ratchet exclusion;
- the builder comment and the 175 pin-control figure;
- the tap's drop count. The leg fails 3 checks on round 1's RTL and passes 66 of 66 at head;
- the CDC check, which admits the held bus only through the `u_fw_req` multiplexer. Its 12 plants, my round 1 R1-R3 and 7 new plants of mine are each refused.

The all-fabric identity holds on all six shapes. My own dump at head equals the a9d69c77 base on every digest. The placement figures match the raw Vivado reports.

One finding is open, so the verdict is NEGATIVE:

- **R791-2-F1 (MINOR, Conformance and Docs).** Ruling 6715535566 item 5 says to state, where `f0-f4` is defined, that it is ruled dead. `syn/ooc/pp_placement.py` still does not say so. The handoff records that this was left out on purpose. No other ruling moves the item, and the task card gives `pp_placement.py` to this lane.

The other lenses (RTL, Robustness and Tests) are clean at this head. Nothing else blocks.

## Findings

### R791-2-F1 MINOR - Conformance, Docs - `syn/ooc/pp_placement.py:14`, `:43` (and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192`) - the ruled-dead `f0-f4` placement is still presented as live where it is defined
- **Authority/evidence:**
  - [A10] ruling issuecomment-6715535566, item 5: "`pp_placement.py` `f0-f4` (item 6): ruled dead. Say so where it is defined. It is removed at the flip (S13), together with the all-fabric placement."
  - S6 task card item 6 gives `pp_placement.py` to this lane. The S6b rulings (6716584453, 6717765106) move the Python idiom gate, but not this item. So item 5 still sits with S6a.
  - At head, `PLACEMENTS = ("all-fabric", "f0-f4", "full-split")` (`:14`) and the `f0-f4` branch of `limits()` (`:43`) carry no such statement. The module docstring doesn't either. `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:192` still describes `f0-f4` as a selectable measurement population, with a recipe at `:212-215`.
  - The author's handoff (section 5) and REVIEW READY comment (issuecomment-6717994137) record the omission as deliberate. The PR body states the ruling's outcome, but the code does not.
- **Impact:**
  - A reader of the population table or the baseline recipe can select or extend a placement the maintainer ruled dead. The ruled decision lives only in an issue comment and the PR body.
  - AGENTS.md section 2: a future cold reviewer must be able to rebuild the decision from the repository.
- **Required outcome:** where `f0-f4` is defined in `pp_placement.py` (at `PLACEMENTS`, or the `f0-f4` branch), a comment states that `f0-f4` is dead and is removed together with the all-fabric placement at the flip. Optionally, the recipe page's `f0-f4` row says the same.
  - Under the owner's comment rule (2026-10-15), the source comment cites `#665` and states the behaviour and the reason.
  - It names no stage label such as "S13", no lane and no comment ID.
  - For example: `# f0-f4 is dead (#665): the firmware owns every control protocol, so this population is removed with the all-fabric placement at the flip.`
- **Verification:**
  - Read `pp_placement.py` at the fixed head.
  - The placement self-test still passes. That is `python3 syn/ooc/pp_baseline.py --selftest`, which imports `pp_placement_selftest`.
  - A scan of the delta finds no lane label, round or comment ID.

### Suggestions (optional, no lens effect)

- **R791-2-S1 (Tests): runts during a full FIFO.** `hdl/milan/KL_ctrl_split.sv:184-191`.
  - Reviewer arm 1 makes `last_kept_r` also record a frame that ends at beat 0, a runt. It survives the leg (receipts/tap-mutant-1.log), because no runt is offered while the FIFO is full.
  - A MAC delivers no frame shorter than 60 bytes, so this is low value. A one-beat frame in the full-FIFO phase of `check_tap_drops` would hold it.
- **R791-2-S2 (Tests): the datapath's own drop wiring.** `hdl/milan/milan_datapath.sv:10107` (`ctrl_split.rx_drops_o -> pp_rx_drops_w -> PP_DIAG[15:8]`).
  - The split leg probes `u_dp.pp_rx_frames_w` and `pp_tx_frames_w` (`tb_split_top.sv:364-365`), but not `pp_rx_drops_w`. A tie-off or swap of that wiring would survive.
  - The tap is proven on `u_tap`. A probe that the datapath's `pp_rx_drops_w` reads 0 after `[RX]` would at least bind the net.
- **R791-2-S3 (Docs): labels left in docs pages.** The pages still carry the lane label and comment IDs that the source comments dropped:
  - `docs/ENDSTATION_BUILDER.md:1073` ("#665 F-INT PR 2");
  - `docs/design/MAILBOX_SPLIT.md:1332` ("#665 F-INT PR 2"), `:1378` ("ruling 6088423771, decision 1"), `:1401` ("ruling 6410169666 item 1") and `:1754` ("comment 6554243203");
  - `docs/design/SPLIT_CONTROL_MEMORY.md:4`, `:167`. These may predate this PR.

  The owner rule covers source comments, so these are not RESIDUE. For consistency, "(#665)" would replace the lane label, and the reason would replace each ID.
- **R791-2-S4 (Tests, cosmetic): bench net names.** `tb/verilator/milan_dp/tb_split_top.sv:102`, `:202`. The nets `pub_idle_slope`, `d_idle_slope`, `fw_pt_offset` and `d_pt_offset` keep unitless names while the ports they bind now carry units. These are not boundaries, so no ratchet reads them.
- **R791-2-S5 (Tests, readability): a confusing CDC message.** `tb/verilator/milan_dp/split_cdc_check.py:178` (`label_of`). A flop is named by its Q net's first alias. So the window plant reports `output m_ctr_ans_data_o (sys) reads m_ctr_ans_data_o (dp)`, which reads as an output reading itself. Printing the flop's non-port alias, or its cell, would make the message unambiguous.
- **Note, not a finding: an out-of-lane reformat.** `scripts/check_solution_docs.py:184` reformats the pre-existing `Interrupt` `PortGroup` into fewer lines. This keeps the file under the long-module ratchet after the lane's own addition, and behaviour is unchanged (`check_solution_docs.py` passes at head). This is a formatting change outside the lane's own lines, so the PR body could say so.

## Round 1 findings at this head

| Finding | Status | Evidence at `526f937c` |
|---|---|---|
| R791-F1 (MAJOR): two boundaries hide their unit | **Fixed** | `i_ctl_pub_idle_slope_bps` (`milan_datapath.sv:714`) and `i_ctl_pt_offset_ns` (`:731`). Also `m_pub_idle_slope_bps_i`, `m_fw_pt_offset_ns_i`, `d_pub_idle_slope_bps_o` and `d_pt_offset_ns_o` on `KL_mbx_cdc`, through `milan_soc.py` and `tb_split_top.sv`. The old names occur nowhere in the tree. No naming exclusion was added: no file under `scripts/` names an `i_ctl_` port except the solution-docs port group. `measure_naming.py --check` PASS (95 candidates, all recorded), `--selftest` 66/66 (receipts/naming-check.log, naming-selftest.log). Hosted `docs-gates-0` **success** at the exact head (receipts/hosted-check-runs.tsv). |
| R791-F2 (MAJOR): firmware boundary red twice | **Fixed** | The builder comment no longer names the firmware's tree (`endstation_builder.py:4424-4426`). `sw/firmware/ctrl/README.md:255` gives 175, the only edit under `sw/firmware/` in the whole PR. My round 1 probe, re-run by me at head, reports **0 unclassified** and **the self-test's 175 = README 175** (receipts/ctrl-boundary-probe.log). Hosted `firmware-boundary` and `firmware-verilator` were still in progress at my last poll. |
| R791-F3 (MINOR): tap tuples and declaration encoding untested | **Fixed** | `check_tap` (`sim_split.cpp:522`) on `u_tap` (`tb_split_top.sv:368`) covers 6 accepted classes and 5 refusals. The `[PUB]` check pins ADVERTISE = 1. My round 1 mutants T1, T2 and D1, re-run by me, are each **CAUGHT** by a named check. E1-E3, G1, G2, C1 and W1 survive as stated; ruling items 1-2 give them to S6b (receipts/r791-1-split-reviewer-mutants.log). |
| R791-F4 (MINOR): drop counter cannot count | **Fixed** | `drop_p_w = ff_overflow_w & last_kept_r` (`KL_ctrl_split.sv:184-191`, `:232`). It is aligned with verilog-axis `axis_fifo.v:260-303`, whose `overflow_reg` is registered on the dropped frame's last beat, the same edge that updates `last_kept_r`. My checks: head leg 66/0, "108 offered, 65 handed out, 43 counted lost" (receipts/split-leg-head.log). Round 1's RTL (blob `69217fab`) gives **3 failures**, the burst, the conservation and the saturation (receipts/oldtap-run.log). The author arm "kept at its second beat" is caught. My arms 0, 2 and 3 are caught; arm 1 is S1 above (receipts/tap-mutant-*.log). The wrapper's identical defect has no Issue yet (pending manager duty below). |
| R791-F5 (MINOR) = R792 T-1 (MINOR): CDC exemption too broad | **Fixed** | `HELD_FLOP`/`GATE` (`split_cdc_check.py:77-78`), `gated()` (`:146`), resets as sinks (`:73-74`) and clock pins (`:239`). `--selftest` 13/13 with sv2v v0.0.12 and Yosys 0.66, 253 sinks (receipts/split-cdc-selftest.log). My round 1 R1-R3 are refused (receipts/r791-1-cdc-plants.log). My 7 new plants (control clean; swapped mux inputs, an AND gate, another dp level, pulse OR level, another flop through a gated mux, and `m_fw_send_i` folded into the data) are all refused (receipts/cdc-extra-plants.log). The docstring and `MAILBOX_SPLIT.md:1432-1442` claim only what the tool checks. Every input of both primitives (`cdc_handshake.sv:27-35`, `cdc_pulse.sv:22-27`) is a sink or a clock pin. |
| R792 D-1 (MINOR): stale pages | **Fixed** | `MAILBOX_SPLIT.md:828-833`, `MARK_II_AREA_PLAN.md:423-425`, and `CLOCK_DOMAINS.md:244-245`, whose two new rows I checked against `milan_soc.py:3120-3121`, `KL_mbx_cdc.sv:242,272-275,383` and `KL_mbx_cdc_window.sv:72,129`. `sw/firmware/ctrl/plat/README.md:137` stays in S2b's tree, as R792 routed it. |
| R791-F6 / R792 R-1 (RESIDUE): labels and comment IDs in source | **Fixed** | A scan of every added non-doc line in `a9d69c77..526f937c` finds no `F-INT`, lane, round, reviewer or comment-ID token. The only matches are byte "lane" words and hex constants. |
| R791-F7 / R792 R-2 (RESIDUE): REBOOT item; PR body | **Fixed** | `MAILBOX_SPLIT.md:1752-1756` names S11 and the `reboot_req_i` tie. The PR body's limitations state the outcome of each ruling. |
| R792 R-3 (RESIDUE): counter word | **Fixed** | `sim_split.cpp:382`: "its STREAM_START counter". |

## Delta beyond the findings

- **Three gates red at `6584b7bf` that the hosted job never reached.** I ran each locally at head and each passes (receipts/gates_summary.txt and gate_*.log):
  - `check_port_contracts.py` and `--selftest` pass;
  - `check_py_idiom.py` and `--selftest` pass;
  - `measure_test_evidence.py --check` and `--selftest` pass;
  - `check_solution_docs.py`, `check_cpp_idiom.py` and `check_sv_idiom.py` also pass.

  Hosted `docs-gates-0/1/2` succeed at the exact head.
- **The two new reader classifications** (`scripts/measure_test_evidence_readers.py:245-252`) are accurate and follow their siblings' wording:
  - `split_mutants.py` reads RTL text only to anchor a plant. Its verdict is the named FAIL line of a completed run.
  - `split_cdc_check.py` reads the netlist structurally. Its only implementation-derived inputs are the allow-list names `fw_r`/`u_fw_req` and the `m_`/`d_` port prefixes, and the plants defend both. Neither tool takes an expected value from RTL text.
- **The dropped `timeout=1800`** (`split_mutants.py:132-141`) is sound:
  - `docs/development/CODE_QUALITY.md:1762` counts host wall-clock deadlines (3 allowed).
  - The leg itself is cycle-bounded: `Tb::sys`, the 8-cycle `access`, and `wait_for` (`sim_split.cpp:83-118`, `:262`). So a mutant cannot hang it.
- **New port docs** (`a8ab58de`) use no unit words. I checked every new port for a unit-bearing meaning. None has one besides the two renamed buses: the `*_wait` ports are levels, and the rest are fields and events.

## Clean results, with evidence (per lens)

```text
[R791] PASS RTL - hdl/milan/KL_ctrl_split.sv:173-191,232 against third_party/verilog-axis/rtl/axis_fifo.v:217,260-303; hdl/milan/mailbox/KL_mbx_cdc.sv:47-451 and KL_mbx_cdc_window.sv:31-46 (renames, port docs, dest_req rationale); hdl/milan/milan_datapath.sv:373-385,711-781,5638,9964-10021 - drop count aligned with the FIFO's registered overflow on the dropped frame's last beat, a refused frame or runt never counted, saturation kept; renames bind 1:1 across the four binding files with no old name left; no logic change on the all-fabric path, confirmed by my own six-shape identity dump equal to a9d69c77
[R791] PASS Robustness - hdl/milan/KL_ctrl_split.sv:184-191 under tb/verilator/milan_dp/sim_split.cpp:565-606 (108-frame burst past 4,096 bytes, refused frames into a full FIFO, a 320-frame burst to saturation); split_mutants.py:132-141 with sim_split.cpp:83-118,262 - full-FIFO, refused-while-full, saturation and reset paths held by checks; no new unbounded wait after the wall-clock removal
[R791] PASS Tests - tb/verilator/milan_dp/sim_split.cpp:500-606, split_mutants.py:38-129, split_cdc_check.py:250-297 - head leg 66/0; round 1 tap RTL 3 failures; author arm and reviewer arms 0/2/3 caught; round 1 T1/T2/D1 caught; CDC selftest 13/13 plus my R1-R3 and 7 extra plants refused; S1-S2/S4-S5 are optional
```

`Conformance` and `Docs` are UNCLEAN at this head because R791-2-F1 is open under both. The rest of each was applied and is clean:

- **Conformance:**
  - ruling items 1-4 and 6-7 are honoured. `reboot_req_i` stays tied 0, the two-placement simulation, census and CDC CI job are left to S6b, and the link is left to S9;
  - the placement figures are a measurement and are not gated;
  - the all-fabric identity is against a9d69c77, not dev.
- **Docs:** checked at head:
  - `MAILBOX_SPLIT.md:828-833,1392-1399,1426-1442,1752-1756`;
  - `MARK_II_AREA_PLAN.md:423-425`;
  - `CLOCK_DOMAINS.md:244-245`;
  - `tb/verilator/milan_dp/README.md:109,1117-1160`;
  - `sw/firmware/ctrl/README.md:255`;
  - `REGISTER_MAP.md:2456`, whose `PP_DIAG[15:8]` definition the split tap now satisfies;
  - the PR body.

## Measurements and identity, checked against receipts

- **All-fabric identity.** My `placement_identity.py --dump` at head (sv2v v0.0.12, Yosys 0.66, `--jobs 3`, 7:58 wall, 2.1 GB peak) gives six digests. They equal:
  - the author's a9d69c77 base (`--compare` rc 0, receipts/ident-compare-r791.log);
  - my round 1 reviewer's independent a9d69c77 base dump (`R791-1/receipts/identity-base.log` on the evidence branch).

  So the head equals a9d69c77 without relying on any author dump. The author's head and base JSONs also agree shape for shape. Only `tree_head` differs.
- **Split placement.** The figures were read from the raw author reports in `author-r2/receipts/vivado/`:
  - `alinx_ax7101_utilization_place.rpt`: Slice LUTs 34228 (53.99 %), Slice Registers 45234, Slice 14383 of 15850 (90.74 %), BRAM 93, DSP 5;
  - `alinx_ax7101_timing_place-summary.rpt`: WNS -0.021 ns over 22 endpoints, WHS -0.248 ns over 431;
  - `run.txt`: clone `526f937c`, Vivado rc 0, 0 ERROR, 0 CRITICAL WARNING.

  These are post-placement estimates, not routed, and a measurement rather than a gate.
- **The evidence packet.** All 1,122 files under `review-evidence/665s6-r1` match `MANIFEST.json` `published_sha256`, with 0 unlisted (receipts/evidence-manifest-check.txt). The evidence commit `1f33e530` carries no git signature. Integrity rests on the manifest.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R791-2-F1 open) | ruling 6715535566 items 1-7; S6 task card; S6b rulings; `syn/ooc/pp_placement.py:14,43`; PR body limitations; identity against a9d69c77 | R791-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| RTL | CLEAN | `KL_ctrl_split.sv:173-191,232` vs `axis_fifo.v:217,260-303`; `KL_mbx_cdc.sv`, `KL_mbx_cdc_window.sv`, `milan_datapath.sv` delta; six-shape identity | R791-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| Robustness | CLEAN | `sim_split.cpp:565-606`; `KL_ctrl_split.sv:184-191`; `split_mutants.py:132-141` with the bounded harness | R791-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| Tests | CLEAN | split leg 66/0; old-tap 3 failures; split mutants (author arm, reviewer arms, round 1 T1/T2/D1); CDC selftest 13/13, R1-R3, 7 extra plants; naming, port-contract, py-idiom, test-evidence gates | R791-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |
| Docs | UNCLEAN (R791-2-F1 open) | `MAILBOX_SPLIT.md`, `MARK_II_AREA_PLAN.md`, `CLOCK_DOMAINS.md`, milan_dp README, firmware README, `REGISTER_MAP.md:2456`, PR body; `PP_SHADOW_BASELINE_RECIPE.md:192` | R791-2 | 526f937cde45e3a591fb3b9484ffdcaddbdfa144 |

What the delta leaves untouched keeps its round 1 verdict (R791-1 at `6584b7bf`). That covers the builder gates 23m/23n, the SoC split tables outside the renames, the population tool's logic (refactored here, no change to what it decides) and the export identity.

## Real limits

- **No manager source bank runs at this head, and I claim none.** The source-head execution evidence is:
  - my focused runs listed above;
  - the author's published receipts;
  - the hosted checks.
- **Hosted.** At my last poll, 36 contexts had succeeded, 1 was skipped (physical gPTP), and 18 were still in progress. Those 18 include `firmware-boundary`, `firmware-verilator`, `firmware-aecp-mutants` and some Verilator shards. None had failed or been cancelled (receipts/hosted-check-runs.tsv). The manager owns hosted acceptance (`rtl-fast`, `verilator-suites`, `yosys-portability`). This PR targets `dev-soft-core`, so no act run applies.
- **Not re-run by me.** I relied on the author's receipts and the fact that this delta does not change their inputs for these:
  - the full 22-arm `split_mutants.py` campaign (I ran one author arm, plus my own arms);
  - `split_population.py --check/--selftest`, refactored only here;
  - the gateware export identity;
  - the builder and firmware banks;
  - the full sweep;
  - the Vivado placement;
  - the publication census.
- **Not dumped by me.** The a9d69c77 base was not dumped this round. My round 1 base dump stands in for it.
- **No physical runs.** Physical calibration NOT RUN. No hardware run. Field skips are not hardware proof.
- **Where the probes ran.** My probes ran in a byte-identical copy of this clone (`cp -a`, HEAD `526f937c`, clean status) under the packet's `scratch/`, which is not published. The review clone was restored and verified afterwards. `write-tree` equals the HEAD tree, there are 0 untracked or ignored entries (two `__pycache__` directories my gate runs created were removed), and the submodule gitlinks are as at HEAD (receipts/clone-integrity.txt).

## Pending manager duties

- **The wrapper's drop count.** Open the public Issue for `KL_pp_shadow.sv`'s identical uncounted drop (`drop_p_w = fw_valid_w & ~fw_ready_w` under `DROP_WHEN_FULL`). R791-F4 asked for it, and the author's round may not post it. Until then, the all-fabric `PP_DIAG[15:8]` contradicts `REGISTER_MAP.md:2456`.
- **Hosted firmware jobs.** Confirm that `firmware-boundary` and `firmware-verilator` finish green at the exact head. They are R791-F2's hosted half.
- **R791-2-F1.** Route it to this lane's next round. It is a comment in `pp_placement.py`, plus optionally the recipe page's row.
- **The S2b staleness.** Carry `sw/firmware/ctrl/plat/README.md:137` (R792 D-1's note) to S2b or S6b.
- **The merge candidate.** At the merge turn, build and validate the current-dev-soft-core merge candidate, from source base a9d69c77 and S6b's merge of this head. That is distinct from this source-head review.

## Receipts (all at head 526f937c; paths relative to this packet)

- `receipts/gates_summary.txt`, `receipts/gate_*.log`: port contracts, py idiom, test evidence, solution docs, cpp/sv idiom.
- `receipts/naming-check.log`, `receipts/naming-selftest.log`: R791-F1.
- `receipts/ctrl-boundary-probe.log`/`.rc`, `scripts/ctrl_boundary_probe.py`: R791-F2.
- `receipts/split-leg-head.log`/`.rc`, `receipts/oldtap-build.log`, `receipts/oldtap-run.log`/`.rc`: R791-F4.
- `receipts/tap-mutant-{0..3}.log`/`.rc`, `scripts/tap_reviewer_mutants.py`: reviewer drop-count arms.
- `receipts/author-arm-kept2.log`/`.rc`: one author arm, re-run.
- `receipts/r791-1-split-reviewer-mutants.log`/`.rc`, `scripts/split_reviewer_mutants.py`: R791-F3.
- `receipts/split-cdc-selftest.log`/`.rc`, `receipts/r791-1-cdc-plants.log`/`.rc`, `scripts/cdc_plants.py`, `receipts/cdc-extra-plants.log`/`.rc`, `scripts/cdc_extra_plants.py`: R791-F5 / T-1.
- `receipts/ident-head-r791.json`, `receipts/ident-dump-head.log`/`.rc`/`.time`, `receipts/ident-compare-r791.log`/`.rc`, `receipts/author-ident-base-a9d69c77.json`: identity.
- `receipts/evidence-manifest-check.txt`, `receipts/hosted-check-runs.tsv`, `receipts/clone-integrity.txt`.
- Local absolute paths in three receipts (`ctrl-boundary-probe.log`, `ident-dump-head.time`, `split-leg-head.log`) are redacted to `<scratch>`, `<packet>`, `<clone>`, `<tools>` and `~`. Nothing else in them was changed.

R791-2 FINISHED
