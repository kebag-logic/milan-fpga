[A826] ROUND 4 - REVIEW READY

Head: dc78aedae34c25a97125ecd6816a1f645db5575f. Branch: pf-loopbram-1. PR #987 into dev-soft-core; issue #979.
Combined rounds 3+4 delta from 2e278379c1ae9ea09063b3e3cb183d0e8a3f0929; implementation base 3cda030c174b325e36c26af6420487ff91346d15.
Local commits this round: 68d17a98843861c67a2491eb64b2700432da4d3b, 2ade81b403aa0fbc32307a31eeedb2ca099a8faf and dc78aedae34c25a97125ecd6816a1f645db5575f.
No push, issue/PR comment, merge, board, bench or test-machine access occurred.

## Combined delta from the reviewed head

Round 3 retained the original capture and queue schedulers, generated the optional
read/copy state, corrected eight-page sample retention with a full claimed-page
address, added real-parent command-to-audio checks, repaired mutation anchors,
bounded timestamp matching, refused unsupported leads and corrected contract wording.

Round 4 restores the disabled leaf port lists and widths. Enabled connections append
their fields to parameter-sized existing buses; zero repetitions remove every appended
field when disabled. Capture and queue instance names remain unchanged. Invalidation
state and its predicates now exist only in the enabled generate branch. The shared
mapping writer matches the base. Harness wiring and the affected mutation anchors
follow the same fields; no assertion, stimulus or planted defect was removed.

## Disabled identity and utilization

CLOSED by construction and measurement: full release-top canonical elaboration and all disabled utilization counts match the base at both supported shapes.

The comparison uses the release flow's complete alinx_ax7101 top, including the
datapath, mailbox and processor, at the generated release parameters. Both sides
execute synth_design -rtl and write_verilog. Canonicalization removes comments,
attributes and whitespace only. All identifiers, ports, widths, cells, parameters,
connections and module order remain. A changed-connection control changes both hashes.

| Shape | Side | Canonical SHA256 |
|---|---|---|
| 1x1/1if | base | 18af89e620ea88ee2a745550bd25b1645702cec071bcba36decced2b5376d9af |
| 1x1/1if | head | 18af89e620ea88ee2a745550bd25b1645702cec071bcba36decced2b5376d9af |
| 8x8/1if | base | fe344bba8709f7b8e72075b38aa81619c316c2207f948e0adaea1540e36da767 |
| 8x8/1if | head | fe344bba8709f7b8e72075b38aa81619c316c2207f948e0adaea1540e36da767 |

The release split top refuses interfaces=2 at both commits, independently exercised
through CtrlMailbox._split. Two-interface firmware fixtures are not release SoC builds.
Therefore neither 1x1/2if nor 8x8/2if is a supported release-top elaboration.

Full synthesis uses AreaOptimized_high, then opt_design ExploreArea, through the
supplied two-slot wrapper with VIVADO_MIN_GB=20. Base synthesis receipts are reused
only at immutable 3cda030c174b325e36c26af6420487ff91346d15; every candidate result uses this head.

| Shape | LUT base / head | FF base / head | BRAM tiles base / head | DSP base / head | F7 / F8 delta |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 33792 / 33792 | 42649 / 42649 | 80 / 80 | 11 / 11 | 0 / 0 |
| 8x8/1if | 45199 / 45199 | 53086 / 53086 | 99 / 99 | 11 / 11 | 0 / 0 |

The reviewer's disabled-leaf procedure reports capture 4339 / 4339 LUT and
3961 / 3961 FF; queue 1017 / 1015 LUT and 406 / 406 FF (base / head).
That procedure retains its head-only undriven cleanup. The complete-release
comparison above executes the same recipe on both sides.

The unchanged mailbox edit window also matches in the 8x8 hierarchical synthesis
report: `u_edit` is 3996 LUT and 445 FF on both sides.

All 12 disabled builder artifacts, descriptors, firmware ROM bytes and initialization
files remain identical. ROM lengths are 126432 and 140544 bytes. Generated SoC text
identity excludes comments and checkout/include paths; CSV identity excludes comments.
Canonical RTL identity is a separate, stronger whole-design comparison.
No FPGA bitstream or ELF debug-section byte-identity claim is made.

## Finding dispositions

| Finding | Response and closure evidence |
|---|---|
| R909-1-F1 | Original arms retained. Reset and timestamp plants follow the packed boundary. ANCHORS INTACT 0. Queue campaign passes 28 checks; complete datapath/render status appears below. |
| R909-1-F2 | CLOSED by construction and measurement: full release-top canonical elaboration and all disabled utilization counts match the base at both supported shapes. |
| R909-1-F3 / R910-1-F1 | Both generated enabled parent controls pass. Production ADD, REMOVE, replacement, rejected/no-op edits, GET pages 0/1, boot clipping and edits during copying reach the real store. All 63 destinations and eight talkers run together. Both parent connection plants and both retention/address plants compile and fail PARENT_SAMPLE. |
| R909-1-F4 | Permitted documentation outcome retained: bind-only flush, claim, expiry, backlog and age remain explicitly untested in isolation. No isolated guard coverage is claimed. |
| R909-1-F5 | Both lead-three negative checks refuse; supported lead controls pass. Eight sample pages and the full claimed page address preserve overlap retention. |
| R909-1-F6 | Four datapath cycles plus 1000 ppm across K+1 periods plus 1 ns rounding. Both shapes pass the signed ramp at 84 ns wrapper jitter and fail at 87 ns. This injects timestamp error, not a retuned oscillator. |
| R909-1-F7 | Banners cover copy-before-scrub, clock-loss flush and two extra capture cycles per output pair. The parent checks every slot and the capture deadline. The new packed port fields are documented. |
| R909-1-R1 | Session label removed from the design document. |
| R909-1-R2 | Off-tree references replaced by PR #987 links. |
| R909-1-R3 | Builder row 16g follows 16e. |
| R910-1-R1 | Stale unmeasured-lane sentence replaced by the measurement reference. |
| R909-1-S1 | Explicitly disclosed: split builds use layout 3's NAME capacity and omit the absent all-fabric backend's 128-record guard. Memory ledgers remain unchanged. |

Parent results: 1x1 has 16169 checks, 4248 capture words and 88 packets; 8x8 has
122517 checks, 34004 words and 704 packets. Both have zero failures and observe five
first-eligible generations. Maximum claim-to-last-pair spans are 89 and 873 cycles.
The parent harness executes the production command core and parent transaction
interface, without processor-instruction or mailbox-transport execution.

## Validation at this head

| Gate | Result |
|---|---|
| input1 | PASS, exit 0 |
| input8 | PASS, exit 0 |
| capture | PASS, exit 0 |
| queue | PASS, exit 0 |
| milan_dp | PASS, exit 0 |
| render | PASS, exit 0 |
| coherence | PASS, exit 0 |
| Parent controls, four runtime plants, seven leaf plants, bounds, anchors, lint, docs | PASS |
| Builder union | PASS, 114 entries; one unchanged calibration row NOT RUN |
| coherence-mutants | PASS |
| portability | PASS |
| reviewer-probes | PASS |
| leaf-off | PASS |
| xvlog | PASS |
| em-dash | PASS |

Fresh enabled 1x1 route: ExtraTimingOpt, minimum setup +0.124 ns and hold +0.036 ns across four corners, zero failing endpoints and routing errors. LUT 32792, FF 42637, BRAM tiles 83.
The enabled 8x8 route is not repeated in this round; earlier route results are not
presented as exact-head receipts.

Fresh control-memory allocation remains 47.0 tiles at 1x1 and 70.5 at 8x8. Normal
8x8 allocation is still refused. The unchanged 59-tile ledger leaves 11.5 tiles of
S14 debt (14.5 above the default 56). No service bound or memory ledger changed.

[Commands, hashes, complete relevant logs and canonical chunks](receipts/INDEX.md)
bind the source and results. Files are plain text below 200 KB. Native compiler
command chatter is filtered as recorded; diagnostics and test results remain.
The one missing calibration report is not hardware evidence.

This is author evidence, not a reviewer verdict or clean-lens ledger. Independent
re-review, manager publication, hosted/local workflow acceptance and live-base
candidate-merge validation remain separate.
