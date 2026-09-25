[A297]

Closes #508

Status: the complete round-3 assigned local gate set passed at
`224ec0e9a9fa129924bf8f0433cf70b4140f7bd2`; delta reviews pending.

The product now serves each Stream Input's actual probing status, ACMP status,
MSRP failure code and 64-bit bridge ID from the processor's state owners.
The parent removes its old selector-7 approximation and selector-5 zero.
Real controller responses cover both sinks, notifications, reset, withdrawal,
and the missing-descriptor case. Eight negative controls detect field loss,
the wrong sink, restoration of the old approximation, and a duplicated
withdrawal notification.

The processor pin advances from `09f9bf38` to
`990f96526bb89356c963a260ebbdcf2a77e6623a` and adopts:

| Processor issue | Processor PR | Change |
|---|---|---|
| [92](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/92), [93](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/93) | [109](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/109) | Saved-binding restore and bounded boot walk |
| [94](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/94) | [110](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/110) | Descriptor-memory guard |
| [43](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/43), [49](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/49) | [111](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/111) | Processor-owned input status and failure fields |
| [112](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/112) | [114](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/114) | Admission grants reflect the current declaration |
| [116](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/116) | [117](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/117) | Parent-gate fixes without behavior or port changes |
| [113](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/113) | [115](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/115) | Latency-only GET_STREAM_INFO notifications |

The parent notify/[GSI] checks drive no isolated latency-only refresh.
G5 observes the coalesced registration, failure and latency event; G6 keeps
latency unchanged. Their expectations remain unchanged. Isolated latency
notification coverage belongs to the processor's response tests.

Reproduction and validation: the datapath suite README documents the response
phases and field lineage; SUBMODULES records the adoption boundaries.
Round 2 at `6a9828c172aa4d5d8ee49725e357a10bae2caa52` recorded
all 65 gate commands returning zero, from clean generated outputs.
The default datapath sweep completed all 36 commands; notification
checks passed 345/345 and all seven negative controls were detected. The shadow
suite passed 371/371 checks, rendering passed both integration legs and all five
control/defect checks, and persistence co-simulation passed 465/465 checks with
39/39 mutations detected. All 54 synthesis tops and 344 behavior scenarios
passed, as did the source, documentation, contract, naming and evidence checks.

Round 2 also passed the complete builder with and without the pinned cross
compiler. Historical resource calibration was unrun in both modes because its
placement report is absent; the compiled census was also unrun in the
compiler-absent mode. No assertion, allowance or ratchet was weakened.

The [acceptance-2 decision](https://github.com/kebag-logic/milan-fpga/issues/508#issuecomment-5825732419)
records ACTIVE with ACMP status zero immediately on bind, then PASSIVE
after an unanswered retry with no discovered talker. G1 and G3 grade
that order. The state oracle remains unchanged.

## Round 3

The historical #530 changelog section matches dev `c266432d` byte for byte.
The #116/#113 entries remain only in the `990f9652` section.
All nine processor citation spans resolve at `990f9652` to their named
constructs, with their source text checked against the earlier references.

G8 now requires exactly two GET_STREAM_INFO pushes per controller:
registrar withdrawal, then settlement teardown to PASSIVE. Both responses
carry PASSIVE, zero ACMP status, and cleared failure fields because the
response reads live state. Each response to each controller is graded,
including body equality with the solicited answer; sink 1 stays quiet.
The README and banner state the count and explain both causes.
A processor-copy mutant replays the withdrawal after 4096 cycles and fails
both named G8 count checks.

Final-head validation: the clean notification leg passes 380/380 checks;
all eight mutants fail their named checks, with 9/9 campaign controls passing.
The duplicate fails both G8 counts with three pushes instead of two.
The complete default datapath sweep and shadow suite pass; the latter grades
371/371 checks. Both documentation inventory modes and every assigned source,
contract, naming, evidence, formatting and path gate return zero. The HDL
frontend retains its four recorded findings, with no budget change. Citation
and historical-changelog proofs also pass. The head remains local and unpushed.

Completion: integration documentation and generated ROM digests are updated.
Independent reviews and hosted candidate checks remain pending.
