[R826] POSITIVE - exact head c7e4badb4caf61dcf47e122dc79de7b709125ec9

# R826-3: external cleared-context delta review of PR #888 (issue #791)

- Head `c7e4badb4caf61dcf47e122dc79de7b709125ec9`, tree `67add9f0786e2b667419a55a59a1d0404a6e9e0f`. Source base `1d6bf555`.
- The delta is `596e2ae3..c7e4badb`. It is one commit by the executor, under the round-3 ruling on #791. That ruling says: fix F5 exactly; nothing else changes; STOP if a generated netlist or all-fabric export byte moves.
- The commit message is one line, with no trailers.
- The commit touches two files only: `sw/litex/milan_soc.py` (+9 -6) and `sw/litex/ctrl_memory_decode.py` (+24 -9).
- **Order of reconstruction:**
  1. AGENTS.md.
  2. The round-3 ruling.
  3. `git diff 596e2ae3..c7e4badb` and the full functions it touches: `exact_cpu_decode`, `cpu_region_lists`, `standin`, `finalized`, `arms`.
  4. The pinned LiteX `VexiiRiscv.generate_netlist_name`, which only reads `memory_regions` to hash it.
  5. The executor's REVIEW READY for this head on the PR, and the PR body at this head.
- **Prior findings.** The prior R826-2 findings (F5, R5, S3, S4) were read in the PR thread after the delta pass and its probes were complete. Their dispositions are below.
- **Other reviewers.** No other reviewer's report was read. This round has one reviewer.
- **Verdict: POSITIVE.**
  - F5 is resolved at its cause. The control fails without the fix.
  - Nothing outside F5's scope changed.
  - No CPU netlist byte moved. No all-fabric export input is reachable from the delta.
  - Every lens is CLEAN at this head.
  - Two RESIDUE items (R5, retained by ruling; R6, new) and three SUGGESTIONs remain open for the manager's checklist.

## What this review ran

**Environment:**
- The product LiteX venv (LiteX `a1e1c365`, migen `4c2ae8df`, pythondata-cpu-vexiiriscv `15cfab52`). These equal `sw/litex/litex_pins.txt`, and the venv was used read-only with `PYTHONDONTWRITEBYTECODE=1`.
- The pinned RV32 SDK.
- The pinned Verilator wrapper, identity `Verilator 5.050 2026-07-01 rev v5.050`.
- `PYTHONHASHSEED=0` and offline sbt.
- Every LiteX run carried `tools/noguard/sitecustomize.py`, which refuses any generator command. No receipt contains `REVIEW GUARD`.
- Host paths in receipts are replaced by placeholders such as `<clone>`, `<packet>`, `<litex>`, `<sdk>`, `<generator-cache>` and `<tools>`.
- `tools/run_all.sh` ran runs 1, 2, 5 and 7 concurrently.

| # | Run | Result | Receipt |
|---|---|---|---|
| 1 | `sw/litex/test_ctrl_memory.py` at the exact-head clone | 185 `[ok  ]`, 0 `[FAIL]`, `test_ctrl_memory: 0 failure(s)`, `RESULT: PASS` (link arm ran, not a skip), rc 0. Both new shapes are refused with the cache-removal words (log lines 122-123). All 59 mutants are caught, including `the named list not copied` (line 190, caught by the in-place re-collection check) | `receipts/tcm/run.{log,rc}` |
| 2 | `tools/decode_arm.py` (only `ctrl_memory_decode.arms`) at the head | 12 ok, 0 failures, rc 0 | `receipts/probes/decode-arm-at-head.*` |
| 3 | **Control:** the same arm on a copy of the head with only the fix line reverted (`named.append(VexiiRiscv.memory_regions)`; `receipts/reverted-control.diff` is the whole difference) | rc 1, **2 failures**. `re-collected in place after naming` is refused, but only as `not aligned powers of two`, without the cache-removal words. `a row appended in place after naming` gives `(None)`: not refused at all | `receipts/probes/decode-arm-head-fix-reverted.*` |
| 4 | The same arm at the parent `596e2ae3` | 0 failures. The parent's arm had no in-place shape, which is the Tests half of F5 | `receipts/probes/decode-arm-at-596e2ae3.*` |
| 5 | The previous round's `tools/guard_probe2.py`, unchanged, at the head | Shape 1 `built exact`; 2 `never-named`; **3-7 `refused; reason names-cache`** | `receipts/probes/guard_probe2-at-head.*` |
| 6 | The same probe at `596e2ae3`, and at the head with the fix reverted | Both: shapes 5 and 6 `refused; reason not-aligned`; **shape 7 `BUILT, GENERATOR LIST != HASHED LIST, SILENTLY`**. This reproduces F5 and shows that the one line is the whole fix | `receipts/probes/guard_probe2-at-596e2ae3.*`, `guard_probe2-head-fix-reverted.*` |
| 7 | `tb/verilator/ctrl_region_decode/run.py --self-test` at the head | `none: fails 0, wants 0`; `single-mask: fails 4, wants 4`; `cover: fails 6, wants 6`; `ctrl_region_decode self-test: PASS`, rc 0. Netlists `88c5cdf9` (none), `18be4f88` (single-mask), `57948043` (cover), all read from the cache | `receipts/sims/region-self-test.{log,rc}` |
| 8 | sha256 of the generator cache's `.v` files, before and after every run; sha256 of the three named netlists against the previous round's receipt at `596e2ae3` | Cache listing byte-identical, 1069 files (`cmp` equal). `6b5a22fc`, `d425a0e7` and `b47ecbdf` are each equal to the `596e2ae3` receipt | `receipts/netlists/*` |
| 9 | `scripts/check_py_idiom.py`; `check_doc_style.py`; `check_em_dash.py --base 596e2ae3` and `--base 1d6bf555` (pinned markdown venv, html5lib 1.1); `git diff --check 1d6bf555 HEAD` and `596e2ae3 HEAD` | All rc 0. Idiom budgets at 0 <= 0. `documentation style: OK`. `0 finding(s)`, arms 339/339. No diff-check output. (A first em-dash attempt in the wrong interpreter exited 2 with "cannot judge"; the receipts kept are the pinned-venv reruns) | `receipts/docs/*`, `receipts/diff-check.*` |
| 10 | Residue scan of the 33 added lines: lane labels, lane names, review rounds, reviewer IDs, issue-comment IDs, `F<n>`, em dashes | No hits | (scan in this report) |
| 11 | Hosted contexts at this head, a read-only snapshot at 21:22Z | 5 in progress, 4 queued; none completed, none skipped or failed yet; PR not draft | `receipts/hosted-snapshot.txt` |
| 12 | Clone restore check | HEAD and tree exact. `write-tree` equals the head tree. The index equals `ls-tree` (mode, blob, path). Every tracked file was rehashed with no mismatch. All six gitlinks are unchanged, and the checked-out submodules are at their gitlinks | `receipts/clone-verify.txt` |

## F5 at its cause

**The cause.**
- `named[-1]` was the class's live list object. So a change in place after naming changed the reference list too, and the after-finalize comparison `rows != pieces` could not see it.
- At the head, `milan_soc.py:3271` stores `list(VexiiRiscv.memory_regions)`.
- The copy is taken immediately before `VexiiRiscv.generate_netlist_name()` runs. The pinned naming step only reads the list (`str(VexiiRiscv.memory_regions)` into md5), so the copy is the list it hashes.
- Rows are tuples, so a shallow copy is a full snapshot.
- `cpu_region_lists` keeps only lists of 4-tuples, so any in-place edit to the class list now differs from the snapshot.

**Required outcomes:**
- **The guard compares against a copy taken at naming.** It does (`:3271`, `:3280-3282`). In-place shapes (runs 5 and 6, shapes 5-7) now get the stray refusal, which names the cached netlist for removal.
- **At least one in-place shape is in the arm, and the arm requires the cache-removal refusal.** There are two:
  - `re-collected in place after naming`: clear, then extend with the whole rows;
  - `a row appended in place after naming`: the aligned `APPENDED` row.
  - `ctrl_memory_decode.py:197-198` now requires `remove it from the generator's cache` for every SHAPES row.
  - That strengthening is what lets the clear-and-extend shape fail without the fix (run 3). Under the old wording it would have passed on the unaligned refusal.
- **A mutant that removes the copy is caught by name.** `the named list not copied` (`:81-82`) is caught (run 1, line 190).
- **The quoted anchors follow the changed line.** `_HANDED` (`:54-55`) and the `pieces handed after the name` mutant (`:64-67`) follow it, and that mutant is still caught (line 182).
- **Doc, docstring and PR are true as written.**
  - `docs/design/SPLIT_CONTROL_MEMORY.md:56` ("a region list other than that step's aligned power-of-two pieces") now holds for in-place changes.
  - The docstrings at `milan_soc.py:3252-3257` and `:3268-3269` state the copy.
  - The PR body's guard bullets and the mutant table row `the named list not copied` match run 1.

**The verification as specified:**
- The probe gives `refused; reason names-cache` for shapes 3-7 and `built exact` for shape 1 (run 5).
- `test_ctrl_memory.py` passes, with the new shapes and the mutant caught (run 1).
- The region self-test is unchanged (run 7).
- The netlist names and bytes are unchanged (runs 7 and 8).

## Nothing else changed; no netlist or export byte moved

- **Scope of the delta.** It touches only the two files above. In `milan_soc.py` the single behavioural change is the `list(...)`; the rest is docstrings. In `ctrl_memory_decode.py` every change is F5's:
  - the module docstring and the `standin` docstring;
  - `_HANDED` and the anchor of `pieces handed after the name`;
  - the new mutant;
  - two SHAPES rows and `APPENDED`;
  - the two in-place branches in `standin`;
  - the strengthened `held`.
- R5, S3 and S4 are untouched, as ruled.
- **Why no generated byte can move.**
  - The snapshot is stored only in the closure's `named` list, and is read only after `finalize()`.
  - The list the naming step hashes, and the rows the generator is handed, are the same objects as at `596e2ae3`.
  - `exact_cpu_decode` has one call site, in `add_ctrl_memory` (`milan_soc.py:3235`), which the all-fabric SoC does not call. So no all-fabric export input is reachable from the delta.
- **Executed evidence for the CPU netlists.**
  - The split export's own `main()` run in `test_ctrl_memory.py`'s SoC arm passed with no generator command. Under the review guard, an uncached name would have been refused.
  - The cache is byte-identical before and after (run 8).
  - The three region-test netlists equal the `596e2ae3` receipt (run 8).
- **The all-fabric compare** at this head is the executor's claim (identical against `1d6bf555`). This review did not rerun it: it is a builder bank, which the round does not allow. The static argument above makes it unreachable from the delta.
- The ruling's STOP condition is not met.

## Findings

### R5 - RESIDUE - Docs - "instead of building a decode other than the pieces" (retained from R826-2, unchanged by ruling)

- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:54`; `sw/litex/milan_soc.py:3250-3251`.
- **Problem:** in the second shape the pinned LiteX has already generated and cached the other decode when the refusal fires. What is refused is the build's output.
- **Exact fix:**
  - doc `:54`: "After LiteX's finalize the build is refused by name, instead of producing an image whose decode is other than the pieces, in two re-pinned LiteX shapes."
  - docstring `:3250-3251`: "After LiteX's finalize, two re-pinned LiteX shapes are refused instead of producing an image whose decode is other than the pieces:".

### R6 - RESIDUE - Tests, Docs - a check label that does not describe the new appended shape (new in this delta)

- **Where:** `sw/litex/ctrl_memory_decode.py:200`: `f"exact_cpu_decode refuses a CPU whose generator may read the whole rows after naming: {shape} "`.
- **Problem:** for `a row appended in place after naming`, the generator reads the pieces plus the aligned `APPENDED` row, not "the whole rows". The label was accurate for every shape before this delta.
- **Why RESIDUE:**
  - It is only the printed description of a graded fact.
  - The boolean that grades it (`seen == [SPLIT_PIECES] and held`) is right for all five shapes.
  - No file or gate reads that text (a repository grep finds only this line).
  - The fix changes no check outcome, mutant kill, figure or claim.
- **Exact fix:** `f"exact_cpu_decode refuses a CPU whose generator may read a region list other than the pieces after naming: {shape} "`.

### S3 - SUGGESTION - Robustness - refuse before the generator writes the cache (retained)

- `milan_soc.py:3274-3286`.
- Unchanged. This is optional hardening: also check the lists just before generation, for example around the instance's `add_sources`.

### S4 - SUGGESTION - Robustness - unreachable branch (retained)

- `milan_soc.py:3280`: `pieces = list(named[-1]) if named else []`.
- The `else []` is unreachable after `if not named: raise`. Unchanged, as ruled.

### S5 - SUGGESTION (issue candidate) - Docs - stale mutant count in TESTING.md

- **Where:** `docs/testing/TESTING.md:792`: "Its forty-four mutants each rebuild one function or class".
- **Evidence:** `test_ctrl_memory.MUTANTS` has 47 rows at the source base `1d6bf555`, 47 + 6 at `03447eaa`, 47 + 11 at `596e2ae3`, and 47 + 12 = 59 at this head (run 1 grades 59).
- **Why not a finding against this PR:**
  - The figure was already wrong at the source base. This PR does not touch `TESTING.md`.
  - The round-3 ruling forbids other changes.
  - The PR's own text states its mutant counts correctly ("twelve mutants", "Six mutants").
- **Suggested outcome:** a separate Issue makes the page state the count, or derive it, so it cannot drift. Raised for the manager to file or fold into the merge turn.

## Prior public findings on this PR, at this head

| Prior finding | At this head | Disposition |
|---|---|---|
| R826-2 F5, MINOR Robustness/Tests/Docs: the guard compares against the live list | Fixed at its cause (`:3271`). Two in-place shapes are required with the cache-removal words. The removing mutant is caught. The control fails without the fix (runs 3 and 6) | **Resolved** |
| R826-2 R5, RESIDUE Docs | Unchanged, as ruled | **Retained as RESIDUE** (exact fix above) |
| R826-2 S3, S4, SUGGESTION Robustness | Unchanged, as ruled | **Retained as SUGGESTION** |
| R826-1 F1-F4 (and R825-1's R825-RES-1 and R825-S-1) | Resolved at `596e2ae3`. The delta touches none of their artifacts | **Resolved** (prior verdict stands) |
| R825-S-2, SUGGESTION Tests: no workflow runs the region-decode test at a re-pin | Unchanged; the re-pin procedure names it | **Retained as SUGGESTION, mitigated** |
| R826-1 issue candidate: instruction-cache refill into `CtrlMemory`'s `err` hole | Still in the PR's Known limitations | **Retained** for the manager (out of scope) |

## Lens results

```text
[R826] PASS Conformance - #791 round-3 ruling F5 item; sw/litex/milan_soc.py:3268-3286 at c7e4badb; receipts/probes/guard_probe2-at-head.log - the guard now compares against a copy of the list the naming step hashed, and every shape the ruling names is refused with the cache-removal refusal. #791's Required items 1-3 depend on no line the delta touched (export check, line 112 of receipts/tcm/run.log, still ok)
[R826] PASS RTL - receipts/sims/region-self-test.log, receipts/netlists/netlist-sha256.txt, cache-v-before/after.txt - the delta changes no HDL and no generated CPU netlist. The region self-test is unchanged (0/0, 4/4, 6/6) with netlists 88c5cdf9, 18be4f88 and 57948043, byte-equal to the 596e2ae3 receipt. The generator cache is byte-identical. The all-fabric SoC cannot reach exact_cpu_decode (single call site, milan_soc.py:3235)
[R826] PASS Robustness - milan_soc.py:3271 against pinned vexiiriscv/core.py generate_netlist_name; receipts/probes/guard_probe2-*.log - rebound, instance, clear+extend, slice-assign and appended-row re-pins are all refused naming the cache. The copy is a full snapshot (tuple rows) taken just before a read-only hash. S3 and S4 remain optional
[R826] PASS Tests - sw/litex/ctrl_memory_decode.py:81-88,143-150,195-201; receipts/tcm/run.log lines 122-123,182,190; receipts/probes/decode-arm-head-fix-reverted.log - the new shapes fail without the fix (2 failures). The strengthened refusal words are what make clear+extend fail. The new mutant is caught by name. 59/59 mutants, 185 ok, 0 FAIL. R6 is label wording only
[R826] PASS Docs - milan_soc.py:3250-3257,3268-3269; ctrl_memory_decode.py:13-18,121-126; docs/design/SPLIT_CONTROL_MEMORY.md:54-57; PR body "The naming guard" and "The guard's tests" at c7e4badb; receipts/docs/* - each states what the code now does. Docs gates are green. No lane, round, reviewer or comment-ID residue in the 33 added lines. R5 and R6 are RESIDUE; S5 predates the PR
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round-3 ruling (F5); `milan_soc.py:3239-3289`; guard probe at the head; export check in the test log | R826-3 | `c7e4badb4caf61dcf47e122dc79de7b709125ec9` |
| RTL | CLEAN | Region-decode self-test log; netlist sha256 against the `596e2ae3` receipt; generator cache listing before and after; `exact_cpu_decode` call site | R826-3 | `c7e4badb4caf61dcf47e122dc79de7b709125ec9` |
| Robustness | CLEAN | `milan_soc.py:3268-3286`; pinned `generate_netlist_name`; guard probe at the head, at `596e2ae3`, and with the fix reverted | R826-3 | `c7e4badb4caf61dcf47e122dc79de7b709125ec9` |
| Tests | CLEAN | `ctrl_memory_decode.py` (delta in full); `test_ctrl_memory.py` run log (185 ok, 59/59 mutants); decode arm at the head, at `596e2ae3`, and with the fix reverted | R826-3 | `c7e4badb4caf61dcf47e122dc79de7b709125ec9` |
| Docs | CLEAN | Both docstrings; design doc `:54-57`; PR body at the head; Python idiom, doc style and em-dash gates; `git diff --check`; residue scan | R826-3 | `c7e4badb4caf61dcf47e122dc79de7b709125ec9` |

- Lenses whose artifacts the delta did not touch keep their R826-2 coverage, and are re-banked here at this head:
  - RTL HDL and harness sources are byte-unchanged since `596e2ae3`;
  - the design doc is unchanged since `596e2ae3`.
- R825-1 is POSITIVE at the ancestor `03447eaa`.

## Real limits

- **Not rerun here:**
  - the all-fabric export compare;
  - the split export decode check at 1x1 and 8x8;
  - the full builder, parent, PP, gPTP and Yosys banks;
  - the split boots;
  - every docs.yml job other than the four gates in run 9.
- Those results are the executor's claims at this head (REVIEW READY on the PR). No author packet for this head was available to hash-check.
- This review's own evidence for them is static: one call site, and an unchanged hashed list and generator input. Executed evidence covers the region-test CPUs and the cache.
- No manager source bank at this head is claimed or inferred.
- Hosted contexts were all still in progress or queued at the snapshot. No hosted result is claimed.
- Physical calibration was NOT RUN. No hardware or field result is implied.
- Gitignored outputs from the SoC arm (`configs/generated/*.hex`, `sw/builder/out/`) were left in the clone. No tracked byte changed.

## Pending manager duties

- Current-dev candidate merge validation: source base `1d6bf555`, live dev `fa6c094b`. This covers the builder and native banks.
- Hosted and act acceptance at this exact head.
- Carry R5 and R6 to the residue checklist.
- File or fold S5, and the retained instruction-cache `err`-hole candidate.
- Merge only with explicit maintainer authorization.

R826-3 FINISHED
