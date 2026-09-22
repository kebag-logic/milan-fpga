# Completed cold comparison

Source: `7ab1c8d0ad073fbc1977c455dea89b7b318d4e52`.
Tree: `790849ab7fcf7c712c77fe051bb5fb6a45d830c2`.
Both full runs and both comparison commands exited 0.

| Measurement | Sequential | Two workers |
|---|---:|---:|
| Full suite, seconds | 1136.415 | 1099.401 |
| Sampled ordinary span, seconds | 492.870 | 445.621 |
| Time before first ordinary sighting, seconds | 325.395 | 332.875 |
| Sampled render-driver span, seconds | 317.868 | 320.491 |
| Checks / failures | 9324 / 0 | 9324 / 0 |
| Sampled maximum ordinary children | 1 | 2 |
| Sampled maximum exclusive-group children | 1 | 1 |
| Sampled peak ordinary RSS, KiB | 5764 | 10900 |
| Sampled peak aggregate descendant RSS, KiB | 2686736 | 2720648 |
| wait4 peak single-process RSS, KiB | 375248 | 375188 |

The full suite saved 37.014 seconds (3.257%). The sampled ordinary span
fell by 47.249 seconds. The other phases were slightly slower in the pooled
run; no build speedup is attributed to pooling. Cold means the suite clean
target removed its build products, not eviction of host filesystem caches.

Every ordinary capture is byte-identical. Executable and input hashes match;
both gPTP transcripts match; the render outcomes and 23 phase records match
apart from measured time fields. Both runs preserve all three tracked-header
byte copies and their committed identity. Both leave the source clean.
The observation recorded 306 samples with independent/group overlap.

The limit tests are separate evidence from these samples. No telemetry adds
a test count or verdict. One cold pair establishes this host's measured result,
not a guaranteed percentage or a hosted-worker result. The warm comparison
is still pending in this interim record; see the final handoff for its result.

Raw receipts: runs/cold-sequential, runs/cold-pooled, runs/cold-comparison.json.
