[A826] ROUND 8 - REVIEW READY (routing evidence; no code change)

Head: 09201d35d7ea720b3ba205da185ba35c159ec24a (tree a3b3dca8a55b738e714ada4662a309a50118a481), unchanged since round 7. Branch: pf-loopbram-1.
PR #987 into dev-soft-core; issue #979. dev-soft-core 5de21ff3661436ea5598718aca36934361e35340 is an ancestor of the head.
No commit, push, issue or PR comment, merge, board or bench access occurred. The checkout is clean.

Verdict attribution, corrected (R910-4-F2): R909-5 POSITIVE at 1516b2ffe321337858389ec8e42897f8a80644bb; R910-3 POSITIVE at 9acb9b828b29aba71bd51303a4836f86c2278267.
The round-7 review handoff attributed both to 1516b2ff. That attribution came from the round-7 brief. R910-3 did not review 1516b2ff. The round-7 files are left as published.

## R910-4-F1 MAJOR / R909-6-N1 MINOR: enabled routes at the merged head - routed, floor met at both shapes

Each shape was exported and routed from the checkout at the exact head, whose hdl tree is 244c59e030d9078054fc88744f22e4e3e7d59246.
The earlier routes read hdl tree aefab0802b86433564fce98219f03a9fb7c9bb53.

**Configurations.** Each is the shipped configuration plus `input_loopback_lane: true`; at 1x1 the old `loopback_lane` is also set to false
(it is already off at 8x8). They are byte-identical to the configurations of rounds 4 and 5 ([1x1](receipts/endstation_ax7101_1x1_tdm8.yaml.txt), [8x8](receipts/endstation_ax7101_8x8.yaml.txt)).

**Recipe, unchanged.** The generated project scripts and constraints equal round 5's (8x8) and round 4's (1x1) apart from local paths. AreaOptimized_high synthesis,
ExploreArea optimization, then each of the three prescribed placement directives from one post-optimization checkpoint, with AggressiveExplore physical
optimization and routing. All three directives ran at both shapes; the greatest worst-corner setup slack is selected. Every vendor run went through `vivado-slot.sh` with
VIVADO_SLOTS=2 and VIVADO_MIN_GB=20 ([slot use](receipts/slot-usage.json.txt): slots 0 and 1, MemAvailable at least 55 GB at each start).
The unit `milan-loopbram-a826h-route1x1` and `-route8x8` ran unbooked at the session's CPU weight, at host load about 145 on 96 CPUs when they started.

**Floor (#818).** Setup >= +0.030 ns and hold >= 0 at every signoff corner, zero failing endpoints (pulse width included), zero routing errors, every routable net routed.

| Shape | Placement | Setup | Hold | Floor | LUT | FF | BRAM tiles (RAMB36 + RAMB18) | Slices | DSP | Routable = routed nets | Errors |
|---|---|---:|---:|---|---:|---:|---|---:|---:|---:|---:|
| 1x1 | ExtraPostPlacementOpt | +0.125 | +0.036 | PASS | 32653 | 42822 | 82.5 (65 + 35) | 13951 | 13 | 73572 | 0 |
| 1x1 | **AltSpreadLogic_high, selected** | **+0.147** | **+0.036** | **PASS** | 32669 | 42821 | 82.5 (65 + 35) | 14225 | 13 | 73564 | 0 |
| 1x1 | ExtraTimingOpt | +0.020 | +0.036 | MISS (setup < +0.030) | 32668 | 42821 | 82.5 (65 + 35) | 14225 | 13 | 73552 | 0 |
| 8x8 | ExtraPostPlacementOpt | +0.117 | +0.015 | PASS | 48508 | 54964 | 110.5 (94 + 33) | 15823 | 13 | 97439 | 0 |
| 8x8 | **AltSpreadLogic_high, selected** | **+0.309** | **+0.036** | **PASS** | 48485 | 54965 | 110.5 (94 + 33) | 15792 | 13 | 97416 | 0 |
| 8x8 | ExtraTimingOpt | +0.049 | +0.036 | PASS | 48501 | 54965 | 110.5 (94 + 33) | 15793 | 13 | 97423 | 0 |

Corners of the selected routes (Slow/Fast models at 0 C and 85 C; the temperature settings are power metadata, not independent timing models):

| Shape | Slow 0 C | Slow 85 C | Fast 0 C | Fast 85 C |
|---|---|---|---|---|
| 1x1 setup / hold | +0.147 / +0.102 | +0.147 / +0.102 | +1.636 / +0.036 | +1.636 / +0.036 |
| 8x8 setup / hold | +0.309 / +0.102 | +0.309 / +0.102 | +1.660 / +0.036 | +1.660 / +0.036 |

Pulse-width slack is +1.100 ns and no endpoint fails at any corner of any route. The check_timing report of the selected 8x8 route has zero in every category except the 14 inputs and
21 outputs without delay constraints, which the board constraint file leaves unconstrained. The register-in-pad packing check passes on all six routes.
Design rule reports hold warnings only (no errors); they are in the receipts and are not a zero-warning claim. No bitstream was generated.

Worst setup paths of the six routes (slow corner): five end in the mailbox (`KL_mbx`), on the 100 MHz system clock.
The 1x1 ExtraPostPlacementOpt one runs from a CPU bridge register (`peripheral_toAxiLite4`) to a CPU hub's distributed memory (`splited_wc_hub`).
None is in the loopback logic. The margin stays placement-sensitive: 1x1 spreads 0.127 ns and 8x8 spreads 0.260 ns across the three directives.

**Historical comparison, separate.** Round 4's 1x1 selection: 32792 LUT, 42637 FF, 83 tiles, 14148 slices, 11 DSP, +0.124/+0.036 ns. Round 5's 8x8 selection: 48901 LUT, 54672 FF,
111 tiles, 15774 slices, 11 DSP, +0.223/+0.036 ns. They remain valid for their recorded sources and are not measurements of this head.
The input differences between those sources and this head are dev's own: #948's receive-path verdicts (four hdl files), the gptp-processor pin 1213ac5b (#995), the
reset of the MAC link-status word in the SoC generator (#972), and firmware changes including the lwSRP pin d1bb4f4e (#992), which move the control ROM contents.

**Ordinary allocation refusal, retained.** The ordinary 8x8 export, with the enabled configuration and no override, exits 1 and writes no project:
"allocation over budget: 70.5 RAMB36 (rom 161152 bytes in 161792, sram 125296 bytes in 126976) exceeds the 56-RAMB36 budget" ([log](receipts/ordinary--endstation_ax7101_8x8--export.log.txt)). The firmware link under the product override is also refused
([log](receipts/builds--endstation_ax7101_8x8-on.log.txt)): the override names one image, and the enabled image carries another `nvm_stage`. The routed 8x8 export is the separate measurement export, which
records that refusal and allocates only in its temporary process ([log](receipts/route--endstation_ax7101_8x8--export.log.txt), [script](receipts/measure_soc.py.txt)). The ordinary 1x1 export is accepted.

| Shape | ROM | SRAM | Tiles | Against the ledger |
|---|---|---|---:|---|
| 1x1 | 130192 B (32 RAMB36) | 60352 B (15 RAMB36) | 47.0 | within 56 |
| 8x8 | 161152 B (39 RAMB36 + 1 RAMB18) | 125296 B (31 RAMB36) | 70.5 | +11.0 over the 59.5 entry of `platform-8x8-one-interface`, +14.5 over 56 |

The 8x8 one-interface ledger entry is 59.5 at this head (dev's own move, 59 before); the enabled 70.5 tiles and the S14 disposition are unchanged. No ledger, budget or product guard was changed here.

**Source binding.** [source-binding.json](receipts/source-binding.json.txt) holds the head, tree, hdl/sw/configs/tb/scripts/avdecc/syn subtree hashes, gitlinks and the submodule heads, before and after.
Each input file the project scripts name or include, the memory images, the constraints, the generated configuration tree, the configuration YAML and the linked ELF are hashed before synthesis, and re-read after
synthesis and after the last route with the identity unchanged ([1x1](receipts/inputs-endstation_ax7101_1x1_tdm8.json.txt), [8x8](receipts/inputs-endstation_ax7101_8x8.json.txt): 161 and 165 files). The two processor ROM images the generated netlist loads were
regenerated by the export and their hashes equal the recorded digests for the pinned processor (`syn/yosys/rom_digests.tsv`, 801ef228), before and after ([start](receipts/generated-hex.start.txt.txt), [end](receipts/generated-hex.end.txt.txt)).
Post-optimization checkpoint SHA256: 1x1 `937c97a442e8791cca86ec5c4e1b7243215c4a596588a371ec0794a67dd56bea`, 8x8 `8547aeb92d608c655ed2406071f2f59aa8ab45c092a7fcb3b1ddf8243cac5755`.
Every other route output, published or not, is hashed in [route-outputs-sha256.json](receipts/route-outputs-sha256.json.txt). All four corner timing reports of all six routes are published in full, split below 190 KB.

## R910-4-F2 MINOR - corrected above and in HANDOFF-r8.md and PR-BODY.md

## Reviewed head, not merge candidate

These are the reviewed head's routes. The PR body says so. If a manager merge moves dev-soft-core past 5de21ff3 before this PR merges, the merge candidate re-routes both shapes.
The issue's routing acceptance is satisfied for 09201d35 and must be re-established for any later composition.

## No documentation commit

No design page states route figures for the enabled shapes: the design page gives the rule, and the figures live in the PR body and receipts. So no page changed and the head stays 09201d35.
Residue R909-5-R1 and R909-6-R1 and the open suggestions are unchanged and stay with the manager.

## Not run and not claimed

- No hosted acceptance, docs, firmware, suite, portability or local-replica evidence was added this round. Round 7's "Not run" list still stands.
- No bitstream, hardware or bench run. Implementation timing is not hardware proof.
- The disabled release-top netlist comparison was not repeated (no source changed since round 7). The disabled utilization table in the PR body is the earlier measurement.
- The 8x8 enabled image stays S14 debt, refused by the ordinary allocator.

Every figure and report: [receipts/INDEX.md](receipts/INDEX.md). Closure labels are the author's dispositions; each finding is cleared only by its reviewer.
