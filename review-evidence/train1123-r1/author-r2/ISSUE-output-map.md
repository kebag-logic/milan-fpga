# The CPU budget harness never measures the output map's largest legal edit at 1x1/1if, and it is 1,850 us against the 975 us stated

## Objective and observed evidence

At 1x1/1if, an ADD/REMOVE_AUDIO_MAPPINGS of 63 mappings on STREAM_PORT_OUTPUT 0's map (the 550 B response and
notice, IEEE 1722.1-2021 9.2.2.6's longest control_data_length of 524) measures a record of **176,099 CPU cycles**. By
the rule (cycles at the CPU clock, plus 5 %, rounded up to 5 us; `record_classes.rule`) that is **1,850 us**. The
harness states the largest legal command's record at **975 us** at 1x1/1if (`rows_tiers.LONG_RECORD_US['1x1/1if']`),
a figure measured on the input map's edit only.

The same probe at 1x1/1if also puts **2 of 105 work passes over THE SHARE** (2 ms, 200,000 cycles), the longest
229,513 cycles (2.295 ms). No graded leg has ever shown this, because no graded leg makes the edit.

At 8x8/1if the same edit on the output map measures 136,201 cycles, 1,435 us, within that point's 1,720 us. No pass
there is over THE SHARE.

**Why the harness has never measured it.** `long_notice.groups` (#894's design) edits the input map wherever it can
change, and the output map only where the input map's capacity is 0, with the `answering-ports` arm. At 1x1/1if the
input map can always change, so the output map's edit is never made, in any arm, at any head. The gap is in the
harness's design and predates the post-flip composition. The firmware's map code, `sw/firmware/ctrl/aecp/aecp_maps.c`,
is unchanged by the composition (`git diff aa30d77f <composition head> -- sw/firmware/ctrl/aecp/aecp_maps.c` is
empty). The output map's cost on `dev-soft-core` itself has not been measured, so this Issue does not claim a figure
for it.

**How this surfaced.** On the composed train, #584's AUDIO_CLUSTER on every 8x8 STREAM_PORT_INPUT let the input map
change at 8x8. So `long_notice.groups` switched from the output map to the input map there, and 8x8/1if's long record
halved (167,199 to 85,310 cycles). A scratch probe of the output map's edit was run at both points to see what the
harness stopped measuring at 8x8/1if. It also showed the 1x1/1if figure above.

## Figures (the composed train's images, `c2b2ba1a`, which every later head of the train keeps byte-identical)

| Point | Map edited | Largest record, CPU cycles | By the rule | Stated (`LONG_RECORD_US`) | Passes over THE SHARE |
|---|---|---:|---:|---:|---|
| 1x1/1if | output (probe) | **176,099** (and 171,743, 158,897) | **1,850 us** | 975 us | **2 of 105**, the longest 229,513 |
| 1x1/1if | input (the graded leg) | 88,914 (arm A; 90,781, 955 us, reported in `declaring-outputs`) | 935 us | 975 us | 0 |
| 8x8/1if | output (probe) | 136,201 (and 130,829, 119,609) | 1,435 us | 1,720 us | 0 of 104 |
| 8x8/1if | input (the graded leg) | 85,310 | 900 us | 1,720 us | 0 |

The input-map rows are the composed train's formal measurement (`record_classes` at each point). The probe's images
hash as the formal `answering-ports` legs' images (`6fc878502d988b52` at 8x8/1if, `a71e34dfffabee4a` at 1x1/1if), so
the probe changes stimulus only.

## How to reproduce

On a clean checkout of the composition head, change only the order in which `long_notice.groups` tries the ports, so
that the output map (port type 15) is tried first in the `answering-ports` arm:

```diff
--- a/tb/verilator/ctrl_service_budget/long_notice.py
+++ b/tb/verilator/ctrl_service_budget/long_notice.py
@@ def groups(p: scenario.Point, build: dict) -> list[scenario.Group]:
     answering = build.get('variant') == 'answering-ports'
-    port, edit = next(((t, e) for t, e in ((14, scenario.map_edit(build, 14, MAPPINGS)),
-                                           (15, scenario.map_edit(build, 15, MAPPINGS) if answering else None)) if e),
+    port, edit = next(((t, e) for t, e in ((15, scenario.map_edit(build, 15, MAPPINGS) if answering else None),
+                                           (14, scenario.map_edit(build, 14, MAPPINGS))) if e),
                       (0, None))
```

Then, with an external build directory:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --variant answering-ports \
    --build-dir <scratch>/1x1-ap --groups aecp-largest-notice \
    --record-budget-findings --record-share-findings
python3 -I tb/verilator/ctrl_service_budget/record_classes.py <scratch>/1x1-ap/results
```

Expected on the composition head: `SHARE aecp-largest-notice: 2 of 105 work passes over the per-pass share`, and from
`record_classes` three `REFUSED ... over the long record's 975 us (the largest legal command's)` lines, the dearest
176,099 CPU cycles, 1,850 us. (`record_classes` also refuses because the one-group pass has no arm A leg. That refusal
is expected.) Use `--point 8x8-1if` for the 8x8/1if row. Each run takes about 10 minutes on 8 CPUs.

## What a fix must show

The scope is a decision for the owner. Either outcome must be measured, not stated:

1. **The harness measures both maps' largest edits at every point where each map can change.** The output map's edit
   must be a graded group in a committed arm at 1x1/1if (and at 8x8/1if, where the composition stopped measuring it),
   held to `LONG_RECORD_US` and to THE SHARE like the input map's. That group must fail on today's image at 1x1/1if,
   with the figures above, before any fix: a test that cannot fail for this defect does not close it.
2. **Then one of these, by an owner decision:**
   - the firmware's output-map edit is made cheaper, so that its record is within 975 us by the rule and no pass is
     over THE SHARE at 1x1/1if, measured on the formal legs, with every owner bound still held; or
   - `LONG_RECORD_US['1x1/1if']` is restated from the measurement by #665's ruling item 4 (measurement + 5 %). In that
     case the tier model's rows that charge the long record (`rows_tiers`, `flip_grade --check`, `load_grade --check`)
     must be re-solved at the new figure, and every owner bound shown to hold (the 0.70 load, last queued notice 130
     ms, ACMP 30 ms, txL 49 ms). The 2 passes over THE SHARE cannot be restated: THE SHARE is an owner bound, so a
     pass over it must be removed in the firmware or ruled on by the owner.
3. **Both maps' figures are recorded at both points** in the design page's CPU budget section, with the image hashes.

## References

- #894: the largest legal notice's group (`long_notice.py`) and its slice ruling of 2026-11-13 (`LONG_RECORD_US`).
- #665: ruling item 4 (the measurement rule, + 5 %); THE SHARE.
- #584: the AUDIO_CLUSTER on every 8x8 STREAM_PORT_INPUT, which moved 8x8's edit to the input map.
- The post-flip composition train's formal measurement (the design page, "The post-flip composition train, measured in
  full (#665)").

## Out of scope

- The input map's edit, which is measured and within at both points.
- 8x8/2if, which this probe did not run.
