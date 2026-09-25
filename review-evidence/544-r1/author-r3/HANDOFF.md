# [A296] Round 3 handoff

Status: implementation and all requested local validation complete at the current local head. Ready for independent review.

Issue comment: https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5825392556

Issue: #544. Pull request: #558. Branch: 544-macro-sample.
Starting head: `77e9ca5ea9e04a7618c577ab511baec63b39dc05`.
Current local head: `8383e929fab3ff57a768c88b8b1ff9b568afcf14`.
Commit subject: `fix(builder): allowlist assembly across the preprocessed boot unit`.

## Assignment and implementation

Public authorities: assignment 5825016512; review reports 5825011598 and 5824963907; decisions 5823832945 and 5824093785. Public evidence was fetched read-only from archives `3fec62a96c28986759aaadf6cae1e9799f0482bf` and `3dc90f5c2dc63d7038756ef8a09642bda0a12c58`.

Only `sw/builder/test_builder.py` and `docs/integration/BAREMETAL_FIRMWARE.md` changed.

- The `boot-unit asm allowlist rule` reads every asm keyword in the expanded boot unit, including headers and uncalled helpers. Eleven frozen forms normalize whitespace between tokens only. Literal bytes, operands, qualifiers, keyword spellings and trailing attributes remain exact. Unknown and incomplete forms receive a named refusal.
- Production preprocessing with the pinned SDK and headers yielded five forms: two firmware fences, header `fence.i` and `nop`, and the `__bsd_qsort_r` assembly-name annotation. The census's SDK headers add six exact scanf-family assembly-name declarations, including trailing attributes. Both measured units pass. See `production-preprocess.json`, `census-production-asm.json` and `census-production-provenance.json`.
- The fifth-fence fixture repeats the production `fence rw, rw` form. It requires no extra entry.
- The round-2 storage, no-escape, interval-absence and interval-asm checks remain active. The new check runs after every established resolver check, preserving previous reason pins. Overlapping asm controls first observe the new named refusal, then disconnect it to prove the remaining contract still accepts the old control.
- W01-W03 are new mutation rows, refused on the allowlist sentence and accepted with only that check disconnected.
- Compiler-free identity coverage is an open class: on macro-free source only the source-text write-form rule checks identity; every unmatched spelling is NOT RUN. The original examples, C09/C11, plain wrappers and asm outputs, and W01-W03 are pinned accepted without compilation and refused with it.
- The page, cost table and COST line state the out-of-unit bound: separately linked pinned library objects (`libc`, `libcompiler_rt`, `libbase`, `libfatfs`, `liblitespi`, `liblitedram`, `libliteeth`, `liblitesdcard`, `liblitesata`), BIOS and startup objects are not read. Their calling-convention compliance and register/memory effects remain trusted, unproved.

## Validation

The compiled full-builder run exits 0, with identical source hashes before and after. Its gate 1b totals are 351/351 mutations refused, 38/38 firmware cases accepted, 4/4 Makefile cases accepted and 46/46 RTL variants elaborated. Its only NOT RUN arm is the pre-existing resource-calibration report.

The compiler-free full-builder run also exits 0, with unchanged source hashes. Gate 1b preserves 249/249 mutations, 35/35 firmware cases, 4/4 Makefile cases and 46/46 RTL variants. Two arms are explicitly NOT RUN: compiler-dependent gate 1b instruments and the existing resource-calibration report. The pinned SDK run took 639 seconds; elapsed times and exact source hashes for both runs are recorded in the corresponding run JSON files.

`full-builder.py` reproduces the assigned compiler argv mapping: only the existing absolute selector's argv[0] changes to the verified pinned SDK executable. The SDK run executes `sw/builder/test_builder.py --require-rv32`; the absent run executes the same file with all cross candidates hidden. Reproduce from the candidate root with `python3 OUTPUT/full-builder.py sdk` and `python3 OUTPUT/full-builder.py absent`. Full logs, argv audits and before/after source hashes are retained.

All static commands exit 0 at the current head (`static-gates.json`):

- `python3 -B scripts/docs_check.py`, with Git metadata.
- `python3 -B scripts/docs_check.py`, in a disposable tracked-file export without Git metadata, matching the second CI mode.
- `python3 scripts/check_baremetal_only.py --check`.
- `python3 scripts/check_em_dash.py --base ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
- `python3 scripts/check_doc_style.py`.
- `python3 scripts/gen_toc.py --check`.
- `python3 scripts/check_doc_paths.py`.
- `python3 scripts/check_py_idiom.py`.
- `git diff --check` and `git diff --check ffcbd33de70278ae34b533dcbadde0b36c8cba13 HEAD`.

The renderer-dependent commands used a disposable environment installed from the hashed repository requirements. It has been deleted.

## Public probes and preservation

Both round-2 drivers and every round-2 case module ran unchanged at the final head: 25 configurations, 483 verdicts. Source fingerprints are in `public-probe-sha256.json`; `probe-summary.json` verifies final-head provenance. Every verdict and refusal reason is retained in `probes/`; the six `*MATRIX.md` files tabulate them.

R316: all 35 cases in five configurations, including separate disconnections of the prior sample check, new unit allowlist, and compiler-free macro check. R317: all 77 cases across its five case sets, each with compiler/absent and connected/disconnected configurations.

`round2-verdict-delta.json` records the connected-mode differences: W01-W03, callee asm, and asm output after the guard now refuse on the allowlist. Every compiler-free verdict remains unchanged. A01-A10 match the declared class. Earlier optional delimiter and labeling suggestions remain unchanged.

`corpus-preservation.json` proves the accepted firmware and Makefile blocks are byte-identical to the starting head. `preserved-production.json` proves unchanged production firmware and CSR source. Existing mutation rows remain, and compiled totals grow by three.

## Cleanup and remaining work

Downloaded public evidence, documentation export and temporary environment have been deleted (`scratch-cleanup.json`). No toolchain, SDK copy, virtual environment or tree export is in this output directory. Preliminary failed runs are isolated under `preliminary/`: the omitted exact SDK header declarations and refusal ordering were corrected before final validation.

`PR-BODY.md` is the complete updated current public body, beginning `[A296]` and retaining `Closes #544`. It has not been applied to the PR.

No push, PR edit, merge, other checkout, sub-agent or hardware action was performed. All requested commands and probe configurations are complete. Published `[A296] REVIEW READY` on #544 with this local head as the final action. Pushing the local commit, applying the prepared PR body, hosted/local-replica acceptance, and independent re-review remain with the management and review roles.
