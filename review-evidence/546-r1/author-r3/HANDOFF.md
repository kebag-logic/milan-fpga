[A278] PR #554 / issue #546, round 3 author handoff

Local head: `0c61d458941088f3847513b7c6fe6589c75b4270`.
Starting head: `d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1`.
Branch: `546-crf-talker-step`.
Two commits, each with a one-line subject, no body and no trailers:

- `28b6bfd38300afd9b66c2e7893c30f6141521a38`: Correct CRF clock citations and prove PI resumes after invalid samples
- `0c61d458941088f3847513b7c6fe6589c75b4270`: Shorten the CRF clock-bound citation sentences

## Assignment and public evidence

The [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/546#issuecomment-5820794596)
accepts the shared citation finding and both resume/disposition suggestions.
The [internal review](https://github.com/kebag-logic/milan-fpga/pull/554#issuecomment-5820211413)
and [external review](https://github.com/kebag-logic/milan-fpga/pull/554#issuecomment-5820787460)
were read with their archived reports and clause excerpts.

Archive commits on `546-review-evidence`:

- `4ba2d203d5f568205f66bf3c7d9cffba8f07a0ee`: internal report and `receipts/clause_texts.txt`.
- `be47379c55dab698fb33501574655f710fe6d1da`: external report and `receipts/authority_excerpts.txt`.

Both reports match their public comments. Evidence objects were fetched into
temporary bare storage, without checkout, and deleted after reading.
[Source record](review-inputs.txt) lists the complete archive paths.
No private transcripts or other management output directories were read.

## Changes

| Assigned item | Change | Evidence |
|---|---|---|
| R302-2 F1 / R303-2 F1 | Receiver comment and timing document cite IEEE 802.1AS Annex B.1.1 for LocalClock within +/-100 ppm, explicitly assumed for the media oscillator. Milan v1.2 section 7.4 requires media-source oscillators better than +/-50 ppm; 100 ppm retains conservative margin. The false absent-clause claim is removed. | `hdl/ieee1722/crf/KL_crf_rx.sv:275`, `docs/design/TIME_SYNC.md:191`, [replacement PR body](PR-BODY.md) |
| R303-2 S1 | U13 restores validity, applies +10 ppm relative to its settled +80 ppm talker rate, and requires trim to increase by more than 5 ppm within 24 ms. It also checks LOCKED at the offset and after restoring the original rate. | `tb/verilator/mmcm_servo/sim_main.cpp:598`; [servo receipt](mmcm_servo.log) |
| S1 mutation | `servo_never_resumes` latches PI off after the first invalid sample. The default campaign requires exit 1 and the exact `[U13] valid offset resumes PI trim` failure; compilation errors and abnormal termination cannot count. | `tb/verilator/crf_rx/mutants.py:98`; [receiver receipt](crf_rx.log) |
| R303-2 S2 / R302-2 S1 | The disposition names receiver and servo source reads, including ignored-validity and PI-resume defects. It still excludes implementation-derived expected values. | `scripts/measure_test_evidence.py:597`; [evidence gate](measure_test_evidence-check.log) |

## RTL identity and threshold

[The identity receipt](rtl-unchanged.log) compares all 72 tracked `.sv`/`.v`
files under `hdl/` between the starting head and the new head.
It removes comments and blank-only lines while preserving code spacing,
strings and escaped identifiers. Every result is identical.
Only the receiver's raw source bytes differ; the servo is byte-identical.

The receiver's comment-free SHA-256 at both heads is
`a5957197ac77d20031d3c48a927c8f560081e5349819fe569283a9fed73e7171`.
The servo's is
`72cc0db964d682d33563c26a93ff4c2c40a35545646cb5f5526a3f466ed23ade`.

Independent elaboration of both revisions gives:

- `RATE_DRIFT_NS_C = 601` (`32'h259`).
- `TS_JUMP_NS_C = 2048` (`64'h800`).

Reproduce from the candidate repository with
`python3 "$receipt_dir/prove_rtl.py"`, where `receipt_dir` names this artifact directory.
The check also verifies current HDL bytes against the committed head.

## Validation

All final result rows return zero. Each row names its measured head.

| Command | rc | Measured head | Receipt |
|---|---|---|---|
| `make -C tb/verilator/crf_rx` | 0 | `28b6bfd38` | [crf_rx](crf_rx.log) |
| `make -C tb/verilator/mmcm_servo` | 0 | `28b6bfd38` | [mmcm_servo](mmcm_servo.log) |
| `python3 scripts/docs_check.py` | 0 | `0c61d4589` | [docs-check](docs-check.log) |
| `python3 scripts/docs_check.py (no git metadata)` | 0 | `0c61d4589` | [docs-check-no-git](docs-check-no-git.log) |
| `python3 scripts/check_em_dash.py --base 57456af96b3127b9d309a995bbbd35a6113ce52d` | 0 | `0c61d4589` | [check_em_dash](check_em_dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | `0c61d4589` | [check_doc_style](check_doc_style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | `0c61d4589` | [gen_toc](gen_toc.log) |
| `python3 scripts/check_doc_paths.py` | 0 | `0c61d4589` | [check_doc_paths](check_doc_paths.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `0c61d4589` | [module_matrix](module_matrix.log) |
| `python3 scripts/xvlog_gate.py --check` | 0 | `28b6bfd38` | [xvlog_gate](xvlog_gate.log) |
| `python3 scripts/check_cpp_idiom.py` | 0 | `28b6bfd38` | [check_cpp_idiom](check_cpp_idiom.log) |
| `python3 scripts/check_py_idiom.py` | 0 | `28b6bfd38` | [check_py_idiom](check_py_idiom.log) |
| `python3 scripts/measure_test_evidence.py` | 0 | `28b6bfd38` | [measure_test_evidence](measure_test_evidence.log) |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `28b6bfd38` | [measure_test_evidence-check](measure_test_evidence-check.log) |
| `git diff --check` | 0 | `0c61d4589` | [git-diff-check](git-diff-check.log) |
| `git diff --check d04a61678c9fc710df9bc2cad5e1bcb9d8925ae1 HEAD` | 0 | `0c61d4589` | [committed-diff-check](committed-diff-check.log) |

The receipt runner executes each command in the foreground with a two-hour
per-command limit. Commands are not piped; output goes directly to each log.
The no-git documentation run uses an exact-head source archive under temporary
storage, without `.git`; that archive is deleted when its check finishes.
The requested em-dash base is `57456af96b3127b9d309a995bbbd35a6113ce52d`.
The evidence inventory and its actual `--check` gate both run.

[Machine-readable results](gate-results.json) include commands, heads,
return codes and elapsed seconds. [The runner](run_gates.py) reproduces the
same command sequence from the candidate repository. Install the pinned
requirements in `tools/markdown/requirements.txt` and
`tools/hdl_reference/requirements.txt` in an environment outside this artifact
directory, activate it, then invoke
`python3 "$receipt_dir/run_gates.py" "$receipt_dir"`.

The receiver gate passed 13,836 unit checks, 1,658 discontinuity checks,
69 connected checks and eight mutation controls. The new mutant returned 1
and was rejected by `[U13] valid offset resumes PI trim`.
The servo gate passed 85 unit, eight rails and 113 PHC-step checks.
All six connected events retained LOCKED, with no receiver unlocks and at
most 0.020 ppm integrator movement. The quiet control observed 550
post-edge artifacts and zero sampled invalidity.

The parser gate performed actual analysis: zero parent HDL findings and
four existing pinned-processor findings matched its unchanged ratchet.
Both documentation CI modes scanned 165 Markdown and 861 text files.
The no-git mode skipped only its git-inventory parity self-check, as expected.

The first full sequence found two overlong citation sentences in the
style gate. Their wording was shortened without changing either bound.
All documentation checks were then rerun successfully at the final head.
[Initial results](initial-gate-results.json) and
[the initial style receipt](initial/check_doc_style.log) retain that failure.

Simulation, parser, idiom and evidence results were measured at
`28b6bfd38300afd9b66c2e7893c30f6141521a38`. The final commit changes only
`docs/design/TIME_SYNC.md`; [the input-identity receipt](validated-inputs-unchanged.log)
proves ancestry and an exhaustive changed-path list. Their source and build
inputs are identical at the final head, so those successful gates were not
repeated for the wording correction. The RTL identity and constant checks
were rerun at the final head.

## Review handoff and limits

This is author evidence, not a review verdict or a completion ledger.
Reviewers must re-cover the changed comments, documentation and tests at the
new head. The unchanged RTL proof supports that review; it does not grant it.

The branch remains local. No push, PR edit, merge, additional checkout,
sub-agent or hardware action was performed. The replacement PR body is
[PR-BODY.md](PR-BODY.md); publication remains with the maintainer.
Required remote validation, independent review, candidate-merge validation
and merge containment remain later workflow duties.

The archived broader reviewer campaigns, behavior bank, synthesis/area and
physical calibration were not rerun. Prior-head evidence is identified as such
in the replacement PR body. Timing closure and hardware behavior are unproved
by this simulation work. Receiver-discard telemetry stays outside the assignment.

Final tracked worktree and index are clean.
Temporary review storage, no-git exports, constant-check sources and the
validation environment have been deleted. This directory contains only
handoff documents, receipt scripts and logs.
The final public action is the assigned `[A278] REVIEW READY` comment on #546;
its prepared text is [REVIEW-READY.md](REVIEW-READY.md).

Posted [review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/546#issuecomment-5821287408).
