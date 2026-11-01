# A725c HANDOFF: round 2 of PR #831, gPTP plane on the MII port (#829)

PRIVATE. Nothing pushed. Receipts are under `receipts/`, indexed in `receipts/INDEX.md`, generated from the files present. Questions for the manager are in `QUESTIONS.md`.

## Status

| Item | State |
|---|---|
| TAKEN on #829 | posted, issuecomment-6561891388 |
| REVIEW READY on #829 | posted, issuecomment-6563126522 |
| `829-mii-gptp` | `2d534bec9348557a9407d3024c0b199c0ebc8bce`, clean, on `4cda0aa0`, 10 commits, not pushed |
| Base | live `dev` `1f29f189`, read unchanged at the end of the gates |
| Bench branches in this clone | untouched |
| RTL behaviour | unchanged: comment-only, shown below. No bench, flash or route was needed |

## How round 1's "documentation gates rc 0" came to be false

Round 1 ran three steps of `.github/workflows/docs.yml` by hand: `docs_check.py`, `gen_toc.py --check` and `check_gptp_docs.py` (its receipts `gates/docs.rc`, `toc.rc`, `gptpdocs.rc`). It reported them as "Documents" in the handoff, and the REVIEW READY called them "the documentation gates". `check_doc_style.py` is a line of `gate_9` and `check_cpp_idiom.py` is `gate_38`, in the same workflow. Neither was run. So the claim described a list the author chose, not the workflow.

**Why it cannot recur from this runner.** `gates/run_docs_yml.py` takes its steps from `docs.yml` in the clean clone it just made, and `gates/verify_docs_yml.py` reads the workflow at the head and exits 1 unless each `run:` step has an rc file of 0 whose log's first line names this head, or an entry with its reason in `gates/not_run.json`. The table below is that script's output pasted in, so a row cannot be left out without the check going red. Copies are in `receipts/gates/tools/`. A manager can re-run the check against any head.

## Findings closed

Each row is at head `2d534bec`.

| Finding | Fix, file:line | Commit | Verification |
|---|---|---|---|
| R761-F1, R762-F1: style gate red | `docs/design/GPTP_PLANE.md:276-375`, `CHANGELOG.md:11,56-71`, reworded, every figure kept | `7bb7f2e6` | `check_doc_style.py` and `--selftest` rc 0, log `docs-gates-0__gate_9.log` |
| R761-F2, R762-F2: idiom ratchet red | `tb/verilator/gptp_txts/Makefile:90`, `-Wall -Wextra` on the MII group; ratchet not raised (`git diff 4cda0aa0 HEAD -- scripts/` is empty) | `43ab0c16` | `check_cpp_idiom.py` rc 0, `build without warnings: 0 <= 0`, log `docs-gates-0__gate_38.log` |
| R761-F3, R762-F7: GMII `ready` called a constant | `sw/litex/milan_soc.py:2085-2087` (and `:2078-2082`, the older `sink.ready` sentence), `docs/design/GPTP_PLANE.md:286-290`, `CHANGELOG.md:65-68`, `hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv:35-36` and `:363-366`, `sw/builder/test_builder.py:18265-18267`; PR change table. "Cannot move" is gone | `0dbc4c42` | Read against the generated chain, `mac_tx_chain.v:2239-2241` (flop set to 1, cleared by `eth_tx_rst`) and `:2600-2601` (`maceth_tx_rst` follows `eth_tx_rst` by two clocks), and R761's `ax-export-ready-lines.txt` for the AX7101 export |
| R761-F4, R762-F8: fragment check could not fail on MII | `tb/verilator/gptp_txts/sim_main.cpp:951`; control `mii_delta_forced_not_measured`, `mutants.py:111` | `b4e9a1a1` | `receipts/fragment/`: under the old check that defect leaves 95 of 95 green, rc 0; under the new one it fails the named check, rc 2. Caught in `gates/gptp_txts-all.log` |
| R761-F5, R762-F3: PHC arm missed the window's early end | `sim_main.cpp:556` (`pad_at_first_symbol`), `:970-971`, `:977-1020`; `kGuardReloadCyc` `:105`, `:107`; controls `mutants.py:95`, `:103` | `19f66a10` | `receipts/guard/guard-probe.txt`, planted values on the MII build: 203 passes; 189 to 202 fail the reload check; 188 and under also fail `phc window, first symbol: that frame's own result is an explicit loss`. Controls at 170 and 202 caught in `gates/gptp_txts-all.log` |
| R761-F7, R762-F5: check's name false on MII | `sim_main.cpp:92`, `:96`, `:884`; anchor `mutants.py:76`; also the suite's `README.md` | `d797b7e4`, `2d534bec` | All 13 controls caught under the new names, `gates/gptp_txts-all.log` |
| R762-F4: no gate holds the datapath's shape wiring | `sw/builder/test_builder.py:18305` (`DATAPATH_SHAPE_WIRING`), `:18345` (gate 1h), registered `:29396` | `194f71f2` | `receipts/wiring/`: `shipped.rc` 0 with 7 of 7 planted cuts rejected; the real cut of `.ETH_TICK_NS_P` or `.ETH_CYC_PER_OCTET_P` from `milan_datapath.sv` fails the gate by name, rc 1 each. It is a text gate like its neighbours 1d and 1g, not an elaboration |
| R761-F6, R762-F6: figures | 10 controls at `4cda0aa0`; 13 at this head; 14 on the bench branch (`7fa8332e`). PR body, this file, REVIEW READY. Comment 6561285235 cannot be edited | not a commit | `receipts/ax7101/checksum-comparison.txt`: 126 of 126 equal, with each route's head and what it covers. `gates/gptp_txts-all.log` ends `controls: 13 failures: 0` |
| R761 RES1, R762-R4 | `sim_main.cpp:14-15` | `9cea8806` | Read: "at 80 MHz and at 100 MHz" |
| R762-R1 | `KL_gptp_gmii_launch.sv:150-153`, `milan_soc.py:2092-2096` | `9cea8806` | Read against `gen_mac_tx_model.py:253-255`; `gen_mac_tx_model.py --check` rc 0 with the region unchanged |
| R762-R2 | `GPTP_PLANE.md:339-340`, `KL_gptp_shadow.sv:91-93`, PR limitations | `9cea8806` | Read |
| R762-R3 | PR bench table only | not a commit | Polled `PDELAY_NS`: `f-07` 631 to 665, `f-10` 631 to 675, `f-11` 639 to 668. Row means 650 to 654 |
| R761 S3 | PR body and the texts I post now cite IEEE 802.1AS-2020 11.3.9. The RTL banners, `KL_gptp_gmii_launch.sv:100` and `KL_gptp_txret.sv:70`, already did | not a commit | Read in the standard: 11.3.9 "Event message timestamp point", "the beginning of the first symbol following the start of frame delimiter". 8.4.3 is the generation of timestamps and the correction to the reference plane. 11.3.2 only lists message types and was the wrong citation. Round 1's comments keep it, since they cannot be edited |
| R761 S6 | `mutants.py:43-44`, `:256-257` | `ebe97d08` | After the full run neither `obj_dir/Vgptp_txts_sim` nor `obj_mii/Vgptp_txts_sim` exists |

## Reviewer items not taken

Not assigned, and no finding is left open by them.

| Item | Note |
|---|---|
| R761 S1, S2 | Answered in `QUESTIONS.md`, findings only |
| R761 S4 | `ci/image/command-table.json` pins. No hosted workflow runs that gate, and it already refuses on `dev` |
| R761 S5 | The fragment arm's two-clock bubble: `run_ns` can stop just short of the second edge when the wire's offset adds a nanosecond. Deterministic, and it passes at this head. Adding 1 ns to the span would close it |
| R762 S1 | Receive range is true of its seven phases, and the document says seven. A denser sweep reads 1170.0 to 1190.5 |
| R762 S3 | 10 Mb/s raises no runtime refusal. The document states the limit; no such link was run |
| R762 S4 | The owned-process deadline: see `QUESTIONS.md` (b) |

## This round's RTL changes are comments, shown

| Check | Result | Receipt |
|---|---|---|
| `hdl/` files that differ from `4cda0aa0` | `KL_gptp_gmii_launch.sv`, `KL_gptp_shadow.sv` only; every changed line is a comment | `receipts/commentonly/rtl-comment-only.txt` |
| `verilator -E -P` of each | Byte-identical | same |
| `sv2v` of the observer alone, and of the plane's 13 files | Byte-identical, 132422 bytes for the plane | same |
| `sw/litex/milan_soc.py`, parsed | AST identical | same |
| AX7101 1x1 export, no Vivado, both heads on clean clones | With comments removed, 30323 lines, identical. Raw, only the date stamps and the order of two lines in a comment tree differ | `receipts/commentonly/ax-export-compare.txt` |

So the 1x1 route of `4cda0aa0` still describes this head, and no route was repeated. Its figures are in the PR body.

**What stays unknown, as both reviews say:** no route of `dev` at `1f29f189` exists, so the routed effect of this PR alone is not measured. That is worth settling at the candidate, since slices are 15841 of 15850.

## Gates

All on commit `2d534bec9348557a9407d3024c0b199c0ebc8bce`, tree clean before and after. Live `dev` is `1f29f189279f9fc0132f4918e47342b87d22f33a`. Nothing is piped: each log and rc file was written by the gate's own run.

### Every `run:` step of `.github/workflows/docs.yml`

Each job on its own fresh clean clone, by the method of `640-a720g`'s gate table: its venv copied, `$VALIDATION_STORAGE/818-mdvenv` for the Markdown rows below, a scratch HOME with the pinned SDK freshly installed and verified, `TMPDIR` in scratch. `gate_8` ran verbatim as a `pull_request` against live `dev`. Logs are in `receipts/gates/docsyml/`, one log and one rc per step; a log over 200 KB is recorded in that directory's `LARGE-LOGS.txt` with its tail kept. The table is the output of `verify_docs_yml.py`, rc 0, and is also `receipts/gates/docs-yml-table.md`.

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
| docs-gates-0 | gate_46 | AEM store generator self-test | 0 | `docs-gates-0__gate_46.log` |
| docs-gates-0 | gate_47 | Sweep/build shape gate | 0 | `docs-gates-0__gate_47.log` |
| docs-gates-0 | gate_48 | Deploy shape gate | 0 | `docs-gates-0__gate_48.log` |
| docs-gates-0 | gate_49 | Entity shape gate | 0 | `docs-gates-0__gate_49.log` |
| docs-gates-0 | ci_step_52 | Fetch inventory dependencies | 0 | `docs-gates-0__ci_step_52.log` |
| docs-gates-0 | gate_50 | CI scheduling and evidence controls | 0 | `docs-gates-0__gate_50.log` |
| docs-gates-0 | ci_step_54 | Record executed gate outcomes | NOT RUN | ci_gate_receipts record reads the hosted step context |
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

64 steps ran, 31 not run with a reason, 0 bad

`docs-gates-1` ran in the first run directory, before the SDK re-run, and its logs were copied in; the clone and the SDK it used were valid. Leg 0 under this venv and scratch HOME: `ALL GATES PASS EXCEPT 1 NOT RUN`. Leg 1: `ALL GATES PASS EXCEPT 16 NOT RUN`. Those 16 arms need a LiteX interpreter or a local Arty report, which is why the legs ran a second time below.

### The rest

| Gate | Command | rc | Result | Log |
|---|---|---:|---|---|
| Closed loop, both shapes, every control | `make -C tb/verilator/gptp_txts` on a clean clone | 0 | 95 of 95 at GMII, at MII 80 MHz and at MII 100 MHz; `controls: 13 failures: 0` | `gates/gptp_txts-all.log` |
| Whitespace | `git diff --check 1f29f189 HEAD` | 0 | no output | `gates/lane/diffcheck.log` |
| Lint | `scripts/lint_rtl.py --check --self-test --jobs 4` | 0 | LINT GATE: PASS (89 violation(s) <= ratchet 89; 19 waived, 0 justified lint_off) | `gates/lane/lint_rtl.log` |
| Source lists | `scripts/pp_srcs.py --check --selftest` | 0 | rc 0 | `gates/lane/pp_srcs.log` |
| Generated chain, pinned LiteX | `gen_mac_tx_model.py --check` | 0 | both shapes re-converted from the product source | `gates/lane/gen_chain_pinned.log` |
| Migen against converted pads | `sw/litex/test_gptp_tx_timestamp.py` | 0 | test_gptp_tx_timestamp: 36 checks: 36 PASS, 0 FAIL | `gates/lane/gptp_tx_timestamp.log` |
| gPTP plane slice | `make -C tb/verilator/gptp_shadow` | 0 | 9 controls; lifecycle test passed | `gates/lane/gptp_shadow.log` |
| gPTP plane | `make -C tb/verilator/gptp_plane` | 0 | phc_step campaign: 8 checks: 8 PASS, 0 FAIL | `gates/lane/gptp_plane.log` |
| Datapath, gPTP | `make -C tb/verilator/milan_dp gptp` | 0 | 210 checks: 210 PASS, 0 FAIL | `gates/lane/milan_dp_gptp.log` |
| Datapath, gPTP latency | `make -C tb/verilator/milan_dp gptp-lat` | 0 | 210 checks: 210 PASS, 0 FAIL | `gates/lane/milan_dp_gptp_lat.log` |
| BDD | `cd tests && behave --no-capture -f plain` | 0 | 508 scenarios passed, 0 failed, 0 skipped | `gates/lane/behave.log` |
| Markdown, pinned venv | `docs_check.py` | 0 | 0 findings | `gates/lane/mdvenv_docs.log` |
| Markdown, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) | `gates/lane/mdvenv_style.log` |
| Markdown, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (151 page(s) carry an annotated contents list, 18 below the 3-section threshold) | `gates/lane/mdvenv_toc.log` |
| Builder leg 0, round 1's interpreter and HOME | `ci_builder_legs.py run 0` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN | `gates/lane/builder_leg0_env1.log` |
| Builder leg 1, round 1's interpreter and HOME | `ci_builder_legs.py run 1` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN | `gates/lane/builder_leg1_env1.log` |
| Full sweep | `native-shards.py 829-a725c ... 4 0-15 32-47 48-63 80-95`, `MAKEFLAGS=-j4 --no-print-directory` | 0 | **65 of 65 suites, 2,192,435 checks, 0 in-suite failures, no rerun.** shard 0: 15 of 15, 361,121 checks, rc 0; shard 1: 17 of 17, 1,525,511 checks, rc 0; shard 2: 17 of 17, 284,228 checks, rc 0; shard 3: 16 of 16, 21,575 checks, rc 0. `gptp_shadow`'s lifecycle test passed | `sweep/shard-*.log`, `sweep/gptp_shadow.log` |

The sweep's 2,192,435 is round 1's 2,192,417 plus 18: six new checks in each of the suite's three runs.

Controls are 13 at this head, 10 at `4cda0aa0`, and 14 on the bench branch at `7fa8332e`, whose four extra are the `latw_*` controls of the writable pair.

### Not run

| Gate | Why |
|---|---|
| Hosted workflows, and the `act` replica | They need a pushed head. This lane pushes nothing. The manager's next step |
| `docs-check` "Require every gate exactly once", `ci-manifest`, `ci-fail-fast`, `ci-cancel-tail` | Hosted orchestration, in the table above with reasons |
| rtl-fast `yosys-elaboration`, `publication-census` | Not run. This round's RTL edits are comment-only, shown above. Hosted runs them |
| rtl-fast `firmware-*` jobs | Not run. No firmware or firmware input changed |
| Candidate merge validation, post-merge containment | The manager's, at the merge turn |
| AX7101 route | Not repeated: comment-only, shown above |
| Bench | Not needed: no change touched the Arty image's logic |

Memory: my unit peaked at 8.4 GiB against the 12 GB limit. Shard 2 reached its 10 GiB cap, with 10.6 GiB in swap at its peak, and finished rc 0. Load and memory readings are in `receipts/gates/load-and-memory.txt`.

## What went wrong

- **The SDK could not be reused by copying.** The scratch HOME under `640-a720e` was copied, and `ci_step_28` refused it, `SDK provenance mismatch`, because the receipt names the install path. I removed the copy, installed fresh into my scratch HOME from the pinned archive, and re-ran the whole job on new clones. The run with rc 1 is in `$VALIDATION_STORAGE/829-a725c/gates/run1`, not in the table's run.
- **Two of my own first receipts were wrong, and I caught them before using them.** A first `sv2v` of `KL_gptp_shadow.sv` alone failed with rc 1 on both sides, and comparing the two empty outputs printed IDENTICAL. The first export script printed "the same text" before computing it, and the computed answer then said DIFFERENT, because the comment tree sits inside a block comment. Both receipts now compute the verdict after requiring rc 0 and non-empty output, and they read IDENTICAL for that reason.
- **Round 1's "126" reproduces, with a caveat.** A first regex found 124 lines, because two checksum lines have no `|`. The receipt now counts every line holding `Checksum:`, which gives 126 on both logs and matches on all of them.

## Not verified

- **No hosted run and no `act` at this head**: this lane pushes nothing.
- **The tap-out check and the physical calibration** stay owed to the owner, through #583.
- **No route of `dev`**: above.
- **No bench or flash this round**: no change touched the Arty image's logic.
