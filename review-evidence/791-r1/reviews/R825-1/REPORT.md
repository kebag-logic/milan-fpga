[R825] POSITIVE - exact head 03447eaa087ba0687362a7372f4a00bd40c6fd46

# R825-1: internal cleared-context review of PR #888 (issue #791)

- Head: `03447eaa087ba0687362a7372f4a00bd40c6fd46`, tree `6fbeedce626546a30cf9a468b774e2b0298a40e5`, two commits on `dev-soft-core` `1d6bf555`.
- Scope: issue #791 Required items 1 to 3, option (a) as the decision; the five lenses of AGENTS.md section 6.
- Reconstructed from: AGENTS.md, the issue body and its three executor comments, the PR body, `git diff 1d6bf555..03447eaa`, the executor's published packet (`review-evidence/791-r1` at `c80c58e9`), and this review's own runs.
- Prior public review findings on this PR or issue: none exist. The PR carries only the two review-start comments, and no review objects or inline comments. Nothing to resolve or retain.
- Verdict: no open BLOCKER, MAJOR or MINOR. One RESIDUE (wording) and two SUGGESTIONs.

## What this review ran (receipts under `receipts/`)

All runs used Verilator 5.050 (the pinned wrapper, identity checked: `Verilator 5.050 2026-07-01 rev v5.050`), the product LiteX tree and the pinned RV32 SDK.
A refusing `sbt` stub was first on `PATH` (`scripts/sbt-stub.sh`), so no run could generate a CPU netlist into the shared generator cache. Every netlist used was already cached.

| # | Run | Result | Receipt |
|---|---|---|---|
| 1 | `tb/verilator/ctrl_region_decode/run.py --self-test`, in the review clone | `SELF-TEST PASS none: fails 0 check(s), wants 0`; `single-mask: fails 4 ..., wants 4`; `cover: fails 6 ..., wants 6`; `ctrl_region_decode self-test: PASS`; rc 0 | `receipts/region-decode/self-test.log`, `soc-*.json` |
| 2 | An exhaustive PMA check that does not use the PR's `decode.py`. A separate textual cone extractor (`scripts/cone_extract.py`) feeds a Verilator sweep of every word address 0..2^32 (`scripts/cone_sweep.cpp`). The expected regions come from LiteX's own `csr.csv` `memory_region` rows. | shipping test CPU: fetch EXACT, load EXACT; single-mask: 24,576 words refused inside `rom`, first 0x8000; cover: 16,384 words admitted past the ends, first 0x38000; split boot CPU: EXACT/EXACT; product split CPU (1x1 and 8x8, DDR3 included): EXACT/EXACT | `receipts/cone/*.txt`, `*.rc` |
| 3 | Product split export at head (builder argv + `--ctrl-mailbox --ctrl-firmware`), at 1x1 and 8x8 | Both name `VexiiRiscvLitex_f8b2743639f353f9ded505dea4bbc545`, as the executor's receipt does. The generator is handed `rom` and `sram` as 0x20000+0x10000+0x8000 at each origin, `main_ram` as 1 GiB on `m`, and the other rows unchanged. The PR's `decode.py` passes both DECODE checks on that netlist | `receipts/cone/product-split-*` |
| 4 | Split boot, 1x1 and 8x8 | 1x1: `BOOT ready ... 84.425 ms`, trace 18 equal, `ctrl_split_boot: PASS (0 finding(s))`, rc 0. 8x8: `184.695 ms`, the same checks, rc 0. Both CPUs are `VexiiRiscvLitex_99bc789b...`, which run 2 finds exact | `receipts/boot/*` |
| 5 | All-fabric: every shipped config, base `1d6bf555` against head, on separate scratch clones (`scripts/af_side.py`, `af_all.sh`, `af_diff.py`) | Every builder output is identical. The CPU netlist name, region rows and generator args are identical: AX7101 `f5f08b17...` at both points, and Arty `7c73187a...` at all three. LiteX's PLL search refuses the Arty exports after the CPU is named, at base and head alike. The AX7101 top Verilog, `csr.csv` and `soc.h` differ raw only in comment lines, and are identical with comments removed | `receipts/allfabric/summary.txt`, `*.diff` |
| 6 | `sw/litex/test_ctrl_memory.py` | 173 `[ok]`, `test_ctrl_memory: 0 failure(s)`, `RESULT: PASS`, rc 0. All six new mutants caught | `receipts/test_ctrl_memory/run.log` |
| 7 | Guard and `CpuPatches` probes against stand-in finalizes (`scripts/guard_probe.py`; nothing written to the clone) | see focus points 2 and 5, and S-1 | `receipts/guard-probe.txt` |
| 8 | `tb/verilator/ctrl_service_budget/run.py --self-test` | `self-test: 0 failures`, rc 0 | `receipts/budget/self-test.log` |
| 9 | Netlist identity against the executor's packet | This review's three test netlists are byte-identical to the executor's (`d43c74db`, `831c88b0`, `e620f662`) apart from the module name. The cache key differed between the two environments; the netlist did not | `receipts/netlists.txt` |
| 10 | Clone restoration | HEAD `03447eaa`, write-tree `6fbeedce`; the index equals the HEAD tree (mode, blob, path); 0 untracked or ignored entries; the six gitlinks as at head | `receipts/clone-verify.txt` |

## The manager's focus points, answered from the code and netlists

1. **The decode is exact.**
   - `decode_pieces(0, 0x38000)` is (0, 0x20000), (0x20000, 0x10000), (0x30000, 0x8000), and the same at 0x1000_0000. The pieces are aligned, disjoint and contiguous, and their union is [origin, origin + 0x38000).
   - `test_ctrl_memory` also checks every region of up to 64 units at every origin below 64 against a search for the fewest pieces.
   - The generated netlists' fetch and load fault terms admit exactly the SoC's regions at every word address. This holds for the shipping test CPU, the boot CPU, and the product split CPU at 1x1 and 8x8, by two independent readers (runs 2 and 3).
   - One word past each end, the shipping decode passes the run-1 checks `rom`/`sram` "a load one word past its end ... (cause 5) before its bus" and "a fetch ... (cause 1) before its bus".
   - The grader requires exactly one trap of that cause, `mtval` equal to the address (and `mepc`, for a fetch), and no bus command for that word or line.
   - Under `cover` those checks fail with `1 command(s) for it on the bus`, so the no-bus-command part of the check can fail.
2. **The guard.**
   - `exact_cpu_decode` refuses a finalize that never runs the instance naming step. The probe shows this refusal for a finalize that names its netlist inline, and for one that calls `VexiiRiscv.generate_netlist_name()` instead of `self.`.
   - A naming step called twice is idempotent: the pieces of the pieces are the pieces.
   - It does not refuse a re-pinned finalize that names before it collects the regions. In that probe the generator would be handed the whole regions, with no refusal.
   - The design doc's own claim is accurate: a LiteX that "stops calling that step fails the build".
   - The executor's REVIEW READY sentence "so a re-pinned LiteX cannot silently restore the single mask" is broader than what the guard proves. The repository's tests (`export_check` and the region test) would catch that reordering, but nothing runs them at a LiteX re-pin.
   - Recorded as S-1, not as a defect: no shipped path is affected at the pinned LiteX.
3. **The mutants fail by their own words** (run 1).
   - `single-mask` fails exactly these checks:
     - `rom: a load at each seam ...` (`0x0001fffc: trap cause 5; 0x0002fffc: trap cause 5`);
     - `rom: a fetch at each seam ...` (`... trap cause 1`);
     - both DECODE checks (`first difference 0x00008000`, refused inside).
   - `cover` fails exactly the four past-the-end checks and both DECODE checks (`first difference 0x00038000, admitted outside`).
4. **All-fabric is identical** (run 5).
   - I repeated the comment-stripped diff myself. At AX7101 1x1 the only raw differences are:
     - the `csr.csv` `#` timestamp line;
     - the `soc.h` `//` timestamp line;
     - in the top Verilog, the `// Date` and `Auto-Generated by LiteX on` lines, and the reordered `[BB:...]` lines of the module-hierarchy listing, which sit inside the header `/* */` block.
   - With comments removed, all three files are identical. At 8x8 the differences are the same kind, with fewer reordered lines.
   - The executor's claim holds.
5. **`CpuPatches` `cover`** (run 7). It records the SoC's whole regions in every case below:
   - with the shipping split, it names the netlist and does not refuse;
   - with the split removed (`cpu_regions` returning the whole rows), it refuses with `the split SoC hands the CPU generator a region it decodes inexactly (#791)` and does not widen the list;
   - with a list that is already its own power-of-two cover, it does not refuse;
   - `as-built` never refuses.

   The boot runs (run 4) go through `CpuPatches('cover')` with the shipping list.
6. **The split boots to ready** at 84.425 ms (1x1) and 184.695 ms (8x8), trace 18 of 18, PASS. These are this review's own runs (run 4).
7. **The sweep's `gptp_shadow` failure.** From the executor's receipt; not re-run here.
   - The first run fails at `test_mutant_lifecycle.py:234` with `REFUSED: CLEANUP FAILED: owned descendants remain`, and its 325 RTL checks pass.
   - That is #833's recorded signature: the `owned_process.py` cleanup raise, at `:234`, one of the sites #833 lists.
   - The re-run passes (`RESULT: PASS`, rc 0).
   - The PR changes no `gptp_shadow`, gPTP or `owned_process` file.
   - The shard totals sum to the claimed 65 suites and 2,192,899 checks.

**The candidate defect should be its own Issue.** The defect is that an instruction-cache refill into `CtrlMemory`'s err hole never completes.
- The executor's observation log shows a `FETCH 00038000` refill under the cover decode. The simulation then hits its time limit with no further fetch response, which is a CPU liveness hazard.
- The shipping plan still leaves an err hole inside each region, past the image's last bank. The exact decode admits that hole, so a fetch-ahead past the last bank can reach the hazard at this head.
- It is not a regression of this PR: the in-region hole was just as reachable before, and this PR removes the past-the-end path. It is also not #791's decode, so it is out of scope here.

## Findings

### R825-RES-1 - RESIDUE - Docs
- **Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:39-40`; `sw/litex/ctrl_memory.py:139-142` (the `decode_pieces` docstring); the PR body's "The fault (#791)" paragraph.
- **The claim:** "The VexiiRiscv generator checks each fetch and load against each region it is handed with one mask compare, `(address & ~(size - 1)) == origin`. That compare is exactly the region only when the size is a power of two and the origin a multiple of it."
- **Evidence that it is false as a general statement:**
  - The single-mask netlist (`receipts/netlists.txt`; lines 12924-12928 and 16697 of `VexiiRiscvLitex_18be4f88...`) decodes `sram` exactly. `sram` is just as non-power-of-two (224 KiB at 0x1000_0000), and is decoded as three terms: `(A & 32'hfffe0000) == 32'h10000000`, `(A & 32'hffff0000) == 32'h10020000` and `(A & 32'hffff8000) == 32'h10030000`. Only `rom`, at origin 0, gets the single mask `32'hfffc8000`.
  - The PR's own `ctrl_region_decode/README.md` and `run.py:137` say that the single-mask netlist's `sram` terms are exact.
- **Impact:** wording only. It changes no code, test, figure or verdict, but a reader is misled about which regions the generator decodes wrongly.
- **Exact fix:** in each of the three places, replace the two sentences with: "At the pinned generator a region handed whole is not always decoded exactly: the 224 KiB `rom` at origin 0 is decoded as one mask compare, `(address & 0xfffc8000) == 0`, which leaves out every address with bit 15 set, while the same-sized `sram` at 0x1000_0000 is decoded exactly. Handing the generator aligned power-of-two pieces makes every region's decode exact without depending on that behaviour."

### R825-S-1 - SUGGESTION - Robustness
- **Where:** `sw/litex/milan_soc.py:3239-3271`, `exact_cpu_decode`'s `do_finalize` wrapper.
- **Evidence:**
  - `receipts/guard-probe.txt`, case `name-then-collect`: `refused=False ... generator_list_exact=False`.
  - The refusal runs only after LiteX's finalize. So in the refused shapes, the whole-region netlist may already have been generated before the refusal.
- **Optional improvements:**
  - After `finalize()`, also refuse unless `VexiiRiscv.memory_regions` is still the list the naming step produced and every row is an aligned power of two.
  - Name `test_ctrl_memory.py` and `tb/verilator/ctrl_region_decode` in the LiteX re-pin procedure (`sw/litex/patches/README.md`).

### R825-S-2 - SUGGESTION - Tests
- **Where:** `tb/verilator/ctrl_region_decode/run.py`, `sw/litex/test_ctrl_memory.py`.
- **Evidence:** no workflow runs either test (a search of `.github/workflows`).
  - This is deliberate and documented: the README explains why the directory has no Makefile.
  - It still leaves the single-mask guard rail as a manual gate.
- **Optional improvement:** record in the Issue which manual gate a LiteX or VexiiRiscv re-pin must re-run.

No other findings. The comment rule was checked over the delta's added lines: no bench lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs.

## Lens results (each applied at the exact head)

| Lens | Result | Artifacts examined |
|---|---|---|
| Conformance | PASS | #791 Required 1: option (a) is stated with its reasons in the PR body and `SPLIT_CONTROL_MEMORY.md:37-60`, and the decode is exact (runs 2, 3). Required 2: `ctrl_region_decode/run.py:98-142` fetches and loads the last word and the word past the end of `rom` and `sram`, and the single-mask mutant fails named checks (run 1). Required 3: the all-fabric CPU netlist's name, rows and args are identical for all 5 configs (run 5) |
| RTL | PASS | The PMA fault terms and bus-decoder compares of netlists `88c5cdf9`, `99bc789b` and `f8b27436`, checked exhaustively (runs 2, 3). The cover and pieces netlists differ only in PMA and `argsHits` decode lines (counted in this review). No clock, reset, CDC, cache or ISA argument changed: `vexii_args` are equal, as are the `soc.json` files of run 1 |
| Robustness | PASS | `ctrl_memory.py:136-163`: `decode_pieces` refuses a negative origin or a size <= 0, splits greedily into aligned pieces, and `test_ctrl_memory` sweeps it exhaustively over 64x64. The guard and `CpuPatches` refusal paths (run 7). The past-the-end fault paths (run 1). The err-hole refill hazard is recorded as a separate Issue candidate |
| Tests | PASS | `ctrl_region_decode/{run.py,decode.py,probe.S,sim_main.cpp,region_soc.py}`: each mutant fails exactly its KILLS. On the netlists checked here, `decode.py` agrees with an independent exhaustive reader. `test_ctrl_memory.py`: all six new mutants caught (run 6). Regressions: boot (run 4), S2 self-test (run 8), and the executor's sweep receipt (65 suites; the #833 flake's re-run passes) |
| Docs | PASS (RESIDUE R825-RES-1 carried) | `docs/design/SPLIT_CONTROL_MEMORY.md`: the new section and the section 4 note. `ctrl_service_budget/README.md:150-155,1058`. `ctrl_split_boot/README.md:51-52`: its results are labelled as measured under the cover, and this review's re-run values are consistent with them. `ctrl_region_decode/README.md`. The PR body |

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #791 Required 1-3; the PR body; `SPLIT_CONTROL_MEMORY.md` section 1; runs 1, 2, 3, 5 | R825-1 | 03447eaa087ba0687362a7372f4a00bd40c6fd46 |
| RTL | CLEAN | Generated CPU netlists `88c5cdf9`, `18be4f88`, `57948043`, `99bc789b`, `f8b27436`, `f5f08b17`, `7c73187a` (PMA and decoder terms); `milan_soc.py:3235-3271` | R825-1 | 03447eaa087ba0687362a7372f4a00bd40c6fd46 |
| Robustness | CLEAN | `ctrl_memory.py:136-163`; `milan_soc.exact_cpu_decode`; `split_soc.CpuPatches`; the guard probes; the past-the-end fault paths | R825-1 | 03447eaa087ba0687362a7372f4a00bd40c6fd46 |
| Tests | CLEAN | `tb/verilator/ctrl_region_decode/*`; `sw/litex/ctrl_memory_decode.py`; `sw/litex/test_ctrl_memory.py`; runs 1, 4, 6, 8; the executor's sweep receipts | R825-1 | 03447eaa087ba0687362a7372f4a00bd40c6fd46 |
| Docs | CLEAN (RESIDUE R825-RES-1 carried to the residue checklist) | `docs/design/SPLIT_CONTROL_MEMORY.md`; the three harness READMEs; the PR body | R825-1 | 03447eaa087ba0687362a7372f4a00bd40c6fd46 |

## Real limits

- Not re-run here; I inspected the executor's receipts but did not reproduce them:
  - S2's budget runs at 1x1/1if and 8x8/2if (`18 groups graded, 0 refusals`; `17 groups graded, 0 refusals`; rc 0);
  - the full Verilator sweep;
  - the workflow-step replay (497 steps ran, 0 failed; 110 not run, with reasons).
- Not checked: that the test's single-mask netlist matches the CPU of #878's Arty image, and its cover netlist that bring-up's diagnostic. Those artifacts are in neither this branch nor the packet, and no Arty split config exists on this branch.
- Stores, and transfers other than a word, are not graded (a documented limit). The independent sweep also checks only the word load and the fetch.
- Hosted contexts at this head were still running when snapshotted (`receipts/hosted-checks-snapshot.txt`: 31 pass, 24 pending, 1 skipping, the nightly physical gPTP job). A skipped context is not evidence.
- Physical calibration NOT RUN. Field skips are not hardware proof. No hardware was used.
- No manager source bank exists at this head, and none is inferred. The source-head execution evidence is the executor's published receipts plus the runs listed above.
- The executor's environment and this review's gave byte-identical netlists different names: the generator cache key, the netlist name, differed between them. This does not affect correctness. It does mean a fresh environment may regenerate a netlist that is already cached under another name.

## Pending manager duties

- Validate the current-dev merge candidate (source base `1d6bf555`, live dev `46c971fa0a09e2c8ca21acb95769defdc06c3068`) with the builder and native banks, and link the receipts.
- Hosted and act acceptance at the exact head; the split PR gets no act.
- Carry R825-RES-1 to the residue checklist.
- Decide whether to open the Issue for the err-hole instruction-cache refill (recommended).
- The external review's verdict.

R825-1 FINISHED
