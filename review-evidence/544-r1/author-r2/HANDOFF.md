[A289]

Status: Round 2 author work complete locally; independent delta review pending.
Branch: `544-macro-sample`.
HEAD: `77e9ca5ea9e04a7618c577ab511baec63b39dc05`.
Parent: `b068763c849a18096b0f46cf9b18e0f904e4d708`.
Validation base: `ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
The worktree is clean. The commit subject is one line, with no body or trailers.
No push or PR edit was made.

Authority

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5823832945
- Exception decision: https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5824093785
- Internal findings: https://github.com/kebag-logic/milan-fpga/pull/558#issuecomment-5823826242
- External findings: https://github.com/kebag-logic/milan-fpga/pull/558#issuecomment-5823671607

Change

Only the builder test and the authoritative bare-metal page changed.
The production sample is an automatic block-scope uint32_t, with no explicit
storage specifier. Its address is refused throughout the expanded unit by a
register diagnostic copy. Nested functions are refused to exclude implicit
capture, including old-style definitions and extension-suppressed warnings.
The existing preprocessed-unit check already refuses surviving directives,
including synthesized diagnostic pragmas. The original unit supplies the census.

In the read-to-guard interval, every asm spelling is refused. The sample may
occur only as the complete delimited `(unsigned long) id` call argument or
complete `(void)(id & <integer-literal>);` statement authorized by the decision.
All listed wrapper/asm bypasses have named mutation refusals and disconnected
controls. All 10 requested near-miss rows receive the named refusal. Seven
are valid C and pass disconnected; three cast-lvalue/macro near misses are
invalid C, so acceptance by the remaining compiler contract is not claimed.

Six after-guard address forms and three inline nested-capture forms are
refused and pass with only the identity check disconnected. The plain generic
lvalue uses the equivalent int association for controlling expression 0;
the older source rule independently bans the keyword default. The public
macro/default spelling is also present and refused on the new rule.

Storage is checked directly at the expanded-unit boundary: three automatic
spellings pass and three nonautomatic spellings receive named refusals. The
older source-statement rule independently rejects storage prefixes earlier.

The compiler-free rule is unchanged. C03, C05, C13, writer alias, writer apply,
C16 and C17 are accepted without a compiler and refused with one. All seven
identity protections are explicitly NOT RUN in that mode, in the prose,
cost table and COST line. The corrected __CONCAT disclosure is restored.

Results

| Full builder mode | rc | Mutations refused | Legitimate firmware | Makefile cases | RTL variants |
|---|---|---|---|---|---|
| Pinned SDK, required target | 0 | 348/348 | 38/38 | 4/4 | 46/46 |
| No firmware compiler | 0 | 249/249 | 35/35 | 4/4 | 46/46 |

The compiled audit records 819 target invocations. The compiler-free audit
records zero firmware compiler invocations. The existing resource-calibration
arm is NOT RUN in both modes. The compiled census and dependent instruments
are additionally NOT RUN without the compiler; those skips are disclosed.
The seven named accepted forgeries do not count as identity protection.

The accepted corpus, fifth fence and production firmware are unchanged.
`corpus-conservation.json` checks the original accepted-case and mutation
construction syntax; the compiler identity reason is intentionally renamed.

Both unchanged reviewer probe sets ran at this commit, in both modes, with
and without their respective check. All eight harness commands returned 0.
Their 55 cases give 220 verdicts in `probe-matrix.md` and the original JSONs.
Harness success is execution evidence, not a reviewer verdict.

| Probe set | Compiled A/R | Compiled disconnected A/R | No compiler A/R | No compiler disconnected A/R |
|---|---|---|---|---|
| Internal, 25 cases | 3/22 | 23/2 | 10/15 | 23/2 |
| External, 30 cases | 4/26 | 22/8 | 9/21 | 23/7 |

Every listed compiler bypass receives the absence-rule refusal and passes
disconnected. Compiler-free probe verdicts match the previous packet exactly.
The internal bare-read case and external reversed-mask and parenthesized
macro-mask cases are outside the two authorized shapes. Their new compiled
refusals are documented conservative costs, not preserved ACCEPTED verdicts.
The verifier #else deletion remains accepted in both modes, unchanged.

Required commands, all rc 0

The full builder entry point was executed through `run-builder.py`, using
the verified pinned selector mapping in compiled mode and hiding cross
candidates in compiler-free mode. The wrappers and argv audits are retained.

- `python3 sw/builder/test_builder.py --require-rv32` via the SDK wrapper.
- `python3 sw/builder/test_builder.py` via the compiler-free wrapper.
- `python3 -B scripts/docs_check.py`, normal inventory and no-git inventory.
  The second process received GIT_DIR pointing to a nonexistent directory;
  its receipt confirms filesystem-walk inventory. No checkout was exported.
- `python3 scripts/check_baremetal_only.py --check`.
- `python3 scripts/check_em_dash.py --base ffcbd33de70278ae34b533dcbadde0b36c8cba13`.
- `python3 scripts/check_doc_style.py`.
- `python3 scripts/gen_toc.py --check`.
- `python3 scripts/check_doc_paths.py`.
- `python3 scripts/check_py_idiom.py`.
- `git diff --check`, plus the committed validation-base-to-HEAD range.

The full-bank hashes equal the committed files. Every static command was
also rerun at the committed head. Receipts: `final-full-*-result.json`,
`final-static-results.json`, `committed-gates.json`, `final-source-hashes.json`.

Packet and cleanup

`PR-BODY.md` preserves the full fetched current PR body, updated to this
round and head, with [A289], a Round 2 section and Closes #544. It has no
absolute home paths, tool/model attribution or footer. It was not published.
`candidate.patch` is the round-2 delta against the parent named above.
`candidate-inputs.json`, `probe-head.json` and `final-state.json` bind the packet.

The 98 public evidence files rehashed unchanged after the final probes.
Internal archive: e3440047cf823c9260f2fce67906b3edddb786f9.
External archive: c37f8e0a09baf2a5e90c9c7123700ec3ae6010a1.
The disposable bare object store and extracted packets were deleted.
The temporary locked documentation dependencies were deleted too.
No toolchain, SDK copy, virtual environment or tree export is in this packet.
To reuse `run-probes.py`, freshly extract the public packets read-only and
recreate `scratch-path.txt`; the removed scratch is not a dependency.

Earlier strict, continued, failed and cancelled receipts are development
history, not evidence for the final head. The generic-address control typo
was fixed before both final banks passed; all 48 focused bypass/escape
outcomes then matched expectations. No old test was weakened.
No private transcript or other management output directory was read.
All commands ran in the foreground. No sub-agent, other checkout, merge or
hardware operation occurred. Independent review, publication and subsequent
integration remain manager-owned steps.

Public handoff

REVIEW READY was posted on issue #544: https://github.com/kebag-logic/milan-fpga/issues/544#issuecomment-5824702131
The exact message is `REVIEW-READY.md`; its successful publication receipt
is `review-ready-receipt.json`. Author work stops here.
