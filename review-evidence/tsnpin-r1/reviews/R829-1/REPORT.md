[R829] NEGATIVE - exact head 50e2a722ef2671b3f5b017f97b1c7d41705c4f32

# R829-1: internal cleared-context review of PR #892 (issue #665), tsn-c-stack pin 70936b77 -> 715589c

Head `50e2a722ef2671b3f5b017f97b1c7d41705c4f32`, tree `895066febbe99d8a88c9152a2432aeab908e9dc9`, eight commits on `dev-soft-core` `1d6bf555`. All five lenses were applied. Two MINOR findings are open (Tests, Docs), so the verdict is NEGATIVE. The code under review (the ACMP adapter's kept command, the RV32 `__lshrdi3` refusal, the re-anchored plants, the ledger re-key) is correct. Every firmware gate I could run on the pinned SDK passed.

Reconstructed from: AGENTS.md, CONTRIBUTING.md, docs/README.md; issue #665's body and the lane's public comments (TAKEN 6792567545, REVIEW READY 6804604273, owner decision 6798230066, flip plan 6799253003); the #859 round 4 ruling (issuecomment-6746289265, item 1); the tsn-c-stack PR #34 round 2 ruling (issuecomment-6789256216, item 3); the #495 residue row (issuecomment-6792448720); tsn-c-stack `docs/PORTING.md` "ACMP owed bound" at `715589c`; the diff `1d6bf555..50e2a722` and its history; the author's public evidence at `8561308e` `review-evidence/tsnpin-r1` (receipts only). There were no prior public review findings on PR #892: zero reviews and zero review comments, and only the two review-start notices.

## Findings

### F1 MINOR [Tests]: the ACMP poll's rewritten "still owes" return is unpinned at one owed frame

- **Where:** `sw/firmware/ctrl/acmp/acmp_mbx.c:164` (`return m->acmp.owed_count != 0u;`, rewritten by `d504f119`). The only test is `sw/firmware/ctrl/test/test_acmp_mbx.cpp:1055` (E1), via the plant `acmp-poll-owes-nothing` (`sw/firmware/ctrl/test/acmp_owed_mutants.py:60`).
- **Authority:** AGENTS.md section 6 (Tests): boundary behaviour is covered, and each test can fail for the defect it claims to detect. `ctrl_loop.h` THE PASS says only a pass that owes nothing may sleep, and a returning TX room raises no interrupt. The adapter now owns this return; before the PR it was `acmp_poll`'s own.
- **Evidence:**
  - Probe P6 replaces the line with `return owed > 1u;`. It differs from the head only when exactly one frame is owed and the egress refuses.
  - P6 escapes the `acmp` and `acmpif2` arms (`receipts/probes/adapter_probes.log`, 0 checks failed).
  - P6 also escapes every suite arm of `test_ctrl_firmware.py --require-rv32` on a planted scratch copy of the head (`receipts/probes/p6-full-suites.log`, `test_ctrl_firmware: PASS`).
  - I added a check (`receipts/probes/p6-control.patch`). With one GET_RX_STATE response owed behind a held egress, it asserts that the loop does not sleep and that the ACMP poll reports it still owes. It passes at the head (`receipts/probes/p6-wake-check-at-head.log`, rc 0). It fails on P6, with both assertions failing (`receipts/probes/p6-wake-check-with-p6.log`, rc 1).
  - E1 cannot see the defect: it runs with two frames owed, and other modules' output owed behind the same paused egress keeps the loop busy.
- **Impact:** a regression of the changed return at the one-owed boundary would let the loop sleep holding an owed ACMP response, until an unrelated interrupt. That delays the answer IEEE 1722.1-2021 8.2.4 and 8.2.5 require, past T_svc and possibly past the 200 ms of Milan v1.2 Table 5.26. No gate would notice.
- **Required outcome:** a test that fails when the ACMP poll reports nothing owed while exactly one frame is owed behind a held egress, isolated from other modules' owed output. Also a planted defect at that boundary, named by that test in the control campaign.
- **Verification:** apply P6 (the `acmp_mbx.c` hunk of `receipts/probes/p6-tree.patch`). The new test must fail by name, and the campaign count must rise by one caught plant.

### F2 MINOR [Docs]: the published replica says the pinned RV32 SDK was used; the compiler it names is not that SDK

- **Where:** the author evidence `review-evidence/tsnpin-r1/author/receipts/gates/verify-final.md:32`, and the rows at lines 67, 78, 149, 158, 165, 172, 179, 189, 214 and 228. Each says "Install and verify the pinned RV32 SDK | NOT RUN | ... the pinned SDK is this host's `<rv32-sdk>/host`". This feeds the PR body's Status figure, "226 not run with a stated reason".
- **Evidence:**
  - The pinned archive is `scripts/ci_rv32_sdk.py:25` (`d42680e9…`, Bootlin `riscv32-ilp32d--glibc--stable-2025.08-1`).
  - Installed with the repository's own installer, it identifies as `Buildroot 2021.11-18033-g83947c7bb6` 14.3.0, with libgcc sha256 `d8ebca8c…`, and `--verify-only` passes (`receipts/gates/ci_rv32_sdk_install_scratch.log`, `receipts/gates/ci_rv32_sdk_verify_scratch.log`).
  - The compiler the author's receipts name is `Buildroot 2026.05` 14.3.0, with libgcc `faef00ac…` (`size-fixture/ctrl_image-at-0ca18868-against-1d6bf555.log:1`, and three more receipts).
  - The repository's verifier refuses that installation: "missing regular SDK provenance receipt; incomplete install" (`receipts/gates/ci_rv32_sdk_verify_host_sdk.log`).
- **Impact:** the replica's RV32 steps and the RV32-built figures (the ROM/RAM ledger images, S2's images) ran on an unpinned compiler, while the evidence says it was the pinned one. A cold reviewer cannot take those figures as pinned-toolchain evidence.
  - My reruns on the pinned SDK reproduce every firmware result I could run.
  - They also reproduce the size fixture byte for byte (`receipts/size/ctrl_image-pinned-sdk.log` equals the author's log apart from the compiler line). So the risk to the figures is low.
  - The LiteX-linked ledger images and S2's images could not be rebuilt here.
- **Required outcome:** do one of the following, and say which in the PR:
  - state the not-run reason accurately (name the compiler build used); or
  - run the SDK step and the RV32-dependent measurements on the pinned SDK.
- **Verification:** `python3 scripts/ci_rv32_sdk.py --verify-only --destination <SDK used>` rc 0, recorded with the receipts, and the ledger table either unchanged or restated.

### RESIDUE (wording only; carried to the residue checklist)

- **RES1:** `sw/firmware/ctrl/test/acmp_owed_mutants.py:3`. A new source docstring names a lane ("lane F3's"), which the comment rule forbids for new instances. Exact fix: `"""acmp_owed_mutants.py - the planted defects of the ACMP owed frames (#665).`
- **RES2:** the PR body's commit table, row "Ledger the platform's struct at its new size". "`struct ctrl_plat` grows 144 to 152 B at every point" reads as a size change from 144 B to 152 B. Exact fix: "`struct ctrl_plat` grows by 152 B with one interface and by 144 B with two, at both shapes". This matches the ledger's +152, +144, +152 and +144.
- **RES3:** `docs/design/MAILBOX_SPLIT.md:582-583`. The sentence leaves out the BIND_RX case of the owed bound. Exact fix: "A command that arrives with all eight owed, or a BIND_RX that arrives with fewer than two owed slots free, is declined, not dropped: …".

### SUGGESTIONS (optional)

- **S1 [Tests]:** pin the exception that `acmp_mbx.h:39-43` states, with a test. Case: a kept BIND_RX that is only answered leaves a slot free, a timer probe takes it, and the next waiting command leaves one pass later. NFR-SCOUT-03 asks for each stated bound to be tested. I traced the stated one-pass figure by hand and it is correct.
- **S2 [Tests]:** add the same `__lshrdi3` refusal to the portable `rv32` arm. The author's receipt `rv32/arms-platrv32-rv32-at-70936b77.log` shows that arm also reached `__lshrdi3` at the old pin. Only `platrv32` refuses it now (`plat_arms.py:112,158`).
- **S3 [Docs]:** `tb/verilator/ctrl_service_budget/README.md:553`. Findings says "The ACMP core drops the commands it cannot owe", which describes the old pin. Since tsn-c-stack#26 at `715589c` the core declines and the adapter keeps the command. The PR leaves the harness READMEs to their owners, so this is S2b's, at its sync.
- **S4 [Conformance]:** record publicly the decision on the author's open question: the adapter offers only the kept record after an accepting poll (`acmp_mbx.h:28-51`), whereas tsn-c-stack `docs/PORTING.md:88` says to offer every waiting frame. Reviewer position: acceptable.
  - PORTING.md:92 and :117-118 describe ports that offer fewer frames, and what each costs.
  - The adapter states its own figure, n + 1 + f + r, with a one-pass delay per probe in the BIND_RX-only-answered case. It does not claim the stack's bound unconditionally.
  - The reason it gives (the loop's per-pass receive budget, `ctrl_loop.h` A1, which this lane does not change) is in scope.
  - S2's receipts show the kept command answered within the 200 ms of Milan v1.2 Table 5.26: 104.915 ms at 1x1 and 137.688 ms at 8x8.

## Scope checks (the assignment's items)

1. **Pin.**
   - `715589c1` is tsn-c-stack `main` (GitHub branch API) and a fast-forward of `70936b77`: compare `ahead_by` 36, `behind_by` 0, and `merge-base --is-ancestor` true.
   - PRs #28 (`ea4af6f`), #29 (`d7e6a2a`), #30 (`cc3362f`), #33 (`9deb0dd`) and #34 (`715589c`) are merged on that line.
   - The submodule worktree is clean, and the only change in it is the gitlink. The stack's pin proof passed in every gate run ("tsn-c-stack at 715589c1…").
2. **Consumer changes.**
   - #28: the adapter offers every record to `acmp_rx` and keeps one on decline. `acmp_rx_ready` is not consulted. The record is re-offered in the accepting poll, before the next pass's timer service.
     - Tests K1 to K3 pass, and the eight K plants are caught.
     - My probes P1 to P5 and P7 are caught; P6 is F1.
     - Liveness holds: the core declines only when its room check fails (tsn-c-stack `src/acmp.c:1126-1146`), so `owed_count` is at least 1 while a command is kept. `owed_count` is decremented only in `acmp_poll` (`src/acmp.c:1318`). So the loop never sleeps while a command is kept, and every accepting poll re-offers it.
   - #29: `platrv32` refuses `__lshrdi3` (`plat_arms.py:158`), and the plant `wire-put-be-shifts-64-bits` is caught (control campaign). `__lshrdi3` is absent from the size fixture at 715589c on the pinned SDK (`receipts/size`, 452 B of helpers). The split image's hot list is not on this base (`git grep` finds no `ctrl_split_hot`, `ctrl_hot.py` or `load_grade`).
   - #33: the parent has no `ACMP_MAX_SINKS` override (16 sinks, one mask word), so no sizing change is needed. The plants are re-anchored on `release[k / 32u]`.
3. **Consumer bar at the moved pin** (pinned SDK, see Evidence):
   - firmware-unit steps PASS, and fw_coverage `--check` PASS (35 files).
   - Campaigns: control 579/579, SRP 278 defects plus 2 pin controls, 280/280 ok, and AECP 139/139 ok.
   - firmware-verilator PASS.
   - firmware-boundary: not completed here (Limits).
   - Ledger: I checked the author's fixture and platform tables at both pins by arithmetic. Every RAMB36 count follows from its banks (for example 26 + 11.5 = 37.5, 29.5 + 28 = 57.5, 31 + 28 = 59.0). The tightest `rom` margin is the fixture's 1x1 with two interfaces at 88 B, which I checked against all eight points. No bank moves.
   - The +132 B over-granule figure belongs to the `answering-every-port` arm, which is not on this base (`git grep` finds nothing). It is owed at S2b's sync, as the PR says, and 32x32 is S15's.
4. **S2.**
   - The author's base and final runs give rc 0 at both pins. Their totals match the PR body: 1x1 34 -> 35 of 141, 13 -> 14 of 81; 8x8 63 -> 59 of 182, 31 of 129.
   - The final-head identity build reproduces the graded image's sha256 (`4047227d…` at 8x8).
   - `run.py --self-test` passes here (0 failures).
   - `load_grade.py` and the flip check (#890, owner ceiling 0.75 at 8x8/2if) are not on this base. They are graded after this merge, on #890's closing path.
5. **Docs naming the old pin.**
   - Only historical mentions remain: `SPLIT_CONTROL_MEMORY.md:296,306`, `SUBMODULES.md:589`, and `ci/image/exec-audit-receipt.json:4185`, an audit receipt of a recorded tree that the PR names.
   - `submodule_boundaries.gen.py --check` and `check_submodule_docs.py` pass.
   - `git diff --check 1d6bf555 HEAD` gives rc 0.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Gitlink and ancestry (API compare, `merge-base`). `acmp_mbx.c:108-165`, `acmp_mbx.h:28-51,195` against tsn-c-stack `docs/PORTING.md:74-119` and `src/acmp.c:1104-1146,1303-1323` at `715589c`. K1/K2 pass figures. S2 receipts' answer times against Milan v1.2 Table 5.26. Issue scope items 1 to 5 | R829-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| RTL | CLEAN | `git diff --stat 1d6bf555..HEAD -- hdl tb '*.sv' '*.v'` is empty (no RTL in the PR or the stack delta). Loop and adapter contracts: `ctrl_loop.c:121-140` (the rx ready hook in `service_rx`), the `mbx.c:384-388` length guard against `kept.frame[MBX_CH_ACMP_MAX_FRAME_BYTES]`, the widths (`uint16_t len`, `uint8_t interface`), the `ACMP_MBX_PASS_MAX` accounting (`acmp_mbx.h:49-51,177-182`). firmware-verilator PASS (`receipts/gates/ctrl_boundary_only_verilator_captured.log`) | R829-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| Robustness | CLEAN | `acmp_mbx.c:111-165` under probes P1 to P5 and P7, all caught (`receipts/probes/adapter_probes.log`). Malformed, foreign and out-of-range-interface frames are taken, never kept (`src/acmp.c:1108-1116`). Reset (K3; plant `acmp-kept-survives-a-start`). Refused polls offer nothing (K1). Liveness invariant (above) | R829-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| Tests | UNCLEAN (F1 open) | `test_acmp_mbx.cpp:1055,1147-1251`, `acmp_owed_mutants.py`, `acmp_mutants.py`, `acmp_review_mutants.py`, `ctrl_mutants.py`, `plat_arms.py`. All campaigns and suites rerun (Evidence); P6 escape and wake-check demonstration (`receipts/probes`) | R829-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |
| Docs | UNCLEAN (F2 open; RES1 to RES3 are residue) | `docs/design/MAILBOX_SPLIT.md:575-588`, `docs/design/SPLIT_CONTROL_MEMORY.md:286-312`, `docs/reference/SUBMODULES.md`, the four READMEs, `sw/firmware/gtest/coverage.ratchet`, the regenerated diagram. PR body. The author's `verify-final.md` and size receipts against `ci_rv32_sdk.py --verify-only` | R829-1 | `50e2a722ef2671b3f5b017f97b1c7d41705c4f32` |

## Evidence (receipts under this packet, all at the exact head, on the pinned SDK installed from the verified archive)

- **Suites:** `receipts/campaigns/suites-shard0of4.log`, the firmware-unit suite step: `test_ctrl_firmware: PASS`.
- **Control campaign:** `receipts/campaigns/control-NNof12.log`, 579 of 579 caught. Driver: `scripts/phase_slice.py`, using `ctrl_mutants.campaign`'s own shard.
- **AECP campaign:** `receipts/campaigns/aecp-{0,1}of2.log`, 139 ok and 0 escaped.
- **SRP campaigns:** `receipts/campaigns/srp-Nof6.log`, two-interface 202 and one-interface 76 defects, plus the lwSRP pin controls; 280 ok and 0 escaped. Driver: `scripts/srp_slice.py`, mirroring `run_srp_mutants`.
- **Coverage:** `receipts/gates/fw_coverage_selftest.log` and `receipts/gates/fw_coverage_check.log`: PASS, 35 files, every file 100 %.
- **Other firmware-unit steps:**
  - `receipts/gates/test_ctrl_nvm.log`: 435 tests, 5 shapes.
  - `receipts/gates/fw_rv32_selftest.log`: 17 checks.
  - `receipts/gates/tally_selftest.log`, `receipts/gates/ci_rv32_sdk_selftest.log` and `receipts/gates/ctrl_image_selftest.log` (40 checks).
- **firmware-verilator:**
  - The three Verilator builders were captured with `ctrl_capture.py` (`receipts/gates/capture-*.log`: mbx mutants 7/7, MAAP differential 17/17, AECP wire PASS).
  - They were then judged by `ctrl_boundary.py --require-rv32 --selftest --only verilator --capture …`: PASS, 939 compiled sources judged (`receipts/gates/ctrl_boundary_only_verilator_captured.log`).
  - Verilator identity: `receipts/gates/verilator-identity.txt` (5.050 rev v5.050).
- **Docs gates:** `receipts/gates/submodule_boundaries_check.log`, `receipts/gates/check_submodule_docs.log` and `receipts/gates/diff_check.rc` (all rc 0).
- **Size fixture:** `receipts/size/ctrl_image-{pinned,host}-sdk.log`, identical apart from the compiler line, and equal to the author's.
- **SDK provenance:** `receipts/gates/ci_rv32_sdk_{install_scratch,verify_scratch,verify_host_sdk}.log`.
- **Probes:** `scripts/adapter_probes.py` and `scripts/run_acmp_arm.py`, with `receipts/probes/*`.
- **Hosted:** `receipts/hosted-check-runs.tsv`, captured at `receipts/hosted-check-runs.captured-at`. At capture, 8 contexts were completed with success and one skipped (the physical gPTP nightly); the six firmware jobs were queued and 6 contexts were in progress. No hosted firmware job had concluded.
- **Clone restore:** `receipts/restore/clone-restore-check.txt`: HEAD and tree exact, empty status including ignored files, index equal to the HEAD tree, all six gitlinks as recorded, submodules clean.

## Real limits

- **firmware-boundary** (`--without verilator`) was not completed. Its builder set includes `test_ctrl_memory.py --build-only`, which needs migen and LiteX, and this host has neither. The run also exceeded the per-command time cap (`receipts/gates/ctrl_boundary_without_verilator.log`, rc 124; its first three builders exit 0).
- **`test_ctrl_memory.py`** was not run (no migen; `receipts/gates/test_ctrl_memory.log`).
- **Not rebuilt here:** the fixture and platform ROM/RAM ledger images (LiteX runtime archives) and S2's harness images (product LiteX tree). Their figures are checked against the author's receipts and by arithmetic only.
- **Gates run in another form than the hosted one:**
  - firmware-verilator was judged on captures made beside the gate, not on the gate's own builder run. I judged 939 compiled sources; the author's own-capture run reports 1019.
  - The campaigns ran in slices, through the drivers' own table partitions. Their union is the full tables, and the totals match the author's.
- **Toolchain:** this host's GCC 16.2.1 and GoogleTest 1.18 differ from the hosted ubuntu-24.04 image.
- **Not run:** the full sweep, `docs.yml`, `behave`, the builder legs and act are outside this review's allowance. No manager source bank ran at this head, and none is claimed.
- **Hardware:** physical calibration was NOT RUN, and no field skip is hardware proof.

## Pending manager duties

- Exact-head hosted acceptance (the firmware jobs were queued at capture) and act.
- The current-dev candidate on live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09` (builder and native banks).
- The residue checklist (RES1 to RES3).
- A recorded decision on the single-offer redelivery variant (S4).
- The S2b sync: drop the hot list's `__lshrdi3` entry, give the +132 B over-granule figure, and run the flip-check re-grade at 0.75 under #890.
- S15's 32x32 rebuild on this pin.

R829-1 FINISHED
