[A654]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED (STOP). No change is proposed. `190-crf-maxframesize` -> `dev` is still at e9cbb676 with no commits. This body is kept for the record only, and no PR is to be opened from it.

## Linked Issue / roles

Relates to Mister-M-alt/protocol-processor-control-plane-avb-milan#190

Executor: `[A654]`
Internal cleared-context reviewer: not assigned (lane stopped)
External reviewer: not assigned (lane stopped)

## Description

The CRF Stream Output declares MaxFrameSize 217. That is the 8-channel AAF value from Milan v1.2 Table 4.4, `tctx_maxf_w[0]` at `hdl/milan/milan_datapath.sv:5641` and `:8201`. The correct CRF value is **29**: the Table 4.4 row "CRF, 1 ts/pdu" specifies it, and the DUT's own 28-octet CRF AVTPDU (IEEE 1722-2016 10.4.1 header of 20 octets plus one 8-octet timestamp) plus the Table 4.4 extra octet derives it. The two values agree.

The parent cannot declare it, though. The processor's `cfg_tspec_max_frame_i` (`protocol-processor/hdl/top/protocol_processor_top.sv:300`) is one scalar, and at `:2700` every source's engine-driven declaration captures it. A per-source value therefore needs a processor interface change, followed by pin adoption here. A maintainer has to decide that before this lane can deliver.

## Authoritative references

- Milan v1.2 4.3.3.2, Table 4.4 and its notes (CRF, 1 ts/pdu: MaxFrameSize 28 + 1, 5632 kbps)
- Milan v1.2 7.3.2 and Table 7.1 (timestamps_per_pdu 1, timestamp_interval 96, base_frequency 48000)
- IEEE 1722-2016 10.4.1, 10.4.11, 10.4.13 (CRF header fields, crf_data_length, crf_data)
- IEEE 802.1Q-2018 35.2.2.8.4 (MaxFrameSize: the largest frame the talker produces)

## How to get into the same state

```sh
git fetch origin
git switch -c 190-crf-maxframesize e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f
git submodule update --init protocol-processor
```

## How to validate

```sh
git grep -n "cfg_tspec_max_frame_i" -- hdl/milan/milan_datapath.sv hdl/milan/KL_pp_shadow.sv
git -C protocol-processor grep -n "cfg_tspec_max_frame_i" -- hdl/top/protocol_processor_top.sv
```

Expected result / pass criteria: the parent passes one scalar, `tctx_maxf_w[0]`, and the processor captures that same scalar for every source's engine-driven DECLARE_TALKER. This confirms the blocker.

## Known limitations / out of scope

- The processor interface change (a per-source TSpec MaxFrameSize) belongs to the processor repository and needs a recorded decision.
- The stale comment at `hdl/ieee1722/crf/KL_crf_tx.sv:206-211` names a deleted `CRF_SRP_MAXF_C` of 42. It should be corrected in the lane that wires the CRF value.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done
