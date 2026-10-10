[R585] NEGATIVE - exact head d1b22e804158cbcb33fa12116d60e982f9a4c55b

# R585-3: external review of PR #705 (issue #697, lane 697c), round 3

- **Head:** `d1b22e804158cbcb33fa12116d60e982f9a4c55b`, tree `bc319e0b59aa24fb561d51a13da5da7b43a9d676`.
- **Delta reviewed:** `386b8e69..d1b22e80`, three commits (`76c0e27c`, `36699f6c`, `d1b22e80`). The full PR diff from source base `8b61b709` was the context. Earlier rounds stand.
- **Verdict: NEGATIVE on one MAJOR.**
  - The round-3 code closes every round-2 finding. Every probe I re-ran is refused by name.
  - Images, coverage and kills are unchanged. My local gate self-test passes.
  - But the required hosted `firmware-unit` job did not finish at this head. It hit its 45-minute limit inside the boundary step that this delta grew. The saved-state suites and the coverage ratchet were skipped, and `rtl-fast` reports failure (R585-3-F1).
- **Also recorded:**
  - Two new SUGGESTIONs (R585-3-S1, R585-3-S2).
  - One retained SUGGESTION (R585-2-S2).
  - One RESIDUE in the PR body (R585-3-RS1).

## 1. Findings

### R585-3-F1 - MAJOR - Conformance, Robustness, Tests - the hosted `firmware-unit` job exceeds its 45-minute limit at this head, inside the boundary step this delta grew

`[R585] MAJOR Conformance/Robustness/Tests — .github/workflows/rtl-fast.yml:251,294-295; sw/firmware/ctrl/test/ctrl_boundary.py:749-761,797-806 — required firmware-unit cancelled by its timeout at the exact head`

**Authority**
- AGENTS.md section 7 requires a successful `rtl-fast` verdict at the current PR head. It also says an existing regression must stay green (section 6, `Tests`).
- The lane scope ([6091228902](https://github.com/kebag-logic/milan-fpga/issues/697#issuecomment-6091228902), item 4) says every hosted job that needs the stack must run, and "nothing may silently skip".
- `docs/testing/CI_WORKFLOWS.md:42-47` says `firmware-unit` runs the store suites and the coverage ratchet. They did not run at this head.

**Evidence** (`receipts/firmware_unit_hosted.txt`, `receipts/firmware_unit_d1b22e80_boundary_step_excerpt.txt`, `receipts/check_runs_d1b22e80.tsv`)
- Job [114173809799](https://github.com/kebag-logic/milan-fpga/actions/runs/38038455090/job/114173809799) ran for the `pull_request` event at `d1b22e80`. It ended `cancelled` with the annotation "The job has exceeded the maximum execution time of 45m0s".
- Step 9, "Hold the TSN stack boundary in both directions", ran from 09:10:09 to 09:22:39 and was cancelled.
  - All 45 boundary controls and all 20 pin controls passed. The last pin control finished at 09:22:25.
  - The job was cancelled during the checkout's own judgement and the stack's gate, so the boundary never gave a verdict at this head.
- Step 10 (the saved-state store suites and their RV32 build) and step 11 (the coverage ratchet) were skipped. The `rtl-fast` aggregate reads `failure`.
- Step timings at the two heads:

| Step | `386b8e69` ([job 114137888898](https://github.com/kebag-logic/milan-fpga/actions/runs/38026314581/job/114137888898), success) | `d1b22e80` (job 114173809799) |
|---|---|---|
| 8, firmware suites and RV32 builds (not changed in this delta) | 19:04 | 32:12 |
| 9, the boundary (changed in this delta) | 2:51 | over 12:30, cancelled (the self-test phase alone took 12:16) |
| 10 and 11, store suites and coverage ratchet | 1:01 and 2:28 | skipped |
| whole job | 25:50 | 45:00, timed out |

- Step 8's code is unchanged, so its 1.69x slowdown is runner variance and not this delta.
  - Scaled by that factor, step 9 still grew about 2.5x, from 2:51 to at least 7:24, before its checkout judgement and the stack's gate even ran.
  - Locally, the round-3 self-test took 609 s (`receipts/runs/gate_selftest.rc`). The author measured 630 s.
- The cost comes from the controls loop (`ctrl_boundary.py:749-761`). Each of the 45 plants runs a full `judge()` over both trees, host, RV32 and C++ (942 preprocessings at the checkout, 4 at a time, `JOBS = 4`, line 160). The pin controls then run every reaching bench target for real (`ctrl_pin.py:179-224`).
- At `386b8e69`, a runner this slow would have needed about 43.7 min (25:50 x 1.69), already close to the limit. This delta adds the rest.
- The PR body flags the risk ("not yet measured on a hosted runner"). Nothing raised the budget or reduced the cost before the push.

**Impact**
- The protected `firmware-unit` context is red at the exact head.
- At this head, nothing hosted measured the coverage ratchet, the saved-state suites, or the boundary's own verdict on the checkout.
- A re-run on a faster runner may pass, but the margin is gone. Any slow runner will cancel the same job again.

**Required outcome**
- `firmware-unit` completes successfully at the exact merge-candidate head, every step executed and none skipped.
- It does so with a margin that holds across the observed runner spread. The repository's precedent is 10% (the [#387 decision](https://github.com/kebag-logic/milan-fpga/issues/387#issuecomment-5819379503) cited at `CI_WORKFLOWS.md:299`).
- Either cut the boundary step's hosted cost or give it a measured budget. Examples: parallelism sized to the runner, sharing the variants and C library closure across controls, or a job of its own. Document the measured worst case and the margin in `CI_WORKFLOWS.md`.
- The design is the author's choice. No test or control may be dropped to fit the budget.

**Verification**
- An exact-head `firmware-unit` run that is green, with steps 9, 10 and 11 executed.
- Its step durations recorded against the stated budget and margin.
- `ctrl_boundary.py --require-rv32 --selftest` still reports 45 boundary and 20 pin controls (or more), with 0 misbehaved.

### R585-3-S1 - SUGGESTION - Robustness - a flag that is neither a literal nor an f-string is neither derived nor refused

`ctrl_configs.py:155-191` reads only these forms:
- a Python string literal that is a whole flag, or a bare `-D`/`-U` literal next to the macro;
- an f-string;
- whitespace-separated Makefile words.

Probes (`scripts/boundary_probes3.py`, `receipts/runs/probes3_c.log`) plant `#ifdef <M>` with `#include "mbx_hal.h"` in the stack's `src/adp.c`. The builder that writes `<M>` takes four forms, and each one ESCAPED (no finding):
- `$(addprefix -D,$(MODES))` in a Makefile;
- `-D$(MODE)` in a Makefile;
- `"-D" + MODE` in Python;
- `"-D%s" % "..."` in Python.

The two Python forms the gate does read are handled as stated:
- a bare `-D` before a name is refused: "writes -D before a macro it computes";
- an f-string macro is refused: "computes a -D or -U flag's macro".

No builder uses any of the escaped forms at this head (`receipts/builder_flag_forms.txt`, empty). Every mode the builders write today is derived, so the round-3 requirement holds.

But `sw/firmware/ctrl/README.md:96-98` states the general case: "A flag a builder computes at run time is a value", and "a unit that tests any other computed value is refused". That is true only of the forms listed in `ctrl_configs.py:17-19`.

Consider two by-construction closures:
- read a Makefile builder's flags from make's own dry run, as `ctrl_pin.py` already reads its recipes;
- refuse any Python string constant that starts with `-D` or `-U` and is not a whole flag or a recognised pair.

Or narrow README line 96 to the forms the gate reads.

### R585-3-S2 - SUGGESTION - Robustness - one C++ source a builder names is not followed

`ctrl_configs.cxx_sources` (`ctrl_configs.py:392-408`) resolves a named source against the builder's directory, `test/`, the stack, the checkout root and the processor. It never resolves against `sw/firmware/ctrl`.

So `maap_differential.py:36` names `ctrl / "test/test_maap_differential.cpp"`, and that source is never followed (`receipts/cxx_names.txt`). The docstring at `ctrl_configs.py:32` says "every C++ source a builder names".

Real path (`scripts/cxx_unfollowed_probe.py`, `receipts/runs/cxx_unfollowed.log`). In a disposable clone, I added a new firmware header `maap/maap_probe.h` whose `#ifdef __cplusplus` region includes the stack's `examples/adp_port.h`:
- included from `test/test_maap_differential.cpp`: **ESCAPED**;
- included from `test/test_maap_mbx.cpp` (the control): **CAUGHT**, with "firmware c++: maap/maap_probe.h includes tsn-c-stack/examples/adp_port.h".

There is no effect at this head:
- that source reaches no firmware header, since its include path holds no firmware directory (`maap_differential.py:29-30`);
- all 24 firmware headers are judged as C++ through other sources (`receipts/cxx_names.txt`).

Consider resolving names against the ctrl tree as well, and refusing a C++-suffixed literal that resolves nowhere unless the builder generates it. `aecp_wire.py`'s `sim_main.cpp` and `reference.cpp` also resolve nowhere today.

### R585-2-S2 - SUGGESTION - Robustness - retained

`aecp_arms.py:144` pins `args.stack`, but `aecp_arms.py:83` still compiles with `-I{STACK_TESTS}`, the submodule's `tests/`. The delta does not touch this, and the PR body's Known limitations lists it as not addressed. It stays optional.

### R585-3-RS1 - RESIDUE - Docs (PR body only) - the Status and Known-limitations lines describe hosted runs that have since happened

The PR body changes no measurement, test or code. Its own wording is now stale:
- Status: "Round 3 is not pushed, so no hosted run covers it yet." PR #705's head is `d1b22e80`, and `rtl-fast` ran at it.
- Known limitations: "630 s here, on a shared host, not yet measured on a hosted runner."

Exact fix:
- Status sentence: "Hosted checks at `d1b22e80`: `firmware-unit` was cancelled at its 45-minute limit inside the boundary step (job 114173809799), so `rtl-fast` failed; see R585-3-F1."
- Known-limitations sentence: "measured on a hosted runner at `d1b22e80`: the step ran more than 12 min and the job exceeded 45 min (job 114173809799)."

Update both again once F1 is fixed.

## 2. Prior public findings at this head

| Finding | Status at `d1b22e80` | Evidence |
|---|---|---|
| R585-2-F1 = R584-2-F1: firmware headers judged only as C, and the image only at 1/1 | **Resolved.** n1 and n2 (C++-only includes in `acmp_mbx.h` and `adp_mbx.h`) and n3 (`#if IMAGE_SINKS > 1u` reaching `src/acmp.c`) are CAUGHT by name. So are this round's s1 (the stack-example form of the shape probe), s2 (`IMAGE_SOURCES == 9u`), c1 and c2 (`#ifdef __cplusplus` reaching an example and a test fake), g1 (C++ and a mode) and g2 (C++ and a shape, labelled `shape=endstation_ax7101_8x8`). The gate's own controls for both forms pass. | `receipts/runs/probes_r2.log`, `probes3_a.log`, `probes3_g.log`, `gate_selftest.log` |
| R585-2-F2 = R584-2-F2: `run-if2` builds against the stack unpinned | **Resolved.** `WIRE-mbx_run_if2` exits 2 with "differs from the pinned 1a9f651c: include/wire.h". These also refuse on the pin, and none compiles the poisoned header: `make all` serial and `-j16`, `-k all`, `-j16 run-if2`, `run-cosim`, `obj_fw/libctrlfw.a`, an `assume-unchanged` poison, and a `tests/` edit behind a library that is already built. | `receipts/runs/pin_r2.log`, `pin3.log`, `pin_all.log` |
| R585-2-S1 = R584-2-S1: a mode written as two arguments | **Resolved.** The Python list, the Python call, Makefile `-D NAME` and `-D NAME=1` are each CAUGHT. My R585-2 probe n4 is CAUGHT. `-U NAME` derives as `-UNAME` in Python and in Makefiles. | `receipts/runs/probes3_b.log`, `probes_r2.log`, `receipts/derive_u.txt` |
| R585-2-S2 | **Retained** (SUGGESTION, above). | `aecp_arms.py:83,144` |
| R585-2-RS1 to RS3 | **Applied** at round 3: Status, Known limitations, and How to validate citing the REVIEW READY comments. RS1's subject has since moved on: see R585-3-RS1. | `receipts/pr705_body.md:19,187,175-179` |
| R584-2-R1 (relative links in the PR body) | **Applied.** No relative link remains. Links are pinned at `d1b22e80`, `1a9f651c` and `ec6854f6`. | `receipts/pr705_body.md` |
| R584-1 and R585-1 findings | Stand as resolved in round 2. Every round-1 probe class (r1-*) is still CAUGHT. | `receipts/runs/probes_r2.log` |

## 3. What I checked, per lens

Everything ran on a local host with gcc 16.2.1, Python 3.14 and GNU make 4.4.1. The pinned RV32 SDK archive's sha256 `d42680e9…` equals `scripts/ci_rv32_sdk.py`. Verilator 5.050 is the pinned build. GoogleTest and GoogleMock are 1.14.0. Every run went into disposable clones of the head or `386b8e69`.

- **Boundary gate, local** (`receipts/runs/gate_selftest.log`): `ctrl_boundary.py --require-rv32 --selftest` gives PASS in 609 s, rc 0. The output reads "51 firmware units (24 also as C++) … 18 build modes, 5 shapes and 2 mailbox contracts (942 preprocessings) … 0 finding(s), 45 boundary and 20 pin controls, 0 misbehaved".
- **Probes:** 29 boundary probes in all, plus the two real-path C++ runs of R585-3-S2. They use `scripts/boundary_probes_r585_2.py`, unchanged from R585-2, and `scripts/boundary_probes3.py`.
  - Prior set: 11 of 11 CAUGHT.
  - This round: s1, s2, c1, c2, d1 to d4, g1 to g4 all CAUGHT. g3 and g4 are RV32-only regions: `__riscv` and `__STDC_HOSTED__ == 0`.
  - f5 and f6 are REFUSED, as designed. f1 to f4 ESCAPED (R585-3-S1).
- **Without `gptp-processor`**: the gate exits 2 and names the submodule (`receipts/no_gptp_refusal.txt`). `firmware-unit` initialises it (`rtl-fast.yml:255`).
- **Pin probes:** 37 arms in all.
  - R585-2's `pin_probes.sh`, unchanged: 27 of 27 refused by name.
  - Round-3 Makefile arms: 10 of 10 refused on the pin, none compiling the poisoned header. The first `make all` arm stopped at `run-wb`, because my null simulator builds no executable. It was re-run with the stand-in that writes executables, as the gate does, and is refused serial and at `-j16`.
- **Images** (`receipts/image_hashes.txt`): 35 of 35 ELF files identical.
  - `ctrl_image.py` at 5 shapes: head equals the `--base aef7ac66` build, the `386b8e69` clone and my round-2 receipt.
  - `ctrl_srp_image.py` at 5 shapes, 1 and 2 interfaces, without SRP / with SRP / with AECP: head equals `386b8e69`, with the same stand-in runtime archives.
  - `--base aef7ac66` is +0 in every section.
- **Firmware gate** (`receipts/runs/fw_head.log`): `test_ctrl_firmware.py --require-rv32 --self-test --jobs 6` gives PASS with `mutants: 471 of 471 caught` and 59 arms. Its 843 verdict lines are identical by name to my round-2 run at `386b8e69` and to dev `aef7ac66` (`receipts/verdicts_vs_round2.txt`, `verdicts_vs_dev.txt`).
- **Coverage** (`receipts/runs/cov_head.log`): `fw_coverage.py --check` gives PASS (30 files). All 30 rows are identical to my round-2 receipt, so the denominator is the same.
- **Mailbox bench** (`receipts/runs/mbx_bench.log`): `make -j16` gives 382, 427, 32, 384, 429 and 369 checks with 0 failures, and `mbx mutants: 5 of 5 caught`. The pin line prints before the firmware build.
- **Delta scope** (`receipts/delta_scope.txt`): no HDL, firmware source, header, test, mutation table, coverage row or gitlink change. The three commit messages are one line with no trailers. No added line carries an em dash.

### Lens lines

```text
[R585] MAJOR Conformance — R585-3-F1 (rtl-fast.yml:251,294-295; job 114173809799) — the exact-head rtl-fast verdict is failure: firmware-unit timed out in the boundary step, store suites and coverage ratchet skipped. Otherwise checked: acceptance 2 (gate + planted controls: receipts/runs/gate_selftest.log), 3 (35/35 images: receipts/image_hashes.txt), 4 (coverage rows and 843 verdicts: receipts/verdicts_vs_dev.txt), round-3 items 1-3 (receipts/runs/probes*.log, pin*.log, receipts/derive_u.txt).
[R585] PASS RTL — git diff --stat 386b8e69..d1b22e80 -- hdl syn constraints '*.sv' '*.svh' '*.v' (empty, receipts/delta_scope.txt); tb/verilator/mbx/Makefile:45-49,82,91,115 (prerequisites only; recipes, VFLAGS, FW_SRC/FW_INC unchanged); receipts/runs/mbx_bench.log (Verilator 5.050: 382/427/32/384/429/369 checks, 0 failures; 5/5 RTL mutants) — no RTL or bench-recipe change; the bench reaches the same tallies with the pin first.
[R585] MAJOR Robustness — R585-3-F1 (timeout path of the required job at this head). Otherwise checked: ctrl_configs.py:155-408 and ctrl_pin.py:88-224 against 29 boundary probes, the -U derivation and 37 pin arms; the gptp-processor refusal (receipts/no_gptp_refusal.txt).
[R585] MAJOR Tests — R585-3-F1 (the hosted regression job does not complete: steps 9-11 cancelled/skipped). Otherwise checked: ctrl_boundary.py:536-761 and ctrl_pin.py:179-312 (45 + 20 controls, each with an expected needle; my probes reproduce each class independently, including the planted unpinned run-if2 and the poisoned bench targets); receipts/runs/fw_head.log, cov_head.log.
[R585] PASS Docs — sw/firmware/ctrl/README.md:80-126, tb/verilator/mbx/README.md:12-20, docs/testing/CI_WORKFLOWS.md:55-66,195-201, rtl-fast.yml:287-295, docstrings of ctrl_boundary.py:1-105, ctrl_configs.py:1-37, ctrl_pin.py:1-32 — the counts (42 + 3 boundary, 20 pin, 51/24 units, 18 modes, 5 shapes, 2 contracts, the five reaching targets) match receipts/runs/gate_selftest.log; every behavioural statement matched a probe at this head (R585-3-S1/S2 note latent generalisations, SUGGESTION); PR body residue R585-3-RS1 recorded with its exact fix.
```

## 4. Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R585-3-F1) | Acceptance 1-5 through the delta; round-3 items 1-3; hosted `rtl-fast` at the head | R585-3 | `d1b22e80` |
| RTL | CLEAN | Empty HDL delta; `tb/verilator/mbx/Makefile`; bench run with Verilator 5.050 | R585-3 | `d1b22e80` |
| Robustness | UNCLEAN (R585-3-F1) | `ctrl_configs.py`, `ctrl_pin.py`, `ctrl_boundary.py`; 29 boundary probes, 37 pin arms, the `-U` derivation, the no-`gptp-processor` refusal; hosted timeout | R585-3 | `d1b22e80` |
| Tests | UNCLEAN (R585-3-F1) | 45 boundary and 20 pin controls (local PASS); firmware gate; coverage; bench; hosted `firmware-unit` cancelled | R585-3 | `d1b22e80` |
| Docs | CLEAN (residue RS1 carried) | README, bench README, CI_WORKFLOWS, workflow comment, module docstrings, PR body | R585-3 | `d1b22e80` |

## 5. Real limits

- **Local toolchain.** The host is not the CI-parity container: gcc 16.2.1 rather than 13.3, Python 3.14 rather than 3.12. GoogleTest is 1.14.0, the RV32 SDK is the pinned archive, and Verilator 5.050 is the pinned build. Verdicts were compared by name with my earlier runs on the same host.
- **Shared host.** Another review ran concurrently, so local durations are not comparable with hosted ones.
- **SRP/AECP stand-in runtime.** Those images were linked with reviewer stand-in runtime archives (`scripts/standin_libc.c`, plus `image_arith.c`), not the repository's runtime builder, and the same archives were used at both heads. The `ctrl_image.py` images use the repository's own harness.
- **Image comparison against dev.** The `--base aef7ac66` build uses the head's harness on dev's firmware. Dev's own harness was compared in round 2 (my receipt, identical hashes).
- **Hosted runs.** At 09:26 UTC three Verilator shards (1, 2, 4) were still running. `firmware-unit` was cancelled and `rtl-fast` failed. I did not re-run any hosted job.
- **Not run:**
  - act, and no manager source bank. I neither claim nor infer one.
  - No full parent, PP, gPTP, Yosys or builder bank.
  - No physical calibration. Field skips are not hardware proof.
- **Not run again (unchanged in the delta, and verified by me in round 2):** the saved-state campaign, the tally listener mutations, the MAAP differential and the AECP wire comparison. I ran only their pin refusals.

## 6. Pending manager duties

- Hosted acceptance at the exact head: R585-3-F1 and the three Verilator shards still running.
- The act run through the audited-install bootstrap for the new submodule manifest.
- The current-dev merge candidate (source base `8b61b709`, live dev `e8454e27`): builder and native banks, image hashes, coverage and kills. Link its receipts on the PR.
- Carry R585-3-RS1 to the residue checklist, and apply it to the PR body after F1.
- Publication of this packet (`REPORT.md` and the files in `MANIFEST.sha256`).

My checkout is byte-exact at the head after the probes (`receipts/restore_verification.txt`):
- 1267 tracked files with 0 blob or mode mismatches, the index equal to HEAD, and no untracked or ignored entries;
- every required gitlink checked out clean: `gptp-processor`, `protocol-processor`, `third_party/lwSRP`, `third_party/tsn-c-stack` and `third_party/verilog-axis`;
- `external` uninitialised, as at the start.

R585-3 FINISHED
