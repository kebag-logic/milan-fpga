[A288] REVIEW READY

Commit: `dd6a68e9063c3f7aa81536197254d187e9cb65ba` (local, unpushed)
Branch: `501-outmap-record`
Round 1 head: `b5ee412cdc0fd771d3df1f7fda49031409cf11fa`

Round 2 assignment items 1-5 are implemented. The four authoritative pages now agree on output entry capacity, stage-3 adoption prerequisites, memory figures, deadlines and capture-hold exposure. Every record-space self-test control requires its named finding and rejects a traceback. The unreachable cleared-store guard is removed; the documentation identifies `nvm_cosim` as the instrument that detects an incorrect firmware output-length table. No RTL, firmware, donor source or pin changed.

Figures from this head's gate output and unchanged reviewer probes:

- 8x8: 72 entries per output port, 576 payload bytes, 584 framed bytes; 12,634 raw bytes, 156 records, 12,680-byte image (19 percent of a slot). The window sum is `40,000 + 4,096 + 12,680 = 56,776` bytes; the declined byte-wide alternative needs `ceil(12,680 / 4,096) = 4` BRAM36.
- Commit bound: `3,000 + ceil(12,680/256)*5 + 12,680*8*1000/12,500,000 = 3,258.1152 ms`, margin 2.46x against 8,000 ms. The corrected 1x1 figures are 3,264 bytes, 13 pages and 3,067.08896 ms, margin 2.61x.
- Copy model: `(10*(6*12,634 + 50*156) + 30*2*12,634)/50,000 = 31.8816 ms`; doubled costs give 63.7632 ms. The rounded hold margins are 1.57x and 0.78x. Both unchanged hold probes reproduce these results; `compare_figures.py` returns zero failures.
- 1x1 remains byte-identical, SHA-256 `103ce107b1402884914036a363055800ad2cd97b8067df41f5cc54be9d3a3aea`.

Sources: `record-space.log`, emitted record tables, `figures_head.json`, `probe-compare.log`, `probe-hold.log`, `probe-hold-r312.log` and `figure-derivation.log` in the handoff packet. The public probe bytes and provenance are retained unchanged.

The unchanged crash probe now reports:

```text
--mutate=collide alone: rc=1; traceback=True
--self-test with a crashing control: rc=1
RESULT: crash refused
restored original bytes
```

The probe itself exits 0. Additional disposable controls confirm rejection of unrelated findings, untagged expected text, and an expected finding followed by a traceback.

| Command | rc | Result |
|---|---|---|
| `python3 scripts/check_nvm_record_space.py` | 0 | Five shapes; zero findings |
| `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 18/18 named controls rejected; real gate passes |
| `make -C tb/verilator/nvm_backend` | 0 | 525/525 at 8x8; 208/208 at 1x1; 4/4 controls rejected |
| `make -C tb/verilator/nvm_cosim` | 0 | 465/465 checks; 39/39 mutants detected; identity controls pass |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py` | 0 | Five shapes pass |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | Five shapes pass; 4/4 controls detected |
| `python3 sw/builder/test_builder.py` | 0 | Isolated full repeat; one calibration arm NOT RUN |
| `python3 scripts/docs_check.py` | 0 | Zero findings; 23/23 scrub and 4/4 routing controls |
| `env GIT_DIR=<absent> python3 scripts/docs_check.py` | 0 | Zero findings; 22/22 scrub and 4/4 routing; parity NOT RUN |
| `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | 0 | Zero findings against the requested base; 339/339 arms |
| `python3 scripts/check_doc_style.py` | 0 | Pass |
| `python3 scripts/gen_toc.py --check` | 0 | Pass |
| `python3 scripts/check_doc_paths.py` | 0 | Pass |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | Pass |
| `python3 scripts/check_py_idiom.py` | 0 | Pass |
| `python3 scripts/check_cpp_idiom.py` | 0 | Pass |
| `git diff --check` | 0 | Clean |
| `git diff --check 573f0052a0e4412e81f0845438fcec2086ce5d55 HEAD` | 0 | Clean base-to-head diff |

The builder reports exactly one NOT RUN arm: gate 11 physical calibration,
because its required existing utilization report is absent. The RV32
compiled census and available elaboration arms executed successfully.

The no-Git documentation mode uses an absent `GIT_DIR`; inventory parity is explicitly NOT RUN in that mode. The first builder attempt overlapped a shape generator and failed its missing-header control. That control passes in isolation, and the complete isolated repeat passes without any source or test changes. Both receipts are retained.

Per the [recorded decision](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5823589125), the 50 ms hold is unchanged. Safety holds through void and retry; liveness under sustained producer activity is at risk for the larger copy. Only BINDING is materialized today. The [donor obligation](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/61#issuecomment-5823590638) requires processor #61/#83 to measure the product's 8x8 copy, establish the hold margin, and record it in UNRESOLVED 6. Shipping 1x1 is unchanged.

`HANDOFF.md`, the complete updated `PR-BODY.md`, command receipts, figure derivations and unchanged probes are in the assigned output directory. Temporary evidence archives and trees were deleted. No push, PR edit, merge, hardware action, or other checkout was performed. Delta reviews from [R312] and [R313] are pending; this is author evidence, not a review verdict.
