# docs.yml replay at 6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c

| Job | Step | Name | rc | Note |
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
| docs__ci-cancel-tail | step1 | Set CPU-derived job budgets | 0 |  |
| docs__ci-cancel-tail | step2 | Cancel confirmed terminal failures | not run | cancels a hosted run's terminal failures through the GitHub API (GH_TOKEN); never run outside a hosted run |

102 steps ran, 0 failed; 6 not run, each with its reason
