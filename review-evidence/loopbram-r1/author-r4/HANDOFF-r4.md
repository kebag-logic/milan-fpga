Status: REVIEW READY
ETA: complete; no author jobs remain.

[A826] Round 4, issue #979 / PR #987.
Head: dc78aedae34c25a97125ecd6816a1f645db5575f; branch pf-loopbram-1; target dev-soft-core.
Three local commits are ready for the manager; nothing was pushed.

CLOSED by construction and measurement: full release-top canonical elaboration and all disabled utilization counts match the base at both supported shapes.

Both disabled release-top canonical netlists match the base exactly.

| Shape | LUT base / head | FF base / head | BRAM tiles base / head | DSP base / head | F7 / F8 delta |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 33792 / 33792 | 42649 / 42649 | 80 / 80 | 11 / 11 | 0 / 0 |
| 8x8/1if | 45199 / 45199 | 53086 / 53086 | 99 / 99 | 11 / 11 | 0 / 0 |

Fresh enabled 1x1 route: ExtraTimingOpt, minimum setup +0.124 ns and hold +0.036 ns across four corners, zero failing endpoints and routing errors. LUT 32792, FF 42637, BRAM tiles 83.

[Combined rounds 3+4 findings and evidence](REVIEW-READY.md)
[Full updated PR body](PR-BODY.md)
[Exact-head receipts](receipts/INDEX.md)

No public comment, push, merge, board, bench or test-machine access occurred.
Independent re-review and manager publication remain pending.
S14 remains open; no owner budget or service bound was relaxed.

REVIEW READY dc78aedae34c25a97125ecd6816a1f645db5575f
