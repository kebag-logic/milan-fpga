[R389] POSITIVE - exact head 11e4e1f2876c99e8f136d869c70674e077ddcf94

# R389-2: external independent re-review of PR #614 for issue #595

- Role: external independent reviewer [R389], round R389-2, cleared context.
- Exact head: `11e4e1f2876c99e8f136d869c70674e077ddcf94`. Tree: `b78b64a0b7fd34797c7e06ece302675f7045cf49`. Hosted PR head (`headRefOid`) equals it; the PR is open, not draft, and targets `dev`.
- Source base: `1fa2357fcb9b83ad7d6cbeab0c7cc0eb957cdd3a`. Round-1 head: `44d3ae3b15a0d058abb837c655ad24bd9b64c6e8`.
- Delta under review: `44d3ae3b..11e4e1f2`, one commit, 3 files, +11/-5, all mode 100644:
  - `sw/builder/test_declarations.py` (+9/-3);
  - `sw/builder/README-parameters.md` (1 line);
  - `docs/ENDSTATION_BUILDER.md` (1 line).
- Unchanged by the delta: `sw/builder/endstation_builder.py`, `sw/builder/test_builder.py`, `scripts/pp_srcs.py` (so `PROSE_OK` too), `configs/`, every HDL file and every gitlink.
- Scope reconstructed from:
  - AGENTS.md and CONTRIBUTING.md;
  - the issue #595 body (acceptance 1-5 and "Not in scope", unchanged since round 1);
  - the round-2 assignment (issue comment 5868165203) and the executor's round-2 REVIEW READY (5868526411);
  - `scripts/pp_srcs.py`, `.github/workflows/rtl-fast.yml:68-109`;
  - the delta, and my own round-1 packet (read-only input).

## Verdict summary

My round-1 finding F1 is resolved at this head.

- The declaration suite no longer names `protocol-processor/hdl/adp/pp_adp_pkg.sv`. It finds the package through `pp_srcs.pp_sources()`, the repository's derived processor source list.
- No `PROSE_OK` entry was added. `scripts/pp_srcs.py` is byte-unchanged in the delta.
- `pp_srcs.py --check --selftest` and `test_declarations.py` both return 0.
- The removed-derivation control, which restores the round-1 literal, makes `pp_srcs.py --check` fail with rc=1 and name the literal.
- The suite's independent read of `ADP_ENTITY_CAPS_C` is kept, and it still decides the pinned value.
- The hosted `rtl-fast / verilator-lint` job succeeded at this exact head, including step 7, the `pp_srcs` step that failed at round 1.
- The two summary lines now say "YAML string".
- The refusal behaviour and the five configurations' artifacts are unchanged. This is re-derived below, not inferred from the diff.

I have no open finding at this head.

## Round-1 finding F1: resolved

F1 was MAJOR, under `Tests` and `RTL`, at `sw/builder/test_declarations.py:231` at `44d3ae3b`. The round-1 text is in my round-1 report.

### (1a) The derivation

At head, `test_declarations.py:15-16` puts `scripts/` on `sys.path` and imports `pp_sources`. `test_declarations.py:233-240` then:
- reads every path `pp_sources()` returns;
- keeps the texts that declare `^\s*package\s+pp_adp_pkg\s*;`;
- asserts that exactly one does (`:237`);
- applies the unchanged `ADP_ENTITY_CAPS_C\s*=\s*32'h(...)` regex to that text;
- asserts one match (`:239`).

`pp_sources()` (`scripts/pp_srcs.py:54-79`) lists tracked `.sv` files only, through `git ls-files` in the submodule. It refuses an absent submodule rather than returning an empty list.

The literal `protocol-processor/hdl/adp/pp_adp_pkg.sv` occurs 0 times in the file at head. The file's hits against `LITERAL_RE` are exactly its three pre-existing `PROSE_OK` literals.

### (1b) Gates at head

Both gates were run in the reviewed clone, with bytecode writes suppressed (`receipts/gates_head_reviewed_clone.log`).

| Command | Result |
|---|---|
| `python3 scripts/pp_srcs.py --check --selftest` | rc=0: "45 tracked source(s) derived; no build input carries a literal copy (self-test passed)" |
| `python3 sw/builder/test_declarations.py` | rc=0. All sections print, including `[595 MAC]`, `[595 uint]` and `[595 formats]`. |

The same command at three revisions, each in a fresh disposable clone with identical gitlinks (`receipts/pp_srcs_revs.txt`):

| Revision | `pp_srcs.py --check --selftest` |
|---|---|
| base `1fa2357f` | rc=0 |
| round-1 head `44d3ae3b` | rc=1 |
| head `11e4e1f2` | rc=0 |

Gate 40 through the builder bank's import path also passes. I imported `test_builder` (which puts `sw/builder`, `avdecc`, `scripts` and `sw/litex` on the path) and then ran `test_declaration_contracts()`: rc=0 (`receipts/gate40_via_test_builder_import.log`). The bank itself was not run. No module under `scripts/` shares a name with a module in `sw/builder`, `sw/litex`, `avdecc` or the descriptor generator directory, so the new `sys.path` entry shadows nothing.

### (1c) Controls

Script: `scripts/controls.py`. Receipt: `receipts/controls.tsv`. Each control ran on its own fresh copy of the head clone. Each edit was anchored to match exactly once, and each copy was removed afterwards.

| Control | Change | `pp_srcs --check` | `test_declarations` | Reading |
|---|---|---|---|---|
| C1 removed derivation (required) | Restore the exact round-1 literal read | **rc=1**: `sw/builder/test_declarations.py: names submodule source(s) literally ... protocol-processor/hdl/adp/pp_adp_pkg.sv` | rc=0 | The literal is the only gate difference, and the two reads are value-equivalent. |
| C2 | The derived list loses the package (`EXCLUDE`) | rc=0 | **rc=1**: `expected one pp_adp_pkg in derived processor sources` | The lookup refuses and does not skip. |
| C3 | Package declaration renamed | rc=0 | **rc=1**: same assertion | Same. |
| C5 | Constant duplicated in the found package | rc=0 | **rc=1**: `assert len(matches) == 1` | The one-match pin bites. |
| C4 | Authority value changed to `0xC580` (AEM_SUPPORTED cleared) | rc=0 | rc=1 (`ImageError`) | The image generator refuses, as expected. |
| C4b, C4c | Authority value changed to legal `0xC589` / `0xC5C8` | rc=0 | rc=0 | The pinned value follows the live authority. |
| C6 | C4b, but the test's value frozen at `0xC588` | rc=0 | **rc=1**: `diverges from ADP_ENTITY_CAPS_C = 0x0000C589` | Contrast for C4b: the suite passes because its read is live. |
| C7 | Processor submodule absent | rc=1 | rc=2 | Loud, with the `git submodule update --init` instruction. It never passes on an empty list. |

**Independence of the read is kept.** The builder obtains the value through `gen_aemi_image.adp_entity_capabilities_declaration()` (`endstation_builder.py:3714-3716`). The suite parses the package text itself. C4b and C6 together show that the suite's expected value comes from its own read, and that this read decides whether the round-trip passes.

### (1d) Rule mutants re-run at head

I re-ran my round-1 script `scripts/mutants.py` (bytecode suppressed) on the head clone: **12/12 KILLED** (`receipts/mutants.tsv`). The three rules the issue names each fail inside the named contract test:
- M1, the `str(v)` reread;
- M5, integer acceptance;
- M9, the scalar `formats`.

## Summary-line wording (taken suggestion)

- `sw/builder/README-parameters.md:70` type column: "EUI-48 YAML string".
- `docs/ENDSTATION_BUILDER.md:883`: "Hexadecimal declarations require YAML strings."

Both are accurate for the code. `_mac48` and `_declared_uint` test `isinstance(v, str)`, so a plain scalar that YAML already resolves to a string (for example `001BC5`) is accepted. That makes "YAML string" more exact than "quoted". The neighbouring lines, which tell the user to quote values, remain correct as instructions.

## Refusal behaviour and artifacts unchanged

**Behaviour.** `receipts/behaviour_head.tsv` is my 91-row MAC/OUI/capabilities/formats matrix run at head. It is byte-identical to my round-1 `behaviour_head.tsv` at `44d3ae3b` (`receipts/behaviour_compare.txt`).

**Artifacts.** `scripts/artifacts.sh` builds the five tracked configurations from base `1fa2357f` and head `11e4e1f2` at one path, with the same gitlink bytes. Results are in `receipts/artifacts_compare.txt` and `receipts/round1_table_compare.txt`.

| Artifact set | Result |
|---|---|
| Default CLI outputs | 50 files; sha256 table and `diff -r` bytes identical base vs head |
| In-tree outputs | 11 identical |
| Configuration files | 5 identical |

Each head table is also byte-identical to my round-1 tables. The CLI table digest `946c79c5...` is unchanged.

**Other images.**
- Packed `aem_desc.{bin,json,map}`: 15 entries, identical to round-1 base and head (`receipts/aem_images_compare.txt`).
- `--write-fragment` sweep fragments: 5, identical to round-1 base and head (`receipts/fragments_compare.txt`).

## Hosted `rtl-fast / verilator-lint` at this head

`receipts/hosted_checks.txt` and `receipts/hosted_lint_job_steps.txt` were read at 2026-09-28T11:05:23Z. Job 108897257968 (run 36412921320, event `pull_request`, `head_sha` 11e4e1f2) concluded **success**:

- step 6 "Run the ratcheted whole-tree lint gate": success;
- step 7 "Prove protocol-processor source lists are derived": success (`rtl-fast.yml:108-109`, `python3 scripts/pp_srcs.py --check --selftest`).

Other contexts at that moment:

| Status | Contexts |
|---|---|
| Completed success | `changes`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`, Yosys shards 0-3 |
| Skipped (not run) | `Physical gPTP (nightly and manual)` |
| In progress | `docs-check`, `elaborate`, Verilator shards 0-4, `yosys-elaboration` |

The rtl-fast run as a whole was still in progress. I report executed jobs only; a skipped context is not a pass.

## Prior public findings on this PR

My own independent pass over the delta was complete before I read the other reviewer's round-1 findings. Until then I knew them only from the manager's round-2 assignment, which lists R388-1 F1, S1 and S2.

| Finding | Status at this head |
|---|---|
| R389-1 F1 (MAJOR, Tests/RTL) | **Resolved.** See the evidence above. |
| R388-1 F1 (the same defect) | **Resolved** by the same evidence. |
| R388-1 S2 (summary wording) | **Resolved**, taken as assigned. |
| R389-1 S1 = R388-1 S1 (stricter six-octet MAC shape; signs and whitespace in quoted values) | **Retained as SUGGESTION**, not a blocker. It is pre-existing behaviour outside this issue's scope. The manager recorded it for the #495 checklist. |

There are no review objects and no inline review comments on the PR.

After writing this verdict and ledger, I read the R388-1 comment (PR #614 comment 5868119667). Its findings are exactly F1 (MAJOR, Tests/RTL), S1 (SUGGESTION, Robustness) and S2 (SUGGESTION, Docs), and the table above disposes of each one. Nothing in it changes my verdict.

## Lens results

```text
[R389] PASS Conformance - issue #595 acceptance 1-5 + round-2 assignment 5868165203 vs delta 44d3ae3b..11e4e1f2 (builder source untouched); receipts/behaviour_head.tsv (91 rows, identical to round-1), artifacts_compare.txt, round1_table_compare.txt, aem_images_compare.txt, fragments_compare.txt - refusal behaviour unchanged; five configs and 50+11+15+5 artifacts byte-identical base vs head; no config value changed; assignment items F1 (derived, no PROSE_OK entry) and S2 met
[R389] PASS RTL - scripts/pp_srcs.py:54-79,87-116 (unchanged) vs sw/builder/test_declarations.py:15-16,233-240 at 11e4e1f2; receipts/pp_srcs_revs.txt (rc 0/1/0 at base/44d3ae3b/head), controls.tsv C1, hosted_lint_job_steps.txt (verilator-lint success incl. step 7 at exact head) - the derived-source-list contract holds again; no HDL, no gitlink change (clone_integrity.txt), generated .svh/ROM outputs identical
[R389] PASS Robustness - sw/builder/test_declarations.py:233-240 at 11e4e1f2; receipts/controls.tsv C2, C3, C5, C7 - the derived lookup fails closed on a missing, renamed or duplicated package and on an absent submodule; tracked-only source list; builder parsers untouched, and behaviour_head.tsv (malformed/boundary/type-confused inputs) identical to round-1
[R389] PASS Tests - sw/builder/test_declarations.py:15-16,230-260 at 11e4e1f2; receipts/gates_head_reviewed_clone.log (rc 0/0), controls.tsv (C1 removed-derivation control fails pp_srcs --check; C4b/C6 prove the independent read is live), mutants.tsv (12/12 killed), gate40_via_test_builder_import.log rc=0
[R389] PASS Docs - sw/builder/README-parameters.md:70; docs/ENDSTATION_BUILDER.md:883-891 at 11e4e1f2; receipts/docs_gates.log (7 pinned Markdown gates rc=0 with the hash-locked renderer) - "YAML string" wording matches the isinstance(str) rule; no other statement changed or made stale
```

## Reviewer-owned completion ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #595 acceptance 1-5 and round-2 assignment; delta scope; 91-row behaviour matrix; 5 configs with 81 hashed artifacts vs base and vs round-1 tables | R389-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| RTL | CLEAN | `scripts/pp_srcs.py` contract; `pp_srcs --check --selftest` at base/44d3ae3b/head; control C1; hosted `verilator-lint` steps 6-7; gitlinks and no-HDL diff; generated `.svh` identity | R389-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| Robustness | CLEAN (S1 retained as SUGGESTION only) | Derived lookup under controls C2/C3/C5/C7; untouched parsers re-checked by the identical behaviour matrix | R389-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| Tests | CLEAN | `test_declarations.py:15-16,230-260`; gate runs; 8 derivation controls; 12 rule mutants; gate 40 via the `test_builder` import path | R389-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |
| Docs | CLEAN | `README-parameters.md:70`; `ENDSTATION_BUILDER.md:883-891`; 7 pinned Markdown gates | R389-2 | 11e4e1f2876c99e8f136d869c70674e077ddcf94 |

Every lens was applied at this exact head. None relies on banking from round 1.

## Real limits

- I did not run these; the assignment disallowed them:
  - the full builder bank (`test_builder.py --require-rv32 --require-elaboration`);
  - the compiler controls;
  - any parent, PP, gPTP or Yosys bank;
  - Docker, act or host `act_ci`.

  For the builder I ran `test_declarations.py`, gate 40 through the `test_builder` import path, the five-config builds, the AEM image and fragment hashes, and the mutants/controls. For the banks at this head I rely on the manager's stated results.
- The public evidence tree I was pointed to (`review-evidence/595-r1` at `a3c8a9a1`) holds the round-1 author evidence at `44d3ae3b` only. I found no published round-2 bank receipt at `11e4e1f2`. The executor's round-2 REVIEW READY comment states its gate results, but I did not verify them from a receipt.
- Verilator was not used, because the PR contains no HDL. So I did not verify the scoped binary's identity.
- Hosted checks were read at one moment, listed above. Several jobs, and the rtl-fast run as a whole, were still in progress. The manager owns the hosted and act acceptance.
- The Markdown gates ran with the hash-locked renderer from `tools/markdown/requirements.txt`, installed into a disposable environment under `scratch/`. Everything else ran with the host interpreter (CPython 3.14, PyYAML 6.0.3).
- Physical calibration was not run, and field skips are not hardware proof.

## Pending manager duties

- Own the hosted and act acceptance at `11e4e1f2`. Wait for the in-progress contexts, and keep executed jobs distinct from skipped contexts.
- Build and validate the final current-dev candidate at the merge turn: source base `1fa2357f`, live dev `7a7582f0`. Source validation at this head does not replace that step.
- Merge requires two independent POSITIVE reviews and explicit maintainer authorisation.
- Carry S1 into the #495 checklist as recorded.

## Packet contents

- `scripts/`:
  - `mkclone.sh`, `gates.sh`, `controls.py`, `pp_srcs_revs.sh`, `docs_gates.sh`, `clone_integrity.sh`;
  - from round 1, reused: `mutants.py` (now with `-B`), `artifacts.sh`, `behaviour_matrix.py`, `aem_images.py`, `fragments.sh`.
- `receipts/`: raw outputs, with local absolute paths redacted to `$PACKET`, `$CLONE` and `$DATA`. `MANIFEST.sha256` lists every publishable file.
- After the probes, the reviewed clone was verified at the exact head (`receipts/clone_integrity.txt`):
  - HEAD, tree and index tree equal the head;
  - 943 tracked blobs re-hashed, with 0 byte or mode mismatches;
  - `git diff-index HEAD` is clean;
  - the gitlinks are unchanged and their checkouts clean: protocol-processor `16be6768`, gptp-processor `5dce647a`, verilog-axis `48ff7a7e`, external `efeb541a` (uninitialised);
  - 0 untracked or ignored files.

  All probes ran on disposable copies under `scratch/`.

R389-2 FINISHED
