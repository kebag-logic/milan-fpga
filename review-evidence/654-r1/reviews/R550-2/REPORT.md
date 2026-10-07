[R550] POSITIVE - exact head 853a7357ba86d758a0e38f65db89a6187fb547bc

Round R550-2, internal independent review of issue #654 / PR #694.
Head `853a7357ba86d758a0e38f65db89a6187fb547bc`, tree `78af3f0b2ca316ad2b14440ff7bd4d64ca322bd2`.
Source base `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`. Delta under review: `d6b6ca89..853a7357` (two commits).
Baseline: R550-1 POSITIVE and R551-1 NEGATIVE (one MINOR), both at `d6b6ca899ae4c248a1342867bb89060e24febcd5`.

Verdict: **POSITIVE**. All five lenses were applied at this head. No BLOCKER, MAJOR, MINOR or RESIDUE is open. One optional SUGGESTION is recorded. Every prior public finding on this PR is resolved at this head.

## 1. Reconstruction

Read in this order: AGENTS.md and CONTRIBUTING.md; docs/README.md; the issue #654 body (acceptance 1-3); assignment 6045462105; STOP ruling 6045774790 (acceptance 3 applies to the two AX7101 product configurations; Arty is excluded under #583); round-2 assignment 6046709819; REVIEW READY 6047197977; then the diff, history and public evidence at `a2917fb3b3fc63c8617c82eaec63f0183d908c05/review-evidence/654-r1`. Prior review findings (R550-1, R551-1 reports) were read only after the independent pass below.

The round-2 frozen items (6046709819) are:

1. R551-1-F1: validate `--l2-bytes` from its token before lossy conversion. `1e-400` and `-1e-400` must exit 2 with the whole-byte reason. Omission and genuine zero keep their meaning. Both tokens go into the CLI bank with a planted control. The reviewer script `byte_count_underflow.py` must return 0.
2. R550-1 RESIDUE: `BUILDING.md:133` must point at section 2.1.
3. R550-1 S2 (recommended): refuse an unknown constructor `cpu`, with a test. S1 (optional): name the isolated-data option of `--netlists`.

Scope (`receipts/scope.txt`): the PR touches exactly four files: `sw/litex/milan_soc.py`, `sw/builder/test_soc_options.py` (new), `sw/builder/test_builder.py` and `docs/integration/BUILDING.md`. No `hdl/`, `configs/`, generator patch, CSR or default change. All four submodule gitlinks are identical at base and head. Each of the three commits has a one-line message with no trailer.

## 2. What changed in round 2 (`d6b6ca89..853a7357`)

- `sw/litex/milan_soc.py:2573` `_parse_l2_bytes`: the CLI token becomes a `Decimal`, so no float rounding happens. A non-numeric token raises `ArgumentTypeError` with the whole-byte reason.
- `:3495` `--l2-bytes` uses that parser instead of `float`.
- `:2582-2599` `_validate_cpu_options`: an unknown `cpu` is refused first (`:2584`). The byte count is checked as `Decimal` for finiteness, sign and integrality (`:2587-2589`). It replaces the `math.isfinite`/`int()` test.
- `sw/builder/test_soc_options.py`: 8 unknown-CPU constructor cases per register width (`:140`). The four CLI refusals `1e-400`, `-1e-400`, `1.000…1` and `invalid` (`:155-158`). Zero-like setup cases `0.0`, `-0` and `0e-400` (`:164-165`). An unknown-CPU guard control (`:183`). Two float-parser controls, one per underflow token (`:201-204`).
- `BUILDING.md:133` now says section 2.1. `:148-149` state decimal-preserving validation and the unknown-CPU refusal. `:159-161` document the cache side effect and `--nax-data-dir`.

Downstream of the parser, the CLI `Decimal` reaches only `int(l2_bytes) if l2_bytes else 0` (`:2663`) on the VexiiRiscv path. CLI NaxRiscv is refused by the product profile at `:3806`. `main()` (`:3925`) is the only in-tree constructor caller, and argparse limits its `--cpu`. So the new unknown-CPU refusal cannot break a tracked caller.

## 3. Executable evidence at this head

The interpreter was the LiteX environment that the builder's own resolver selects (`sw/litex/sweep.sh` venv). `PYTHONHASHSEED=0` and `-B` were set for every run. The independent campaigns ran concurrently.

| Check | Result | Receipt |
|---|---|---|
| Focused refusal bank `test_soc_options.py` | rc 0. 52 constructor cases, 18 CLI cases, 9 controls killed, matching the REVIEW READY counts | `receipts/refusal-bank-head.{log,rc}` |
| Builder registration `test_builder.test_soc_option_refusals()` (single entry, not the full bank) | rc 0. The same 52/18/9 run through the builder's interpreter resolution | `receipts/builder-entry.{log,rc}` |
| `byte_count_underflow.py` (R551-1 script, unchanged, sha256 `6af4325d…`) at head | rc 0. `0` reaches setup. `1e-12`, `1e-400` and `-1e-400` exit 2 with "--l2-bytes must be a finite, non-negative whole number of bytes" | `receipts/underflow-head.{log,rc}` |
| Same script at `d6b6ca89` (detection control) | rc 1. `1e-400` and `-1e-400` reach setup, so the script detects the defect it targets | `receipts/underflow-base-d6b6ca89.{log,rc}` |
| `--netlists --nax-data-dir <isolated copy>` | rc 0. 4 effects (RV32/RV64 FPU and L2=8192 change normalized RTL) and 4 forwarding controls killed. 5 netlists were generated into the isolated copy; the rest were cache hits | `receipts/netlists-head.{log,rc}`, `receipts/nax-isolated-copy-new-netlists.txt` |
| AX7101 byte identity, source base `e21c1ca0` vs head, one tree path, fixed timestamp and Instance repr before generation | rc 0 for both configs. **ax7101_1x1_tdm8 32/32 raw artifacts identical** (population `2ad2308b…`). **ax7101_8x8 32/32 identical** (population `0af782d1…`). Argv equal; both argv carry `--cpu vexiiriscv --l2-bytes 0`, so the new `Decimal('0')` path is exercised. Only the diagnostic `export/litex.log` differs. No tracked file was rewritten | `receipts/ax/compare-fixed-*.txt`, `receipts/ax/*-fixed-*.json`, `receipts/ax/status-*.txt`, `receipts/ax-compare.{log,rc}` |
| Reviewer edge-token probe: 50 cases (31 CLI, 19 constructor), CPU setup replaced by a sentinel | rc 0, no unexpected outcome. See section 4 | `receipts/edge-tokens-head.{log,rc}` |
| Reviewer mutants on the round-2 delta (13 mutants plus a null control) | 13/13 killed. The null control passes with 52/18/9 | `receipts/mutants.{log,rc}`, `receipts/mut/` |
| Docs and style gates | rc 0: `check_doc_paths`, `check_doc_style`, `check_hygiene --check`, `check_py_idiom`, `check_soc_sources`, `check_solution_docs`, `docs_check`, `measure_fail_fast --check`, `measure_test_evidence --check`. Run with the pinned Markdown renderer interpreter, also rc 0: `gen_toc --check` (139 pages), `gen_toc --verify-anchors` (390 links), `check_em_dash --base e21c1ca0` (0 findings over 31 added lines) | `receipts/gates/*` (`md_*` are the renderer runs) |

The `receipts/gates/scripts_gen_toc*` and `scripts_check_em_dash*` files record rc 2 runs under an interpreter without the pinned Markdown renderer. They are environment refusals ("renderer is not installed"), not gate results. The `md_*` runs supersede them. `receipts/mutants-attempt1-invalid.*` is a discarded first mutant run: its copied trees lacked `.git`, so the null control failed and no result from that run is used.

## 4. Lens work

**Conformance.**
- Acceptance 1 holds at both entry points. VexiiRiscv `--with-fpu` and nonzero L2 are refused with named reasons. NaxRiscv explicit zero is refused. NaxRiscv FPU and positive L2 take effect, with a netlist change shown in `netlists-head.log`.
- R551-1-F1 holds. The token is never converted to float: `_parse_l2_bytes` returns `Decimal(token)`, and validation compares `Decimal` values. `1e-400` and `-1e-400` exit 2 with the whole-byte reason (`underflow-head.log`, `edge-tokens-head.log`). Omission, `0`, `0.0`, `-0`, `+0`, `0e-400`, `0E+999999`, ` 0 `, `0_0` and `000` reach setup.
- Acceptance 2: see Tests.
- Acceptance 3: the AX comparison above.
- Round-2 items 2 and 3 are satisfied (Docs; edge-token and mutant evidence).

**RTL.**
- No HDL, generator source, configuration or gitlink changed (`receipts/scope.txt`).
- The exported AX7101 gateware (`export/gateware/alinx_ax7101.v`), constraints, CSR map, headers and images are raw-byte identical base to head for both product configurations.
- NaxRiscv forwarding at `milan_soc.py:2697-2706` is unchanged and still produces both effects. There is no clock, reset, CDC, width or register-map surface in this delta.

**Robustness** (`edge-tokens-head.log`, 50 cases):
- Fractional, negative, NaN/sNaN, infinite, empty, hex and non-numeric CLI tokens exit 2 with the whole-byte reason.
- Whole nonzero tokens (`8192.0`, `8.192e3`, `1E+999999`, `1_000`, `4096.000`) exit 2 with the cacheless-L2 reason.
- At the constructor: `Decimal('sNaN')`, `Decimal('NaN')`, `Decimal('1e-400')`, `1e-300` and `-inf` are refused as non-whole. `-0`/`0.0` behave as zero. NaxRiscv `Decimal('-0')` and `0.0` are refused as the retained default.
- Unknown CPU spellings `vexii`, `VexiiRiscv`, `" naxriscv"` and `42` are refused before setup.
- The finiteness guard runs before any `Decimal` comparison, so a NaN never raises `InvalidOperation` instead of a refusal. Mutant M06, which removes that guard, turns a refusal into a crash and is killed.

**Tests.** Each round-2 regression fails for the defect it names:
- The bank's own float-parser controls are killed (`refusal-bank-head.log`).
- The R551-1 script fails at `d6b6ca89` and passes at head.
- Reviewer mutants, all killed:
  - M01/M02: parser returns float, or converts through float.
  - M03: validator converts through float.
  - M04/M05/M06: sign, integrality and finiteness checks removed.
  - M07/M08: weakened unknown-CPU guards (`is None`, case-folding).
  - M09: CLI raises instead of exiting 2.
  - M10: invalid token silently omitted.
  - M11: NaxRiscv zero refusal skips `Decimal`.
  - M12: bare `Decimal` parser type.
  - M13: over-refusal of negative zero.
- The null control passes.
- The counts are derived, not hard-coded: `_cli_cases` and `_refusal_controls` return counts.
- The lambda in the per-token control loop runs inside its own iteration, so it cannot bind late.
- The builder registration runs the bank (`test_builder.py:28727`, `:29036`).

**Docs.**
- `BUILDING.md:133` reads "the section 2.1 refusals" and the 2.1 heading is at `:165`.
- `:147-149` match the code: whole-byte rule, decimal-preserving CLI validation with both tokens named, and the unknown-CPU refusal.
- `:159-161` match `test_soc_options.py:249`, the build.sbt assertion and the cache side effect observed in `nax-isolated-copy-new-netlists.txt`.
- The `--l2-bytes` help (`milan_soc.py:3496`) is consistent.
- The REVIEW READY counts (52/18/9, 4+4) match executed results.
- The docs gates are rc 0.

## 5. Findings

```text
[R550] SUGGESTION Docs - docs/integration/BUILDING.md:154-155 - name the interpreter the option tests need
Requirement/evidence: both commands are spelled `python3 sw/builder/test_soc_options.py`. The probes import migen/LiteX. On a host where the default python3 lacks LiteX (this review host), the command fails loudly with a RuntimeError; no false pass is possible. The builder registration resolves the right interpreter by itself (test_builder.py _litex_python).
Impact: none on correctness or evidence. A reader running the documented command outside the LiteX environment gets an import failure.
Required change: optional. Say that the commands run under the LiteX interpreter the builder bank resolves (MILAN_LITEX_PYTHON or the sweep.sh venv).
Verification: doc reading.
```

No BLOCKER, MAJOR, MINOR or RESIDUE is recorded.

### Prior public review findings on this PR (read after the independent pass)

| Finding | Status at `853a7357` | Evidence |
|---|---|---|
| R551-1-F1 MINOR (Conformance, Robustness, Tests, Docs): fractional byte counts underflow to zero | **Resolved** | `underflow-head` rc 0 vs `underflow-base-d6b6ca89` rc 1; bank cases `test_soc_options.py:155-156`; controls `:201-204` killed; M01-M03 killed; `BUILDING.md:147-148`; AX 32/32 identical |
| R550-1 RESIDUE (Docs): `BUILDING.md:133` "refusals below" | **Resolved** | `BUILDING.md:133` reads "the section 2.1 refusals" |
| R550-1 SUGGESTION S1 (Docs, Tests): name `--nax-data-dir` | **Resolved** | `BUILDING.md:159-161` |
| R550-1 SUGGESTION S2 (Robustness): unknown constructor cpu bypasses the NaxRiscv zero refusal | **Resolved** | `milan_soc.py:2584`; `test_soc_options.py:140` (16 cases); control `:183` killed; M07/M08 killed; edge-token constructor rows |

PR #694 has no other review findings (PR comments 6046415109 through 6047221970, no PR reviews or inline comments).

## 6. Reviewer-owned completion ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #654 acceptance 1-3; rulings 6045774790 and 6046709819; `milan_soc.py:2573-2599`, `:2624`, `:3495`, `:3802-3810`; `underflow-head.log`; `netlists-head.log`; `ax/compare-fixed-*.txt` | R550-2 | 853a7357ba86d758a0e38f65db89a6187fb547bc |
| RTL | CLEAN | `receipts/scope.txt` (no HDL/config/gitlink change); `ax/*-fixed-*.json` (gateware `.v`, `.xdc`, `.tcl`, CSR, headers byte-identical); `milan_soc.py:2645-2710` forwarding; `netlists-head.log` | R550-2 | 853a7357ba86d758a0e38f65db89a6187fb547bc |
| Robustness | CLEAN | `milan_soc.py:2573-2599`; `edge-tokens-head.log` (50 CLI/constructor boundary cases); mutants M04-M06, M09-M10 | R550-2 | 853a7357ba86d758a0e38f65db89a6187fb547bc |
| Tests | CLEAN | `test_soc_options.py:119-205`, `:223-244`; `test_builder.py:28727`, `:29036`; `refusal-bank-head.log`; `builder-entry.log`; `mutants.log` and `mut/` (13/13 killed, null passes); `underflow-base-d6b6ca89.log` | R550-2 | 853a7357ba86d758a0e38f65db89a6187fb547bc |
| Docs | CLEAN | `BUILDING.md:129-163`; `milan_soc.py:3480-3497` help; REVIEW READY 6047197977 counts; `receipts/gates/*` | R550-2 | 853a7357ba86d758a0e38f65db89a6187fb547bc |

```text
[R550] PASS Conformance - sw/litex/milan_soc.py:2573-2599,3495,3803 and receipts/underflow-head.log - acceptance 1-3 and round-2 item 1 checked against issue #654, 6045774790 and 6046709819
[R550] PASS RTL - receipts/scope.txt and receipts/ax/compare-fixed-ax7101_{1x1_tdm8,8x8}.txt - no RTL/config/gitlink change; both product exports 32/32 raw-identical e21c1ca0 vs head
[R550] PASS Robustness - receipts/edge-tokens-head.log - 50 boundary CLI/constructor cases against the whole-byte, cacheless-L2, NaxRiscv-zero and unknown-CPU rules
[R550] PASS Tests - sw/builder/test_soc_options.py:140-205 and receipts/mutants.log - every new regression and control fails for its named defect; 13/13 reviewer mutants killed
[R550] PASS Docs - docs/integration/BUILDING.md:133,147-161 and receipts/gates/ - text matches code and test behavior; gates rc 0
```

## 7. Real limits

- The AX7101 comparison is a gateware/firmware **export** (no `--build`). No synthesis, implementation, timing or bitstream was run. It runs at one tree path with timestamps and Instance repr fixed before generation. The population digests include this tree's absolute path, so they reproduce only at this path. The claim is base vs head at one path.
- The VexiiRiscv netlist for both product configurations came from the cache in an isolated data copy; no new Vexii netlist was generated (`vex-isolated-copy-new-netlists.txt`). The CPU generator is unchanged by this PR.
- `--netlists` generated 5 NaxRiscv netlists into an isolated copy; the rest were cache hits from the installed package copy.
- The full builder bank was not run here, nor the parent/PP/gPTP/Yosys banks, LiteX simulations or lint. I ran only the builder's `test_soc_option_refusals` entry. Those banks are the manager's source evidence.
- No candidate merge against live dev `d8b355fe0f41d49dca6cae1cd8b3826e2edde364` was built or validated.
- Hosted checks were pending at snapshot time (`receipts/hosted-checks-snapshot.txt`): Verilator and Yosys shards, docs-check, elaborate and yosys-elaboration. "Physical gPTP" is a skipped context, not an executed job. No hosted result is claimed.
- Physical calibration was NOT RUN. No hardware was touched. Field skips are not hardware proof.
- The shared CPU data install was untouched: its listing digest is identical before and after (`shared-install-{before,after}.txt`). The review clone is byte-identical to the head: worktree and index equal HEAD, no untracked files, gitlinks unchanged (`clone-integrity.txt`).

## 8. Pending manager duties

- Hosted/act acceptance at exact head `853a7357` (`rtl-fast`, `verilator-suites`, `yosys-portability`).
- Candidate-merge validation against live dev `d8b355fe`.
- Obtain the second independent positive (external R551-2) and confirm no review round is still in flight.
- Post-merge containment.
- Optional: carry the SUGGESTION above if wanted.

## 9. Reproduction

Scripts in `scripts/`:
- `run_ax_compare.sh`, `export_ax.py` and `compare_manifests.py` are the public R550-1 harness, unchanged.
- `byte_count_underflow.py` is the public R551-1 script, unchanged.
- `mutants.py`, `edge_tokens.py` and `bg.sh` are new in this round.

```sh
PY=<LiteX interpreter>; T=<clean tree at 853a7357>
$PY -B $T/sw/builder/test_soc_options.py
$PY -B scripts/byte_count_underflow.py $T            # expect rc 0 (rc 1 at d6b6ca89)
$PY -B $T/sw/builder/test_soc_options.py --netlists --nax-data-dir <isolated nax data copy>
bash scripts/run_ax_compare.sh $PY <scratch clone> <isolated vex data copy> <work> fixed \
  e21c1ca024d37ea188ad15b5c8f9c2dae18628df 853a7357ba86d758a0e38f65db89a6187fb547bc
$PY -B scripts/mutants.py <scratch copy of T> <work> $PY 9
$PY -B scripts/edge_tokens.py $T
```

R550-2 FINISHED
