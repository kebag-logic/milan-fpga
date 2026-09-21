# R217 round-four reproduction artifacts

These accompany the reviewer-owned contract verdict in `../REVIEW.md`.
They do not change product sources. The fresh focused results are byte-for-byte
equal to the corresponding build entries in the immutable published results.

Use a disposable public checkout of evidence commit
`c1ee27d81c4a1e98f9584e979b73a88acfe238b3`, with its three required submodules
initialized. Set `EVIDENCE_ROOT` to that checkout and `SCRATCH` to a private
directory under `/data`; set `D3_OUT`, `OOC_OUT`, `TMPDIR` and `REVIEW_OUT`
explicitly beneath it. Run from
`design-evidence/500-materialization/proposal-evidence`:

```sh
rtk proxy taskset -c 64-79 python3 -B run.py prep
rtk proxy taskset -c 64-79 python3 -B run.py build <selected-builds.txt names> --pool 1 --jobs 8
rtk proxy taskset -c 64-79 python3 -B run.py run <same names> --pool 8
rtk proxy taskset -c 64-79 python3 -B run.py controls --pool 8
rtk proxy taskset -c 64-79 bash ooc/ooc_measure.sh r217-admit-8x8 KL_pp_acmp_lsn_admit 'N_SINKS_P=9' 0 prototype/KL_pp_acmp_lsn_admit.proto.sv
```

`selected-builds.txt` names all 27 builds. `results-focused.json` contains all
310 completed scenario judgements and `results-focused.txt` the verdicts.
`omitted-builds-and-cases.json` names every one of the 49 omitted builds and
76 omitted build/scenario pairs relative to the published full campaign.
All planned scenarios for the selected builds ran. The synthetic-rate baseline
was omitted; its selected rate mutant and the CLI failed-baseline control ran.

The independent `router_probe.sv` connects the real pinned event router to S4
with a controlled listener-ready endpoint. This supplements, rather than
replaces, the immutable harness's real listener/timer cases. It checks held
first payload, counted coalescing, two source queues, release under
backpressure, same-edge acknowledge/refire and hard reset. MODE 1 admits valid
without ready; MODE 2 admits ready without valid. Each must fail the pop/take
agreement assertion; a build failure does not count. Reproduce with:

```sh
rtk proxy taskset -c 64-79 python3 -B reproduce_router.py
```

The initial execution used the equivalent inline driver; `router-results.json`
preserves its observed exits and diagnostics with scratch paths removed.
`docs-gates.json` records the 16 sequential candidate checks. `ooc-result.txt`
and `controls-result.txt` record the separately observed results.
`initial-integrity.json` and `completion-integrity.json` preserve identity and
tracked-byte checks using portable checkout labels. No public write was made.
