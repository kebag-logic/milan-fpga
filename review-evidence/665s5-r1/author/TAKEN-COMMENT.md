[A702] TAKEN

Lane S5, the F2-F5 timing hooks on the target core, as assigned in issuecomment-6513150371.

Branch: `665-s5-hooks`, from `dev-soft-core` `5b5f4336`. The PR targets `dev-soft-core`.

Authoritative references:
- FR_NFR.md 3.4.1, 3.4.2 and the H-ADP, H-DISC, H-ACMP, H-AECP, H-NOTIFY, H-COUNTERS, H-MAAP and H-SRP rows; NFR-SCOUT-03.
- The bound: T_svc = 20 ms. Each hook is graded against min(T_svc, 10 % of its family's ceiling), per issuecomment-6495692075: SRP 18 ms; ACMP, discovery, AECP, notifications, MAAP and ADP 20 ms. The margin to each normative timeout is recorded.
- The clocks, per issuecomment-6508196970: the split CPU's product clock is 50 MHz and its bus 100 MHz. The 100 MHz CPU figures are a labelled variant, never presented as the product's.
- #664's ruling of 2026-10-06, item 4: ordering is tested apart from the budget.
- ARCHITECTURE_HW_SW_SPLIT.md section 5; MAILBOX_SPLIT.md; SPLIT_CONTROL_MEMORY.md; S2's `tb/verilator/ctrl_service_budget` and S3's `tb/verilator/ctrl_split_boot` and `sw/firmware/ctrl/plat`, all as merged.

Interpreted scope:
A new sibling harness, `tb/verilator/ctrl_service_hooks/`. It runs S3's platform image (`ctrl_plat_image.py`), linked unmodified, on S2's test SoC. That SoC is S2's split CPU with its instruction cache, `CtrlMemory`, and `KL_mbx` with each face commit acknowledged at the contract's bound. This harness adds the platform's CSR window and UART.

It measures at the shipping shape (1x1, one interface) and the largest (8x8, two interfaces, the ledgered `platform-8x8-two-interfaces` point). Each point runs at the 50 MHz product CPU clock and at the labelled 100 MHz variant.

Each hook is measured in target cycles, from its RX_HEAD commit or triggering event to its last TX commit. It is measured idle and under the composed load: full rings, bounded ingress, SRP churn, flash activity and delayed events. Each hook's ordering obligation is graded on its own, apart from the budget.

Each hook gets two plants, a late service and an ordering defect. Each is a scratch copy of the firmware tree, never an edit, and each must fail with its own words. A hook that misses only at 50 MHz is reported as held for the owner's clock decision, with its figures.

S2's and S3's harness files are imported read only and not edited, because S2b and S4 both edit S2's testbench, SoC and build. This lane edits only `tb/` and test READMEs. Any firmware instrumentation the hooks need is a STOP, not an edit.

Validation plan:
- the new harness's portable self-test and grader mutants;
- the 16 plants, each caught by its own words;
- the hook runs at both points and both clocks;
- `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`;
- S2's harness at both points, and its `--self-test`;
- `python3 sw/builder/test_builder.py --require-rv32`;
- the TSN stack boundary gate;
- the docs gates;
- rtl-fast's bdd-conformance (`cd tests && behave`).

No RTL changes, so the full sweep and Vivado are not run.

Blockers: none yet.

Watched:
- H-COUNTERS. Its push needs the face block's counter-change event and its CTR window answered, and S2's SoC holds both idle. This harness drives them as a labelled answering-face arm, in test code. If the push cannot be reached without instrumenting the firmware, that hook STOPs.
- The firmware base. S2b's firmware cuts are not merged, so every figure is on `dev-soft-core` as it is.
