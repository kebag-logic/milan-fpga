[A389] REVIEW READY

Commit: `5c7577e51702b00683a121f97a9806c167eb072b` on `75-reconnect-bench`, local and unpushed.

Changed: the findings page and its index entry answer round-2 items 1-4 and the taken suggestions. The SRP link is pinned upstream; the acceptance rows name the two CRF pairs and disconnect/two-second-hold/reconnect sequence. The page records the initial-bind exception under #606, its DUT-side declaration difference, slope intervals, timing resolution, complete measured validity predicate, and the retained dynamic destination state.

Offline recomputation verifies all 200 raw capture hashes, transaction anchors, original intervals, and per-cycle counters. Stop assertions pass 197 attempts. Talker cycles 13, 24, and 75 each transmit 1,000 valid PDUs through the two-second hold, with continuous sequence/timestamp progression and zero start/stop increments. They are **NOT RESTARTS**, excluded from quantiles and counts. The remaining 97 talker cycles each increment both counters once, exactly explaining the retained +97/+97 totals. Every cycle's stop counts and counter deltas are published in the corrected page and round-2 addendum.

| Direction | Demonstrated restarts | Min, s | Median, s | p95, s | Max, s |
|---|---|---|---|---|---|
| DUT listener | 100 | 0.006641168 | 0.1102795055 | 0.188503018 | 0.204858977 |
| DUT talker | 97 | 0.017426921 | 0.0191746130 | 0.042346644 | 0.117736084 |

Validation: each command below returns **rc 0 at this committed head**, synchronously and without pipelines:

```text
python3 scripts/docs_check.py
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base 8bc97021
python3 scripts/check_doc_paths.py
python3 scripts/ci_scope.py --selftest
python3 scripts/check_baremetal_only.py --check
python3 scripts/check_feature_status.py --self-test
git diff --check
```

`docs_check.py` also returns rc 0 in an exact-head validation clone without submodules, then without Git metadata. The full committed-diff whitespace check passes. Every table renders with all rows and cells preserved; direct page prose analysis reports zero findings. The initial bare-metal gate invocation refused a missing environment dependency; the unchanged gate passes with the existing interpreter that supplies it. Receipts retain both outcomes.

Acceptance: all 197 demonstrated restarts remain below one second, with no progressive growth observed. **The talker 100-restart requirement remains unmet.** #75 retains the three non-restarts and missing measurements; AAF remains unmeasured. The 6.889398468-second initial bind is outside reconnect criterion 1 by the recorded decision and remains an open exception owned by #606.

The separate round-2 addendum contains HANDOFF.md, recomputation source, per-cycle stop checks, distributions, capture-size explanations, source hashes, and gate receipts. The original packet is unchanged. PR-BODY.md retains its [A386] first line and `Refs #75`, with a Round 2 section.

Independent re-review by [R370] and [R371] remains required. No push, PR edit, issue closure, merge, or bench action was performed.
