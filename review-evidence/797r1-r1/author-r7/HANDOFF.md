# [A711g] #797 lane R1, sync round handoff

- Head: `1de759d3e4d2cfd7d069cf812e5e6549ae8fcb33`. Local branch `797-r1-regref` (PR #825). Nothing pushed; the manager pushes.
- Start: `2c500d0a9c3eb0ef0c764db6978bf8d0ab217ea2`, where both reviews (R753, R754) are POSITIVE.
- Dev merged: `0a75aa774b89ac89351700f63dd8cbb89694af6c` (live `origin/dev`, read by `git ls-remote` at the start and at the end). `git merge-base --all 0a75aa77 HEAD` gives one line, `0a75aa77`. Origin `https://github.com/kebag-logic/milan-fpga.git`.
- Posted on #797: TAKEN issuecomment-6719042923; REVIEW READY issuecomment-6720131225 (text in `review_ready.md`).
- Receipts: `receipts/INDEX.md`, generated from the files present, host paths replaced. Tools: `tools/`.

## Assignment

Sync round. Merge `origin/dev` with `--no-ff` (no rebase, force or amend), resolve each conflict keeping both sides' intent, regenerate what the lane's files feed through their generators, change nothing else, run the named gates on a clean clone of the committed head, post REVIEW READY.

## Commits

| Commit | Subject | Files |
|---|---|---|
| `57264e30` | Merge dev 0a75aa77 into the register reference lane, keeping both style-gate pages, regenerating the workflow, page and inventory, and moving dev's MAC_ADDR sequencing note onto the design notes (#797) | parents `2c500d0a`, `0a75aa77` |
| `c73cecf1` | Refresh the SoC extract from a builder export at the merged head, which carries dev's prototype station MAC and identity (#797) | `scripts/register_map_soc.json` only, +8/-8 |
| `1de759d3` | Count both added docs-check steps in the CI event selftest, since dev's inventory gate and this lane's register gate each raised the job from 51 to 52 steps and git merged the two edits as one (#797) | `scripts/ci_events.py` only, +7/-7 |

One wording note on `57264e30`'s subject: "regenerating the page" means the generator ran and wrote `REGISTER_MAP.md` byte-identical. No amend was allowed, so the subject stands.

Dev brought ten PRs (first parent, `1f29f189..0a75aa77`): #828, #831, #836, #815, #834, #841, #842, #849, #847, #846. 402 files differ between `2c500d0a` and `0a75aa77`.

## Conflicts and resolutions

Git reported three content conflicts. Two more needed a change that git could not see: dev edited text this lane had moved, and both sides made one identical edit that now has to count twice.

| File | Conflict | Resolution | Why |
|---|---|---|---|
| `.github/workflows/docs.yml` | Dev added "Documentation inventory freshness gate" (#815, `gate_46`). This lane added "Register reference freshness gate". Both renumbered the later ids | The file is generated (its line 1 says so) from `.github/ci-templates/docs.yml`, which git merged with no conflict and with both steps (`ci-templates/docs.yml:436-439` and `:485-489`). Regenerated with `python3 scripts/ci_gate_workflows.py`; `--check` rc 0. Result: dev's file plus the register step as `gate_51`, with `ci_step_54`, `gate_52`, `ci_step_56` and `ci_step_57` moved up one | Both gates kept. Only the generator writes this file |
| `scripts/check_doc_style.py:37-38` | Dev added `STRICTER_READINGS.md` (#842) at the same line where this lane added `REGISTER_MAP.md` | Both lines kept, this lane's first | Both rules kept. The gate prints "OK (25 current documents)" |
| `docs/reference/REGISTER_MAP.md` | Dev made two edits to the old hand-written page; this lane replaced the page with the generated one | Took this lane's side, then ran `gen_register_reference.py --write`. Dev's RTL changed no CSR input (`git diff 1f29f189 0a75aa77 -- hdl/common/csr` is empty), so the page came out byte-identical and `--check` is fresh | The page is generated from dev's RTL |
| `docs/design/CSR_REGISTER_NOTES.md:188`, `:192` | No git conflict. Dev's two edits to the old page had to go somewhere | Edit 1 (bee02d0c, #797 D0): the `#599` sentence now says "is recorded in the [#599 link-cycle finding]". It was already on this lane's page (`REGISTER_MAP.md:313`) and notes (`CSR_REGISTER_NOTES.md:164`), so nothing changed. Edit 2 (68c76360, #839 / PR #841): the "Sequencing (#839)" text on the `MAC_ADDR_LO` and `MAC_ADDR_HI` cells is appended verbatim to the same cells on the design notes, which hold the old page's cells (`gen_register_reference.py:33`) and to which each register links | Keeps dev's fact. It is moved, not new content, and it is in the same words. The design notes are not in the style gate's `DOCUMENTS` |
| `scripts/ci_events.py:7494`, `:7508`, `:7521`, `:7524`, `:7542`, `:7582`, `:8117` | No git conflict. Dev (#815) and this lane each added one step to the template's `docs-check` job, and each changed the selftest's literal count from 51 to 52 and "found 50" to "found 51". The two edits were identical, so git kept one, but the merged job has 53 steps (`.github/ci-templates/docs.yml`). At `c73cecf1`, `gate_41` (`ci_events.py --selftest`) failed: "expected a finding naming 'job `docs-check` must carry exactly 52 steps', got ... must carry exactly 53 steps" | Commit `1de759d3`: 52 becomes 53 and "found 51" becomes "found 52", in the seven places both sides edited. `--check` rc 0 and `--selftest` rc 0 (5514 arms). No other line changed | Keeps both sides' intent: each side's count was "the steps this job carries" |

Auto-merged with no conflict and checked: `.github/ci-templates/docs.yml` (both steps present), `ci/image/command-table.json`, `docs/README.md`, `scripts/ci_events.py` (then corrected, see above), `sw/builder/test_builder.py`. The gates below cover them.

## Generated files regenerated

| File | Generator | Result |
|---|---|---|
| `.github/workflows/docs.yml` | `python3 scripts/ci_gate_workflows.py` | Regenerated, see above; `--check` rc 0 |
| `docs/reference/REGISTER_MAP.md`, `docs/diagrams/regmap/*` | `python3 scripts/gen_register_reference.py --write` | Byte-identical; `--check` fresh (203 registers, 34 modules, 240 files) |
| `docs/diagrams/memory_map.svg` | `python3 docs/diagrams/memory_map.gen.py --check` | Fresh, no write needed |
| `docs/DOCUMENTATION_AUDIT.md` | `python3 scripts/docs_inventory.py --write` | It changed: it now lists `docs/design/CSR_REGISTER_NOTES.md` (design 26 to 27 pages, total 214 to 215), and the generated page's title and sources. D0's findings on `REGISTER_MAP.md` (D0-006 to -008, -014 to -017, -057 to -060) and `REGISTER_MAP_CLASSES.md` (D0-040 to -044) now read "re-verify: quote not found": this lane removed those quotes. The status column is D0's ledger, and this round does not change it |
| `scripts/register_map_soc.json` | `python3 scripts/gen_register_reference.py --write --soc-from <export>` | It changed, in commit `c73cecf1`. See below |

### The SoC extract

The docs job runs `--check` without `--soc-from` (CI cannot run a LiteX export), so a stale extract would not fail any hosted gate. It was checked anyway, because the extract is this lane's generated file and dev changed its source.

- Export: `python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml`, then the `milan_soc.py` line `sw/litex/deploy.sh build --dry-run` prints, without `--build` and with `--output-dir`. No Vivado. About 25 s.
- At the lane parent `2c500d0a`: `--check --soc-from <its export>` rc 0, fresh (`receipts/export/parent_soc_from_check.*`).
- At the merge `57264e30`: rc 1, "STALE scripts/register_map_soc.json" (`receipts/export/merge_soc_from_check.*`).
- The difference is #842's prototype identity: `milan_station_mac_*` now `02:4B:4C:4B:4C:01`, `milan_entity_id_*`, `milan_model_id_*`, `milan_aem_image_crc32` and `csr_csv_sha256`. The page prints none of these. `--write` left the page and diagrams byte-identical.
- At the head `1de759d3`: `--check --soc-from <export>` rc 0 (`receipts/lane/gen_regref_soc_from.*`). The exports' `csr.csv` and `aem_desc.json` are in `receipts/export/`.

## Generator and its freshness gate

- `scripts/gen_register_reference.py`, unchanged this round. The docs workflow step "Register reference freshness gate" (`gate_51` at this head) runs `--check`, `--selftest` and the memory-map `--check`.
- At the head: `--selftest` rc 0, 61/61 controls; `--check` rc 0, fresh.
- Plants on a fresh clone of the head (`receipts/plants/`, each with its diff):

| Plant | rc | What `--check` says |
|---|---:|---|
| None (control) | 0 | fresh |
| Dev's hand-written `REGISTER_MAP.md` (the conflict taken to dev's side) | 1 | `STALE docs/reference/REGISTER_MAP.md` |
| `MAC_IFG` reset `0x0C` to `0x0D`, in the flop reset and the defaults ROM (`milan_csr.sv:1576`, `:2003`) | 1 | STALE, 4 files |
| The `MAC_IFG` field's signal `mac_ifg` renamed `mac_gap` (4 lines) | 1 | `STALE docs/diagrams/regmap/rtl_fingerprint.txt` |
| `A_ETH_GUARD` renamed `A_ETH_LOCK` | 2 | REFUSED: `register ETH_LOCK at 0x7D8 needs a name and a purpose` |
| Comment only: `[0] guarded` to `[0] fenced` (`milan_csr.sv:897`) | 0 | fresh. Expected: the fingerprint is over comment-stripped sources, as the PR's limitations state |

## Findings count per area

| Area | Count | State |
|---|---:|---|
| Review findings open at `2c500d0a` | 0 | Both reviews POSITIVE there |
| Merge conflicts | 3 | Resolved above |
| Semantic conflict git merged silently (`ci_events.py` step count) | 1 | Fixed in `1de759d3`, found by `gate_41` at `c73cecf1` |
| Moved-text carry (dev's `MAC_ADDR` note) | 1 | Carried onto the design notes, verbatim |
| Generated files the merge left stale | 2 | `DOCUMENTATION_AUDIT.md` and `register_map_soc.json`, regenerated |
| Suggestions and residue carried (R753-5 S1, R754-5 S1/S2; R753-3 RES2/RES3, R754-3 R1) | 6 | Unchanged, not this round's scope |
| New content or rewording | 0 | None |

## Gate table

`tools/verify_docs_yml.py 1de759d3 <run>` reads `.github/workflows/docs.yml` at the head. It exits 1 unless every `run:` step has an rc file of 0 whose log's first line names the head, or a reason in `tools/not_run.json`. Its output follows unchanged: rc 0 (`receipts/gates/verify_docs_yml.{txt,rc}`).

| Job | Step | Name | rc | Log |
|---|---|---|---:|---|
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 | `wire-accountability__ci_step_1.log` |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 | `wire-accountability__ci_step_3.log` |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 | `wire-accountability__ci_step_4.log` |
| wire-accountability | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | 0 | `docs-check-no-git__ci_step_1.log` |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 | `docs-check-no-git__ci_step_2.log` |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 | `docs-check-no-git__ci_step_3.log` |
| docs-check-no-git | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-0__ci_step_1.log` |
| docs-gates-0 | gate_1 | Build the validated HDL reference | 0 | `docs-gates-0__gate_1.log` |
| docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 | `docs-gates-0__ci_step_5.log` |
| docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 | `docs-gates-0__ci_step_7.log` |
| docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-0 | ci_step_10 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 | `docs-gates-0__gate_7.log` |
| docs-gates-0 | gate_8 | Added-line em-dash gate | 0 | `docs-gates-0__gate_8.log` |
| docs-gates-0 | gate_9 | Concise audience documentation gate | 0 | `docs-gates-0__gate_9.log` |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 | `docs-gates-0__gate_10.log` |
| docs-gates-0 | gate_11 | Product solution source-fact gate | 0 | `docs-gates-0__gate_11.log` |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 | `docs-gates-0__gate_12.log` |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 | `docs-gates-0__gate_13.log` |
| docs-gates-0 | gate_14 | Published diagram PNG gate | 0 | `docs-gates-0__gate_14.log` |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 | `docs-gates-0__gate_15.log` |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 | `docs-gates-0__gate_16.log` |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 | `docs-gates-0__ci_step_21.log` |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 | `docs-gates-0__gate_18.log` |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 | `docs-gates-0__gate_19.log` |
| docs-gates-0 | ci_step_25 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-0 | gate_21 | Bare-metal scope gate | 0 | `docs-gates-0__gate_21.log` |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-0__ci_step_28.log` |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 | `docs-gates-0__gate_24.log` |
| docs-gates-0 | gate_26 | NVM record-space gate | 0 | `docs-gates-0__gate_26.log` |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 | `docs-gates-0__gate_27.log` |
| docs-gates-0 | gate_28 | Saved-state writer gate | 0 | `docs-gates-0__gate_28.log` |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without this) | 0 | `docs-gates-0__gate_29.log` |
| docs-gates-0 | gate_30 | RTL source-list drift gate | 0 | `docs-gates-0__gate_30.log` |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 | `docs-gates-0__gate_31.log` |
| docs-gates-0 | gate_32 | Port contract gate | 0 | `docs-gates-0__gate_32.log` |
| docs-gates-0 | gate_33 | Fail-fast ratchet | 0 | `docs-gates-0__gate_33.log` |
| docs-gates-0 | gate_34 | TODO ownership gate | 0 | `docs-gates-0__gate_34.log` |
| docs-gates-0 | gate_35 | Test-evidence ratchet | 0 | `docs-gates-0__gate_35.log` |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 | `docs-gates-0__gate_36.log` |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 | `docs-gates-0__gate_37.log` |
| docs-gates-0 | gate_38 | C and C++ idiom gate | 0 | `docs-gates-0__gate_38.log` |
| docs-gates-0 | gate_39 | Python idiom gate | 0 | `docs-gates-0__gate_39.log` |
| docs-gates-0 | gate_40 | Shell idiom gate | 0 | `docs-gates-0__gate_40.log` |
| docs-gates-0 | gate_43 | Doc cited-path gate | 0 | `docs-gates-0__gate_43.log` |
| docs-gates-0 | gate_44 | Archive integrity gate | 0 | `docs-gates-0__gate_44.log` |
| docs-gates-0 | gate_45 | Per-page contents gate | 0 | `docs-gates-0__gate_45.log` |
| docs-gates-0 | gate_46 | Documentation inventory freshness gate | 0 | `docs-gates-0__gate_46.log` |
| docs-gates-0 | gate_47 | AEM store generator self-test | 0 | `docs-gates-0__gate_47.log` |
| docs-gates-0 | gate_48 | Sweep/build shape gate | 0 | `docs-gates-0__gate_48.log` |
| docs-gates-0 | gate_49 | Deploy shape gate | 0 | `docs-gates-0__gate_49.log` |
| docs-gates-0 | gate_50 | Entity shape gate | 0 | `docs-gates-0__gate_50.log` |
| docs-gates-0 | gate_51 | Register reference freshness gate | 0 | `docs-gates-0__gate_51.log` |
| docs-gates-0 | ci_step_54 | Fetch inventory dependencies | 0 | `docs-gates-0__ci_step_54.log` |
| docs-gates-0 | gate_52 | CI scheduling and evidence controls | 0 | `docs-gates-0__gate_52.log` |
| docs-gates-0 | ci_step_56 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-0 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-1__ci_step_1.log` |
| docs-gates-1 | ci_step_3 | Install the python gate dependencies | 0 | `docs-gates-1__ci_step_3.log` |
| docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs-gates-1__ci_step_5.log` |
| docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-1 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs-gates-1__ci_step_9.log` |
| docs-gates-1 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-1__ci_step_13.log` |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 | `docs-gates-1__gate_25_0.log` |
| docs-gates-1 | ci_step_15 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-1 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 | `docs-gates-2__ci_step_1.log` |
| docs-gates-2 | ci_step_3 | Install the python gate dependencies | 0 | `docs-gates-2__ci_step_3.log` |
| docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | 0 | `docs-gates-2__ci_step_5.log` |
| docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | NOT RUN | apt package index for librsvg2-bin; this host has rsvg-convert installed and no apt |
| docs-gates-2 | ci_step_8 | Install diagram gate dependencies | NOT RUN | sudo apt-get for librsvg2-bin; rsvg-convert is installed here and the venv carries wavedrom==2.0.3.post3 |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 | `docs-gates-2__ci_step_9.log` |
| docs-gates-2 | ci_step_11 | Install the pinned sv2v release | NOT RUN | sudo install into /usr/local/bin through /tmp; /usr/local/bin/sv2v is already the pinned v0.0.12 |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | `docs-gates-2__ci_step_13.log` |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 | `docs-gates-2__gate_25_1.log` |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 | `docs-gates-2__gate_41.log` |
| docs-gates-2 | gate_42 | Local act runner contract gate | 0 | `docs-gates-2__gate_42.log` |
| docs-gates-2 | ci_step_17 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
| docs-gates-2 | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| docs-check | ci_step_1 | Set CPU-derived job budgets | NOT RUN | this job has no local gate |
| docs-check | ci_step_4 | Install the pinned evidence reader | NOT RUN | installs the reader only docs-check's hosted verify uses |
| docs-check | ci_step_6 | Require every gate exactly once | NOT RUN | verifies uploaded hosted receipts; this job's gates ran above |
| docs-check | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-manifest | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step2 | Fetch inventory dependencies | NOT RUN | CI orchestration, no local gate |
| ci-manifest | step4 | Install the pinned evidence reader | NOT RUN | CI orchestration, no local gate |
| ci-manifest | ci_collect | Collect actual runtime evidence | NOT RUN | reads a hosted run's artifacts |
| ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-fail-fast | ci_observe | Observe the first failed job | NOT RUN | watches a hosted run |
| ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | NOT RUN | cancels a hosted run |
| ci-fail-fast | ci_record | Record actual job execution | NOT RUN | records GitHub's own step results; needs the hosted step context |
| ci-cancel-tail | step1 | Set CPU-derived job budgets | NOT RUN | CI orchestration, no local gate |
| ci-cancel-tail | step2 | Cancel confirmed terminal failures | NOT RUN | cancels a hosted run |

66 steps ran, 31 not run with a reason, 0 bad

Key lines: `gate_7` docs_check 0 findings across 215 md files. `gate_8` em-dash 0 findings over 5,792 added lines, `[0a75aa77..HEAD]`. `gate_9` "documentation style: OK (25 current documents)". `gate_43` 1,646 cited paths resolve. `gate_45` TOC OK, 152 pages. `gate_46` inventory fresh, 60 controls. `gate_51` register reference fresh, 61/61. `gate_41` ci_events 5,514 arms PASS. The builder legs print "ALL GATES PASS EXCEPT 1 NOT RUN" and "... EXCEPT 16 NOT RUN", the same internal arms as round 6. Every job's clone ended at the head with an empty status (`receipts/gates/*__tree-after.txt`).

The four jobs `docs-check`, `ci-manifest`, `ci-fail-fast` and `ci-cancel-tail` verify uploaded hosted receipts or cancel runs, so they run only on GitHub. `Record ...` and `Retain checkout identity` read the hosted step context. `Install ...` (apt, sudo) and `Resolve exact package downloads` are covered by the venv and the host's pinned `sv2v` and `rsvg-convert`.

## Lane checks

On a fresh clean clone of `1de759d3` with each submodule at its pin (`tools/clone_at.sh`). Logs and rc files: `receipts/lane/`.

| Check | rc | Result |
|---|---:|---|
| `git diff --check 0a75aa77 HEAD` (the merge base) | 0 | |
| `git diff --check 1f29f189 HEAD` (the old base) | 0 | |
| `git diff --check 2c500d0a HEAD` (the lane parent) | 0 | |
| `git merge-base --all 0a75aa77 HEAD` | 0 | one line, `0a75aa77` |
| `scripts/docs_inventory.py --check` | 0 | "documentation inventory: OK (548 lines, docs/DOCUMENTATION_AUDIT.md is fresh)" |
| `scripts/docs_inventory.py --selftest` | 0 | 60 controls |
| `scripts/check_doc_style.py` | 0 | "OK (25 current documents)" |
| `scripts/check_doc_style.py --selftest` | 0 | OK |
| `scripts/gen_register_reference.py --check` / `--selftest` / `--check --soc-from <export>` | 0 | fresh / 61/61 / fresh |
| `docs/diagrams/memory_map.gen.py --check` | 0 | fresh |
| `scripts/ci_gate_workflows.py --check` | 0 | |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed, 0 skipped |
| Clone status after all of the above | | empty (`clone_status_after.txt`) |

**The style gate on every page the merge touched.** `check_doc_style.py` takes no path; it judges its `DOCUMENTS`. The merge touched 52 Markdown pages: 47 against the lane parent and 8 against dev. 18 of them are in `DOCUMENTS`, and the gate passes on all 25 of its documents. The other 34 are outside the rule, which this sync does not widen. List: `receipts/lane/style_scope.txt`.

## How the gates ran

- Runner and verifier: `../829-a725c/receipts/gates/tools/run_docs_yml.py` and `verify_docs_yml.py`, copied to `tools/`. The only edits are the lane path, the venv path and the scratch HOME path.
- `tools/not_run.json` differs from 829's in one entry. The bare `ci_step_54` key named "Record executed gate outcomes" at 829's head. At this head `ci_step_54` is "Fetch inventory dependencies", and the record step is `docs-gates-0/ci_step_56`. Left as it was, the runner would have skipped the fetch and run the hosted-only record. The key now names `docs-gates-0/ci_step_56`.
- Each job ran on its own fresh clone of `1de759d3` (`git clone --shared` of the lane, checked out detached, status asserted empty), one `bash -e` script per `run:` step, its output written to a file and never piped. Two chains, by `tools/run_all_jobs.sh`: docs-gates-0, docs-gates-1 and docs-gates-2 in turn; and wire-accountability then docs-check-no-git beside them.
- Venv: Python 3.14 with pyyaml, wavedrom 2.0.3.post3, the hash-pinned `tools/markdown` and `tools/hdl_reference` requirements, and behave (for `tests/`). The pinned RV32 SDK was installed once into the scratch HOME by `scripts/ci_rv32_sdk.py` (verified), so both builder jobs read a verified cache and never install at once.
- Earlier runs, not receipts for this head:
  - On the merge `57264e30`: stopped after 4 minutes, once the SoC extract showed stale. Its clones were left alone.
  - On `c73cecf1`: complete. 66 steps ran and 65 gave rc 0. `docs-gates-2/gate_41` gave rc 1, the step-count fault above. Its verifier output is kept as `receipts/earlier_run_c73cecf1/verify_docs_yml.txt`, with the failing log. In that run two builder-heavy jobs overlapped, and the unit's `memory.peak` reached 8.9 GB against the 12 GB cap. That is over the 8 GB target, so this run puts the three docs-gates jobs in one chain.
- Memory in this run: the three docs-gates jobs ran one after another. The unit's highest `memory.current` in 5-second samples was 7.9 GB, at 10:17, inside docs-gates-0's "Saved-state writer gate" (`gate_28`) running alone (`receipts/gates/memory_max_5s.txt`). That is under 8 GB, with little margin. The `memory.peak` column of `memory.txt` is the unit's peak since it started, so it still shows the earlier run's 8.9 GB.
- The launcher's last `wait` also waited on its own memory loop, which stops only when `ALL_DONE` exists. So after every job's `DONE` file existed and no job process was left, `ALL_DONE` was written by hand. That happened for this run and for the `c73cecf1` run. `tools/run_all_jobs.sh` now waits on the two chains only, and says so.

## Lane state at the end

`git status --porcelain` in the lane is empty. The lane's `gptp-processor` and `protocol-processor` checkouts were moved to the merged pins (`1616fc8f`, `92100657`) by `git submodule update`. Before that, each was confirmed as its own top level, with the origin `.gitmodules` names and an empty status. Live `origin/dev` and `origin/797-r1-regref` were read at the end: `0a75aa77` and `2c500d0a`. Nothing is pushed.

## Open risks

1. Dev may move again before merge; the candidate merge result is validated only against `0a75aa77`.
2. The SoC extract's freshness is checked only with a local export; no hosted gate runs `--soc-from` (unchanged limitation).
3. The D0 inventory still marks `REGISTER_MAP.md` and `REGISTER_MAP_CLASSES.md` stale, with "re-verify: quote not found" on the findings this lane fixed. D0's ledger owns that status; this sync does not edit it.
4. The `c73cecf1` run's memory peak exceeded the 8 GB target, as stated above.
5. Not run: Verilator suites, Yosys, the read-table sweep, hardware, Vivado. This is a documentation lane, and the sync changes no RTL in this PR's diff.
6. Other literal counts that both sides could have bumped identically were not hunted by hand. The full docs workflow at the head is the evidence that none remains in its scope.
