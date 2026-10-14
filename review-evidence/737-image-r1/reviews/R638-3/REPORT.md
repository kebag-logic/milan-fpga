[R638] NEGATIVE - exact head e6b86814e6844ef61ba46a867a0fdbfbb925cceb

# R638-3: internal cleared-context review of PR #738 (issue #737, image lane), round 3

- Reviewer: [R638], internal independent reviewer, round R638-3.
- Exact head `e6b86814e6844ef61ba46a867a0fdbfbb925cceb`, tree `7e566e139576b082580ab07e334a62ffa1b881f7`.
- Source base `fa7347fc59173f90e4feec2df207692e6e6e72ec`; live dev `fa8209889411e8ca95757174c981f720dbcd95a2`.
- Full range `fa7347fc..e6b86814`: 31 files, 15 one-line commits. Round-3 delta `18f2df92..e6b86814`: three commits, 15 files.
- Zero paths under `.github/`: `git diff --quiet fa7347fc HEAD -- .github` is rc 0, and the `.github/workflows` tree listing is byte-identical at both commits (ruling d holds).
- Authorities read, in order:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - Issue #737: body, registry 6160859632, lane assignment 6160953880, scope change 6166823105, author STOP 6167951082 and REVIEW READY 6169166135.
  - PR #738 rulings 6162652582, 6163057631, 6165220472 and 6166238176; round-3 assignment 6167899804 and its amendment 6167966247.
  - The PR body.
  - The diff and history.
  - Public evidence `review-evidence/737-image-r1/author-r3/round3-*` at `d7f2e7f1`.
- Independence: I applied all five lenses to the diff and planted the command-table probes before reading any prior review. Only then did I read R638-2 (6167893456) and R639-2 (6166908258), to resolve their findings. I read no other round-3 review and no private author material.
- No manager source bank ran at this head, and none is claimed or inferred. Physical calibration is NOT RUN.

## Verdict summary

Round 3 fixed all four round-2 MINOR findings at their cause. It also refuses every installation form R638-2 and R639-2 listed. I reproduced the image-side claims myself:

- **Image identity.** My own export of `fpga-validation@sha256:86d7aa16…5e6c` authenticates as follows: every blob against its name, then index, manifest, config and all 14 diff-ids. Results are in `receipts/image-scan-summary.json` (header) and `receipts/verify-archive.log`.
- **Lock.** `build.py --check-lock --verify-archive` passes against my own `--prepare-only` context, which re-downloaded and verified every source. That run reproduced recipe `08fe0f5b…906e` (`receipts/prepare-only.log`).
- **Cold builds.** The two public cold records agree on manifest `sha256:86d7aa16…`, config `sha256:62b56e1a…` and all 14 compressed and uncompressed layers. My export equals both records.
- **Privacy.** The privacy report my verification run produced is byte-identical to the author's: SHA-256 `2ef6b8ef…`, 526 authenticated allowances. My independent scan of every layer, the config, history, labels and Env found 54 word-bounded protected hits. Every one is an authenticated upstream member.
- **Offline smoke.** The smoke run passes offline (rc 0). Tool versions equal the workflow pins.

Two defects remain open, so the verdict is NEGATIVE:

- **R638-3-F1 (MAJOR).** The closed command table is not closed. 19 in-class forms are accepted with no refusal, no tool record and no residue entry. Examples include `gh release download`, `git submodule add <url>`, `os.popen(...)`, `python3 <<EOF`, a Makefile pattern rule, a step `working-directory:` and a job-level reusable workflow.
- **R638-3-F2 (MINOR).** The deriver treats any directory under `/tmp/` as runtime residue. As a result, the documented `ci_tool_inventory_selftest.py` fails under the default temp directory, including inside the image on the reference CPython 3.12.3.

## Findings

### R638-3-F1 MAJOR: the closed command table still accepts installing forms silently

- **Lenses:** Conformance, Robustness, Tests, Docs.
- **Where:**
  - `ci/image/command-table.json:530`: `gh` is `non-installing` with no `prefixes`.
  - `ci/image/command-table.json:543`, `:564`, `:571`, `:631`: git `archive`, `clone`, `config` and `submodule` carry no argument restriction.
  - `scripts/ci_command_table.py:19-20`: the `NETWORK` denylist and the `CALLS` set. `os.popen`, `os.exec*`, `os.spawn*` and `asyncio` subprocesses are absent.
  - `scripts/ci_command_table.py:238`: only the exact argv `python3 -` and `python -` follow a heredoc.
  - `scripts/ci_command_table.py:378-380`: a clone without `://` counts as local.
  - `scripts/ci_command_table.py:398`: `-f` and `-C` only.
  - `scripts/ci_command_table.py:475-485`: only literal rule names are followed, so pattern rules are skipped.
  - `scripts/ci_tool_inventory.py:183-193`: a step's `working-directory:` and a job-level `uses:` are ignored.
  - `docs/testing/CI_IMAGE.md:28` and `:30`.
- **Authority:** the round-3 class ruling, 6167899804 item 1 and amendment 6167966247:
  - "Every command the deriver meets must be in one committed table … non-installing, with its subcommands where it matters: for example git checkout, diff and status, but not fetch <url> or clone".
  - "a followed Python script's subprocess call in any argument form".
  - "A followed script that imports a network module … or runs subprocesses must be declared".
  - "Every script that is run is followed. That includes root-level scripts and Makefile targets."
  - Assignment 6160953880 item 1: "A check fails when a workflow installs a tool the inventory lacks".
- **Evidence:** `probe_command_table.py` plants each form in a fixture tree under the packet scratch directory and runs `derive()`. The output is in `receipts/probe-command-table.jsonl`.
  - **Controls behave correctly:** `npx`, the `python3 -` heredoc, a followed `urllib.request` script, a literal Makefile target and `bash -c` (residue) are each refused or recorded.
  - **The following 19 in-class forms are ACCEPTED-SILENT:** no refusal, no tool, no residue entry.
    - Subcommands classified as non-installing wholesale:
      - `gh extension install example/gh-fixture`;
      - `gh release download v1.0 -R example/tool`;
      - `git submodule add https://…`;
      - `git config submodule.x.url https://…` followed by `git submodule update --init x`;
      - `git clone --no-hardlinks git@host:org/tool.git`, a network clone treated as local;
      - `git archive --remote=https://…`.
    - Python program text not followed:
      - `python3 <<'EOF' … urllib … EOF` (no `-`);
      - `python3 -I - <<'EOF' … EOF`.
    - Python subprocess calls in other forms, none requiring a declaration:
      - `os.popen('npx …')`;
      - `os.execvp('npx', …)`;
      - `os.spawnlp(…, 'npx', …)`;
      - `asyncio.create_subprocess_exec('npx', …)`.
    - Network and installing modules outside the five-name denylist, none requiring a declaration:
      - in-process `pip._internal` `install`;
      - `urllib3`;
      - `asyncio.open_connection` with `ssl`.
    - Followed scripts and Makefile targets not actually followed:
      - a selected target whose prerequisite is built by a `%` pattern rule running `npx`;
      - `make --directory=fx run`, where the root Makefile is followed instead;
      - a `make` step with `working-directory: fx`, where the root Makefile is followed instead of `fx/Makefile`;
      - a job-level `uses: example/tools/.github/workflows/install.yml@main`, which runs a remote workflow that is never seen.
  - **Four borderline forms, within the ruling's residue class but not even recorded as residue:** `echo 'npx …' | bash`, `bash <<< 'npx …'`, a static alias `runner = subprocess.run`, and `importlib.import_module('urllib.request')`. Note that `__import__` is recorded as residue but `importlib.import_module` is not. Also, the committed inventory's residue list (735 entries) carries one entry, `Python command assembled at runtime`, with no location, so it cannot be actioned from the checklist.
  - **The two digest-pinned `container:`/`services:` fixtures are recorded as image tools.** They show as ACCEPTED-SILENT in the receipt only because they produce no residue, and they are correct.
  - **At this head the derived inventory is still complete for the unchanged workflows.** `--check` is rc 0 on host Python and on CPython 3.12.3 in the image (`receipts/inventory-check.log`, `receipts/inventory-in-image.log`). The workflows use none of these forms. `rtl-fast.yml:130` does use `working-directory: tests`, but only with `behave`.
- **Impact:**
  - The guarantee the ruling chose, "classify every command, refuse the unknown", is complete by construction only if every row is closed over its installing subcommands, every execution surface is classified, and every run path is followed. Those three properties fail here.
  - A later workflow or script edit using any form above regenerates (`--write`) and passes `--check` with the installed tool absent from the inventory. That is exactly what acceptance item 1 forbids. Once the switch lane adopts the image, such a tool is missing offline or is installed outside the pinned image.
  - The guide's sentence at `CI_IMAGE.md:28`, "Unknown names and unclassified subcommands refuse generation", is false for `gh` and these git subcommands. `:30` implies subprocess coverage that does not include the `os`/`asyncio` forms.
- **Required outcome:**
  - **Table rows:** give every command row that has installing subcommands an explicit permitted-form list, and refuse other subcommands. At least `gh` and git `submodule`/`config`/`archive`/`clone` (any remote syntax) need this; also review `node`, `java`, `cmake` and `sbt` rows for the same property.
  - **Python execution surfaces:** classify all of them (`os.popen`, `os.exec*`, `os.spawn*`, `os.posix_spawn*`, `asyncio` subprocess, `pty.spawn`), or refuse any call on the `os`/`subprocess`/`asyncio` modules not in the table.
  - **Network imports:** decide them by a closed allowlist of permitted imports, or refuse any import outside a known non-network standard-library set, rather than a five-name denylist.
  - **Python from stdin:** follow it in every argv form, or refuse it.
  - **Run paths:** follow `working-directory:`/`defaults.run.working-directory`, the `--directory`/`-C<dir>` forms and pattern rules, or refuse them.
  - **Reusable workflows:** refuse a job-level `uses:` unless it is a local workflow that is itself derived.
  - **Residue:** the indirect-shell forms the ruling places in residue must at least appear in the residue list, with a location.
  - **Controls and guide:** add a refusal control for each class above, and make `CI_IMAGE.md:28-31` describe the exact guarantee.
- **Verification:** `CI_IMAGE_SHFMT=<pinned shfmt> python3 -I probe_command_table.py <checkout> <scratch-not-under-/tmp>` reports no ACCEPTED-SILENT outcome, except the two digest-pinned image rows, which must list the image as a tool. The repository self-test contains the new controls, and `--check` stays rc 0 at the corrected head.

This retains the cause of R638-2-F1, R639-2-F1, R638-1-F3 and R639-1-F2 under the round-3 class ruling. The specific forms those rounds listed are closed; see the disposition table below.

### R638-3-F2 MINOR: a checkout or fixture under `/tmp` stops Makefile following, and the inventory self-test fails by default

- **Lenses:** Tests, Robustness.
- **Where:**
  - `scripts/ci_command_table.py:389`: `if '$' in str(target) or str(target).startswith('/tmp/')` makes the residue decision on the absolute resolved directory, including the checkout root itself.
  - `scripts/ci_tool_inventory_selftest.py:143` uses `tempfile.TemporaryDirectory`, and `:117-119` is the Makefile `curl` control.
  - `docs/testing/CI_IMAGE.md:108` and the PR body's "How to validate" both list the self-test.
- **Evidence:**
  - On the host with `TMPDIR` unset, `ci_tool_inventory_selftest.py` exits 1 with `AssertionError: installer needs an explicit pin reader` (`receipts/inventory-selftest.log`).
  - On the host with `TMPDIR` outside `/tmp`, the same command exits 0 (`receipts/inventory-selftest-tmpdir-scratch.log`).
  - In the final image (CPython 3.12.3, offline, `TMPDIR` unset), the result is `default_tmp_selftest_rc=1`, while `TMPDIR=/var/tmp/x` gives rc 0 (`receipts/inventory-in-image.log`).
  - The author's public cold-build driver sets `TMPDIR` to a scratch directory (`author-r3/round3-cold-build-driver.py`). Hosted runners and the image do not.
- **Impact:**
  - **Self-test fails by default:** the documented validation command fails on a default runner and in the image, for a reason unrelated to the property it tests. This repeats the R638-2-F4 pattern.
  - **Planted control evades:** under a `/tmp` root, the planted Makefile `curl` installer is accepted instead of refused.
  - **Location-dependent derivation:** for a real checkout located under `/tmp`, every `make` command becomes residue, and the derived inventory depends on the checkout location.
- **Required outcome:**
  - Base the runtime and external-directory decision on the literal `-C`/working-directory argument, or on paths outside the checkout. Never base it on the checkout's own absolute location.
  - The self-test passes with the default temp directory, both on the host and in the image.
- **Verification:**
  - `python3 scripts/ci_tool_inventory_selftest.py` with `TMPDIR` unset is rc 0 in the image.
  - `--check` gives byte-identical output from a checkout copy under `/tmp` and one elsewhere.

### Suggestions (do not affect the verdict)

- **S1 (retained from R638-2-S1).** Add runtime privacy rules for the checkout and `--work` paths. The absolute-path class covers `/home/` and `/data/X/`, but not other roots. My scan found no host working root in any layer.
- **S2 (retained from R638-2-S2).** The guide's pull-by-digest step assumes the registry serves the lock's manifest digest unchanged. State how the push preserves it, and check the registry digest against `image.lock.json` before announcing it.
- **S3.** The table row for `python`/`python3` carries an `installer_forms` field that `ci_command_table.py` never reads; the `pip install` form is hard-coded at `:349`. Either drive the behaviour from the table or drop the field.

No RESIDUE is recorded.

## Focus items at this head

| Item | Result | Evidence |
|---|---|---|
| 1. Derived inventory and its check | `--check` rc 0. All R638-2/R639-2 forms refused, and container/services digests recorded with moving tags refused. A new command name is refused. Both declared-script controls (undeclared network import; changed declared content) pass, as do the missing and orphan controls. All 109 declared script hashes equal the head bytes. The table is not closed (F1), and the self-test is TMPDIR-dependent (F2). | `receipts/inventory-check.log`, `receipts/probe-command-table.jsonl`, `receipts/inventory-selftest-tmpdir-scratch.log`, `receipts/inventory-in-image.log` |
| 2. Dockerfile: multi-stage, one layer per tool, pinned base, checksummed sources | Unchanged since round 2. `docker history --no-trunc` shows the base plus 13 tool COPY/RUN layers, 14 layers in all. Base pinned by digest. Every source checksummed, verified again by my `--prepare-only`. | `receipts/image-history.txt`, `receipts/prepare-only.log` |
| 3. Reproducible build and lock | The two cold records match (manifest, config, 14 layers and 14 diff-ids). Recipe digest reproduced. The lock is bound to my export by `--verify-archive`. Against round 2, base and all 12 tool layers have identical diff-id and OCI digest; only the validation layer changed. Every per-layer recipe digest changed by the parent chain, and the system/gtest source digests changed with the added fallback URLs. Pin change, digest change. | public `author-r3/round3-cold-comparison.json`, `receipts/verify-archive.log`, `receipts/image-inspect.json` |
| 4. Versions and offline smoke | Smoke rc 0 with `--network none` in 27 s. Verilator `rev v5.050`, Yosys 0.66 (`86f2ddeb`), sv2v v0.0.12, sbt 1.10.x, CPython 3.12.3, and a real oracle packet. | `receipts/smoke-offline.log` |
| 5. Privacy | Config: no `User`/`WorkingDir`. The only label is the base `org.opencontainers.image.version`. Env has the 8 documented entries. History has 27 entries with no host path. My scan matched no protected identity in member names, link targets or owners, and no build-context leftover. 54 word-bounded content hits, 54 covered by authenticated upstream allowances. The repository report is byte-identical to the author's. | `receipts/image-scan-summary.json`, `receipts/privacy-report.json`, `receipts/image-inspect.json`, `receipts/image-history.txt` |
| 6. CI_IMAGE.md | Rebuild, digest-change and pull-by-digest sections are accurate. The SDK link and `MILAN_RV32_CC` consumers match `fw_rv32.py:31`, `ctrl_image.py:445` and `test_builder.py:4767-4768`. Retention and the literal-mask step are documented. Exception: `:28`/`:30` (F1). | doc gates, `receipts/gate-*.log`, `receipts/gate-in-image-emdash-toc.log` |
| 7. No workflow change | Holds. | `receipts/clone-integrity.txt`; tree listing hash equal at `fa7347fc` and HEAD |

## Round-3 MINOR fixes, verified

- **R638-2-F2 (durable Ubuntu packages): closed.**
  - 185 of 186 package rows carry one `snapshot.ubuntu.com/ubuntu/20261014T000000Z/…` fallback; the Docker client row comes from a non-archive host.
  - `verified_download` tries the fallback only after a primary HTTP 404, and still applies the original size and SHA-256 (`build.py:118-136`).
  - The 404-primary, corrupt-fallback and plain-primary controls pass (`receipts/build_selftest.log`).
  - My own fetch matched 181 of 185 fallbacks byte-for-byte with zero mismatches. The other four (`libfribidi0`, `libthai0`, `libtiff6`, `netbase`) still returned 5xx from the snapshot service after five retries per attempt across four runs. That is service availability, not a mismatch (`receipts/fallback-urls-summary.json`).
  - The guide states the retention property and the `CI_IMAGE_LOCK_LITERALS` step. `check_baremetal_only.py --check`/`--selftest` are rc 0 with the new literals.
- **R638-2-F3 (buildx config key): closed at the cause.**
  - `build.py:327-333` exports the image, authenticates the archive (`image_archive.metadata`), compares its manifest digest with the build result, and takes the config digest from the authenticated manifest.
  - The author's public `round3-buildx.json` records v0.38.0 metadata without the old key, and both cold builds complete.
  - I did not run buildx (see limits). The code no longer reads the key.
- **R638-2-F4 (patch self-test identity): closed.**
  - The self-test passes on the host with an empty `HOME` and `GIT_CONFIG_NOSYSTEM=1`.
  - It also passes inside the image with no global or system identity (`global-identity-rc=1`, `system-identity-rc=1`, then rc 0 with all PASS lines). See `receipts/privacy_patch_selftest-*.log`.
- **R638-2-F5 (SDK location and consumers): closed.**
  - The guide documents the `$HOME/br-milan-rv32/host -> /opt/rv32-sdk` link for the job user.
  - It also documents that the census (`test_builder.py:4767-4768`) does not read `MILAN_RV32_CC`, while `fw_rv32.py:31` and the ctrl tests (`ctrl_image.py:445`, `ctrl_capture.py:242`) do.

## Manager rulings, checked

- **(a)** The `mf48` resource-calibration arm NOT RUN is the existing hosted skip. It is not a finding.
- **(b)** The grouped builder evidence remains applicable at this head. `sha256(HEAD:sw/builder/test_builder.py)` is `997e8528…`, the hash every group was verified against in round 2, and the command table pins that same hash. The base and all tool layers the campaign ran on are byte-identical in the new image. It is accepted as the completed verdict and was not re-run.
- **(c)** `MAKEFLAGS += -e`: the make layer (GNU Make 4.3, `make 4.3-4.1build2`) is unchanged from round 2, where the hosted docs-check at live dev took the identical skip. No coverage loss, and not a finding.
- **(d)** No workflow file changed.

## Prior findings at this head

| Finding | Status at e6b86814 | Evidence |
|---|---|---|
| R638-2-F1 / R639-2-F1 MAJOR inventory forms | **Every listed form closed.** Refused: `dpkg -i`, `npx`, `go install`, `snap`, `uv tool`, `docker run`, `git -C … fetch <url>`, the followed `urlretrieve` script, keyword `args=`, a root-level script, and the Makefile download/extract/install. Container and services digests are recorded, and moving tags refused. **The cause is retained as R638-3-F1** under the class ruling. | `receipts/probe-command-table.jsonl` (`r638-2-*`, `r639-2-*`) |
| R638-2-F2 MINOR package retention | Closed | see above |
| R638-2-F3 MINOR buildx key | Closed | `build.py:327-333`; public `round3-buildx.json` |
| R638-2-F4 MINOR patch identity | Closed | `receipts/privacy_patch_selftest-in-image.log` |
| R638-2-F5 MINOR SDK location | Closed | `CI_IMAGE.md` Environment and adoption sections |
| R638-2-S1/S2 | Not implemented; retained as S1/S2 | |
| R638-2-S3 literal-mask note | Implemented | `CI_IMAGE.md` regeneration section |
| Round-1 findings (R638-1-F1..F10, R1; R639-1-F1..F5) | Closed in round 2. Nothing in the round-3 delta reopens them: the Dockerfile, `install.py`, `smoke.py`, `normalize.py` and the tool layers are unchanged, and privacy and bare-metal gates pass. | `receipts/verify-archive.log`, `receipts/gate-*.log` |

## Clean lens

[R638] PASS RTL - `ci/image/install.py` and `ci/image/Dockerfile`, unchanged since `18f2df92` (`git diff --quiet 18f2df92 HEAD -- ci/image/Dockerfile ci/image/install.py ci/image/smoke.py ci/image/normalize.py sw scripts/ci_rv32_sdk.py` is rc 0). Checked against the inventory pins `verilator v5.050`, `yosys v0.66` and `sv2v v0.0.12`. The Verilator and Yosys layer diff-ids are unchanged from the round-2 image, and the offline smoke run in `receipts/smoke-offline.log` exercises them:

- a Verilator `--binary --assert` model build and run;
- sv2v, then Yosys `synth`, `abc -g AND` and `check -assert`.

No HDL, testbench, synthesis source or submodule gitlink changes in `fa7347fc..e6b86814`; all six gitlinks are equal at base and head (`receipts/clone-integrity.txt`).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R638-3-F1) | Class ruling and amendment; `scripts/ci_command_table.py`; `scripts/ci_tool_inventory.py`; `ci/image/command-table.json`; `tool-inventory.json`; `sources.lock.json`; `image.lock.json`; `build.py`; my image export; `probe-command-table.jsonl` | R638-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| RTL | CLEAN | `install.py`/`Dockerfile` vs workflow pins; unchanged tool-layer diff-ids; offline Verilator/Yosys/sv2v smoke; gitlinks | R638-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| Robustness | UNCLEAN (R638-3-F1, F2) | Command-form probes; TMPDIR-dependence on host and in image; 185 fallback URLs; 404/corrupt controls; no-identity runs; `--prepare-only` and `--verify-archive` | R638-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| Tests | UNCLEAN (R638-3-F1, F2) | `ci_tool_inventory_selftest.py` (default and non-/tmp TMPDIR, host and image); build/integrity/privacy/patch self-tests; bare-metal `--check`/`--selftest`; py-idiom; smoke | R638-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |
| Docs | UNCLEAN (R638-3-F1) | `docs/testing/CI_IMAGE.md` (all sections); `docs/README.md`; PR body; REVIEW READY; doc gates (`docs_check`, doc style, doc paths, em-dash and TOC in the image) | R638-3 | e6b86814e6844ef61ba46a867a0fdbfbb925cceb |

## Real limits

- **No reviewer cold build this round.** The two cold-build records are author evidence. I verified that they agree, re-derived the recipe digest, and authenticated the locally present final image against the lock with my own staged sources. I did not run buildx: the host has no buildx plugin, and I did not install one. That buildx v0.38.0 completes the build therefore rests on the code change plus the author's public `round3-buildx.json`.
- **Docker use.** It was limited to read-only inspection and offline disposable runs:
  - `image inspect`, `history` and `save` of the final image and of the pinned base, which was already present locally;
  - the offline smoke, the patch self-test, the inventory check and self-test, and the em-dash and TOC gates, each in `--rm --network none` containers with the clone mounted read-only.
  - No pull, build, push, login, tag or daemon state change.
- **Fallback verification incomplete.** Four snapshot URLs could not be fetched because the snapshot service kept returning 5xx. One background retry attempt was stopped at the session's background limit before printing anything, and it is superseded by the four foreground retry receipts.
- **Host interpreter.** The host is CPython 3.14.7. The inventory check and self-test were repeated on CPython 3.12.3 in the image. Host-only gates that needed the pinned Markdown renderer (em-dash, TOC) exit 2 on the host, which is a setup failure and not a pass. They were re-run in the image with rc 0.
- **One host only.** Cross-host reproducibility and a registry round trip are untested.
- **Not run.** No builder campaign re-run, product regression, act run, hardware or physical calibration.
- **Hosted snapshot.** `receipts/exact-head-check-runs.tsv` records one observation at 14:08Z: 22 success, 1 skipped (Physical gPTP), and Verilator shards 0, 1, 3 and 4 of 5 in progress. It is not a hosted verdict.
- **Clone untouched.** `receipts/clone-integrity.txt` records the following. All probes ran in fixture trees under the packet scratch directory.
  - The worktree and index equal HEAD.
  - The staged blob/mode listing equals the HEAD tree listing (SHA-256 `d455bb16…`).
  - All six gitlinks equal HEAD and base.
  - `git status --porcelain` is empty.

## Pending manager duties

- Hosted and act acceptance at the eventual head; the Verilator shards were in progress at read time.
- Current-dev merge-candidate validation: source base `fa7347fc`, live dev `fa820988`.
- Re-review of F1 and F2 at a corrected head; a new cold-build pair if the recipe inputs change. `command-table.json` and `ci_command_table.py` are recipe inputs.
- Image publication only after both reviews are POSITIVE, then confirmation that the registry digest equals `image.lock.json` (S2).

## Publishable files

`MANIFEST.sha256` lists every published script and receipt. Host-specific paths in receipts are replaced by `<packet>`, `<clone>`, `<home>` and `<host>`. The image scan publishes neutral needle labels and counts only. The exported image, staged sources and fixture trees stay under `scratch/` and are not published.

R638-3 FINISHED
