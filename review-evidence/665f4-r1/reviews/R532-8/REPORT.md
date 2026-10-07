[R532] NEGATIVE - exact head a6e6916826448f81de2b779ca61a87a9f8c47278

Round R532-8: internal, cleared-context, independent delta review of issue #665 / PR #690.

- Head: `a6e6916826448f81de2b779ca61a87a9f8c47278`, tree `819d9290c443690487fbc8123765a14a5ba4535e`.
- Parents: `f74b9403` (F4 Round 7, POSITIVE baseline for F4-only code) and dev `d8b355fe` (F3, PR #688).
- Verdict: **NEGATIVE**. One MAJOR finding and three MINOR findings are open. Conformance, RTL and Robustness are CLEAN. Tests and Docs are UNCLEAN.

The merge itself is sound. Both parents' tests and planted defects are retained. SRP is composed beside ADP, ACMP and MAAP with an exact receive and event interrupt mask. The SRP-only wake and the six new plants work at one and two interfaces. The pass bound and the T_svc table recompute exactly. R532-7-R1 is fixed, and the merge carries no RTL, register-map or mailbox-contract change.

The verdict is NEGATIVE for four reasons:

- **F1:** the required hosted `firmware-unit` job, and so `rtl-fast`, fails at this exact head. An inherited ACMP planted defect is detected only through an out-of-bounds stack read, and on the hosted toolchain it escapes.
- **F2:** the merge's new SRP pass bound has no check that can fail when the bound is too small.
- **F3:** one README still gives the redefined `CTRL_APP_PASS_MAX` its old value.
- **F4:** one README overstates which of the new checks have planted defects.

## 1. Reconstruction (public state only)

I read the following in the required order:

1. `AGENTS.md` and `CONTRIBUTING.md` (lenses, severity, completion bar), then `docs/README.md`.
2. Issue #665's round-8 assignment ([comment 6045716528](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6045716528)):
   - `--no-ff` merge of dev `d8b355fe`, keeping F3's explicit ADP + ACMP + MAAP composition and F4's SRP;
   - SRP composed the way MAAP is: attach order, `FILTER_EN`, SRP's receive interrupt beside the ADP, ACMP, MAAP and event bits, and disjoint timer slots;
   - U6/F6 extended for an exact IRQ mask, an idle wake on an SRP record, and `CTRL_APP_PASS_MAX` tied to the four module bounds less the shared event reads;
   - a planted defect for each new check at one and two interfaces;
   - the `MAILBOX_SPLIT.md` table and T_svc paragraph updated;
   - R532-7-R1 fixed exactly;
   - the listed gates; and a STOP if an RTL, register-map or mailbox change were needed.
3. REVIEW READY ([comment 6046592070](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6046592070)) and the review start (PR comment 6046622298).
4. Authorities: `docs/design/MAILBOX_SPLIT.md` (ACMP service latency, open items) and `sw/firmware/ctrl/mbx/mbx_contract.h` (channel indices, `IRQ_ENABLE` and `FILTER_EN` fields).
5. Headers and READMEs: `loop/ctrl_loop.h`, `app/ctrl_app.h`, `acmp/acmp_mbx.h`, `maap/maap_mbx.h`, `srp/srp_mbx.h`, and the `ctrl`, `srp` and `maap` READMEs.
6. The diff `d8b355fe..a6e69168`, the diff `f74b9403..a6e69168` and the merge's remerge-diff (`receipts/remerge-diff.txt`). The remerge-diff shows exactly what the resolution changed relative to an automatic merge, including all six conflicted files.
7. Public executable evidence: the author's `review-evidence/665f4-r1/author-r8` at `60ce747f` (GATES, ROUND8-GATES, ROUND8-COVERAGE, ROUND8-SIZES), the live PR body, and the exact-head hosted check runs.

I read the prior public review verdicts only after my own pass over the diff was complete (section 4).

## 2. Merge review against both parents

| Item | Result | Evidence |
|---|---|---|
| (1) F3 and F4 both intact; no test dropped | **Met** | Every `TEST`/`TEST_F` name of both parents exists at the head (`receipts/tests-*.txt`: 281 F4, 295 dev, 381 head, none missing). Every planted-defect name of both parents is retained, and exactly six are new: the `four-way-*` plants (`receipts/plants-*.txt`). `srp_mbx.c`/`.h`, the loop, the port layer, the SRP suites and the lwSRP gitlink are byte-identical to `f74b9403`. `ctrl_image.py` is byte-identical to dev. F4's auditor became `ctrl_srp_image.py`, now with ACMP in its fixture (`test/ctrl_image.c:15-22`, `:55`, `:61-67`). In the merged `ctrl_mutants.campaign` (`ctrl_mutants.py:531-578`), dev's slice and F4's stable work path are combined. `--mutation-shard` now partitions inside the campaign, while "unnamed tests" is still computed over the full table. |
| (2) IRQ mask, wake, timers, shared tick, IF=1/2, six plants | **Met** | `app/ctrl_app_srp.c:13-20` enables RX for ADP, MAAP, SRP and, when composed, ACMP, plus EVT, as a replacing write (`mbx.c:328`). It also enables the tick and opens the same channel set as the filter. Bits are within the 8-bit RX field; SRP is channel 4 (`mbx_contract.h:123-129`, `:709`). `srp_mbx.c` arms no one-shot slot (no `mbx_timer_arm`); it takes one tick consumer (`srp_mbx.c:745`), and `CTRL_LOOP_MAX_TICKS`/`SINKS`/`POLLS` have room (`ctrl_loop.h:75-77`). U6 checks the exact four-channel filter and mask, the attach order and `n_ticks == 1` (`test_acmp_mbx.cpp:1145-1155`). `wake_on_srp()` (`:1080-1103`) injects only an SRP record from the sleeping HAL after checking that no interrupt is pending. The full campaign catches all six plants at IF=2 and again at IF=1 (`receipts/ctrl-selftest.log`). My own plants on the ACMP-absent branch and on the tick enable are caught by `srp_app.cpp` at IF=1/2 (`receipts/probe-attach-*.log`). |
| (3) `CTRL_APP_PASS_MAX` = four bounds less shared event reads (3,128 / 3,977), runtime tie, MAILBOX_SPLIT recompute | **Met** (test weakness F2) | From the exact-head headers (`receipts/pass-bounds.txt`): IF=1 ACMP 1,012 + MAAP 616 + SRP 1,596 − 2×48 = 3,128; IF=2 1,043 + 664 + 2,366 − 96 = 3,977. Both the independent sum and the macro agree. The tie is `test_acmp_mbx.cpp:1041-1043`. All eight table cells (floor to 0.01 us as stated), both statements on what fits and the open-items figures recompute (`receipts/tsvc-table.txt`). I traced every mailbox access in `srp_mbx.c` against `srp_bounds.h`: LINK event 1 (`:594`); receive readiness `IRQ_STATUS` 1 plus a refused receive's `NOW_MS` 1 (`:350`, `:391`); per interface LINK 1, `RX_HEAD` mark 1, `IRQ_STATUS` 1 and `NOW_MS` 1 (`:643`, `:594`, `:350`, `:391`); at most 2×`MBX_N_IF` `mrp_transmit` calls, each costing at most `mbx_tx_send`'s 1 + 2 + payload + 1 (`mbx.c:203-227`); ticks make no access. The derivation holds, but no executable check can falsify it (F2). |
| (4) R532-7-R1 | **Met** | `srp/README.md:64` reads "Retry after owed transmission commits and retained reception completes or expires.", the same as `srp_mbx.h:97-98`. The sentence moved from `:59` because lines were added above it. The optional R532-7-S1 is addressed at `:38`. |
| (5) No RTL, mailbox-contract or register change beyond dev | **Met** | `git diff d8b355fe..HEAD -- hdl rtl tb sw/mailbox docs/reference/MAILBOX_CONTRACT.md sw/firmware/ctrl/mbx/mbx_contract.h '*.sv' '*.v' '*.yaml'` is empty. `gen_mailbox.py --check` reports 0 findings (`receipts/docs-gates.log`). |
| (6) Gates at `a6e69168` | **Met locally; hosted firmware-unit failed (F1)** | See section 5. |

## 3. Findings

### R532-8-F1 | MAJOR | Tests | `sw/firmware/ctrl/test/test_acmp.cpp:208-213` with plant `acmp-init-too-many-sources` (`test/acmp_mutants.py:26-28`); hosted job 113011249325 | A planted defect is detected only through an out-of-bounds stack read, and the required hosted gate fails at this head

- **Authority/evidence:**
  - `AGENTS.md` §6 Tests requires that each test "can fail for the defect it claims to detect". §7 requires a successful `rtl-fast` verdict at the current PR head.
  - The hosted `firmware-unit` job ran on `pull_request` with head_sha `a6e69168` ([run 37685180789](https://github.com/kebag-logic/milan-fpga/actions/runs/37685180789/job/113011249325)). It used gcc 13.3.0 and GoogleTest 1.14.0 and reports `[ESCAPED] mutant acmp-init-too-many-sources (acmp): 0 check(s) failed`, then `mutants: 468 of 469 caught` and `test_ctrl_firmware: FAIL`. The saved-state and coverage steps were skipped and `rtl-fast` concluded failure (`receipts/hosted-firmware-unit-escape.txt`, `receipts/hosted-checks.txt`).
  - Both parents' hosted `firmware-unit` passed (`d8b355fe`: job 112986324471; `f74b9403`: job 112866215042).
- **Cause:**
  - The plant relaxes `cfg->n_sources > ACMP_MAX_SOURCES` by one. A0 then calls `acmp_init` with `n_sources = 17`, and the loop at `acmp/acmp.c:979-983` reads `source_interface[16]`. That array is the last member of `struct acmp_config` (`acmp/acmp.h:274-282`, struct size 88 with no tail padding), so the byte is outside `bad`, on the stack.
  - Whether the plant is caught depends on that byte. If it happens to be at least `n_interfaces`, `acmp_init` refuses through another check and A0 passes.
  - My probe (`receipts/probe-acmp-a0.log`): the unplanted tree passes under gcc 16, gcc 16 with AddressSanitizer, and clang. The planted tree is caught by local gcc and clang, but under AddressSanitizer it aborts with `stack-buffer-overflow` in this test.
  - The sink case of the same test avoids this by placing the read on `n_sources` (`test_acmp.cpp:203`); the source case has no such guard.
- **Impact:** the required fast verdict is red at the exact head, so the completion bar cannot be met. Detection of this plant changes with stack layout and toolchain, which is the case the merged layout exposed. A rerun of the same binary will most likely fail the same way.
- **Required outcome:** catching `acmp-init-too-many-sources` must not depend on memory outside the configuration object, for example through a fixture whose 17th source-interface byte lies in owned, controlled storage. Hosted `firmware-unit` must then pass at the new head.
- **Verification:**
  - Run the planted tree under AddressSanitizer with no stack overflow and the A0 sources check failing by name (`scripts/probe_acmp_a0.py`).
  - Run the full campaign locally and in hosted `firmware-unit` with 469/469 caught.
  - `rtl-fast` succeeds at the new head.

### R532-8-F2 | MINOR | Tests | `sw/firmware/ctrl/srp/srp_bounds.h:8-17` (new in the merge); `test/test_acmp_mbx.cpp:1035-1043` | The new SRP pass bound has no check that can fail if it is understated

- **Authority/evidence:**
  - `SRP_MBX_PASS_MAX` (1,596 / 2,366) and its terms are introduced by the merge commit. They feed `CTRL_APP_PASS_MAX` and every row of the new `MAILBOX_SPLIT.md` table.
  - The only checks are the algebraic `EXPECT_EQ` (`:1041`), which restates the macro definition, and the measured four-way worst pass. That measurement is 265 / 260 accesses against 3,128 / 3,977 (`receipts/ctrl-selftest.log`).
  - Each sibling module bound has a measured check, and F3 plants an understatement against it: `test_adp.cpp:1047`, `test_acmp_mbx.cpp:840` with plant `acmp-pass-bound-understated`, and `test_maap_mbx.cpp:171` and `:367`.
  - Four reviewer plants each understate `srp_bounds.h`: drop all SRP transmits from the poll term, drop SRP's receive and poll terms entirely, zero `SRP_MBX_RX_MAX`, or zero `SRP_MBX_EVENT_MAX`. All four pass every suite that compiles the header (`test_acmp_mbx.cpp` with SRP and `srp_app.cpp`, at IF=1 and IF=2). The unmodified control passes too (`receipts/probe-srp-*.log`, `receipts/probes.summary`; in the driver's wording, "ESCAPED" means every suite passed).
  - My manual trace (section 2, row 3) finds today's figures correct, so this is a test gap, not a wrong bound.
- **Impact:** a later access added to `srp_mbx.c`, or a wrong term, silently invalidates the published four-module T_svc envelope.
- **Required outcome:** an executable SRP measurement that fails when any of these terms is understated, as MAAP's per-term and full-pass checks do: for example the event, refused receive and poll paths, including a poll that transmits. Each such check needs a named planted understatement at IF=1 and IF=2.
- **Verification:** `scripts/probes.sh` reports all four `srp-*` plants CAUGHT, the control still passes, and the new plants are caught in the campaign.

### R532-8-F3 | MINOR | Docs | `sw/firmware/ctrl/maap/README.md:134-135` | `CTRL_APP_PASS_MAX` is still given its old three-module value

- **Authority/evidence:** the README says "Composed with ADP and ACMP, a pass costs at most `CTRL_APP_PASS_MAX` (`ctrl_app.h`): 1,580 accesses for one interface, 1,659 for two." At this head that macro is the four-module bound, 3,128 / 3,977 (`app/ctrl_app.h:72`, `receipts/pass-bounds.txt`). The 1,580 / 1,659 figure is `CTRL_APP_THREE_PASS_MAX` (`app/ctrl_app.h:69`). The text came from dev (`d7e5fee5`) and became false when the merge redefined the macro. The merge renamed the other references (`ctrl/README.md:108`, `MAILBOX_SPLIT.md:693`, `acmp_review_mutants.py:412`) but not this one. Two code comments name the macro with the same stale meaning: `test/test_acmp_mbx.cpp:20` and `test/acmp_review_mutants.py:398`.
- **Impact:** an authoritative module page attributes a wrong figure to a code constant. A reader would treat the 3,128-access bound as 1,580.
- **Required outcome:** `maap/README.md` attributes 1,580 / 1,659 to `CTRL_APP_THREE_PASS_MAX`, or states the four-module figure for `CTRL_APP_PASS_MAX`. The two comments name the macro their build actually uses.
- **Verification:** grep `CTRL_APP_PASS_MAX` across the tree. Each occurrence must denote the four-module bound or carry the four-module value.

### R532-8-F4 | MINOR | Tests, Docs | `sw/firmware/ctrl/README.md:133-136` | "Each added check has a named planted defect" is not true

- **Authority/evidence:** the paragraph lists "exact interrupt mask, an idle HAL awakened by SRP alone, ordered attachment, disjoint timer slots, full receive backlogs and the algebraic pass bound". It then states that "Each added check has a named planted defect."
  - Plants exist only for the mask (`U6 exact four-channel …`, `U6 four receive channels …`), the wake (`U6 idle loop wakes for SRP alone`) and the algebraic tie (`F6 four modules count …`).
  - No plant in any mutant table names these new checks:
    - `U6 SRP attaches after ADP ACMP MAAP and uses the shared tick` (ordered attachment);
    - `F6 SRP backlog drains after the event prefix` and `F6 SRP backlog drains` (full receive backlogs);
    - `U6 waking consumes the SRP record`;
    - `U6 loop really slept`;
    - `F6 the worst pass of the four-way backlog`.

  This was checked by grepping the needles across `*mutants*.py` at the head. The PR body's own Round 8 list is accurate; the README is not.
- **Impact:** a false statement about mutation evidence in the authoritative gate page. A reader would believe the attach-order and backlog-drain checks have proven failure power.
- **Required outcome:** either add named plants for the checks the sentence covers, at IF=1 and IF=2, or narrow the sentence to the mask, wake and bound checks that have them.
- **Verification:** each check named in that paragraph maps to a plant caught in the campaign log.

### Residue (wording only; the manager carries these to the residue checklist)

- **R532-8-R1** | RESIDUE | Docs | `sw/firmware/ctrl/README.md:44`. "the static composition a platform starts, in two calls: compose, then open" omits the SRP attachment the same page now requires. Exact fix: "the static composition a platform starts: compose, then open, then `ctrl_app_attach_srp` for SRP".
- **R532-8-R2** | RESIDUE | Docs | `sw/firmware/ctrl/README.md:335-336`. "lwSRP's pool is the host tests' 256 bytes until F4 sizes it" is stale now that F4 is merged. Exact fix: "lwSRP's pool is the host tests' 256 bytes in this fixture; `ctrl_srp_image.py` measures the entity-sized pool".

### Suggestions (non-blocking)

- **R532-8-S1** | Tests | `test/test_acmp_mbx.cpp:1025`, `:966`. In the SRP build, the F6 printout still says "three-way backlog" and the test name still says "ThreeWayBound". Label the build that prints.
- **R532-8-S2** | Docs, Robustness | `app/ctrl_app.h:125`. "After open (or start_maap)" does not say that `ctrl_app_attach_srp` refuses unless MAAP is composed (`app/ctrl_app_srp.c:9`); state that requirement.
- **R532-8-S3** | Docs | `sw/firmware/ctrl/README.md:391-406`. The F3 linked-size table and static-object figures are correctly scoped to "lane F3 round 6". At this head `ctrl_image.py` measures 8x8 text 33,472 and bss 22,800, with app 7,928 and loop 1,768, against the table's 33,448 / 22,784 / 7,904 / 1,748 (`receipts/image-f3-ctrl_image.out`). Consider noting that the merged head differs, or refreshing the figures.

## 4. Prior public findings at this head

| Prior finding | Status at `a6e69168` |
|---|---|
| R532-7-R1 (RESIDUE, `srp/README.md:59` omits expiry) | **Resolved**: `srp/README.md:64`, exact wording. |
| R532-7-S1 (SUGGESTION, `refused` counts attempts) | **Addressed**: `srp/README.md:38`, which matches each refused attempt being counted (`srp_mbx.c:377`, `:657`). |
| R533-7-R1 (RESIDUE, live PR body "After the manager publishes …") | **Retained**: the live PR body still reads "After the manager publishes the new head, use this checkout recipe." Exact fix as published: "Use this checkout recipe." |
| R532-1..6 and R533-1..6 findings | These were closed by the Round 7 POSITIVE verdicts at `f74b9403`, which are the baseline. The merge does not touch `srp_mbx.c`/`.h`, the loop, the port layer or the SRP suites, so none is reopened. |

## 5. Executable evidence (this reviewer, at `a6e69168`)

Every result below was produced on this host by commands in `scripts/`. Logs are in `receipts/` with paths normalized to `$PACKET`, `$CLONE`, `$HOME` and `$TOOLS`.

| Gate | Result |
|---|---|
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --lwsrp <pinned submodule> --build-dir …`, with the pinned SDK | rc 0, 1529 s. 51 arms pass (IF=1/2, all five shapes, RV32 objects, processor-wire walks). 469/469 control plants are caught. 114 SRP plants are caught: 108 at IF=2 plus the 6 four-way plants at IF=1. Both lwSRP pin controls refuse. Local toolchain: gcc/g++ 16.2.1, GoogleTest 1.18.0 (`ctrl-selftest.log`, `.rc`). |
| `fw_coverage.py --selftest` / `--check --lwsrp … --jobs 4` | rc 0 / rc 0: 28/28 planted cases, and 22 files at 100 % lines and branches after the existing exclusions. This includes `ctrl_app_srp.c` 12/12, 8/8 and `mbx.c` 189/189, 74/74, matching `coverage.ratchet` (`cov-*.log`). |
| Pinned RV32 SDK `riscv32-ilp32d--glibc--stable-2025.08-1` (archive sha256 `d42680e9…`), fresh install verified | rc 0 (`sdk-install.log`). |
| F3 `ctrl_image.py` (both shapes), `ctrl_image_selftest.py --require-rv32`, `fw_rv32_selftest.py --require-rv32` | rc 0, 33/33 image controls, 17/17 RV32 controls (`images.log`, `image-f3-*.out`, `rv32-selftest.out`). |
| F4 `ctrl_srp_image.py` at 1x1 and 8x8, IF=1 and IF=2 | rc 0. RAM spans 77,376 / 90,064 / 92,080 / 119,536 match the author's `ROUND8-SIZES.json` exactly. Runtime archives were rebuilt from provisioned Picolibc, compiler-rt and LiteX sources. All 58 compiled inputs match the author's published runtime record (`ROUND7-RUNTIME.json` at `60ce747f`) by SHA256. The two archives match by size; `ar` embeds member timestamps (`images.log`, `runtime-provenance.json`, `image-srp-*.size.json`). |
| Mailbox suite, `make -C tb/verilator/mbx` with pinned Verilator 5.050 (wrapper sha256 `905795b9…`, reports `rev v5.050`), on an exported copy of the head | rc 0. WB 382, AXI 427, cosim 32, IF=2 WB 384, AXI 429, model 369, all with zero failures; 5/5 mailbox plants caught (`mailbox.log`). |
| Docs: `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `gen_mailbox.py --check`, `check_baremetal_only.py --check`; with the pinned Markdown renderer, `check_em_dash.py --base d8b355fe`, `gen_toc.py --check`, `gen_toc.py --verify-anchors` | rc 0. The first three Markdown attempts without the renderer were refusals ("cannot judge"); they are superseded by the reruns in the same log (`docs-gates.log`). |
| Reviewer probes | `probe_mutants.py` / `probes.sh`, run on a scratch clone of the head with submodules linked read-only: control passes; 2 attach plants caught; 4 SRP-bound plants escape (F2). `probe_acmp_a0.py`: A0 overflow under AddressSanitizer (F1). |
| Clone integrity after all runs | Index tree = HEAD tree `819d9290…`. 1,208 tracked blobs match by bytes and mode. Status is clean, with no ignored files. Gitlinks: lwSRP `9197193e`, protocol-processor `ead80360`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, external `efeb541a` (uninitialized). Submodule worktrees are clean (`clone-integrity.txt`). |

## 6. Lens results

- [R532] PASS Conformance — `app/ctrl_app_srp.c:9-21`, `app/ctrl_app.h:58-73`, `srp/srp_bounds.h:8-17`, `docs/design/MAILBOX_SPLIT.md:715-742`, `srp/README.md:38,64`, `git diff d8b355fe..HEAD -- hdl tb sw/mailbox …` (empty) — Checked every round-8 acceptance item against the assignment: the merge parents; the attach order; `FILTER_EN` and IRQ with SRP beside ADP, ACMP, MAAP and EVT; disjoint slots with SRP on the shared tick; U6/F6 extended; six plants at IF=1/2; 3,128 / 3,977; all table cells; R1 exact; no RTL or contract change; local gates rc 0. The hosted gate failure is F1 (Tests).
- [R532] PASS RTL — `mbx_contract.h:35,123-129,461-719`, `mbx.c:93-95,203-227,304-327`, `loop/ctrl_loop.c:66-86`, `loop/ctrl_loop.h:75-79`, `srp/srp_mbx.c:346-411,584-730` — Checked the mask field widths and channel indices; the replacing-write semantics of `IRQ_ENABLE` and `FILTER_EN`, consistent with `ctrl_loop_open`; that the attach adds no sink, poll or tick beyond the loop limits; and every SRP mailbox access against each `srp_bounds.h` term. No RTL, register or contract change. The mailbox suite (RTL and cosim) passes with pinned 5.050.
- [R532] PASS Robustness — `test/srp_app.cpp:6-20,22-80`, `test/test_acmp_mbx.cpp:1080-1103`, `receipts/probe-attach-acmp-always.log`, `probe-attach-no-tick.log` — Checked the refusal paths (attach without ADP or MAAP, double attach), which leave the composition intact; the ACMP-absent branch with an exact three-channel mask; the tick enable; wake only on SRP with nothing else pending; and IF=1/2. Mutations of the ACMP branch and of the tick enable are caught at both interface counts.
- Tests — **UNCLEAN**: F1 (MAJOR), F2 (MINOR) and F4 (MINOR) are open. Artifacts examined: `test_acmp_mbx.cpp:930-1155`, `srp_mutants.py:611-645`, `test_ctrl_firmware.py:114-205`, `ctrl_mutants.py:531-578`, `test_acmp.cpp:190-213`, campaign and coverage logs, hosted job 113011249325.
- Docs — **UNCLEAN**: F3 (MINOR) and F4 (MINOR) are open. R1 and R2 are wording residue. Artifacts examined: `ctrl/README.md:1-410`, `srp/README.md:30-70,160-200,250-262`, `maap/README.md:126-136`, `MAILBOX_SPLIT.md:660-742,970-990`, `gtest/README.md:400-430`, the live PR body.

## 7. Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Assignment items 1-4 vs `ctrl_app_srp.c`, `ctrl_app.h`, `srp_bounds.h`, `MAILBOX_SPLIT.md:715-742`, `srp/README.md:64`, empty RTL/contract diff, `receipts/pass-bounds.txt`, `tsvc-table.txt` | R532-8 | `a6e6916826448f81de2b779ca61a87a9f8c47278` |
| RTL | CLEAN | `mbx_contract.h`, `mbx.c`, `ctrl_loop.c/.h`, `srp_mbx.c` access trace, mailbox suite with pinned 5.050 | R532-8 | `a6e6916826448f81de2b779ca61a87a9f8c47278` |
| Robustness | CLEAN | `srp_app.cpp`, U6 wake path, refusal and ACMP-absent branches, attach probes at IF=1/2 | R532-8 | `a6e6916826448f81de2b779ca61a87a9f8c47278` |
| Tests | UNCLEAN (F1 MAJOR, F2, F4) | U6/F6, six plants, merged campaign drivers, A0, full campaign, coverage, hosted firmware-unit | R532-8 | `a6e6916826448f81de2b779ca61a87a9f8c47278` |
| Docs | UNCLEAN (F3, F4) | ctrl/srp/maap/gtest READMEs, `MAILBOX_SPLIT.md`, live PR body | R532-8 | `a6e6916826448f81de2b779ca61a87a9f8c47278` |

## 8. Real limits

- These are host-model and native results only. Physical calibration was NOT RUN; no hardware, target CPU timing or booted image is involved. The linked images are size fixtures.
- I did not run the full parent, protocol-processor, gPTP, Yosys or builder banks, the saved-state campaign, the MAAP differential or the docs bank beyond the listed checks. Those are the manager's evidence at this head.
- My hosted-check reading is a snapshot (`receipts/hosted-checks.txt`). At that time `docs-check` and three Verilator shards were still in progress. "Physical gPTP" was skipped, which is not an executed result.
- The local toolchain differs from hosted (gcc 16.2.1 / GoogleTest 1.18.0 vs gcc 13.3.0 / 1.14.0). F1's escape was not reproduced with the hosted compiler; it is shown by the hosted log plus the local AddressSanitizer overflow.
- The SRP image runtime was built from locally provisioned sources, checked by hash against the author's public record rather than fetched independently.
- The probes ran from a scratch clone of the head with submodules linked read-only. They plant only into scratch copies.

## 9. Pending manager duties

- Hosted acceptance at this head, including F1's red `firmware-unit`/`rtl-fast`, and trusted local replication.
- The external review's verdict, the current-dev candidate merge validation and containment.
- Carrying residue R532-8-R1, R532-8-R2 and the retained R533-7-R1 to the residue checklist.
- Publishing this report and the listed receipts.

R532-8 FINISHED
