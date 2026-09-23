[A191] REVIEW READY
Commit: `97aa1ec943ac740a27b942210a248f6512ae3ff6`, tree `4a12a545bdb478083d711a8f319d3c6d70c1b1d9`. The head is local and unpushed.

It descends from live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2` through the merge `4914eea5`. That merge is clean: its tree `fdf07c85` equals `git merge-tree --write-tree 5081a25a 574c29fa` (exit 0). The two files both sides changed, `CI_WORKFLOWS.md` and `ci_events.py`, auto-merged. `ci_events.py` passes `--check` (1631 items) and `--selftest` (2183 arms) at the merge and at the head.

Two one-line commits follow the merge, with no trailers: `3f7f083e` (builder) and `97aa1ec9` (docs). The worktree, the index and the ignored list are clean, and the gitlinks are unchanged.

Changed: `sw/builder/test_builder.py` (the frame-slot model, and the resolver's controls and compiled mutants), `docs/integration/BAREMETAL_FIRMWARE.md` and `docs/testing/CI_WORKFLOWS.md`. These are blob-identical to the reviewed head:

- the installer, so the cache key is unchanged;
- its self-test;
- both workflows;
- `test_firmware_compiler.py`;
- `check_baremetal_only.py`.

No product, RTL, firmware, pin, residual, text-rule or ratchet change. The changes only add refusals.

| Finding | Resolution at the root | Failing control, and the fix-removal result at the head |
|---|---|---|
| R227-2-F1 MINOR | **Route 1, the model fix.** `_rv32_store_value()` is the single source of the whole word a store leaves at its own address: `sw` and `amoswap.w` only. The frame and static branches both store it, so a byte or half-word store at the word's own offset, an FP store, any other AMO and an SC leave the word unknown. A store through a stack address forgets every frame slot. The docstring, the gate note and the page state this. | **Literal controls:** byte and half-word stores at a frame slot's own offset, a byte store at a static's own offset, and integer and FP stores through a pointer to the slot. Each must leave the next store unplaced, and three whole-word positive arms must stay placed. **Compiled mutants:** a union byte overwrite, a union half-word overwrite, and an integer and a `float` rewrite through a pointer. Each is refused as the unplaced store in `configure_fabric()`. **Removal:** reverting the value rule or the stack rule is KILLED by the literal control. With that control also removed, it is KILLED by the compiled mutant. **Reviewer plants:** R227-2 byte and half, and R228-2 E12 and E12f, are REFUSED; no-overwrite is still REFUSED. **Probes:** R227-2 `resolver_controls.py` passes F1 92/92, and X-stack-alias and X-subword-slot-store now pass. |
| R227-2-F2 MINOR | A control for each of the three changes. | **Range footprint:** `sw` and `fsd` loops whose first bytes all lie under the window must be placed to the window's first byte. R5 is KILLED by it. **Slot mirror:** an `fsw` over the slot, and an `amoor.w` or `amocas.w` through a pointer to it, must stop the refinement; a positive arm must still be refined. R6 is KILLED by it. **Non-swap AMO and SC:** these, handed a placed address, must leave the word unknown, and the `amoswap.w` positive arm must carry it. R10 is KILLED by it; its anchor line changed, so it was re-anchored. |
| R228-F4 MINOR | Controls for both terms. | RM8 is R5 above, KILLED. RM11 is KILLED by "an fsd over a static's first word, reloaded at its second". RM12 is still KILLED. The E10b and E11b plants stay REFUSED. Optional S4 taken: RM1 is R6, KILLED; RM5 is KILLED by a `cbo.zero (a4)` probe. |
| R228-F5 MINOR | The page claims only what is proved. The class is named RV32A AMO and SC instructions, and an atomic builtin compiled to a call is not one. A new paragraph, "What a store leaves behind", states the model exactly. A new list, "What the census does NOT observe", has three entries: stores inside a called function (C-library and libatomic calls handed a window pointer, and a callee's write into its caller's frame); numeric and range stores and the two models; and sub-word frame-slot loads (R227-2 OBS-1). The instrument-table cell, the ISA sentences on both pages and the gate's printed coverage lines match the page. Optional R227-2-S1 taken: both unbound LR/SC edges are named. | E8 (a 64-bit atomic compiled to `call __atomic_exchange_8`) and E9b (`memset`) still PASS the complete gate at this head, as the page now says. R228-2 `probe_resolver.py` is identical to their published 5081a25a receipt, 47/47. The docs, em-dash, style, paths and TOC gates are green. |

Validation at the head. Everything ran with the scoped 5.050 elaborator and the SDK freshly installed from the verified archive (102,597,892 bytes, pinned SHA256) into disposable scratch.

- **SDK:** fresh install 12.96 s, cache hit 1.00 s, verify-only exit 0. GCC 14.3.0, target `riscv32-buildroot-linux-gnu`.
- **Gate 1b, SDK mapped:** exit 0.
  - 217/217 mutations (213 plus 4), 17/17 and 4/4 positives, 46/46 RTL variants.
  - 0 NOT RUN, 235 compiles.
  - All 120 census assemblies have arch `rv32i2p1_m2p0_a2p1_f2p2_d2p2_zicsr2p0_zifencei2p0`.
  - The audit mapped only argv[0], and every argument tail is preserved.
  - The residual is unchanged.
- **Gate 1b, absent:** exit 0.
  - 182/182, 17/17, 4/4, 46/46.
  - Exactly 1 NOT RUN, 0 compiles, and 35 registered skips (31 plus 4).
- **Variants:** 19 in-memory runs, all as expected. 10 fix-removal mutants are each KILLED on their own control's sentence, 7 plants are REFUSED, and E8 and E9b PASS.
- **Resolver equivalence:** old against new over all 120 census assemblies of a mapped run.
  - Store addresses are identical in 116. The 4 that differ are exactly the new rewrite mutants.
  - Calls, handed arguments and seeds are identical in all 120.
- **Static and focused gates, 22/22 exit 0:**
  - `ci_rv32_sdk_selftest.py` (25 tests) and `test_firmware_compiler.py --selftest`;
  - `check_baremetal_only.py`: 0 findings and 365 arms;
  - `ci_events.py`: 1631 items and 2183 arms;
  - `docs_check.py`;
  - `check_em_dash.py`: 0 findings against `52711029`, `574c29fa` and `483a133e`;
  - the doc path, TOC, anchor, doc style, Python idiom, hygiene, fail-fast, test-evidence, naming, TODO and `py_compile` gates.
- **Integrity:** 860 blobs are byte- and mode-exact, the index equals HEAD with no hidden flags, and the three submodules are at their gitlinks.

Acceptance: items 2, 3 and 5 were re-measured locally at this head. Items 1 and 4 (hosted, act and the full banks) remain with the manager. The hosted compiled tally grows by the same 4 resolver-only entries.

Open risks/questions:
- R228-S2 and S3 were not taken, because they change installer behaviour.
- For a public Issue before #408/#409 retire any text rule onto the census. The page now lists four shapes as not observed. They predate this PR, and it does not close them:
  1. a store inside a called function that is handed a window pointer (R228-2 O1 class 1);
  2. a callee's write into its caller's frame through a pointer it was handed (the call-crossing half of O1 class 2; this round closes the in-function half);
  3. a numeric store that happens to hit the stack;
  4. a sub-word frame-slot load (R227-2 OBS-1).
- Raw receipts carry local paths.

The handoff, PR body, commands, scripts and receipts are in the author packet (504-a191). There was no push, PR edit, merge, delegation or self-approval. R227 and R228 re-review the corrected head.
