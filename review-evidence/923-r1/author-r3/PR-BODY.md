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

GREEN except the timing floor owed to #927 — `923-aecp-maps` -> `dev-soft-core`, on #901's review head `16ba667d`; head `d06ded5a`.

Round 3 answers R848-1 (issuecomment-6928957357) and R847-1 (issuecomment-6929792570): the late-reply store model and its agreement checks (R848-1 F1); the face's record selection through the `EDIT` window (R847-1 F1); the platform guide's ROM figure (both F2); the ledger comment's lane label (R848-1 F3, R847-1 R1). The firmware is unchanged since `70c100da`, so the platform images at 1x1/1if and 8x8/1if and the release image are byte-identical to `70c100da`'s by hash, and its routes, CPU budget harness and 4-shard sweep (65 suites, 2,713,040 checks, 0 failures) carry. At `d06ded5a` the workflow jobs of `rtl-fast.yml`, `elaborate.yml` and `docs.yml` ran step by step on clean clones: 118 steps rc 0, 130 not run with their reasons, 0 bad: among them the AECP (331 of 331), SRP (421 of 421) and control (716 of 716) campaigns, `fw_coverage.py --check` (PASS, 39 files), the docs jobs, the publication census and `ctrl_boundary.py`. 8x8/1if meets the timing floor on all three of S9's directives. 1x1/1if misses the hold floor on the TDM render FIFO crossing, as its base does: owed to #927 by the ruling on the round-2 STOP (#923 issuecomment-6923091710).

## Linked Issue / roles

Closes #923
Closes #924
Relates to #665

Executor: `[A789]`
Internal cleared-context reviewer: `[R847]` (R847-1 NEGATIVE at `70c100da`: F1, F2 MINOR, R1 residue; answered at `d06ded5a`)
External reviewer: `[R848]` (R848-1 NEGATIVE at `70c100da`: F1, F2 MINOR, F3 residue; answered at `d06ded5a`)

## Description

**#923: the split image's audio map edits reach the datapath's render map store.** Before this change the firmware's AECP owner held the maps alone. No firmware wrote the mailbox's `EDIT` window, so the render map kept its boot image and the format verdict read it (#665 issuecomment-6904803181, finding 15).

| Piece | Change |
|---|---|
| `aecp.h`, `aecp_maps.c` | A new optional port, `edit`: the integrator's map store. An ADD or REMOVE_AUDIO_MAPPINGS the core accepts reaches it before the core's map moves. It is one transaction of the mappings that change the map, each once, in command order. A refusal there is the command's answer, and nothing changes (all or none, Milan v1.2 5.4.2.27, 5.4.2.28). A command the core refuses, or one that changes nothing, reaches no store. |
| `aecp_face.c`, `mbx.c` | The face's `edit` runs the release processor's transaction on interface 0's `EDIT` window: begin, validate each record, begin the commit, commit each, finish. A refused begin answers NOT_SUPPORTED, a refused record or commit-begin BAD_ARGUMENTS, and no answer before the commit is reserved ENTITY_MISBEHAVING; each aborts. After an accepted commit-begin nothing refuses. `EDIT_REQ` is written once a transaction (`mbx_win_ask`). A begin with no answer is asked once more, because the store's edit face waits for the boot sweep. |
| `aecp_maps.c`, `ctrl_app_aecp.c` | `aecp_restore_commit`, called by `ctrl_app_open_aecp` after the acknowledged publication of the restore's terminal and before AECP opens. Every moved port's reset set, as the restored formats clip it, is removed; then each restored set is added. A port the store refuses keeps what the store holds. |
| `aecp_mbx.c`, `ctrl_app_aecp.c` | The port is forwarded through both composition layers, NULL where the environment has none. |

**#924:**

| Piece | Change |
|---|---|
| `aecp_commands.c` | SET_CONFIGURATION with an index at or past configurations_count answers NO_SUCH_DESCRIPTOR with the index in force (IEEE 1722.1-2021 7.4.7.1, Table 7-141), as the fabric processor does. |
| `aecp_commands.c` | SET_STREAM_INFO takes the 48-octet IEEE 1722.1-2013 body (fields ending at stream_vlan_id), with the 2021 body's refusals in the same order, and answers in the 84-octet 2021 form. A body of 49 to 83 octets is still refused. |

**The control memory (#923's ruling (A), issuecomment-6906679024):**

| Piece | Change |
|---|---|
| `sw/litex/ctrl_memory.py` | A product ledger entry `platform-8x8-one-interface` at the 8x8/1if platform image's measured 56.5 RAMB36, debt of half a tile (1,280 B of rom) owed to the cold-code-to-flash work (#665 decision D3). The two 8x8/2if entries go to their measured 59.5 (size fixture) and 61.0 (platform, `ctrl_plat` 20,416 B). |
| `sw/litex/ctrl_memory.py`, `milan_soc.py` | `own_point`: the product SoC build plans a ledgered image at its own entry, matched by every one of its symbols. Every other image stays at the 56-RAMB36 budget. |
| `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, `plat_ledger.py`, fit page sections 3 and 5 | The ledger tests and the platform ledger gate follow the entries. Each image is refused half a tile past its entry, and an unledgered 8x8 image is refused at 56.5. |

**Tests and harnesses:**

- 17 new GoogleTest cases in `test_aecp.cpp` (Core; Face, with a model of the datapath's transaction server behind the `EDIT` window; AppStore). 32 planted defects in the AECP campaign, each caught by its named test on its words. Branch coverage of every changed firmware file is 100 % (`coverage.ratchet`).
- The store model follows the release engine's transaction contract (`KL_aecp_engine.sv`: an accepted commit-begin reserves the transaction, and each record's commit and the finish complete without back-pressure). A begin, validation or commit-begin with no answer is held and not taken; a commit or finish with no answer is taken and only its reply is lost. `Face.ALostReplyAfterTheReservedCommitLeavesTheStoreAndTheMapAgreeing` and `Face.ALostReplyInTheRestoresCommitLeavesTheStoreAndTheMapAgreeing` lose the first or second record's commit reply in a two-record ADD and REMOVE and in the restore's removal and addition, and hold GET_AUDIO_MAP to the store after each, as `Face.AnUnansweredEditFailsUntilItsCommitIsReserved` now does after its post-commit cases. A face that stops committing at a lost reply (`window-lost-reply-stops-the-commit`) is caught by both, and round 2's model, which dropped the write with the reply, fails all three. Delivery loss after the commit-begin is outside the contract and has no recovery here (`sw/firmware/ctrl/aecp/README.md`).
- `Face.AnEditCommitsTheMappingsTheCorePicksAndNoOthers` sends, through the face and the `EDIT` window, an ADD of a held and a new mapping and a REMOVE naming a mapping twice: the store validates and commits the mappings the core picked and no others, and GET_AUDIO_MAP agrees with it. A face that reads the command's first records in place of the picked ones (`window-pick-ignored`) is caught by name.
- `make -C tb/verilator/milan_dp twin-maps` runs the platform firmware on `tb_split_top` and reads the render store `amap_in_store_r` (`twin_probes.vlt`, read only; no RTL change).
  - An edited map reaches the store, and GET_AUDIO_MAP agrees after every command.
  - A narrowing SET_STREAM_FORMAT answers BAD_ARGUMENTS with the mappings in place, and 1, 2, 4 and 6 channels answer SUCCESS once they are removed.
  - A saved map, restored at the next boot, reaches the store.
  - `twin-maps-plants` plants #923's defect (the edit port cut) and requires its checks to fail by name.
- The CPU budget harness's SoC answers the `EDIT` window at the contract's bound with every beat accepted (`split_soc.slowest_edit`). So an edit's record is measured with the longest wait the contract allows. Its verdicts are a constant on the port: at two interfaces a per-slice comb assignment had left them 0. Its 8x8 two-interface plan takes the SoC build's `ledgered=` and plans the harness's named point in its place.

**Costs** (CPU cycles, `16ba667d` -> head, the same legs; section 13, "The map edits' commit (#923)"):

| Point | Record | Base | Head | By the rule | Stated |
|---|---|---:|---:|---:|---:|
| 1x1/1if | one-row edit, arm B | 23,877 | 27,866 | 295 us | 300 (class); member 260 -> 295 |
| 1x1/1if | largest legal command, arm B | 86,698 | 92,714 | 975 us | 975 |
| 8x8/2if | one-row edit, arm B | 28,627 | 33,481 | 355 us | 595 (class); member 325 -> 355 |
| 8x8/2if | largest legal command, arm B | 126,152 | 132,751 | 1,395 us | 1,650 |

No statement the tier model reads moves, so every row, the load, the pace and the slice stand.

## Authoritative references

- Milan v1.2 5.4.2.7, 5.4.2.27, 5.4.2.28, 5.3.10.1; IEEE 1722.1-2021 7.4.7.1, 7.4.15.1, 7.4.45, 7.4.46, Table 7-141; IEEE 1722.1-2013 7.4.15 (the 48-octet body)
- [`docs/reference/MAILBOX_CONTRACT.md`](../docs/reference/MAILBOX_CONTRACT.md), the face block's `EDIT` window (unchanged)
- [`docs/design/MAILBOX_SPLIT.md`](../docs/design/MAILBOX_SPLIT.md), the open item on the audio maps, now closed
- [`docs/design/SPLIT_CONTROL_MEMORY.md`](../docs/design/SPLIT_CONTROL_MEMORY.md) sections 3, 5 and 13
- #665 issuecomment-6904803181 (findings 15 to 17) and issuecomment-6904832963; #923 issuecomment-6906679024 (the ruling); protocol-processor PR #183

## How to get into the same state

```sh
git fetch origin && git checkout 923-aecp-maps
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4..3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --self-test
make -C tb/verilator/milan_dp twin-maps twin-maps-plants
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <dir> --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <dir> --variant answering-ports --groups aecp-fanout,aecp-largest-notice --record-budget-findings --record-share-findings
```

Expected result / pass criteria:
- the workflow jobs of `rtl-fast.yml`, `elaborate.yml` and `docs.yml`, step by step on a clean clone: every `run:` step rc 0 or not run with its reason
- `scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0..3: exit 0 each
- the firmware shards: `RESULT: PASS` each; the AECP campaign catches every planted defect (331); `fw_coverage.py --check`: `firmware coverage: PASS (39 files)`
- `test_ctrl_memory`: `0 failure(s)`; `plat_ledger.py --self-test`: `plat_ledger: PASS`
- `twin-maps`: 20 checks PASS (`maps: 0 failed`); `twin-maps-plants`: the no-edit plant fails its store, format and edit checks by name
- the CPU budget harness at 1x1: 0 refusals, budget misses only the seven `backlog-owed` held-egress rows (the base's), 0 passes over the share; `record_classes.py` over every leg: `RESULT: PASS`
- at 8x8 (two interfaces), answering-ports: every map edit answered SUCCESS with its notices, the one-row edit 355 us and the largest legal command 1,395 us by the rule, within 595 and 1,650

## Known limitations / out of scope

- SET_STREAM_INFO with a body longer than 84 octets is still taken, as before; the fabric processor refuses it. That is #926's.
- `twin-maps` is a target of its own, outside the milan_dp suite's `run` inventory, as `twin` and `srptx` are.
- The 8x8/1if image's half tile and the 8x8/2if entries are debt owed to the cold-code-to-flash work by the ruling; no compaction is in this PR.
- The `EDIT` window's late cases are those the release engine's contract allows (a reply lost after a taken commit or finish); delivery loss after the commit-begin would need a recovery contract no issue defines.
- The 1x1/1if split image misses WHS >= +0.030 ns on all three directives (+0.015 / +0.014 / +0.014) on the datapath's TDM render FIFO crossing (`chan_tdm_render/bank_r` into `u_fcdc/mem_r` DIADI, 0 levels), as its base does (+0.014): recorded as misses at the base, owed to #927. The export differs from the base's only in the control memory.
- The 8x8/1if harness point is reported, not held: the shape's costs past 1x1/1if's statements print STATED there, as at the base.
- The 2 KiB rom bank the control-memory plan counts as a RAMB18 is placed as a RAMB36 at 1x1/1if (81 -> 82 tiles of 135); the plan's accounting is not this PR's.
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
