[A615] REVIEW READY

PR: #738. Relates to #737.
Commit: `d7cb1f90af1b8c2f115f58281991f1c9626447f9` on `737-ci-image` (local, not pushed).
Round-ten assignment: PR #738 comment 6208056999. Starting head `6f86eee6` (POSITIVE in R638-9 6207639165 and R639-9 6207314215).

Changed:
- Item 1, merge. `03dcd0c36` merges `origin/dev` `4a9b5a2a` with a merge commit. The one conflict was in `scripts/check_baremetal_only.py`, where both sides added an arm function at the same place; both are kept (867 arms pass).
- Item 2, regeneration through the generators. No workflow changed; each guard that refused a merged form was extended.
  - Readers: `PIP_CONSTRAINT` is read exactly, as a checkout file whose every line is an exact archive URL with its `sha256`. `apt-get -o Dir::Cache::archives=${RUNNER_TEMP}/…`, `scripts/ci_install_cache.py` and `python3 -m venv DIR` are modelled; any other option refuses by name.
  - Make and shell forms the merged scripts use, each with a differential fixture: 224/224 fixtures over 185 census shapes, measured in the locked image.
  - Inventory regenerated: 46 records (`e19dd3542`, `f1c041bce`). Source lock: the PyYAML 6.0.2 wheel the constraints file pins (`e8d58bd19`).
  - Image: the Python layer holds PyYAML 6.0.2 and the validation layer the merged walker and audit. Manifest `sha256:68331c7908fcf2c1c6226c621bcd48287916ff20bac23f1f2b7279dffab94e08`, config `sha256:772f24ce…`, 3,930,754,018 bytes.
  - Lock: recipe `712f7b38…` (`54fbcba6a`), after recipe `a8e55b00…` (`943d47dbe`). For each recipe, two `--no-cache` cold builds gave the same image (353,518/386,192 ms and 434,076/419,175 ms), with `--record-lock` passing on export A and `--check-lock --verify-archive` on export B. Offline smoke: 97/97 records.
  - #749's job-private environment, `pip` into `RUNNER_TEMP` and the LiteX patch series, and #745's census budget step are inventoried and traced. The environment step runs in its image form, the patch series as committed, and the budget step verbatim.
  - Audit: `python3 --version`/`-V` and `node --version`/`-v`, exactly, are runs of the image interpreter (76 controls). Reviewed lists: 26 inline and 15 generated entries were added for the merged workflows' new programs, and 21 and 4 that no traced step runs any more were removed, leaving 108 and 461.
  - Population merge: each step's reconciliation row comes from the run that selected its job (`ea5822952`).
- Item 3, re-trace. Every reached step was traced in the image with `--network none` at `54fbcba6a`.
  - The docs gate legs and union and the elaboration legs and union ran as root (112 steps); every rtl-fast job ran as uid 1000 (83 steps).
  - 195 of 230 steps were traced, every exit status was 0, there were zero findings and 320,983 exec instances. All 115 listed gate commands were observed, 111 with the listed arguments; the other 4 are runner values.
  - The 35 untraced steps are 30 orchestration steps (`ci-manifest`, `ci-fail-fast` and `ci-cancel-tail` call the GitHub API by design) and 5 cache-miss Verilator and Yosys builds the image replaces.
  - All 108 inline or streamed and 461 generated reviewed entries are used, and no other.
  - The receipt is committed as `ci/image/exec-audit-receipt.json` in `d7cb1f90a`, which changes only the receipt (864,566 bytes, sha256 `b8c28953…`).
- Item 4, residue. R638-9-R3: the PR body's Round 9 row uses the reviewer's exact text. R638-9-R2: the reviewer's line is in the guide's boundary list (`docs/testing/CI_IMAGE.md:107-108`). R638-9-R1 and the suggestions were not taken (to #495).

Validation:
- 26 checks at `d7cb1f90a` under CPython 3.12.3 return rc 0, with `ci_tool_inventory.py --check` last. They cover:
  - the inventory, patterns, nodes and exact self-tests;
  - the differential check and the census-gate self-test;
  - the build, integrity, privacy and privacy-patch self-tests;
  - the bare-metal check (0 findings) and its self-test;
  - the idiom gate and its self-test;
  - the docs, doc-style, doc-paths, em-dash (`--base 4a9b5a2a`), TOC, anchors, hygiene and whitespace gates;
  - the exec audit self-test in the image (76/76);
  - `--check-lock --verify-archive`;
  - `--prepare-only`.

Open risks/questions (decision points):
1. Each reviewed scope-text entry names the generated workflow the scope history self-test reads, not its `.github/ci-templates/` source. The new reasons state that the self-test runs the shipping text and planted mutations; the old ones said "historical revision".
2. The trace uses `--base fa7347fc`, the lane's fork point, as before. Every diff-scoped gate sees a superset of the diff against `4a9b5a2a`, and no reached step is skipped.
3. The differential receipt was re-measured in the locked image (same 224 outcomes). That changed the inventory input digest and the recipe digest, so the cold builds and lock were repeated, and the image is the same.
4. The first final trace (at `7e718354e`) was clean, but its merge refused because of the row-selection defect fixed in `ea5822952`. A second trace was cut by a host reboot. Both are superseded, and the committed receipt names its traced parent `54fbcba6a`.
5. `dev` has since moved to `1f6f2f57` (#751, #753). Those commits change documentation and `scripts/check_doc_style.py` only, and touch none of this PR's files. A read-only `git merge-tree` is conflict-free, and the doc-style gate passes on that tree. It is not merged here, because the assignment names `4a9b5a2a`.

HANDOFF.md and PR-BODY.md have Round 10 sections: the commits, the change map with file:line, the reviewed programs, the image, lock and cold-build table, the population evidence and the final checks. This is local evidence, not hosted CI and not a review verdict. No push, registry login, PR edit, merge, firmware or linked-image change, or product-test assertion change occurred. The R638-10 merge-and-regeneration re-review is required.
