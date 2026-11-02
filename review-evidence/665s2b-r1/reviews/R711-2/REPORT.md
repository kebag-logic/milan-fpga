[R711] NEGATIVE - exact head c954b8a91e720f87d2dfa9294c8501058dc55df3

Round R711-2, internal cleared-context review of PR #810 (#665 lane S2b) into `dev-soft-core`, round 12. Head `c954b8a91e720f87d2dfa9294c8501058dc55df3`, tree `5e2989e8c7a2f72a1f1a7009d2132f4319017fd2`, source base `a68536fa`. All five lenses applied. The whole diff was judged against the base, by the delta since `f884c7e9`, with the author's public packet `author-r12` and raw results `author-r12-results`, plus my own probes in a scratch copy of the head.

## Verdict in one paragraph

The clock move, the crossing's removal, the rows, the section 14 arithmetic and the merge all hold. All 13 unheld rows and all 14 section 14 rows recompute from the raw results with no difference. Every prior finding is resolved except the per-pass share. "Every pass fits" is true only of the groups the harness stages. A save and a composed window overlap in ordinary use, and when they do at 8x8/2if the pass measures **2.72 ms against the 2.0 ms share (F1, MAJOR)**. The author derived this as about 2.67 ms and left it open. Both links changing together measure **2.08 ms (F2, MINOR)**. No row missed its bound in any probe. The closest was the last SRP record at 17.55 ms against 18, so these are breaches of the frozen per-pass acceptance, not of a wire deadline. Two smaller findings: the boot simulation still reads flash through the data cache (F3, MINOR), and three stale statements remain in the READMEs (F4, MINOR).

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests - a save's store step in a composed window breaks the per-pass share, 2.72 ms measured at 8x8/2if

**Where:**
- `sw/firmware/ctrl/plat/ctrl_plat.c:258`: the store is a centisecond consumer, with no regard to what else its pass carries.
- `sw/firmware/ctrl_nvm/nvm_store.h:60`-`:64`, `nvm_store.c:653`: the 128-byte read-back step.
- `sw/firmware/ctrl/loop/ctrl_loop.h:55`-`:77`, THE SHARE: "no pass may exceed", and its list of slices names no store step.
- `tb/verilator/ctrl_service_budget/scenario.py`: no group stages a composed window during a save.
- `docs/design/SPLIT_CONTROL_MEMORY.md:1318` and the PR's "A pass no group stages": disclosed as derived, with no decision.

**Authority:**
- Frozen acceptance, #665 issuecomment-6414297191 items 3 and 6: "every pass within the per-pass share".
- Round 11 item 4 (issuecomment-6508235352).
- Round 12 item 3 and exit (issuecomment-6514866239): "every pass fits the share"; "REVIEW READY when every row and every pass fits at 100 MHz. Otherwise STOP with the residual."

**Evidence** (`receipts/probe/`, 8x8/2if, arm A, CPU on `sys` at 100 MHz, the ELF byte-identical to the author's `N-A8`, `6d8c4931`). A SET_NAME starts a save. The window is then the head's own composed load, opened at phases of the 10 ms tick:

| Window | Phases over the share | Longest pass, ms | Last SRP record, ms (bound 18) | Last AECP record, ms (bound 20) |
|---|---:|---:|---:|---:|
| `backlog` + save (`x-save-0..5`) | 3 of 6 | **2.388** | 14.02 to 14.86 | 12.84 to 13.90 |
| `backlog-adp` + save (`y-save-0..7`) | 7 of 8 | **2.716** | 16.39 to 17.55 | 15.40 to 16.28 |

- Without a save the same windows measure 1.55 and 1.97 ms on the same arm, with 15.88 ms on the last SRP record.
- `save-steps.txt`, one whole save with no other load, gives each step's cost:
  - a read-back step is about 70,600 flash-port cycles, which confirms the 0.70 ms the author states;
  - a page program takes about 79,000 to 93,000 cycles, up to 0.93 ms, which is **more than the read step the fix halved**.
- A program step in the heaviest pass would be about 2.9 ms. That figure is derived, not measured.
- The overlap is ordinary. Any persisted change starts a save, and at 8x8 the save's blank check, program and verify phases put a heavy flash step on 260 of about 312 ticks. All 14 save windows measured one or two read-back steps. Their spans are 14.6 to 18.6 ms.

**Impact:**
- The acceptance is not met in a reachable state, and the nine-pass derivation in `ctrl_loop.h` does not hold for the passes it names.
- The disclosed reassurance is too generous. "The least margin, 2.04 ms, is more than a few such steps" describes under three read steps. I measured 1.67 ms of that margin spent, leaving 0.45 ms on arm A. Arm B and the drafts were not run with a save.
- No row missed, so this is not a measured wire-deadline miss. It is MAJOR because it is an explicit exit criterion with a measured 36 % overshoot and no gate that can see it.

**Required outcome:** one of the following.
- (a) Every store step is bounded so that any pass carrying it stays within the share, at both points, both arms, with and without the drafts, and the save's own progress stays bounded and stated.
- (b) A public owner or manager amendment replaces the share for a pass carrying a store step, with its bound derived from the deepest admitted wait and graded.

Either way the harness must stage it, so that the share's gate can fail on it, and THE SHARE's slice list must name the store.

**Verification:** a composed group during each store phase (read-back and program, not only blank check), at no fewer than eight tick phases, on the heaviest window, at both points and both arms, graded by `grade.pass_share`, with a planted store step that must fail the share while every row fits.

### F2 - MINOR - Conformance, Robustness, Tests - the two-pass reset bounds one interface's build, and a joint link change builds both in one pass, 2.08 ms

**Where:** `sw/firmware/ctrl/srp/srp_mbx.c:840`-`:866` (`poll` builds every interface whose reopen count has run out), `sw/firmware/ctrl/srp/srp_bounds.h:7`-`:16`, `sw/firmware/ctrl/test/srp_app.cpp` (`LinkEdgesOfOnePassBuildOnce` covers one interface), and `scenario.py:871` (a window changes `link 0` only).

**Authority:** as F1. The commit's stated purpose is that "no 8x8 pass is over the 2.0 ms share".

**Evidence** (`receipts/probe/`, 8x8/2if, arm A): both links dropping together under the composed load.

| Window | Longest pass, ms | Modules | Last SRP / AECP record, ms |
|---|---:|---|---:|
| `backlog` load, joint (`x-links-same`) | **2.004** | `ctrl_mem` 61,312, `acmp` 33,588, `mrp_mad` 32,931, `srp_mbx` 17,695 | 10.76 / 10.11 |
| `backlog-adp` load, joint (`y-links`) | **2.081** | `ctrl_mem` 61,697, `acmp` 34,886, `mrp_mad` 32,969, `srp_mbx` 18,014 | 11.25 / 10.74 |
| `backlog` load, the links 1 ms apart (`x-links-1ms`) | 1.573 | | 11.02 / 10.37 |
| `backlog` load, the links 2 ms apart (`x-links-2ms`) | 1.314 | | 11.37 / 10.38 |
| No other load, eight separations (`x-links-quiet`) | 1.682 | | |

Reachability: both ports' events taken in one pass, for example a shared PHY, power or upstream event. The redundant-network design makes two ports the normal shape.

**Impact:** the fix holds for one interface, and a two-interface pass goes over the share by up to 4 %. No row is hurt. The harness cannot see it, because no window changes the second link.

**Required outcome:** every pass that builds interfaces stays within the share at two interfaces, for example at most one interface built a pass, or an amendment under F1. A test and a composed group must cover the joint change.

**Verification:** the `y-links` stimulus at both arms grades 0 over the share, plus a plant that fails a named check when both interfaces build in one pass.

### F3 - MINOR - Tests, Docs - the boot simulation still reads flash through the data cache, which the product never does

**Where:** `tb/verilator/ctrl_split_boot/boot_soc.py:90` (`add_devices`, with no `ctrl_uncached_flash`, while `split_soc.py:494` and `milan_soc.py:3523` have it), `tb/verilator/ctrl_split_boot/README.md:75`-`:78` (the figures), and `:42` (the SoC description).

**Authority:** round 12's own finding on the budget harness, as the PR body says: "the cached window read the flash through the data cache, which the product never does". The README claims the boot simulation boots the split SoC.

**Evidence:** one added call in a scratch copy (`receipts/probe/boot-uncached.patch`).

| Shape | Head, cached window | With the product's window | Change |
|---|---:|---:|---:|
| 1x1 | 24.660 ms | 25.413 ms | +0.753 ms |
| 8x8 | 64.271 ms | 65.026 ms | +0.755 ms |

The UART figures and trace are unchanged, and all verdicts are unchanged against the 20 s ADP valid time.

**Impact:** the figures, published as the product's boot on `sys`, are about 3 % and 1 % low. No check refuses the mismatch here, as `build.flash_window_refusals` does for the budget harness. The flash is blank, so a valid slot's boot, S4's lane, is the case with more at stake.

**Required outcome:** the boot SoC has the product's flash window, a build with another is refused, and the README's figures are restated.

**Verification:** `run.py` at both shapes; a plant removing the call must be refused.

### F4 - MINOR - Docs - statements this PR's own decisions made false

Each fix restates a figure or a behaviour, so none is pure wording under the residue rule.

- `sw/firmware/ctrl/srp/README.md:215`: "against the share of 1.1 ms (`ctrl_loop.h`)". `ctrl_loop.h` says 2.0 ms. Fix: "against the share of 2.0 ms", or name 1.1 ms as the share at the 10 ms first proposed.
- `sw/firmware/ctrl/aecp/README.md:310`: "and the 10 ms local service target". T_svc is 20 ms, and AECP's bound is 20 ms (FR_NFR 3.4.1). Fix: "the 20 ms local service bound". The line predates this PR, but this PR moved the target.
- `sw/firmware/ctrl_nvm/README.md:127`-`:128`: "calls `nvm_store_service()` once per pass". It is a centisecond consumer (`ctrl_plat.c:258`, `ctrl/README.md:362`), up to 16 per pass in catch-up. This is the fact that sets a save's duration, which round 12 lengthened. Fix: "once per centisecond the loop dispatches".

**Impact:** a reader of these pages gets a wrong share, a wrong target and the wrong cadence.

**Verification:** read the three lines at the corrected head.

### RESIDUE (wording only; no verdict effect)

- **R1, PR body, "Saved-state read-back" row, and `SPLIT_CONTROL_MEMORY.md:1303`:** "takes twice as many ticks" gives no time, and only the handoff does. Fix: add "at 8x8 the read-back is 2.08 s of ticks, 1.04 s before; a save is about 4.7 s from the change on a flash with no busy time. The owner's 0.5 s (#823) is the append-only design's, not this image's."
- **R2, `tb/verilator/ctrl_split_boot/README.md:42`:** says "instruction cache" where the SoC has both caches. Fix: "with the split placement's instruction and data caches".

### SUGGESTION

- **S1, `srp_mbx.c` `reset_interface`:** `listener_present` is not cleared by the reset, and `deliver()` (`ctrl_app_srp.c:53`-`:57`) now reads the old value for up to two passes more, where the one-pass reset's snapshot cleared it in its own poll. It is bounded, and clearing it in the reset removes the question.
- **S2, section 14's gPTP table:** "Added to any row, 1.6 ms" counts four frames in 87 ms and omits the servo runs the sustained line counts (16 a second, 1.4 more, about 2.2 ms in all), and 87 ms has no stated basis. It is correctly labelled an assumption, so this is a precision point only.
- **S3, the platform image's hot list:** `bc50a190` removes the platform's link check, because four entries name fixture callbacks and its own callbacks are not on the list. This is disclosed. The figures are the size fixture's, so a check with an exclusion list would keep the guard on the product image.

## The six questions

**(1) The split CPU on `sys`: holds, apart from F3.**
- Wiring: `milan_soc.py:3192`-`:3207` refuses any other domain, `:3281`-`:3283` derives the clock, `:3324` builds no CPU clock, and `:3467`-`:3475` builds the crossing only for a CPU with `cpu_clk`.
- The all-fabric path is unchanged.
- `test_soc_options.py` passes with its 6 controls killed, re-run here.
- Mailbox tick from `sys`; `sim_main.cpp` has a `static_assert` that `cpu_hz == sys_hz`.
- OOC receipt recomputed from `route_hier.rpt`, `timing.rpt` and `clock_interaction.rpt`: WNS +1.605, WHS +0.070, one clock pair, 3,543 LUT, 5,643 FF, RAMB36/18 6/7 = 9.5 tiles, no routing error.
- The boot simulation builds through `ctrl_cpu_cd`; its flash window is F3.

**(2) Rows and passes: recomputed, no difference.**
- `receipts/rows.txt` re-derives every row from `results.json`, in all eight legs, against its own table of bounds (18 for SRP, 20 otherwise).
- Worst per family, ms: ACMP 7.98, ADP 5.85, MAAP 5.84, AECP 15.16, SRP 15.96.
- Longest pass in the staged groups: 1.966 ms at 8x8, 1.211 ms at 1x1.
- Over the share in staged groups: 0, including arm A's 0 of 7,837 and 0 of 8,477.
- Every record names the clock (`CPU 100 MHz on sys`).
- The ELF at this head is byte-identical to the author's `N-A8`, and `4c0805b5..HEAD` changes only documents and the matrix.

**(3) SRP two passes: bounded, not lost, not reordered; pass share F2.**
- `reset_interface` closes licences and withdraws before destroying, in the pass that takes the change.
- A bind refused in the gap stays pending and is retried (`ctrl_app_srp.c:78`-`:82`).
- Receive waits rather than refuses; a record is taken on the pass after the build (`rx_ready`, tested).
- A failed build is retried with the existing counters.
- Each further edge restarts the two passes, so the wait is bounded by the edge rate, at most 8 edges a pass.
- A rebuild adds at most one pass, about 2 ms, ahead of a 200 ms JoinTime with an 18 ms service bound. The rows with both links are 10.76 to 11.37 ms.

**(3) Store read-back: complete, ordered, slower; pass share F1.**
- Blank check and verify still cover the whole container, and authority still moves only on a full verify (`nvm_store.c:653`, plant `read_back_a_whole_page`, `read-fail` tests at the step positions).
- DR2a and DR2c are untouched, so a change during a save is taken by the next capture.
- Measured with no other load: blank check 104 ticks, program 52 pages over 104 ticks, verify from +3,666 ms, 13,256 bytes programmed. That gives about 4.7 s from the change to durable, derived for the last 21 ticks, on a flash with no busy time.
- The owner's 0.5 s (#823, 2026-10-31) is unmet by this design at the base too: the 1,000 ms first-dirty window alone exceeds it. This PR adds 1.04 s at 8x8. #823 owns the bound, so it is not a finding here, but it belongs in the PR's text (R1).

**(4) Harness changes: each is a truer model, and hides nothing it claims to model.**

| Change | Truer? | Check |
|---|---|---|
| Uncached flash window | Yes | `N-A8/build.json` has the flash region at mode `r`, as `milan_soc.py:3523` gives the product. `CC-A8` and `CC-A1` reproduce 12.391 and 4.069 ms. A build with another window is refused. Not applied to the boot simulation (F3) |
| AECP frames paced | Yes | The bucket admits a burst, then one a period. The paced groups are single-command paths. The burst stays in the composed windows, unpaced: `population` shows `aecp: 16` in all four. Unpaced controls show 3 and 15 refused. The self-test's plant is caught |
| Windows on a drained ring | Yes | Ring capacity bounds the event work either way, and a held window carries the same 16. `events_held` is 0 in all windows of all legs. The self-test's plant is caught |
| 15 of 15 definition | Yes | `check_load` requires exact population. `xip-1x1-4k` has 0 refusals and 0 held, and its 40.25 ms is flagged `lower_bound`, with SRP 26 and 23 unreleased, as stated |

What these windows do not contain is a save or a second link: F1 and F2.

**(5) Section 14: labelled, and its arithmetic is right.** `receipts/estimate.txt` recomputes all 14 rows of U, L and S from raw results with no difference. The one-CPU arms recompute (62 and 64 passes, 3.61 and 3.85 ms; AECP 26.83 and 28.51; SRP 30.26 and 34.52; 1x1 17.98 and 21.63). gPTP is labelled an assumption, and 2.48 % (1.24 to 6.2), 17.3 and 9.0 ms all check; see S2. Milan v1.2 4.2.6.2.6's 15 ms matches the compliance matrix.

**(6) Merge: both sides kept.**
- `git show --remerge-diff 8b448143` shows six conflicted files, each resolved keeping both sides' lines.
- `08618784` and `392ba9bc` move the boot to the clock and the approved 20 ms.
- `99f51950`, `bc50a190` and `ff2e855f` build the platform for the split hart, and 19,944 B is re-measured.
- `82efbe36` moves the MAAP plants out whole. The firmware gate counts 603 of 603.

## Prior public findings, read after the independent pass above

| Finding | Status at this head | Evidence |
|---|---|---|
| R711-1 F1, clock | **Resolved** | Owner decision issuecomment-6514866239; `CTRL_CPU_CD`; every figure at the product clock, recomputed |
| R711-1 F2 = R712-1 F1, length wrap | **Resolved** | `KL_mbx_dma.sv` 13-bit sum (`f52e65a9`), D10, plant `length-sum-wraps`, `gates/sweep/shard-1/logs/mbx.log` |
| R711-1 F3, bench blind spots | **Resolved** | Plants `error-burst-continues`, `fill-during-cpu-answer` and `held-partial-write-widened` caught; 21 of 21 |
| R711-1 F4, firmware mover arm | **Resolved** | `test_mbx_dma_driver.cpp`, `mbx_dma_mutants.py` (8 plants), coverage gate |
| R711-1 residue | **Resolved** | `ctrl_mem.c:7`, `mbx_wire.h:62`, harness README `:134` |
| R712-1 F2, per-pass share | **Partly resolved, retained as F1 and F2** | The share is graded apart from the rows with a plant, and every staged pass fits. Reachable passes outside the staged groups do not |

## Comment rule

I scanned added source and script lines against the base for bench labels, lane names, review rounds, reviewer IDs and issue-comment IDs. There are no new instances. The only hits are byte lanes (`lanes_w`, "ring word's lanes").

## Lens results

| Lens | Result | Artifact, at this head |
|---|---|---|
| Conformance | UNCLEAN, F1, F2 | Acceptance items, rounds 11 and 12, `FR_NFR.md` 3.4.1; `receipts/rows.txt`; probes |
| RTL | **PASS** | `milan_soc.py` clock wiring and `ctrl_uncached_flash`; `KL_mbx_dma.sv` delta; `area/ooc-sys-10/` receipts; `test_soc_options.py` re-run |
| Robustness | UNCLEAN, F1, F2 | `srp_mbx.c` reset, poll and bind; `ctrl_app_srp.c`; `nvm_store.c`; probes |
| Tests | UNCLEAN, F1, F2, F3 | `scenario.py`, `grade.py`, `selftest*.py` (self-test re-run, 0 failures); `srp_reopen_mutants.py`; `nvm_mutants.py`; gate receipts |
| Docs | UNCLEAN, F3, F4 | `SPLIT_CONTROL_MEMORY.md` 13, 14; harness and boot READMEs; `srp`, `aecp`, `ctrl_nvm` READMEs; `ctrl_loop.h`; PR body |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Acceptance items 3 and 6; rounds 11, 12; `FR_NFR.md` 3.4.1; rows recomputed; probes | R711-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| RTL | CLEAN | `milan_soc.py:3192-3283`, `:3324`, `:3467-3475`, `:3523`; `KL_mbx_dma.sv`; OOC timing, hierarchy and clock receipts | R711-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| Robustness | UNCLEAN (F1, F2) | `srp_mbx.c`, `srp_bounds.h`, `ctrl_app_srp.c`, `nvm_store.c/.h`, `ctrl_plat.c`, `ctrl_loop.c`; link and save probes | R711-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| Tests | UNCLEAN (F1, F2, F3) | Harness files and plants; `srp_app.cpp`, `srp_reopen_mutants.py`; `test_nvm_write.cpp`, `nvm_mutants.py`; `boot_soc.py`; published gates | R711-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |
| Docs | UNCLEAN (F3, F4) | `SPLIT_CONTROL_MEMORY.md` 5, 11 to 14; `ARCHITECTURE_HW_SW_SPLIT.md`; `MAILBOX_SPLIT.md`; READMEs; PR body | R711-2 | c954b8a91e720f87d2dfa9294c8501058dc55df3 |

Coverage this round: RTL is clean at this head. Re-run the other four lenses at the corrected head; RTL is un-covered by any change in its scope. This is one internal round, and the external review is separate.

## Execution evidence

- `receipts/evidence.txt`: all 1,849 entries of the public `MANIFEST.json` match. Of the author's `INDEX.md` entries, 430 match directly, 6 differ only through path redaction (the manifest's originals match), and 21 `results.json.gz` are published decompressed, so they are checked through the rows rather than by hash.
- `receipts/checkout-integrity.txt`: my clone matches the exact head and tree, with blob bytes, modes, index and the five submodule gitlinks all verified. Every probe ran in a scratch copy; the patches are `receipts/probe/*.patch`.
- Probes: `scripts/probe_groups*.py`, `scripts/run_probes*.sh`, `scripts/probe_passes.py`, `scripts/save_phases.py`, results in `receipts/probe/`. Harness and SoC-option self-tests re-run, rc 0. Author's published source-head gates spot-checked.

## Limits

- Probes ran at 8x8/2if, arm A, without the drafts. 1x1, arm B and the drafts were not run with a save or a joint link change. The rows and passes elsewhere are the author's receipts, recomputed but not re-executed. At 1x1 the published figures leave the question open: 1.07 ms in the backlog windows plus a 0.93 ms program step is 2.00 ms, which is not measured.
- The 2.9 ms program-step figure is derived from a pass and a step measured separately. The 4.7 s save is measured to +4,500 ms and derived for the last 21 ticks, on a flash model with no busy time; datasheet erase and program times would add to it.
- A catch-up pass can dispatch up to 16 ticks, so 16 store steps. It needs a stall of tens of ms that no measured pass makes, so I did not stage it.
- The flash model's timing is the harness's, and bench calibration was not run. Physical calibration NOT RUN; field skips are not hardware proof; out-of-context timing is not whole-board timing, and the routed split image is lane S9's.
- The three egress-held rows are over by record and belong to tsn-c-stack #26. The 32x32 misses are reported results.
- No manager source bank exists at this head, and none is claimed. Source validation against `a68536fa` does not validate incorporation of live dev `1f29f189279f9fc0132f4918e47342b87d22f33a`.

## Pending manager duties

- Rule on F1's option (a) or (b), and accept or re-file the lenses under AGENTS.md section 3.
- Carry the residue.
- Hosted and act acceptance, the external review, the current-dev merge candidate with its builder and native banks, post-merge containment and maintainer merge authorization.

R711-2 FINISHED
