[A295]

Closes #508

Status: the complete assigned local gate set passed at
`6a9828c172aa4d5d8ee49725e357a10bae2caa52`; independent review pending.

The product now serves each Stream Input's actual probing status, ACMP status,
MSRP failure code and 64-bit bridge ID from the processor's state owners.
The parent removes its old selector-7 approximation and selector-5 zero.
Real controller responses cover both sinks, notifications, reset, withdrawal,
and the missing-descriptor case. Seven negative controls detect field loss,
the wrong sink and restoration of the old approximation.

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
All 65 gate commands returned zero at the final commit, from clean generated
outputs. The default datapath sweep completed all 36 commands; notification
checks passed 345/345 and all seven negative controls were detected. The shadow
suite passed 371/371 checks, rendering passed both integration legs and all five
control/defect checks, and persistence co-simulation passed 465/465 checks with
39/39 mutations detected. All 54 synthesis tops and 344 behavior scenarios
passed, as did the source, documentation, contract, naming and evidence checks.

The complete builder passed both with the pinned compiler and with no cross
compiler. Historical resource calibration was unrun in both modes because its
placement report is absent; the compiled census was also unrun in the
compiler-absent mode. No assertion, allowance or ratchet was weakened.

The existing acceptance wording says PASSIVE after bind. The adopted processor
contract and recorded round-1 evidence instead show ACTIVE immediately on bind
and PASSIVE after an unanswered retry. The state oracle is unchanged in this
round; independent review should retain that distinction.

Completion: integration documentation and generated ROM digests are updated.
Independent reviews and hosted candidate checks remain pending.
