[R842] POSITIVE - exact head 8e523a2b17faf17c4564e5af155b73f95dc2a0a5

External independent review R842-2 of issue #911 / PR #913. Tree `2c53a871df1f717ba7cb72f77147c549155beed5`; source base `b7d692952305e4e0e132abb8f99c339eeb17a873`. All five lenses are CLEAN. Every named round-1 finding is resolved at its cause, including both suggestions and both wording residues. No new BLOCKER, MAJOR or MINOR was found. One new wording-only RESIDUE is recorded below.

## Scope and authority

Reconstructed AGENTS.md / CONTRIBUTING.md, docs/README.md, [issue #911](https://github.com/kebag-logic/milan-fpga/issues/911), its [integrator-documentation decision](https://github.com/kebag-logic/milan-fpga/issues/911#issuecomment-6876968816) and [JTAG instructions decision](https://github.com/kebag-logic/milan-fpga/issues/911#issuecomment-6877123911), REQUIREMENTS.md product ownership and REQ-VER-02 through REQ-VER-06, [#818](https://github.com/kebag-logic/milan-fpga/issues/818), and QSPI_FLASHBOOT.md / BOARD_DEPLOYMENT.md / BUILDING.md. The scope is a pre-release board variant and its deployment path, not silicon qualification.

Inspected the source-base diff and history, then independently reviewed the six-commit, nine-file delta from `4958ca4f630da1f715bdcd78113b798bbe332b81`. Recorded a provisional independent verdict and five-lens ledger before opening the prior public findings. Reconciled [R841-1](https://github.com/kebag-logic/milan-fpga/pull/913#issuecomment-6881465909) and [R842-1](https://github.com/kebag-logic/milan-fpga/pull/913#issuecomment-6881181571) only after that pass. No other current-round review report or private author material was read.

Evidence below uses the fixed [public archive](https://github.com/kebag-logic/milan-fpga/tree/489e06bd1c6adbf19eb36d5fbc7ca4e47944b18d/review-evidence/911-r1), abbreviated **archive**. Paths starting `receipts/` refer to `author-r2/receipts/` there unless otherwise stated. Also checked the current PR body, issue REVIEW READY comment `6883755663`, and manager evidence/start comments. The archive's published SHA-256 manifest verifies all 96 author-r1 and 98 author-r2 entries. This is published-byte hash verification, not a claim of a cryptographically verified author signature.

## Prior-finding disposition

| Prior ID and lenses | Disposition at this head | Cause checked and evidence |
|---|---|---|
| R841-1-F1, MINOR, Tests | RESOLVED | `sw/builder/test_builder.py:19125` constructs both 200T sets with budget/AEM at `0xA00000` and a 9,730,652-B payload, invokes `build.sh flash ax7a200t`, asserts writes `[0xA00000, 0]`, and checks both byte ranges. `sw/builder/test_timing_grade.py:216` reconstructs both dies from rendered `soc.h`, compares exported images/device, and validates payloads. Both changed gates pass locally. Published K7 fails the committed timing-grade gate; K9 fails that gate and gate 1e at the 4 MiB cap. |
| R841-1-F2, MINOR, Conformance, Docs | RESOLVED | `receipts/guide-run/02-update-200t-D-to-R.*` and `03-update-200t-R-to-D.*` have rc 0, AEM-before-bitstream order and matching readback at `0xA00000`/0. The PR body and issue acceptance-4 statement disclose that the second set changes and rebinds one payload byte; the old compressed-set refusal is now explicitly described. Baseline clock/CDC/I/O reports are openable under `receipts/ax7101-release/`; independently parsed comparisons agree with `receipts/buildC-release/`. |
| R841-1-F3, MINOR, Conformance, Docs | RESOLVED | `docs/guides/BOARD_DEPLOYMENT.md:309` and `:321`, plus `docs/integration/QSPI_FLASHBOOT.md:91`, state the pre-#911 target-layout refusal, rebuild/regeneration/manual-JTAG remedies, need for `soc.h` when regenerating, and the stub-only limit on both boards. Old metadata remains usable for installed-state proof. Guide receipts 05/06/07 show refusal, regeneration, then successful update. |
| R841-1-F4, SUGGESTION, Tests, Robustness | IMPLEMENTED | `sw/builder/test_builder.py:19105` plants conflicting JEDEC forms, unlike dies and identical dies on one chain. Each is refused before dump/write on all three persistent paths. Published K3/K4 fail gate 1e; C1 restores set-based deduplication and fails on the identical-die control. The local transaction run exercises these controls successfully. |
| R841-1-F5, SUGGESTION, Conformance, Docs | IMPLEMENTED | `receipts/vivado-buildC-route/` supplies raw per-corner timing summaries, operating-condition reports and CDC reports from the routed image checkpoint. Their summaries agree with the previously published signoff figures; raw CDC categories also agree with the original image signoff and AX7101 baseline. |
| R841-1-RS1, RESIDUE, Docs | RESOLVED | `docs/guides/BOARD_DEPLOYMENT.md:394` now says “a Digilent FT232H”; the current PR limitations and round-2 acceptance text agree. |
| R842-1-F1, MINOR, Conformance, Docs | RESOLVED | `docs/integration/BUILDING.md:472` now gives both dies' slot/AEM boundaries and names `FLASHBOOT_BITSTREAM_SLOT` / `layout_for()`. Related wording is scoped in `BAREMETAL_FIRMWARE.md:103`, `QSPI_FLASHBOOT.md:252` and `build.sh:62`. The map and executed reconstruction test agree. |
| R842-1-R1, RESIDUE, Docs | RESOLVED | Both references in `docs/integration/BUILDING.md:312` and `:363` now name the existing `BUILD_DIES` declaration. |

Mutation evidence is `receipts/mutants/K3-K4-K7-K9-at-head.txt` and `K9-words-C1-C2-at-head.txt`. I inspected the published mutation anchors and driver against the committed assertions. K7 is caught by the timing-grade gate, not gate 1e; the published table correctly preserves that distinction. These mutation executions are author receipts, not claimed as independent reruns.

## New finding

### R842-2-R1 - RESIDUE - Docs

**Artifact:** archive `author-r2/receipts/vivado-buildC-route/RUN.txt:8`.

**Title:** A copied size-limit annotation incorrectly describes the small check-timing report.

**Authority/evidence:** The line correctly records 4,828 B and SHA-256 `3cdda5147210ad5c84b56bbce3be52dfc62051885a33933c85f78bfa1c2a8f34`, then says “over the 200 KB limit; not copied”. That exact report is published at `author-r2/receipts/buildC-release/alinx_ax7101_signoff_check_timing.rpt` and its manifest hash verifies.

**Impact:** The parenthetical misdirects readers about where an already available receipt lives. No measurement, figure, verdict, test, source behavior, generated design artifact or conformance claim changes.

**Required outcome / exact fix:** Replace only that parenthetical with `(published in ../buildC-release/alinx_ax7101_signoff_check_timing.rpt)`. Preserve the size and hash.

**Verification:** Open the named report and verify the unchanged hash. This is wording-only RESIDUE and leaves Docs CLEAN; the manager carries it to the residue checklist.

## Evidence and lens results

[R842] PASS Conformance - `docs/integration/BUILDING.md:472`, `sw/litex/build.sh:385`, `sw/litex/flash_map.py:55`, archive guide/signoff/identity receipts - Acceptance 1-4 are supported within the stated desk-only scope. The selected recipe retains the 1x1 TDM8 configuration and derived platform; the 200T map has the required capacity and offset. The corrected acceptance statements match their executable evidence.

The image recipe is `ax7a200t`, image commit `1e604e1b4f0aa8015544eb0d363a965fbb4cd985`, first ExtraPostPlacementOpt route, AreaOptimized_high synthesis, ExploreArea optimization, AggressiveExplore timing optimization, with the disclosed eight-thread implementation. Raw summaries give Slow 0/85 C WNS +0.174 ns / WHS +0.102 ns and Fast 0/85 C WNS +1.633 ns / WHS +0.036 ns, all TNS/THS zero. These meet #818's +0.030/0 ns floors. Endpoint temperatures remain power conditions over fixed Slow/Fast timing models. Recorded utilization remains 53,590 LUT, 54,971 FF, 87.5 BRAM and 15 DSP.

[R842] PASS RTL - `sw/litex/milan_soc.py:3857`, `sw/litex/platforms/alinx_ax7101.py:297`, `sw/litex/platforms/ax7101_timing.py:21`, archive `receipts/identity/*` and raw clock/CDC/I/O reports - No gateware input changes in the round-2 delta; the earlier clean RTL scope remains valid. Both 150-entry recipe input lists equal their image-commit counterparts. The 200T list also equals build C's own list; the AX7101 list equals the source-base list. Independently matched all 143 checkout-resident entries per recipe. Seven generated/SDK entries are unavailable in this clone; their equality rests on the published lists and comparison receipts. Reviewed the comparison script's stamp/path normalization and the disclosed thread-cap difference.

The raw report comparison independently confirms 16 clock pairs with identical endpoint counts/classifications/constraints, eight identical CDC rule/severity/count rows, and 113 identical used-pin signal/name/use/standard/bank rows. This is not a claim that clock-pair slack or physical pin voltages are identical.

[R842] PASS Robustness - `sw/litex/qspi_owner_transition.py:333`, `sw/litex/deploy.sh:245`, `sw/builder/test_builder.py:19077`, local `transaction.log` - Counting matching device entries preserves the identical-die refusal. The checked paths retain pre-write identification and fail closed. Extra independent assertions observed the first-check message naming layout or FPGA for both actual causes on flash-pair, flash and flash-images (three observations each), plus three identical-die refusals. The committed gate separately proves no dump/write and no premature bridge load in those cases. Single-device successful controls and the real-size 200T transaction pass.

[R842] PASS Tests - `sw/builder/test_builder.py:19125`, `sw/builder/test_timing_grade.py:216`, local `transaction.log`, `timing-layout.log`, `evidence-audit.log` - Focused transaction and timing/layout gates passed concurrently, including the six table mutations and the new two-die reconstruction. Verified the published census: 150 rc-0 workflow-step rows, 522 NOT RUN rows with reasons, and 27 rc-0 additional gates at the exact clean-clone head. No failed row is counted as a pass. Round-2 Verilator shards were not executed; the unchanged RTL/testbench scope retains the round-1 65/65 evidence. Full source-bank logs were not independently reproduced.

[R842] PASS Docs - `docs/guides/BOARD_DEPLOYMENT.md:290`, `:309`, `:321`, `docs/integration/QSPI_FLASHBOOT.md:91`, `docs/integration/BUILDING.md:472`, current PR/issue acceptance text and archive receipts - The operational geometry, installed-build definition, old-set remedies and both-board limits agree. The new source comments contain no bench lane label, review round, reviewer ID or issue-comment ID. All previously open documentation findings are resolved; R842-2-R1 is residue only.

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #911 acceptance/decisions; #818; BUILDING.md:472; build.sh:385; flash map; guide/signoff/identity receipts | R842-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| RTL | CLEAN | Six-commit delta; milan_soc/platform contracts; both 150-input lists; raw timing/CDC/clock/pin reports; prior unchanged RTL scope | R842-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| Robustness | CLEAN | qspi_owner_transition.py:333; deploy.sh:245; test_builder.py:19077; transaction.log; K3/K4/C1 receipts | R842-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| Tests | CLEAN | test_builder.py:19125; test_timing_grade.py:216; timing-layout.log; mutation receipts; evidence-audit.log | R842-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |
| Docs | CLEAN | BOARD_DEPLOYMENT.md:309/321; QSPI_FLASHBOOT.md:91; BUILDING.md:312/363/472; BAREMETAL_FIRMWARE.md:103; PR/issue and archive | R842-2 | 8e523a2b17faf17c4564e5af155b73f95dc2a0a5 |

## Limits and pending manager duties

- No hardware was touched. Physical calibration is NOT RUN; field skips and stub-programmer success are not hardware proof. No REQ-VER-05/06 boot, soak, audio or power-cycle qualification is granted. Both boards' new identification path still awaits its first real execution.
- The timing reports retain 46 inputs with false-path/no-input-delay diagnostics, 87 outputs without output delays, and ten CDC-10 critical rows, matching the baseline. Timing closure does not erase those diagnostics or establish complete physical-interface timing.
- The actual bitstream and routed checkpoint were not rebuilt or independently rehashed. The published part is `7a200tfbg484` (`xc7a200tfbg484`); bitstream SHA-256 is `b7d7dc4ec9ce9254a089fc99d6699d13eba1b8271ed889d000bded46be64954f`, AEM `bdfde7cf448ed032ffb1663b0898aeef9ded3bb11b4ead5dc36dfa3df873f180`, layout `73c2d40e3f3d6ae122b93b71b896abdf75a2f75e9014411b84dced32289a1837`. The input-identity evidence supports retaining that delivered image; it is not an independent repeat build.
- There is no manager source bank at this head, and none is inferred. The source execution evidence is the author's published receipts. Hosted/local-replica acceptance belongs to the manager; I did not run or accept those jobs. At the merge turn the manager must validate the current-dev candidate with the required builder/native banks, link receipts, complete both independent reviews with none in flight, obtain merge authorization, and perform post-merge containment. Source base and supplied live dev are `b7d692952305e4e0e132abb8f99c339eeb17a873`.
- Carry R842-2-R1 to the residue checklist. Keep the delivered guide link reachable and ensure the handover includes the corrected deployment instructions. Pre-existing #912 and BAREMETAL_FIRMWARE.md journal-slot wording remain outside this review's scope.
- No source edits, commits, pushes, GitHub writes, shared installs or prohibited broad banks occurred. Final raw verification matched all 1,731 superproject tracked blobs/modes/index entries and the four required submodules' pins, bytes, modes and indexes. No source restoration was necessary.

## Reproduction

With this packet as `PACKET`, the exact checkout as `CHECKOUT`, and the existing pinned LiteX interpreter as `LITEX_PYTHON`:

```sh
python3 "$PACKET/focused_probe.py" "$CHECKOUT" "$PACKET" "$LITEX_PYTHON"
python3 "$PACKET/audit_evidence.py" "$CHECKOUT" "$PACKET"
python3 "$PACKET/verify_checkout.py" "$CHECKOUT"
```

All three exited 0. `audit_evidence.py` requires archive commit `489e06bd1c6adbf19eb36d5fbc7ca4e47944b18d` in the checkout object database. Disposable files remain under `scratch/`, excluded from publication. `MANIFEST.sha256` enumerates the publishable scripts and raw receipts.

R842-2 FINISHED
