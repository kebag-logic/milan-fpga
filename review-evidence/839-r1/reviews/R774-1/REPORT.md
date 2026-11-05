[R774] NEGATIVE - exact head 992c3d7bb37f4ade0b151c17d718baed0e119753

External independent review, round R774-1, of PR #841 (issue #839) at exact head `992c3d7bb37f4ade0b151c17d718baed0e119753`, tree `06bd3e03aece23b59ff01ebd641d1f4e4515a840`, source base `604899c08ff1cd1830e1dd08b733109ef852400c` (ten commits). I rebuilt the task from AGENTS.md, CONTRIBUTING.md, the issue body and its public comments, the PR body, the linked register-map and firmware-boot documents, the diff and history, and the published area receipts. All five lenses were applied. When this pass started, no review findings had been published on the PR (only two review-start notices), so there are no prior findings to resolve or retain.

Verdict: NEGATIVE. The RTL fix is correct as far as I could probe it. One MINOR finding under `Tests` is still open: the transmit hold on three of the four held transmitters (MAAP, AAF, CRF) is shipped and documented, but no test can fail if it is removed. I planted that removal and it passes the leg 40 of 40. Two RESIDUE wording items follow.

## Findings

### F1 - MINOR - Tests - removing the hold on MAAP, AAF and CRF goes undetected

- Where: `hdl/milan/milan_datapath.sv:8817-8822` (the six gate assigns for MAAP, AAF and CRF); `tb/verilator/milan_dp/bootsa_mutants.py:63-87` (the mutant list); `tb/verilator/milan_dp/sim_boot_sa.cpp:547` (the early-start check).
- Authority and evidence:
  - AGENTS.md section 5 says to add self-checking tests for changed behaviour and to test ordering paths. The Tests lens says each new test must be able to fail for the defect it claims to detect.
  - The PR adds a hold on four transmitters. `docs/reference/REGISTER_MAP.md:414`, `docs/integration/BAREMETAL_FIRMWARE.md:114` and `:217`, `CHANGELOG.md` and the RTL comments all document that hold as a register-level guarantee. The leg's check "no CSR-addressed transmitter starts a frame before the station MAC is written" claims it.
  - In the firmware's real order, MAAP, AAF and CRF are enabled only after the MAC write (`milan_baremetal.c:1815`). So for those three the check cannot fail.
  - Probe: I removed only those three holds and kept the processor hold and the stamp (`receipts/probe_noxtra_rtl.diff`). The unmodified leg passes: `receipts/bootsa_noxtra.log`, `checks: 40 failures: 0`.
  - The behaviour itself is correct. I wrote a probe leg that enables MAAP, AAF (enable plus bypass) and CRF at reset release, before the MAC write (`receipts/probe_early_enable_leg.diff`):
    - At head it passes 40 of 40 (`receipts/bootsa_headearly.log`). Nothing leaves during the BIOS window. The first MAAP and CRF frames leave at cycles 40614 and 40622, right after the MAC write at 40608, with the station MAC. `A_TXARB_DIAG` reads 0.
    - On the mutant it fails 4 of 40 (`receipts/bootsa_noxtraearly.log`). The failing checks are the all-zero source address, a CSR-addressed transmitter starting early, and the MAAP and CRF source addresses: 11 frames with source 000000000000 before the MAC write.
  - No AAF frame left before cycle 3.2 M in either probe run, so the AAF hold is verified only by reading the RTL.
  - The README (`tb/verilator/milan_dp/README.md:1176`) and the PR body disclose that this order is not driven. Disclosing it does not give the shipped mechanism a test.
- Impact: a later edit could drop the hold on MAAP, AAF or CRF and every gate would stay green, while four documents keep claiming the hold.
- Required outcome: a boot or arm that enables MAAP, AAF and CRF before the station-MAC write and grades their frames. Plus a planted control that removes those three holds and must fail that arm by name. The AAF talker must actually offer a frame inside the held window, or the AAF part must say why that cannot happen.
- Verification: the new control fails by its named checks, and the clean leg still passes. `scripts/plant_noxtra.py` and `scripts/plant_early_enable.py` show the shape of both.

### R1 - RESIDUE - PR #841 body, stale "pending a maintainer" wording

- The PR body records "Maintainer decision (2026-11-05): both readings are accepted".
- Its Known limitations section still says "A maintainer decides whether that meets the item".
- The Definition of Done still says "3 and 4 as read above, pending a maintainer".
- Exact fix: replace both phrases with "accepted by the maintainer on 2026-11-05 (no register-map generator; no hardware capture yet, so this PR relates to #839)".
- This changes no measurement or verdict.

### R2 - RESIDUE - issue #839 REVIEW READY comment, area-run commit

- The comment says "Validation (all at 992c3d7b, each on a clean clone of the head)" and lists the area figure among those results.
- The receipt (`review-evidence/839-r1/author/receipts/area/AREA.md` at `1904ad85`) shows the synthesis ran at `8d2dfb65`.
- `git diff --stat 8d2dfb6547 992c3d7b` is only `tb/verilator/milan_dp_render/sim_tdm8_render.cpp`, which synthesis does not read. So the figure is valid at the exact head (`receipts/area_check.txt`).
- Exact fix: "Area at `8d2dfb65`, whose synthesis inputs are byte-identical to `992c3d7b` (the only later change is a render-harness .cpp)".

### S1 - SUGGESTION - `tb/verilator/milan_dp/sim_boot_sa.cpp:591-592`

- The shipping config declares a CRF output, and the leg graded 781 CRF frames.
- CRF is still not in the "frames were sent and graded" list. Adding it would turn a silent loss of CRF coverage into a failure.
- Optional.

## Per-lens results (artifact-specific)

```text
[R774] PASS Conformance - hdl/milan/milan_datapath.sv:3106-3115,8815-8822,8924-8942; hdl/common/csr/milan_csr.sv:1117-1145,1682-1683,2690; sw/firmware/milan_baremetal/milan_baremetal.c:1815-1834,1894-1914; sw/litex/boot_policy.py:43-49; sw/builder/endstation_builder.py:2677,3280-3300,3417-3421,5925-5941; sw/litex/milan_soc.py:857,995-1001; receipts/bootsa_head.log, bootsa_base.log, bootsa_headdump.log, bootsa_basedump.log, ports_base.txt, ports_head.txt - against issue #839 acceptance 1-4, IEEE 802.1AC-2016 11.1 and IEEE 802.1Q-2022 6.8.1 as quoted in the issue
```

What the Conformance pass found:

1. **Every transmitter is accounted for.** Exactly five sources reach `m_axis_mac_tx`: the processor, MAAP, AAF, CRF and gPTP. The first four are held. gPTP is not held: `KL_gptp_shadow` has no MAC input, and its source address exists only in the ROM.
2. **The pair's sequencing matches the CSR's own write commit.** `mac_addr_seq` keys on AWVALID and AWREADY, where AWREADY is `wr_fire`. That needs WVALID, `!b_valid` and `!sweep_busy`, the same conditions under which `mac_alo`/`mac_ahi` commit. The CSR and the sequencing share `axis_resetn`. In the SoC, `axis_resetn` comes only from the `milan_cd` system reset (`milan_soc.py:857`). The MAC reinit path resets `macsys`/`macdp`, not the datapath, so nothing besides the documented resets closes the gate again.
3. **The control-lane stamp writes octets 6 to 11 and nothing else.** The CSR packing is LSB-first, so wire octet 6 is `cfg_mac_addr[7:0]`. That matches `station_mac_be_w`, and the leg's expected address is computed independently, from the overlay's wire-order bytes.
4. **The held PDU is not damaged.** The first MSRP PDU, held and then released at head, is byte-identical (30 octets) to the base's unheld PDU except octets 6 to 11 (`bootsa_headdump.log` / `bootsa_basedump.log`).
5. **gPTP gets the same address as the firmware.** The gPTP ROM's `--mac` and the firmware's `MILAN_STATION_MAC_LO/HI` both come from `cfg.platform.mac_address`. The overlay's `adp.mac_address` is that value, and `_mac48` refuses zero and group addresses. So any config change moves both together.
6. **The leg reproduces the issue and the fix.** Head: 40 of 40; the first frame is MSRP at cycle 40112, after the MAC is complete at 40088. Base RTL: 9 of 40 fail, the first being `#0 MSRP cycle 20198 source 000000000000`. Both match the author's figures.
7. **No new top-level port.** There are 140 port declarations, identical at base and head.
8. **The accepted readings are stated in the PR body.** The PR says "Relates to #839" and no commit carries a closing keyword.

```text
[R774] PASS RTL - hdl/milan/milan_datapath.sv:3106-3115 (mac_addr_seq), 8806-8822 (gate), 8885-8942 (gasket output, ctl_sa_position, ctl_sa_stamp), 8832-8880 and 9083-9156 (arbiters); hdl/milan/KL_pp_shadow.sv:1519-1584 (TX packer); protocol-processor/hdl/packet_engine/KL_pp_tx_arbiter.sv:1-45; hdl/ieee1722/aaf/KL_aaf_packetizer.sv:506-552; hdl/ieee1722/crf/KL_crf_tx.sv:509; hdl/ieee1722/maap/KL_maap.sv:260-290; published area receipts util_base.rpt and util_head.rpt - clocks, resets, widths, handshake, watchdog, resources
```

What the RTL pass found:

1. **Clocking and handshake.** Everything is in the single `axis_clk` domain, so there is no CDC. `tx_sa_ok_w` only rises, and it gates valid and ready together at each source. A source therefore sees no transfer and holds its beat, the AXI-Stream rule is kept, and no arbiter is granted a stalled frame. `A_TXARB_DIAG` reads 0 in every head run, including the early-enable probe. The processor's internal arbiter and slot pool have no watchdog, so a multi-second hardware BIOS hold cannot truncate a frame.
2. **The stamp counter.**
   - Widths: `TX_SA_BPB_C`=8, `TX_SA_BEATS_C`=2, `TX_SA_IW_C`=2. The counter saturates at 2 and resets on `tlast` with handshake.
   - Packing: the processor packer emits full beats except the last (`KL_pp_shadow.sv:1519-1584`), and so does MAAP. Beat position therefore fixes octet position.
   - Downstream arbiters see only an unchanged handshake.
3. **AAF, CRF and MAAP addresses.** All three form octets 6 to 11 combinationally from `station_mac_i` on the beat they emit. A held first beat cannot carry a stale address.
4. **Feature-off builds.** With MAAP off, the tie-off moves to `maap_txs_tvalid_w`. With gPTP off, the stamped `ctlg2` lane passes through unchanged.
5. **Area.** The receipts read 45,176 to 45,275 LUTs (+99) and 40,222 to 40,233 registers (+11), F7 +115, F8 +5, BRAM and DSP unchanged. These match the PR's figures (`receipts/area_check.txt`).

```text
[R774] PASS Robustness - hdl/milan/milan_datapath.sv:3106-3115,8815-8822,8924-8942; hdl/milan/KL_pp_shadow.sv:323-328 (RX tap); receipts/bootsa_headearly.log (MAAP/AAF/CRF enabled before the MAC write); receipts/bootsa_head.log (the two pair-order boots) - invalid ordering, reset, backpressure, repeated writes, feature-off
```

What the Robustness pass found:

1. **Out-of-order enables.** When MAAP, AAF and CRF are enabled before the MAC write, they stay held and release whole, with the station MAC.
2. **Either half alone opens nothing.** Each pair-order boot passes.
3. **Reset during activity.** It resets the sequencing, the sources and the counter together.
4. **No RX back-pressure.** The processor's RX is a monitor tap that never drives ready, so a long TX hold cannot stall RX or gPTP.
5. **Repeated MAC writes** keep the gate open. Non-atomic rewrites are disclosed.
6. **A failed identity check** in `milan_init()` means the MAC is never written. The CSR-addressed transmitters then stay silent rather than send a zero address, and gPTP still runs. That is conservative and consistent with the issue.

I counted the untested early-enable order under `Tests` (F1), not here. The design behaves correctly on that path; only the test is missing.

```text
[R774] MINOR Tests - tb/verilator/milan_dp/bootsa_mutants.py:63-87, sim_boot_sa.cpp:547; receipts/bootsa_noxtra.log - F1 open (lens UNCLEAN). Examined clean in the same lens: sim_boot_sa.cpp, gen_boot_fw.py, Makefile:492-525,714-740,901-907, the four harness edits, receipts/bootsa_mutants_head.log
```

What was clean under Tests:

1. **The leg runs the firmware's real boot.** `gen_boot_fw.py` copies `configure_fabric()` and `entity_advertise()` from the firmware, makes exactly the two stated edits (each checked to apply once), and reads the stage order out of `milan_init()`.
2. **Expected values are independent.** The expected source address comes from the overlay's wire bytes.
3. **The precondition is checked.** The leg confirms the processor offered a frame before the MAC write.
4. **The author's campaign reproduces.** Rerun at head: `8 checks: 8 PASS, 0 FAIL`. The defect as shipped fails by the three names that acceptance 2 reads.
5. **The harness MAC writes mask nothing.**
   - Each writes the reset value (0) the register already holds, so the only RTL effect is opening the gate, which is the base behaviour.
   - The render leg's mid-test reset arms (T18 to T22) grade the listener and TDM side, not TX, so the hold cannot make them pass vacuously.
   - I checked every other datapath harness: each writes both halves. In the main leg, everything it observes on TX comes after its MAC write.

```text
[R774] PASS Docs - docs/reference/REGISTER_MAP.md:414-415; docs/integration/BAREMETAL_FIRMWARE.md:112-121,217; docs/testing/TESTING.md:277,406-421; tb/verilator/milan_dp/README.md (obj_bootsa row; section at 1114-1180); CHANGELOG.md; PR #841 body; issue #839 comments - against the RTL and the leg as read above
```

What the Docs pass found:

1. **The RTL and leg descriptions are accurate.** The MAC_ADDR rows describe the sequencing (either order, reads do not count, held until reset, non-atomic rewrite).
2. **The TESTING count is right.** "eighteen" commands and "eight" legs without data files add up: 18 − 8 `sim_nxn` − 2 `sid_move` = 8.
3. **No source-comment residue.** Searching the delta's added source comments for lane labels, round or reviewer IDs and comment IDs found nothing.
4. **No stale tracker.** No obsolete document is restored.
5. **Open wording items.** R1 and R2 are RESIDUE only and do not leave the lens unclean.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | RTL gate, sequencing and stamp; CSR write commit; firmware boot order; builder MAC path to ROM and firmware words; `bootsa` head/base/dump receipts; port lists | R774-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| RTL | CLEAN | `milan_datapath.sv` gate, stamp and arbiters; `KL_pp_shadow` packer; processor TX arbiter; AAF/CRF/MAAP framers; area receipts | R774-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| Robustness | CLEAN | early-enable probe at head; pair-order boots; reset and RX-tap analysis; identity-fail path | R774-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| Tests | UNCLEAN (F1 MINOR open) | `sim_boot_sa.cpp`, `gen_boot_fw.py`, `bootsa_mutants.py`, Makefile, four harness edits; mutant campaign rerun; no-extra-hold mutant survives | R774-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |
| Docs | CLEAN (R1, R2 RESIDUE carried) | REGISTER_MAP, BAREMETAL_FIRMWARE, TESTING, milan_dp README, CHANGELOG, PR body, issue comments | R774-1 | 992c3d7bb37f4ade0b151c17d718baed0e119753 |

## What I ran (all at the exact head unless stated)

All runs were on copies under this packet's scratch directory, using the pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`, wrapper sha256 `905795b99e0a8803383b198b118bafcbd87d20b877e3f09c39c31ea81979e92f`):

| Run | Result | Receipt |
|---|---|---|
| `make bootsa`, head | 40 of 40 | `receipts/bootsa_head.log` |
| Same leg, base RTL | 9 of 40 fail | `receipts/bootsa_base.log` |
| No-extra-hold mutant (F1) | 40 of 40: the mutant survives | `receipts/bootsa_noxtra.log` |
| Early-enable probe, head | 40 of 40 | `receipts/bootsa_headearly.log` |
| Early-enable probe, mutant | 4 of 40 fail | `receipts/bootsa_noxtraearly.log` |
| Byte-dump probes, head and base | dumps compared (Conformance item 4) | `receipts/bootsa_headdump.log`, `receipts/bootsa_basedump.log` |
| `make bootsa-mutants`, head | 8 of 8 | `receipts/bootsa_mutants_head.log` |

- `receipts/probe_summary.txt` collects the tallies, and `scripts/reproduce.sh` reruns them.
- The clone was never modified. `receipts/clone_integrity.txt` shows HEAD, tree, clean status, empty index diff, and all six gitlinks unchanged.
- In the published logs I replaced a local home-directory path with `<home>` / `<pinned-simulator-root>`.

## Real limits

- I did not run the full 65-suite sweep, the firmware self-tests, coverage, the builder, behave, the LiteX SoC simulations, Yosys or the docs.yml steps. Those results are the author's receipts.
- I reran only the `bootsa` leg, its campaign and my probes. I ran no other leg changed by the harness edits (gptp, gptp-lat, tdm8_render, nxn, capture_coherence). My conclusion about those edits is from reading the code.
- Hosted contexts at the exact head were still running when I took the snapshot: several completed with success, many Verilator shards were in progress or queued, `rtl-fast` and `docs-check` were queued, and Physical gPTP was skipped (`receipts/hosted_checks_snapshot.txt`). That is not evidence of acceptance.
- No hardware boot capture exists, and physical calibration was not run. Per the maintainer reading, the issue stays open.
- I could not check the IEEE and Milan clause numbering cited in the new comments against the standard texts, which are not in the tree.
- The AAF hold is verified only by reading the RTL: no AAF frame was offered inside the held window in any run.
- The area figure is the out-of-context synthesis at `8d2dfb65`, not a routed image.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) and link its receipts.
- Own acceptance of the hosted and act runs on the exact head.
- Carry R1 and R2 to the residue checklist.
- Route F1 to the executor and have a reviewer re-check the fix at a new head. Because the Tests lens is unclean, the lens has to be covered again at a head that includes the fix.

R774-1 FINISHED
