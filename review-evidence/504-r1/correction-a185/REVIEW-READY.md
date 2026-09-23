[A185] REVIEW READY
Commit: `5081a25a451b4ac1c00f286ec59ab041c22fdde9`, tree `68a0628be2b55c1180a0e5751d2355cb8f987268`. The head is local and unpushed. It descends from live dev `483a133ed08867ea0d300d2b4a027b5b48a4282f` through the clean merge `f6a55e4c`. That merge's tree equals `git merge-tree` of `3d90958f` and `483a133e`. Two one-line commits follow the merge, with no trailers. Worktree and index are clean. Gitlinks are unchanged: verilog-axis `48ff7a7e`, protocol-processor `424c688f`, gptp-processor `c1b61743`.
Changed: `sw/builder/test_builder.py` (store-class resolver and its controls) and `scripts/ci_rv32_sdk_selftest.py` (download and receipt controls). Also `docs/integration/BAREMETAL_FIRMWARE.md` and `docs/testing/CI_WORKFLOWS.md`. The installer, both workflows, `ci_events.py`, `check_baremetal_only.py` and `test_firmware_compiler.py` are blob-identical to the reviewed head, so the cache key is unchanged. No product, RTL, firmware, pin, residual, text-rule or ratchet change.

| Finding | Resolution at the root | Failing control and evidence at the head |
|---|---|---|
| F1 MAJOR | Stores are classified by instruction class: integer, FP (`fsh`/`fsw`/`fsd`/`fsq`) and atomic (`amo*.w`, `sc.w`). Each is judged at every 32-bit word it writes. Any other memory-addressing non-load is refused as unclassified. Overlapped modelled words are invalidated. The census ISA and SDK selection are unchanged. The docs state the census ISA (`rv32imafd`/ILP32D) and the classifier boundary. | Literal-assembly class controls run on every machine. Five compiled paged-base mutants are refused on `RESOLVER_STORE_PIN`: float, double, exchange, fetch-or and compare-exchange. Each is measured to emit its class. R228-1's float, double and uint32 plants are all refused on that pin with the gate otherwise green. 8/8 fix-removal mutants are KILLED. Pre-fix and post-fix resolvers agree on 106 of 116 census assemblies; the 10 that differ are the new mutants. |
| F2 MAJOR | The self-test drives `install()` with no `--archive`, through a mocked download. | Unpinned well-formed, truncated, empty and near-pin payloads are each refused before tar or relocation runs. A positive download control proves the path is taken. R228-1's deleted-check mutant is KILLED, as are 6/6 weakenings (prefix compare, warn-only, check after tar and others). R228-1's download probe is unchanged. |
| F3 MINOR | The provenance field set and installer digest are pinned independently of the installer. New controls retarget a symlink and plant an escaping compiler. R228-S1 guards gain controls too. | R228-1's `mutate_installer.py`: 23/23 KILLED, against 15/23 at the reviewed head. |

Validation, exit 0 at the head:
- A fresh SDK install into a new prefix took 13.1 s from the verified archive. A cache hit took 0.83 s, and verify-only passed.
- Gate 1b mapped to that prefix, with the scoped 5.050 elaborator: 213/213 mutations (208 plus 5 new) and 17/17 and 4/4 positives. 46/46 RTL variants elaborated, and 7/7 instrument-only shapes passed. 0 NOT RUN and 227 compiles, with argv[0]-only mapping and argument tails preserved. The residual is unchanged.
- Gate 1b absent: 182/182, 17/17, 4/4 and 46/46, with exactly one NOT RUN and zero compiles.
- `ci_rv32_sdk_selftest.py` passes 25 tests, and `test_firmware_compiler.py --selftest` passes.
- `check_baremetal_only.py`: `--check` finds 0 findings and `--selftest` passes 365 arms.
- `ci_events.py`: `--check` passes 1555 items and `--selftest` passes 1198 arms.
- `docs_check.py` passes.
- `check_em_dash.py` finds 0 findings against `52711029` and against `483a133e`.
- The doc path, TOC, doc style, Python idiom, hygiene and ratchet gates pass.

Acceptance: items 2, 3 and 5 were re-measured locally at this head. The hosted, act and full-bank parts of items 1 and 4 remain with the manager. No hosted cache-hit run exists yet.
Open risks/questions:
- R228-S2 and S3 were not taken, because they change installer behaviour.
- Out-of-scope observations for possible new Issues:
  - The CFG drops branch targets that are not block labels. GCC uses numeric labels in LR/SC loops; the SC store is still reached by fall-through.
  - The pre-existing sub-word frame-slot value imprecision remains.
- Raw receipts carry local paths.

The handoff, PR body, commands, scripts and receipts are in the author packet (`$AUTHOR_EVIDENCE`, 504-a185). There was no push, PR edit, merge, delegation or self-approval. R227 and R228 re-review the corrected head.
