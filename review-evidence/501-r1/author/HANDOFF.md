# [A282] Issue #501 handoff

Status: local implementation and required validation commands complete. No review verdict.
Branch: `501-outmap-record`
Base: `573f0052a0e4412e81f0845438fcec2086ce5d55`
Head: `b5ee412cdc0fd771d3df1f7fda49031409cf11fa`
Assignment: https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5821769708
Reviewers: [R312] internal; [R313] external.

## Scope

Implement parent scope items 1-6. Grow 8x8 output-map records from shape;
preserve every 1x1 byte. Keep per-port layout. Donor writer: processor #61/#83.
No push, PR operation, merge, donor edit, hardware, or other checkout.

## Changes

| File:line | Change |
|---|---|
| scripts/nvm_shape.py:164 | Derive dynamic output entries from the descriptor key space; preserve larger existing allocations. |
| scripts/nvm_shape.py:177 | Publish per-port entry counts to firmware; inventory uses the same allocation. |
| scripts/nvm_contract.py:216 | Isolated control seams for old output lengths and a changed 1x1 image. |
| scripts/check_nvm_record_space.py:338 | Independent key-space expectation, journal tests, named negative-control refusals. |
| scripts/nvm_map_checks.py:31 | Baseline SHA-256, K16/full-boundary journal round trips, cleared-first restore, atomic oversized-frame refusal. |
| sw/firmware/milan_baremetal/milan_baremetal.c:274 | Consume entry counts in area sizing, record decode and per-port backend table writes. |
| sw/builder/test_builder.py:3789 | Update the firmware census fixture to the entry-count identifiers. |
| tb/verilator/nvm_backend/records_endstation_ax7101_8x8.txt:59 | Regenerated grown output frames, following name offsets and image CRC. |
| tb/verilator/nvm_backend/sim_main.cpp:761 | Whole output reads/writes/erases on every port; grown tail and one-byte-over-capacity refusals. |
| tb/verilator/nvm_backend/Makefile:11 and README.md:45 | Correct the shape/record description and test tally. |
| docs/design/SAVED_STATE_FASTCONNECT.md:300 | Capacity decision, all arithmetic, preserved 1x1, deadline, donor obligation. |
| docs/design/SAVED_STATE_MATERIALIZATION.md:1627 | Capacity decision and remaining donor adoption; distinguish historical K16 containment. |

The HDL is unchanged, including KL_nvm_backend.sv. Its existing 16-bit
per-port prefix/length tables (lines 313-316) and output decode already serve
the grown length; firmware loads the new values at milan_baremetal.c:737.
No milan_dp source leg changed; its entire default sweep completed successfully.

## Derived figures

Derived from generated overlays and encoded KLJ2 bytes; full inputs in figures.json.
8x8: 9 stream descriptors * 8 slots = 72 entries per output port;
72 * 8 = 576 payload bytes; 8 + 576 = 584 framed bytes;
8 ports * (72 - 9) * 8 = 4032 extra bytes; journal 12680 bytes.
156 records, highest ID 0xE2; worst commit 3258.1152 ms, below 8000/2 ms.
1x1: max(17 clusters, 2 * 8 slots) = 17 entries, 136 payload / 144 framed;
53 records, 3264 bytes; baseline and after images compare byte-identical.
No RTL logic or parameters changed: backend tables already accept the lengths.
OOC area/BRAM delta gate is conditional on RTL changes and does not apply.

Full journal derivations:

| Quantity | 1x1 | 8x8 |
|---|---|---|
| Fixed record bytes | 10+16+12+10+74+2*(28+16+16+12)=266 | 10+16+12+10+74+9*(28+16+16+12)=770 |
| Input map bytes | 1*(8+8*8)=72 | 8*(8+0*8)=64 |
| Output map bytes | 1*(8+17*8)=144 | 8*(8+72*8)=4672 |
| Name bytes | 38*(8+64)=2736 | 99*(8+64)=7128 |
| Raw area | 266+72+144+2736=3218 | 770+64+4672+7128=12634 |
| Image bytes | 40+align4(3218)+4=3264 | 40+align4(12634)+4=12680 |
| IDs used | 5+2*4+2+38=53 | 5+9*4+16+99=156 |
| Highest ID | 0x80+38-1=0xA5 | 0x80+99-1=0xE2 |
| Commit bound (ms) | 3000+ceil(3264/256)*5+3264*8*1000/12500000=3067.08896 | 3000+ceil(12680/256)*5+12680*8*1000/12500000=3258.1152 |

At 8x8, 2*3258.1152=6516.2304 < 8000 ms. Slot headroom:
65536-12680=52856 bytes. Unpadded record offsets are in figures.json.
The three static-output configurations retain their prior images.

The 1x1 digest, captured before any edit at the base and compared directly:
`103ce107b1402884914036a363055800ad2cd97b8067df41f5cc54be9d3a3aea`.
Files: baseline-1x1.klj2 and after-1x1.klj2, both 3264 bytes.

## Tests and controls

| Test/control | Expected | Result |
|---|---|---|
| 8x8 old output length | Reject for output-record capacity | rc 1, named refusal; self-test rc 0 |
| 1x1 pre-change image digest | Byte-identical | SHA-256 and direct byte comparison pass; changed-image control rc 1 |
| Boundary journal decode and cleared-first restore | All keys restored | 64 legal audio keys and 72 reserved storage slots pass; storage-slot D3 run explicitly synthetic |
| K16 journal decode and cleared-first restore | Ten mappings restored | D3 replay passes, every port compared from cleared state |
| D3 8x8 evidence replay | Run or documented incompatibility | passes via replay_d3.py; scratch-only harness adaptations |

## D3 replay and limits

`replay_d3.py` extracts only public evidence from immutable Git commit
`a21b165ac1c671d10cba7255beaf75cea0f81d18` to temporary scratch and deletes
it afterward. No second checkout or donor edit is used. It imports the
candidate's shape, codec and firmware, and compiles the prototype with the
candidate's backend and pinned processor sources.

The scratch adapter changes the evidence runner's root, separates physical
clusters from record capacity in its map model, and replaces K16's shrink
step with a full commit. It adds boundary and cleared-first restore cases.
The prototype RTL and donor source bytes are unchanged. Each restore runs
in a fresh process using the saved journal slots. The map model is cleared
and inspected before boot; every port is compared with decoded slot bytes.
The co-simulation's processor command and map-plane faces remain models.

| Case | Keys | Checks | Result |
|---|---:|---:|---|
| K16 old-capacity-plus-one | 9+1=10 | 17 | PASS |
| Current legal audio boundary | 8 AAF streams*8=64 | 23 | PASS |
| Full reserved storage-key boundary | 9 descriptors*8=72 | 23 | PASS |

The 72-key case changes only the map model's last default format to AAF;
that CRF row is not a legal product mapping source. This explicitly synthetic
case grades every allocated slot. The 64-key case retains the actual formats.
Neither is a claim of full D3 product integration or silicon persistence.

Additional local controls in map_controls.py remove clear and replay,
respectively. Each is detected in 2 cases*8 ports=16 checks. These controls
and the D3 process checks return zero only when every expectation holds.

Reproduce from the candidate lane:

```sh
python3 <output-directory>/replay_d3.py
python3 <output-directory>/map_controls.py
```

## Gates

Each command ran in the foreground, without a pipeline. The command recorder
used a four-hour subprocess timeout. `<output>` denotes this directory.

| Gate / command | rc / result | Log |
|---|---|---|
| `python3 scripts/check_nvm_record_space.py` | 0 | record-default.log |
| `python3 scripts/check_nvm_record_space.py --self-test` | 0 | record_space.log |
| `make -C tb/verilator/nvm_backend` | 0 | nvm_backend.log |
| `make -C tb/verilator/milan_dp` | 0; full default sweep, 1303.49 seconds | milan_dp.log |
| `python3 sw/builder/test_builder.py` | 0; physical calibration arm NOT RUN | builder.log |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | firmware.log |
| `python3 <output>/replay_d3.py` | 0 | d3-replay.log |
| `python3 <output>/map_controls.py` | 0 | map-controls.log |
| `python3 scripts/docs_check.py` | 0 | docs.log |
| `GIT_DIR=/tmp/501-no-git-metadata python3 scripts/docs_check.py` | 0 | docs-no-git.log |
| `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | 0 | em-dash.log |
| `python3 scripts/check_doc_style.py` | 0 | doc-style.log |
| `python3 scripts/gen_toc.py --check` | 0 | toc.log |
| `python3 scripts/check_doc_paths.py` | 0 | doc-paths.log |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | traceability.log |
| `python3 scripts/xvlog_gate.py --check` | 0; 0 parent, 4 existing pinned-processor findings | xvlog.log |
| `python3 scripts/check_rtl_source_lists.py` | 0 | source-lists.log |
| `python3 scripts/check_cpp_idiom.py` | 0 | cpp-idiom.log |
| `python3 scripts/check_py_idiom.py` | 0 | py-idiom.log |
| `git diff 573f0052a0e4412e81f0845438fcec2086ce5d55 --check` | 0 | diff-check.log |
| OOC area/BRAM recipe | Not applicable: no RTL changes | HDL and pins byte-identical to base |

The Markdown gates used the repository hash-locked requirements in a temporary
virtual environment outside this output directory. The no-git documentation
mode used an absent GIT_DIR, selecting the same filesystem-walk fallback as CI;
its inventory-parity self-test is explicitly skipped without Git metadata.
The temporary dependency environment and extracted D3 trees were deleted.

The builder command exits zero but reports its physical calibration arm as
NOT RUN: the required existing utilization report is absent. No hardware or
other checkout was accessed to manufacture that evidence.

The backend checks: 525/525 at 8x8, 208/208 at 1x1. Its four existing
negative controls each fail. Record-space self-test: all 18 registered controls
are detected. New direct controls return the expected rc 1:
`control-old-length.log` names output-record capacity, and
`control-1x1-digest.log` names a changed 1x1 image digest.
The default datapath sweep also caught all four render mutations; its final
control group reports 6/6 checks passing, including the two clean baselines.

## Handoff and downstream work

REVIEW-READY.md contains the final [A282] REVIEW READY report for #501.
PR-BODY.md contains the prepared PR description. The local head is committed
and the lane is clean; its subject is one line with no body or trailers.
No push, PR operation, merge, donor edit or hardware operation is authorized.
Hosted CI, independent review, reviewer-owned lens coverage, candidate merge
validation and containment remain downstream.
