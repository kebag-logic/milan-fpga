[R261] POSITIVE - exact head 0ca178678490024707b3a2393a86dc9e7b2a0ca4

Independent external review R261-1 of Mister-M-alt/protocol-processor-control-plane-avb-milan issue #104 / PR #105.

- Exact head `0ca178678490024707b3a2393a86dc9e7b2a0ca4`, tree `897a49d0e7eb25e910ff63984c5000403375dca2`, one commit on PP `main` `e1d0176d3a486bce4a80765cfbcefcb61964f8e9` (still the live `main` tip when this review was written).
- Parent live `dev` `ede8d48ecd7c7f589a14b957951f040d92c99c70`.
- Cleared context, reconstructed from public state only. No private author material, lane scratch or other reviewer report was read.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses were applied and are covered clean. One SUGGESTION (S1) is recorded. It is optional and does not affect lens coverage.

The change is behaviour-neutral. With only the two new return annotations and the two new docstrings removed, both files' ASTs equal base. The docstrings state contracts the code really implements, and the annotations are correct. The parent's Rule 12 gate goes from exit 1 (the issue's two failures) to exit 0 with this head staged. This repository's gates are green locally and on the hosted runners at the exact head.

## Reconstruction order and authorities

1. The PP repository has no `AGENTS.md` or `CONTRIBUTING.md`. The governing process documents are the parent's (`kebag-logic/milan-fpga@ede8d48e`): `AGENTS.md` §6-7 (lenses, severities, ledger) and `CONTRIBUTING.md`. PP's own `README.md`, `docs/README.md` and `hdl/README.md` (consumption contract: the pin moves only to a commit whose `make check` and full `tb/` sweep are green here) were also read.
2. Issue #104 body, frozen acceptance:
   - (a) both functions are annotated and documented;
   - (b) the parent's `check_py_idiom.py` exits 0 with this repository staged at the fix head;
   - (c) this repository's own gates stay green.
   Also read: the manager assignment comment and the author's REVIEW READY comment.
3. Interface authority: parent `docs/development/CODE_QUALITY.md` Rule 12 (lines 2567-2680) and `scripts/check_py_idiom.py` at `ede8d48e`. The fetched blob id `5d84953a` equals the parent tree's blob. The gate treats a function as public when its name has no leading underscore. It needs every parameter except `self`/`cls` annotated, plus a return annotation, and it needs `ast.get_docstring` to be non-empty.
4. `git diff e1d0176..0ca1786` and history (receipt `pr-diff.patch`, receipt 09).
5. Public evidence:
   - the author packet and the manager parent-consumer receipts at `kebag-logic/milan-fpga@a906e65c/review-evidence/pp104-r1`, a superset of the `667e9203` tree that holds only the author packet;
   - the manager comments on the issue and the PR.
   Every downloaded file's sha256 equals its MANIFEST `published_sha256` (receipt 14).

## Acceptance criteria

| Criterion | Result | Evidence |
|---|---|---|
| (a) both functions annotated and documented | MET | `tb/pp_top/fixture_guards.py:13` `def main() -> int:` + docstring 14-23. `tb/pp_top/test_fixture_guards.py:15` `def test_compiler_environment_and_arguments(self) -> None:` + docstring 16-22. The parent scanner, applied to every tracked `*.py` here, counts 2 unannotated + 2 undocumented at base (exactly these two sites) and 0 at head. Every other counter is unchanged (receipt 03). |
| (b) parent `check_py_idiom.py` exits 0 with this head staged | MET, reproduced independently | Disposable shallow parent clone at live `dev` `ede8d48e`, `gptp-processor` at its pin `c1b61743`, `git submodule status` clean ` ` for both. PP staged at `e1d0176`: exit 1, `unannotated public function 2 > ratchet 0`, `undocumented public function 2 > ratchet 0`, and `--list` attributes 1+1 to each file. PP staged at `0ca1786`: exit 0, `220 first-party modules, 160384 lines`, both ratchets `0 <= 0`. `--selftest` 54/54. `check_cpp_idiom.py` exit 0 (receipt 08). This is identical to the manager's `02.log` (receipt 14). |
| (c) this repository's gates stay green | MET | Local, at the head (receipt 07): `check-links` 807 OK, `check-matrix` OK, `gen_matrix --check` 86 rows / 0 untested, `make stale` 0, `check_upc_map` PASS, `lint_hdl.sh` 37/37, `make lint` 41 mermaid + 18 wavedrom OK. `tb/pp_top` full `make`: unit test OK, 4 fixture guards PASS, `1411 checks: 1411 PASS, 0 FAIL` (receipt 12). Hosted at the exact head, push and pull_request runs (receipt 13): `docs-gates` (links, matrix, `wavedrom: 18 blocks checked, OK`, stale), `suites` (lint, `PASS pp_top (1411 ...)`, `suites: 14943 checks total, 0 failing`, matrix, nvm_port figures), `portability`: all executed and all succeeded. The only skipped hosted step is the cached Verilator build. |

## Findings

### S1 - SUGGESTION - Docs, Robustness

`tb/pp_top/fixture_guards.py:16-22`: the `main()` docstring could name the non-zero-exit condition and two unstated preconditions.

- **Authority/evidence.** Issue #104 asks for docstrings stating the contract. Rule 12's checklist asks "Does this public function say what it takes and what it returns?". Receipt 04 shows:
  - A VERILATOR_ROOT query or a model generation that *exits non-zero* raises `CalledProcessError`, as documented.
  - An absent or unlaunchable `verilator` raises `FileNotFoundError`.
  - An absent compiler raises `FileNotFoundError` rather than returning 1.
  - `sim_main.cpp` (line 54) is resolved against the working directory, so `main()` must run from `tb/pp_top`. The Makefile does this; the docstring does not say it.
  - `--cxx` is split shell-style (line 44), which the docstring also leaves unstated. The unit test does pin it.
- **Impact.** None on behaviour or on any caller. The Makefile turns any exception into a failing exit. A reader could take `CalledProcessError` as the only exception those two steps can raise.
- **Suggested outcome (optional).** For example: "exits non-zero ... raises CalledProcessError; an executable that cannot be started raises OSError; run from tb/pp_top".
- **Verification.** Re-run `scripts/probe_main_contract.py`. `probe_ast_equality.py` must still PASS. The parent `check_py_idiom.py` must stay exit 0.

No BLOCKER, MAJOR or MINOR finding.

## Clean-lens results

```text
[R261] PASS Conformance — issue #104 acceptance; parent scripts/check_py_idiom.py@ede8d48e (blob 5d84953a) with PP staged — both functions carry complete Rule 12 signatures (self exempt) and docstrings; parent gate exit 1 at base staging with exactly the issue's two failures, exit 0 at head staging, --selftest 54/54, cpp idiom exit 0 (receipts 03, 08, 14); repo gates green locally and hosted at the exact head (receipts 07, 12, 13). No IEEE 1722.1/Milan behaviour is touched; the Milan §4.2.7.2.1 VID fixture guards pass unchanged.
[R261] PASS RTL — git diff --raw e1d0176..0ca1786 (receipt 09) — only tb/pp_top/fixture_guards.py and tb/pp_top/test_fixture_guards.py change, modes 100644 unchanged; no HDL, sim_main.cpp, wrap or Makefile change; lint_hdl.sh 37/37 on Verilator 5.050; the fixture guards compile the real sim_main.cpp against a generated model with identical results at base and head (receipt 10); tb/pp_top 1391 + 20 = 1411 PASS (receipt 12); hosted suites 14943/0 and portability at the exact head (receipt 13). No module or interface contract is affected.
[R261] PASS Robustness — tb/pp_top/fixture_guards.py:13-71 — AST equals base after stripping only the new annotation/docstring (receipt 01), so no path changed; every failure path probed: exit-status, static-assertion and error-count mismatches each return 1 after printing the compiler output, the first mismatch stops the run, warnings alone do not fail, non-zero root query / model generation raise CalledProcessError, missing executables raise FileNotFoundError, a bad option or flags without `--` raise SystemExit (receipt 04). S1 is a SUGGESTION only.
[R261] PASS Tests — tb/pp_top/test_fixture_guards.py:15-67 — test body AST-identical to base; each property the new docstring states is enforced: 11 single-point mutants of fixture_guards.py (LC_ALL override removed / only-if-unset / leaked to model generation / leaked to the root query, caller env mutated / dropped, --cxx not split, `--` kept, three cases, exit 1, define spelling) all killed, control passes (receipt 05); with the real compiler under a French gettext caller, head PASS and the override-removed mutant FAIL (receipt 06); unittest -v output differs from base only by the docstring's first line (receipt 10).
[R261] PASS Docs — tb/pp_top/fixture_guards.py:14-23, tb/pp_top/test_fixture_guards.py:16-22, tb/pp_top/README.md:531-544 — every clause of both docstrings checked against code and probes (receipts 04, 05); consistent with the README's fixture-guard and locale text, which needs no change because behaviour is unchanged; module docstring (argparse description) unchanged; commit subject one line, no body or trailers; PR body and public handoff claims reproduced (receipts 01, 05, 08, 10, 14). S1 is a SUGGESTION only.
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue #104 acceptance (a)-(c); parent Rule 12 text + `check_py_idiom.py`@`ede8d48e`; parent gate with PP staged at base and head; receipts 03, 07, 08, 12, 13, 14 | R261-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| RTL | CLEAN | `git diff --raw e1d0176..0ca1786` (no HDL); `lint_hdl.sh`; real-bench fixture guards; `tb/pp_top` two builds; hosted suites/portability; receipts 07, 09, 10, 12, 13 | R261-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| Robustness | CLEAN (S1 SUGGESTION) | `tb/pp_top/fixture_guards.py:13-71` failure paths; AST equality; receipts 01, 04 | R261-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| Tests | CLEAN | `tb/pp_top/test_fixture_guards.py:15-67`; 11 mutants + control; real-compiler locale probe; receipts 05, 06, 10 | R261-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |
| Docs | CLEAN (S1 SUGGESTION) | both docstrings vs code; `tb/pp_top/README.md:531-544`; commit message; PR body; public author handoff; receipts 01, 04, 05, 09, 14 | R261-1 | `0ca178678490024707b3a2393a86dc9e7b2a0ca4` |

## Prior public review findings

This review's own verdict and ledger were written first. After that, PR #105 and issue #104 were read. At that time they held no published review verdict or finding: 0 PR reviews, 0 review comments, and only manager status comments ("parent consumer gates pass", "review started" for R260-1 and R261-1) plus the author's REVIEW READY. The evidence tree `a906e65c` holds no reviewer report. There is nothing to resolve or retain at this head.

## Receipts

Every file below is listed in `MANIFEST.sha256`. Paths are relative to this packet. Private paths in `receipts/12` were redacted to `$PACKET`, `$PINNED_TOOL_BIN` and `$VERILATOR_OVERLAY`; the unredacted original sha256 is `8fcb5d31b63396dcb2d1ce7712cca4c790cf984ce7d4f001b68590e3b57e70bc`.

| Receipt | Content |
|---|---|
| `receipts/pr-diff.patch` | raw `git diff e1d0176..0ca1786` |
| `receipts/00-tool-identity.txt` | Verilator 5.050 wrapper and binary sha256, Python 3.14.7, GCC 16.2.1, git |
| `receipts/01-ast-equality.txt` | `scripts/probe_ast_equality.py`: only the two target functions differ, and stripped head AST == base for both files |
| `receipts/02-parent-gate-source.sha256` | sha256 and GitHub blob id of the fetched parent gate sources |
| `receipts/03-rule12-scan.txt` | `scripts/probe_rule12_scan.py`: parent `scan()` over this repository at base and head |
| `receipts/04-main-contract.txt` | `scripts/probe_main_contract.py`: each `main()` docstring clause against behaviour |
| `receipts/05-test-mutations.txt` | `scripts/probe_test_mutations.sh`: control + 11 mutants |
| `receipts/06-locale-real.txt` | `scripts/probe_locale_real.sh`: real compiler under a French gettext caller |
| `receipts/07-repo-gates.txt` | this repository's gates at the head, in a scratch clone |
| `receipts/08-parent-rule12-gate.txt` | `scripts/probe_parent_gate.sh`: parent gates with PP staged at base, then head |
| `receipts/09-hygiene.txt` | `diff --check`, modes/blobs, commit object, `-W error` compile, line length, runtime annotations, guard-output diff |
| `receipts/10-fixture-guards-{base,head}.{stdout,stderr}` | `make fixture-guards` at base and head |
| `receipts/12-pp_top-make-head.log` | full `make -C tb/pp_top` at the head (redacted) |
| `receipts/13-hosted-exact-head.txt` | hosted check runs and job steps at the exact head, key log lines, live refs |
| `receipts/14-manager-evidence-check.txt` | public evidence hashes vs MANIFEST, key manager log lines |
| `receipts/99-clone-restored.txt` | `scripts/verify_clone_restored.sh`: review clone byte-identical to the head |

## Limits

- **Local toolchain differs from the hosted one.** Local runs used the scoped Verilator 5.050 (identity in receipt 00), GCC 16.2.1 and Python 3.14.7. The hosted runners use their Ubuntu toolchain with a source-built Verilator 5.050.
- **Build parallelism was capped.** Local `tb/pp_top` runs replaced the Makefile's `-j 0` with `-j 8` to respect the job cap. Only parallelism differs.
- **Not re-run locally:**
  - `render-wavedrom.py --check`, because it would bootstrap a networked virtualenv. The hosted `docs-gates` ran it at the exact head: `wavedrom: 18 blocks checked, OK`.
  - `run_suites.sh` and the nvm_port figures step (full-bank exclusion). The hosted `suites` ran both at the exact head.
- **Parent gates.** This review re-ran only `check_py_idiom.py` (plus `--list` and `--selftest`) and `check_cpp_idiom.py`, in a disposable shallow parent clone. The manager's xvlog, RTL source-list, `pp_srcs`, builder and `pp_shadow` results were hash-verified, not re-run. The builder log records `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11, the calibration report, is absent from disk.
- **Annotations were not type-checked.** No static type checker was available. The annotations were checked by AST and by the return paths: every return is an `int` literal 0 or 1, and the test method returns nothing.
- **No hardware.** Physical calibration was NOT RUN, no hardware was used, and field skips are not hardware proof.
- **Merge candidate not validated.** This review validates the source head only, not the current-dev merge candidate.

## Pending manager duties

- At the merge turn, build and validate the current-dev candidate (source base `e1d0176`, live `dev` `ede8d48e` or its successor), including the parent consumer gates with the candidate's gitlink.
- Own hosted/act acceptance for the exact head and the candidate.
- Obtain the second independent positive review (R260-1), reconcile the ledgers, and obtain explicit maintainer merge authorization.
- Handle post-merge containment and close issue #104. Adopting the parent pin (#400/#403) is separate parent-side work.
- Publish this packet (`REPORT.md` plus the files in `MANIFEST.sha256`).

R261-1 FINISHED
