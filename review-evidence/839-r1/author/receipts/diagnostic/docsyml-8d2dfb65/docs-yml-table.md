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
