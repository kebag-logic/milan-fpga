# Docs workflow replay at head 490d54ee (clean clone per job)

| Job | Step id | Step | Action | rc | Seconds | Note |
|---|---|---|---|---|---|---|
| wire-accountability | ci_step_0 | Run actions/checkout@v4 | not run |  |  | hosted action actions/checkout@v4 |
| wire-accountability | ci_step_1 | Set CPU-derived job budgets | run | 0 | 0.0 |  |
| wire-accountability | ci_step_2 | Cache exact Python downloads | not run |  |  | hosted action actions/cache@v4 |
| wire-accountability | ci_step_3 | Fetch the engine authority the builder derives from | run | 0 | 1.0 |  |
| wire-accountability | ci_step_4 | Advertised-vs-emitted gate (green since 2026-07-28, item 00) | run | 0 | 1.0 |  |
| wire-accountability | ci_record | Record actual job execution | not run |  |  | hosted evidence plumbing |
| wire-accountability | ci_upload | Upload actual job execution | not run |  |  | hosted action actions/upload-artifact@v4 |
| **wire-accountability** | | **job result** | | **success** | | |
| docs-check-no-git | ci_step_0 | Run actions/checkout@v4 | not run |  |  | hosted action actions/checkout@v4 |
| docs-check-no-git | ci_step_1 | Retain checkout identity before removing metadata | not run |  |  | hosted evidence plumbing |
| docs-check-no-git | ci_step_2 | Set CPU-derived job budgets | run | 0 | 0.0 |  |
| docs-check-no-git | ci_step_3 | Strip git metadata, then run the docs gate | run | 0 | 6.8 |  |
| docs-check-no-git | ci_record | Record actual job execution | not run |  |  | hosted evidence plumbing |
| docs-check-no-git | ci_upload | Upload actual job execution | not run |  |  | hosted action actions/upload-artifact@v4 |
| **docs-check-no-git** | | **job result** | | **success** | | |
| docs-gates-0 | ci_step_0 | Run actions/checkout@v4 | not run |  |  | hosted action actions/checkout@v4 |
| docs-gates-0 | ci_step_1 | Set CPU-derived job budgets | run | 0 | 0.0 |  |
| docs-gates-0 | ci_step_2 | Cache exact Python downloads | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-0 | gate_1 | Build the validated HDL reference | run | 0 | 4.1 |  |
| docs-gates-0 | gate_2 | Upload the HDL reference HTML | not run |  |  | hosted action actions/upload-artifact@v4 |
| docs-gates-0 | ci_step_5 | Install the python gate dependencies | run | 0 | 0.5 |  |
| docs-gates-0 | ci_step_6 | Cache the pinned Markdown renderer downloads | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-0 | ci_step_7 | Install the pinned Markdown renderer | run | 0 | 1.0 |  |
| docs-gates-0 | ci_packages_6 | Resolve exact package downloads 6 | not run |  |  | apt package resolution; librsvg2-bin present on host |
| docs-gates-0 | ci_step_9 | Cache exact package downloads 6 | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-0 | ci_step_10 | Install diagram gate dependencies | run | 0 | 2.9 | apt-get line dropped (librsvg2-bin present); pip line run |
| docs-gates-0 | gate_7 | Link health, wording, dead-reference and local-info gate | run | 0 | 5.5 |  |
| docs-gates-0 | gate_8 | Added-line em-dash gate | run | 0 | 3.0 |  |
| docs-gates-0 | gate_9 | Concise audience documentation gate | run | 0 | 0.8 |  |
| docs-gates-0 | gate_10 | Audience diagram no-drift gate | run | 0 | 1.5 |  |
| docs-gates-0 | gate_11 | Product solution source-fact gate | run | 0 | 3.0 |  |
| docs-gates-0 | gate_12 | Verified submodule documentation gate | run | 0 | 1.5 |  |
| docs-gates-0 | gate_13 | HDL timing diagram no-drift gate | run | 0 | 0.9 |  |
| docs-gates-0 | gate_14 | Published diagram PNG gate | run | 0 | 7.6 |  |
| docs-gates-0 | gate_15 | Milan feature-status consistency gate | run | 0 | 1.7 |  |
| docs-gates-0 | gate_16 | Traceability matrix no-drift gate | run | 0 | 1.3 |  |
| docs-gates-0 | ci_step_21 | Fetch the builder source dependencies | run | 0 | 4.3 |  |
| docs-gates-0 | gate_18 | Imported gPTP documentation gate | run | 0 | 1.1 |  |
| docs-gates-0 | gate_19 | Code-quality measurement self-tests | run | 0 | 0.1 |  |
| docs-gates-0 | ci_step_24 | Cache verified sv2v archive | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-0 | ci_step_25 | Install the pinned sv2v release | run | 0 | 0.4 | same pinned archive and sha256, installed into scratch bin instead of sudo /usr/local/bin |
| docs-gates-0 | gate_21 | Bare-metal scope gate | run | 0 | 31.9 |  |
| docs-gates-0 | ci_step_27 | Cache the pinned RV32 SDK | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-0 | ci_step_28 | Install and verify the pinned RV32 SDK | run | 0 | 18.6 |  |
| docs-gates-0 | gate_24 | Compiler-absent firmware controls | run | 0 | 568.2 |  |
| docs-gates-0 | gate_26 | NVM record-space gate | run | 0 | 35.7 |  |
| docs-gates-0 | gate_27 | Capture measurement census and clock gate | run | 0 | 0.6 |  |
| docs-gates-0 | gate_28 | Saved-state writer gate | run | 0 | 288.8 |  |
| docs-gates-0 | gate_29 | SoC source-list gate (Vivado would fail 40 min in without this) | run | 0 | 2.2 |  |
| docs-gates-0 | gate_30 | RTL source-list drift gate | run | 0 | 4.0 |  |
| docs-gates-0 | gate_31 | Boundary-unit naming ratchet | run | 0 | 0.9 |  |
| docs-gates-0 | gate_32 | Port contract gate | run | 0 | 6.0 |  |
| docs-gates-0 | gate_33 | Fail-fast ratchet | run | 0 | 3.1 |  |
| docs-gates-0 | gate_34 | TODO ownership gate | run | 0 | 3.7 |  |
| docs-gates-0 | gate_35 | Test-evidence ratchet | run | 0 | 18.8 |  |
| docs-gates-0 | gate_36 | Mechanical hygiene ratchet | run | 0 | 0.9 |  |
| docs-gates-0 | gate_37 | SystemVerilog idiom gate | run | 0 | 0.7 |  |
| docs-gates-0 | gate_38 | C and C++ idiom gate | run | 0 | 3.4 |  |
| docs-gates-0 | gate_39 | Python idiom gate | run | 0 | 11.5 |  |
| docs-gates-0 | gate_40 | Shell idiom gate | run | 0 | 0.4 |  |
| docs-gates-0 | gate_43 | Doc cited-path gate | run | 0 | 0.1 |  |
| docs-gates-0 | gate_44 | Archive integrity gate | run | 0 | 0.5 |  |
| docs-gates-0 | gate_45 | Per-page contents gate | run | 0 | 11.0 |  |
| docs-gates-0 | gate_46 | Documentation inventory freshness gate | run | 0 | 2.8 |  |
| docs-gates-0 | gate_47 | AEM store generator self-test | run | 0 | 0.1 |  |
| docs-gates-0 | gate_48 | Sweep/build shape gate | run | 0 | 16.3 |  |
| docs-gates-0 | gate_49 | Deploy shape gate | run | 0 | 0.4 |  |
| docs-gates-0 | gate_50 | Entity shape gate | run | 0 | 51.6 |  |
| docs-gates-0 | gate_51 | Register reference freshness gate | run | 0 | 87.0 |  |
| docs-gates-0 | ci_step_54 | Fetch inventory dependencies | run | 0 | 1.7 |  |
| docs-gates-0 | gate_52 | CI scheduling and evidence controls | run | 0 | 29.8 |  |
| docs-gates-0 | ci_step_56 | Record executed gate outcomes | not run |  |  | hosted evidence plumbing |
| docs-gates-0 | ci_step_57 | Upload executed gate outcomes | not run |  |  | hosted action actions/upload-artifact@v4 |
| docs-gates-0 | ci_record | Record actual job execution | not run |  |  | hosted evidence plumbing |
| docs-gates-0 | ci_upload | Upload actual job execution | not run |  |  | hosted action actions/upload-artifact@v4 |
| **docs-gates-0** | | **job result** | | **success** | | |
| docs-gates-1 | ci_step_0 | Run actions/checkout@v4 | not run |  |  | hosted action actions/checkout@v4 |
| docs-gates-1 | ci_step_1 | Set CPU-derived job budgets | run | 0 | 0.0 |  |
| docs-gates-1 | ci_step_2 | Cache exact Python downloads | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-1 | ci_step_3 | Install the python gate dependencies | run | 0 | 0.7 |  |
| docs-gates-1 | ci_step_4 | Cache the pinned Markdown renderer downloads | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-1 | ci_step_5 | Install the pinned Markdown renderer | run | 0 | 1.1 |  |
| docs-gates-1 | ci_packages_4 | Resolve exact package downloads 4 | not run |  |  | apt package resolution; librsvg2-bin present on host |
| docs-gates-1 | ci_step_7 | Cache exact package downloads 4 | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-1 | ci_step_8 | Install diagram gate dependencies | run | 0 | 2.6 | apt-get line dropped (librsvg2-bin present); pip line run |
| docs-gates-1 | ci_step_9 | Fetch the builder source dependencies | run | 0 | 3.9 |  |
| docs-gates-1 | ci_step_10 | Cache verified sv2v archive | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-1 | ci_step_11 | Install the pinned sv2v release | run | 0 | 0.7 | same pinned archive and sha256, installed into scratch bin instead of sudo /usr/local/bin |
| docs-gates-1 | ci_step_12 | Cache the pinned RV32 SDK | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-1 | ci_step_13 | Install and verify the pinned RV32 SDK | run | 0 | 17.7 |  |
| docs-gates-1 | gate_25_0 | End-station builder gates, leg 0 of 2 | run | 0 | 1072.1 |  |
| docs-gates-1 | ci_step_15 | Record executed gate outcomes | not run |  |  | hosted evidence plumbing |
| docs-gates-1 | ci_step_16 | Upload executed gate outcomes | not run |  |  | hosted action actions/upload-artifact@v4 |
| docs-gates-1 | ci_record | Record actual job execution | not run |  |  | hosted evidence plumbing |
| docs-gates-1 | ci_upload | Upload actual job execution | not run |  |  | hosted action actions/upload-artifact@v4 |
| **docs-gates-1** | | **job result** | | **success** | | |
| docs-gates-2 | ci_step_0 | Run actions/checkout@v4 | not run |  |  | hosted action actions/checkout@v4 |
| docs-gates-2 | ci_step_1 | Set CPU-derived job budgets | run | 0 | 0.0 |  |
| docs-gates-2 | ci_step_2 | Cache exact Python downloads | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-2 | ci_step_3 | Install the python gate dependencies | run | 0 | 0.6 |  |
| docs-gates-2 | ci_step_4 | Cache the pinned Markdown renderer downloads | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-2 | ci_step_5 | Install the pinned Markdown renderer | run | 0 | 1.0 |  |
| docs-gates-2 | ci_packages_4 | Resolve exact package downloads 4 | not run |  |  | apt package resolution; librsvg2-bin present on host |
| docs-gates-2 | ci_step_7 | Cache exact package downloads 4 | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-2 | ci_step_8 | Install diagram gate dependencies | run | 0 | 2.7 | apt-get line dropped (librsvg2-bin present); pip line run |
| docs-gates-2 | ci_step_9 | Fetch the builder source dependencies | run | 0 | 4.1 |  |
| docs-gates-2 | ci_step_10 | Cache verified sv2v archive | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-2 | ci_step_11 | Install the pinned sv2v release | run | 0 | 0.4 | same pinned archive and sha256, installed into scratch bin instead of sudo /usr/local/bin |
| docs-gates-2 | ci_step_12 | Cache the pinned RV32 SDK | not run |  |  | hosted action actions/cache@v4 |
| docs-gates-2 | ci_step_13 | Install and verify the pinned RV32 SDK | run | 0 | 19.8 |  |
| docs-gates-2 | gate_25_1 | End-station builder gates, leg 1 of 2 | run | 0 | 492.0 |  |
| docs-gates-2 | gate_41 | CI event and SHA contract gate | run | 0 | 273.3 |  |
| docs-gates-2 | gate_42 | Local act runner contract gate | run | 0 | 154.4 |  |
| docs-gates-2 | ci_step_17 | Record executed gate outcomes | not run |  |  | hosted evidence plumbing |
| docs-gates-2 | ci_step_18 | Upload executed gate outcomes | not run |  |  | hosted action actions/upload-artifact@v4 |
| docs-gates-2 | ci_record | Record actual job execution | not run |  |  | hosted evidence plumbing |
| docs-gates-2 | ci_upload | Upload actual job execution | not run |  |  | hosted action actions/upload-artifact@v4 |
| **docs-gates-2** | | **job result** | | **success** | | |
