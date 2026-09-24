[A282] REVIEW READY

Commit: `b5ee412cdc0fd771d3df1f7fda49031409cf11fa` (local, unpushed)
Branch: `501-outmap-record`
Base: `573f0052a0e4412e81f0845438fcec2086ce5d55`

Parent scope items 1-6 are implemented. Dynamic output-map capacity is derived per port from the stream/channel key space, retaining a larger existing allocation where needed. The gate keeps its image-and-readback structure. Firmware programs the existing backend prefix/length tables with the derived entries. The backend fixture, boundary tests, firmware census fixture, and authoritative saved-state documents are updated. No synthesizable RTL or donor source changed.

Derived 8x8 figures: `9 descriptors * 8 slots = 72 entries/port`, `72 * 8 = 576` payload bytes, and `8 + 576 = 584` framed bytes. Eight ports add `8 * (72 - 9) * 8 = 4032` bytes. The journal is `40 + align4(770 + 64 + 4672 + 7128) + 4 = 12680` bytes, containing `5 + 9*4 + 16 + 99 = 156` records, with highest ID `0x80 + 99 - 1 = 0xE2`. The worst commit bound is `3000 + ceil(12680/256)*5 + 12680*8*1000/12500000 = 3258.1152 ms`; twice that remains below 8000 ms.

The complete 1x1 image remains byte-identical: 3264 bytes, SHA-256 `103ce107b1402884914036a363055800ad2cd97b8067df41f5cc54be9d3a3aea`. Its output allocation remains `max(17, 2*8) = 17` entries. The digest was captured at the base before edits and compared directly after the change.

Validation (foreground commands, no pipelines):

| Command | Result |
|---|---|
| `python3 scripts/check_nvm_record_space.py` | rc 0 |
| `python3 scripts/check_nvm_record_space.py --self-test` | rc 0; all 18 controls caught |
| `python3 scripts/check_nvm_record_space.py --mutate old_output_length` | expected rc 1; named output-record capacity refusal |
| `python3 scripts/check_nvm_record_space.py --mutate changed_1x1_image` | expected rc 1; named changed 1x1 image digest refusal |
| `make -C tb/verilator/nvm_backend` | rc 0; 525/525 at 8x8, 208/208 at 1x1; all four existing negative controls caught |
| `make -C tb/verilator/milan_dp` | rc 0; full default sweep in 1303.49 seconds, including all four render controls |
| `python3 sw/builder/test_builder.py` | rc 0; physical calibration arm NOT RUN, as detailed below |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | rc 0; five shapes and four controls |
| `python3 scripts/docs_check.py` | rc 0 in both Git and no-Git CI modes |
| `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | rc 0 |
| `python3 scripts/check_doc_style.py` | rc 0 |
| `python3 scripts/gen_toc.py --check` | rc 0 |
| `python3 scripts/check_doc_paths.py` | rc 0 |
| `python3 docs/traceability/gen_module_matrix.py --check` | rc 0 |
| `python3 scripts/xvlog_gate.py --check` | rc 0; zero parent findings, four existing pinned-processor findings within the ratchet |
| `python3 scripts/check_rtl_source_lists.py` | rc 0 |
| `python3 scripts/check_cpp_idiom.py` | rc 0 |
| `python3 scripts/check_py_idiom.py` | rc 0 |
| `git diff --check` and base-to-head diff check | rc 0 |
| OOC area/BRAM delta | Not applicable: HDL and donor pins are byte-identical to the base |

The no-Git documentation mode used an absent `GIT_DIR`, selecting the CI filesystem-walk fallback without another checkout. Its Git-inventory parity control is explicitly skipped in that mode.

K16 and boundary evidence: the new record-space checks save, decode, clear, and restore ten entries and all 72 reserved keys separately on every grown output port. CRC-clean oversized records must be refused atomically. Separate controls removing clear or replay are each caught in 16 cases.

The public D3 evidence at `a21b165ac1c671d10cba7255beaf75cea0f81d18` also replays successfully against the current backend and pins. Temporary scratch adaptations separate physical clusters from record capacity, remove K16's shrink step, and add boundary and fresh-process cleared-first restore cases. The prototype RTL and donor sources remain unchanged. K16 passes 17/17 checks with ten mappings; the current legal audio boundary and reserved storage boundary each pass 23/23 checks. Every port is checked empty before boot and compared with the actual decoded journal after restore. Temporary evidence trees were deleted.

The actual 8x8 formats permit 64 audio keys (`8 AAF streams * 8`). The 72-slot D3 storage case explicitly substitutes an audio format for the final CRF row in the map model to exercise every allocated slot. It does not change product mapping permission. The evidence still models the processor command and map-plane faces; it is not full product integration or hardware persistence acceptance.

Acceptance criteria: parent items 1-6 met, including both named controls, unchanged 1x1 bytes, per-port layout, and K16/boundary journal decode with cleared-first restore. The processor writer adoption remains processor #61/#83, and hardware persistence acceptance remains with #70. The builder's calibration arm lacks its required existing physical utilization report; the command exits zero and reports that arm NOT RUN.

`HANDOFF.md`, `PR-BODY.md`, exact command/result metadata, logs, before/after 1x1 images, and reproducible D3/control drivers are in the assigned output directory. No push, PR operation, or merge was performed. Independent internal and external review remain pending; this is author evidence, not a review verdict.
