[A789]

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

PENDING — `923-aecp-maps` -> the split train's base, on #901's review head `16ba667d`.

## Linked Issue / roles

Closes #923
Closes #924
Relates to #665

Executor: `[A789]`
Internal cleared-context reviewer: to be assigned
External reviewer: to be assigned

## Description

**#923: the split image's audio map edits reach the datapath's render map store.** Until now the firmware's AECP
owner held the maps alone; no firmware wrote the mailbox's `EDIT` window, so the render map kept its boot image and
the format verdict read it (#665 issuecomment-6904803181, finding 15).

| Piece | Change |
|---|---|
| `aecp.h`, `aecp_maps.c` | a new optional port, `edit`, the integrator's map store. An ADD or REMOVE_AUDIO_MAPPINGS the core accepts reaches it before the core's map moves: one transaction of the mappings that change the map, each once, in command order. A refusal there is the command's answer, and nothing changes (all or none, Milan v1.2 5.4.2.27, 5.4.2.28). A command the core refuses, or one that changes nothing, reaches no store. |
| `aecp_face.c`, `mbx.c` | the face's `edit`: the release processor's transaction on interface 0's `EDIT` window: begin, validate each record, begin the commit, commit each, finish. A refused begin answers NOT_SUPPORTED, a refused record or commit-begin BAD_ARGUMENTS, and no answer before the commit is reserved ENTITY_MISBEHAVING; each aborts. After an accepted commit-begin nothing refuses. `EDIT_REQ` is written once a transaction (`mbx_win_ask`). A begin with no answer is asked once more, because the store's edit face waits for the boot sweep. |
| `aecp_maps.c`, `ctrl_app_aecp.c` | `aecp_restore_commit`, called by `ctrl_app_open_aecp` after the acknowledged publication of the restore's terminal and before AECP opens. Every moved port's reset set (as the restored formats clip it) is removed, then each restored set is added. A port the store refuses keeps what the store holds. |
| `aecp_mbx.c`, `ctrl_app_aecp.c` | the port forwarded through both composition layers, NULL where the environment has none |

**#924:**

| Piece | Change |
|---|---|
| `aecp_commands.c` | SET_CONFIGURATION with an index at or past configurations_count answers NO_SUCH_DESCRIPTOR with the index in force (IEEE 1722.1-2021 7.4.7.1, Table 7-141), as the fabric processor does |
| `aecp_commands.c` | SET_STREAM_INFO takes the 48-octet IEEE 1722.1-2013 body (fields ending at stream_vlan_id), with the 2021 body's refusals in the same order, and answers in the 84-octet 2021 form; a body of 49 to 83 octets is still refused |

**Tests and harnesses:**

- 14 new GoogleTest cases in `test_aecp.cpp` (Core, Face with a model of the datapath's transaction server behind the `EDIT` window, AppStore), and 31 planted defects in the AECP campaign, each caught by its named test on its words.
- `make -C tb/verilator/milan_dp twin-maps` runs the platform firmware on `tb_split_top` and reads the render store `amap_in_store_r` (`twin_probes.vlt`, read only; no RTL change). An edited map reaches the store, and GET_AUDIO_MAP agrees after every command. A narrowing SET_STREAM_FORMAT answers BAD_ARGUMENTS with the mappings in place, and 1, 2, 4 and 6 channels answer SUCCESS once they are removed. A saved map, restored at the next boot, reaches the store. `twin-maps-plants` plants #923's defect (the edit port cut) and requires its checks to fail by name.
- The CPU budget harness's SoC answers the `EDIT` window at the contract's bound with every beat accepted (`split_soc.slowest_edit`), so an edit's record is measured with the longest wait the contract allows.

## Authoritative references

- Milan v1.2 5.4.2.7, 5.4.2.27, 5.4.2.28, 5.3.10.1; IEEE 1722.1-2021 7.4.7.1, 7.4.15.1, 7.4.45, 7.4.46, Table 7-141; IEEE 1722.1-2013 7.4.15 (the 48-octet body)
- [`docs/reference/MAILBOX_CONTRACT.md`](../docs/reference/MAILBOX_CONTRACT.md), the face block's `EDIT` window (unchanged)
- [`docs/design/MAILBOX_SPLIT.md`](../docs/design/MAILBOX_SPLIT.md), the open item on the audio maps, now closed
- #665 issuecomment-6904803181 (findings 15 to 17) and issuecomment-6904832963; protocol-processor PR #183

## How to get into the same state

```sh
git fetch origin && git checkout 923-aecp-maps
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4..3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
make -C tb/verilator/milan_dp twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <dir> --record-budget-findings --record-share-findings
```

Expected result / pass criteria: (pending)

## Known limitations / out of scope

- SET_STREAM_INFO with a body longer than 84 octets is still taken, as before; the fabric processor refuses it. That is outside #924's two findings and is recorded for a decision.
- `twin-maps` is a target of its own, outside the milan_dp suite's `run` inventory, as `twin` and `srptx` are.
- The bench acceptance of #923 and #924 is the gating run's.

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
