[R826] NEGATIVE - exact head 596e2ae3708c4693e0929b530fea37020dc8db25

# R826-2: external cleared-context delta review of PR #888 (issue #791)

- Head `596e2ae3708c4693e0929b530fea37020dc8db25`, tree `e7f1b5919e7dab3928769c147da97f9f758b785a`.
- The delta is `03447eaa..596e2ae3`: five commits by the executor under the round-2 ruling (#791, the `[A10]` ruling on R825-1 and R826-1). Each commit message is one line with no trailers. Source base `1d6bf555`.
- Reconstructed in this order:
  - AGENTS.md;
  - the issue's Required items (option (a) or (b), the edge test with a single-mask mutant, all-fabric byte identity);
  - the round-2 ruling (items 1 to 4);
  - the executor's TAKEN and REVIEW READY on #791;
  - the PR body at this head;
  - `git diff 03447eaa..596e2ae3` and the commit history;
  - the pinned LiteX VexiiRiscv source (`vexiiriscv/core.py`: `generate_netlist_name`, `generate_netlist`, `add_sources`, `do_finalize`);
  - my R826-1 receipts (`generator_terms.txt`, `guard_probe.txt`);
  - the executor's round-2 packet, `review-evidence/791-r1/author-r2` at archive `7a130467`.
- My verdict and ledger were written into this report's interim version before I listed the PR's later comments. The only review comments on the PR are R825-1 and R826-1, and both were already known from round 1. No other reviewer's report was read.
- **Verdict NEGATIVE: one open MINOR (F5), under Robustness, Tests and Docs.**
  - The round-1 items are resolved: F1 (root cause), F2 (the guard against both silent shapes, the re-pin procedure and the PR wording), and F3/F4 with their exact texts.
  - No generated CPU netlist or all-fabric export byte changed.
  - F5 is new and sits in the ruling's own item 2. The guard compares what the generator may read against the naming step's list object, not against a copy of the list that step hashed. So an in-place change to that list after naming is either not refused, or is refused without naming the poisoned cache entry.

## What this review ran

Tools:
- Verilator 5.050 through the pinned wrapper (identity `Verilator 5.050 2026-07-01 rev v5.050`, first on `PATH`);
- the product LiteX venv (LiteX `a1e1c365`);
- the pinned RV32 SDK (`riscv32-linux-gcc` 14.3.0, Buildroot 2026.05);
- `PYTHONHASHSEED=0`, offline sbt.

Every LiteX run carried the generator-refusing guard `tools/noguard/sitecustomize.py` on `PYTHONPATH`. No run logged a generator command or a guard refusal, and the set of cached `.v` netlists is identical before and after (`receipts/netlists/cache-v-{before,after}.txt`). Receipts replace host paths with `<clone>`, `<packet>`, `<litex>`, `<sdk>`, `<generator-cache>`, `<tools>`, `<verilator-root>` and `<home>`.

| # | Run (exact-head clone) | Result | Receipt |
|---|---|---|---|
| 1 | `sw/litex/test_ctrl_memory.py` | 182 `[ok  ]`, 0 `[FAIL]`, `test_ctrl_memory: 0 failure(s)`, `RESULT: PASS`, rc 0. The three SHAPES refusals (log lines 119-121), the unaligned refusal (122) and all five new mutants (183-187) are caught. `naming guard off` (181) is now caught by its message | `receipts/tcm/run.{log,rc}` |
| 2 | `tb/verilator/ctrl_region_decode/run.py --self-test` | `none: fails 0, wants 0`; `single-mask: fails 4, wants 4`; `cover: fails 6, wants 6`; `ctrl_region_decode self-test: PASS`, rc 0. CPUs `88c5cdf9`, `18be4f88`, `57948043`, the same names as at `03447eaa`, all read from the cache | `receipts/sims/region-self-test.{log,rc}` |
| 3 | R826-1's own `guard_probe.py`, unchanged, at this head | `pinned order: built exact`; `class-level naming call: refused`; **`list re-collected after naming: refused`**; **`list kept on the instance: refused`** (both were `BUILT SINGLE-MASK SILENTLY` at `03447eaa`) | `receipts/probes/guard_probe-r1-at-head.{txt,rc}` |
| 4 | `tools/guard_probe2.py`: shapes 1-4 as in run 3, plus three in-place changes to the class list after naming. It records the list the naming step hashed and the list the generator reads | Shapes 1-4 as in run 3. Shapes 5 and 6 (clear+extend, `[:] =`) are refused, but as `the naming step's list is not aligned powers of two`, without the cache-removal instruction. **Shape 7 (an aligned row appended after naming): `BUILT, GENERATOR LIST != HASHED LIST, SILENTLY`** | `receipts/probes/guard_probe2.{txt,rc}` (F5) |
| 5 | The same probe with an in-memory one-line fix, `named.append(list(VexiiRiscv.memory_regions))` (`--snapshot-fix`; the module text is patched in memory and no file is written) | Shape 1 still `built exact`. Shapes 3-7 all `refused; reason names-cache` | `receipts/probes/guard_probe2-snapshot-fix.{txt,rc}`, `receipts/probes/snapshot-fix.diff` |
| 6 | Docs gates: `docs_check.py`, `check_doc_paths.py`, `gen_toc.py --verify-anchors` / `--check` (pinned markdown venv); `git diff --check 1d6bf555 HEAD` | All rc 0: `docs_check: 0 finding(s)`, `doc path gate: OK`, `anchor check: 610 ... reproduced`, `TOC gate: OK`; no diff-check output | `receipts/docs/*` |
| 7 | sha256 of the seven cached netlists the delta's runs name | Equal to the executor's `netlist-identity.log` and `allfabric-compare.txt`: `88c5cdf9` `6b5a22fc`, `18be4f88` `d425a0e7`, `57948043` `b47ecbdf`, `f8b27436` `c9ce67a1`, `99bc789b` `1fde79b5`, `f5f08b17` `c208df0b`, `7c73187a` `2ba0e339` | `receipts/netlists/netlist-sha256.txt` |
| 8 | Executor packet spot-check: seven receipts fetched from `7a130467` and hashed | Each matches its `receipts/INDEX.md` sha256 prefix | `receipts/author-packet-spotcheck.txt` |
| 9 | A residue scan of the 137 added lines (lane labels, lane names, review rounds, reviewer IDs, issue-comment IDs) and an em-dash scan | No hits; 0 em dashes | (commands in this report) |
| 10 | Hosted contexts at this head, a read-only snapshot at 20:36 local | 5 success, 1 skipped (physical gPTP), 9 in progress, 30 queued | `receipts/hosted-snapshot.txt` |

## The focus points, answered

1. **F1, the root cause (resolved).**
   - All four places now say the same thing:
     - `docs/design/SPLIT_CONTROL_MEMORY.md:39-50`;
     - `:396`, which names `rom` only;
     - `sw/litex/ctrl_memory.py:139-149`;
     - the PR body's "The fault (#791)".
   - What they say: the pinned generator decomposes each region through `AddressMapping.terms` into aligned power-of-two terms. A region based at 0 is taken whole, as `(address & ~(size - 1)) == 0`, so `rom` became `(address & 0xfffc8000) == 0`, while `sram` at `0x1000_0000` was already exact as 128, 64 and 32 KiB terms. Aligned pieces make every region exact without depending on that decomposition.
   - Against `generator_terms.txt`:
     - `ptr == 0` gives `step = m.size = 0x38000`, which fits, so it becomes one term with mask `~0x37fff = 0xfffc8000`;
     - the as-built netlist `18be4f88` (sha256 `d425a0e7`, run 7) has `32'hfffe0000 == 32'h10000000`, `32'hffff0000 == 32'h10020000` and `32'hffff8000 == 32'h10030000` for `sram`.
   - Every statement matches.
2. **F2, the guard (resolved as ruled, with the gap in F5).**
   - **What is refused now.** After `finalize()`, `exact_cpu_decode` (`milan_soc.py:3271-3285`) refuses:
     - when any 4-tuple region list on the instance or on a class in its MRO (`cpu_region_lists`, `:3291-3301`) differs from the naming step's list;
     - when that list is not aligned powers of two.
   - **Both silent shapes are caught.** Run 3 is round 1's probe, unchanged, and both shapes print `refused`. `test_ctrl_memory`'s SHAPES arm catches the re-collected shape and both instance shapes (`memory_regions`, `generator_regions`) by message (run 1). Each of the five new mutants is caught by a named check.
   - **The re-pin procedure.** `sw/litex/patches/README.md:38-52` names `test_ctrl_memory.py` and `tb/verilator/ctrl_region_decode` with runnable commands, and links the prerequisites at `ctrl_region_decode/README.md#run`, an anchor that exists (line 17).
   - **The PR wording.** The PR says "a LiteX that stops calling the naming step is refused".
   - **The gap (F5).** Item 2 asks the guard to refuse "unless the list the generator reads is still the naming step's aligned-power-of-two list". At this head that holds only when the list is rebound, not when it is changed in place.
3. **F3/F4 (resolved).**
   - `tb/verilator/ctrl_region_decode/README.md:7` and `:101` carry R826-1's exact texts, character for character.
   - `ctrl_service_budget/README.md:155` and the `CpuPatches` docstring (`split_soc.py:404-412`) now describe `as-built` as the build without the hookup.
4. **No generated CPU netlist or all-fabric byte changed (holds).**
   - The new code runs only after `finalize()`, and it changes neither the name nor the rows the generator is handed.
   - `as-built` now leaves `exact_cpu_decode` out (`split_soc.py:451-452`) and still names `18be4f88` (run 2).
   - All seven netlist names, and their sha256 values, equal the executor's at both heads (runs 2 and 7). The executor's all-fabric compare against `1d6bf555` reports every builder output identical, comment-only lines at AX7101, and the same CPU netlists. Its receipt hash matches the packet index (run 8).
   - The all-fabric SoC does not call `add_ctrl_memory`, so the delta cannot reach it.
   - The ruling's STOP condition is not met.

## Findings

### F5 - MINOR - Robustness, Tests, Docs - the guard compares against the naming step's live list, not a copy of what it hashed

- **Where:**
  - `sw/litex/milan_soc.py:3268`: `named.append(VexiiRiscv.memory_regions)` stores a reference;
  - `:3277-3278`: `pieces = list(named[-1])` is read after `finalize()`, so it is the list as it is now, not as it was hashed;
  - the docstring at `:3250-3258`;
  - `docs/design/SPLIT_CONTROL_MEMORY.md:56-57`;
  - the PR body's "The naming guard" bullets;
  - `sw/litex/ctrl_memory_decode.py:81` (SHAPES), which has no in-place shape.
- **Authority:**
  - Round-2 ruling item 2: refuse "unless the list the generator reads is still the naming step's aligned-power-of-two list".
  - The design doc, which says the build is refused when the generator is left "a region list other than that step's aligned power-of-two pieces, on the CPU or its classes", and that "the second refusal names the netlist the build may have cached under the pieces' name, for removal".
- **Evidence** (`receipts/probes/guard_probe2.txt`). The pinned LiteX itself builds the class list in place (`VexiiRiscv.memory_regions = []` then `.append(...)`, `core.py:724-736`). A re-pin that changes that same list after naming defeats the comparison, because `named[-1]` is that object:
  - **Shape 7**, an aligned row appended after naming: not refused. The generator reads 8 rows and the name hashed 7, so the cache holds a netlist under a name that does not describe its decode, and every later build reuses it.
  - **Shapes 5/6**, a re-collection into the same list (clear+extend, `[:] =`): refused, but as "the naming step's list is not aligned powers of two", with no cache-removal instruction. Yet the pinned `add_sources` (`core.py:540-545`) has just generated a single-mask netlist under the pieces' name.
    - After the operator corrects the LiteX, the next build names the pieces and hits that cache entry. The guard then passes, because every list equals the pieces.
    - That is a silent single-mask build: the outcome the guard exists to prevent, reached in two steps. Only the region-decode simulation, which no workflow runs, would catch it.
  - With a one-line snapshot, `named.append(list(VexiiRiscv.memory_regions))`, shapes 3 to 7 are all refused with the cache-removal message, and the pinned order is still built exact (`receipts/probes/guard_probe2-snapshot-fix.txt`).
- **Why MINOR and not SUGGESTION:**
  - In round 1 the same class of gap was a SUGGESTION, because the guard was optional hardening there.
  - Round 2's ruling makes the refusal a required behaviour, and the design doc and docstring now state it as fact.
  - So the stated behaviour is not what the code does, and the test arm that grades it has no shape that would show the difference.
  - It is not wording only. No shipped path is affected at the pinned LiteX.
- **Lenses:** Robustness (invalid re-pin ordering), Tests (the SHAPES arm cannot fail for this defect), and Docs (the design doc, the docstring and the PR state a refusal that does not happen). Conformance is not attributed: #791's Required items do not include the guard.
- **Impact:** at a LiteX re-pin, an in-place change to the region list after naming either builds silently with a name that does not identify its decode (shape 7), or poisons the netlist cache without telling the operator (shapes 5/6). A later build can then use the single-mask decode silently.
- **Required outcome:**
  - The guard compares every list the generator may read against a copy of the list the naming step handed to LiteX's naming, taken at naming time. Then any in-place change after naming is refused with the cache-removal refusal.
  - `test_ctrl_memory`'s decode arm adds at least one in-place shape (for example, a row appended to the class list after naming, or clear+extend with the whole rows) and requires the cache-removal refusal.
  - A mutant that removes the copy is caught by name. The mutant anchor texts that quote the changed line (`ctrl_memory_decode.py:53-54`, `_HANDED`, and `:65`) have to follow it.
  - The doc, docstring and PR text are then true as written. If the executor prefers to narrow the claim instead, the doc, docstring and PR must say that in-place changes are not detected.
- **Verification:**
  - `tools/guard_probe2.py <clone>` at the fix head prints `refused; reason names-cache` for shapes 3 to 7 and `built exact` for shape 1;
  - `test_ctrl_memory.py` passes, with the new shape and its mutant caught;
  - the region self-test is unchanged;
  - the netlist names are unchanged, since the copy changes neither the hashed list nor the rows.

### R5 - RESIDUE - Docs - "instead of building a decode other than the pieces"

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:54` and `sw/litex/milan_soc.py:3250-3251`.
- **The problem:** in the second shape the pinned LiteX has already generated, and cached, a netlist with a decode other than the pieces when the refusal fires. The next sentence (`:57`, `:3255-3258`) says so. What is refused is the build's output, not the generation.
- **Exact fix:**
  - doc `:54`: "After LiteX's finalize the build is refused by name, instead of producing an image whose decode is other than the pieces, in two re-pinned LiteX shapes."
  - docstring `:3250-3251`: "After LiteX's finalize, two re-pinned LiteX shapes are refused instead of producing an image whose decode is other than the pieces:".

### S3 - SUGGESTION - Robustness - refuse before the generator writes the cache

- **Where:** `sw/litex/milan_soc.py:3271-3285`.
- **The issue:** the refusal comes after the pinned `add_sources` has run the generator, which is why it has to ask for a cache entry to be removed.
- **Optional:** also check the lists immediately before generation, for example by wrapping the instance's `add_sources`, which the pinned `do_finalize` calls after naming. A stray list would then be refused before any netlist is written under the pieces' name. Keep the after-finalize check for shapes that bypass that hook.

### S4 - SUGGESTION - Robustness - unreachable branch

- **Where:** `sw/litex/milan_soc.py:3277`.
- **The issue:** in `pieces = list(named[-1]) if named else []`, the `else []` is unreachable, because `if not named:` has just raised.
- **Optional:** drop it. This matters if F5's fix rewrites the line anyway.

## Prior public findings on this PR, resolved or retained at this head

The prior review rounds on this PR are R825-1 (`[R825] POSITIVE`) and R826-1 (`[R826] NEGATIVE`). Their findings are taken from my R826-1 report, which recorded R825-1's.

| Prior finding | At this head | Disposition |
|---|---|---|
| R826-1 F1, MINOR Docs (= R825-RES-1): the generator described as one mask compare per region; `:389` named `sram` | All four places corrected; checked against `generator_terms.txt` and netlist `18be4f88` | **Resolved** |
| R826-1 F2, SUGGESTION Robustness/Tests (= R825-S-1): the guard does not refuse a list re-collected after naming or kept on the instance | Both refused (runs 1 and 3); the re-pin procedure names both checks; the PR wording is as asked | **Resolved** for both named shapes. The in-place variant of the same cause is **new as F5** |
| R825-S-2, SUGGESTION Tests: no workflow runs the region test at a re-pin | Still no workflow runs the region-decode simulation. `test_ctrl_memory.py` does run, in `elaborate`'s LiteX aggregate (`scripts/run_litex_sims.sh`). The re-pin procedure now names both, and the PR's Known limitations and the design doc state it | **Retained as SUGGESTION, mitigated** by the documented re-pin procedure |
| R826-1 F3, RESIDUE Docs (`ctrl_region_decode/README.md:7`) | Exact text | **Resolved** |
| R826-1 F4, RESIDUE Docs (`ctrl_region_decode/README.md:101`) | Exact text | **Resolved** |
| R826-1 Issue candidate: the instruction-cache refill into `CtrlMemory`'s `err` hole | The PR's Known limitations carry it as a candidate issue | **Retained** for the manager (out of scope) |

## Lens results at the exact head

[R826] PASS Conformance - #791 Required 1-3 at `sw/litex/ctrl_memory.py:136-163`, `sw/litex/milan_soc.py:3239-3301`, runs 1, 2, 7 and the executor's `decode/product-decode.log` (index-verified, run 8) - the delta changes neither the pieces nor the rows the generator is handed, nor any netlist name. Option (a) and its reasons are stated correctly at this head. The edge test and its single-mask mutant fail exactly the named checks (4/4). All-fabric is byte-identical under the executor's compare, with netlist hashes equal to mine. F5 concerns the hardening guard, which is not a Required item.

[R826] PASS RTL - netlists `88c5cdf9`, `18be4f88`, `57948043`, `f8b27436`, `99bc789b`, `f5f08b17`, `7c73187a` (`receipts/netlists/netlist-sha256.txt`, run 2) - every netlist the delta's runs elaborate is named and hashed as at `03447eaa`. The delta touches no RTL, generator input, clock, reset or CDC path, so round 1's netlist verdict carries over unchanged.

[R826] UNCLEAN Robustness - `sw/litex/milan_soc.py:3264-3301`, `tb/verilator/ctrl_service_budget/split_soc.py:404-452`, runs 3-5 - F5 is open. `CpuPatches` `as-built` and `cover` are correct: `cover` still refuses a non-cover list, and `as-built` reaches the single-mask control without the hookup (run 2).

[R826] UNCLEAN Tests - `sw/litex/ctrl_memory_decode.py:47-190`, `sw/litex/test_ctrl_memory.py`, `tb/verilator/ctrl_region_decode/*` (runs 1, 2) - F5: the SHAPES arm has no in-place shape. Every other new check can fail: each of the five new mutants is caught by its named check, and the self-test's three planted decodes each fail exactly their KILLS.

[R826] UNCLEAN Docs - `docs/design/SPLIT_CONTROL_MEMORY.md:36-62,396`, `sw/litex/ctrl_memory.py:137-150`, `sw/litex/patches/README.md:38-52`, `tb/verilator/ctrl_region_decode/README.md:7,101`, `tb/verilator/ctrl_service_budget/README.md:155`, the PR body, docs gates (run 6) - F5 (`:56-57` and the PR state a refusal the code does not make for in-place changes). R5 is RESIDUE. F1, F3 and F4 are resolved, and there is no comment-rule residue in the delta.

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #791 Required 1-3; `ctrl_memory.py:136-163`; `milan_soc.py:3239-3301`; runs 1, 2, 7; the executor's product decode receipt | R826-2 | 596e2ae3708c4693e0929b530fea37020dc8db25 |
| RTL | CLEAN | Seven CPU netlists by name and sha256; the delta has no RTL or generator-input change (round 1's netlist analysis carries over) | R826-2 | 596e2ae3708c4693e0929b530fea37020dc8db25 |
| Robustness | UNCLEAN (F5 MINOR open) | `exact_cpu_decode`, `cpu_region_lists`; `CpuPatches`; guard probes runs 3-5 | R826-2 | 596e2ae3708c4693e0929b530fea37020dc8db25 |
| Tests | UNCLEAN (F5 MINOR open) | `ctrl_memory_decode.py`; `test_ctrl_memory.py` run 1; region self-test run 2 | R826-2 | 596e2ae3708c4693e0929b530fea37020dc8db25 |
| Docs | UNCLEAN (F5 MINOR open; R5 RESIDUE) | `SPLIT_CONTROL_MEMORY.md`; the `ctrl_memory.py` docstring; `patches/README.md`; the two harness READMEs; the PR body; docs gates run 6 | R826-2 | 596e2ae3708c4693e0929b530fea37020dc8db25 |

## Clone restoration

`receipts/clone-verify.txt`:
- HEAD is `596e2ae3708c4693e0929b530fea37020dc8db25`, and `write-tree` equals `HEAD^{tree}`, `e7f1b5919e7dab3928769c147da97f9f758b785a`.
- The index equals the HEAD tree in mode, blob and path over 1552 entries.
- No staged or unstaged change.
- 0 untracked or ignored entries. The ignored products of runs 1 and 2 were removed with `git clean -fdX`, including one `__pycache__` in `protocol-processor`: `__pycache__`, `sw/builder/out/` and `configs/generated/*.hex`.
- The six gitlinks are as at head. The five checked-out submodules are at their gitlinks and clean, and `external` is uninitialised.
- No file in the clone was edited. Run 5's fix exists only in memory.

## Real limits

- Not re-run here; I read the executor's index-verified receipts instead:
  - the product split export's decode check at 1x1 and 8x8 (`f8b27436`);
  - the all-fabric compare;
  - the split boots;
  - the S2 runs;
  - the full four-shard sweep;
  - the workflow-step replay.
  The delta does not change the generator input of any of them, and the netlist hashes match (run 7).
- The packet commit `7a130467` carries no cryptographic signature (the API reports `unsigned`). Its integrity was checked only through its own `INDEX.md` sha256 prefixes, for seven receipts.
- The guard probes use stand-in finalizes. The in-place shapes are hypothetical re-pins, constructed to falsify the stated claim. No shipped path at the pinned LiteX is affected.
- Hosted contexts at this head were mostly queued or in progress at the snapshot. A skipped or unfinished context is not evidence either way, and the manager owns hosted and act acceptance.
- No manager source bank exists at this head, and none is inferred. Source-head execution evidence is the executor's published receipts plus this review's runs.
- Physical calibration NOT RUN. Field skips are not hardware proof. No hardware was used.

## Pending manager duties

- F5 must be fixed (or the claim narrowed in the doc, docstring and PR), then re-reviewed under Robustness, Tests and Docs at the new head.
- Carry R5 to the residue checklist.
- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `fa6c094b8e196666a8a8865788d5e83b5bbaea09`) with the builder and native banks, and link the receipts.
- Hosted acceptance at the exact head. At the snapshot, 39 of 45 check runs were queued or in progress.
- Open the Issue for the instruction-cache refill into `CtrlMemory`'s `err` hole (carried from R826-1).
- Decide on the round-1 extra cache entry `VexiiRiscvLitex_88c5cdf9...` (R826-1 Deviations). It is still present and is used by run 2.

R826-2 FINISHED
