[A288]

# PR #557 / issue #501: Round 2 handoff

Candidate: `dd6a68e9063c3f7aa81536197254d187e9cb65ba`.
Branch: `501-outmap-record`.
Round 1 head: `b5ee412cdc0fd771d3df1f7fda49031409cf11fa`.
PR base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
One local commit, one-line subject, no body or trailers.
Executor: [A288]. Internal reviewer: [R312]. External reviewer: [R313].

[Assignment](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5823589125),
[internal review](https://github.com/kebag-logic/milan-fpga/pull/557#issuecomment-5823344017),
[external review](https://github.com/kebag-logic/milan-fpga/pull/557#issuecomment-5823585783),
and [donor obligation](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/61#issuecomment-5823590638)
are copied beside this handoff as public inputs.

## Assignment disposition

| Item | Change | Evidence |
|---|---|---|
| 1: R312 F1 / R313 F1 | MATERIALIZATION's parameter row and framing rule use section 4.2 output entry capacities; input records retain cluster counts. Current stage-3 statements require donor adoption of the decided allocation. | Committed documentation; `probe-compare.log`; documentation gates |
| 2: R312 F3 / R313 F2 | Current image, slot, DRAM, alternative BRAM, deadline, margin, stage-container and durable-latency figures corrected. Stale 1x1 figures in the same passages corrected. Firmware documentation names generated entry constants. Explicit historical review rows remain historical. | `record-space.log`, both emitted record tables, `figures_head.json`, `figure-derivation.log`, `derived-figures.json` |
| 3: R312 F2 / R313 F3 | SNAPSHOT_OWNERSHIP section 18 and UNRESOLVED 6 derive nominal/doubled copy costs and margins. They state 8x8 liveness exposure, retained safety, unchanged shipping 1x1, and measured hold sizing as processor #61/#83 adoption acceptance. | `probe-hold.log`, `probe-hold-r312.log`; linked manager decision and donor obligation |
| 4: R313 F4 | Every mutation registers its named finding. Exit 1 alone, unrelated output, and tracebacks are rejected. | `record-space-selftest.log`, `probe-crash.log`, `refusal-paths.log` |
| 5: R313 S1/S2 | FASTCONNECT names `nvm_cosim` as the check for incorrect firmware output-length tables; the unreachable post-clear guard is removed. | `nvm-cosim.log`; `reviewer-source_mutants.log` is the published earlier mutant receipt; record-space checks remain green |

The change touches four documentation files and two Python checks.
No RTL, firmware, donor source, or submodule pin changes.
`scope-verification.log` and `validated-source-sha256.json` bind the tested bytes.
No push, PR edit, merge, hardware action, or other checkout was performed.

## Derived figures

The unchanged `tree_figures.py` builds this head's shapes and assembles its
complete gate images; `probe-compare.log` checks the tables, decoded payloads,
firmware constants, offsets, and pinned 1x1 image against the archived base.
`derive_figures.py` applies the documented arithmetic to that output.
Every figure below comes from those outputs, not review prose.

| Quantity | Shipping 1x1 | 8x8 | Source |
|---|---|---|---|
| Complete image | 3,264 B | 12,680 B | `record-space.log`, emitted record tables |
| Raw record area / records | 3,218 B / 53 | 12,634 B / 156 | `figures_head.json`, `probe-hold.log` |
| Output entries / payload / framed bytes per port | 17 / 136 / 144 | 72 / 576 / 584 | `figures_head.json`, `probe-compare.log` |
| Flash pages / programming | 13 / 65 ms | 50 / 250 ms | `figure-derivation.log` |
| Read-back / worst commit | 2.08896 / 3,067.08896 ms | 8.1152 / 3,258.1152 ms | `figure-derivation.log` |
| 8,000 ms deadline margin | 2.61x | 2.46x | `figure-derivation.log` |
| Copy instructions / DDR accesses | 21,958 / 6,436 | 83,604 / 25,268 | `probe-hold.log` |
| Nominal cycles | 412,660 | 1,594,080 | `probe-hold.log` |
| Nominal copy / hold margin | 8.3 ms / 6.06x | 31.9 ms / 1.57x | `probe-hold.log` |
| Doubled-cost copy / hold margin | 16.5 ms / 3.03x | 63.8 ms / 0.78x | `probe-hold.log` |
| Two debounces plus commit | 4,567.08896 ms, about 4.6 s | 4,758.1152 ms, about 4.8 s | `figure-derivation.log` |

At 8x8, the gate reports 19 percent slot occupancy (integer truncation;
exactly 19.34814453125 percent). The DRAM sum is
`40,000 + 4,096 + 12,680 = 56,776` bytes. The declined byte-wide BRAM
alternative needs `ceil(12,680 / 4,096) = 4` blocks. The erase contributes
about 92 percent of the commit bound. All are in `figure-derivation.log`.
The chosen DRAM placement adds no BRAM.

The complete 1x1 image retains SHA-256
`103ce107b1402884914036a363055800ad2cd97b8067df41f5cc54be9d3a3aea`.
`probe-compare.log` verifies it and the unchanged record table.

These are cost-model results, not hardware measurements.
A grant after hold expiry voids capture; release and retry preserve safety.
Sustained producer activity can prevent convergence at the grown 8x8 size.
Only BINDING is materialized today; maps are not copied yet.
Processor #61/#83 must measure the product copy and either size the hold with
an explicit margin or prove the existing 50 ms adequate, recording it in
UNRESOLVED 6. The shipping 1x1 layout is unchanged.

## Gates

| Command | rc | Result | Receipt |
|---|---|---|---|
| `python3 scripts/check_nvm_record_space.py` | 0 | Five shapes; zero findings | [record-space.log](record-space.log) |
| `python3 scripts/check_nvm_record_space.py --self-test` | 0 | 18/18 named controls rejected; real gate passes | [record-space-selftest.log](record-space-selftest.log) |
| `make -C tb/verilator/nvm_backend` | 0 | 525/525 at 8x8; 208/208 at 1x1; 4/4 controls rejected | [nvm-backend.log](nvm-backend.log) |
| `make -C tb/verilator/nvm_cosim` | 0 | 465/465 checks; 39/39 mutants detected; identity controls pass | [nvm-cosim.log](nvm-cosim.log) |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py` | 0 | Five shapes pass | [firmware.log](firmware.log) |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | Five shapes pass; 4/4 controls detected | [firmware-selftest.log](firmware-selftest.log) |
| `python3 sw/builder/test_builder.py` | 0 | Isolated full repeat; one calibration arm NOT RUN | [builder.log](builder.log) |
| `python3 scripts/docs_check.py` | 0 | Zero findings; 23/23 scrub and 4/4 routing controls | [docs-git.log](docs-git.log) |
| `env GIT_DIR=<absent> python3 scripts/docs_check.py` | 0 | Zero findings; 22/22 scrub and 4/4 routing; parity NOT RUN | [docs-no-git.log](docs-no-git.log) |
| `python3 scripts/check_em_dash.py --base 573f0052a0e4412e81f0845438fcec2086ce5d55` | 0 | Zero findings against the requested base; 339/339 arms | [em-dash.log](em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | Pass | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | Pass | [toc.log](toc.log) |
| `python3 scripts/check_doc_paths.py` | 0 | Pass | [doc-paths.log](doc-paths.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | Pass | [module-matrix.log](module-matrix.log) |
| `python3 scripts/check_py_idiom.py` | 0 | Pass | [python-idiom.log](python-idiom.log) |
| `python3 scripts/check_cpp_idiom.py` | 0 | Pass | [cpp-idiom.log](cpp-idiom.log) |
| `git diff --check` | 0 | Clean | [diff-check.log](diff-check.log) |
| `git diff --check 573f0052a0e4412e81f0845438fcec2086ce5d55 HEAD` | 0 | Clean base-to-head diff | [diff-base-check.log](diff-base-check.log) |

All commands ran in the foreground with a 7,200-second outer timeout.
Gate stdout/stderr went directly to files, without pipelines.
The Markdown gates used the repository's hashed dependency lock in a
disposable environment under temporary storage, outside this evidence directory.
The no-Git documentation mode used an absent `GIT_DIR`; its inventory-parity
control is explicitly NOT RUN because Git metadata is unavailable by design.

The builder reports exactly one NOT RUN arm: gate 11 physical calibration,
because its required existing utilization report is absent. The RV32
compiled census and available elaboration arms executed successfully.

The first builder attempt overlapped record-space generation and failed its
missing-header control. The generator writes the same tracked header that
this control removes (`endstation_builder.py:5669`); the isolated control
passes without any source change. The full isolated repeat supplies the final
gate result. `builder-attempt1.log` / `.json` preserve the failed attempt,
and `builder-preservation-isolated.log` records the focused check.
Run the builder bank without simultaneous shape generators.

## Unchanged reviewer probes

`probe-provenance.json` records the immutable archive commits and SHA-256
for each copied probe and the published base figures. R312's archive is
`289c7906aa58696561f8055fa31e03f072a87712`; R313's is
`16f870f21b428b531b12069a6cc2f361c253011b`.
The downloaded archives and extracted trees were deleted after reading.
The individual public probes and relevant receipts remain here.

| Probe | Expected and observed result | Receipt |
|---|---|---|
| R313 `compare_figures.py` | rc 0, zero failures; 1x1 unchanged; 8x8 table and image agree | `probe-compare.log` |
| R313 `hold_margin.py` | rc 0; 31.9/63.8 ms and 1.57x/0.78x at 8x8; 1x1 unchanged | `probe-hold.log` |
| R312 `hold_margin.py` | rc 0; same head figures; its historical baseline retains the page's old 8,604 B input | `probe-hold-r312.log` |
| R313 `selftest_crash_probe.py` | probe rc 0; direct crashing control rc 1 with traceback; `--self-test` rc 1, `RESULT: crash refused`; original copied bytes restored | `probe-crash.log` |

The crash probe ran on a disposable copy of the committed gate script.
`PYTHONPATH` selected this head's unchanged supporting modules; the candidate
script itself was never planted. This avoids another checkout or donor copy.
The probe bytes are unchanged. Additional disposable controls also reject
unrelated findings, untagged expected text, and a named finding followed by a
traceback (`refusal-paths.log`).

From the candidate repository, with `EVIDENCE` set to this directory:

```sh
python3 "$EVIDENCE/probes/tree_figures.py" . "$EVIDENCE/figures_head.json"
python3 "$EVIDENCE/probes/compare_figures.py" "$EVIDENCE/reviewer-figures_base.json" "$EVIDENCE/figures_head.json" .
python3 "$EVIDENCE/probes/hold_margin.py" "$EVIDENCE/reviewer-figures_base.json" "$EVIDENCE/figures_head.json"
python3 "$EVIDENCE/probes/hold_margin_r312.py"
probe_dir=$(mktemp -d)
mkdir "$probe_dir/scripts"
cp scripts/check_nvm_record_space.py "$probe_dir/scripts/"
PYTHONPATH="$PWD/scripts" PYTHONDONTWRITEBYTECODE=1 python3 "$EVIDENCE/probes/selftest_crash_probe.py" "$probe_dir"
rm -rf "$probe_dir"
```

The derived figures can be regenerated with
`python3 "$EVIDENCE/derive_figures.py" .`.
The normal record-space self-test still passes all 18 registered controls.

## Handoff boundary

`PR-BODY.md` is the complete current PR body retrieved with
`gh pr view 557 --json body`, updated for this round. Its first line is
`[A288]`, and it retains `Closes #501`. The fetched original is retained as
`PR-BODY-ORIGINAL.json`; no PR edit was made.

The final authorized action posts `[A288] REVIEW READY` on #501.
`REVIEW-READY.md` contains the exact text; `review-ready-url.txt` records its URL.

Delta reviews from [R312] and [R313], reviewer-owned lens coverage,
publication/push and hosted/local workflow acceptance, candidate-merge
validation, merge authorization, and containment remain manager duties.
This handoff provides author evidence, not a review verdict.
