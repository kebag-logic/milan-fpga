head e69d243a61a8ec1c1ad8c473f809e1351dab1b61
# CI replay at e69d243a61a8ec1c1ad8c473f809e1351dab1b61

| Workflow / job | Step | Name | rc | Note |
|---|---|---|---|---|
| docs__wire-accountability | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs__wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | 0 |  |
| docs__wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | 0 |  |
| docs__wire-accountability | ci_record | Record actual job execution | 0 |  |
| docs__wire-accountability | ci_upload | Upload actual job execution | 0 |  |
| docs__docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | 0 |  |
| docs__docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | 0 |  |
| docs__docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | 0 |  |
| docs__docs-check-no-git | ci_record | Record actual job execution | 0 |  |
| docs__docs-check-no-git | ci_upload | Upload actual job execution | 0 |  |
| docs__docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs__docs-gates-0 | gate_1 | Build the validated HDL reference | 0 |  |
| docs__docs-gates-0 | gate_2 | Upload the HDL reference HTML | 0 |  |
| docs__docs-gates-0 | ci_step_5 | Install the python gate dependencies | 0 |  |
| docs__docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | 0 |  |
| docs__docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| docs__docs-gates-0 | ci_step_10 | Install diagram gate dependencies | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | 0 |  |
| docs__docs-gates-0 | gate_8 | Added-line em-dash gate | 0 |  |
| docs__docs-gates-0 | gate_9 | Concise audience documentation gate | 0 |  |
| docs__docs-gates-0 | gate_10 | Audience diagram no-drift gate | 0 |  |
| docs__docs-gates-0 | gate_11 | Product solution source-fact gate | 0 |  |
| docs__docs-gates-0 | gate_12 | Verified submodule documentation gate | 0 |  |
| docs__docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | 0 |  |
| docs__docs-gates-0 | gate_14 | Published diagram PNG gate | 0 |  |
| docs__docs-gates-0 | gate_15 | Milan feature-status consistency gate | 0 |  |
| docs__docs-gates-0 | gate_16 | Traceability matrix no-drift gate | 0 |  |
| docs__docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | 0 |  |
| docs__docs-gates-0 | gate_18 | Imported gPTP documentation gate | 0 |  |
| docs__docs-gates-0 | gate_19 | Code-quality measurement self-tests | 0 |  |
| docs__docs-gates-0 | ci_step_25 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-0 | gate_21 | Bare-metal scope gate | 0 |  |
| docs__docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-0 | gate_24 | Compiler-absent firmware controls | 0 |  |
| docs__docs-gates-0 | gate_26 | NVM record-space gate | 0 |  |
| docs__docs-gates-0 | gate_27 | Capture measurement census and clock gate | 0 |  |
| docs__docs-gates-0 | gate_28 | Saved-state writer gate | 0 |  |
| docs__docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without th | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-0 | gate_30 | RTL source-list drift gate | 0 |  |
| docs__docs-gates-0 | gate_31 | Boundary-unit naming ratchet | 0 |  |
| docs__docs-gates-0 | gate_32 | Port contract gate | 0 |  |
| docs__docs-gates-0 | gate_33 | Fail-fast ratchet | 0 |  |
| docs__docs-gates-0 | gate_34 | TODO ownership gate | 0 |  |
| docs__docs-gates-0 | gate_35 | Test-evidence ratchet | 0 |  |
| docs__docs-gates-0 | gate_36 | Mechanical hygiene ratchet | 0 |  |
| docs__docs-gates-0 | gate_37 | SystemVerilog idiom gate | 0 |  |
| docs__docs-gates-0 | gate_38 | C and C++ idiom gate | 0 |  |
| docs__docs-gates-0 | gate_39 | Python idiom gate | 0 |  |
| docs__docs-gates-0 | gate_40 | Shell idiom gate | 0 |  |
| docs__docs-gates-0 | gate_43 | Doc cited-path gate | 0 |  |
| docs__docs-gates-0 | gate_44 | Archive integrity gate | 0 |  |
| docs__docs-gates-0 | gate_45 | Per-page contents gate | 0 |  |
| docs__docs-gates-0 | gate_46 | AEM store generator self-test | 0 |  |
| docs__docs-gates-0 | gate_47 | Sweep/build shape gate | 0 |  |
| docs__docs-gates-0 | gate_48 | Deploy shape gate | 0 |  |
| docs__docs-gates-0 | gate_49 | Entity shape gate | 0 |  |
| docs__docs-gates-0 | ci_step_52 | Fetch inventory dependencies | 0 |  |
| docs__docs-gates-0 | gate_50 | CI scheduling and evidence controls | 0 |  |
| docs__docs-gates-0 | ci_step_54 | Record executed gate outcomes | 0 |  |
| docs__docs-gates-0 | ci_step_55 | Upload executed gate outcomes | 0 |  |
| docs__docs-gates-0 | ci_record | Record actual job execution | 0 |  |
| docs__docs-gates-0 | ci_upload | Upload actual job execution | 0 |  |
| docs__docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs__docs-gates-1 | ci_step_3 | Install the python gate dependencies | 0 |  |
| docs__docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | 0 |  |
| docs__docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| docs__docs-gates-1 | ci_step_8 | Install diagram gate dependencies | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | 0 |  |
| docs__docs-gates-1 | ci_step_11 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | 0 |  |
| docs__docs-gates-1 | ci_step_15 | Record executed gate outcomes | 0 |  |
| docs__docs-gates-1 | ci_step_16 | Upload executed gate outcomes | 0 |  |
| docs__docs-gates-1 | ci_record | Record actual job execution | 0 |  |
| docs__docs-gates-1 | ci_upload | Upload actual job execution | 0 |  |
| docs__docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs__docs-gates-2 | ci_step_3 | Install the python gate dependencies | 0 |  |
| docs__docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | 0 |  |
| docs__docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| docs__docs-gates-2 | ci_step_8 | Install diagram gate dependencies | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | 0 |  |
| docs__docs-gates-2 | ci_step_11 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| docs__docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | 0 |  |
| docs__docs-gates-2 | gate_41 | CI event and SHA contract gate | 0 |  |
| docs__docs-gates-2 | gate_42 | Local act runner contract gate | 0 |  |
| docs__docs-gates-2 | ci_step_17 | Record executed gate outcomes | 0 |  |
| docs__docs-gates-2 | ci_step_18 | Upload executed gate outcomes | 0 |  |
| docs__docs-gates-2 | ci_record | Record actual job execution | 0 |  |
| docs__docs-gates-2 | ci_upload | Upload actual job execution | 0 |  |
| docs__docs-check | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs__docs-check | ci_step_4 | Install the pinned evidence reader | 0 |  |
| docs__docs-check | ci_step_5 | Download executed gate outcomes | 0 |  |
| docs__docs-check | ci_step_6 | Require every gate exactly once | 0 |  |
| docs__docs-check | ci_step_7 | Upload verified gate union | 0 |  |
| docs__docs-check | ci_record | Record actual job execution | 0 |  |
| docs__docs-check | ci_upload | Upload actual job execution | 0 |  |
| docs__ci-manifest | step1 | Set CPU-derived job budgets | 0 |  |
| docs__ci-manifest | step2 | Fetch inventory dependencies | 0 |  |
| docs__ci-manifest | step4 | Install the pinned evidence reader | 0 |  |
| docs__ci-manifest | step5 | Download completed execution artifacts | 0 |  |
| docs__ci-manifest | ci_collect | Collect actual runtime evidence | not run | collects a hosted run's artifacts through the GitHub API (GH_TOKEN, GITHUB_RUN_ID); this head has no hosted run |
| docs__ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| docs__ci-fail-fast | ci_observe | Observe the first failed job | not run | watches a hosted run through the GitHub API (GH_TOKEN); this head has no hosted run |
| docs__ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | skipped (if: false) |  |
| docs__ci-fail-fast | ci_record | Record actual job execution | 0 |  |
| docs__ci-fail-fast | ci_upload | Upload actual job execution | 0 |  |
| docs__ci-cancel-tail | step1 | Set CPU-derived job budgets | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |
| docs__ci-cancel-tail | step2 | Cancel confirmed terminal failures | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |
| elaborate__elaborate-gates-0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| elaborate__elaborate-gates-0 | scope | Decide whether this head needs an elaboration | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_6 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| elaborate__elaborate-gates-0 | ci_step_8 | Put a job-private Python environment on PATH | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_10 | Install LiteX at the pinned revisions | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_13 | Install sbt | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| elaborate__elaborate-gates-0 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_15 | Apply the toolchain patch series | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_17 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| elaborate__elaborate-gates-0 | gate_15_0 | Elaboration gates, leg 0 of 2 | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_19 | Keep the generated CPU netlist arguments for the next run | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_20 | Record executed gate outcomes | 0 |  |
| elaborate__elaborate-gates-0 | ci_step_21 | Upload executed gate outcomes | 0 |  |
| elaborate__elaborate-gates-0 | ci_record | Record actual job execution | 0 |  |
| elaborate__elaborate-gates-0 | ci_upload | Upload actual job execution | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| elaborate__elaborate-gates-1 | scope | Decide whether this head needs an elaboration | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_4 | Fetch the source dependencies the elaboration reads | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_6 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| elaborate__elaborate-gates-1 | ci_step_8 | Put a job-private Python environment on PATH | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_10 | Install LiteX at the pinned revisions | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_13 | Install sbt | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| elaborate__elaborate-gates-1 | ci_step_14 | Place the VexiiRiscv source at the revision LiteX pins | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_15 | Apply the toolchain patch series | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_17 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| elaborate__elaborate-gates-1 | gate_15_1 | Elaboration gates, leg 1 of 2 | 0 |  |
| elaborate__elaborate-gates-1 | ci_packages_17 | Resolve exact package downloads 17 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| elaborate__elaborate-gates-1 | ci_step_22 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| elaborate__elaborate-gates-1 | ci_step_23 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| elaborate__elaborate-gates-1 | gate_19 | Standalone LiteX simulation aggregate | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_25 | Keep the generated CPU netlist arguments for the next run | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_26 | Record executed gate outcomes | 0 |  |
| elaborate__elaborate-gates-1 | ci_step_27 | Upload executed gate outcomes | 0 |  |
| elaborate__elaborate-gates-1 | ci_record | Record actual job execution | 0 |  |
| elaborate__elaborate-gates-1 | ci_upload | Upload actual job execution | 0 |  |
| elaborate__elaborate | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| elaborate__elaborate | ci_step_4 | Install the pinned evidence reader | 0 |  |
| elaborate__elaborate | ci_step_5 | Download executed gate outcomes | 0 |  |
| elaborate__elaborate | ci_step_6 | Require every gate exactly once | 0 |  |
| elaborate__elaborate | ci_step_7 | Upload verified gate union | 0 |  |
| elaborate__elaborate | ci_record | Record actual job execution | 0 |  |
| elaborate__elaborate | ci_upload | Upload actual job execution | 0 |  |
| elaborate__ci-manifest | step1 | Set CPU-derived job budgets | 0 |  |
| elaborate__ci-manifest | step2 | Fetch inventory dependencies | 0 |  |
| elaborate__ci-manifest | step4 | Install the pinned evidence reader | 0 |  |
| elaborate__ci-manifest | step5 | Download completed execution artifacts | 0 |  |
| elaborate__ci-manifest | ci_collect | Collect actual runtime evidence | not run | collects a hosted run's artifacts through the GitHub API (GH_TOKEN, GITHUB_RUN_ID); this head has no hosted run |
| elaborate__ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| elaborate__ci-fail-fast | ci_observe | Observe the first failed job | not run | watches a hosted run through the GitHub API (GH_TOKEN); this head has no hosted run |
| elaborate__ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | skipped (if: false) |  |
| elaborate__ci-fail-fast | ci_record | Record actual job execution | 0 |  |
| elaborate__ci-fail-fast | ci_upload | Upload actual job execution | 0 |  |
| elaborate__ci-cancel-tail | step1 | Set CPU-derived job budgets | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |
| elaborate__ci-cancel-tail | step2 | Cancel confirmed terminal failures | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |
| rtl-fast__changes | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__changes | scope | Classify the change conservatively | 0 |  |
| rtl-fast__changes | ci_record | Record actual job execution | 0 |  |
| rtl-fast__changes | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__verilator-lint | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__verilator-lint | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl-fast__verilator-lint | ci_packages_3 | Resolve exact package downloads 3 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__verilator-lint | ci_step_6 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl-fast__verilator-lint | ci_step_7 | Run the ratcheted whole-tree lint gate | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__verilator-lint | ci_step_8 | Prove protocol-processor source lists are derived | 0 |  |
| rtl-fast__verilator-lint | ci_record | Record actual job execution | 0 |  |
| rtl-fast__verilator-lint | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__bdd-conformance | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__bdd-conformance | ci_step_3 | Fetch the processor model inputs | 0 |  |
| rtl-fast__bdd-conformance | ci_step_4 | Install behave | 0 |  |
| rtl-fast__bdd-conformance | ci_step_5 | Run the specification-facing suite | 0 |  |
| rtl-fast__bdd-conformance | ci_record | Record actual job execution | 0 |  |
| rtl-fast__bdd-conformance | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__yosys-tool | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__yosys-tool | ci_step_5 | Build Yosys from source on cache miss | not run | builds Yosys v0.66 (86f2ddeb) from source into /opt/yosys; this host's Yosys is 0.66 at that commit, ABC linked in, and the job finds it on PATH and at $HOME/opt/yosys/bin |
| rtl-fast__yosys-tool | ci_record | Record actual job execution | 0 |  |
| rtl-fast__yosys-tool | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__yosys-elaboration | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__yosys-elaboration | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl-fast__yosys-elaboration | ci_step_4 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl-fast__yosys-elaboration | ci_step_6 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__yosys-elaboration | ci_step_7 | Elaborate the integration-heavy tops | 0 |  |
| rtl-fast__yosys-elaboration | ci_step_8 | Prove the OOC read sets come from run.sh and refuse a bad on | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__yosys-elaboration | ci_step_9 | Prove ooc.sh generates the ROMs and fails on a failed top | 0 |  |
| rtl-fast__yosys-elaboration | ci_step_10 | Prove both synthesis flows refuse active elaboration guards | 0 |  |
| rtl-fast__yosys-elaboration | ci_step_11 | Prove the result cache refuses a planted entry | 0 |  |
| rtl-fast__yosys-elaboration | ci_record | Record actual job execution | 0 |  |
| rtl-fast__yosys-elaboration | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__publication-census | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__publication-census | ci_step_2 | Set memory-derived census workers | 0 |  |
| rtl-fast__publication-census | ci_step_4 | Fetch RTL dependencies | 0 |  |
| rtl-fast__publication-census | ci_packages_3 | Resolve exact package downloads 3 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__publication-census | ci_step_8 | Build Yosys from source on cache miss | not run | builds Yosys v0.66 (86f2ddeb) from source into /opt/yosys; this host's Yosys is 0.66 at that commit, ABC linked in, and the job finds it on PATH and at $HOME/opt/yosys/bin |
| rtl-fast__publication-census | ci_step_9 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl-fast__publication-census | ci_step_11 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__publication-census | ci_step_12 | Run the publication census in every shape the builder builds | 0 |  |
| rtl-fast__publication-census | ci_record | Record actual job execution | 0 |  |
| rtl-fast__publication-census | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__split-cdc | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__split-cdc | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl-fast__split-cdc | ci_packages_3 | Resolve exact package downloads 3 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__split-cdc | ci_step_6 | Build Yosys from source on cache miss | not run | builds Yosys v0.66 (86f2ddeb) from source into /opt/yosys; this host's Yosys is 0.66 at that commit, ABC linked in, and the job finds it on PATH and at $HOME/opt/yosys/bin |
| rtl-fast__split-cdc | ci_step_7 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl-fast__split-cdc | ci_step_9 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__split-cdc | ci_step_10 | Prove every split crossing goes through an approved primitiv | 0 |  |
| rtl-fast__split-cdc | ci_record | Record actual job execution | 0 |  |
| rtl-fast__split-cdc | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__firmware-unit | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__firmware-unit | ci_step_3 | Fetch RTL dependencies | 0 |  |
| rtl-fast__firmware-unit | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__firmware-unit | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-unit | ci_step_7 | Prove the tally reads a failing and a crashing test as failu | 0 |  |
| rtl-fast__firmware-unit | ci_step_9 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-unit | ci_step_10 | Run the control-plane firmware suites and RV32 builds | 0 |  |
| rtl-fast__firmware-unit | ci_step_11 | Run the saved-state store suites and its RV32 build | 0 |  |
| rtl-fast__firmware-unit | ci_step_12 | Hold the firmware coverage ratchet | 0 |  |
| rtl-fast__firmware-unit | ci_record | Record actual job execution | 0 |  |
| rtl-fast__firmware-unit | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__firmware-control-mutants | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__firmware-control-mutants | ci_step_3 | Fetch RTL dependencies | 0 |  |
| rtl-fast__firmware-control-mutants | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__firmware-control-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-control-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-control-mutants | ci_step_9 | Run the control mutation campaign | 0 |  |
| rtl-fast__firmware-control-mutants | ci_record | Record actual job execution | 0 |  |
| rtl-fast__firmware-control-mutants | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__firmware-aecp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__firmware-aecp-mutants | ci_step_3 | Fetch RTL dependencies | 0 |  |
| rtl-fast__firmware-aecp-mutants | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__firmware-aecp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-aecp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-aecp-mutants | ci_step_9 | Run the AECP mutation campaign | 0 |  |
| rtl-fast__firmware-aecp-mutants | ci_record | Record actual job execution | 0 |  |
| rtl-fast__firmware-aecp-mutants | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__firmware-srp-mutants | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__firmware-srp-mutants | ci_step_3 | Fetch RTL dependencies | 0 |  |
| rtl-fast__firmware-srp-mutants | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__firmware-srp-mutants | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-srp-mutants | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-srp-mutants | ci_step_9 | Run both SRP mutation campaigns and pin controls | 0 |  |
| rtl-fast__firmware-srp-mutants | ci_record | Record actual job execution | 0 |  |
| rtl-fast__firmware-srp-mutants | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__firmware-boundary | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__firmware-boundary | ci_step_3 | Fetch RTL dependencies | 0 |  |
| rtl-fast__firmware-boundary | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__firmware-boundary | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | 0 | replaced: the boundary gate's LiteX is the pinned tree in its own venv, the one the split image recipe uses; the step's pip install of sw/litex/litex_pins.txt would rewrite that venv, so this proves the venv carries pyyaml, migen and LiteX; GoogleTest from pacman (no apt) |
| rtl-fast__firmware-boundary | ci_step_8 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-boundary | ci_step_9 | Hold the TSN stack boundary over the firmware builders' comp | 0 |  |
| rtl-fast__firmware-boundary | ci_record | Record actual job execution | 0 |  |
| rtl-fast__firmware-boundary | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__firmware-verilator | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__firmware-verilator | ci_step_3 | Fetch RTL dependencies | 0 |  |
| rtl-fast__firmware-verilator | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__firmware-verilator | ci_step_6 | Install GoogleTest and GoogleMock and print the versions | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-verilator | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl-fast__firmware-verilator | ci_step_10 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl-fast__firmware-verilator | ci_step_11 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-verilator | ci_step_13 | Install and verify the pinned RV32 SDK | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl-fast__firmware-verilator | ci_step_14 | Hold the TSN stack boundary over the Verilator builders' com | 0 |  |
| rtl-fast__firmware-verilator | ci_record | Record actual job execution | 0 |  |
| rtl-fast__firmware-verilator | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__rtl-fast | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__rtl-fast | ci_step_2 | Require every applicable fast gate to pass | 0 |  |
| rtl-fast__rtl-fast | ci_record | Record actual job execution | 0 |  |
| rtl-fast__rtl-fast | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__ci-manifest | step1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__ci-manifest | step2 | Fetch inventory dependencies | 0 |  |
| rtl-fast__ci-manifest | step4 | Install the pinned evidence reader | 0 |  |
| rtl-fast__ci-manifest | step5 | Download completed execution artifacts | 0 |  |
| rtl-fast__ci-manifest | ci_collect | Collect actual runtime evidence | not run | collects a hosted run's artifacts through the GitHub API (GH_TOKEN, GITHUB_RUN_ID); this head has no hosted run |
| rtl-fast__ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl-fast__ci-fail-fast | ci_observe | Observe the first failed job | not run | watches a hosted run through the GitHub API (GH_TOKEN); this head has no hosted run |
| rtl-fast__ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | skipped (if: false) |  |
| rtl-fast__ci-fail-fast | ci_record | Record actual job execution | 0 |  |
| rtl-fast__ci-fail-fast | ci_upload | Upload actual job execution | 0 |  |
| rtl-fast__ci-cancel-tail | step1 | Set CPU-derived job budgets | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |
| rtl-fast__ci-cancel-tail | step2 | Cancel confirmed terminal failures | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |
| rtl__full-ci-gate | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__full-ci-gate | target | Print the event and pin the one SHA this run validates | 0 |  |
| rtl__full-ci-gate | ci_step_4 | Assert the repository default branch is dev | not run | reads the repository's default branch through the GitHub API (gh api, GH_TOKEN); not authenticated here, and the step would read 'unreadable' |
| rtl__full-ci-gate | ci_step_5 | Hold every workflow file to its contract | 0 |  |
| rtl__full-ci-gate | gate | Decide whether this exact head needs the exhaustive gates | 0 |  |
| rtl__full-ci-gate | ci_record | Record actual job execution | 0 |  |
| rtl__full-ci-gate | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__0 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__0 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__0 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__0 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__0 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__0 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__0 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__0 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__0 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__0 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__0 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__0 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__0 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__0 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__0 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__0 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__1 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__1 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__1 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__1 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__1 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__1 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__1 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__1 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__1 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__1 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__1 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__1 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__1 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | 0 |  |
| rtl__verilator-shards__1 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__1 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__1 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__1 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__2 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__2 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__2 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__2 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__2 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__2 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__2 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__2 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__2 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__2 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__2 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__2 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__2 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__2 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__2 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__2 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__2 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__3 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__3 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__3 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__3 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__3 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__3 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__3 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__3 | ci_packages_8 | Resolve exact package downloads 8 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__3 | ci_step_13 | Build Yosys from source on cache miss | not run | builds Yosys v0.66 (86f2ddeb) from source into /opt/yosys; this host's Yosys is 0.66 at that commit, ABC linked in, and the job finds it on PATH and at $HOME/opt/yosys/bin |
| rtl__verilator-shards__3 | ci_packages_9 | Resolve exact package downloads 9 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__3 | ci_step_16 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl__verilator-shards__3 | ci_step_18 | Install sv2v for the netlist-level suite owner | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__3 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__3 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__3 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__3 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__3 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__4 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__4 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__4 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__4 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__4 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__4 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__4 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__4 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__4 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__4 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__4 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__4 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__4 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__4 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__4 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__4 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__4 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__5 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__5 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__5 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__5 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__5 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__5 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__5 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__5 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__5 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__5 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__5 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__5 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__5 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__5 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__5 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__5 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__5 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__6 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__6 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__6 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__6 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__6 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__6 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__6 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__6 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__6 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__6 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__6 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__6 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__6 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__6 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__6 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__6 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__6 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__7 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__7 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__7 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__7 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__7 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__7 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__7 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__7 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__7 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__7 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__7 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__7 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__7 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__7 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__7 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__7 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__7 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__8 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__8 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__8 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__8 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__8 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__8 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__8 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__8 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__8 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__8 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__8 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__8 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__8 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__8 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__8 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__8 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__8 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__9 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__9 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__9 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__9 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__9 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__9 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__9 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__9 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__9 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__9 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__9 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__9 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__9 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__9 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__9 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__9 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__9 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__10 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__10 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__10 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__10 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__10 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__10 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__10 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__10 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__10 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__10 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__10 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__10 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__10 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__10 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__10 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__10 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__10 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__11 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__11 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__11 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__11 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__11 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__11 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__11 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__11 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__11 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__11 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__11 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__11 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__11 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__11 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__11 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__11 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__11 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__12 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__12 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__12 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__12 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__12 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__12 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__12 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__12 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__12 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__12 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__12 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__12 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__12 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__12 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__12 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__12 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__12 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__13 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__13 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__13 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__13 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__13 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__13 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__13 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__13 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__13 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__13 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__13 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__13 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__13 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__13 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__13 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__13 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__13 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__14 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__14 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__14 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__14 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__14 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__14 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__14 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__14 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__14 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__14 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__14 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__14 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__14 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__14 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__14 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__14 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__14 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__15 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__15 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__15 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__15 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__15 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__15 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__15 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__15 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__15 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__15 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__15 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__15 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__15 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__15 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__15 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__15 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__15 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__16 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__16 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__16 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__16 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__16 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__16 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__16 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__16 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__16 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__16 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__16 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__16 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__16 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__16 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__16 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__16 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__16 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__17 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__17 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__17 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__17 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__17 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__17 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__17 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__17 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__17 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__17 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__17 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__17 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__17 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__17 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__17 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__17 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__17 | ci_upload | Upload actual job execution | 0 |  |
| rtl__verilator-shards__18 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-shards__18 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__verilator-shards__18 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__verilator-shards__18 | ci_packages_4 | Resolve exact package downloads 4 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__verilator-shards__18 | ci_step_7 | Build Verilator from source on cache miss | not run | builds Verilator v5.050 from source into /opt/verilator; the pinned Verilator v5.050 (rev v5.050) is already built on this host and the job finds it on PATH and at $HOME/opt/verilator |
| rtl__verilator-shards__18 | ci_step_8 | Put Verilator on PATH and prove the version | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__verilator-shards__18 | ci_step_9 | Prove specialized suite ownership | 0 |  |
| rtl__verilator-shards__18 | ci_packages_8 | Resolve exact package downloads 8 | skipped (if: false) |  |
| rtl__verilator-shards__18 | ci_step_13 | Build Yosys from source on cache miss | skipped (if: false) |  |
| rtl__verilator-shards__18 | ci_packages_9 | Resolve exact package downloads 9 | skipped (if: false) |  |
| rtl__verilator-shards__18 | ci_step_16 | Install the pinned Yosys and prove the version | skipped (if: false) |  |
| rtl__verilator-shards__18 | ci_step_18 | Install sv2v for the netlist-level suite owner | skipped (if: false) |  |
| rtl__verilator-shards__18 | ci_step_20 | Build the pinned tsn-gen field oracle on its suite owner | skipped (if: false) |  |
| rtl__verilator-shards__18 | ci_step_21 | Run this exhaustive suite shard | 0 |  |
| rtl__verilator-shards__18 | ci_step_22 | Upload this shard's suite logs | 0 |  |
| rtl__verilator-shards__18 | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-shards__18 | ci_upload | Upload actual job execution | 0 |  |
| rtl__physical-gptp | (job) | | skipped | the job's if: is false for this event |
| rtl__verilator-suites | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__verilator-suites | ci_step_2 | Fetch inventory dependencies | 0 |  |
| rtl__verilator-suites | download-logs | Download every shard's logs | 0 |  |
| rtl__verilator-suites | ci_step_4 | Download verified suite unions | 0 |  |
| rtl__verilator-suites | ci_step_5 | Require every shard to have validated this run's SHA | 0 |  |
| rtl__verilator-suites | ci_step_6 | Prove exhaustive ownership and tally every log | 0 |  |
| rtl__verilator-suites | ci_step_7 | Require every Verilator worker to pass | 0 |  |
| rtl__verilator-suites | ci_step_8 | Require every case union to succeed | 0 |  |
| rtl__verilator-suites | ci_record | Record actual job execution | 0 |  |
| rtl__verilator-suites | ci_upload | Upload actual job execution | 0 |  |
| rtl__yosys-shards__0 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__yosys-shards__0 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__yosys-shards__0 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__yosys-shards__0 | ci_step_4 | Download the pinned Yosys build | 0 |  |
| rtl__yosys-shards__0 | ci_step_5 | Restore the pinned Yosys build | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__0 | ci_packages_5 | Resolve exact package downloads 5 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__yosys-shards__0 | ci_step_8 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl__yosys-shards__0 | ci_step_10 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__0 | ci_step_12 | Run this weighted portability shard | 0 |  |
| rtl__yosys-shards__0 | ci_step_13 | Upload per-top and structural evidence | 0 |  |
| rtl__yosys-shards__0 | ci_record | Record actual job execution | 0 |  |
| rtl__yosys-shards__0 | ci_upload | Upload actual job execution | 0 |  |
| rtl__yosys-shards__1 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__yosys-shards__1 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__yosys-shards__1 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__yosys-shards__1 | ci_step_4 | Download the pinned Yosys build | 0 |  |
| rtl__yosys-shards__1 | ci_step_5 | Restore the pinned Yosys build | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__1 | ci_packages_5 | Resolve exact package downloads 5 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__yosys-shards__1 | ci_step_8 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl__yosys-shards__1 | ci_step_10 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__1 | ci_step_12 | Run this weighted portability shard | 0 |  |
| rtl__yosys-shards__1 | ci_step_13 | Upload per-top and structural evidence | 0 |  |
| rtl__yosys-shards__1 | ci_record | Record actual job execution | 0 |  |
| rtl__yosys-shards__1 | ci_upload | Upload actual job execution | 0 |  |
| rtl__yosys-shards__2 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__yosys-shards__2 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__yosys-shards__2 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__yosys-shards__2 | ci_step_4 | Download the pinned Yosys build | 0 |  |
| rtl__yosys-shards__2 | ci_step_5 | Restore the pinned Yosys build | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__2 | ci_packages_5 | Resolve exact package downloads 5 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__yosys-shards__2 | ci_step_8 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl__yosys-shards__2 | ci_step_10 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__2 | ci_step_12 | Run this weighted portability shard | 0 |  |
| rtl__yosys-shards__2 | ci_step_13 | Upload per-top and structural evidence | 0 |  |
| rtl__yosys-shards__2 | ci_record | Record actual job execution | 0 |  |
| rtl__yosys-shards__2 | ci_upload | Upload actual job execution | 0 |  |
| rtl__yosys-shards__3 | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__yosys-shards__3 | ci_step_2 | Fetch RTL dependencies | 0 |  |
| rtl__yosys-shards__3 | ci_step_3 | Record the tree this worker validates | 0 |  |
| rtl__yosys-shards__3 | ci_step_4 | Download the pinned Yosys build | 0 |  |
| rtl__yosys-shards__3 | ci_step_5 | Restore the pinned Yosys build | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__3 | ci_packages_5 | Resolve exact package downloads 5 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__yosys-shards__3 | ci_step_8 | Install the pinned Yosys and prove the version | 0 | replaced: the version proof runs as the step's; the host's Yosys is a package at the pinned commit with ABC linked in, so there is no yosys-abc binary or ABC_REV file to link and print |
| rtl__yosys-shards__3 | ci_step_10 | Install the pinned sv2v release | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-shards__3 | ci_step_12 | Run this weighted portability shard | 0 |  |
| rtl__yosys-shards__3 | ci_step_13 | Upload per-top and structural evidence | 0 |  |
| rtl__yosys-shards__3 | ci_record | Record actual job execution | 0 |  |
| rtl__yosys-shards__3 | ci_upload | Upload actual job execution | 0 |  |
| rtl__yosys-portability | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__yosys-portability | download-results | Download every shard's evidence | 0 |  |
| rtl__yosys-portability | ci_step_3 | Require every shard to have validated this run's SHA | 0 |  |
| rtl__yosys-portability | ci_step_4 | Reconcile the live inventory and structural gates | 0 |  |
| rtl__yosys-portability | ci_step_5 | Require every Yosys worker to pass | 0 |  |
| rtl__yosys-portability | ci_record | Record actual job execution | 0 |  |
| rtl__yosys-portability | ci_upload | Upload actual job execution | 0 |  |
| rtl__yosys-tool | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__yosys-tool | ci_packages_2 | Resolve exact package downloads 2 | not run | resolves the runner's APT downloads through apt-get's solver (scripts/ci_install_cache.py); this host is Arch with no apt; the packages the job's install step names are installed here (gtest 1.18.0, librsvg's rsvg-convert, tcl, the compiler and build tools) |
| rtl__yosys-tool | ci_step_5 | Build Yosys from source on cache miss | not run | builds Yosys v0.66 (86f2ddeb) from source into /opt/yosys; this host's Yosys is 0.66 at that commit, ABC linked in, and the job finds it on PATH and at $HOME/opt/yosys/bin |
| rtl__yosys-tool | ci_step_6 | Package the pinned Yosys build | 0 | rewritten: this host has no apt and no root: apt-get lines dropped (the packages are installed here: gtest, librsvg2's rsvg-convert, tcl), dpkg-query read from pacman, what a step installs under /opt or /usr/local placed in the job's $HOME/opt instead, and the RV32 SDK installed from a local copy of its pinned archive (--archive; the installer checks its sha256) rather than downloaded again |
| rtl__yosys-tool | ci_step_7 | Upload the pinned Yosys build | 0 |  |
| rtl__yosys-tool | ci_record | Record actual job execution | 0 |  |
| rtl__yosys-tool | ci_upload | Upload actual job execution | 0 |  |
| rtl__union-milan_dp | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__union-milan_dp | ci_step_2 | Fetch inventory dependencies | 0 |  |
| rtl__union-milan_dp | ci_step_3 | Download executed case evidence | 0 |  |
| rtl__union-milan_dp | ci_step_4 | Require successful owners and every case exactly once | 0 |  |
| rtl__union-milan_dp | ci_step_5 | Upload verified suite union | 0 |  |
| rtl__union-milan_dp | ci_record | Record actual job execution | 0 |  |
| rtl__union-milan_dp | ci_upload | Upload actual job execution | 0 |  |
| rtl__union-milan_dp_mclk | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__union-milan_dp_mclk | ci_step_2 | Fetch inventory dependencies | 0 |  |
| rtl__union-milan_dp_mclk | ci_step_3 | Download executed case evidence | 0 |  |
| rtl__union-milan_dp_mclk | ci_step_4 | Require successful owners and every case exactly once | 0 |  |
| rtl__union-milan_dp_mclk | ci_step_5 | Upload verified suite union | 0 |  |
| rtl__union-milan_dp_mclk | ci_record | Record actual job execution | 0 |  |
| rtl__union-milan_dp_mclk | ci_upload | Upload actual job execution | 0 |  |
| rtl__union-capture_coherence | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__union-capture_coherence | ci_step_2 | Fetch inventory dependencies | 0 |  |
| rtl__union-capture_coherence | ci_step_3 | Download executed case evidence | 0 |  |
| rtl__union-capture_coherence | ci_step_4 | Require successful owners and every case exactly once | 0 |  |
| rtl__union-capture_coherence | ci_step_5 | Upload verified suite union | 0 |  |
| rtl__union-capture_coherence | ci_record | Record actual job execution | 0 |  |
| rtl__union-capture_coherence | ci_upload | Upload actual job execution | 0 |  |
| rtl__union-maap | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__union-maap | ci_step_2 | Fetch inventory dependencies | 0 |  |
| rtl__union-maap | ci_step_3 | Download executed case evidence | 0 |  |
| rtl__union-maap | ci_step_4 | Require successful owners and every case exactly once | 0 |  |
| rtl__union-maap | ci_step_5 | Upload verified suite union | 0 |  |
| rtl__union-maap | ci_record | Record actual job execution | 0 |  |
| rtl__union-maap | ci_upload | Upload actual job execution | 0 |  |
| rtl__union-milan_dp_render | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__union-milan_dp_render | ci_step_2 | Fetch inventory dependencies | 0 |  |
| rtl__union-milan_dp_render | ci_step_3 | Download executed case evidence | 0 |  |
| rtl__union-milan_dp_render | ci_step_4 | Require successful owners and every case exactly once | 0 |  |
| rtl__union-milan_dp_render | ci_step_5 | Upload verified suite union | 0 |  |
| rtl__union-milan_dp_render | ci_record | Record actual job execution | 0 |  |
| rtl__union-milan_dp_render | ci_upload | Upload actual job execution | 0 |  |
| rtl__union-pp_shadow | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__union-pp_shadow | ci_step_2 | Fetch inventory dependencies | 0 |  |
| rtl__union-pp_shadow | ci_step_3 | Download executed case evidence | 0 |  |
| rtl__union-pp_shadow | ci_step_4 | Require successful owners and every case exactly once | 0 |  |
| rtl__union-pp_shadow | ci_step_5 | Upload verified suite union | 0 |  |
| rtl__union-pp_shadow | ci_record | Record actual job execution | 0 |  |
| rtl__union-pp_shadow | ci_upload | Upload actual job execution | 0 |  |
| rtl__ci-manifest | step1 | Set CPU-derived job budgets | 0 |  |
| rtl__ci-manifest | step2 | Fetch inventory dependencies | 0 |  |
| rtl__ci-manifest | step4 | Install the pinned evidence reader | 0 |  |
| rtl__ci-manifest | step5 | Download completed execution artifacts | 0 |  |
| rtl__ci-manifest | ci_collect | Collect actual runtime evidence | not run | collects a hosted run's artifacts through the GitHub API (GH_TOKEN, GITHUB_RUN_ID); this head has no hosted run |
| rtl__ci-fail-fast | ci_step_1 | Set CPU-derived job budgets | 0 |  |
| rtl__ci-fail-fast | ci_observe | Observe the first failed job | not run | watches a hosted run through the GitHub API (GH_TOKEN); this head has no hosted run |
| rtl__ci-fail-fast | ci_step_3 | Cancel this run and sibling workflows | skipped (if: false) |  |
| rtl__ci-fail-fast | ci_record | Record actual job execution | 0 |  |
| rtl__ci-fail-fast | ci_upload | Upload actual job execution | 0 |  |
| rtl__ci-cancel-tail | step1 | Set CPU-derived job budgets | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |
| rtl__ci-cancel-tail | step2 | Cancel confirmed terminal failures | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |

546 steps ran, 0 failed or missing; 86 not run, each with its reason
