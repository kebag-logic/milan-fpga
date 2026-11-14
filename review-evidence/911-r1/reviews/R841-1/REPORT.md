[R841] NEGATIVE - exact head 4958ca4f630da1f715bdcd78113b798bbe332b81

Round R841-1 is the internal cleared-context review of PR #913 (issue #911, the XC7A200T variant of the ALINX AX7101 board). It covers the exact head `4958ca4f630da1f715bdcd78113b798bbe332b81`, tree `cc92bd5f2ef6d44d1510157a612578458e1e0ab6`, delta `b7d69295..4958ca4f` (ten commits). All five lenses were applied independently.

**Verdict:** NEGATIVE. Three MINOR findings are open: F1 (Tests), F2 (Conformance, Docs) and F3 (Conformance, Docs). The product is sound in every respect this round could check without hardware:
- The AX7101 is unchanged apart from two layout fields.
- The 200T derives its part and its AEM offset from one source each.
- The board refusals come before any dump or write.
- The 200T update path works when it is given valid image sets.

What is open is test coverage of the 200T flash map on the deploy side, two evidence claims, and two undocumented AX7101 deploy changes. The RTL and Robustness lenses are clean.

## Authority reconstructed

- Issue #911 body: scope bullets and acceptance 1-4. Scope changes in issuecomment-6876968816 (integrator docs, not a kit) and issuecomment-6877123911 ("Flash an image set over JTAG", `INSTALLED_BUILD` defined, part and offset taken from the layout).
- #818: +0.030 ns WNS and 0 ns WHS at every signoff corner. #395: `TIMING_GRADE`.
- `docs/integration/QSPI_FLASHBOOT.md`, `docs/guides/BOARD_DEPLOYMENT.md`, `docs/integration/BUILDING.md`.
- The executor's packet `review-evidence/911-r1/author-r1` at archive `6d63052b`, plus the REVIEW READY comment issuecomment-6880655385 and the PR body.
- **Prior public findings:** none existed on PR #913 when this round started. The earlier started review was stopped before any finding (issuecomment-6880989188). A parallel round's verdict was published while this round was running; it was not read before this verdict and ledger were written, and nothing here depends on it.

## Findings

### F1 - MINOR - Tests - the 200T flash map never reaches deploy.sh or layout_from_soch.py in a committed gate

- **Artifact:**
  - `sw/builder/test_builder.py:18755` (`make_build` always writes the AX7101 map: bitstream budget `0x400000`, AEM `0x400000`).
  - `sw/builder/test_builder.py:19112-19140` (`on_200t()` re-binds only the bitstream part, so the "200T" flash-pair arm runs on the 4 MiB map).
  - `sw/litex/layout_from_soch.py:66-108` (new: the budget comes from the compiled AEM offset, the flash device from litespi; no test references this file).
  - `sw/litex/qspi_owner_transition.py:238` (the budget read).
- **Authority/evidence:**
  - AGENTS.md section 5 requires self-checking tests for changed behaviour, and the Tests lens requires that each test can fail for the defect it claims to detect. Issue #911 scope moves the AEM region "deriving the new offset everywhere it is read", and deploy.sh and `layout_from_soch.py` are among those readers.
  - Reviewer mutants in a disposable copy (`receipts/probes/mutants.txt`):
    - **K9** caps the deploy bitstream budget at 4 MiB. Gate 1e still passes ("ALL GATES PASS").
    - **K7** reverts `layout_from_soch.py` to the fixed `0x40_0000` budget. Gate 1e and `board_variants.py` both still pass. `test_timing_grade.py` has no reference to the file.
  - Under K9 the reviewer's probe of the guide's update step on two real-shape 200T image sets fails (`receipts/probes/probe_200t_update_under_K9.txt`: the update arm returns rc 2 with no writes). The same probe passes at the head (`receipts/probes/probe_200t_update.txt`).
- **Impact:** a regression that restores the AX7101's 4 MiB slot anywhere on the deploy or reconstruction side would make `build.sh flash ax7a200t` refuse every 200T image set. That includes sweep builds, whose layout is reconstructed from soc.h. Every committed gate would stay green. The failure is fail-closed (no wrong write), but it disables exactly the variant this issue ships.
- **Required outcome:** a committed, self-checking test drives an image set on the 200T map through the deploy path and proves the result. The map is bitstream budget `0xA00000`, AEM at `0xA00000`, with a payload larger than 4 MiB. The deploy path is `build.sh flash ax7a200t` or `deploy.sh flash-pair`, and the result is the AEM written at `0xA00000` and the bitstream at 0. A test also covers `layout_from_soch.py`'s budget and flash device on a 200T soc.h.
- **Verification:** with the new tests, mutants K7 and K9 turn them red. The tests are green at the fixed head.

### F2 - MINOR - Conformance, Docs - acceptance 4 is reported "Met" over a guide step whose receipt failed, and two comparisons cite AX7101 receipts that are not published

- **Artifact:**
  - The packet's `receipts/guide-run/11-update-flash-pair.{cmd,log,rc}`: rc 2, "installed bitstream payload 5566832 B exceeds 4194304 B slot".
  - `receipts/guide-run/guide_run.sh.txt`, whose comment says that step "updates it to the image set".
  - The REVIEW READY comment, acceptance item 4, and the PR body's "Guide run" bullet: "the guide's steps ran as written". It lists the refusals of steps 3-7, 10 and 12, and does not mention step 11.
  - The same texts' "Clock interaction and CDC categories match the AX7101 release" and "all 113 used pins match the AX7101 release".
- **Authority/evidence:**
  - Acceptance 4: "The deployment guide's steps for the variant run as written". AGENTS.md section 6, Docs lens: "The PR and Issue contain enough evidence for another cold reviewer".
  - The "Update a flashed board" step is one of the guide's steps for the variant. The only receipt for it is a refusal. The refusal is correct (the installed set chosen was a compressed build on the 4 MiB map), but it is reported as neither a pass nor an expected refusal.
  - The packet holds no AX7101 release clock-interaction, CDC or I/O report, so the comparisons cannot be checked. The nearest public record, `docs/findings/COMMERCIAL_TIMING_395.md:173-185`, is an older AX7101 build whose CDC counts differ (CDC-10 6 against the 200T's 10; CDC-12 4 against 0).
  - The reviewer's own probe shows the update step succeeds on valid image sets. The XDC is byte-identical between the dies (`receipts/probes/ax7101_vs_ax7a200t_head.txt`), so the pin claim holds by construction. The defect is the evidence, not the behaviour.
- **Impact:** a cold reviewer reading the acceptance statement would believe the update step ran green, and cannot open the baseline that the CDC and clock-interaction comparison rests on.
- **Required outcome:**
  - Either publish a receipt of the guide's update step ending rc 0 on two valid 200T image sets, or state that step's result and limit plainly.
  - Correct the acceptance 4 statement to match.
  - Either publish the AX7101 release reports the comparisons cite, or restate those claims as what was measured on the 200T only.
- **Verification:** the republished acceptance text and receipts agree line for line, and each comparison names a receipt that can be opened.

### F3 - MINOR - Conformance, Docs - two AX7101 deploy changes are not stated for integrators

- **Artifact:**
  - `sw/litex/deploy.sh:473,490,533` (`prove_board` now runs on every AX7101 persistent write).
  - `sw/litex/qspi_owner_transition.py:328-333` (a target layout without `flash_device`/`flash_jedec_id` is refused).
  - `docs/integration/QSPI_FLASHBOOT.md:83-89` ("The AX7101 map, image and firmware are unchanged").
  - `docs/guides/BOARD_DEPLOYMENT.md:280-286` and `:345-360` (the untested list covers only the XC7A200T).
  - The PR's "Known limitations".
- **Authority/evidence:**
  - Acceptance 3: "or the change to it is stated and justified". AGENTS.md section 7: "no undocumented requirement/interface change remains".
  - **Old image sets refused:** every AX7101 image set built before this change has a layout without the two new fields. deploy.sh `flash`, `flash-images` and `flash-pair` now refuse such a set as a target. Gate 1e tests this as "a layout naming no flash device". The refusal message says to regenerate the layout with `layout_from_soch.py` from soc.h, but a delivered image set (three files) has no soc.h. No page tells an integrator that an earlier AX7101 image set no longer flashes through deploy.sh.
  - **Stub-only check on the bench board:** the new board proof (`--detect`, then `--detect -f --verbose` through the bridge) has run only against stub programmers. That applies to the AX7101 as well, which is the bench board and the shipping one. The format the parser expects does match the installed programmer's own output strings ("`\tmodel  %s`", "`read %x`", "`JEDEC ID: 0x%06x`", and "detect FPGA, add -f to show connected flash"). The docs and PR state the stub-only limit for the XC7A200T only.
- **Impact:**
  - An integrator holding an earlier AX7101 image set meets a refusal the guide does not explain, with a fix they cannot apply.
  - The first real AX7101 flash after merge is also the first real run of the new parser, which is not stated.
- **Required outcome:** the deployment guide or the QSPI page states three things:
  - layouts without `flash_device`/`flash_jedec_id` (image sets built before #911) are refused as targets;
  - what to do with one, whether that is a rebuild, the plain JTAG commands, or regenerating from a build directory's soc.h;
  - the new die and flash ID check has run only against a stub programmer on both boards, until a bench run is recorded.
- **Verification:** the stated text is present at the fixed head, and the docs gates pass.

### F4 - SUGGESTION - Tests, Robustness - two refusal branches of check-board have no planted control

- **Artifact:** `sw/litex/qspi_owner_transition.py:335` (`len(models) != 1`) and `:350` (`len(ids) != 1`).
- **Evidence:** the code handles both correctly, but no committed control plants either case:
  - **K3** lets two disagreeing JEDEC ID forms through and survives gate 1e. No fake output prints two different IDs.
  - **K4** accepts several FPGA models on the chain and survives. No fake output prints a two-device chain.
- **Suggested outcome:** gate 1e plants two disagreeing ID lines and a two-device `--detect` output, and expects refusal before any dump or write. This is optional; it does not affect coverage.

### F5 - SUGGESTION - Conformance, Docs - per-corner timing and CDC are published as summaries

- **Artifact:** the packet's `buildC-release/buildC-release-signoff.md` and `buildC-release-cdc-summary.txt`.
- **Evidence:** the route, `check_timing`, clock interaction, utilisation and IOB reports are raw Vivado output. The per-corner WNS/WHS table and the CDC table are condensed by the executor's tooling, and no raw `report_timing_summary` or `report_cdc` is published.
- **Suggested outcome:** add the raw per-corner timing summary and CDC report for the image commit, so the #818 floor can be read off Vivado's own output.

### RESIDUE

- **RS1 - Docs - `docs/guides/BOARD_DEPLOYMENT.md:355`:** "The JTAG cable is the onboard FT232H." contradicts `:25`, "The board's JTAG cable, a Digilent FT232H." The REVIEW READY comment and the PR body repeat "onboard".
  - **Exact fix:** change line 355 to "The JTAG cable is a Digilent FT232H." and drop "onboard" from the PR body's Known limitations.

## What was checked, by claim

1. **AX7101 unchanged.** I elaborated `build.sh ax7101` without `--build` at `b7d69295` and at the head (`receipts/probes/ax7101_base_vs_head.txt`, `ax7101_verilog_body.txt`).
   - 15 of the 22 in-scope outputs are byte-identical, including the Tcl, the XDC, the ROM/RAM/SRAM init and `aem_desc.bin`.
   - The Verilog body is identical once the header, the hierarchy comment and LiteX's footer timestamp are removed. `csr.*` and the generated headers differ only in generated-on lines.
   - `flashboot_layout.json` gains exactly `flash_device` and `flash_jedec_id`.
   - The executor's 140-input lists (`b7d69295` against `1e604e1b`) are byte-identical files. Since `1e604e1b`, the only change to `milan_soc.py` is a type annotation, and the platforms are untouched.
2. **200T layout derivation.** `FLASHBOOT_BITSTREAM_SLOT` (`sw/litex/milan_soc.py:156`) and `flash_map.layout_for()` (`sw/litex/flash_map.py:55-65`) are each stated once.
   - At the head, the elaborated 200T has `MILAN_AEM_FLASH_OFFSET 0xa00000` and `MILAN_FLASHBOOT_AEM_OFFSET 0xa00000` (soc.h), a layout with budget and AEM at 10485760, and `SPIFLASH_SIZE 0x01000000`, so the firmware's memory-mapped read at `SPIFLASH_BASE + 0xa00000` is inside the window.
   - `layout_from_soch.py` reproduces main()'s images and flash device for both dies (`receipts/probes/layout_from_soch_vs_main.txt`).
   - The diagrams regenerate byte-identical (`receipts/probes/flash_layout_regen.txt`).
   - The arithmetic checks out: 10,485,760 - 9,730,652 = 755,108 B, and 5,566,832 - 4,194,304 = 1,372,528 B.
   - The `aem_desc.bin` sha256 `bdfde7cf...` matches the handover SHA256SUMS.
3. **check-board.** prove_board sits after staging and validation and before the first dump or write on all three paths (`deploy.sh:473,490,533`). `FPGA_PART` is bound to the bitstream part by `--expected-fpga-part` before it.
   - Gate 1e is green at the head.
   - Reviewer mutants **K1** (dump before proof), **K2** (family-only die compare), **K5** (write before proof) and **K8** (200T programmer part reverted) are each killed with "dumped or wrote after the refusal" or "accepted".
   - The reviewer's probe refuses a 100T die, another JEDEC ID, the ax7101 recipe and an identical refresh, with no writes in each case.
4. **Timing and pins.** From the executor's packet:
   - The raw `check_timing` at the image build shows 0 unconstrained internal endpoints, 0 no-clock pins and 0 loops. Route status shows 0 nets with routing errors, and IOB pack is 21 PASS. Utilisation is on `xc7a200tfbg484-2`.
   - The summary table gives Slow WNS +0.174 / WHS +0.102 ns and Fast WNS +1.633 / WHS +0.036 ns, which meets the #818 floor at all four corners.
   - The reviewer's elaboration at the head shows the 200T Verilog body identical to the AX7101's. Between the dies only the part (Tcl: create_project, synth_design, `kl_timing_grade_configure`) and the AEM constant (soc.h, BIOS ROM init) differ, which supports "the 200T build inputs at 4958ca4f equal the built ones" as far as derivation goes.
   - The pin claim holds by construction, because the XDC is byte-identical.
5. **Guide.**
   - `board_variants.py` is green, and its self-test is green with 6 controls. Reviewer mutant **K6** (AEM not moved) is caught by both `board_variants.py` and `test_timing_grade.py`.
   - The JTAG section reads the part, offset and ID from the layout. The Vivado part name `mt25ql128-spi-x1_x2_x4` is in the executor's Vivado part list, and that list has no N25Q entry.
   - `INSTALLED_BUILD` is defined at `:290`, and the untested items are listed at `:345-360`. See F2 and F3.
6. **Gate pass.** From the executor's `workflow-steps.md`: 150 rows at rc 0 and 522 NOT RUN, each with a non-empty reason. `sweep.txt` shows 65/65 suites across four shards.
   - The reviewer re-ran leg 0's only member, `test_gptp_tx_timestamp`: PASS in 576 s (`receipts/probes/litex_sim_test_gptp_tx_timestamp.log`).
   - The leg wrapper itself refused to run in this clone because its submodule origin points at a local path. That is an environment matter, not a finding.
   - Re-run at the head: `check_sweep_shape --self-test`, `board_variants` and its self-test, gate 1e, `test_timing_grade`, `build.sh ax7a200t --dry-run`, `git diff --check`, `docs_inventory --check`, `docs_check`, `check_doc_style`, `check_doc_paths`, `check_diagram_pngs`, `check_hygiene`, `check_py_idiom`, `check_sh_idiom`, `check_solution_docs` and `check_deploy_shape --self-test`. All exit 0.
   - The em-dash gate could not run here (its pinned renderer is not installed); the added lines carry no U+2014.
7. **Comment rule.** There is no lane label, review round, reviewer ID or issue-comment ID in any added line of the delta.

## Lens results

```text
[R841] MINOR Conformance -- review-evidence/911-r1/author-r1/receipts/guide-run/11-update-flash-pair.rc; issuecomment-6880655385 item 4 -- F2
[R841] MINOR Conformance -- sw/litex/qspi_owner_transition.py:328-333; docs/integration/QSPI_FLASHBOOT.md:83 -- F3
[R841] PASS RTL -- sw/litex/platforms/alinx_ax7101.py:297-311, sw/litex/platforms/ax7101_timing.py:21-53, elaborated gateware/alinx_ax7101.{v,xdc,tcl} for both recipes at 4958ca4f (receipts/probes/ax7101_vs_ax7a200t_head.txt), author buildC-release check_timing/route_status/iob_pack/clock_interaction -- the die reaches create_project, synth_design and the timing-grade hook; Verilog body and constraints identical across dies; no site or pblock constraint depends on the die; 0 unconstrained internal endpoints, 0 routing errors; PLL speed grade reached (test_pll_grade green)
[R841] PASS Robustness -- sw/litex/deploy.sh:223-260,473,490,533; sw/litex/qspi_owner_transition.py:290-360; sw/litex/milan_soc.py:4434-4436; receipts/probes/{mutants,probe_200t_update}.txt -- die mismatch, JEDEC mismatch, unreadable die and ID, deviceless layout, unknown part, --fpga-part with arty, stale 4-MiB-map installed set, identical refresh: each refused before any dump or write (K1, K2, K5, K8 killed); F4 is optional
[R841] MINOR Tests -- sw/builder/test_builder.py:18755,19112-19140; sw/litex/layout_from_soch.py:66-108 -- F1 (K7, K9 survive)
[R841] MINOR Docs -- issuecomment-6880655385 / PR #913 body "Guide run" and AX7101-release comparisons -- F2
[R841] MINOR Docs -- docs/guides/BOARD_DEPLOYMENT.md:280-286,345-360; docs/integration/QSPI_FLASHBOOT.md:83-89 -- F3
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3) | Issue #911 acceptance 1-4 and both scope comments; build.sh:71,197,384-390; milan_soc.py:147-163,3857-3911,4027-4032,4433-4444,4612-4620; flash_map.py:55-80; head elaborations of both recipes; the executor's signoff, guide-run and cfgmem receipts | R841-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| RTL | CLEAN | platforms/alinx_ax7101.py:297-311; platforms/ax7101_timing.py:21-53; elaborated .v/.xdc/.tcl/init for both recipes and the AX7101 at b7d69295; buildC-release check_timing, route_status, iob_pack, clock_interaction, utilization_place | R841-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| Robustness | CLEAN | deploy.sh:28-34,223-260,440-560; qspi_owner_transition.py:285-360,655-700; layout_from_soch.py:66-108,181-184; mutants K1-K9; probe_200t_update arms | R841-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| Tests | UNCLEAN (F1) | test_builder.py:18660-18680,18741-18760,19061-19156,25536; test_timing_grade.py:166-226; check_sweep_shape.py:64-127,465-470; board_variants.py (whole file); gate runs at the head; mutants K1-K9 | R841-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |
| Docs | UNCLEAN (F2, F3) | BOARD_DEPLOYMENT.md (whole delta); QSPI_FLASHBOOT.md (whole delta); BUILDING.md:302-322,360-364; diagrams README and regenerated flash maps; DOCUMENTATION_AUDIT.md row; PR body; REVIEW READY comment; comment-rule scan of the delta | R841-1 | 4958ca4f630da1f715bdcd78113b798bbe332b81 |

## Real limits

- No hardware was touched. Physical calibration was NOT RUN, and field skips are not hardware proof. The new board check's parsing was compared against the installed programmer's format strings, not against a live board.
- No Vivado run. The timing, utilisation, CDC, IO and bitstream-header figures, and the image hashes, come from the executor's packet. The 9.4 MB handover bitstream is not published, so its header part and sha256 were not re-read.
- "The 200T build inputs at 4958ca4f equal the built ones" was checked by derivation only: the head's 200T elaboration differs from the AX7101's only in the part and the AEM constant. Build C's own inputs are not published to compare byte for byte.
- No manager source bank runs at this head, and none is claimed or inferred. The full parent, Verilator and Yosys banks were not run; the 65/65 suite sweep is the executor's receipt.
- Two gates did not run here. The em-dash gate's renderer is not installed (and the round may not make shared installs), so the added lines were scanned directly. The LiteX leg wrapper refused this clone's local submodule origin, so its single member was run directly.
- Hosted checks were read only. At the second read there were 59 successes, 1 skipped (the nightly physical job), 1 in progress and 6 queued.

## Pending manager duties

- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and link its receipts. Live dev is `b7d692952305e4e0e132abb8f99c339eeb17a873`, equal to the source base.
- Own hosted and local-replica acceptance at the exact head.
- Carry RS1 to the residue checklist.
- The handover README links the guide at `1e604e1b`. If the PR is squash-merged, confirm that the linked commit stays reachable, or relink to the merged commit.
- `qspi_owner_transition.py --self-test`'s NameError is pre-existing and tracked as #912, outside this scope.

R841-1 FINISHED
