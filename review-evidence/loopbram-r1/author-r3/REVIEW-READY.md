[A826] ROUND 3 - STOP: F2 disabled 8x8 grows by 1041 LUTs; exact equality is not met

Head: `855529fe21fea685725a9edc4fe0a798154c6469`. Delta from `2e278379c1ae9ea09063b3e3cb183d0e8a3f0929`; implementation base `3cda030c174b325e36c26af6420487ff91346d15`.
Branch `pf-loopbram-1`; PR #987 targets `dev-soft-core`; issue #979.
Three local commits are committed and unpushed. The worktree is clean.
No issue/PR comments, push, merge, board, bench or test-machine access occurred.

## Delta from the reviewed head

The capture engine retains the original four-state, two-bit common FSM.
An enabled generate branch owns the extra synchronous-read phases, held left/right samples,
address, selects and their writes. The original disabled emit assignments are preserved.
The queue retains its original three-state scheduler; an enabled-only copy-active register
holds scrubbing until the mapped copy finishes.

The generated parent integration exposed a real 1x1 retention defect: a later domain event
could overwrite a claimed four-page sample buffer during a capture walk. The sample RAM is
now eight pages of 64 x 24 bits (12,288 bits), still one RAMB18. Four availability records
remain sufficient for the accepted lead range. A claim saves all three page-address bits
before metadata reuse. Timestamp matching uses a scalar comparison over the four
availability records. Both overwrite and truncated-address runtime plants reproduce
named sample failures. Enabled image and leaf measurements make range diagnostics
fatal; a short-metadata negative control proves rejection of a bad declaration.

The production AECP generator now initializes enabled loopback input defaults consistently
with the real parent: the 1x1 extra rows and 8x8 port boundaries are correct. Disabled
artifacts and firmware load bytes remain identical to the base.

## Finding disposition

| Finding | Implemented response and exact-head evidence |
|---|---|
| R909 F1 | Both original mutation arms retained and re-anchored. The later drain predicate anchor also follows the copy-active scheduler. Reviewer audit says `ANCHORS INTACT 0`; queue passes all 28 checks (26 plants and two controls); the complete datapath run, including `render_mutants.py`, exits 0. All candidate receipts and source hashes bind this head. |
| R909 F2 | Structural exclusion implemented. F2 remains OPEN: disabled 8x8 grows by 1041 LUTs. Queue leaf LUT delta is -2; all full-image deltas are recorded below. No equality or completed-review claim is made. |
| R909 F3 / R910 F1 | Both generated enabled parent controls pass. Production AECP ADD/REMOVE/replacement, rejected/no-op edits, GET pages 0/1, boot format clipping followed by widening, and an accepted edit during copying reach the real parent map store/writers. Silence and first eligible samples are graded. Two parent-connection plants fail `PARENT_SAMPLE` at runtime; all 63 destinations and eight talkers run concurrently. |
| R909 F4 | The permitted documentation outcome is used. Both design and test README explicitly list bind-only flush, one-shot claim, expiry, backlog and age guards as untested defence in depth. Reviewer probes confirm these five plants survive. This is not isolated guard coverage. |
| R909 F5 | Enabled lead above two refuses elaboration; both lead-three negative checks refuse. Eight-page sample retention additionally fixes the real capture-overlap defect found by the parent test. |
| R909 F6 | Window derived from four datapath cycles, 1000 ppm across K+1 media periods, and 1 ns rounding. Both shapes pass signed ppm ramps with 84 ns wrapper jitter; 87 ns fails sample assertions. This injects timestamp error, not a physically retuned oscillator. |
| R909 F7 | Module banners describe copy before scrub, enabled clock-loss flush, and two added capture cycles per slot. Parent tests grade every output slot and enforce the capture deadline. |
| R909 R1 | Session label removed from the authoritative design document. |
| R909 R2 | Off-tree packet references replaced with links to PR #987. |
| R909 R3 | Builder row 16g moved after 16e. |
| R910 R1 | Stale unmeasured-lane sentence replaced with the fresh-measurement reference on PR #987. |
| R909 S1 | Explicitly disclosed: split builds use layout 3's NAME capacity and no longer apply the absent all-fabric backend's 128-record bound. This is a guard change; owner memory ledgers remain unchanged. |

## Parent integration and limits

1x1: 16,169 checks, 4,248 capture words, 88 AAF packets, zero failures.
8x8: 122,517 checks, 34,004 capture words, 704 AAF packets, zero failures.
The full-width run exercises all 63 mapped destinations and eight output streams concurrently,
and checks the final unavailable channel is silent. Both shapes observe five first-eligible
generations. Claim through last valid pair is at most 89 / 873 cycles. The final configured
gap remains part of the full FSM budget (899 cycles at the generated 8x8 geometry; 930 for
32 legacy input pairs).

The production AECP C core and generated entity decode real command packets; callbacks
exercise the actual split parent transaction protocol. This does not execute processor
instructions or mailbox transport. Expected maps derive from command intent, and expected
audio from input wire identities and commit timing, never DUT map or buffer contents.
Both GET pages are checked through production command handling and independently through
the real parent GET port. The four runtime plants are missing parent invalidation,
disconnected parent map, modulo-four sample reuse, and truncated claimed-page address.
Every plant compiles and then fails `PARENT_SAMPLE`.

## Disabled identity and utilisation

The disabled capture structure is repaired, but F2 remains OPEN: disabled 8x8 grows by 1041 LUTs, violating the owner no-growth rule. Exact equality is also unmet. Capture: 3961 FF and 4339 LUT at both commits. Queue: 406 FF at both commits, 1017 -> 1015 LUT (-2). The full-image results below are measured independently and do not waive the equality criterion.

| Shape | LUT base / head (delta) | FF base / head (delta) | BRAM tiles base / head (delta) | F7 / F8 mux delta |
|---|---:|---:|---:|---:|
| endstation_ax7101_1x1_tdm8 | 33792 / 33692 (-100) | 42649 / 42642 (-7) | 80 / 80 (+0) | +62 / +3 |
| endstation_ax7101_8x8 | 45199 / 46240 (+1041) | 53086 / 53051 (-35) | 99 / 99 (+0) | -14 / +3 |

DSP usage remains 11 at both disabled shapes and both commits.
All 12 builder artifacts and descriptor images match byte for byte at both shapes.
Disabled firmware ROM bytes match (126,432 / 140,544 bytes), as do memory initialization
bytes. Generated SoC text matches after comment and checkout/include-path normalization.
CSR CSV equality excludes generated comments. Raw SoC/CSV text and ELF debug data are
outside the byte-identity claim. Processor naming uses
a fixed Python hash seed. Base measurements are reused only from immutable `3cda030c174b325e36c26af6420487ff91346d15`;
no earlier candidate measurement is used for this head.

Before area optimization, `KL_mbx_cdc` grows by 2,024 LUTs, including 1,823 in its
`u_edit` subtree, while the full datapath subtree is smaller (-1,221 LUTs). These figures
locate the measured change; they are not a root-cause proof or a waiver of the final
+1,041 LUT result. Both synthesis hierarchies are included in the receipts.

## Enabled physical measurements and S14

All three route recipes were attempted at both sizes. Selection uses greatest minimum
setup slack among completed routes with no routing errors. Each selected route has four
signoff reports, zero failing setup/hold endpoints, setup >= 0.030 ns and hold >= 0 ns.
Every run used the supplied two-slot wrapper with a 20 GB MemAvailable admission minimum.

| Shape | Selected placement | LUT | FF | RAMB36 / RAMB18 | Slices | Minimum setup / hold ns |
|---|---|---:|---:|---:|---:|---:|
| endstation_ax7101_1x1_tdm8 | ExtraTimingOpt | 33038 | 42642 | 65 / 36 | 14320 | +0.228 / +0.011 |
| endstation_ax7101_8x8 | AltSpreadLogic_high | 48114 | 54677 | 94 / 34 | 15763 | +0.295 / +0.036 |

Fresh isolated leaf increments: mapped path 605 LUT / 260 FF / 0 RAMB36 / 1 RAMB18; legacy capture 2216 LUT / 2360 FF / 1 RAMB36 / 0 RAMB18. Capacities and semantics differ (63 mapped versus 64 legacy channels); this is not a like-for-like replacement claim.

Enabled 1x1 control memory is 47.0 tiles: ROM 129,056 bytes allocated 131,072; SRAM 60,352
allocated 61,440. Enabled 8x8 remains 70.5 tiles: ROM 160,024 allocated 161,792; SRAM 125,104
allocated 126,976. The latter is 11.5 above the unchanged 59-tile ledger and 14.5 above the
56-tile default budget. Normal product allocation is still REFUSED. Only disposable
measurement exports bypass that refusal. S14 remains open; this packet does not authorize
adoption or relax loads 0.70/0.75, last notice 140 ms, ACMP 30 ms, 1x1/1if txL 49 ms or
THE SHARE 2 ms. Enabled service timing is not inferred from disabled identity.

## Completed gates

| Gate | Result |
|---|---|
| `make -C tb/verilator/render_queue all` | PASS, 28/28 checks: 26 plants and two controls |
| `make -C tb/verilator/milan_dp run` | PASS, includes `render_mutants.py` |
| `make -C tb/verilator/milan_dp_render run ship8 tdm8render-mutants` | PASS; extended campaign 32/32 checks |
| `make -C tb/verilator/chmap_capture run` | PASS |
| `make -C tb/verilator/capture_coherence run dp` and its mutation campaign | PASS; 42 checks pass; 32 planted mutations plus controls and build checks |
| Original wire harness, both approved sizes | PASS, 76,017 checks / 447 packets and 79,587 / 468 |
| Seven original loopback plants plus control | PASS; all seven detected |
| New enabled parent controls and four runtime plants | PASS |
| Bounds and adapted reviewer probes | PASS expected verdicts; five guard plants explicitly untested |
| 114-entry builder union with required elaboration and RV32 legs | PASS inventory; one unchanged calibration-report row is NOT RUN because its external report is absent |
| 63 portability tops and structural controls | PASS |
| RTL syntax, lint ratchet, docs/style/privacy and em-dash checks | PASS |
| Exact-head source hash recheck and clean worktree | PASS |

Exact commands, versions, environment, exit codes and complete relevant test output are
in [receipts/INDEX.md](receipts/INDEX.md). Compiler command chatter is filtered as declared;
original log hashes are retained. Large text receipts are split below 200 KB, without gzip.
The missing calibration-report row is not a hardware claim. No hardware validation ran.

This is an author implementation/evidence packet, not a reviewer verdict or lens ledger.
Independent re-review, manager publication, act/hosted acceptance and live-base candidate
merge validation remain separate. F2 has not been silently downgraded or moved elsewhere.
