[R249] POSITIVE - exact head e122f3302cf8a8e89de960233a8638b9dd1387dc

# R249-3: internal independent review of PR #566 (issues #400 and #403), round 3

- **Round:** R249-3. Cleared context, own detached clone, delta review.
- **Exact head:** `e122f3302cf8a8e89de960233a8638b9dd1387dc`, tree `59497ea361687e8d49e468bc884f220a418680b5`.
- **Delta judged:** `7463ab08..e122f330`, which is two commits: `de36e514` and `e122f330`. That is 17 files, +137/-36. My R249-2 review covered `864b36f5..7463ab08` in full.
- **Authority, in the order read:**
  - AGENTS.md and CONTRIBUTING.md.
  - docs/README.md.
  - The #400 body and every comment on it. The binding comments are decisions 5770922734 and 5781042070, the 2026-09-23 owner decision 5789766951, resume 5831927176, round-2 order 5832912970, and the round-3 assignment and F2 decision 5834690477, along with A319's REVIEW READY 5836209846.
  - `docs/testing/CI_WORKFLOWS.md` (per-suite budget table).
  - The delta and its history.
  - Public evidence: the tree `a94b8b81:review-evidence/400-403-r1`, used only for my own R249-2 mutant definitions, and the hosted checks at this head.
- **Ordering:** my own round-2 findings were read only after my independent pass over the delta. The other reviewer's round-2 findings were read after that pass and after my verdict, findings and ledger were settled. Their resolution is in its own section below. See also "Real limits" for one disclosure about ordering.
- **Verdict basis:**
  - All four of my R249-2 findings (F1 BLOCKER; F2, F3, F4 MINOR) are closed at this head, with executable evidence.
  - All three findings of the other reviewer's round 2 are closed.
  - No new BLOCKER, MAJOR or MINOR was found.
  - All five lenses are CLEAN at this exact head.
  - Two SUGGESTIONs are recorded. They do not affect coverage.

## Round-2 findings: closed or retained at this head

### R249-2 F1 (BLOCKER; Tests, Conformance): `nvm_cosim` crashed on a stale `constants_header()` caller. **CLOSED.**

- `tb/verilator/nvm_cosim/run_cases.py:110,132` now reads `lwsrp_table.json` next to the overlay. It passes `ref.fabric_constants(overlay, lwsrp)` into `constants_header`.
  - `ref.fabric_constants` is the object `test_nvm_firmware.py:85` imports from `sw/litex/boot_policy.py`.
  - I checked that in the interpreter: `ref.fabric_constants is boot_policy.fabric_constants` is `True`.
  - So the suite uses the one shared derivation, the same as `test_nvm_firmware.py:228` and `milan_soc.py:3950`.
- `make -C tb/verilator/nvm_cosim quick` exits 0 with `315 checks: 315 PASS` in 28.1 s (receipt `05`).
- `make -C tb/verilator/nvm_cosim run` covers both shapes plus the mutants. It exits 0 with `465 checks: 465 PASS` and `39 of 39 mutant(s) killed by their named check`, in 348.9 s (receipt `06`).
- **Caller census:** I ran `git grep --recurse-submodules` over the whole tree for `constants_header` and `fabric_constants` (receipt `07`).
  - Each has exactly one definition: `test_nvm_firmware.py:166` and `boot_policy.py:35`.
  - `constants_header` has two callers, both passing the derived mapping.
  - Every `fabric_constants` caller passes `(overlay, lwsrp)`.
  - The round-3 delta adds no changed signature. Its only new `def`s are in the new `tb/common/gen_declaration_fixture.py`.
  - No stale caller remains.
- **Hosted:** see "Hosted evidence".

### R249-2 F2 (MINOR; Tests, Docs): discriminating legs existed only outside the repository. **CLOSED.**

This was answered under decision 5834690477 (the durable option).

- **Committed fixtures:**
  - `tb/verilator/pp_shadow/fixtures/vid73.yaml` sets `emitter_srp_vid: 73`.
  - `tb/verilator/pp_shadow/fixtures/crf_on.yaml` sets `clocking.crf_output.enabled: true`.
  - `tb/verilator/csr/fixtures/reset_bits.yaml` sets both `srp.*_at_reset: true`.
  - All three use base `configs/endstation_arty_current.yaml`.
- **Default targets run them:**
  - pp_shadow: `run: run-base run-vid73 run-crf` (`tb/verilator/pp_shadow/Makefile:134-152`).
  - csr: `run` ends with `$(MAKE) reset-bits` (`tb/verilator/csr/Makefile:134-142`).
  - The hosted runner calls the default goal: `make -C "$d"` at `scripts/run_all_suites.sh:390`.
- **Headers are generated, not edited.** `tb/common/gen_declaration_fixture.py` loads the base, applies the leaf overrides and writes `config.yaml`. It then runs the real `eb.load_config()` and calls the builder's own `emit_adp_shape_svh(cfg)` and `emit_csr_defaults_svh(cfg)`, the same emitters `_derive_artifacts` uses at `endstation_builder.py:5571-5572`.
  - Nothing generated is committed. `obj_*/` is ignored (`.gitignore:98`), and the tree stays clean after runs (receipt `91`).
- **The fixture headers are the ones compiled.** Verilator's own dependency files show it (receipt `03`):
  - `obj_vid73`, `obj_crf` and `obj_reset` compiled `obj_*/fixture/gen/{adp_shape_defaults,lwsrp_csr_defaults}.svh`.
  - The base legs compiled the tracked `configs/generated/endstation_arty_current/gen/adp_shape_defaults.svh` and `hdl/common/csr/gen/lwsrp_csr_defaults.svh`.
- **Each fixture changes exactly what it claims** (receipt `04`). Compared with the tracked headers:
  - vid73 changes only `LWSRP_VID_RST_C` (0x49) and `ADP_SRP_DOM_DEF_VID_C` (73), plus the Source comment.
  - reset_bits changes only `LWSRP_CTRL_RST_C` (0x10 to 0x13).
  - crf_on changes only `ADP_TALKER_SRC_C` (2), `AEM_NAME_ENTRIES_C`, `ADP_TALKER_CAPS_C` (MEDIA_CLOCK_SOURCE) and a two-row `ADP_STROUT_PRES_NS_C`.
  - The unmodified vid73 base otherwise reproduces the tracked header byte for byte, so the YAML round trip through `obj_*/fixture/config.yaml` is faithful.
- **Expectations are independent literals in the recipes:**
  - `-DDECLARATION_VID=73` and `-DDECLARATION_OUTPUTS=2` (pp_shadow).
  - `-DCSR_SRP_RESET_BITS=3u` (csr).
  - These feed `pp_shadow/sim_main.cpp:627-654,1564-1570,1640` and `csr/sim_main.cpp:111-114,385-387,816`.
  - A fixture typo or a dropped override therefore turns red rather than green.
- **Mutants against the DEFAULT targets** (`make -C tb/verilator/{pp_shadow,csr}`, no target named). Each was applied to a disposable copy at this head and restored with a SHA-256 check (`scripts/run-mutants.sh`, `scripts/mutate3.py`, receipts `mutants/`):

| ID | Mutant | Default target | Exit | Failing checks |
|---|---|---|---:|---|
| m41 (= R249-2 receipt 41) | drop `.SRP_DOM_DEF_VID_P (SRP_DOM_DEF_VID_P)` in `KL_pp_shadow.sv:1056` | pp_shadow | 2 | 3 VID checks in run-vid73, `got=0x00030002 exp=0x00030049` |
| m43 (= receipt 43) | drop `.SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C)` in `milan_datapath.sv:7410` | pp_shadow | 2 | same 3 |
| m35 (= receipt 35) | `lwsrp_ctrl <= LWSRP_CTRL_RST_C & ~32'h3` in `milan_csr.sv` | csr | 2 | reset-bits leg: both admission outputs `got=0x0 exp=0x1` |
| m60 | drop `.DOM_DEF_VID_P (SRP_DOM_DEF_VID_P)` in the processor top `:2226` | pp_shadow | 2 | same 3 |
| m65 (= other reviewer's R7b) | `KL_srp_top.sv:341` `.DEF_VID_P (16'd2)` | pp_shadow | 2 | same 3 |
| m61 | builder emits `ADP_SRP_DOM_DEF_VID_C = 16'd2` | pp_shadow | 2 | same 3 |
| m62 | builder drops `talker_declare_at_reset` from `LWSRP_CTRL` | csr | 2 | readback `0x11` vs `0x13`, arm output, `LWSRP_CTRL(reset)` |
| m63 | builder stops counting the CRF output in `talker_stream_sources` | pp_shadow | 2 | run-crf: `#403 declared output count` 1 vs 2, boundary status and destination |
| m64 | `o_lwsrp_talker_en` stuck at 0 | csr | 2 | `declaration boot SRP arm output`, `o_lwsrp_talker_en` |

  With every mutant restored, both default targets pass again: pp_shadow 3 x 402 checks; csr 391/391/110/44/391/391 (receipts `15`, `16`). Every hop of the generated-VID path now has a durable regression: builder, datapath, wrapper, processor top and child. So do the CRF-on exact count and both live reset bits.
- **Wall clock:** I timed a cold, clean default target on this host (receipts `01`, `02`):
  - pp_shadow: 52.7 s (author: 18.5 to 52.7 s).
  - csr: 36.0 s (author: 30.5 to 35.1 s).
  - `CI_WORKFLOWS.md:156-159` gives both suites the 1800 s per-suite budget. No deadline changed.
  - Hosted, csr took about 66 s including its build (shard 3/5 timestamps 17:02:47 to 17:03:53).
- **Harness comments:** `pp_shadow/sim_main.cpp:625-626` and `csr/sim_main.cpp:103-104,750` now describe recipes that exist.

### R249-2 F3 (MINOR; Docs, RTL): RTL contract comments. **CLOSED.**

- **`hdl/common/csr/milan_csr.sv:1542-1543`** now reads "Neutral disabled reset: enable=0, bypass=0, VID=0." That matches `AAF_CTRL_RST_C = 32'd0` at `:1207`.
- **`:1548-1550`** now say the lwSRP startup VID is 2 and the separate neutral AAF VID is 0, and that MAAP resets disabled with count 0. That matches `MAAP_CTRL_RST_C = 32'd0` at `:1208` and the builder's VID-2 rule at `endstation_builder.py:1934`.
- **`hdl/milan/milan_datapath.sv:274-275` (`MAAP_P`)** says "The builder requires MAAP for every supported configuration; numeric stream_dmac_base values are legacy scratch". That matches the unconditional refusal at `endstation_builder.py:3208-3214`.
- **`:299-301` (`RXFILT_P`)** now says presence is selected independently by `board.features.rx_mac_filter` and that the policy stays promiscuous. That matches `endstation_builder.py:386-392,3225`.
- **Stale strings:** `git grep -E 'bypass=1|rx_address_filter' -- hdl` is empty (receipt `08`).
- **Comment-only:** every changed `.sv`/`.cpp` line in the delta is a comment (receipt `14`). The RTL behaviour I covered at `7463ab08` is therefore unchanged, and so is the zero OOC area delta.

### R249-2 F4 (MINOR; Docs): as-built documents. **CLOSED.**

- **`docs/design/MAAP_FABRIC.md:83-84`** gives reset `0` with no default count.
- **`:151-153`** says the firmware claims exactly the declared Stream Outputs, with CRF included only when its output is declared. That matches REGISTER_MAP `0x6CC` (`docs/reference/REGISTER_MAP.md:1242`).
- **`PRES_DFLT_C`:** `tb/verilator/milan_dp/README.md:683-684` and `sim_main.cpp:1330` now name `ADP_STROUT_PRES_NS_C`. `git grep PRES_DFLT_C` is empty.
- **`docs/ENDSTATION_BUILDER.md:1018`** says "71 rows", and section 3 holds 71 numbered rows (0 through 44 with lettered rows).
  - The historical convention counts every row including row 0: `89cd95ee` stated 66 and held 66, and `d72c4a4f` stated 58 and held 58.
  - The base's "66" against its 67 rows was drift that predates this PR.
- **Also verified** (in the assignment, and R250-2 F3):
  - `docs/design/AREA_BUDGET.md:41` now reads "never in supported configurations; every declared talker requires MAAP".
  - The `--no-maap` help at `sw/litex/milan_soc.py:3464-3470` says the flag is unsupported by the builder and that numeric `srp.stream_dmac_base` is legacy scratch.
  - `git grep -i 'statically provisioned'` now hits only the historical sentence in `MAAP_FABRIC.md:4` and the KL_maap integration note, both accurate descriptions of `en = 0`.

### R249-2 S1 (SUGGESTION; Conformance): `boot_policy.py` literals. **RETAINED as SUGGESTION.**

Out of scope under 5834690477 and routed to #495. It does not affect coverage.

## Other reviewer's round-2 findings (R250-2)

- **F1 (BLOCKER; Tests), `nvm_cosim`:** closed. The evidence is the same as R249-2 F1 above: both shapes, 39/39 mutants, and the caller census.
- **F2 (MINOR; Tests), no committed recipe for the discriminating legs:** closed.
  - Their R1 is my m43. Their R7b is my m65, which is now detected by the default target. It was previously invisible to both gate 40 and `make`.
  - Their "preferably shape/reset legs": the reset legs are in `csr` `reset-bits`. The shape legs were not required by the decision (5834690477 names distinct-VID, CRF-on and nonzero reset bits). `csr` already elaborates 1x1, 4x4 and 8x8 headers in its default target.
- **F3 (MINOR; Docs), five items:** closed.
  - Item 1 (`milan_csr.sv`), items 3 and 4 (the `milan_datapath.sv` banners) and item 2 (`MAAP_FABRIC.md`) are covered under R249-2 F3 and F4 above.
  - Item 3 (`AREA_BUDGET.md:41`, `milan_soc.py` help) and item 5 (`PRES_DFLT_C`) are covered under F4 above.
- **S1 (SUGGESTION; Tests, Conformance), timer instance override:** out of scope, routed to #495 by 5834690477. Not re-measured.

## New findings at this head

No BLOCKER, MAJOR or MINOR.

### S2 - SUGGESTION - Docs, Tests - `tb/verilator/csr/README.md:19-33`, `tb/verilator/pp_shadow/README.md:4`, `tb/verilator/csr/Makefile:4-23`

- **Evidence:** the suite READMEs and the csr Makefile banner still describe what `make` runs, and neither mentions the new default legs:
  - The csr README says "`make` builds and runs **three** self-checking harnesses". Its table lists `sim_live`, which was deleted, and omits `obj_100m`, `obj_gptp`, `obj_pps` and now `obj_reset`.
  - The pp_shadow README quotes "371 checks" for one executable. `make` now runs three executables of 402 checks each.
  - Both documents were already stale at base `864b36f5`, before this PR's legs existed. The Makefile recipes and harness comments, which the round-2 finding named, are accurate.
- **Impact:** a reader of the README under-reads the default coverage. No gate or behaviour is affected.
- **Suggested outcome:** a follow-up issue refreshes both run sections from the recipes, without quoting check counts.
- **Verification:** reread the two sections against `make -n`.

## Robustness of the new test machinery

These are the checks behind the Robustness lens. The artifacts are `tb/common/gen_declaration_fixture.py:21-50` and the recipes above.

- **Post-validation VID injection.**
  - `eb.load_config()` validates the unmodified shipping VID 2. Only then does the script set `cfg["srp"]["vid"] = 73`, guarded by `type(vid) is int and 1 <= vid <= 4094 and vid != 2`.
  - Both emitters read `cfg["srp"]["vid"]` at emission time: `endstation_builder.py:2166` through `srp_reset_words()`, and `:2913`. No derived copy is made at load time; receipt `04` shows exactly the two VID constants change.
  - **This cannot mask a builder defect.** A defective emitter or binding produces 2, not 73, and turns the leg red (m61). A defect in the load-time VID handling cannot be observed on any legal config, because 2 is the only legal value. A future emitter that read a load-time-derived copy would fail loud, not green.
  - Refusal of a non-2 VID remains the declaration gate's job (`sw/builder/test_declarations.py`, 26 refusals, R249-2 receipt 10). The fixture docstring states that division.
- **Malformed fixtures fail loud or red.**
  - A missing `base` raises `KeyError`.
  - A dict override onto a scalar raises.
  - An unknown or typo'd key leaves the base config in place, and the independent `-D` expectation fails.
- **Parallel and clean behaviour.**
  - Each leg has its own `--Mdir` (`obj_vid73`, `obj_crf`, `obj_reset`), and none writes files into the working directory.
  - `clean` removes all three.
  - The generated outputs are ignored, and the tree is clean after runs (receipt `91`).
- **Warning posture.**
  - Every added `-CFLAGS` group carries `-Wall -Wextra`, and `scripts/check_cpp_idiom.py` passes: "build without warnings: 0 <= 0" (receipt `09`).
  - pp_shadow keeps warnings fatal, and all three legs build without a warning.

## Static gates run at this head (disposable copy)

- `check_py_idiom.py` 0.
- `check_cpp_idiom.py` 0.
- `check_doc_style.py` 0.
- `check_doc_paths.py` 0: 847 paths.
- `gen_toc.py --check` 0.
- `check_em_dash.py --base 864b36f5` 0: 0 findings over 57 added Markdown lines.
- `git diff --check 7463ab08 e122f330` 0.
- No U+2014 on any added line in the delta.

Receipts `09` to `13`. The TOC and em-dash gates used a pre-existing pinned Markdown-renderer environment. Nothing was installed.

## Packet

- **Scripts:**
  - `scripts/run-focused.sh` reproduces receipts `01`-`03`, `05`, `06` and `09`-`14`.
  - `scripts/run-mutants.sh` with `scripts/mutate3.py` reproduces `mutants/`.
  - `scripts/verify-clone.sh` reproduces `90` and `91`.
- **Self-describing receipts:** `04` (fixture header diffs), `07` (caller census), `08` (stale-text searches) and `20` (hosted check runs and suite-log extracts) carry their own section headers.
- **Path placeholders:** host paths in the logs are replaced by `<packet>`, `<probe-tree>`, `<clone>` and `<verilator-5.050-root>`.
- **Manifest:** `MANIFEST.sha256` lists every published file.

## Hosted evidence at this exact head (manager owns acceptance)

- **Run `36164202471`**, `pull_request` on the merge ref `cbcfd172e29c35fabddff236c3710e3371e85bc5`, which is the PR head merged onto dev and not the exact head tree.
- **Executed and succeeded:** `Verilator shard 0/5`, `2/5` and `3/5`.
  - Shard 3/5 includes `PASS csr` with the `declaration fixture: reset_bits.yaml` leg in its suite log (`suite-logs-3` artifact).
- **Also succeeded:** `rtl-fast`, `verilator-lint`, `elaborate`, `yosys-elaboration`, Yosys shards 0-3/4, `docs-check`, `docs-check-no-git`, `bdd-conformance`, `wire-accountability`, `full-ci-gate` and `changes`.
- **Skipped, not a result:** `Physical gPTP (nightly and manual)`.
- **Completed later and succeeded** (receipt `20`, observed 17:37 UTC):
  - `Verilator shard 1/5`: 21 of 21 suites.
    - `PASS nvm_cosim` with `465 checks: 465 PASS` and 39/39 mutants killed. This is the shard where it failed at `7463ab08`.
    - `PASS pp_shadow`, whose suite log shows three `402 checks, 0 failures` tallies, including `declaration fixture: vid73.yaml` and `crf_on.yaml`.
  - `Verilator shard 4/5`: `PASS milan_dp`.
  - The aggregate `verilator-suites` and `yosys-portability` both succeeded.
- **Hosted wall clocks** from shard timestamps: `pp_shadow` about 128 s, `csr` about 66 s and `nvm_cosim` about 706 s, each against the 1800 s per-suite budget.
- My local runs of `nvm_cosim` (quick and full), `pp_shadow` and `csr` at the exact head all pass.

## Completion ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | decisions 5770922734 / 5789766951 / 5834690477 against the committed legs: generated-VID hops builder -> `milan_datapath.sv:7410` -> `KL_pp_shadow.sv:1056` -> processor top `:2226` -> `KL_srp_top.sv:341` (m41/m43/m60/m61/m65), live reset bits (m35/m62/m64), exact CRF-on count (m63); `run_cases.py:110,132` shared derivation; nvm_cosim quick/full; comment-only RTL delta (receipt 14) | R249-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| RTL | CLEAN | `milan_csr.sv:1207-1208,1542-1552,2776-2777`; `milan_datapath.sv:267-301,7410`; `KL_pp_shadow.sv:1056`; processor `protocol_processor_top.sv:2226`, `KL_srp_top.sv:341` at pin 990f9652; delta comment-only (receipt 14); fixture include resolution (receipt 03) | R249-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| Robustness | CLEAN | `tb/common/gen_declaration_fixture.py:21-50` (post-validation injection, guard, malformed fixture), `endstation_builder.py:2166,2913,5571-5572`; recipe isolation `pp_shadow/Makefile:134-156`, `csr/Makefile:134-145`; `.gitignore:98`; receipts 03, 04, 91 | R249-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| Tests | CLEAN | default `make -C tb/verilator/{pp_shadow,csr}` (receipts 01, 02, 15, 16); 9 mutants all red on default targets (receipts mutants/); nvm_cosim quick 315/315 and run 465/465 + 39/39 mutants (receipts 05, 06); caller census (receipt 07); hosted `verilator-suites` success with nvm_cosim, pp_shadow (3 legs) and csr (reset-bits leg) passing (receipt 20) | R249-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |
| Docs | CLEAN (S2 SUGGESTION only) | `MAAP_FABRIC.md:83-84,151-153`; `AREA_BUDGET.md:41`; `ENDSTATION_BUILDER.md:1018` (71 rows counted); `milan_soc.py:3464-3470`; `milan_dp/README.md:683-684`, `milan_dp/sim_main.cpp:652,659,1330`; harness comments `pp_shadow/sim_main.cpp:625-626`, `csr/sim_main.cpp:103-104,750`; doc gates (receipts 08, 10-13) | R249-3 | e122f3302cf8a8e89de960233a8638b9dd1387dc |

Every lens was applied again at this exact head. That includes Robustness, which my R249-2 round had covered at `7463ab08`, because the delta adds new test machinery within its scope.

## Real limits

- **Not run here, per the brief:** the complete builder, parent, PP, gPTP and Yosys banks; `scripts/run_all_suites.sh`; `act`; behave; the `milan_dp` recipe; the final current-dev candidate; hardware. Physical calibration was NOT RUN. Field skips are not hardware proof.
  - The `milan_dp` sources changed only in comments (receipt `14`), and its README was read, not executed.
- **Tool path:** the tool path named in the brief (`.../372-manager-candidate1/pinned-tool-bin/verilator`) does not exist on this host. I wrote my own wrapper to the same pinned Verilator 5.050 installation and recorded its identity and binary hashes (receipt `00`). The hosted runs also use v5.050.
- **Job cap:** the recipes' `--build -j 0` uses all cores during each Verilator build. The mutants ran sequentially, one suite at a time.
- **Ordering disclosure:** my first attempt to write the draft report with verdict and ledger failed for a file-tool precondition. The other reviewer's round-2 report was read before the retry succeeded. My verdict, findings and ledger had been settled from my independent pass before that read. The only work that followed from it was the extra child-hop mutant m65, which is now in the table and detected.
- **Hosted:** hosted results are recorded as observed. They ran on GitHub's merge ref `cbcfd172`, not on the bare head tree. The manager owns their acceptance.
- **Clone integrity:** the review clone was never modified; all probes ran in a disposable copy. At the end, HEAD, tree, index tree, worktree bytes/modes, clean status and the gitlinks `990f9652`, `e5dcea6e` and `48ff7a7e` all matched the head (receipt `90`). The probe copy also verified clean after every mutant was restored (receipt `91`).

## Pending manager duties

- Every executed hosted context succeeded at this head; `Physical gPTP` was skipped, which is not a result.
- Still owed:
  - hosted and act acceptance of this head's contexts;
  - the final current-dev candidate (source base `864b36f5`, live dev `5c78ce2e`);
  - candidate-merge validation, merge authorization, post-merge containment and issue closure.
- R250 remains the external reviewer for this round.
- #495 owns R249-2 S1 and R250-2 S1. S2 above is offered for a follow-up issue.

R249-3 FINISHED
