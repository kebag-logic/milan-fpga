[A731] REVIEW READY
Commit: 992c3d7bb37f4ade0b151c17d718baed0e119753 (branch `839-boot-source-address`, base dev 604899c08ff1cd1830e1dd08b733109ef852400c; pushed with the PR)

Changed:
- `hdl/milan/milan_datapath.sv`: the station-MAC pair's own sequencing (`mac_addr_seq`, each half's first write since reset, read off the CSR slave's write handshake; `milan_csr` unchanged); a transmit gate that holds the processor's control lane (SRP, ADP, ACMP, AECP), MAAP, the AAF talkers and the CRF talker at frame start until both halves are written; and a control-lane stamp of octets 6 to 11 from the CSR, because the processor's SRP encoder builds the PDU into its slot before it is offered. The gPTP plane is not held: its ROM carries the same station MAC (builder `platform.mac_address`, refused when zero or group). Acceptance 1's first option: the fix holds each transmitter; the firmware boot order is unchanged.
- New `bootsa` leg in `tb/verilator/milan_dp` (`sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_probes.vlt`): the shipping 1x1 datapath booted through `milan_init()`'s own stage order with the firmware's own `configure_fabric()` and `entity_advertise()` compiled in, every frame graded at `m_axis_mac_tx` up to and past the first ENTITY_AVAILABLE, then two boots writing one half alone. `bootsa_mutants.py`: seven planted controls.
- Four harnesses that never wrote the station MAC now do, as `configure_fabric()` does (the render leg also after its mid-test resets).
- Docs: `REGISTER_MAP.md` `MAC_ADDR_LO/HI` rows, `BAREMETAL_FIRMWARE.md`, `TESTING.md`, the milan_dp README, `CHANGELOG.md`. No field, address, reset value or top-level port changes; no submodule change.

Validation (all at 992c3d7b, each on a clean clone of the head):
- `scripts/run_all_suites.sh <logs> --wait --shard k/4`, four shards: 65 of 65 suites, 0 failed, 0 timed out, 2,192,475 checks, 0 in-suite failures. `bootsa`: `checks: 40 failures: 0`; gptp and gptp-lat 210 of 210 each; `tdm8_render` 263 of 263.
- `make -C tb/verilator/milan_dp bootsa-mutants`: `8 checks: 8 PASS, 0 FAIL`.
- The head's leg against the base RTL: fails 9 of 40, first `#0 MSRP cycle 20198 source 000000000000 (before the MAC write)`.
- `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4` (k = 0..3), `test_ctrl_nvm.py --require-rv32`, `fw_rv32_selftest.py --require-rv32`, `tally_selftest.py`: all PASS (shard 1 `mutants: 523 of 523 caught`).
- `fw_coverage.py --selftest` and `--check`: `firmware coverage: PASS (30 files)`.
- `test_builder.py --require-rv32` (docs.yml's two legs) and `--require-elaboration --require-rv32` (elaborate.yml's two legs): all exit 0; the arms not run are listed by the builder with their reasons.
- `scripts/run_litex_sims.sh --selftest` and its three legs: 16 of 16; all eight members PASS.
- `cd tests && behave`: 508 scenarios, 2330 steps passed.
- Every `run:` step of `docs.yml`: 64 ran, all exit 0; 31 hosted-only steps not run, each with a stated reason.
- `syn/yosys/run.sh`, `scripts/lint_rtl.py --check --self-test`, `scripts/pp_srcs.py --check --selftest`, `git diff --check 604899c0 HEAD`: all exit 0.
- `scripts/docs_inventory.py --check`: not run; it is not in the tree at the base or the head.
- Area, out-of-context synthesis of `milan_datapath` (`syn/ooc/milan_datapath_ooc.tcl`, default 1x1 shape, base and head): LUTs 45,176 to 45,275 (+99), registers 40,222 to 40,233 (+11), block RAM and DSP unchanged, OOC WNS unchanged.

Acceptance criteria:
1. Met: from reset no frame carries 00:00:00:00:00:00 and every frame's source is the station MAC (831 frames graded: MSRP, gPTP, ADP, AECP, ACMP, MAAP, AAF, CRF); the first frame is MSRP at cycle 40112, after `configure_fabric()` completes the MAC at 40088. The fix holds each transmitter.
2. Met: the leg runs the firmware's real boot order past the first ENTITY_AVAILABLE; the defect as shipped (no hold, no stamp) fails it by `no frame carries the all-zero source address`, `no CSR-addressed transmitter starts a frame before the station MAC is written` and `every MSRP frame's source address is the station MAC`.
3. No new top-level port; the register-map change is the pair's sequencing only, documented on the `MAC_ADDR_LO/HI` rows. Needs a decision: the tree has no register-map generator (`REGISTER_MAP.md` is maintained by hand; the builder generates only the 0x680 group's reset words), and nothing generated changes.
4. Green in simulation: the firmware self-test, the builder, behave and the simulated boot runs (the `bootsa` boot and the LiteX SoC simulations). Not run: a hardware boot with a capture of its first frames; this lane has no bench access.

Open risks/questions:
- Items 3 and 4 as read above; until a maintainer accepts those readings the PR body says `Relates to #839`, not `Closes #839`.
- Rewriting the station MAC after boot is not atomic across the two words (a frame stamped between the two writes carries half of each); firmware writes the pair once per boot.
- The area figure is the out-of-context synthesis, not the routed shipping image.
